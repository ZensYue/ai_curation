from __future__ import annotations

import logging
from dataclasses import asdict
from pathlib import Path
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

from .auth import AuthProfileStore
from .fetcher import FetchResponse, HttpFetcher
from .models import CrawlError, CrawlRequest, CrawlResult, utc_now_iso
from .parser import detect_fallback_reason, enrich_from_detail_html, parse_list_page
from .storage import ArtifactStore


LOGGER = logging.getLogger(__name__)


class KpCrawlService:
    def __init__(
        self,
        *,
        fetcher: HttpFetcher | None = None,
        artifact_store: ArtifactStore | None = None,
        auth_store: AuthProfileStore | None = None,
    ) -> None:
        self.fetcher = fetcher or HttpFetcher()
        self.artifact_store = artifact_store or ArtifactStore()
        self.auth_store = auth_store or AuthProfileStore()

    def crawl(self, request: CrawlRequest) -> CrawlResult:
        started_at = utc_now_iso()
        artifacts = self.artifact_store.create_job("kp")
        self.artifact_store.write_json(artifacts.request_file, asdict(request))

        errors: list[CrawlError] = []
        items = []
        auth_used = False
        strategy = "http"
        fallback_required = False

        try:
            auth = self.auth_store.get(request.auth_profile)
            auth_used = auth is not None
        except (FileNotFoundError, KeyError) as exc:
            errors.append(
                CrawlError(
                    stage="auth",
                    message=str(exc),
                    retryable=False,
                )
            )
            auth = None

        total_pages_fetched = 0
        detail_pages_fetched = 0

        for page_number in range(1, request.page_limit + 1):
            page_url = build_page_url(request.seed_url, page_number)
            try:
                response = self.fetcher.fetch_text(page_url, auth)
            except Exception as exc:  # noqa: BLE001
                errors.append(
                    CrawlError(
                        stage="list_fetch",
                        url=page_url,
                        message=str(exc),
                        retryable=True,
                    )
                )
                fallback_required = True
                break

            total_pages_fetched += 1
            raw_ref = self._save_fetch_response(
                artifacts, f"list_page_{page_number}", response
            )

            reason = detect_fallback_reason(response.body_text)
            if reason:
                errors.append(
                    CrawlError(
                        stage="strategy",
                        url=page_url,
                        message=reason,
                        retryable=True,
                    )
                )
                fallback_required = True
                break

            page_items = parse_list_page(
                response.body_text,
                base_url=page_url,
                category_name=request.category_name,
                scraped_at=started_at,
            )

            if not page_items:
                errors.append(
                    CrawlError(
                        stage="parse_list",
                        url=page_url,
                        message="no items parsed from list page",
                        retryable=True,
                    )
                )
                fallback_required = True
                snapshot = self.artifact_store.attach_raw_html(
                    artifacts, f"list_page_{page_number}_snapshot", response.body_text
                )
                LOGGER.warning("saved fallback snapshot to %s", snapshot)
                break

            for item in page_items:
                item.raw_payload_ref = raw_ref

            items.extend(page_items)

        if request.include_detail and items:
            for index, item in enumerate(items, start=1):
                try:
                    response = self.fetcher.fetch_text(item.source_url, auth)
                except Exception as exc:  # noqa: BLE001
                    errors.append(
                        CrawlError(
                            stage="detail_fetch",
                            url=item.source_url,
                            item_ref=item.listing_id or item.source_url,
                            message=str(exc),
                            retryable=True,
                        )
                    )
                    continue

                detail_pages_fetched += 1
                raw_ref = self._save_fetch_response(
                    artifacts, f"detail_{index}", response
                )
                enriched = enrich_from_detail_html(item, response.body_text)
                enriched.raw_payload_ref = raw_ref
                items[index - 1] = enriched

        ended_at = utc_now_iso()
        job_meta = {
            "site": "kp",
            "seed_url": request.seed_url,
            "category_name": request.category_name,
            "page_limit": request.page_limit,
            "include_detail": request.include_detail,
            "auth_profile": request.auth_profile,
            "auth_used": auth_used,
            "strategy": strategy,
            "browser_fallback_required": fallback_required,
            "browser_fallback_reason": (
                errors[-1].message if fallback_required and errors else None
            ),
            "started_at": started_at,
            "ended_at": ended_at,
            "total_pages_fetched": total_pages_fetched,
            "detail_pages_fetched": detail_pages_fetched,
            "items_returned": len(items),
            "error_count": len(errors),
        }
        result = CrawlResult(
            job_meta=job_meta,
            items=items,
            errors=errors,
            artifacts=artifacts,
        )
        self.artifact_store.finalize(artifacts, result.to_dict())
        return result

    def _save_fetch_response(
        self, artifacts, name: str, response: FetchResponse
    ) -> str:
        record = {
            "url": response.url,
            "status_code": response.status_code,
            "headers": response.headers,
            "elapsed_ms": response.elapsed_ms,
            "body_preview": response.body_text[:2000],
        }
        self.artifact_store.attach_raw_html(artifacts, name, response.body_text)
        return self.artifact_store.attach_raw_json(artifacts, name, record)


def build_page_url(seed_url: str, page_number: int) -> str:
    if page_number <= 1:
        return seed_url
    parsed = urlparse(seed_url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["page"] = str(page_number)
    return urlunparse(parsed._replace(query=urlencode(query)))
