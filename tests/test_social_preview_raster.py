"""Prevent publishing SVG-only social-card images for blog posts."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
IMAGE_LINE = re.compile(r"^image:\s*[\"\']?([^\s\"\']+)", re.MULTILINE)


class SocialPreviewRasterTest(unittest.TestCase):
    def test_post_frontmatter_does_not_point_to_svg(self):
        checked = 0
        for post in ROOT.glob("_posts/**/*.md"):
            source = post.read_text(encoding="utf-8")
            if not source.startswith("---"):
                continue
            sections = source.split("---", 2)
            if len(sections) < 3:
                continue
            match = IMAGE_LINE.search(sections[1])
            if match is None:
                continue
            checked += 1
            url = match.group(1).split("?", 1)[0].lower()
            with self.subTest(post=str(post.relative_to(ROOT))):
                self.assertFalse(
                    url.endswith(".svg"),
                    "Social image must use a raster format; inline SVG is allowed",
                )
        self.assertGreater(checked, 0, "No published blog image frontmatter found")


if __name__ == "__main__":
    unittest.main()
