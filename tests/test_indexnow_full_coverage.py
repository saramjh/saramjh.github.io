"""No-network coverage for the root site's existing IndexNow notification route."""
import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from scripts import submit_search_engines as submit


class Response:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class IndexNowCoverageTests(unittest.TestCase):
    def make_urls(self, count):
        return [f"https://saramjh.github.io/post-{i:05d}/" for i in range(count)]

    def collect(self, urls, failure=None):
        calls = []

        def urlopen(req, timeout):
            calls.append((req, timeout))
            if failure is not None:
                raise failure
            return Response()

        output = io.StringIO()
        with patch.object(submit.urllib.request, "urlopen", side_effect=urlopen):
            with redirect_stdout(output):
                submit.submit_indexnow(urls)
        return calls, output.getvalue()

    def assert_payload(self, req, original_urls):
        self.assertEqual(req.full_url, "https://api.indexnow.org/indexnow")
        self.assertEqual(req.get_header("Content-type"), "application/json; charset=utf-8")
        data = json.loads(req.data.decode("utf-8"))
        self.assertEqual(data["host"], "saramjh.github.io")
        self.assertEqual(data["key"], submit.INDEXNOW_KEY)
        self.assertEqual(data["keyLocation"], f"{submit.BASE_URL}/{submit.INDEXNOW_KEY}.txt")
        self.assertEqual(data["urlList"], original_urls)

    def test_all_118_urls_including_after_100_are_sent_once(self):
        urls = self.make_urls(118)
        calls, output = self.collect(urls)
        self.assertEqual(len(calls), 1)
        self.assert_payload(calls[0][0], urls)
        self.assertIn("Batch 1/1 (118 URLs) Response 200: Accepted", output)

    def test_over_10000_splits_into_two_bounded_batches(self):
        urls = self.make_urls(10001)
        calls, output = self.collect(urls)
        self.assertEqual(len(calls), 2)
        self.assert_payload(calls[0][0], urls[:10000])
        self.assert_payload(calls[1][0], urls[10000:])
        self.assertIn("Batch 1/2 (10000 URLs) Response 200: Accepted", output)
        self.assertIn("Batch 2/2 (1 URLs) Response 200: Accepted", output)

    def test_empty_list_has_no_network_side_effect(self):
        calls, output = self.collect([])
        self.assertEqual(calls, [])
        self.assertIn("No URLs to submit", output)

    def test_uncertain_network_error_is_not_replayed(self):
        urls = self.make_urls(3)
        calls, output = self.collect(urls, failure=TimeoutError("response not known"))
        self.assertEqual(len(calls), 1)
        self.assert_payload(calls[0][0], urls)
        self.assertIn("response not known", output)
        self.assertNotIn("Response 200", output)


if __name__ == "__main__":
    unittest.main()
