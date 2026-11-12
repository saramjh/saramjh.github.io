"""Original source-bound bilingual technical article about the PR #98 project schema bug."""
from pathlib import Path
import struct
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE='https://github.com/saramjh/saramjh.github.io/pull/98'
PR_RUN='https://github.com/saramjh/saramjh.github.io/actions/runs/43240987471'


class JekyllProjectSchemaCaseTest(unittest.TestCase):
    def source(self,lang):
        return (ROOT/f'_posts/jekyll-project-schema-date-{lang}/2026-11-13-jekyll-project-schema-date-{lang}.md').read_text(encoding='utf8')

    def test_bilingual_document_scope_and_source(self):
        for lang in ('ko','en'):
            body=self.source(lang)
            peer='en' if lang=='ko' else 'ko'
            for required in [SOURCE,PR_RUN,'https://schema.org/WebApplication',
                '/portfolio/koreaves/','/portfolio/space-atlas/','/portfolio/spoonie/',
                'WebApplication','WebPage','BlogPosting','page.date',
                "page.layout == 'project'",'2026-11-13',
                f'permalink: /jekyll-project-schema-date-{lang}/',f'lang: {lang}',
                f'alternate_lang: {peer}',f'alternate_url: /jekyll-project-schema-date-{peer}/',
                f'image: /jekyll-project-schema-date-{lang}/jekyll-schema-{lang}-og.png',
                'image_width: 1200','image_height: 630','published: true']:
                self.assertIn(required,body,(lang,required))
            self.assertNotIn('\ufffd',body)
            self.assertNotIn('????',body)
            self.assertIn('{% raw %}',body)
            self.assertIn('{% endraw %}',body)
        self.assertGreaterEqual(sum('가'<=c<='힣' for c in self.source('ko')),200)

    def test_actual_og_images_exist_are_true_png_and_are_source_owned(self):
        for lang,expected in [('en','e210815ba5dc2be583aa5c7f6e0e7cf02bac0bc3114ea49d761ba5c04c5d632f'),('ko','ff36d6c6ee3f497335f665aa164d377e54db38989952995a56e4446aa53e0acb')]:
            import hashlib
            p=ROOT/f'_posts/jekyll-project-schema-date-{lang}/jekyll-schema-{lang}-og.png'
            data=p.read_bytes()
            self.assertEqual(data[:8],b'\x89PNG\r\n\x1a\n')
            self.assertEqual(data[12:16],b'IHDR')
            self.assertEqual(struct.unpack('>II',data[16:24]),(1200,630))
            self.assertEqual(hashlib.sha256(data).hexdigest(),expected)
            self.assertIn(f'/jekyll-project-schema-date-{lang}/jekyll-schema-{lang}-og.png',self.source(lang))

    def test_project_schema_follows_current_actual_pr98_code(self):
        src=(ROOT/'_includes/seo_schema.html').read_text(encoding='utf8')
        self.assertLess(src.index("{%- if page.layout == 'project'"),src.index("{%- elsif page.date -%}"))
        self.assertIn('"mainEntity"',src)
        self.assertIn('"@type": "WebApplication"',src)
        self.assertIn("where: 'status', 'confirmed'",src)
        self.assertIn('"@type": "BlogPosting"',src)


if __name__=='__main__':
    unittest.main()
