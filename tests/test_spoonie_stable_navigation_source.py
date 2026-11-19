"""Keep the November 14 Spoonie navigation story linked to a durable source revision."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
POSTS = {
    'en': ROOT / '_posts/spoonie-route-loading-citation-en/2026-11-12-spoonie-route-loading-citation-en.md',
    'ko': ROOT / '_posts/spoonie-route-loading-citation-ko/2026-11-12-spoonie-route-loading-citation-ko.md',
}
STABLE = ('https://github.com/saramjh/spoonie/blob/'
          '6f84ed861176eedc43412a12834adda51c4e1d0b/'
          'src/components/layout/NavigationProgress.tsx')

class SpoonieStableSourceTest(unittest.TestCase):
    def test_both_languages_keep_the_original_claim_without_linking_a_retired_bundle(self):
        for language, post in POSTS.items():
            with self.subTest(language=language):
                body = post.read_text(encoding='utf-8')
                self.assertEqual(body.count(STABLE), 1)
                self.assertNotIn('https://spoonie.kr/_next/static/chunks/app/layout-', body)
                self.assertIn('https://github.com/saramjh/spoonie/pull/44', body)
                self.assertIn('https://github.com/saramjh/spoonie/pull/45', body)
                self.assertIn('407', body)
                self.assertNotIn('\ufffd', body)
                self.assertNotIn('????', body)
                self.assertIn('2026-11-12', str(post))

    def test_historical_build_and_human_outcome_limits_remain_explicit(self):
        en = POSTS['en'].read_text(encoding='utf-8')
        ko = POSTS['ko'].read_text(encoding='utf-8')
        self.assertIn('November 14', en)
        self.assertIn('11월 14일', ko)
        self.assertIn('no longer', en)
        self.assertIn('현재 열리지 않', ko)
        self.assertIn('abandonment', en)
        self.assertIn('이탈 감소', ko)

if __name__ == '__main__':
    unittest.main()
