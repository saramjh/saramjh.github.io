"""Keep context-specific original Dev writing accessible from AI Agent Systems."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "_projects/ai-agent-systems.md"
SOURCES = {
    "/en-ai-coding-context-continuity-cokacremote/":
        ROOT / "_posts/en-ai-coding-context-continuity-cokacremote/2026-10-05-en-ai-coding-context-continuity-cokacremote.md",
    "/en-impeccable-review-ai-ui-design/":
        ROOT / "_posts/en-impeccable-review-ai-ui-design/2026-10-05-en-impeccable-review-ai-ui-design.md",
}


class AIAgentCaseRelatedSources(unittest.TestCase):
    def test_precise_first_party_source_links_exist_and_are_contextual(self):
        case = CASE.read_text(encoding="utf8")
        self.assertIn("## Further reading", case)
        section = case.split("## Further reading", 1)[-1]
        for url, target in SOURCES.items():
            self.assertEqual(section.count(f"]({url})"), 1, url)
            source = target.read_text(encoding="utf8")
            self.assertRegex(source, re.compile(r"(?m)^permalink: " + re.escape(url) + r"$"))
            self.assertRegex(source, r"(?m)^lang: en$")
        self.assertRegex(section.lower(), r"context|resume|session")
        self.assertRegex(section.lower(), r"design|ui|detector|critique")
        self.assertIn("browser-harness engineering write-up", section)

    def test_links_are_to_dev_articles_not_to_independent_project_routes(self):
        case = CASE.read_text(encoding="utf8")
        section = case.split("## Further reading", 1)[-1]
        self.assertNotIn("https://spaceatlasedu.org/", section)
        self.assertNotIn("https://spoonie.kr/", section)
        self.assertNotIn("/recipeCalc/", section)
        self.assertNotIn("/scratchLottery/", section)
        self.assertNotIn("Google ranking", section)
        self.assertNotIn("improved conversion", section)


if __name__ == "__main__":
    unittest.main()
