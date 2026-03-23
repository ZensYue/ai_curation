from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest import TestCase

from kp_crawler.auth import AuthProfileStore
from kp_crawler.http_api import KpCrawlerApplication
from kp_crawler.service import KpCrawlService
from kp_crawler.storage import ArtifactStore

from test_service import FakeFetcher


class HttpApiTests(TestCase):
    def test_application_handle_crawl_returns_items(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            service = KpCrawlService(
                fetcher=FakeFetcher(),
                artifact_store=ArtifactStore(data_root=Path(tmp)),
                auth_store=AuthProfileStore(auth_file=Path(tmp) / "missing.json"),
            )
            app = KpCrawlerApplication(service=service)
            status, body = app.handle_crawl(
                {
                    "seed_url": "https://www.kupujemprodajem.com/mobilni-telefoni",
                    "category_name": "手机",
                    "page_limit": 1,
                    "include_detail": True,
                }
            )
            self.assertEqual(200, int(status))
            self.assertEqual(2, len(body["items"]))

    def test_application_rejects_bad_request(self) -> None:
        app = KpCrawlerApplication()
        status, body = app.handle_crawl({"page_limit": "x"})
        self.assertEqual(400, int(status))
        self.assertIn("error", body)
