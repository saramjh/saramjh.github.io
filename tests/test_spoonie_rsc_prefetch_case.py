"""Guard the bilingual Spoonie RSC-prefetch case study and its original OG diagrams."""

from pathlib import Path
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
SLUG = "spoonie-rsc-prefetch-20261119"
IMAGE_DIR = ROOT / "assets/img/dev" / SLUG
POSTS = {
    "ko": ROOT / "_posts" / f"{SLUG}-ko" / f"2026-11-19-{SLUG}-ko.md",
    "en": ROOT / "_posts" / f"{SLUG}-en" / f"2026-11-19-{SLUG}-en.md",
}


def frontmatter(source: str) -> str:
    parts = source.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise AssertionError("Expected one YAML frontmatter block")
    return parts[1]


class SpoonieRscPrefetchCaseTest(unittest.TestCase):
    def test_bilingual_frontmatter_and_reciprocal_language_links(self):
        sources = {lang: path.read_text(encoding="utf-8") for lang, path in POSTS.items()}
        expected = {
            "ko": ("/spoonie-rsc-prefetch-20261119-ko/", "/spoonie-rsc-prefetch-20261119-en/", "en"),
            "en": ("/spoonie-rsc-prefetch-20261119-en/", "/spoonie-rsc-prefetch-20261119-ko/", "ko"),
        }
        for lang, source in sources.items():
            with self.subTest(lang=lang):
                meta = frontmatter(source)
                permalink, alternate, alternate_lang = expected[lang]
                self.assertIn(f"lang: {lang}\n", meta)
                self.assertIn(f"alternate_lang: {alternate_lang}\n", meta)
                self.assertIn(f"permalink: {permalink}\n", meta)
                self.assertIn(f"alternate_url: {alternate}\n", meta)
                self.assertIn("published: true\n", meta)
                self.assertIn("image_width: 1200\n", meta)
                self.assertIn("image_height: 630\n", meta)
                self.assertIn(f"/{SLUG}/", meta)
                self.assertIn(alternate, source)
                self.assertIn("width=\"1200\" height=\"630\"", source)
                self.assertRegex(source, r"<img[^>]+alt=\"[^\"]+\"")
                self.assertIn("<figcaption>", source)
                self.assertNotIn("\ufffd", source)

    def test_original_sources_and_measurement_limits_are_present(self):
        for lang, path in POSTS.items():
            source = path.read_text(encoding="utf-8")
            with self.subTest(lang=lang):
                for pr in (48, 49, 50):
                    self.assertIn(f"https://github.com/saramjh/spoonie/pull/{pr}", source)
                self.assertIn("https://spoonie.kr/", source)
                self.assertIn("https://spoonie.kr/search", source)
                self.assertIn("HTTP 410", source)
                self.assertRegex(source.lower(), r"monthly functions usage.*not been compared|월간 functions 사용량.*아직 비교하지 않았")
                self.assertIn("44244452809", source)
                self.assertIn("44255793226", source)
                self.assertIn("44338009228", source)

    def test_project_page_reference_remains_unchanged_and_case_links_back(self):
        project = (ROOT / "_projects/spoonie.md").read_text(encoding="utf-8")
        self.assertIn("last_modified_at: 2026-11-17T21:31:15+09:00", project)
        self.assertIn("writing_url: /spoonie-bookmark-privacy-boundary-en/", project)
        for lang, path in POSTS.items():
            with self.subTest(lang=lang):
                article = path.read_text(encoding="utf-8")
                self.assertIn("(/portfolio/spoonie/)", article)

    def test_local_og_images_are_original_sized_pngs(self):
        for lang in ("ko", "en"):
            image = IMAGE_DIR / f"spoonie-rsc-prefetch-{lang}.png"
            with self.subTest(lang=lang):
                data = image.read_bytes()
                self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(struct.unpack(">II", data[16:24]), (1200, 630))
                self.assertGreater(len(data), 20000)
                self.assertLess(len(data), 400000)
                self.assertNotIn(b"\xef\xbf\xbd", data)
                pos = 8
                chunks = []
                while pos + 12 <= len(data):
                    size = struct.unpack(">I", data[pos:pos + 4])[0]
                    kind = data[pos + 4:pos + 8]
                    chunks.append(kind)
                    pos += 12 + size
                    if kind == b"IEND":
                        break
                self.assertIn(b"IHDR", chunks)
                self.assertIn(b"IDAT", chunks)
                self.assertEqual(chunks[-1], b"IEND")
                self.assertFalse(set(chunks) & {b"tEXt", b"iTXt", b"eXIf"})

    def test_source_diagram_does_not_claim_quota_recovery(self):
        for lang, path in POSTS.items():
            source = path.read_text(encoding="utf-8").lower()
            with self.subTest(lang=lang):
                self.assertIn("10", source)
                self.assertIn("390", source)
                self.assertIn("125,000", source)
                self.assertIn("54", source)
                self.assertTrue(
                    "remain unknown" in source or "확인되지 않았다" in source,
                    "The article must retain the explicit no-quota-recovery qualification",
                )


if __name__ == "__main__":
    unittest.main()
