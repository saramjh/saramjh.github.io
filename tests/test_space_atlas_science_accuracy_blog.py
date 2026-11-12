"""New Space Atlas live science-copy correction post sources and locale metadata."""
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ScienceAccuracyBlogTest(unittest.TestCase):
    def posts(self):
        return {language: (ROOT / f"_posts/space-atlas-science-accuracy-{language}/2026-11-12-space-atlas-science-accuracy-{language}.md").read_text(encoding="utf8") for language in ("en", "ko")}

    def test_true_source_and_real_deployment_distinctions(self):
        for content in self.posts().values():
            self.assertIn("https://github.com/saramjh/space_atlas_student/pull/2", content)
            self.assertIn("https://spaceatlasedu.org/galaxies/types/", content)
            self.assertIn("https://spaceatlasedu.org/moon/eclipses/", content)
            self.assertIn("https://spaceatlasedu.org/stars/life-cycle/", content)
            self.assertIn("https://doi.org/10.1038/s41550-025-02563-1", content)
            self.assertIn("https://eclipse.gsfc.nasa.gov/LEcat5/LE2001-2100.html", content)
            self.assertIn("/portfolio/space-atlas/", content)
            self.assertNotIn("\ufffd", content)
            self.assertNotRegex(content, r"\?{4,}")

    def test_two_actual_language_permalinks_and_real_owned_image(self):
        for language,content in self.posts().items():
            peer = "ko" if language=="en" else "en"
            self.assertIn(f"permalink: /space-atlas-science-accuracy-{language}/", content)
            self.assertIn(f"alternate_url: /space-atlas-science-accuracy-{peer}/", content)
            self.assertIn(f"lang: {language}", content)
            self.assertIn("date: 2026-11-12", content)
            self.assertIn("image: /assets/images/portfolio/space-atlas-desktop.jpg", content)
            self.assertTrue((ROOT/"assets/images/portfolio/space-atlas-desktop.jpg").exists())
            self.assertIn("published: true", content)
            self.assertIn("seo:", content)

    def test_project_case_surfaces_both_language_notes(self):
        case=(ROOT / "_projects/space-atlas.md").read_text(encoding="utf8")
        self.assertIn("/space-atlas-science-accuracy-en/", case)
        self.assertIn("/space-atlas-science-accuracy-ko/", case)
        self.assertEqual(case.count("## Scientific claims in the live lessons"),1)
        self.assertIn("not a physics-engine change",case)
        self.assertIn("/space-atlas-eusci-diagrams-en/",case)


if __name__=='__main__':
    unittest.main()
