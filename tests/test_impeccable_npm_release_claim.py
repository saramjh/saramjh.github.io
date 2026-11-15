"""Source-bound Impeccable npm version annotation, preserving historical CI tests."""
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
POSTS={
    lang:ROOT/f"_posts/{slug}"/f"2026-10-05-{slug}.md"
    for lang,slug in (
        ("en","en-impeccable-review-ai-ui-design"),
        ("ko","impeccable-review-ai-ui-design"),
    )
}
OFFICIAL="https://www.npmjs.com/package/impeccable"
HISTORICAL="impeccable@4.1.0 detect app storefront extensions/profit-scratch-widget"

class ImpeccableNpmVersionSourceTest(unittest.TestCase):
    def test_source_and_check_date_in_both_editions(self):
        for lang,path in POSTS.items():
            data=path.read_text(encoding="utf8")
            self.assertGreaterEqual(data.count(OFFICIAL),1,lang)
            self.assertIn("last_modified_at: 2026-11-16",data)
            self.assertIn("4.9.1",data)
            self.assertIn("62",data)

    def test_preserve_exact_historical_ci_pin(self):
        for lang,path in POSTS.items():
            data=path.read_text(encoding="utf8")
            self.assertEqual(data.count(HISTORICAL),1,lang)
            self.assertIn("4.1.0",data)

    def test_no_stale_rule_count_or_unverified_retest_claim(self):
        en=POSTS["en"].read_text(encoding="utf8")
        ko=POSTS["ko"].read_text(encoding="utf8")
        self.assertNotIn("61 deterministic rules",en)
        self.assertNotIn("61개의 deterministic rule",ko)
        self.assertIn("I have not rerun that project with 4.9.1.",en)
        self.assertIn("4.9.1에서 다시 검사한 결과는 아닙니다.",ko)

    def test_reciprocal_language_metadata_and_existing_media(self):
        en=POSTS["en"].read_text(encoding="utf8")
        ko=POSTS["ko"].read_text(encoding="utf8")
        self.assertIn("alternate_url: /impeccable-review-ai-ui-design/",en)
        self.assertIn("alternate_url: /en-impeccable-review-ai-ui-design/",ko)
        for lang,data in (("en",en),("ko",ko)):
            self.assertIn("impeccable-review-og.png",data,lang)
            self.assertNotIn("\ufffd",data,lang)

if __name__=="__main__":
    unittest.main()
