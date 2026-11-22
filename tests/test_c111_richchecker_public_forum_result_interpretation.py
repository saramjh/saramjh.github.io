"""C111: source-backed forum mention helps readers interpret results without invented adoption."""
from pathlib import Path
import unittest
import re

ROOT=Path(__file__).resolve().parents[1]
KO=ROOT/'_posts/rich-face-test/2026-09-12-rich-face-test.md'
EN=ROOT/'_posts/rich-face-test-en/2026-11-14-rich-face-test-en.md'
LINK='https://gall.dcinside.com/board/view/?id=physiognomy&no=52237'

class RichcheckerPublicForumReadingTest(unittest.TestCase):
    def test_source_bound_in_both_original_languages(self):
        for path in (KO,EN):
            with self.subTest(path=path.name):
                text=path.read_text(encoding='utf8')
                self.assertEqual(text.count(LINK),1)
                self.assertIn('2026-11-23',text)
                self.assertIn('38%',text)
                self.assertIn('modified: 2026-11-23',text)
                self.assertIn('last_modified_at: 2026-11-23',text)
                self.assertNotIn('<img',text[text.find(LINK):text.find(LINK)+1000])
                self.assertNotIn('gall.dcinside.com/viewimage',text)
    def test_source_truth_bounded_no_personal_data_or_unverified_impact(self):
        ko=KO.read_text('utf8')
        en=EN.read_text('utf8')
        self.assertIn('익명 작성자',ko)
        self.assertIn('게시글만으로 작성자의 신원이나 실제 이용 여부를 확인할 수 없으므로',ko)
        self.assertIn('부자가 될 확률이 38%인 것은 아닙니다',ko)
        self.assertIn('An anonymous writer',en)
        self.assertIn('not independently verified user activity',en)
        self.assertIn('not the probability of becoming wealthy',en)
        self.assertNotRegex(ko+en,r'175\.203|user_id=|ip=|author_ip|http://gall')
    def test_original_languages_routes_and_source_article_dates_stay_intact(self):
        ko,en=KO.read_text('utf8'),EN.read_text('utf8')
        for key,v in [('lang','ko'),('alternate_lang','en'),('permalink','/rich-face-test/')]:
            self.assertRegex(ko,rf'(?m)^{key}: {re.escape(v)}$')
        for key,v in [('lang','en'),('alternate_lang','ko'),('permalink','/rich-face-test-en/')]:
            self.assertRegex(en,rf'(?m)^{key}: {re.escape(v)}$')
        self.assertRegex(ko,r'(?m)^date: 2026-09-12$')
        self.assertRegex(en,r'(?m)^date: 2026-11-14$')
        self.assertIn('Richchecker PR #3',en)
        self.assertIn('Richchecker PR #3',ko)

if __name__=='__main__':unittest.main()
