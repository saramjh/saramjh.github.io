"""Homepage project directory should stay accessible and responsive."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / '_layouts/home.html'
LAYOUT = ROOT / '_sass/klise/_layout.scss'
DARK = ROOT / '_sass/klise/_dark.scss'
TARGETS = ('/scratchLottery/', '/space_atlas_student/', '/richChecker/', '/richChecker-us/')

class ProjectShowcaseTests(unittest.TestCase):
    def test_semantic_directory_with_four_crawlable_destinations(self):
        html = HOME.read_text(encoding='utf-8')
        self.assertIn('<section class="project-showcase" aria-labelledby="projects-heading">', html)
        self.assertIn('<nav aria-label="Interactive projects">', html)
        self.assertIn('<ul class="project-showcase-list">', html)
        self.assertIn('</ul>', html)
        self.assertEqual(html.count('class="project-showcase-link"'), len(TARGETS))
        for href in TARGETS:
            self.assertEqual(html.count(f'href="{href}"'), 1, href)
        self.assertNotIn('<p>Interactive projects:', html)
        self.assertIn('class="project-showcase-description"', html)
        self.assertIn('class="project-showcase-arrow" aria-hidden="true"', html)
        self.assertIn('id="projects-heading"', html)

    def test_keyboard_mobile_and_dark_styles(self):
        light = LAYOUT.read_text(encoding='utf-8')
        dark = DARK.read_text(encoding='utf-8')
        self.assertIn('.project-showcase {', light)
        self.assertIn('grid-template-columns: repeat(2, minmax(0, 1fr))', light)
        self.assertIn('grid-template-columns: 1fr', light)
        self.assertIn('&:focus-visible', light)
        self.assertIn('body[data-theme="dark"]', dark)
        self.assertRegex(dark, r'(?s)\.project-showcase\s*\{')

if __name__ == '__main__':
    unittest.main()
