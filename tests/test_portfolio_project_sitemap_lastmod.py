"""Portfolio sitemap dates must come from actual project source edits, not builds."""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

# Dates of the last verified _projects/* source changes (not deployment times).
SOURCE_LASTMOD = {
    "ai-agent-systems": "2026-11-19T00:31:29+09:00",
    "koreaves": "2026-11-17T21:18:41+09:00",
    "sigub": "2026-11-02T16:29:10+09:00",
    "space-atlas": "2026-11-17T22:14:23+09:00",
    "spoonie": "2026-11-21",
}


class ProjectSitemapLastmod(unittest.TestCase):
    def test_each_project_uses_source_change_date_not_deployment_clock(self):
        self.assertEqual(
            {p.stem for p in (ROOT / "_projects").glob("*.md")},
            set(SOURCE_LASTMOD),
        )
        for name, expected in SOURCE_LASTMOD.items():
            with self.subTest(project=name):
                source = (ROOT / "_projects" / f"{name}.md").read_text("utf8")
                self.assertTrue(source.startswith("---\n"))
                frontmatter = source.split("---\n", 2)[1]
                values = re.findall(
                    r"^last_modified_at:\s*([^\s#]+)\s*$",
                    frontmatter,
                    re.MULTILINE,
                )
                self.assertEqual(values, [expected])


if __name__ == "__main__":
    unittest.main()
