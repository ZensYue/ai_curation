from __future__ import annotations

import json
import re
from dataclasses import replace
from html import unescape
from typing import Any
from urllib.parse import urljoin

from .models import CrawlItem


SCRIPT_JSON_RE = re.compile(
    r"<script[^>]+type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>",
    re.IGNORECASE | re.DOTALL,
)
TAG_RE = re.compile(r"<[^>]+>")


def strip_tags(value: str | None) -> str | None:
    if value is None:
        return None
    text = TAG_RE.sub(" ", value)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip() or None


def parse_int(value: str | None) -> int | None:
    if not value:
        return None
    digits = re.sub(r"[^\d]", "", value)
    return int(digits) if digits else None


def detect_fallback_reason(html: str) -> str | None:
    lowered = html.lower()
    if "captcha" in lowered or "cloudflare" in lowered:
        return "anti-bot challenge detected"
    if "enable javascript" in lowered:
        return "javascript-required page detected"
    return None


def extract_json_ld_blocks(html: str) -> list[Any]:
    blocks: list[Any] = []
    for raw in SCRIPT_JSON_RE.findall(html):
        raw = raw.strip()
        if not raw:
            continue
        try:
            blocks.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return blocks


def parse_list_page(
    html: str,
    *,
    base_url: str,
    category_name: str,
    scraped_at: str,
) -> list[CrawlItem]:
    blocks = extract_json_ld_blocks(html)
    items = _items_from_json_ld(blocks, base_url, category_name, scraped_at)
    if items:
        return items
    return _items_from_generic_html(html, base_url, category_name, scraped_at)


def enrich_from_detail_html(item: CrawlItem, html: str) -> CrawlItem:
    seller_name = _match_named_group(
        html,
        [
            r'data-seller-name=["\'](?P<value>[^"\']+)["\']',
            r'"sellerName"\s*:\s*"(?P<value>[^"]+)"',
            r'Prodavac[:\s]*</[^>]+>\s*<[^>]+>(?P<value>[^<]+)<',
        ],
    )
    view_count = parse_int(
        _match_named_group(
            html,
            [
                r'data-view-count=["\'](?P<value>[^"\']+)["\']',
                r'"viewCount"\s*:\s*"?(?P<value>[\d\.\s]+)"?',
                r'Pregleda[:\s]*</[^>]+>\s*<[^>]+>(?P<value>[^<]+)<',
            ],
        )
    )
    favorite_count = parse_int(
        _match_named_group(
            html,
            [
                r'data-favorite-count=["\'](?P<value>[^"\']+)["\']',
                r'"favoriteCount"\s*:\s*"?(?P<value>[\d\.\s]+)"?',
                r'Omiljeni[:\s]*</[^>]+>\s*<[^>]+>(?P<value>[^<]+)<',
            ],
        )
    )
    posted_at = _match_named_group(
        html,
        [
            r'data-posted-at=["\'](?P<value>[^"\']+)["\']',
            r'"postedAt"\s*:\s*"(?P<value>[^"]+)"',
            r'Objavljen[:\s]*</[^>]+>\s*<[^>]+>(?P<value>[^<]+)<',
        ],
    )
    return replace(
        item,
        seller_name=seller_name or item.seller_name,
        view_count=view_count if view_count is not None else item.view_count,
        favorite_count=(
            favorite_count if favorite_count is not None else item.favorite_count
        ),
        posted_at_raw=posted_at or item.posted_at_raw,
    )


def _items_from_json_ld(
    blocks: list[Any],
    base_url: str,
    category_name: str,
    scraped_at: str,
) -> list[CrawlItem]:
    results: list[CrawlItem] = []
    for block in blocks:
        if isinstance(block, dict) and block.get("@type") == "ItemList":
            item_list = block.get("itemListElement", [])
            for index, entry in enumerate(item_list, start=1):
                candidate = entry.get("item", entry) if isinstance(entry, dict) else {}
                if not isinstance(candidate, dict):
                    continue
                url = candidate.get("url") or entry.get("url")
                title = candidate.get("name")
                image = candidate.get("image")
                offers = candidate.get("offers", {})
                price = None
                currency = None
                if isinstance(offers, dict):
                    price = str(offers.get("price")) if offers.get("price") else None
                    currency = (
                        str(offers.get("priceCurrency"))
                        if offers.get("priceCurrency")
                        else None
                    )
                if not url or not title:
                    continue
                results.append(
                    CrawlItem(
                        source_url=urljoin(base_url, str(url)),
                        title=str(title).strip(),
                        price_raw=price,
                        currency=currency,
                        image_urls=_normalize_images(image, base_url),
                        category_raw=category_name,
                        rank_in_page=index,
                        listing_id=_extract_listing_id(str(url)),
                        scraped_at=scraped_at,
                    )
                )
    return results


def _items_from_generic_html(
    html: str,
    base_url: str,
    category_name: str,
    scraped_at: str,
) -> list[CrawlItem]:
    pattern = re.compile(
        r'<article[^>]*class=["\'][^"\']*ad-item[^"\']*["\'][^>]*>'
        r'(?P<body>.*?)</article>',
        re.IGNORECASE | re.DOTALL,
    )
    results: list[CrawlItem] = []
    for index, match in enumerate(pattern.finditer(html), start=1):
        body = match.group("body")
        url = _match_named_group(
            body,
            [
                r'<a[^>]+href=["\'](?P<value>[^"\']+)["\'][^>]*class=["\'][^"\']*ad-link',
                r'data-href=["\'](?P<value>[^"\']+)["\']',
            ],
        )
        title = strip_tags(
            _match_named_group(
                body,
                [
                    r'<h2[^>]*>(?P<value>.*?)</h2>',
                    r'<a[^>]+class=["\'][^"\']*ad-link[^"\']*["\'][^>]*>(?P<value>.*?)</a>',
                ],
            )
        )
        price_raw = strip_tags(
            _match_named_group(
                body,
                [
                    r'<span[^>]+class=["\'][^"\']*price[^"\']*["\'][^>]*>(?P<value>.*?)</span>',
                    r'data-price=["\'](?P<value>[^"\']+)["\']',
                ],
            )
        )
        image = _match_named_group(
            body,
            [
                r'<img[^>]+src=["\'](?P<value>[^"\']+)["\']',
                r'data-image=["\'](?P<value>[^"\']+)["\']',
            ],
        )
        if not url or not title:
            continue
        results.append(
            CrawlItem(
                source_url=urljoin(base_url, url),
                title=title,
                price_raw=price_raw,
                currency=_detect_currency(price_raw),
                image_urls=_normalize_images(image, base_url),
                category_raw=category_name,
                rank_in_page=index,
                listing_id=_extract_listing_id(url),
                scraped_at=scraped_at,
            )
        )
    return results


def _normalize_images(image: Any, base_url: str) -> list[str]:
    if image is None:
        return []
    if isinstance(image, list):
        values = image
    else:
        values = [image]
    return [urljoin(base_url, str(value)) for value in values if value]


def _extract_listing_id(url: str) -> str | None:
    match = re.search(r"/(\d{3,})[-/]", url)
    if match:
        return match.group(1)
    match = re.search(r"[?&]id=(\d+)", url)
    if match:
        return match.group(1)
    return None


def _match_named_group(html: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if match:
            value = strip_tags(match.group("value"))
            if value:
                return value
    return None


def _detect_currency(price_raw: str | None) -> str | None:
    if not price_raw:
        return None
    lowered = price_raw.lower()
    if "rsd" in lowered or "дин" in lowered:
        return "RSD"
    if "eur" in lowered or "€" in lowered:
        return "EUR"
    return None
