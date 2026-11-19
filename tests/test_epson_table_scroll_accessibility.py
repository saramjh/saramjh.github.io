"""Keep original bilingual Epson maintenance-cost comparisons fully readable on small screens."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
POSTS = {
    'ko': ROOT / '_posts/epson-waste-ink-pad-reset-without-key/2026-09-15-epson-waste-ink-pad-reset-without-key.md',
    'en': ROOT / '_posts/en-epson-waste-ink-pad-reset-without-key/2026-09-15-en-epson-waste-ink-pad-reset-without-key.md',
}
BASE = ROOT / '_sass/klise/_base.scss'


class EpsonTableScrollBoundary(unittest.TestCase):
    def test_original_scroll_container_reused_without_css_override(self):
        self.assertIn('.overflow-table {', BASE.read_text(encoding='utf8'))
        self.assertIn('overflow-x: auto;', BASE.read_text(encoding='utf8'))

    def test_bilingual_table_stays_semantic_and_keyboard_scrollable(self):
        for lang, file in POSTS.items():
            with self.subTest(lang=lang):
                content = file.read_text(encoding='utf8')
                self.assertEqual(content.count('<div class="overflow-table" markdown="1"'), 1)
                self.assertIn('role="region" tabindex="0" aria-label=', content)
                self.assertRegex(content, re.compile(
                    r'<div class="overflow-table" markdown="1"[^>]*>\s*'
                    r'\|[^\n]*\|\n\|\s*:\-+[^\n]*\|\s*\n'
                    r'(?:\|[^\n]*\|\n){4,7}\s*</div>',
                    re.M,
                ))
                self.assertIn('L3100', content)
                self.assertIn('L3156', content)
                self.assertIn('L3106', content)


if __name__ == '__main__':
    unittest.main()
