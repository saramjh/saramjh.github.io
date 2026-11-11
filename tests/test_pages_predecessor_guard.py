"""No-network verification of the original Pages predecessor lookup."""
import contextlib
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import resolve_pages_predecessor as guard

A = "a" * 40
B = "b" * 40
C = "c" * 40
REPO = guard.REPOSITORY


def item(sha, deploy_id, environment="github-pages", ref="main"):
    return {"sha": sha, "id": deploy_id, "environment": environment, "ref": ref}


class PreviousPagesDeploymentTests(unittest.TestCase):
    def fetch_with(self, deployments, states):
        def fetch(path):
            if path.endswith("per_page=30"):
                return deployments
            for n, state in states.items():
                if f"/deployments/{n}/statuses?" in path:
                    return [{"state": state}]
            raise AssertionError("Unexpected API path " + path)
        return fetch

    def test_last_successful_deployment_is_not_previous_git_parent(self):
        fetch = self.fetch_with(
            [item(A, 103), item(B, 102), item(C, 101)],
            {103: "failure", 102: "success", 101: "success"},
        )
        result = guard.resolve_previous_successful_deployment(A, fetch, lambda previous, target: previous == B)
        self.assertEqual(result, (B, 102))

    def test_identical_last_successful_sha_is_no_op_not_replay(self):
        fetch = self.fetch_with([item(A, 103)], {103: "success"})
        result = guard.resolve_previous_successful_deployment(A, fetch, lambda *_: False)
        self.assertEqual(result, (A, 103))

    def test_non_ancestor_refuses_fallback_to_arbitrary_commit(self):
        fetch = self.fetch_with([item(B, 102), item(C, 101)], {102: "success", 101: "success"})
        self.assertIsNone(guard.resolve_previous_successful_deployment(A, fetch, lambda *_: False))

    def test_missing_or_corrupt_native_status_fails_closed(self):
        self.assertIsNone(guard.resolve_previous_successful_deployment(A, lambda path: [], lambda *_: True))
        fetch = lambda path: [item(B, 103)] if path.endswith("per_page=30") else []
        self.assertIsNone(guard.resolve_previous_successful_deployment(A, fetch, lambda *_: True))
        fetch = self.fetch_with([item("not-a-sha", 103)], {103: "success"})
        self.assertIsNone(guard.resolve_previous_successful_deployment(A, fetch, lambda *_: True))

    def test_unrelated_deployment_is_ignored(self):
        fetch = self.fetch_with(
            [item(C, 104, environment="not-blog"), item(C, 103, ref="unrelated"), item(B, 102)],
            {102: "success"},
        )
        self.assertEqual(
            guard.resolve_previous_successful_deployment(A, fetch, lambda *_: True),
            (B, 102),
        )

    def test_wrong_repository_or_absent_token_is_fail_closed_no_requests(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "output"
            for variables in (
                {"GITHUB_REPOSITORY": "saramjh/unrelated", "GITHUB_TOKEN": "test"},
                {"GITHUB_REPOSITORY": REPO, "GITHUB_TOKEN": ""},
            ):
                with patch.dict(os.environ, {**variables, "GITHUB_SHA": A, "GITHUB_OUTPUT": str(output)}):
                    with patch.object(guard, "github_json", side_effect=AssertionError("no api")):
                        with contextlib.redirect_stdout(io.StringIO()):
                            self.assertEqual(guard.main(), 0)
            self.assertEqual(output.read_text().count("before_sha=\n"), 2)

    def test_native_workflow_reads_predecessor_before_deployment(self):
        source = Path(__file__).resolve().parents[1] / ".github/workflows/pages.yml"
        text = source.read_text(encoding="utf-8")
        self.assertIn("deployments: read", text)
        self.assertIn("fetch-depth: 0", text)
        self.assertLess(text.index("name: Verify last successful Pages revision"), text.index("name: Deploy"))
        self.assertIn("INDEXNOW_BEFORE_SHA: ${{ steps.predecessor.outputs.before_sha }}", text)
        self.assertNotIn("INDEXNOW_BEFORE_SHA: ${{ github.event.before }}", text)


if __name__ == "__main__":
    unittest.main()
