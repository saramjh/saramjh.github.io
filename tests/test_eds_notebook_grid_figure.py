"""Source-bound figure must not turn a sparse GBIF example into a species range claim."""
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE_SHA='0fb26d2974897882ff3cc952727c1449026e982faa51fbda3854d7229bf40ab4'
PATH='/assets/images/dev/eds-notebook-grid-20261115'

class NotebookVisual(unittest.TestCase):
    def test_pair_links_localized_figure_and_source(self):
        for lang in ('ko','en'):
            article=next((ROOT/'_posts'/f'eds-book-bird-occurrence-notebook-preparation-{lang}').glob('*.md')).read_text('utf8')
            self.assertIn(f'{PATH}/grid-comparison-{lang}.svg',article)
            self.assertIn(f'{PATH}/grid-comparison-{lang}-mobile.svg',article)
            self.assertIn('<picture>',article)
            self.assertIn('media="(max-width: 560px)"',article)
            self.assertIn('https://github.com/saramjh/bird-records-not-absence-notebook/pull/1',article)

    def test_svg_uses_exact_same_screened_records(self):
        for lang in ('ko','en'):
          for mobile in (False,True):
            suffix='-mobile' if mobile else ''
            doc=ET.parse(ROOT / f'{PATH.lstrip("/")}/grid-comparison-{lang}{suffix}.svg').getroot()
            self.assertEqual(doc.attrib['data-source-sha256'],SOURCE_SHA)
            self.assertEqual(doc.attrib['viewBox'],'0 0 390 1000' if mobile else '0 0 1152 680')
            ns={'s':'http://www.w3.org/2000/svg'}
            self.assertIsNotNone(doc.find('s:title',ns))
            self.assertIsNotNone(doc.find('s:desc',ns))
            for scale,count in [(10,12),(50,8)]:
                group=next(e for e in doc.findall('.//s:g',ns) if e.attrib.get('data-grid-km')==str(scale))
                cells=[e for e in group.findall('s:rect',ns) if e.attrib.get('data-count')]
                self.assertEqual(len(cells),count)
                self.assertEqual(sum(int(e.attrib['data-count']) for e in cells),50)
            self.assertEqual(doc.attrib['data-selection-first-page-records'],'100')
            self.assertEqual(doc.attrib['data-records-accepted'],'50')
            self.assertEqual(doc.attrib['data-unknown-uncertainty'],'39')
            self.assertEqual(doc.attrib['data-over-threshold'],'11')

    def test_figure_is_not_misrepresented_as_range_or_doi(self):
        for lang in ('ko','en'):
          for suffix in ('','-mobile'):
            p=ROOT/f'{PATH.lstrip("/")}/grid-comparison-{lang}{suffix}.svg'
            s=p.read_text('utf8')
            self.assertIn('6c411e0b7159897b164621143bb863537a606994',s)
            self.assertNotIn('<script',s)
            self.assertNotIn('xmlns:xlink',s)
            self.assertNotIn('gbif.org/occurrence/',s)

if __name__=='__main__':unittest.main()
