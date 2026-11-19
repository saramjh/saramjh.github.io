"""Original Logitech macOS 2026 patch instructions must stay accurate and legible."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "en": ROOT / "_posts/en-logi-option-infinite-loading-solution/2026-01-07-en-logi-option-infinite-loading-solution.md",
    "ko": ROOT / "_posts/kr-logi-option-infinite-loading-solution/2026-01-07-kr-logi-option-infinite-loading-solution.md",
}
INSTALLER = "https://download01.logi.com/web/ftp/pub/techsupport/optionsplus/logioptionsplus_installer.zip"
OFFICIAL = "https://www.logitech.com/blog/2026/01/07/restoring-access-to-options-and-g-hub-on-macos/"


class LogitechMacPatchInstructions(unittest.TestCase):
    def test_original_source_links_and_bilingual_frontmatter(self):
        for lang, file in PAGES.items():
            with self.subTest(lang=lang):
                text = file.read_text(encoding="utf-8")
                self.assertIn(f"lang: {lang}", text)
                self.assertIn("alternate_lang: " + ("ko" if lang == "en" else "en"), text)
                self.assertIn("alternate_url:", text)
                self.assertIn("2026-01-07", text)
                self.assertEqual(text.count(f"]({INSTALLER})"), 1)
                self.assertEqual(text.count(f"]({OFFICIAL})"), 1)
                self.assertNotIn(f"[{INSTALLER}]({INSTALLER})", text)
                self.assertNotIn("\ufffd", text)
                self.assertFalse(re.search(r"\?{3,}", text))
                if lang == "ko":
                    self.assertTrue(re.search(r"[가-힣]", text))

    def test_do_not_uninstall_warning_preserves_profiles(self):
        en = PAGES["en"].read_text(encoding="utf-8")
        ko = PAGES["ko"].read_text(encoding="utf-8")
        self.assertIn("Do not uninstall", en)
        self.assertIn("profiles", en)
        self.assertIn("customizations", en)
        self.assertIn("삭제하지 마세요", ko)
        self.assertIn("사용자 설정", ko)
        self.assertNotIn("overwrite or reinstall it", en)
        self.assertNotIn("덮어쓰거나 재설치하는 것을 권장합니다", ko)

    def test_original_patch_scope_and_verified_incident(self):
        for lang, file in PAGES.items():
            with self.subTest(lang=lang):
                text = file.read_text(encoding="utf-8")
                self.assertIn("macOS 26", text)
                self.assertIn("macOS 15", text)
                self.assertIn("macOS 14", text)
                self.assertIn("macOS 13", text)
                self.assertNotIn("authentication process at startup", text)
                self.assertNotIn("인증 과정에서 멈춰", text)


if __name__ == "__main__":
    unittest.main()
