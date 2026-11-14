"""Regression coverage for developer GA4 scope clarification.

This test reads only the two author-owned analytics articles.
It never accesses Google Analytics, another product repository or the network.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "ko": ROOT / "_posts/gh-pages-analytics-notes-3-decision-kr/2026-09-20-gh-pages-analytics-notes-3-decision-kr.md",
    "en": ROOT / "_posts/gh-pages-analytics-notes-3-decision-en/2026-09-20-gh-pages-analytics-notes-3-decision-en.md",
}

class OriginalBlogGa4ScopeCorrectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = {lang: path.read_text(encoding="utf-8") for lang, path in PAGES.items()}

    def test_shared_hostname_not_equivalent_to_per_tool_reporting(self):
        self.assertIn("hostName만으로는 같은 호스트의 도구들을 분리할 수 없습니다", self.text["ko"])
        self.assertIn("hostName alone cannot separate tools sharing that hostname", self.text["en"])
        self.assertIn("pagePath", self.text["ko"])
        self.assertIn("pagePath", self.text["en"])

    def test_real_counterexample_and_limits_in_both_languages(self):
        for lang, text in self.text.items():
            with self.subTest(lang=lang):
                self.assertIn("2026-11-15", text)
                self.assertIn("streamName=blog", text)
                self.assertIn("/richChecker/", text)
                self.assertIn("app_entry", text)
                self.assertIn("core_warmup_complete", text)
                self.assertIn("m.search.naver.com / referral", text)
                self.assertIn("/scratchLottery/", text)
                self.assertIn("https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema", text)

    def test_missing_event_rows_not_equal_to_zero_real_usage(self):
        self.assertIn("실제 사용자가 없었다는 의미는 아닙니다", self.text["ko"])
        self.assertIn("does not establish zero actual use", self.text["en"])

    def test_original_public_urls_stable(self):
        self.assertIn("permalink: /gh-pages-analytics-notes-3-decision-kr/", self.text["ko"])
        self.assertIn("permalink: /gh-pages-analytics-notes-3-decision-en/", self.text["en"])

if __name__ == "__main__":
    unittest.main()
