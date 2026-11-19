"""Keep the GA4, Search Console and Clarity guidance distinct in the bilingual series."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PARTS = {
    ("1", "en"): ("_posts/gh-pages-analytics-notes-1-problem-en/2026-09-18-gh-pages-analytics-notes-1-problem-en.md", "en", "/gh-pages-analytics-notes-1-problem-en/"),
    ("1", "ko"): ("_posts/gh-pages-analytics-notes-1-problem-kr/2026-09-18-gh-pages-analytics-notes-1-problem-kr.md", "ko", "/gh-pages-analytics-notes-1-problem-kr/"),
    ("2", "en"): ("_posts/gh-pages-analytics-notes-2-reasoning-en/2026-09-19-gh-pages-analytics-notes-2-reasoning-en.md", "en", "/gh-pages-analytics-notes-2-reasoning-en/"),
    ("2", "ko"): ("_posts/gh-pages-analytics-notes-2-reasoning-kr/2026-09-19-gh-pages-analytics-notes-2-reasoning-kr.md", "ko", "/gh-pages-analytics-notes-2-reasoning-kr/"),
    ("3", "en"): ("_posts/gh-pages-analytics-notes-3-decision-en/2026-09-20-gh-pages-analytics-notes-3-decision-en.md", "en", "/gh-pages-analytics-notes-3-decision-en/"),
    ("3", "ko"): ("_posts/gh-pages-analytics-notes-3-decision-kr/2026-09-20-gh-pages-analytics-notes-3-decision-kr.md", "ko", "/gh-pages-analytics-notes-3-decision-kr/"),
}
GA4 = "https://support.google.com/analytics/answer/9679158?hl=en"
GA4_CROSS = "https://support.google.com/analytics/answer/10071811?hl=en"
CLARITY = "https://learn.microsoft.com/en-us/clarity/faq/"
GSC = "https://support.google.com/webmasters/answer/34592?hl=en"
VERIFY = "https://support.google.com/webmasters/answer/9008080?hl=en"
CLARITY_SETUP = "https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-setup"
SUBDOMAIN_FAQ = "https://developers.google.com/search/help/crawling-index-faq?hl=en"
CRAWL_BUDGET = "https://developers.google.com/crawling/docs/crawl-budget?hl=en"
CRAWL_MYTHS = "https://developers.google.com/crawling/docs/myths-about-crawling"
LINKS = "https://developers.google.com/search/docs/crawling-indexing/links-crawlable"
RANKING = "https://developers.google.com/search/docs/appearance/ranking-systems-guide"
DOMAIN_AGE = "https://www.youtube.com/watch?v=-pnpg00FWJY"


class AnalyticsToolBoundaryTests(unittest.TestCase):
    def load(self, part, lang):
        return (ROOT / PARTS[(part, lang)][0]).read_text(encoding="utf8")

    def test_part_one_teaser_describes_property_types_not_only_domain_verification(self):
        for lang in ("en", "ko"):
            with self.subTest(lang=lang):
                text = self.load("1", lang)
                self.assertIn("URL-prefix", text)
                self.assertIn("Domain", text)
                self.assertNotIn("verification works at the domain level", text)
                self.assertNotIn("도메인 단위 검증", text)

    def test_part_two_distinguishes_each_tools_actual_boundary(self):
        for lang in ("en", "ko"):
            with self.subTest(lang=lang):
                text = self.load("2", lang)
                for url in (GA4, GA4_CROSS, CLARITY, GSC, VERIFY, CLARITY_SETUP,
                            SUBDOMAIN_FAQ, CRAWL_BUDGET, CRAWL_MYTHS, LINKS, RANKING, DOMAIN_AGE):
                    self.assertIn(url, text)
                self.assertIn("URL-prefix", text)
                self.assertIn("DNS", text)
                self.assertNotIn("Across all three tools, the same shape", text)
                self.assertNotIn("세 도구 모두에서 반복해서 나온 구조", text)
                self.assertNotIn("Verify / create at the broadest reasonable unit", text)
                self.assertNotIn("도메인 전체)에서 검증/속성을 만들고", text)
                if lang == "en":
                    for phrase in ("logical user base", "one web stream per property", "same tag ID", "same web stream", "different domains", "heatmaps", "Domain property",
                                   "no indexing or ranking preference", "unique hostname", "crawling itself is not a ranking signal",
                                   "does not establish a blanket trust score", "not proof of shared ranking trust"):
                        self.assertIn(phrase, text)
                    self.assertNotIn("Google's own recommendation for organizations", text)
                    self.assertNotIn("can be followed as a single journey within the same property", text)
                    self.assertNotIn("domain age accumulate at the domain level", text)
                else:
                    for phrase in ("논리적 사용자 집단", "속성당 웹 스트림 하나", "같은 태그 ID", "같은 웹 스트림", "도메인이 다른 사이트", "히트맵", "도메인 속성",
                                   "어느 쪽도 선호하지 않는다고", "고유 호스트 이름", "크롤링 자체는 순위 신호가 아니며",
                                   "순위 신뢰를 자동으로 공유한다는 증거는 아닙니다"):
                        self.assertIn(phrase, text)
                    self.assertNotIn("하나의 속성 + 여러 데이터 스트림", text)
                    self.assertNotIn("같은 속성 안에서 하나의 사용자 여정으로 이어볼 수 있습니다", text)
                    self.assertNotIn("도메인 나이 같은 신호는 도메인 단위로 누적됩니다", text)

    def test_part_three_marks_multi_stream_setup_as_historical_reporting_choice(self):
        for lang in ("en", "ko"):
            with self.subTest(lang=lang):
                text = self.load("3", lang)
                self.assertIn("G-4DYFKSNFBG", text)
                self.assertIn("streamName=blog", text)
                self.assertIn("2026-11-20", text)
                self.assertIn(GA4, text)
                self.assertIn(GA4_CROSS, text)
                if lang == "en":
                    for phrase in ("reporting choice", "not a general GA4 recommendation",
                                   "does not automatically join users across streams",
                                   "one web stream per property", "same tag ID"):
                        self.assertIn(phrase, text)
                    old_claim = "representing the " + chr(96) + "saramjh.github.io" + chr(96) + " domain"
                    self.assertNotIn(old_claim, text)
                else:
                    for phrase in ("보고 목적에 따른 제 설정", "일반 권장안은 아닙니다",
                                   "자동으로 연결되지는 않습니다",
                                   "속성당 웹 스트림 하나", "같은 웹 스트림의 같은 태그 ID"):
                        self.assertIn(phrase, text)
                    self.assertNotIn("도메인을 대표하는 하나의 GA4 속성", text)

    def test_original_bilingual_metadata_and_unicode_remain_intact(self):
        for (part, lang), (relative, expected_lang, permalink) in PARTS.items():
            with self.subTest(part=part, lang=lang):
                text = (ROOT / relative).read_text(encoding="utf8")
                self.assertIn("lang: " + expected_lang, text)
                self.assertIn("alternate_lang: " + ("ko" if lang == "en" else "en"), text)
                self.assertIn("permalink: " + permalink, text)
                self.assertNotIn("\ufffd", text)
                self.assertNotRegex(text, r"\?{5,}")
                if lang == "ko":
                    self.assertRegex(text, r"[가-힣]")


if __name__ == "__main__":
    unittest.main()
