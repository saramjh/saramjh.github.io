"""Bilingual source, rights and original schematic integrity for DNT release notes."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
STEM = "jekyll-dnt-analytics-compress-regression"
ASSETS = ROOT / "assets" / "img" / "dev-dnt-analytics-20261110"
PR = "https://github.com/saramjh/saramjh.github.io/pull/31"
RUNS = ("42737126098", "42737547315", "42737713334")


def document(lang):
    slug = STEM + "-" + lang
    p = ROOT / "_posts" / slug / ("2026-11-10-" + slug + ".md")
    text = p.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if match is None:
        raise AssertionError(f"Missing Jekyll frontmatter: {p}")
    return match.group(1), match.group(2)


class DntBlogPublicationContract(unittest.TestCase):
    def test_bilingual_metadata_and_crosslinks(self):
        for lang, other in (("ko", "en"), ("en", "ko")):
            with self.subTest(lang=lang):
                front, body = document(lang)
                self.assertIn("permalink: /" + STEM + "-" + lang + "/", front)
                self.assertIn("alternate_lang: " + other, front)
                self.assertIn("alternate_url: /" + STEM + "-" + other + "/", front)
                self.assertIn("lang: " + lang, front)
                self.assertIn("published: true", front)
                self.assertIn("image_width: 1200", front)
                self.assertIn("image_height: 630", front)
                self.assertIn("seo:", front)
                self.assertIn("/" + STEM + "-" + other + "/", body)
                self.assertGreaterEqual(body.count("\n## "), 4)

    def test_exact_original_source_and_scope_boundaries(self):
        for lang in ("ko", "en"):
            with self.subTest(lang=lang):
                _, body = document(lang)
                self.assertIn(PR, body)
                for run in RUNS:
                    self.assertIn("actions/runs/" + run, body)
                self.assertIn("developer.mozilla.org/en-US/docs/Web/API/Navigator/doNotTrack", body)
                self.assertIn("developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar", body)
                self.assertIn("DNT", body)
                self.assertIn("Clarity", body)
                self.assertIn("~~~javascript", body)
                self.assertIn("/privacy/", body)
                self.assertIn("/portfolio/", body)
                self.assertIn("G-EXAMPLE", body)
                self.assertNotIn("100% consent", body)

    def test_original_bilingual_schematics_and_png_metadata(self):
        for lang in ("ko", "en"):
            with self.subTest(lang=lang):
                front, body = document(lang)
                basename = "loader-gate-" + lang
                image = "/assets/img/dev-dnt-analytics-20261110/" + basename
                self.assertIn("image: " + image + ".png", front)
                self.assertIn('src="' + image + '.png"', body)
                self.assertIn(image + ".svg", body)
                self.assertIn("<figcaption>", body)
                png = (ASSETS / (basename + ".png")).read_bytes()
                svg = (ASSETS / (basename + ".svg")).read_text("utf-8")
                self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(
                    (int.from_bytes(png[16:20], "big"),
                     int.from_bytes(png[20:24], "big")),
                    (1200, 630),
                )
                self.assertIn("DNT = 1", svg)
                self.assertIn("DNT = 0", svg)
                self.assertIn("PR #31", svg)


if __name__ == "__main__":
    unittest.main()
