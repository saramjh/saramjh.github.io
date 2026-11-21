"""Source-bound project WebApplication schema emitted by production Jekyll."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ProjectStructuredEvidenceTest(unittest.TestCase):
    def test_generated_project_schema_is_scoped_to_real_project_pages(self):
        schema = (ROOT / "_includes/seo_schema.html").read_text(encoding="utf8")
        self.assertIn("page.layout == 'project' and page.site_url and page.slug", schema)
        self.assertIn('"@type": "WebApplication"', schema)
        self.assertLess(schema.index("{%- if page.layout == 'project'"), schema.index("{%- elsif page.date -%}"), "Jekyll collection pages may have synthetic page.date: project branch must run first")
        self.assertIn('"subjectOf"', schema)
        self.assertIn("where: 'status', 'confirmed'", schema)
        self.assertIn("where: 'type', 'listing'", schema)
        self.assertNotIn('"endorsement"', schema)
        self.assertNotIn('"aggregateRating"', schema)
        self.assertNotIn('"review"', schema)
        self.assertNotIn('"offers"', schema)

    def test_spoonie_portfolio_connects_verified_newer_cases_bilingually(self):
        source = (ROOT / '_projects' / 'spoonie.md').read_text(encoding='utf8')
        for slug, lang in (
            ('spoonie-rsc-prefetch-20261119-en', 'en'),
            ('spoonie-rsc-prefetch-20261119-ko', 'ko'),
        ):
            self.assertIn(f'/{slug}/', source)
            posts = list((ROOT / '_posts' / slug).glob('*.md'))
            self.assertEqual(len(posts), 1)
            article = posts[0].read_text(encoding='utf8')
            self.assertIn(f'permalink: /{slug}/', article)
            self.assertIn(f'lang: {lang}', article)
            self.assertIn('published: true', article)
        for pr_number in (48, 49, 50):
            self.assertIn(f'https://github.com/saramjh/spoonie/pull/{pr_number}', source)
        self.assertIn('monthly Functions savings and reader retention have not been measured', source)

    def test_original_project_name_and_destination_are_source_bound(self):
        for slug, url, name in (
            ('koreaves', 'https://koreaves.com/', 'KoreAves'),
            ('space-atlas', 'https://spaceatlasedu.org/', 'Space Atlas'),
            ('spoonie', 'https://spoonie.kr/', 'Spoonie'),
        ):
            source=(ROOT / '_projects' / f'{slug}.md').read_text(encoding='utf8')
            self.assertIn('slug: '+slug, source)
            self.assertIn('site_url: '+url, source)
            self.assertIn('name: '+name, source)
            self.assertIn('image: /assets/images/portfolio/', source)


if __name__=='__main__':
    unittest.main()
