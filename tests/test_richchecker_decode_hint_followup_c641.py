"""First-party bilingual article regression for Nov 14 RichChecker decode hint.

This test reads only original author posts; no image, personal data, provider,
analytics service or separate product repository is accessed or modified.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "ko": ROOT / "_posts/richchecker-mobile-photo-upload-recovery-ko/2026-11-14-richchecker-mobile-photo-upload-recovery-ko.md",
    "en": ROOT / "_posts/richchecker-mobile-photo-upload-recovery-en/2026-11-14-richchecker-mobile-photo-upload-recovery-en.md",
}
COMMIT = "eede7730408b6aa2ec6afc9b2e4e5d6ab1531609"
SOURCE = "https://github.com/saramjh/richChecker/commit/" + COMMIT
DEPLOY = "https://github.com/saramjh/richChecker/actions/runs/43578267276"

class OriginalRichCheckerDecodeHintFollowup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parts = {k: p.read_text(encoding="utf-8") for k,p in SOURCES.items()}

    def test_exact_author_source_and_release_receipt(self):
        for lang, s in self.parts.items():
            with self.subTest(lang=lang):
                self.assertIn("2026-11-14", s)
                self.assertIn(SOURCE, s)
                self.assertIn(DEPLOY, s)

    def test_bounded_failure_only_16_byte_hint_and_fallback(self):
        for lang, s in self.parts.items():
            with self.subTest(lang=lang):
                for phrase in ["HEIC", "TIFF", "16", "250", "File.slice", "image_decode"]:
                    self.assertIn(phrase, s)

    def test_no_actual_android_device_success_claim(self):
        self.assertIn("실제 안드로이드 기기에서 해결됐다는 증거는 아직 없습니다", self.parts["ko"])
        self.assertIn("does not establish a fix on affected Android devices", self.parts["en"])

    def test_original_permalinks_and_context_still_exist(self):
        self.assertIn("permalink: /richchecker-mobile-photo-upload-recovery-ko/", self.parts["ko"])
        self.assertIn("permalink: /richchecker-mobile-photo-upload-recovery-en/", self.parts["en"])
        for s in self.parts.values():
            self.assertIn("FileReader.readAsDataURL(file)", s)
            self.assertIn("https://saramjh.github.io/richChecker/", s)

if __name__ == "__main__":
    unittest.main()
