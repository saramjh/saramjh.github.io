"""Exact externally observed WLI resource link and existing bilingual case coverage."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LEDGER = (ROOT / "_data/recognitions.yml").read_text(encoding="utf8")
ID = "wli-migratory-birds-koreaves"
URL = "https://wli.wwt.org.uk/resources/priority-theme-resources/migratory-birds/"
POSTS = {
    lang: ROOT / f"_posts/folio-koreaves-resources-{lang}" /
          f"2026-11-02-folio-koreaves-resources-{lang}.md"
    for lang in ("en", "ko")
}


class WliMigratoryResourceEvidenceTest(unittest.TestCase):
    def test_exact_single_confirmed_listing_and_no_invented_publication_date(self):
        match = re.search(rf"(?ms)^- id: {re.escape(ID)}\n(.*?)(?=^- id: |\Z)", LEDGER)
        self.assertIsNotNone(match)
        block = match.group(1)
        self.assertEqual(LEDGER.count("- id: " + ID + "\n"), 1)
        self.assertIn("project: koreaves", block)
        self.assertIn("type: listing", block)
        self.assertIn("status: confirmed", block)
        self.assertIn('source: "Wetland Link International"', block)
        self.assertIn(f'url: "{URL}"', block)
        self.assertIn('verified_at: "2026-11-16"', block)
        self.assertNotIn("\n  date:", block)
        self.assertIn("not WLI membership, partnership, endorsement or measured use", block)

    def test_original_wli_page_source_is_linked_in_each_language(self):
        for lang, page in POSTS.items():
            text = page.read_text(encoding="utf8")
            self.assertEqual(text.count(URL), 1, lang)
            self.assertIn(ID, text)
            self.assertIn("modified: 2026-11-22", text)
            self.assertIn("last_modified_at: 2026-11-22", text)
            self.assertNotIn("\ufffd", text)
            self.assertNotIn("????", text)
            self.assertIn("https://koreaves.com/", text)

    def test_ten_distinct_listings_preserve_the_older_ones(self):
        ko = POSTS["ko"].read_text(encoding="utf8")
        en = POSTS["en"].read_text(encoding="utf8")
        self.assertIn("외부에서 확인되는 열 가지 연결", ko)
        self.assertIn("Ten public source pages", en)
        self.assertIn("WLI 회원 자격이나 기관의 공식 제휴", ko)
        self.assertIn("not WLI membership, a partnership", en)
        for record_id in (
            "beary-resource", "nzbirds-resource", "greenus-koreaves-community-tool",
            "kantorilode-koreaves-legacy-links", "gbif-literature"
        ):
            self.assertIn(record_id, ko)
            self.assertIn(record_id, en)

    def test_original_reciprocal_navigation_and_evidence_source_constraints(self):
        self.assertIn("alternate_url: /koreaves-external-resources-en/", POSTS["ko"].read_text("utf8"))
        self.assertIn("alternate_url: /koreaves-external-resources-ko/", POSTS["en"].read_text("utf8"))
        for lang in ("ko", "en"):
            self.assertIn(
                f'case_{lang}: "/koreaves-external-resources-{lang}/"',
                re.search(rf"(?ms)^- id: {re.escape(ID)}\n(.*?)(?=^- id: |\Z)", LEDGER).group(1)
            )
        self.assertEqual(LEDGER.count(URL), 1)


if __name__ == "__main__":
    unittest.main()
