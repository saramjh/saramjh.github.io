"""First-party source and no-overclaim regression for the two EDS Book case studies."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
URL = "https://github.com/saramjh/bird-records-not-absence-notebook/pull/2"
POSTS = (
    ROOT / "_posts/eds-book-bird-occurrence-notebook-preparation-ko/2026-11-14-eds-book-bird-occurrence-notebook-preparation-ko.md",
    ROOT / "_posts/eds-book-bird-occurrence-notebook-preparation-en/2026-11-14-eds-book-bird-occurrence-notebook-preparation-en.md",
)

class EDSGBIFIntegritySourceTest(unittest.TestCase):
    def test_original_merged_pr_link_in_both_editions(self):
        for path in POSTS:
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count(URL), 1, path.name)

    def test_actual_error_modes_and_test_result_preserved(self):
        for path in POSTS:
            text = path.read_text(encoding="utf-8")
            self.assertIn("DwC-A", text, path.name)
            self.assertIn("csv.DictReader", text, path.name)
            self.assertIn("81", text, path.name)

    def test_existing_pilot_and_data_source_limits_still_present(self):
        for path in POSTS:
            text = path.read_text(encoding="utf-8")
            self.assertIn("100", text, path.name)
            self.assertIn("1,000", text, path.name)
            self.assertIn("GBIF", text, path.name)
            self.assertIn("DOI", text, path.name)

    def test_bilingual_metadata_and_existing_pr1_source_survive(self):
        for path in POSTS:
            text = path.read_text(encoding="utf-8")
            self.assertIn("alternate_url:", text, path.name)
            self.assertIn("https://github.com/saramjh/bird-records-not-absence-notebook/pull/1", text, path.name)

if __name__ == "__main__":
    unittest.main()
