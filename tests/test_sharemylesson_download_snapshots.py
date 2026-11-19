"""Safeguard dated first-party snapshots of the original Share My Lesson public download counter.

These are platform-displayed values, not proven learners, adoption or impact.
No network calls or third-party PDF reuse occur in these regressions.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = (
    "https://sharemylesson.com/teaching-resource/"
    "moon-phases-predict-test-explain-interactive-grades-4-8-lesson-412086"
)


class ShareMyLessonDownloadSnapshotTests(unittest.TestCase):
    def test_original_bilingual_posts_preserve_earlier_and_later_snapshots(self):
        for lang in ("en", "ko"):
            with self.subTest(lang=lang):
                source = ROOT / "_posts" / f"space-atlas-share-my-lesson-{lang}" / (
                    f"2026-11-10-space-atlas-share-my-lesson-{lang}.md"
                )
                text = source.read_text(encoding="utf8")
                self.assertIn("date: 2026-11-10", text)
                self.assertIn("modified: 2026-11-19", text)
                self.assertIn("last_modified_at: 2026-11-19", text)
                self.assertIn(SOURCE_URL, text)
                self.assertIn(f"permalink: /space-atlas-share-my-lesson-{lang}/", text)
                self.assertIn(f"lang: {lang}", text)
                self.assertIn(
                    f"alternate_url: /space-atlas-share-my-lesson-{'ko' if lang=='en' else 'en'}/",
                    text,
                )
                self.assertIn("CC BY-NC-ND", text)
                self.assertNotIn("sharemylesson.com/sites/default/files", text)
                self.assertNotIn("\ufffd", text)
                self.assertNotIn("???", text)
                if lang == "en":
                    self.assertIn("November 13, 2026", text)
                    self.assertIn("**7 downloads**", text)
                    self.assertIn("November 19, 2026", text)
                    self.assertIn("**9 downloads**", text)
                    self.assertIn("not verified numbers of distinct educators or classroom uses", text)
                else:
                    self.assertIn("2026년 11월 13일", text)
                    self.assertIn("**다운로드 7회**", text)
                    self.assertIn("2026년 11월 19일", text)
                    self.assertIn("**다운로드 9회**", text)
                    self.assertIn("서로 다른 이용자 수나 실제 수업 활용 건수를 입증하지 않는다", text)
                    self.assertGreater(len(re.findall(r"[가-힣]", text)), 150)


if __name__ == "__main__":
    unittest.main()
