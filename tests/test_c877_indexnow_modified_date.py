"""Keep the actual Nov19 revision date consistent across JSON-LD, OG and sitemap."""
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
POSTS = [
    ROOT / "_posts/indexnow-image-page-scope-en/2026-11-10-indexnow-image-page-scope-en.md",
    ROOT / "_posts/indexnow-image-page-scope-ko/2026-11-10-indexnow-image-page-scope-ko.md",
]

class ModifiedDate(unittest.TestCase):
    def test_updated_articles_preserve_initial_date_and_report_actual_revision(self):
        for p in POSTS:
            with self.subTest(p=p.name):
                text = p.read_text(encoding="utf-8")
                frontmatter = text.split("---",2)[1]
                values = dict(re.findall(r"(?m)^(date|modified|last_modified_at):\s*(\S+)\s*$",frontmatter))
                self.assertEqual(values["date"],"2026-11-10")
                self.assertEqual(values["modified"],"2026-11-19")
                self.assertEqual(values["last_modified_at"],"2026-11-19")
                self.assertEqual(text.count("portfolio.js"),1)
                self.assertIn("44386020085",text)
                self.assertIn("44387509083",text)
                self.assertNotIn("\ufffd",text)

    def test_existing_jekyll_templates_use_corresponding_frontmatter_keys(self):
        header = (ROOT/"_includes/header.html").read_text(encoding="utf-8")
        schema = (ROOT/"_includes/seo_schema.html").read_text(encoding="utf-8")
        config = (ROOT/"_config.yml").read_text(encoding="utf-8")
        self.assertIn("page.modified | default: page.date",header)
        self.assertIn("page.modified | default: page.date",schema)
        self.assertIn("- jekyll-sitemap",config)

if __name__ == "__main__":
    unittest.main()
