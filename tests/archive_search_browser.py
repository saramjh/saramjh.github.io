"""Rendered archive search, browse fallback, reload and index-failure regression."""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:4317"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        channel=os.environ.get("BLOG_TEST_BROWSER_CHANNEL") or None,
    )
    for width in (375, 1440):
        page = browser.new_page(viewport={"width": width, "height": 780})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        response = page.goto(BASE + "/archive/", wait_until="domcontentloaded", timeout=20000)
        assert response.status == 200
        browse = page.locator("#archive-browse-section")
        field = page.locator("#search-input")
        assert browse.is_visible(), ("initial archive hidden", width)
        assert browse.locator("article").count() > 10
        field.fill("Spoonie")
        page.wait_for_function(
            "() => document.querySelector('#search-result-status').textContent.includes('Articles:')"
        )
        assert browse.is_hidden(), ("full archive mixed with search", width)
        assert page.locator("#search-article-section").is_visible()
        assert page.locator("#search-results li").count() > 0
        field.fill("zz-no-matches-999")
        page.wait_for_function(
            "() => document.querySelector('#search-result-status').textContent.includes('No matching')"
        )
        assert browse.is_hidden(), ("unfiltered posts below no-match result", width)
        assert page.locator("#search-results li").count() == 0
        field.fill("")
        assert browse.is_visible(), ("clearing search did not restore archive", width)
        field.fill("Spoonie")
        page.wait_for_function(
            "() => document.querySelector('#search-result-status').textContent.includes('Articles:')"
        )
        page.reload(wait_until="domcontentloaded")
        page.wait_for_function(
            "() => document.querySelector('#search-result-status').textContent.includes('Articles:')"
        )
        assert field.input_value() == "Spoonie", ("history query lost", width)
        assert browse.is_hidden(), ("restored query exposed full archive", width)
        # Native same-document Back/Forward changes the active history entry
        # without reloading this page or re-running its initial search setup.
        page.evaluate("() => history.pushState({unrelated:'keep'}, '', '#native-query')")
        field.fill("KoreAves")
        page.wait_for_function(
            "() => document.querySelector('#search-result-status').textContent.includes('Articles:')"
        )
        page.go_back()
        page.wait_for_function(
            "() => document.querySelector('#search-input').value === 'Spoonie'"
        )
        assert browse.is_hidden(), ("Back lost the archived query", width)
        page.go_forward()
        page.wait_for_function(
            "() => document.querySelector('#search-input').value === 'KoreAves'"
        )
        page.evaluate("() => history.pushState({unrelated:'keep'}, '', '#fresh-browse')")
        page.go_back()
        page.wait_for_function(
            "() => document.querySelector('#search-input').value === 'KoreAves'"
        )
        page.go_forward()
        page.wait_for_function(
            "() => document.querySelector('#search-input').value === ''"
        )
        assert browse.is_visible(), ("fresh history entry inherited stale search", width)
        assert not errors, (width, errors)
        page.close()

        offline = browser.new_page(viewport={"width": width, "height": 780})
        offline.route("**/assets/search.json", lambda route: route.abort())
        offline.goto(BASE + "/archive/", wait_until="domcontentloaded", timeout=20000)
        offline.locator("#search-input").fill("Spoonie")
        offline.wait_for_function(
            "() => document.querySelector('#search-result-status').textContent.includes('unavailable')"
        )
        assert offline.locator("#archive-browse-section").is_visible(), (
            "index failure removed the no-JS browse fallback", width
        )
        offline.close()

        no_js = browser.new_context(
            viewport={"width": width, "height": 780},
            java_script_enabled=False,
        )
        static = no_js.new_page()
        static.goto(BASE + "/archive/", wait_until="domcontentloaded", timeout=20000)
        assert static.locator("#archive-browse-section").is_visible(), (
            "dated archive missing without JS", width
        )
        no_js.close()
    browser.close()
print("PASS archive search filtered state, no-results, clear, reload, index failure, no-JS fallback")
