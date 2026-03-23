from __future__ import annotations

import tempfile
from pathlib import Path
from unittest import TestCase

from kp_crawler.auth import AuthProfileStore
from kp_crawler.fetcher import FetchResponse
from kp_crawler.models import CrawlRequest
from kp_crawler.service import KpCrawlService
from kp_crawler.storage import ArtifactStore


FIXTURES = Path(__file__).parent / "fixtures"


class FakeFetcher:
    def __init__(self) -> None:
        self.list_html = (FIXTURES / "kp_list.html").read_text(encoding="utf-8")
        self.detail_html = (FIXTURES / "kp_detail.html").read_text(encoding="utf-8")

    def fetch_text(self, url: str, auth=None) -> FetchResponse:  # noqa: ANN001
        body = self.detail_html if "/oglasi/" in url else self.list_html
        return FetchResponse(
            url=url,
            status_code=200,
            headers={"content-type": "text/html"},
            body_text=body,
            elapsed_ms=12,
        )


class EmptyFetcher:
    def fetch_text(self, url: str, auth=None) -> FetchResponse:  # noqa: ANN001
        return FetchResponse(
            url=url,
            status_code=200,
            headers={"content-type": "text/html"},
            body_text="<html><body>empty</body></html>",
            elapsed_ms=12,
        )


class ServiceTests(TestCase):
    def test_crawl_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            service = KpCrawlService(
                fetcher=FakeFetcher(),
                artifact_store=ArtifactStore(data_root=Path(tmp)),
                auth_store=AuthProfileStore(auth_file=Path(tmp) / "missing.json"),
            )
            result = service.crawl(
                CrawlRequest(
                    seed_url="https://www.kupujemprodajem.com/mobilni-telefoni",
                    category_name="手机",
                    page_limit=1,
                    include_detail=True,
                )
            )
            self.assertFalse(result.job_meta["browser_fallback_required"])
            self.assertEqual(2, len(result.items))
            self.assertEqual(2, result.job_meta["detail_pages_fetched"])
            self.assertTrue(Path(result.artifacts.result_file or "").exists())

    def test_crawl_marks_browser_fallback_when_no_items_parsed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            service = KpCrawlService(
                fetcher=EmptyFetcher(),
                artifact_store=ArtifactStore(data_root=Path(tmp)),
                auth_store=AuthProfileStore(auth_file=Path(tmp) / "missing.json"),
            )
            result = service.crawl(
                CrawlRequest(
                    seed_url="https://www.kupujemprodajem.com/mobilni-telefoni",
                    category_name="手机",
                    page_limit=1,
                    include_detail=False,
                )
            )
            self.assertTrue(result.job_meta["browser_fallback_required"])
            self.assertEqual(1, len(result.errors))
