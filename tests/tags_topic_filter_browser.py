import os
import sys
from playwright.sync_api import sync_playwright

base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:4317"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        headless=True,
        channel=os.environ.get("BLOG_TEST_BROWSER_CHANNEL") or None,
    )
    for width in (280, 375, 1440):
        page = browser.new_page(viewport={"width": width, "height": 800})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        response = page.goto(base + "/tags/", wait_until="domcontentloaded", timeout=20000)
        assert response.status == 200
        field = page.locator("#tag-topic-query")
        panel = page.locator("#tag-topic-filter")
        tag_links = page.locator("#tag-topic-links .tag-item")
        groups = page.locator("#tag-topic-post-groups .tag-topic-group")
        assert panel.is_visible()
        assert groups.count() == tag_links.count() - 1
        assert groups.count() > 100
        assert page.locator("#tag-topic-post-groups .tag-topic-group:visible").count() == groups.count()

        field.fill("__unmatched_topic_928736")
        assert page.locator("#tag-topic-status").inner_text().startswith("0 of ")
        assert page.locator("#tag-topic-links .tag-item:visible").count() == 0
        assert page.locator("#tag-topic-post-groups .tag-topic-group:visible").count() == 0
        assert page.locator("#tag-topic-post-groups article:visible").count() == 0

        field.fill("recipe")
        matched_links = page.locator("#tag-topic-links .tag-item:visible")
        matched_groups = page.locator("#tag-topic-post-groups .tag-topic-group:visible")
        assert matched_links.count() > 0
        assert matched_groups.count() == matched_links.count()
        assert matched_groups.first.locator("h2[id]").is_visible()
        matched_links.first.click()
        assert page.evaluate("window.location.hash") != ""

        page.reload(wait_until="domcontentloaded")
        assert field.input_value() == "recipe"
        assert page.locator("#tag-topic-post-groups .tag-topic-group:visible").count() == matched_links.count()
        field.fill("")
        assert page.locator("#tag-topic-post-groups .tag-topic-group:visible").count() == groups.count()
        assert page.locator("#tag-topic-links .tag-item:visible").count() == tag_links.count()
        assert not errors, (width, errors)
        page.close()

        no_js = browser.new_context(
            viewport={"width": width, "height": 800},
            java_script_enabled=False,
        )
        static = no_js.new_page()
        fallback = static.goto(base + "/tags/", wait_until="domcontentloaded", timeout=20000)
        assert fallback.status == 200
        assert static.locator("#tag-topic-filter").is_hidden()
        assert static.locator("#tag-topic-post-groups .tag-topic-group:visible").count() == groups.count()
        assert static.locator("#tag-topic-links .tag-item:visible").count() == tag_links.count()
        no_js.close()
    browser.close()
print("PASS topic groups match search; clear/reload/hash/no-JS and 280/375/1440 widths")
