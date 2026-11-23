"""Homepage links to the newly shipped source-bound Korean evidence archive."""
from pathlib import Path
import re
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]
HOME=(ROOT/"_layouts/home.html").read_text("utf-8")
STYLE=(ROOT/"_sass/klise/_layout.scss").read_text("utf-8")
PRIVACY=(ROOT/"privacy.md").read_text("utf-8")
SCRIPT=ROOT/"assets/js/home-recognition-selection.js"

class HomeRecognitionLanguageEntryTests(unittest.TestCase):
    def test_only_existing_original_archive_routes_and_no_new_sender(self):
        self.assertTrue((ROOT/"portfolio/recognition/index.html").is_file())
        self.assertTrue((ROOT/"portfolio/recognition/ko/index.html").is_file())
        self.assertEqual(HOME.count('href="/portfolio/recognition/"'),1)
        self.assertEqual(HOME.count('href="/portfolio/recognition/ko/"'),1)
        self.assertIn('data-recognition-locale="en" lang="en"',HOME)
        self.assertIn('data-recognition-locale="ko" lang="ko" hreflang="ko"',HOME)
        self.assertIn('한국어로 외부 기록 보기',HOME)
        self.assertIn('Browse publications and resource listings',HOME)
        self.assertIn('<script src="/assets/js/home-recognition-selection.js" defer></script>',HOME)
        self.assertEqual(HOME.count('class="project-showcase-link"'),7)

    def test_click_scope_user_input_and_dnt(self):
        src=SCRIPT.read_text("utf-8")
        for item in ('navigator.doNotTrack', 'window.doNotTrack','navigator.msDoNotTrack',
                     "typeof window.gtag!=='function'",'homepage_recognition_archive',
                     "item_id:locale","link.getAttribute('href')!==routes[locale]"):
            self.assertIn(item,src)
        for dangerous in ('window.location=', 'preventDefault(', 'fetch(', 'localStorage', 'navigator.sendBeacon'):
            self.assertNotIn(dangerous,src)
        self.assertIn('choosing the English or Korean external-record archive',PRIVACY)
        result=subprocess.run(["node",str(ROOT/"tests/home_recognition_language_selection_runtime.cjs")],
                              cwd=ROOT,check=False,capture_output=True,text=True,timeout=15)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('PASS exact first-party',result.stdout)

    def test_small_screen_links_wrap_keep_keyboard_focus(self):
        self.assertRegex(STYLE,r'(?s)\.project-showcase-proof\s*\{[^}]*display: flex;')
        self.assertRegex(STYLE,r'(?s)\.project-showcase-proof\s*\{[^}]*flex-wrap: wrap;')
        self.assertRegex(STYLE,r'(?s)\.project-showcase-proof-link\s*\{[^}]*max-width: 100%;')
        self.assertIn('&:focus-visible',STYLE.split('.project-showcase-proof-link {',1)[1])
        self.assertIn('min-height: 44px',STYLE.split('.project-showcase-proof-link {',1)[1])
        self.assertNotIn('\ufffd',HOME)
        self.assertNotIn('????',HOME)


if __name__=="__main__":unittest.main()
