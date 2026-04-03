from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Smoke test the local KP crawler HTTP API."
    )
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8080",
        help="Base URL of the local crawler service.",
    )
    parser.add_argument(
        "--seed-url",
        required=True,
        help="KP category page URL to crawl.",
    )
    parser.add_argument(
        "--category-name",
        default="手机",
        help="Category label passed to the crawler service.",
    )
    parser.add_argument(
        "--page-limit",
        type=int,
        default=1,
        help="How many list pages to fetch.",
    )
    parser.add_argument(
        "--include-detail",
        action="store_true",
        help="Whether to fetch detail pages for enrichment.",
    )
    parser.add_argument(
        "--auth-profile",
        default=None,
        help="Optional auth profile name.",
    )
    parser.add_argument(
        "--save-json",
        default=None,
        help="Optional path to save the full response JSON.",
    )
    return parser.parse_args()


def http_json(method: str, url: str, payload: dict | None = None) -> tuple[int, dict]:
    body = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(url=url, data=body, headers=headers, method=method)
    with urlopen(request, timeout=60) as response:
        status = getattr(response, "status", response.getcode())
        text = response.read().decode("utf-8")
        return status, json.loads(text)


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")

    try:
        health_status, health_body = http_json("GET", f"{base_url}/healthz")
    except (HTTPError, URLError, TimeoutError) as exc:
        print(f"[FAIL] health check request failed: {exc}", file=sys.stderr)
        return 1

    print(f"[OK] GET /healthz -> {health_status} {health_body}")
    if health_status != 200:
        print("[FAIL] health check did not return 200", file=sys.stderr)
        return 1

    payload = {
        "seed_url": args.seed_url,
        "category_name": args.category_name,
        "page_limit": args.page_limit,
        "include_detail": args.include_detail,
    }
    if args.auth_profile:
        payload["auth_profile"] = args.auth_profile

    try:
        status, body = http_json("POST", f"{base_url}/jobs/kp/crawl", payload)
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        print(
            f"[FAIL] crawl request returned HTTP {exc.code}: {error_body}",
            file=sys.stderr,
        )
        return 1
    except (URLError, TimeoutError) as exc:
        print(f"[FAIL] crawl request failed: {exc}", file=sys.stderr)
        return 1

    print(f"[OK] POST /jobs/kp/crawl -> {status}")
    job_meta = body.get("job_meta", {})
    items = body.get("items", [])
    errors = body.get("errors", [])
    artifacts = body.get("artifacts", {})

    print("job_meta:")
    print(json.dumps(job_meta, ensure_ascii=False, indent=2))
    print(f"items_returned: {len(items)}")
    print(f"errors: {len(errors)}")
    if artifacts.get("job_dir"):
        print(f"job_dir: {artifacts['job_dir']}")

    if items:
        print("first_item:")
        print(json.dumps(items[0], ensure_ascii=False, indent=2))

    if errors:
        print("errors_detail:")
        print(json.dumps(errors, ensure_ascii=False, indent=2))

    save_path = args.save_json
    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"saved_response: {path}")

    if status != 200:
        print("[FAIL] crawl request did not return 200", file=sys.stderr)
        return 1

    print("[DONE] Smoke test finished.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
