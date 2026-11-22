"""Scoped original-blog GA4 event, not a child/workshop usage metric."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOOTER = (ROOT / '_includes/footer.html').read_text(encoding='utf8')
JS = (ROOT / 'assets/js/no-tilt-worksheet-outbound.js').read_text(encoding='utf8')
SOURCES = {
    'ko': ROOT / '_posts/earth-seasons-no-tilt-experiment-ko/2026-11-15-earth-seasons-no-tilt-experiment-ko.md',
    'en': ROOT / '_posts/earth-seasons-no-tilt-experiment-en/2026-11-15-earth-seasons-no-tilt-experiment-en.md',
}
TARGET='https://spaceatlasedu.org/assets/handouts/earth-seasons-no-tilt.html'

class ScopedWorksheetLinkSelectionTest(unittest.TestCase):
    def test_original_bilingual_artifact_source_unchanged(self):
        for locale, path in SOURCES.items():
            with self.subTest(locale=locale):
                text=path.read_text('utf8')
                self.assertEqual(text.count(TARGET),3)
                self.assertIn(f'lang: {locale}',text)
                self.assertIn('date: 2026-11-15',text)

    def test_loader_only_for_exact_two_pages_and_existing_ga_opt_out(self):
        self.assertEqual(FOOTER.count('src="/assets/js/no-tilt-worksheet-outbound.js"'),1)
        self.assertIn("page.url == '/earth-seasons-no-tilt-experiment-ko/'",FOOTER)
        self.assertIn("page.url == '/earth-seasons-no-tilt-experiment-en/'",FOOTER)
        self.assertIn('site.google_analytics and page.tracking != false and page.date',FOOTER)
        self.assertNotIn('page.url contains',FOOTER)

    def test_click_only_private_payload_and_exact_allowlist(self):
        self.assertIn("document.querySelectorAll('main a[href]')",JS)
        self.assertIn("url.origin !== exactOrigin",JS)
        self.assertIn("url.pathname !== exactPath",JS)
        self.assertIn("link.addEventListener('click'",JS)
        self.assertIn('navigator.doNotTrack',JS)
        self.assertIn("window.gtag('event', 'no_tilt_worksheet_select'",JS)
        for sensitive in ('page_location:', 'link_url:', 'client_id:', 'email:', 'user_id:'):
            self.assertNotIn(sensitive,JS)
        self.assertNotIn('preventDefault(',JS)
        self.assertNotIn('localStorage',JS)
        self.assertNotIn('sendBeacon',JS)

if __name__ == '__main__': unittest.main()
