"""Source-bound Dev portfolio update for a published regional search UI fix."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
POSTS = {
    "ko": ROOT / "_posts/koreaves-bird-evidence-atlas" /
          "2026-10-12-koreaves-bird-evidence-atlas.md",
    "en": ROOT / "_posts/koreaves-bird-evidence-atlas-en" /
          "2026-10-12-koreaves-bird-evidence-atlas-en.md",
}
REGION = "https://koreaves.com/regions/seoul/"
CATALOG = "https://koreaves.com/species/browse/"


class KoreavesRegionCatalogLiveFixContextTest(unittest.TestCase):
    def test_original_pair_and_source_immutable_identity(self):
        for lang, path in POSTS.items():
            source = path.read_text("utf8")
            self.assertIn("date: 2026-10-12", source)
            self.assertIn("modified: 2026-11-16", source)
            self.assertIn("last_modified_at: 2026-11-16", source)
            self.assertIn("published: true", source)
            self.assertIn("lang: " + lang, source)
            self.assertNotIn("\ufffd", source)
            self.assertNotIn("????", source)
            self.assertIn(REGION, source)
            self.assertIn(CATALOG, source)
        self.assertIn("alternate_url: /koreaves-bird-evidence-atlas-en/",
                      POSTS["ko"].read_text("utf8"))
        self.assertIn("alternate_url: /koreaves-bird-evidence-atlas/",
                      POSTS["en"].read_text("utf8"))

    def test_reader_problem_actual_fix_and_visible_before_after(self):
        ko = POSTS["ko"].read_text("utf8")
        en = POSTS["en"].read_text("utf8")
        for source in (ko, en):
            self.assertIn("Accipiter gularis", source)
            self.assertIn("280", source)
            self.assertIn("390px", source)
            self.assertIn("1440px", source)
            self.assertIn("hidden", source)
            self.assertIn("display: grid", source)
        self.assertIn("조롱이", ko)
        self.assertIn("one matching bird", en)

    def test_factual_boundaries_preserve_original_evidence_and_no_fabricated_adoption(self):
        ko = POSTS["ko"].read_text("utf8")
        en = POSTS["en"].read_text("utf8")
        self.assertIn("조류 기록", ko)
        self.assertIn("이용량 변화", ko)
        self.assertIn("source records", en)
        self.assertIn("not been measured", en)
        self.assertNotIn("more visitors", en)
        self.assertNotIn("classroom adoption", en)


if __name__ == "__main__":
    unittest.main()
