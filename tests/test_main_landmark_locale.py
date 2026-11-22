"""Accessibility names for main landmarks follow the page language."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = (
    "aria-label=\"{% if skip_lang == 'ko' or skip_lang == 'ko-KR' %}"
    "본문{% else %}Content{% endif %}\""
)

class MainLandmarkLocaleTest(unittest.TestCase):
    def test_main_landmark_uses_existing_locale_selector(self):
        for name in ("default.html", "page.html", "post.html"):
            with self.subTest(layout=name):
                src = (ROOT / "_layouts" / name).read_text(encoding="utf-8")
                self.assertIn("{% assign skip_lang = page.lang", src)
                self.assertEqual(src.count('id="main-content"'), 1)
                self.assertIn(EXPECTED, src)
                self.assertNotIn('aria-label="Content"', src)

if __name__ == "__main__":
    unittest.main()
