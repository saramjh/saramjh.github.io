"""EDS Book's source-backed reading paths must not be displaced by a generic Python-tag match."""
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
EXPECTED={
  'en':['/koreaves-bird-evidence-atlas-en/','/koreaves-unsustainable-bird-map-en/','/koreaves-external-resources-en/'],
  'ko':['/koreaves-bird-evidence-atlas/','/koreaves-unsustainable-bird-map-ko/','/koreaves-external-resources-ko/'],
}

class RelatedReadingTests(unittest.TestCase):
    def test_existing_bilingual_eds_articles_have_exact_related_paths(self):
        for lang,urls in EXPECTED.items():
            p=next((ROOT/'_posts'/f'eds-book-bird-occurrence-notebook-preparation-{lang}').glob('*.md'))
            fm=p.read_text('utf8').split('---',2)[1]
            related=re.search(r'(?ms)^related_urls:\s*\n((?:\s+-\s+[^\n]+\n)+)',fm)
            self.assertIsNotNone(related,(lang,'related list missing'))
            self.assertEqual(re.findall(r'^\s+-\s+(\S+)\s*$',related.group(1),re.M),urls)
            for u in urls:
                matches=[]
                for post in (ROOT/'_posts').glob('*/*.md'):
                    t=post.read_text('utf8')[:1200]
                    if re.search(r'(?m)^permalink:\s*'+re.escape(u)+r'\s*$',t):
                        matches.append(t)
                self.assertEqual(len(matches),1,(lang,u,'must reference one real authored post'))
                self.assertRegex(matches[0],r'(?m)^lang:\s*'+lang+r'\s*$')

    def test_shared_include_uses_curated_targets_when_supplied(self):
        src=(ROOT/'_includes/related_posts.html').read_text('utf8')
        self.assertIn('page.related_urls',src)
        self.assertIn("site.posts | where: 'url', target",src)
        self.assertIn('post_lang == current_lang',src)
        self.assertIn('max_related',src)

    def test_unrelated_posts_keep_original_tag_fallback(self):
        src=(ROOT/'_includes/related_posts.html').read_text('utf8')
        self.assertIn('for post in site.posts',src)
        self.assertIn('post.tags contains tag',src)
        self.assertIn('post.url != page.url',src)

if __name__=='__main__':unittest.main()
