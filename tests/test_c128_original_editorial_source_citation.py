"""One original third-party editorial citation, not a new byline or partnership."""
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LEDGER=(ROOT/'_data/recognitions.yml').read_text('utf8')
EN=(ROOT/'portfolio/recognition/index.html').read_text('utf8')
KO=(ROOT/'portfolio/recognition/ko/index.html').read_text('utf8')
COMP=(ROOT/'_includes/portfolio-evidence.html').read_text('utf8')
SOURCE_URL='https://dailykorea.net/en/travel/suncheon-bay-first-birdwatching/'
KO_URL='https://dailykorea.net/ko/travel/suncheon-bay-first-birdwatching/'
ID='daily-korea-suncheon-koreaves-citation'

class OriginalDailyKoreaEditorialSourceCitationTests(unittest.TestCase):
    def test_one_original_article_cited_in_one_source_record(self):
        blocks=re.split(r'(?m)^- id: ',LEDGER)[1:]
        self.assertEqual(len(blocks),31)
        self.assertEqual(len({b.splitlines()[0] for b in blocks}),31)
        citations=[b for b in blocks if re.search(r'(?m)^  type: citation$',b)]
        self.assertEqual(len(citations),1)
        record=citations[0]
        self.assertTrue(record.startswith(ID+'\n'))
        for required in (
          '  project: koreaves','  status: confirmed',
          '  date: 2026-11-19',
          '  source: "Daily Korea"',
          '  type: citation',
          '  url: "'+SOURCE_URL+'"',
          '  mirror_url: "'+KO_URL+'"',
          '  case_en: "/koreaves-external-resources-en/"',
          '  case_ko: "/koreaves-external-resources-ko/"',
          '  verified_at: "2026-11-23"',
          'not a developer byline',
          '기고자 표기',
          'not a developer byline, endorsement or measured use',
        ):
          self.assertIn(required,record)
        self.assertNotIn('Jihun Oh',record)
        self.assertNotIn('type: collaboration',record)
        self.assertNotIn('  image:',record)
        self.assertNotIn('????',record)
        self.assertNotIn('\ufffd',record)

    def test_both_original_articles_already_cover_editorial_context(self):
        en=(ROOT/'_posts/folio-koreaves-resources-en/2026-11-02-folio-koreaves-resources-en.md').read_text('utf8')
        ko=(ROOT/'_posts/folio-koreaves-resources-ko/2026-11-02-folio-koreaves-resources-ko.md').read_text('utf8')
        self.assertIn(SOURCE_URL,en)
        self.assertIn(KO_URL,ko)
        self.assertIn('My contribution was a fact-check',en)
        self.assertIn('내 역할은 지도 해석에 대한 사실 검토',ko)

    def test_original_30_unchanged_classifications_and_bilingual_archive_index(self):
        recs=re.split(r'(?m)^- id: ',LEDGER)[1:]
        types=[re.search(r'(?m)^  type: (\S+)$',b).group(1) for b in recs]
        projects=[re.search(r'(?m)^  project: (\S+)$',b).group(1) for b in recs]
        self.assertEqual({t:types.count(t) for t in set(types)},{
           'publication':7,'coverage':1,'citation':1,'listing':21,'dataset_record':1})
        self.assertEqual({n:projects.count(n) for n in set(projects)},{
           'koreaves':16,'space-atlas':11,'spoonie':3,'scratch-lottery':1})
        for page,name,label in ((EN,'EN','Source citations'),(KO,'KO','자료 인용')):
            self.assertIn('data-filter="citation"',page,name)
            self.assertIn('>'+label+'</button>',page,name)
            self.assertEqual(page.count('{% include portfolio-evidence.html type="citation" %}'),1)
            self.assertIn('type="publication"',page)
            self.assertIn('type="coverage"',page)
            self.assertIn('type="listing"',page)
        self.assertEqual(COMP.count("{% when 'citation' %}"),4)
        self.assertIn('record.id | escape',COMP)
        self.assertIn('record.detail_ko',COMP)
        self.assertIn('record.url | escape',COMP)

if __name__=='__main__':
 unittest.main()
