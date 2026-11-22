"""Blog default/page/post keyboard bypass and mobile menu focus contract."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LAYOUTS = ('default.html', 'page.html', 'post.html')


class DefaultBlogSkipLinkTest(unittest.TestCase):
    def test_all_three_original_layouts_have_one_bypass_before_menu(self):
        for name in LAYOUTS:
            with self.subTest(name=name):
                src = (ROOT / "_layouts" / name).read_text(encoding="utf8")
                self.assertEqual(src.count('class="site-skip-link"'), 1)
                self.assertLess(src.index('href="#main-content"'), src.index('{% include navbar.html %}'))
                self.assertEqual(src.count('id="main-content"'), 1)
                self.assertIn('tabindex="-1" aria-label="{% if skip_lang ==', src)

    def test_language_specific_fallback_labels(self):
        for name in LAYOUTS:
            src = (ROOT / "_layouts" / name).read_text(encoding="utf8")
            self.assertIn("skip_lang == 'ko' or skip_lang == 'ko-KR'", src)
            self.assertIn('본문으로 건너뛰기', src)
            self.assertIn('Skip to main content', src)

    def test_site_style_offscreen_until_keyboard_focus(self):
        src = (ROOT / "_sass/klise/_layout.scss").read_text(encoding="utf8")
        self.assertIn('body:not(.portfolio-body) .site-skip-link', src)
        self.assertIn('top: -100px;', src)
        self.assertIn('top: 12px;', src)
        self.assertIn('outline: 3px solid $text-link-blue', src)

    def test_dark_theme_has_distinct_legible_surface_and_outline(self):
        src = (ROOT / "_sass/klise/_dark.scss").read_text(encoding="utf8")
        self.assertIn('body[data-theme="dark"] .site-skip-link', src)
        self.assertIn('background: $dark-white;', src)
        self.assertIn('color: $dark-black;', src)
        self.assertIn('outline-color: $dark-text-link-blue;', src)

    def test_mobile_fullscreen_overlay_inerts_the_new_bypass(self):
        js = (ROOT / "assets/js/main.js").read_text(encoding="utf8")
        unit = (ROOT / "tests/mobile_navigation_focus_runtime.cjs").read_text(encoding="utf8")
        browser = (ROOT / "tests/portfolio_layout_smoke.py").read_text(encoding="utf8")
        for src in (js, unit, browser):
            self.assertIn('body > .site-skip-link', src)
        self.assertIn('mobile.siteSkip.inert, true', unit)
        self.assertIn('mobile.siteSkip.inert, false', unit)


if __name__ == "__main__":
    unittest.main()
