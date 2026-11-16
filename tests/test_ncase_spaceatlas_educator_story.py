"""First-party bilingual educator-discovery case study; no fabricated adoption claims."""
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLUG = "space-atlas-educator-discovery"
MEDIA = ROOT / "assets" / "img" / "dev-ncase-spaceatlas-educator-20261116"


class SpaceAtlasEducatorDiscoveryStory(unittest.TestCase):
    def test_bilingual_source_posts_are_distinct_and_linked(self):
        for lang, counterpart in (("ko", "en"), ("en", "ko")):
            with self.subTest(lang=lang):
                post = (
                    ROOT / "_posts" / f"{SLUG}-{lang}"
                    / f"2026-11-16-{SLUG}-{lang}.md"
                )
                s = post.read_text(encoding="utf-8")
                self.assertTrue(s.startswith("---" + chr(10)))
                self.assertIn("date: 2026-11-16", s)
                self.assertIn("lang: " + lang, s)
                self.assertIn("published: true", s)
                self.assertIn("alternate_lang: " + counterpart, s)
                self.assertIn("alternate_url: /" + SLUG + "-" + counterpart + "/", s)
                self.assertIn("permalink: /" + SLUG + "-" + lang + "/", s)
                self.assertIn("layout: default", s)
                self.assertIn("seo:", s)
                self.assertIn("/" + SLUG + "-" + counterpart + "/", s)
                self.assertGreaterEqual(s.count(chr(10) + "## "), 3)
                self.assertIn("https://ncase.org/programs/", s)
                self.assertIn("https://sharemylesson.com/teaching-resource/moon-phases-predict-test-explain-interactive-grades-4-8-lesson-412086", s)
                self.assertIn("https://spaceatlasedu.org/moon/phases/", s)
                self.assertIn("/space-atlas-student/space-atlas-moon-phases.png", s)
                self.assertIn(f"/assets/img/dev-ncase-spaceatlas-educator-20261116/space-atlas-ncase-{lang}.png", s)
                self.assertIn("October 19, 2026" if lang == "en" else "2026년 10월 19일", s)
                self.assertNotIn(chr(0xfffd), s)
                self.assertFalse(any(ln.startswith("|") for ln in s.splitlines()))
                self.assertNotIn("NASA-certified", s)
                self.assertNotIn("NCASE approved the simulator", s)
                self.assertNotIn("classroom adoption proven", s)

    def test_self_owned_visual_assets_are_real_og_pngs(self):
        self.assertTrue(
            (ROOT / "_posts/space-atlas-student/space-atlas-moon-phases.png").is_file()
        )
        for lang in ("ko", "en"):
            with self.subTest(lang=lang):
                p = MEDIA / f"space-atlas-ncase-{lang}.png"
                b = p.read_bytes()
                self.assertGreater(len(b), 16000)
                self.assertEqual(b[:8], bytes([137, 80, 78, 71, 13, 10, 26, 10]))
                self.assertEqual(struct.unpack(">II", b[16:24]), (1200, 630))


if __name__ == "__main__":
    unittest.main()
