"""Browser geometry regression for portfolio design system and legacy theme collisions.
Run with: python3.9 tests/portfolio_layout_smoke.py [base_url]
Requires playwright + chromium in local development environment.
"""
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://127.0.0.1:4317'
PAGES = ('/portfolio/', '/portfolio/recognition/', '/portfolio/koreaves/', '/portfolio/space-atlas/', '/portfolio/spoonie/', '/portfolio/sigub/', '/portfolio/ai-agent-systems/', '/koreaves-external-resources-ko/')

# Match the actual confirmed recognition ledger and the article's selected IDs.
ROOT = Path(__file__).resolve().parents[1]
LEDGER = (ROOT / '_data' / 'recognitions.yml').read_text(encoding='utf-8')


def confirmed_evidence():
    records = []
    for block in re.split(r'(?m)^- id: ', LEDGER)[1:]:
        fields = dict(re.findall(r'(?m)^  (project|type|status): (.+)$', block))
        if fields.get('status') == 'confirmed':
            records.append({'id': block.splitlines()[0].strip(), **fields})
    assert records, 'No confirmed external evidence found in source ledger'
    assert len({record['id'] for record in records}) == len(records), 'Duplicate external evidence IDs'
    return records


EVIDENCE = confirmed_evidence()
POST = (ROOT / '_posts' / 'folio-koreaves-resources-ko' / '2026-11-02-folio-koreaves-resources-ko.md').read_text(encoding='utf-8')
EVIDENCE_IDS_MATCH = re.search(r'(?m)^evidence_ids: \[([^\]]+)\]$', POST)
assert EVIDENCE_IDS_MATCH, 'Milestone article evidence list missing'
POST_EVIDENCE_IDS = {value.strip() for value in EVIDENCE_IDS_MATCH.group(1).split(',')}


