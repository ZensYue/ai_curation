from __future__ import annotations

import json
from pathlib import Path
from unittest import TestCase

from kp_crawler.auth import AuthProfileStore
from support import managed_tempdir


class AuthTests(TestCase):
    def test_load_auth_profile(self) -> None:
        with managed_tempdir("test_load_auth_profile") as tmp:
            auth_file = Path(tmp) / "auth_profiles.json"
            auth_file.write_text(
                json.dumps(
                    {
                        "profiles": {
                            "kp-default": {
                                "headers": {"x-kp-test": "1"},
                                "cookies": {"sessionid": "abc123"},
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            store = AuthProfileStore(auth_file=auth_file)
            profile = store.get("kp-default")
            assert profile is not None
            self.assertEqual("1", profile.headers["x-kp-test"])
            self.assertIn("sessionid=abc123", profile.cookie_header() or "")
