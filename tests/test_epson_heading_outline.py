"""Verify accessible KO/EN Epson article heading outlines."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "_posts/epson-waste-ink-pad-reset-without-key/2026-09-15-epson-waste-ink-pad-reset-without-key.md",
    "_posts/en-epson-waste-ink-pad-reset-without-key/2026-09-15-en-epson-waste-ink-pad-reset-without-key.md",
)


def visible_headings(markdown):
    """Extract Markdown section headings, ignoring fenced code samples."""
    inside = False
    fence = ""
    result = []
    for line in markdown.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if not inside:
                inside, fence = True, marker[0]
            elif marker[0] == fence:
                inside, fence = False, ""
            continue
        if not inside:
            match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if match:
                result.append((len(match.group(1)), match.group(2)))
    if inside:
        raise AssertionError("Unclosed Markdown code fence")
    return result


class EpsonHeadingOutlineTests(unittest.TestCase):
    def test_localized_articles_use_h2_sections_and_h3_subsections(self):
        for path in PAGES:
            with self.subTest(path=path):
                page = (ROOT / path).read_text(encoding="utf-8")
                headings = visible_headings(page.split("\n---\n", 1)[-1])
                self.assertGreaterEqual(len(headings), 14)
                self.assertEqual(2, headings[0][0])
                self.assertTrue(all(level in (2, 3) for level, _ in headings))
                for (previous, _), (current, _) in zip(headings, headings[1:]):
                    self.assertLessEqual(current - previous, 1)
                self.assertTrue(any(level == 3 for level, _ in headings))

    def test_modified_date_matches_semantic_heading_change(self):
        for path in PAGES:
            with self.subTest(path=path):
                page = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn("modified: 2026-11-23\n", page)
                self.assertIn("last_modified_at: 2026-11-23\n", page)


if __name__ == "__main__":
    unittest.main()
