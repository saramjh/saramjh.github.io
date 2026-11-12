"""Project case reading-link selections use only the existing privacy-aware GA4 hook."""
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PortfolioProjectCaseSelectionTest(unittest.TestCase):
    def test_portfolio_case_link_event_is_purpose_limited(self):
        result = subprocess.run(
            ["node", str(ROOT / "tests" / "portfolio_project_case_selection_runtime.cjs")],
            cwd=ROOT, capture_output=True, text=True, timeout=12,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS project-case tracking", result.stdout)
        privacy = (ROOT / "privacy.md").read_text(encoding="utf-8")
        self.assertIn("case-study card or related case-study link", privacy)
        self.assertIn("They do not establish that the destination was read", privacy)
        script = (ROOT / "assets" / "js" / "portfolio.js").read_text(encoding="utf-8")
        self.assertIn("portfolio_project_note", script)
        self.assertIn("navigator.msDoNotTrack", script)
        self.assertNotIn("navigator.sendBeacon", script)


if __name__ == "__main__":
    unittest.main()