def expected_evidence_count(path):
    if path in ('/portfolio/', '/portfolio/recognition/'):
        return len(EVIDENCE)
    if path == '/koreaves-external-resources-ko/':
        return sum(item['project'] == 'koreaves' and item['id'] in POST_EVIDENCE_IDS for item in EVIDENCE)
    if path.startswith('/portfolio/'):
        project = path.strip('/').split('/')[-1]
        return sum(item['project'] == project for item in EVIDENCE)
    return 0

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for viewport in (390, 768, 1440):
        for path in PAGES:
            page = browser.new_page(viewport={'width': viewport, 'height': 900})
            errors = []
            page.on('pageerror', lambda exc: errors.append(f'JS: {exc}'))
            response = page.goto(BASE + path, wait_until='domcontentloaded', timeout=20000)
            assert response.status == 200, (viewport, path, response.status)
            assert page.locator('main h1').count() == 1, (viewport, path, 'h1')
            info = page.evaluate('''() => ({
              docWidth: document.documentElement.scrollWidth,
              viewportWidth: window.innerWidth,
              ads: document.querySelectorAll('script[src*="pagead2.googlesyndication.com"], meta[name="google-adsense-account"], ins.adsbygoogle').length
            })''')
            assert info['docWidth'] <= viewport + 2, (viewport, path, 'overflow', info)
            assert (info['ads'] == 0) == path.startswith('/portfolio/'), (viewport, path, 'ads', info)
            records = page.locator('.folio-evidence-item')
            expected = expected_evidence_count(path)
            assert records.count() == expected, (viewport, path, 'evidence count', expected, records.count())
            if expected:
                for record in records.all():
                    coords = record.evaluate('''e => {
                      const b=(s)=>{const r=e.querySelector(s).getBoundingClientRect();return {left:r.left,top:r.top,right:r.right,bottom:r.bottom,width:r.width,height:r.height}};
                      return {row:e.getBoundingClientRect().height, before:getComputedStyle(e,'::before').content, label:b('.folio-evidence-kind'), main:b('.folio-evidence-main'), date:e.querySelector('.folio-evidence-date')?b('.folio-evidence-date'):null};
                    }''')
                    assert coords['before'] in ('none','normal'), (viewport, path, 'spurious CSS counter', coords)
                    assert coords['main']['width'] >= 180, (viewport, path, 'collapsed evidence text', coords)
                    assert coords['row'] < (290 if viewport == 390 else 180), (viewport, path, 'excessive row height', coords)
                    if viewport >= 681:
                        assert coords['main']['left'] > coords['label']['right'], (viewport, path, 'type/content overlap', coords)
                        assert coords['main']['left'] - coords['label']['right'] <= 70 + (170 if viewport >= 1020 else 142), (viewport, path, 'phantom grid column', coords)
                        if coords['date']:
                            assert coords['date']['left'] > coords['main']['left'], (viewport, path, 'date wrong grid column', coords)
                            assert abs(coords['date']['top'] - coords['main']['top']) < 22, (viewport, path, 'date wrong row', coords)
                    else:
                        assert coords['label']['bottom'] <= coords['main']['top'], (viewport, path, 'mobile metadata overlap', coords)
                        if coords['date']:
                            assert coords['date']['top'] >= coords['main']['bottom'], (viewport, path, 'mobile date overlap', coords)
            if path == '/portfolio/':
                # Synthetic selections only. Prevent real navigation and network measurement.
                tracked = page.evaluate("""() => {
                  const cards = Array.from(document.querySelectorAll('.folio-writing-card'));
                  const calls = [];
                  const priorGtag = window.gtag;
                  const priorDoNotTrack = window.doNotTrack;
                  window.doNotTrack = '0';
                  window.gtag = function() { calls.push(Array.from(arguments)); };
                  cards.forEach(function(link) {
                    link.addEventListener('click', e => e.preventDefault(), {once:true});
                    link.click();
                  });
                  const collected = calls.slice();
                  // The existing privacy guard must suppress events for a DNT request.
                  window.doNotTrack = '1';
                  cards[0].addEventListener('click', e => e.preventDefault(), {once:true});
                  cards[0].click();
                  const countAfterDnt = calls.length;
                  // No gtag should remain a valid browsing configuration.
                  window.doNotTrack = '0';
                  window.gtag = undefined;
                  cards[0].addEventListener('click', e => e.preventDefault(), {once:true});
                  cards[0].click();
                  window.gtag = priorGtag;
                  window.doNotTrack = priorDoNotTrack;
                  return {
                    ids: cards.map(e => e.dataset.caseId),
                    hrefs: cards.map(e => e.getAttribute('href')),
                    emitted: collected,
                    countAfterDnt: countAfterDnt,
                    totalCount: calls.length
                  };
                }""")
                ids = [
                    'jekyll_og_png_ci_regression',
                    'spoonie_author_header',
                    'koreaves_resource_lists',
                    'koreaves_published_contributions'
                ]
                assert tracked['ids'] == ids, (viewport, 'portfolio case IDs', tracked)
                assert len(tracked['emitted']) == 4, (viewport, 'portfolio case events count', tracked)
                assert tracked['emitted'] == [
                    ['event', 'select_content', {
                        'content_type': 'portfolio_case_study', 'item_id': item_id
                    }] for item_id in ids
                ], (viewport, 'portfolio case source IDs', tracked)
                assert tracked['countAfterDnt'] == 4, (viewport, 'DNT guard failed', tracked)
                assert tracked['totalCount'] == 4, (viewport, 'gtag unavailable guard failed', tracked)
            if path == '/portfolio/recognition/':
                # Synthetic click: verify an event without opening a real external tab.
                evidence_event = page.evaluate("""() => {
                  const item = document.querySelector('.folio-evidence-item');
                  const link = item.querySelector('.folio-evidence-main h3 a');
                  const calls = [];
                  const prior = window.gtag;
                  window.gtag = function() { calls.push(Array.from(arguments)); };
                  link.addEventListener('click', function(e) { e.preventDefault(); }, {once: true});
                  link.click();
                  window.gtag = prior;
                  return {id: item.dataset.evidenceId, href: link.href, target: link.target, calls: calls};
                }""")
                assert evidence_event['id'] in {item['id'] for item in EVIDENCE}, (viewport, 'unknown evidence ID')
                assert evidence_event['target'] == '_blank', (viewport, 'external navigation contract')
                assert len(evidence_event['calls']) == 1, (viewport, 'GA4 event not emitted once')
                assert evidence_event['calls'][0] == ['event', 'select_content', {
                    'content_type': 'portfolio_external_evidence',
                    'item_id': evidence_event['id']
                }], (viewport, 'event lacks exact source ID')
                assert page.locator('.folio-evidence-item:visible').count() == len(EVIDENCE)
                page.locator('[data-filter="publication"]').click()
                assert page.locator('.folio-evidence-item:visible').count() == sum(item['type'] == 'publication' for item in EVIDENCE)
                page.locator('[data-filter="collaboration"]').click()
                assert page.locator('.folio-evidence-item:visible').count() == 0
                assert page.locator('#folio-filter-empty').is_visible()
                page.locator('[data-filter="all"]').click()
                assert page.locator('.folio-evidence-item:visible').count() == len(EVIDENCE)
                page.locator('.folio-evidence-list').scroll_into_view_if_needed()
                page.screenshot(path=f'/tmp/folio-evidence-fixed-{viewport}.png')
            if errors:
                raise AssertionError((viewport,path,errors))
            print('PASS',viewport,path)
            page.close()
    # Root-portfolio analytics must respect an explicit browser Do Not Track signal.
    # No real analytics network calls or production clicks are made by this check.
    for dnt in ('1', '0'):
        context = browser.new_context()
        init = """(() => {
          const dnt = '__DNT__';
          Object.defineProperty(navigator, 'doNotTrack', {configurable:true, get: () => dnt});
          window.doNotTrack = dnt;
          window.requestIdleCallback = (callback) => {
            callback({didTimeout:false,timeRemaining:() => 50});
            return 1;
          };
        })();""".replace('__DNT__', dnt)
        context.add_init_script(init)
        page = context.new_page()
        page.route('https://www.googletagmanager.com/**', lambda route: route.abort())
        page.route('https://www.clarity.ms/**', lambda route: route.abort())
        response = page.goto(BASE + '/portfolio/', wait_until='domcontentloaded', timeout=20000)
        assert response.status == 200, ('DNT browser setup', dnt)
        info = page.evaluate("""() => ({
          dnt: navigator.doNotTrack,
          ga: document.querySelectorAll('script[data-blog-ga]').length,
          clarity: document.querySelectorAll('script[data-blog-clarity]').length,
          hasGtag: typeof window.gtag === 'function'
        })""")
        assert info['dnt'] == dnt, ('DNT browser signal', info)
        assert info['ga'] == (0 if dnt == '1' else 1), ('GA loader DNT contract', info)
        assert info['clarity'] == (0 if dnt == '1' else 1), ('Clarity DNT contract', info)
        assert info['hasGtag'] == (dnt == '0'), ('gtag DNT contract', info)
        print('PASS root analytics DNT', dnt, info)
        context.close()
    browser.close()
print('PASS all browser geometry checks')
