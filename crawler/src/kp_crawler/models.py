from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(slots=True)
class CrawlRequest:
    seed_url: str
    category_name: str
    page_limit: int = 1
    include_detail: bool = True
    auth_profile: str | None = None

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "CrawlRequest":
        seed_url = str(payload.get("seed_url", "")).strip()
        category_name = str(payload.get("category_name", "")).strip()
        if not seed_url:
            raise ValueError("seed_url is required")
        if not category_name:
            raise ValueError("category_name is required")

        page_limit_raw = payload.get("page_limit", 1)
        try:
            page_limit = int(page_limit_raw)
        except (TypeError, ValueError) as exc:
            raise ValueError("page_limit must be an integer") from exc
        if page_limit < 1 or page_limit > 20:
            raise ValueError("page_limit must be between 1 and 20")

        include_detail = payload.get("include_detail", True)
        if not isinstance(include_detail, bool):
            raise ValueError("include_detail must be a boolean")

        auth_profile = payload.get("auth_profile")
        if auth_profile is not None:
            auth_profile = str(auth_profile).strip() or None

        return cls(
            seed_url=seed_url,
            category_name=category_name,
            page_limit=page_limit,
            include_detail=include_detail,
            auth_profile=auth_profile,
        )


@dataclass(slots=True)
class CrawlError:
    stage: str
    message: str
    url: str | None = None
    item_ref: str | None = None
    retryable: bool = False


@dataclass(slots=True)
class CrawlItem:
    source_url: str
    title: str
    price_raw: str | None
    currency: str | None
    image_urls: list[str]
    category_raw: str | None
    rank_in_page: int | None
    listing_id: str | None
    seller_name: str | None = None
    view_count: int | None = None
    favorite_count: int | None = None
    posted_at_raw: str | None = None
    scraped_at: str = field(default_factory=utc_now_iso)
    raw_payload_ref: str | None = None


@dataclass(slots=True)
class CrawlArtifacts:
    job_dir: str
    request_file: str
    result_file: str | None = None
    raw_files: list[str] = field(default_factory=list)


@dataclass(slots=True)
class CrawlResult:
    job_meta: dict[str, Any]
    items: list[CrawlItem]
    errors: list[CrawlError]
    artifacts: CrawlArtifacts

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_meta": self.job_meta,
            "items": [asdict(item) for item in self.items],
            "errors": [asdict(error) for error in self.errors],
            "artifacts": asdict(self.artifacts),
        }
