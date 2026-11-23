"""Keep the newly published BOU contribution visible in the KoreAves project profile."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class KoreAvesBouProjectProfileTests(unittest.TestCase):
    def test_profile_links_the_original_author_credited_publication(self):
        profile = (ROOT / "_projects/koreaves.md").read_text("utf-8")
        article = (ROOT / "_posts/koreaves-bou-when-records-become-maps-en/2026-11-23-koreaves-bou-when-records-become-maps-en.md").read_text("utf-8")
        ko = (ROOT / "_posts/koreaves-bou-when-records-become-maps-ko/2026-11-23-koreaves-bou-when-records-become-maps-ko.md").read_text("utf-8")
        archive = (ROOT / "_data/recognitions.yml").read_text("utf-8")
        url = "https://bou.org.uk/blog-oh-when-records-become-maps/"
        self.assertEqual(profile.count(url), 1)
        self.assertIn("When Records Become Maps", profile)
        self.assertIn("Jihun Oh", article)
        self.assertIn(url, article)
        self.assertIn("Jihun Oh", ko)
        self.assertIn("/koreaves-bou-when-records-become-maps-ko/", profile)
        self.assertIn("/koreaves-bou-when-records-become-maps-en/", profile)
        self.assertIn("bou-when-records-become-maps", archive)
        self.assertIn("not peer-reviewed research", profile)
        self.assertIn("or evidence of measured adoption", profile)


if __name__ == "__main__":
    unittest.main()
