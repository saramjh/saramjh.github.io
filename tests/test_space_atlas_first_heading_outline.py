"""Both Space Atlas overview editions expose an unbroken heading outline."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "ko": ("_posts/space-atlas-student/2026-09-15-space-atlas-student.md", "주요 인터랙티브 도구 바로가기"),
    "en": ("_posts/space-atlas-student-en/2026-09-15-space-atlas-student-en.md", "Try the interactive astronomy tools directly"),
}


class SpaceAtlasFirstHeadingOutlineTest(unittest.TestCase):
    def test_ko_and_en_heading_hierarchy(self):
        for lang, (path, first_section) in PAGES.items():
            with self.subTest(lang=lang):
                text = (ROOT / path).read_text(encoding="utf-8")
                headings = [(len(m.group(1)), m.group(2)) for m in re.finditer(r"(?m)^(#{1,6}) (.+)$", text)]
                self.assertGreaterEqual(len(headings), 10)
                self.assertEqual(1, headings[0][0])
                self.assertEqual((2, first_section), headings[1])
                self.assertTrue(all(nxt[0] - prev[0] <= 1 for prev, nxt in zip(headings, headings[1:])))
                self.assertEqual(1, sum(level == 1 for level, _ in headings))
                self.assertIn("modified: 2026-11-23\n", text)
                self.assertIn("last_modified_at: 2026-11-23\n", text)
                self.assertNotIn("\ufffd", text)


if __name__ == "__main__":
    unittest.main()
