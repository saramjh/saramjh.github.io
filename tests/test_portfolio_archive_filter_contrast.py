"""Archive filter visual state must agree with its aria-pressed behavior."""
from pathlib import Path
import unittest


CSS = (Path(__file__).resolve().parents[1] / "assets/css/portfolio.css").read_text(encoding="utf8")


class ArchiveFilterContrastTest(unittest.TestCase):
    def test_active_selection_has_explicit_opaque_accent_and_dark_ink(self):
        selector = '.portfolio-body .folio .folio-filter[aria-pressed="true"]'
        self.assertEqual(CSS.count(selector), 1)
        rule = CSS.split(selector + "{", 1)[1].split("}", 1)[0]
        self.assertIn("background:var(--folio-accent)!important", rule)
        self.assertIn("color:var(--folio-accent-ink)!important", rule)
        self.assertIn("border-color:var(--folio-accent)!important", rule)

    def test_inactive_hover_has_separate_neutral_state(self):
        selector = '.portfolio-body .folio .folio-filter[aria-pressed="false"]:hover'
        self.assertEqual(CSS.count(selector), 1)
        rule = CSS.split(selector + "{", 1)[1].split("}", 1)[0]
        self.assertIn("background:var(--folio-raised)!important", rule)
        self.assertIn("color:var(--folio-text)!important", rule)
        self.assertNotIn("background:var(--folio-accent)!important", rule)

    def test_no_legacy_hover_active_conflation(self):
        self.assertNotIn(".folio-filter:hover,.portfolio-body .folio .folio-filter.is-active", CSS)


if __name__ == "__main__":
    unittest.main()
