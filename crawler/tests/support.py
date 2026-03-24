from __future__ import annotations

import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4


@contextmanager
def managed_tempdir(label: str):
    artifacts_root = os.environ.get("KP_CRAWLER_TEST_ARTIFACTS_ROOT")
    if artifacts_root:
        base_dir = Path(artifacts_root).expanduser().resolve()
        path = base_dir / f"{label}_{uuid4().hex[:8]}"
        path.mkdir(parents=True, exist_ok=True)
        yield str(path)
        return

    with tempfile.TemporaryDirectory() as tmp:
        yield tmp
