from __future__ import annotations

import json
import logging
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .models import CrawlRequest
from .service import KpCrawlService


LOGGER = logging.getLogger(__name__)


class KpCrawlerApplication:
    def __init__(self, service: KpCrawlService | None = None) -> None:
        self.service = service or KpCrawlService()

    def handle_crawl(self, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        try:
            request = CrawlRequest.from_payload(payload)
        except ValueError as exc:
            return HTTPStatus.BAD_REQUEST, {"error": str(exc)}

        try:
            result = self.service.crawl(request)
        except Exception as exc:  # noqa: BLE001
            LOGGER.exception("crawl failed")
            return HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)}
        return HTTPStatus.OK, result.to_dict()


class KpCrawlerHandler(BaseHTTPRequestHandler):
    server_version = "KpCrawler/0.1"

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/jobs/kp/crawl":
            self._write_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self._write_json(
                HTTPStatus.BAD_REQUEST,
                {"error": "request body must be valid JSON"},
            )
            return

        status, response = self.server.app.handle_crawl(payload)  # type: ignore[attr-defined]
        self._write_json(status, response)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/healthz":
            self._write_json(HTTPStatus.OK, {"status": "ok"})
            return
        self._write_json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def log_message(self, format: str, *args: object) -> None:
        LOGGER.info("%s - %s", self.address_string(), format % args)

    def _write_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server(host: str, port: int, service: KpCrawlService | None = None) -> None:
    app = KpCrawlerApplication(service=service)
    server = ThreadingHTTPServer((host, port), KpCrawlerHandler)
    server.app = app  # type: ignore[attr-defined]
    LOGGER.info("serving on http://%s:%s", host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        LOGGER.info("server interrupted")
    finally:
        server.server_close()
