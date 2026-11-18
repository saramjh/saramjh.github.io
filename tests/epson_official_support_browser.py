"""Render the actual Jekyll pages and dispatch local, non-navigating link selections."""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:4317"
ARTICLES = {
    "ko": "/epson-waste-ink-pad-reset-without-key/",
    "en": "/en-epson-waste-ink-pad-reset-without-key/",
}
LINKS = {
    "ink_pad_faq": "https://epson.com/support/epson-ink-pad-reset-utility-faqs",
    "waste_ink_service": "https://epson.com/support/wa00369",
}

with sync_playwright() as playwright:
    channel = os.environ.get("BLOG_TEST_BROWSER_CHANNEL") or None
    browser = playwright.chromium.launch(headless=True, channel=channel)
    for lang, path in ARTICLES.items():
        for viewport in (390, 1440):
            page = browser.new_page(viewport={"width": viewport, "height": 900})
            # Synthetic browser verification never calls Analytics, Ads, or Epson.
            page.route("**/*", lambda route: route.continue_()
                       if route.request.url.startswith(BASE + "/")
                       else route.abort())
            page.add_init_script("Object.defineProperty(navigator, 'doNotTrack', {value:'0', configurable:true});")
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            response = page.goto(BASE + path, wait_until="domcontentloaded", timeout=20000)
            assert response and response.status == 200, (lang, viewport, response)
            assert page.locator('script[src="/assets/js/epson-official-support-click.js"]').count() == 1, (lang, viewport)
            events = page.evaluate("""() => {
              const links = {
                ink_pad_faq: 'https://epson.com/support/epson-ink-pad-reset-utility-faqs',
                waste_ink_service: 'https://epson.com/support/wa00369'
              };
              const values = [];
              const oldGtag = window.gtag;
              const oldDnt = window.doNotTrack;
              window.gtag = (...args) => values.push(args);
              window.doNotTrack = '0';
              for (const [id, href] of Object.entries(links)) {
                const a = document.querySelector('main a[href="' + href + '"]');
                if (!a) throw new Error('Missing original source link ' + id);
                a.addEventListener('click', e => e.preventDefault(), {once:true});
                a.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true}));
              }
              const beforeDnt = values.length;
              window.doNotTrack = '1';
              const a = document.querySelector('main a[href="' + links.ink_pad_faq + '"]');
              a.addEventListener('click', e => e.preventDefault(), {once:true});
              a.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true}));
              window.gtag = oldGtag;
              window.doNotTrack = oldDnt;
              return {values, beforeDnt};
            }""")
            expected = [
                ["event","epson_support_reference_select",
                 {"reference_id":reference,"article_lang":lang}]
                for reference in LINKS
            ]
            assert events["values"] == expected, (lang, viewport, events)
            assert events["beforeDnt"] == 2, (lang, viewport, events)
            assert not errors, (lang, viewport, errors)
            page.close()
    browser.close()
print("epson-official-support-browser: PASS KO/EN actual Jekyll page, mobile/desktop, no external requests")
