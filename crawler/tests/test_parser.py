from __future__ import annotations

from pathlib import Path
from unittest import TestCase

from kp_crawler.parser import enrich_from_detail_html, parse_list_page


FIXTURES = Path(__file__).parent / "fixtures"


class ParserTests(TestCase):
    def test_parse_list_page_from_json_ld(self) -> None:
        html = (FIXTURES / "kp_list.html").read_text(encoding="utf-8")
        items = parse_list_page(
            html,
            base_url="https://www.kupujemprodajem.com/mobilni-telefoni",
            category_name="手机",
            scraped_at="2026-03-23T00:00:00+00:00",
        )
        self.assertEqual(2, len(items))
        self.assertEqual("Apple iPhone 15 Pro 256GB", items[0].title)
        self.assertEqual("145000", items[0].price_raw)
        self.assertEqual("RSD", items[0].currency)
        self.assertEqual("123456789", items[0].listing_id)
        self.assertEqual(1, items[0].rank_in_page)

    def test_enrich_from_detail_html(self) -> None:
        list_html = (FIXTURES / "kp_list.html").read_text(encoding="utf-8")
        detail_html = (FIXTURES / "kp_detail.html").read_text(encoding="utf-8")
        item = parse_list_page(
            list_html,
            base_url="https://www.kupujemprodajem.com/mobilni-telefoni",
            category_name="手机",
            scraped_at="2026-03-23T00:00:00+00:00",
        )[0]
        enriched = enrich_from_detail_html(item, detail_html)
        self.assertEqual("Tech Store Belgrade", enriched.seller_name)
        self.assertEqual(1234, enriched.view_count)
        self.assertEqual(98, enriched.favorite_count)
        self.assertEqual("2026-03-20T09:00:00+01:00", enriched.posted_at_raw)
