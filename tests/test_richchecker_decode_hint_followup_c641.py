"""First-party bilingual article regression for RichChecker photo recovery updates through Nov 17.

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

    def test_november_16_kr_and_us_recovery_sources_and_deployments(self):
        pull_requests = [
            "https://github.com/saramjh/richChecker/pull/4",
            "https://github.com/saramjh/richChecker/pull/5",
            "https://github.com/saramjh/richChecker-us/pull/1",
            "https://github.com/saramjh/richChecker-us/pull/2",
        ]
        deployments = [
            "https://github.com/saramjh/richChecker/actions/runs/43821895201",
            "https://github.com/saramjh/richChecker-us/actions/runs/43824121306",
            "https://github.com/saramjh/richChecker/actions/runs/43842302246",
            "https://github.com/saramjh/richChecker-us/actions/runs/43842311161",
        ]
        for lang, source in self.parts.items():
            with self.subTest(lang=lang):
                self.assertIn("date: 2026-11-14", source)
                self.assertIn("modified: 2026-11-17", source)
                self.assertIn("last_modified_at: 2026-11-17", source)
                for link in pull_requests + deployments:
                    self.assertIn(link, source)
                self.assertIn("https://saramjh.github.io/richChecker/", source)
                self.assertIn("https://saramjh.github.io/richChecker-us/", source)
                self.assertIn("createImageBitmap", source)
                self.assertIn("heic2any@0.0.4", source)
                self.assertIn("MIT", source)
                for limit in ["20 MiB", "12 MiB", "2,200", "50MP"]:
                    self.assertIn(limit, source)
                if lang == "en":
                    for limit in ["seven seconds", "five-second", "ten seconds"]:
                        self.assertIn(limit, source)
                    self.assertIn("physical Android device", source)
                else:
                    for limit in ["7초", "5초", "10초"]:
                        self.assertIn(limit, source)
                    self.assertIn("실제 문제가 발생한 Android 기기에서 재현하지 못했고", source)
                self.assertNotIn("\ufffd", source)
                self.assertNotIn("????", source)

    def test_november_16_claims_keep_production_uncertainty_open(self):
        ko = self.parts["ko"]
        en = self.parts["en"]
        self.assertIn("실제 문제가 발생한 Android 기기에서 재현하지 못했고", ko)
        self.assertIn("운영 P0를 닫지 않는다", ko)
        self.assertIn("physical Android device", en)
        self.assertIn("production P0 remains open", en)
        self.assertIn("post-deployment window", en)
        self.assertIn("13", ko)
        self.assertIn("2", en)

    def test_november_16_tiff_recovery_and_cancellation_followup(self):
        pull_requests = [
            "https://github.com/saramjh/richChecker/pull/6",
            "https://github.com/saramjh/richChecker-us/pull/3",
        ]
        deployments = [
            "https://github.com/saramjh/richChecker/actions/runs/43888945586",
            "https://github.com/saramjh/richChecker-us/actions/runs/43888946580",
        ]
        for lang, source in self.parts.items():
            with self.subTest(lang=lang):
                for link in pull_requests + deployments:
                    self.assertIn(link, source)
                for phrase in ["38/38", "9/9", "Deflate", "tiff-worker.js", "utif.js"]:
                    self.assertIn(phrase, source)
                if lang == "ko":
                    for limit in ["8MP", "32MiB", "12MiB"]:
                        self.assertIn(limit, source)
                else:
                    for limit in ["8 MP", "32 MiB", "12 MiB"]:
                        self.assertIn(limit, source)
                if lang == "ko":
                    self.assertIn("실제 Android 기기 테스트는 아니다", source)
                    self.assertIn("운영 P0는 계속 열린 상태다", source)
                else:
                    self.assertIn("No physical Android device was used", source)
                    self.assertIn("production P0 remains open", source)

    def test_post_final_deployment_ga4_window_is_scoped_and_not_a_success_claim(self):
        for lang, source in self.parts.items():
            with self.subTest(lang=lang):
                for boundary in ["23:45 KST", "01:25 KST", "06:45", "08:25"]:
                    self.assertIn(boundary, source)
                if lang == "ko":
                    self.assertIn("두 속성 모두 일치하는 행이 없었다", source)
                    self.assertIn("짧은 조회 구간에서 행이 없었다는 사실만으로", source)
                else:
                    self.assertIn("No matching rows were returned", source)
                    self.assertIn("A zero-row result over this short interval does not establish", source)

if __name__ == "__main__":
    unittest.main()
