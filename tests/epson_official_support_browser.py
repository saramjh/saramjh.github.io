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
    "kr_l3106_maintenance": "https://www.epson.co.kr/faq/SPT_C11CG88513~EKL_FAQ_0871",
    "kr_customer_support": "https://www.epson.co.kr/cs",
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
                waste_ink_service: 'https://epson.com/support/wa00369',
                kr_l3106_maintenance: 'https://www.epson.co.kr/faq/SPT_C11CG88513~EKL_FAQ_0871',
                kr_customer_support: 'https://www.epson.co.kr/cs'
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
            assert events["beforeDnt"] == 4, (lang, viewport, events)
            assert not errors, (lang, viewport, errors)
            page.close()
    # Keep the original markdown table semantic while allowing narrow readers
    # to scroll all three columns without page-level horizontal overflow.
    for lang, path in ARTICLES.items():
        for viewport in (240, 280, 320, 390, 768):
            page = browser.new_page(viewport={"width": viewport, "height": 900})
            page.route("**/*", lambda route: route.continue_()
                       if route.request.url.startswith(BASE + "/")
                       else route.abort())
            response = page.goto(BASE + path, wait_until="domcontentloaded", timeout=20000)
            assert response and response.status == 200, (lang, viewport, "article")
            region = page.locator('main .overflow-table[role="region"][tabindex="0"]')
            assert region.count() == 1, (lang, viewport, "missing scroll region")
            assert region.locator('table').count() == 1, (lang, viewport, "markdown table not rendered")
            assert region.locator('th').count() == 3, (lang, viewport, "comparison headers")
            assert region.locator('tbody tr').count() == (5 if lang == 'ko' else 4), (
                lang, viewport, "original comparison body changed")
            geometry = region.evaluate("""el => {
              const wrapper = el.getBoundingClientRect();
              const table = el.querySelector('table').getBoundingClientRect();
              const before = {
                left: wrapper.left, right: wrapper.right,
                scrollWidth: el.scrollWidth, clientWidth: el.clientWidth,
                tableRight: table.right,
                documentWidth: document.documentElement.scrollWidth,
                viewport: innerWidth,
                overflow: getComputedStyle(el).overflowX
              };
              el.scrollLeft = el.scrollWidth;
              const last = el.querySelector('tbody tr:last-child td:last-child').getBoundingClientRect();
              return {...before, scrollLeft: el.scrollLeft, lastCellRight: last.right};
            }""")
            assert geometry['overflow'] == 'auto', (lang, viewport, geometry)
            assert geometry['left'] >= -1 and geometry['right'] <= viewport + 1, (
                lang, viewport, 'comparison outside viewport', geometry)
            assert geometry['documentWidth'] <= viewport + 2, (
                lang, viewport, 'page horizontal overflow', geometry)
            assert geometry['lastCellRight'] <= geometry['right'] + 1, (
                lang, viewport, 'last comparison column clipped', geometry)
            if lang == 'en' and viewport <= 280:
                assert geometry['scrollWidth'] > geometry['clientWidth'], (
                    lang, viewport, 'missing horizontal scroll', geometry)
                assert geometry['scrollLeft'] > 0, (
                    lang, viewport, 'comparison cannot reach last column', geometry)
            region.focus()
            assert region.evaluate('el => document.activeElement === el'), (
                lang, viewport, 'comparison keyboard focus unavailable')
            page.close()
            print('PASS accessible Epson comparison', lang, viewport)
    browser.close()
print("epson-official-support-browser: PASS KO/EN actual Jekyll page, mobile/desktop, no external requests")
