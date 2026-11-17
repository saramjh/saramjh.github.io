"""Bilingual GREENUS resource-listing context, backed by the original page."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "_data/recognitions.yml"
SRC = "https://greenus.upb.ro/share.php?t=t_35802c3c02e2be7201"
POSTS = {
    "ko": ROOT / "_posts/folio-koreaves-resources-ko/2026-11-02-folio-koreaves-resources-ko.md",
    "en": ROOT / "_posts/folio-koreaves-resources-en/2026-11-02-folio-koreaves-resources-en.md",
}

class GreenusResourceContext(unittest.TestCase):
    def test_exact_original_entry_has_native_bilingual_case_context(self):
        text = EVIDENCE.read_text("utf-8")
        entry = re.search(r"(?ms)^- id: greenus-koreaves-community-tool\n(.*?)(?=^- id: |\Z)", text)
        self.assertIsNotNone(entry)
        block = entry.group(1)
        self.assertIn(f'url: "{SRC}"', block)
        self.assertIn('type: listing', block)
        self.assertIn('case_ko: "/koreaves-external-resources-ko/"', block)
        self.assertIn('case_en: "/koreaves-external-resources-en/"', block)
        self.assertNotIn('date:', block)

    def test_articles_explain_training_value_and_link_correct_gis_not_stale_external_path(self):
        for lang, filename in POSTS.items():
            with self.subTest(lang=lang):
                t = filename.read_text("utf-8")
                self.assertIn("greenus-koreaves-community-tool", t)
                self.assertIn(SRC, t)
                self.assertIn("https://koreaves.com/gis/", t)
                self.assertIn("modified: 2026-11-18", t)
                self.assertIn("last_modified_at: 2026-11-18", t)
                self.assertNotIn("https://koreaves.com/explorer/", t)
                self.assertNotIn("\ufffd", t)
                self.assertNotIn("????", t)

    def test_nine_listing_count_and_existing_pairs_remain(self):
        ko, en = (POSTS[l].read_text("utf-8") for l in ("ko", "en"))
        self.assertIn("아홉 가지", ko)
        self.assertIn("Nine public", en)
        self.assertIn("alternate_url: /koreaves-external-resources-en/", ko)
        self.assertIn("alternate_url: /koreaves-external-resources-ko/", en)
        self.assertIn("GBIF Literature", ko)
        self.assertIn("GBIF Literature", en)

if __name__ == "__main__":
    unittest.main()
