"""Spoonie project case links to its verified external directory entry."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SpoonieDirectoryProjectCaseTest(unittest.TestCase):
    def test_first_party_project_case_has_original_and_bilingual_record(self):
        case = (ROOT / "_projects/spoonie.md").read_text(encoding="utf-8")
        self.assertIn("https://webapps.directory/directory/spooniespoonie", case)
        self.assertIn("October 25, 2026", case)
        self.assertIn("/spoonie-webapps-directory-en/", case)
        self.assertIn("/spoonie-webapps-directory-ko/", case)
        self.assertIn("Referral traffic and repeat use from the directory have not been measured.", case)
        self.assertEqual(case.count("## An outside directory listing"), 1)
        for locale in ("en", "ko"):
            post = ROOT / f"_posts/spoonie-webapps-directory-{locale}/2026-11-10-spoonie-webapps-directory-{locale}.md"
            self.assertTrue(post.is_file())
            source = post.read_text(encoding="utf-8")
            self.assertIn(f"permalink: /spoonie-webapps-directory-{locale}/", source)
            self.assertIn("https://webapps.directory/directory/spooniespoonie", source)

    def test_existing_project_achievements_retained(self):
        case = (ROOT / "_projects/spoonie.md").read_text(encoding="utf-8")
        for original in ("/spoonie-privacy-cache-transition-en/", "/spoonie-privacy-cache-transition-ko/", "/spoonie-search-discovery-en/", "/spoonie-live-polls-en/"):
            self.assertIn(original, case)


if __name__ == "__main__":
    unittest.main()
