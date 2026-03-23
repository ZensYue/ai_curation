from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .auth import AuthProfile


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


@dataclass(slots=True)
class FetchResponse:
    url: str
    status_code: int
    headers: dict[str, str]
    body_text: str
    elapsed_ms: int

    def as_record(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "status_code": self.status_code,
            "headers": self.headers,
            "elapsed_ms": self.elapsed_ms,
            "body_text": self.body_text,
        }


class HttpFetcher:
    def __init__(self, timeout_seconds: int = 20, retry_count: int = 1) -> None:
        self.timeout_seconds = timeout_seconds
        self.retry_count = retry_count

    def fetch_text(self, url: str, auth: AuthProfile | None = None) -> FetchResponse:
        last_error: Exception | None = None
        for attempt in range(self.retry_count + 1):
            try:
                return self._fetch_once(url, auth)
            except (HTTPError, URLError, TimeoutError) as exc:
                last_error = exc
                if attempt >= self.retry_count:
                    raise
                time.sleep(0.4 * (attempt + 1))
        assert last_error is not None
        raise last_error

    def _fetch_once(self, url: str, auth: AuthProfile | None) -> FetchResponse:
        headers = dict(DEFAULT_HEADERS)
        if auth:
            headers.update(auth.headers)
            cookie_header = auth.cookie_header()
            if cookie_header:
                headers["Cookie"] = cookie_header

        request = Request(url=url, headers=headers, method="GET")
        started = time.monotonic()
        with urlopen(request, timeout=self.timeout_seconds) as response:
            body = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            text = body.decode(charset, errors="replace")
            elapsed_ms = int((time.monotonic() - started) * 1000)
            return FetchResponse(
                url=url,
                status_code=getattr(response, "status", response.getcode()),
                headers={key: value for key, value in response.headers.items()},
                body_text=text,
                elapsed_ms=elapsed_ms,
            )


def compact_json_text(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
