"""Measure only explicit clicks on three first-party portfolio CTAs."""
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PortfolioLiveProjectSelectionTest(unittest.TestCase):
    def test_exact_ctas_and_consent(self):
        completed = subprocess.run(
            ["node", str(ROOT / "tests/portfolio_live_project_selection_runtime.cjs")],
            cwd=ROOT, capture_output=True, text=True, timeout=12,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("PASS exact CTA", completed.stdout)
        layout = (ROOT / "_layouts/project.html").read_text(encoding="utf-8")
        self.assertIn('class="folio-primary-cta" href="{{ page.site_url | escape }}"', layout)
        for slug, site in (
            ("koreaves", "https://koreaves.com/"),
            ("space-atlas", "https://spaceatlasedu.org/"),
            ("spoonie", "https://spoonie.kr/"),
        ):
            page = (ROOT / "_projects" / f"{slug}.md").read_text(encoding="utf-8")
            self.assertIn(f"site_url: {site}", page)
        privacy = (ROOT / "privacy.md").read_text(encoding="utf-8")
        self.assertIn("portfolio_live_project_select", privacy)
        self.assertIn("does not include the destination URL", privacy)


if __name__ == '__main__':
    unittest.main()
