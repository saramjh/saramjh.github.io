"""No-send browser QA: eligible Spoonie links emit selection-only events on real article pages."""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://127.0.0.1:4317'
ARTICLES = {
    '/recipe-calc-to-spoonie-origin-en/': 'spoonie_recipe',
    '/chocolate-french-toast-guide/': 'spoonie_recipe',
    '/20-minute-home-cooking-decision-guide/': 'spoonie_recipe',
    '/spoonie-editorial-curators-en/': 'spoonie_curators',
}

with sync_playwright() as playwright:
    channel = os.environ.get('BLOG_TEST_BROWSER_CHANNEL') or None
    browser = playwright.chromium.launch(headless=True, channel=channel)
    passed = 0
    for path, expected_id in ARTICLES.items():
        for viewport in (240, 390):
            page = browser.new_page(viewport={'width': viewport, 'height': 900})
            # Only first-party local Jekyll resources are allowed; no external analytics or destination requests.
            page.route('**/*', lambda route: route.continue_()
                       if route.request.url.startswith(BASE + '/') else route.abort())
            page.add_init_script("Object.defineProperty(navigator, 'doNotTrack', {value:'0', configurable:true});")
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            response = page.goto(BASE + path, wait_until='load', timeout=20000)
            assert response is not None and response.status == 200, (path, viewport, 'HTTP')
            assert page.locator('script[src="/assets/js/article-product-outbound.js"]').count() == 1, (path, viewport, 'loader')
            result = page.evaluate("""() => {
              const anchors = Array.from(document.querySelectorAll('main a[href]'));
              const allowed = anchors.find(link => {
                try {
                  const url = new URL(link.href);
                  return url.origin === 'https://spoonie.kr' &&
                    (/^\\/recipes\\/[a-f0-9-]{36}\\/?$/i.test(url.pathname) ||
                     url.pathname === '/curators');
                } catch (err) { return false; }
              });
              if (!allowed) throw Error('Missing original allowed Spoonie link');
              const values = [];
              const oldGtag = window.gtag;
              const oldDnt = window.doNotTrack;
              window.gtag = (...args) => values.push(args);
              window.doNotTrack = '0';
              allowed.addEventListener('click', e => e.preventDefault());
              allowed.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
              const beforeDnt = values.length;
              window.doNotTrack = '1';
              allowed.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
              const afterDnt = values.length;
              window.gtag = undefined;
              window.doNotTrack = '0';
              allowed.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
              const withoutGtag = values.length;
              window.gtag = oldGtag;
              window.doNotTrack = oldDnt;
              return {values,beforeDnt,afterDnt,withoutGtag,href:allowed.href,path:location.pathname};
            }""")
            assert result['values'] == [['event', 'select_content', {
                'content_type': 'developer_article_live_product',
                'content_id': expected_id,
            }]], (path, viewport, result)
            assert (result['beforeDnt'], result['afterDnt'], result['withoutGtag']) == (1,1,1), (path, viewport, result)
            assert result['path'] == path, (path, viewport, 'navigation prevention')
            assert result['href'].startswith('https://spoonie.kr/'), (path,viewport,result)
            assert not errors, (path, viewport, errors)
            page.close()
            passed += 1
    # Unrelated EUSci post does not pay the extra JavaScript load.
    page = browser.new_page()
    page.route('**/*', lambda route: route.continue_()
               if route.request.url.startswith(BASE + '/') else route.abort())
    response = page.goto(BASE + '/space-atlas-eusci-diagrams-en/', wait_until='load', timeout=20000)
    assert response and response.status == 200
    assert page.locator('script[src="/assets/js/article-product-outbound.js"]').count() == 0
    page.close()
    browser.close()
print(f'article-product-outbound-browser: PASS {passed} native DOM width cases, actual click-only allowlist, DNT and unrelated-page opt-out')
