"""Validate source-backed modification metadata for five updated Dev articles."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "_posts/ai-coding-context-continuity-cokacremote/2026-10-05-ai-coding-context-continuity-cokacremote.md": "2026-10-05",
    "_posts/en-ai-coding-context-continuity-cokacremote/2026-10-05-en-ai-coding-context-continuity-cokacremote.md": "2026-10-05",
    "_posts/impeccable-review-ai-ui-design/2026-10-05-impeccable-review-ai-ui-design.md": "2026-10-05",
    "_posts/en-impeccable-review-ai-ui-design/2026-10-05-en-impeccable-review-ai-ui-design.md": "2026-10-05",
    "_posts/recipe-scaling-application/2024-09-03-recipe-scaling-application.md": "2024-09-03",
}

class FiveRevisionDates(unittest.TestCase):
    def test_exact_source_revision_dates(self):
        for path, first_published in CASES.items():
            with self.subTest(path=path):
                article = (ROOT/path).read_text(encoding="utf-8")
                self.assertTrue(article.startswith("---\n"))
                frontmatter = article.split("---",2)[1]
                fields = dict(re.findall(r"(?m)^(date|modified|last_modified_at):\s*(\S+)",frontmatter))
                self.assertEqual(fields["date"],first_published)
                self.assertEqual(fields["modified"],"2026-11-19")
                self.assertEqual(fields["last_modified_at"],"2026-11-19")
                self.assertEqual(article.count("permalink:"),1)
                self.assertNotIn("\ufffd",article)

    def test_existing_schema_and_og_templates_use_correct_key(self):
        self.assertIn("page.modified | default: page.date",(ROOT/"_includes/seo_schema.html").read_text(encoding="utf-8"))
        self.assertIn("page.modified | default: page.date",(ROOT/"_includes/header.html").read_text(encoding="utf-8"))
        self.assertIn("- jekyll-sitemap",(ROOT/"_config.yml").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
