"""Source-bound current GA4/GSC provider configuration checks in original bilingual notes."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    ("2","en"): "_posts/gh-pages-analytics-notes-2-reasoning-en/2026-09-19-gh-pages-analytics-notes-2-reasoning-en.md",
    ("2","ko"): "_posts/gh-pages-analytics-notes-2-reasoning-kr/2026-09-19-gh-pages-analytics-notes-2-reasoning-kr.md",
    ("3","en"): "_posts/gh-pages-analytics-notes-3-decision-en/2026-09-20-gh-pages-analytics-notes-3-decision-en.md",
    ("3","ko"): "_posts/gh-pages-analytics-notes-3-decision-kr/2026-09-20-gh-pages-analytics-notes-3-decision-kr.md",
    ("4","en"): "_posts/gh-pages-analytics-notes-4-open-en/2026-09-21-gh-pages-analytics-notes-4-open-en.md",
    ("4","ko"): "_posts/gh-pages-analytics-notes-4-open-kr/2026-09-21-gh-pages-analytics-notes-4-open-kr.md"
}
GA4_PROPERTY = "properties/456806471"
GA4_STREAM = "properties/456806471/dataStreams/8626988215"
MEASUREMENT = "G-4DYFKSNFBG"
GSC_PREFIX = "https://saramjh.github.io/"
GSC_DOMAIN = "sc-domain:saramjh.github.io"

class NativeAnalyticsInventory(unittest.TestCase):
    def read(self,part,lang):
        return (ROOT/FILES[(part,lang)]).read_text(encoding="utf-8")

    def test_current_ga4_stream_inventory_is_one_not_ten(self):
        for part in ("2","3","4"):
            for lang in ("en","ko"):
                with self.subTest(part=part,lang=lang):
                    body=self.read(part,lang)
                    for marker in (MEASUREMENT,"2026-11-20"):
                        self.assertIn(marker,body)
                    self.assertNotIn(GA4_PROPERTY,body)
                    self.assertNotIn(GA4_STREAM,body)
                    self.assertTrue(("one current web stream" in body) if lang=="en" else ("현재 웹 스트림은 1개" in body))
                    if part=="4":
                        self.assertNotIn("data streams go from around ten",body)
                        self.assertNotIn("데이터 스트림이 지금의 10개 안팎",body)

    def test_native_gsc_current_permission_is_distinct_from_september_history(self):
        for part in ("2","3","4"):
            for lang in ("en","ko"):
                with self.subTest(part=part,lang=lang):
                    body=self.read(part,lang)
                    for marker in (GSC_PREFIX,GSC_DOMAIN,"siteOwner","siteUnverifiedUser"):
                        self.assertIn(marker,body)
                    self.assertTrue(("September" in body) if lang=="en" else ("9월" in body))
                    self.assertTrue(("cannot reconstruct" in body or "cannot be reconstructed" in body or "cannot verify" in body) if lang=="en" else ("확인할 수 없" in body or "확인할 수는 없" in body or "재구성할 수 없" in body))

    def test_original_article_identity_and_unicode(self):
        for (part,lang), path in FILES.items():
            with self.subTest(part=part,lang=lang):
                body=(ROOT/path).read_text(encoding="utf-8")
                self.assertIn("lang: "+lang,body)
                self.assertIn("alternate_lang: "+("ko" if lang=="en" else "en"),body)
                self.assertIn("permalink: /gh-pages-analytics-notes-"+part,body)
                self.assertNotIn("\ufffd",body)
                self.assertNotIn("§",body)
                self.assertNotRegex(body,r"\?{5,}")
                if lang=="ko":self.assertRegex(body,r"[가-힣]")

    def test_original_ga4_september_and_november_measurement_records_retained(self):
        for lang in ("en","ko"):
            part3=self.read("3",lang)
            part4=self.read("4",lang)
            for marker in ("app_entry","core_warmup_complete","streamName=blog","m.search.naver.com / referral"):
                self.assertIn(marker,part3)
            for marker in ("672","651","127.0.0.1","localhost"):
                self.assertIn(marker,part4)

if __name__=="__main__":unittest.main()
