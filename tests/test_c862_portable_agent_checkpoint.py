from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "_posts/en-ai-coding-context-continuity-cokacremote/2026-10-05-en-ai-coding-context-continuity-cokacremote.md"
KO = ROOT / "_posts/ai-coding-context-continuity-cokacremote/2026-10-05-ai-coding-context-continuity-cokacremote.md"

class PortableAgentCheckpoint(unittest.TestCase):
    def test_both_editions_have_reader_applicable_checkpoint(self):
        for path, heading in [(EN, "### A portable checkpoint for the next coding agent"), (KO, "### 다음 코딩 에이전트를 위한 인계 메모")]:
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count(heading), 1)
            section = text.split(heading, 1)[1].split("\n## ", 1)[0]
            for field in ("Goal:", "Branch / HEAD:", "Decision:", "Verified:", "Held / unknown:", "Next action:", "Evidence:"):
                self.assertIn(field, section)
            self.assertIn("git status --short", section)
            self.assertIn("git rev-parse HEAD", section)
            self.assertIn("~~~text", section)
            self.assertNotIn("\ufffd", section)
            self.assertNotIn("????", section)

    def test_edition_source_metadata_remains_reciprocal(self):
        self.assertIn("alternate_url: /ai-coding-context-continuity-cokacremote/", EN.read_text(encoding="utf-8"))
        self.assertIn("alternate_url: /en-ai-coding-context-continuity-cokacremote/", KO.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
