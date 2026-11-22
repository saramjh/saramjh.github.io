"""Portfolio keyboard-navigation skip link must be visible on focus and target main."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = (ROOT / "_layouts/portfolio.html").read_text(encoding="utf8")
CSS = (ROOT / "assets/css/portfolio.css").read_text(encoding="utf8")


class PortfolioSkipLinkTest(unittest.TestCase):
    def test_skip_link_is_first_interactive_element_before_navigation(self):
        self.assertEqual(LAYOUT.count('class="folio-skip-link"'), 1)
        self.assertLess(LAYOUT.index('href="#main-content"'), LAYOUT.index('{% include navbar.html %}'))
        self.assertIn(">Skip to main content</a>", LAYOUT)

    def test_link_target_is_unique_and_programmatically_focusable(self):
        self.assertEqual(LAYOUT.count('id="main-content"'), 1)
        self.assertIn('<main class="folio" id="main-content" tabindex="-1"', LAYOUT)

    def test_initially_offscreen_but_revealed_with_keyboard_focus(self):
        selector = ".portfolio-body .folio-skip-link"
        self.assertEqual(CSS.count(selector + "{"), 1)
        offscreen = CSS.split(selector + "{", 1)[1].split("}", 1)[0]
        self.assertIn("top:-100px", offscreen)
        self.assertIn("z-index:9999", offscreen)
        focus = CSS.split(selector + ":focus,", 1)[1].split("}", 1)[0]
        self.assertIn("top:12px", focus)
        self.assertIn("outline:3px", focus)

    def test_mobile_overlay_inerts_bypass_link_with_other_backgrounds(self):
        nav = (ROOT / "assets/js/main.js").read_text(encoding="utf8")
        self.assertIn("body > .folio-skip-link", nav)
        browser = (ROOT / "tests/portfolio_layout_smoke.py").read_text(encoding="utf8")
        self.assertIn("body > .folio-skip-link", browser)

    def test_visible_link_inherits_existing_high_contrast_portfolio_tokens(self):
        rule = CSS.split(".portfolio-body .folio-skip-link{", 1)[1].split("}", 1)[0]
        self.assertIn("background:var(--folio-accent)", rule)
        self.assertIn("color:var(--folio-accent-ink)", rule)
        self.assertNotIn("display:none", rule)
        self.assertNotIn("visibility:hidden", rule)


if __name__ == "__main__":
    unittest.main()
