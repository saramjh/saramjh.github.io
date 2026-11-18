"""Check truthful, original PR #47 Open Graph diagrams in both languages."""
from pathlib import Path
import re
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "assets/img/dev/spoonie-pr47-pwa-og-20261118"


class SpooniePR47OGSourceTest(unittest.TestCase):
    def test_pages_use_local_1200x630_original_source_diagram(self):
        for lang in ("ko", "en"):
            with self.subTest(lang=lang):
                path = ROOT / f"_posts/spoonie-pwa-search-state-recovery-{lang}" / (
                    f"2026-11-16-spoonie-pwa-search-state-recovery-{lang}.md"
                )
                body = path.read_text(encoding="utf8")
                frontmatter = body.split("---", 2)[1]
                expected = f"/assets/img/dev/spoonie-pr47-pwa-og-20261118/spoonie-pr47-{lang}.png"
                self.assertIn("image: " + expected + "\n", frontmatter)
                self.assertIn("image_width: 1200\n", frontmatter)
                self.assertIn("image_height: 630\n", frontmatter)
                image = IMAGE_DIR / f"spoonie-pr47-{lang}.png"
                buf = image.read_bytes()
                self.assertEqual(buf[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(struct.unpack(">II", buf[16:24]), (1200, 630))
                self.assertGreater(len(buf), 20000)
                self.assertLess(len(buf), 400000)
                self.assertNotIn(b"\xef\xbf\xbd", body.encode("utf8"))

    def test_diagram_is_explicitly_not_a_product_screenshot_or_iphone_validation(self):
        script = (ROOT / "scripts/dev-spoonie-pr47-og.swift").read_text(encoding="utf8")
        self.assertIn("Physical iPhone not tested", script)
        self.assertIn("실제 제품 화면이 아닌 구현 흐름 도식", script)
        self.assertIn("URL의 검색어와 탭 복원", script)
        self.assertIn("Restore query and tab from URL", script)
        self.assertIn("Spoonie PR #47", script)
        self.assertNotRegex(script, r"(?i)measured adoption|proven iphone install")


if __name__ == "__main__":
    unittest.main()
