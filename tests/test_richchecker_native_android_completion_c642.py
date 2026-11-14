"""Regressions for source-bound, post-release RichChecker Android GA4 case note.

Reads the original Dev bilingual blog posts only; no GA4/provider/API calls.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "ko": ROOT / "_posts/richchecker-mobile-photo-upload-recovery-ko/2026-11-14-richchecker-mobile-photo-upload-recovery-ko.md",
    "en": ROOT / "_posts/richchecker-mobile-photo-upload-recovery-en/2026-11-14-richchecker-mobile-photo-upload-recovery-en.md",
}
COMMIT = "eede7730408b6aa2ec6afc9b2e4e5d6ab1531609"

class ActualProductAndroidCompletionNote(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = {lang: p.read_text("utf-8") for lang, p in PAGES.items()}

    def test_original_version_and_ga4_native_event_semantics(self):
        for lang, text in self.data.items():
            with self.subTest(lang=lang):
                self.assertIn("2026-11-15" if lang == "ko" else "November 15", text)
                self.assertIn(COMMIT, text)
                self.assertIn("analysis_complete", text)
                self.assertIn("google / organic", text)
                self.assertIn("renderResults", text)

    def test_exact_timed_postrelease_android_counts(self):
        self.assertIn("17:58", self.data["ko"])
        self.assertIn("19시 3건", self.data["ko"])
        self.assertIn("20시 1건", self.data["ko"])
        self.assertIn("17:58", self.data["en"])
        self.assertIn("19:00 (3 events)", self.data["en"])
        self.assertIn("20:00 (1 event)", self.data["en"])
        for text in self.data.values():
            self.assertIn("Android Chrome", text)

    def test_event_not_people_nor_a_measured_repair_rate(self):
        self.assertIn("완료 이벤트 4건은 사용자 4명을 뜻하지 않습니다", self.data["ko"])
        self.assertIn("Four completion events do not represent four distinct users", self.data["en"])
        self.assertIn("기존 오류가 해결됐다는 증거는 아닙니다", self.data["ko"])
        self.assertIn("do not prove that the original Android decoding issue is resolved", self.data["en"])

    def test_keep_original_permalink_paired_languages_and_release_account(self):
        self.assertIn("permalink: /richchecker-mobile-photo-upload-recovery-ko/", self.data["ko"])
        self.assertIn("permalink: /richchecker-mobile-photo-upload-recovery-en/", self.data["en"])
        for text in self.data.values():
            self.assertIn("https://saramjh.github.io/richChecker/", text)
            self.assertIn("https://github.com/saramjh/richChecker/commit/" + COMMIT, text)
            self.assertIn("FileReader.readAsDataURL(file)", text)

if __name__ == "__main__":
    unittest.main()
