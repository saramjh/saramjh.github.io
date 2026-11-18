"""The Nov19 incident must be explained without creating a new script consumer."""
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
POSTS = {
    "en": ROOT / "_posts/indexnow-image-page-scope-en/2026-11-10-indexnow-image-page-scope-en.md",
    "ko": ROOT / "_posts/indexnow-image-page-scope-ko/2026-11-10-indexnow-image-page-scope-ko.md",
}
HISTORIC_REFERENCES = {
    "https://github.com/saramjh/saramjh.github.io/pull/208",
    "https://github.com/saramjh/saramjh.github.io/pull/209",
    "https://github.com/saramjh/saramjh.github.io/actions/runs/44386020085",
    "https://github.com/saramjh/saramjh.github.io/actions/runs/44387509083",
}

class BilingualFollowup(unittest.TestCase):
    def test_source_bound_note_with_no_extra_js_filename_reference(self):
        for lang, path in POSTS.items():
            with self.subTest(lang=lang):
                text = path.read_text(encoding="utf-8")
                # These articles themselves caused a false positive when read as
                # script consumers. Preserve exactly one existing inline mention.
                self.assertEqual(text.count("portfolio.js"), 1)
                self.assertEqual(text.count("`assets/js/portfolio.js`"), 1)
                self.assertEqual(text.count("<script"), 0)
                for link in HISTORIC_REFERENCES:
                    self.assertIn(link, text)
                self.assertIn("195", text)
                self.assertIn("11", text)
                self.assertIn("HTTP 200", text)
                self.assertNotIn("\ufffd", text)
                if lang == "ko":
                    self.assertRegex(text, r"[가-힣]{2,}")
                self.assertRegex(text, r"(?m)^layout: default$")
                self.assertRegex(text, rf"(?m)^lang: {lang}$")
                self.assertIn(f"/indexnow-image-page-scope-{'ko' if lang=='en' else 'en'}/", text)

    def test_no_new_posts_or_original_headline_change(self):
        en = POSTS["en"].read_text(encoding="utf-8")
        ko = POSTS["ko"].read_text(encoding="utf-8")
        self.assertIn('title: "One image change sent 120 URLs to IndexNow"', en)
        self.assertIn('title: "이미지 한 장을 바꿨는데 IndexNow에는 URL 120개가 전송됐다"', ko)
        self.assertIn("42760722178", en)
        self.assertIn("42760722178", ko)

if __name__=="__main__":
    unittest.main()
