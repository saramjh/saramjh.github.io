"""Verified source-bound distinction between public upstream and private local extension."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'ko': ROOT / '_posts/ai-coding-context-continuity-cokacremote/2026-10-05-ai-coding-context-continuity-cokacremote.md',
    'en': ROOT / '_posts/en-ai-coding-context-continuity-cokacremote/2026-10-05-en-ai-coding-context-continuity-cokacremote.md',
}

class LocalVsUpstreamDistinctionTest(unittest.TestCase):
    def test_local_extension_not_described_as_upstream_shipped(self):
        for lang, file in SOURCES.items():
            with self.subTest(lang=lang):
                text = file.read_text(encoding='utf8')
                self.assertIn('https://github.com/kstost/cokacremote', text)
                for tool in ('project_context_bootstrap','project_context_checkpoint','project_context_recall'):
                    self.assertIn(tool, text)
                self.assertIn('2026-11-23' if lang == 'ko' else 'November 23, 2026', text)
                self.assertIn('로컬에서 덧붙인' if lang == 'ko' else 'belong to my local project-context extension', text)
                self.assertIn('그대로 설치해도 제공되지 않습니다' if lang == 'ko' else 'does not install them', text)

    def test_original_source_and_paired_public_routes_retained(self):
        for lang, file in SOURCES.items():
            with self.subTest(lang=lang):
                text = file.read_text(encoding='utf8')
                self.assertIn('date: 2026-10-05',text)
                self.assertIn('modified: 2026-11-23',text)
                self.assertIn('last_modified_at: 2026-11-23',text)
                self.assertIn('lang: ' + lang,text)
                self.assertIn('alternate_url: /'+('en-' if lang=='ko' else '')+'ai-coding-context-continuity-cokacremote/',text)
                self.assertIn('permalink: /'+('en-' if lang=='en' else '')+'ai-coding-context-continuity-cokacremote/',text)
                self.assertIn('(https://github.com/kstost/cokacremote)',text)
                self.assertNotIn('\ufffd',text)

    def test_fallback_not_promised_as_automatic_memory(self):
        ko=SOURCES['ko'].read_text('utf8')
        en=SOURCES['en'].read_text('utf8')
        self.assertIn('[수동 인계 메모]',ko)
        self.assertIn('](#다음-코딩-에이전트를-위한-인계-메모)',ko)
        self.assertIn('[portable handoff note]',en)
        self.assertIn('컨텍스트',ko)
        self.assertIn('continuity',en)

if __name__ == '__main__': unittest.main()
