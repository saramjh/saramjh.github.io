"""Search index post fields must be JSON text, never HTML-escaped payloads."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (ROOT / "assets/search.json").read_text(encoding="utf-8")
RUNTIME = (ROOT / "assets/js/archive-search.js").read_text(encoding="utf-8")


class SearchJsonNativeText(unittest.TestCase):
    def test_post_strings_use_json_serializer(self):
        for field, value in (
            ("title", "post.title"),
            ("description", "post.description"),
            ("tags", "post.tags | join: ', '"),
        ):
            with self.subTest(field=field):
                pattern = r'"' + field + r'"\s*:\s*\{\{\s*' + re.escape(value) + r'\s*\|\s*jsonify\s*\}\}'
                self.assertRegex(TEMPLATE, pattern)
        self.assertNotRegex(TEMPLATE, r"post\.(?:title|description)\s*\|\s*escape")

    def test_external_evidence_is_also_native_json_text(self):
        self.assertIn("{{ record.source }} — {{ record.title }}", TEMPLATE)
        self.assertIn("{{ record.detail | jsonify }}", TEMPLATE)
        self.assertNotIn("record.detail | escape", TEMPLATE)

    def test_reader_does_not_parse_public_index_values_as_html(self):
        self.assertNotIn("decoder.innerHTML", RUNTIME)
        self.assertNotIn("createElement('textarea')", RUNTIME)


if __name__ == "__main__":
    unittest.main()
