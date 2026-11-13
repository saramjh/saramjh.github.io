"""Source-bound bilingual release checks for the public Spoonie search case."""

from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "spoonie-search-discovery"
DATE = "2026-11-12"


class SpoonieSearchDiscoveryCaseTest(unittest.TestCase):
    def test_source_bound_reciprocal_localized_articles(self):
        for language, other in (("ko", "en"), ("en", "ko")):
            slug = f"{BASE}-{language}"
            text = (ROOT / "_posts" / slug / f"{DATE}-{slug}.md").read_text(
                encoding="utf-8"
            )
            self.assertTrue(text.startswith("---\n"))
            for required in (
                f"permalink: /{slug}/",
                f"lang: {language}",
                f"alternate_lang: {other}",
                f"alternate_url: /{BASE}-{other}/",
                f"](/{BASE}-{other}/)",
                f"image: /{slug}/spoonie-search-flow-og.png",
                "published: true",
                "https://github.com/saramjh/spoonie/pull/31",
                "https://spoonie.kr/search",
                "/portfolio/spoonie/",
            ):
                self.assertIn(required, text, (slug, required))
            self.assertIn("20", text)
            self.assertIn("10", text)
            self.assertNotIn("\ufffd", text)
            self.assertNotIn("????", text)
            self.assertGreater(len(text), 2800)

    def test_spoonie_project_case_links_search_in_both_languages(self):
        project = (ROOT / "_projects" / "spoonie.md").read_text(encoding="utf-8")
        for needed in (
            "https://github.com/saramjh/spoonie/pull/31",
            "https://spoonie.kr/search",
            "/spoonie-search-discovery-en/",
            "/spoonie-search-discovery-ko/",
            "up to twenty",
            "ten-item",
        ):
            self.assertIn(needed, project)
        self.assertEqual(project.count("/spoonie-search-discovery-en/"), 1)
        self.assertEqual(project.count("/spoonie-search-discovery-ko/"), 1)
        self.assertIn("/spoonie-live-polls-en/", project)

    def test_diagrams_are_distinct_original_accessible_svgs(self):
        visuals = []
        for language in ("ko", "en"):
            slug = f"{BASE}-{language}"
            file = ROOT / "_posts" / slug / "spoonie-search-flow.svg"
            content = file.read_text(encoding="utf-8")
            root = ET.fromstring(content)
            self.assertEqual(root.attrib["width"], "1280")
            self.assertEqual(root.attrib["height"], "530")
            self.assertEqual(root.attrib["role"], "img")
            self.assertEqual(root.attrib["aria-labelledby"], "title desc")
            self.assertNotIn("<script", content)
            self.assertNotIn("\ufffd", content)
            self.assertIn("20", content)
            visuals.append(content)
        self.assertNotEqual(visuals[0], visuals[1])


if __name__ == "__main__":
    unittest.main()
