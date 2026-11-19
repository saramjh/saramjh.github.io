"""Keep portfolio project thumbnail links inside the mobile card grid."""
from pathlib import Path
import re
import unittest

CSS = Path(__file__).resolve().parents[1] / "assets/css/portfolio.css"


class MobileProjectImageBoundsTest(unittest.TestCase):
    def test_very_narrow_mobile_thumbnail_width_is_constrained(self):
        css = CSS.read_text(encoding="utf-8")
        rule = re.search(
            r"@media\s*\(max-width:\s*560px\)\s*\{\s*"
            r"\.portfolio-body\s+\.folio\s+\.folio-project-image\s*\{([^{}]+)\}",
            css,
        )
        self.assertIsNotNone(rule, "Missing scoped project-image mobile overflow guard")
        declarations = dict(
            (name.strip(), value.strip())
            for name, value in re.findall(r"([a-z-]+)\s*:\s*([^;]+)", rule.group(1))
        )
        self.assertEqual(declarations.get("width"), "100%")
        self.assertEqual(declarations.get("min-width"), "0")
        self.assertEqual(declarations.get("box-sizing"), "border-box")


if __name__ == "__main__":
    unittest.main()
