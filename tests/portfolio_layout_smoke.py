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
    browser.close()
print('PASS all browser geometry checks')
