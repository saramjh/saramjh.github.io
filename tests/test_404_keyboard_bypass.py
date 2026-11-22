"""404 pages retain the shared keyboard bypass and error response contract."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = (ROOT / "_layouts/404.html").read_text(encoding="utf8")
NOT_FOUND = (ROOT / "404.md").read_text(encoding="utf8")


class NotFoundKeyboardBypassTest(unittest.TestCase):
    def test_skip_link_precedes_navigation_and_targets_focusable_main(self):
        self.assertEqual(LAYOUT.count('class="site-skip-link"'), 1)
        self.assertLess(LAYOUT.index('href="#main-content"'), LAYOUT.index('{% include navbar.html %}'))
        self.assertEqual(LAYOUT.count('id="main-content"'), 1)
        self.assertIn('id="main-content" tabindex="-1"', LAYOUT)
        self.assertIn("본문으로 건너뛰기", LAYOUT)
        self.assertIn("Skip to main content", LAYOUT)

    def test_main_landmark_name_matches_localized_layout_contract(self):
        for required in ("skip_lang == 'ko' or skip_lang == 'ko-KR'",
                         "본문{% else %}Content{% endif %}"):
            self.assertIn(required, LAYOUT)

    def test_custom_404_remains_nonindexed_and_retains_home_link(self):
        self.assertIn('permalink: "/404.html"', NOT_FOUND)
        self.assertIn('robots: "noindex, follow"', NOT_FOUND)
        self.assertIn('sitemap: false', NOT_FOUND)
        self.assertIn('href="{{ site.url }}"', LAYOUT)


if __name__ == "__main__":
    unittest.main()
