from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .config import get_data_root
from .models import CrawlArtifacts


class ArtifactStore:
    def __init__(self, data_root: Path | None = None) -> None:
        self.data_root = data_root or get_data_root()

    def create_job(self, site_name: str) -> CrawlArtifacts:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        job_id = uuid4().hex
        job_dir = self.data_root / site_name / today / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        request_file = job_dir / "request.json"
        return CrawlArtifacts(
            job_dir=str(job_dir),
            request_file=str(request_file),
            result_file=None,
            raw_files=[],
        )

    def write_json(self, file_path: str | Path, payload: object) -> str:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            json.dump(
                self._normalize(payload),
                fh,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        return str(path)

    def write_text(self, file_path: str | Path, content: str) -> str:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return str(path)

    def attach_raw_json(
        self, artifacts: CrawlArtifacts, name: str, payload: object
    ) -> str:
        path = Path(artifacts.job_dir) / f"{name}.json"
        written = self.write_json(path, payload)
        artifacts.raw_files.append(written)
        return written

    def attach_raw_html(
        self, artifacts: CrawlArtifacts, name: str, html: str
    ) -> str:
        path = Path(artifacts.job_dir) / "html" / f"{name}.html"
        written = self.write_text(path, html)
        artifacts.raw_files.append(written)
        return written

    def finalize(self, artifacts: CrawlArtifacts, result: object) -> str:
        path = Path(artifacts.job_dir) / "result.json"
        written = self.write_json(path, result)
        artifacts.result_file = written
        return written

    def _normalize(self, payload: object) -> object:
        if is_dataclass(payload):
            return asdict(payload)
        if isinstance(payload, list):
            return [self._normalize(item) for item in payload]
        if isinstance(payload, dict):
            return {str(key): self._normalize(value) for key, value in payload.items()}
        return payload
