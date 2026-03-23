from __future__ import annotations

from dataclasses import dataclass
from http.cookies import SimpleCookie
from pathlib import Path

from .config import get_auth_file, load_json_file


@dataclass(slots=True)
class AuthProfile:
    name: str
    headers: dict[str, str]
    cookies: dict[str, str]

    def cookie_header(self) -> str | None:
        if not self.cookies:
            return None
        jar = SimpleCookie()
        for key, value in self.cookies.items():
            jar[key] = value
        return "; ".join(m.OutputString() for m in jar.values())


class AuthProfileStore:
    def __init__(self, auth_file: Path | None = None) -> None:
        self.auth_file = auth_file or get_auth_file()

    def get(self, profile_name: str | None) -> AuthProfile | None:
        if not profile_name:
            return None
        if not self.auth_file.exists():
            raise FileNotFoundError(
                f"auth profile file not found: {self.auth_file}"
            )
        payload = load_json_file(self.auth_file)
        profile = payload.get("profiles", {}).get(profile_name)
        if profile is None:
            raise KeyError(f"auth profile not found: {profile_name}")
        headers = {
            str(key): str(value)
            for key, value in dict(profile.get("headers", {})).items()
        }
        cookies = {
            str(key): str(value)
            for key, value in dict(profile.get("cookies", {})).items()
        }
        return AuthProfile(name=profile_name, headers=headers, cookies=cookies)
