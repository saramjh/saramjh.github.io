"""Navigation-menu accessible name follows the page's language."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MenuLocaleTest(unittest.TestCase):
    def test_nav_checkbox_uses_page_language_and_site_fallback(self):
        nav = (ROOT / "_includes/navbar.html").read_text(encoding="utf8")
        self.assertIn(
            "{% assign menu_lang = page.lang | default: site.lang | default: 'en' %}",
            nav,
        )
        self.assertIn("menu_lang == 'ko' or menu_lang == 'ko-KR'", nav)
        self.assertIn('탐색 메뉴 열기 또는 닫기{% else %}Toggle navigation menu{% endif %}', nav)
        self.assertEqual(nav.count('id="menu-trigger"'), 1)
        self.assertIn('aria-controls="primary-navigation"', nav)
        self.assertIn('<label for="menu-trigger">', nav)

    def test_existing_theme_mode_and_navigation_markup_unchanged(self):
        nav = (ROOT / "_includes/navbar.html").read_text(encoding="utf8")
        self.assertIn('id="mode" aria-label=', nav)
        self.assertIn('aria-pressed="{% if site.mode ==', nav)
        self.assertIn('id="primary-navigation"', nav)
        self.assertIn('class="menu-link', nav)


if __name__ == "__main__":
    unittest.main()
