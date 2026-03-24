from __future__ import annotations

import json
from pathlib import Path
from unittest import TestCase

from kp_crawler.storage import ArtifactStore
from support import managed_tempdir


class StorageTests(TestCase):
    def test_create_and_finalize_job(self) -> None:
        with managed_tempdir("test_create_and_finalize_job") as tmp:
            store = ArtifactStore(data_root=Path(tmp))
            artifacts = store.create_job("kp")
            store.write_json(artifacts.request_file, {"seed_url": "https://example.com"})
            raw = store.attach_raw_json(artifacts, "list_page_1", {"ok": True})
            result = store.finalize(artifacts, {"items": []})

            self.assertTrue(Path(artifacts.job_dir).exists())
            self.assertTrue(Path(raw).exists())
            self.assertTrue(Path(result).exists())
            payload = json.loads(Path(result).read_text(encoding="utf-8"))
            self.assertEqual([], payload["items"])
