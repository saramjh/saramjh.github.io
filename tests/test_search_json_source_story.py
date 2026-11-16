"""Source-bound bilingual post for the shipped search JSON repair."""
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "jekyll-search-json-native-text"
BASE = "assets/img/dev-search-json-20261116"


class ShippedSearchIndexStory(unittest.TestCase):
    def test_bilingual_metadata_and_real_proof(self):
        for lang, other in (("ko", "en"), ("en", "ko")):
            f = ROOT / "_posts" / f"{SLUG}-{lang}" / f"2026-11-16-{SLUG}-{lang}.md"
            with self.subTest(lang=lang):
                text = f.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---" + chr(10)))
                front = text.split("---", 2)[1]
                self.assertIn(f"lang: {lang}", front)
                self.assertIn(f"alternate_lang: {other}", front)
                self.assertIn(f"alternate_url: /{SLUG}-{other}/", front)
                self.assertIn(f"permalink: /{SLUG}-{lang}/", front)
                self.assertIn(f"image: /{BASE}/search-json-{lang}.png", front)
                self.assertIn("image_width: 1200", front)
                self.assertIn("image_height: 630", front)
                self.assertIn("published: true", front)
                self.assertIn("seo:", front)
                self.assertIn("https://github.com/saramjh/saramjh.github.io/pull/175", text)
                self.assertIn("43802310024", text)
                self.assertIn("43802506835", text)
                self.assertIn("post.title | jsonify", text)
                self.assertEqual(text.count("{% raw %}"), 1)
                self.assertEqual(text.count("{% endraw %}"), 1)
                self.assertIn("204", text)
                self.assertIn("15", text)
                self.assertIn("13", text)
                self.assertIn("4", text)
                self.assertIn(f"/{SLUG}-{other}/", text)
                self.assertIn("/archive/", text)
                self.assertIn(f"/{BASE}/search-json-{lang}.svg", text)
                self.assertIn(f"/{BASE}/search-json-{lang}.png", text)
                self.assertGreaterEqual(len(text.split("## ")), 5)
                self.assertNotRegex(text, r"(?i)guaranteed traffic|proved adoption|100% uplift")

    def test_source_and_png_are_exact_size(self):
        for lang in ("ko", "en"):
            with self.subTest(lang=lang):
                svg = (ROOT / BASE / f"search-json-{lang}.svg").read_text(encoding="utf-8")
                png = (ROOT / BASE / f"search-json-{lang}.png").read_bytes()
                self.assertIn('viewBox="0 0 1200 630"', svg)
                self.assertIn("Spoonie&amp;#39;s", svg)
                self.assertIn("Spoonie&#39;s", svg)
                self.assertIn("Spoonie", svg)
                self.assertEqual(png[:8], bytes([137, 80, 78, 71, 13, 10, 26, 10]))
                self.assertEqual(struct.unpack(">II", png[16:24]), (1200, 630))

    def test_inline_liquid_filter_is_literal_code_not_markdown_table(self):
        for lang in ("ko", "en"):
            f = ROOT / "_posts" / f"{SLUG}-{lang}" / f"2026-11-16-{SLUG}-{lang}.md"
            with self.subTest(lang=lang):
                source = f.read_text(encoding="utf-8")
                code_span = chr(96) + "record.detail | jsonify" + chr(96)
                self.assertIn(code_span, source)
                lines = source.splitlines()
                in_fence = False
                for line in lines:
                    if line.startswith("~~~"):
                        in_fence = not in_fence
                        continue
                    if not in_fence and "record.detail | jsonify" in line:
                        self.assertIn(code_span, line)
                        self.assertFalse(line.startswith("|"), "Unexpected Markdown table cell")

    def test_live_code_is_already_deployed_fixed(self):
        index = (ROOT / "assets/search.json").read_text(encoding="utf-8")
        runtime = (ROOT / "assets/js/archive-search.js").read_text(encoding="utf-8")
        self.assertIn("post.title | jsonify", index)
        self.assertIn("post.description | jsonify", index)
        self.assertNotIn("decoder.innerHTML", runtime)


if __name__ == "__main__":
    unittest.main()
