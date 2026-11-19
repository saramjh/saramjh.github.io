"""No-network guard for Pages search-engine notifications."""
from pathlib import Path
import unittest


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/pages.yml"


class PagesSearchEngineNotificationGateTests(unittest.TestCase):
    def test_notifications_require_manual_opt_in(self):
        lines = WORKFLOW.read_text(encoding="utf-8").splitlines()

        dispatch = lines.index("  workflow_dispatch:")
        dispatch_block = []
        for line in lines[dispatch + 1:]:
            if line and not line.startswith(" "):
                break
            dispatch_block.append(line)

        self.assertIn("    inputs:", dispatch_block)
        self.assertIn("      enable_search_engine_notifications:", dispatch_block)
        self.assertIn("        required: false", dispatch_block)
        self.assertIn("        type: boolean", dispatch_block)
        self.assertIn("        default: false", dispatch_block)

        step = lines.index("      - name: Notify Search Engines (Bing API & IndexNow)")
        step_block = []
        for line in lines[step + 1:]:
            if line.startswith("      - "):
                break
            step_block.append(line)

        self.assertIn(
            "        if: github.event_name == 'workflow_dispatch' && inputs.enable_search_engine_notifications == true",
            step_block,
        )
        self.assertIn("        run: python3 scripts/submit_search_engines.py", step_block)
        self.assertEqual(lines.count("        run: python3 scripts/submit_search_engines.py"), 1)

    def test_no_other_workflow_can_bypass_notification_gate(self):
        workflows = WORKFLOW.parent
        candidates = sorted((*workflows.glob("*.yml"), *workflows.glob("*.yaml")))
        self.assertIn(WORKFLOW, candidates)
        submitter_call = "python3 scripts/submit_search_engines.py"
        consumers = [
            path for path in candidates
            if submitter_call in path.read_text(encoding="utf-8")
        ]
        self.assertEqual(consumers, [WORKFLOW])


if __name__ == "__main__":
    unittest.main()
