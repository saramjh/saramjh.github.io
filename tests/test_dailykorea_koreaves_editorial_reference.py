"""Source-bound bilingual third-party editorial reference regression."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
URL="https://dailykorea.net/ko/travel/suncheon-bay-first-birdwatching/"
POSTS={lang:ROOT/f"_posts/folio-koreaves-resources-{lang}"/f"2026-11-02-folio-koreaves-resources-{lang}.md" for lang in ("ko","en")}

class DailyKoreaKoreAvesEditorialReferenceTest(unittest.TestCase):
    def test_exact_original_editorial_url_and_existing_locale_metadata(self):
        for lang,path in POSTS.items():
            text=path.read_text(encoding="utf8")
            self.assertEqual(text.count(URL),1,lang)
            self.assertIn("alternate_url:",text)
            self.assertIn("modified: 2026-11-18",text)
            self.assertIn("2026",text)

    def test_exact_first_party_resource_links_in_both_languages(self):
        for path in POSTS.values():
            text=path.read_text(encoding="utf8")
            self.assertIn("https://koreaves.com/gis/",text)
            self.assertIn("https://koreaves.com/guide/",text)
            self.assertIn("Daily Korea Editorial",text)

    def test_not_owner_byline_or_independent_directory_record(self):
        ledger=(ROOT/"_data/recognitions.yml").read_text(encoding="utf8")
        self.assertNotIn(URL,ledger)
        self.assertIn("내 역할은 지도 해석에 대한 사실 검토였고",POSTS["ko"].read_text(encoding="utf8"))
        self.assertIn("My contribution was a fact-check of the map interpretation",POSTS["en"].read_text(encoding="utf8"))

    def test_previous_listing_evidence_and_unicode_intact(self):
        for path in POSTS.values():
            text=path.read_text(encoding="utf8")
            self.assertIn("kantorilode-koreaves-legacy-links",text)
            self.assertIn("https://kantorilode.com/links.html",text)
            self.assertNotIn("\ufffd",text)
            self.assertNotIn("????",text)

if __name__=="__main__":
    unittest.main()
