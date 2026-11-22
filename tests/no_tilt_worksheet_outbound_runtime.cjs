'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('assets/js/no-tilt-worksheet-outbound.js', 'utf8');

function fixture(lang) {
  const calls = [];
  const exact = 'https://spaceatlasedu.org/assets/handouts/earth-seasons-no-tilt.html';
  const links = [
    exact,
    exact + '?utm_source=example#handout',
    exact + '#print',
    'https://spaceatlasedu.org/assets/handouts/earth-seasons-no-tilt.htm',
    exact + '.evil',
    'https://spaceatlasedu.org/assets/handouts/earth-seasons-no-tilt.html/extra',
    'http://spaceatlasedu.org/assets/handouts/earth-seasons-no-tilt.html',
    'https://spaceatlasedu.org.evil.example/assets/handouts/earth-seasons-no-tilt.html',
    'https://attacker@spaceatlasedu.org/assets/handouts/earth-seasons-no-tilt.html',
    'https://attacker.example/?next=' + encodeURIComponent(exact),
    'https://spaceatlasedu.org/earth/seasons/',
    '/assets/handouts/earth-seasons-no-tilt.html',
    'javascript:alert(1)'
  ].map(href => ({
    href, onClick: null,
    getAttribute(name) { return name === 'href' ? this.href : null; },
    addEventListener(name, handler) {
      assert.equal(name, 'click');
      assert.equal(this.onClick, null);
      this.onClick = handler;
    },
    click() {
      let prevented = false;
      this.onClick?.({preventDefault() { prevented = true; }});
      assert.equal(prevented, false, 'Navigation must remain unchanged');
    }
  }));
  const document = {
    documentElement: {lang},
    querySelectorAll(selector) {
      assert.equal(selector, 'main a[href]');
      return links;
    }
  };
  const navigator = {doNotTrack: '0', msDoNotTrack: '0'};
  const window = {doNotTrack: '0', gtag(...args) { calls.push(args); }};
  vm.runInNewContext(source, {document, navigator, window, URL}, {timeout: 1000});
  return {calls, links, window, navigator};
}
for (const lang of ['ko', 'en']) {
  const t = fixture(lang);
  assert.equal(t.calls.length, 0, 'No synthetic impression or pageview');
  assert.equal(t.links.filter(x => typeof x.onClick === 'function').length, 3,
    'Only exact resource HTTPS host and path, allowing query/fragment');
  t.links.forEach(x => x.click());
  assert.deepEqual(JSON.parse(JSON.stringify(t.calls)), Array.from({length: 3}, () => [
    'event', 'no_tilt_worksheet_select',
    {resource_id: 'space_atlas_no_tilt_worksheet', article_lang: lang}
  ]));
  for (const [o, key] of [[t.window,'doNotTrack'],[t.navigator,'doNotTrack'],[t.navigator,'msDoNotTrack']]) {
    o[key] = '1';
    t.links[0].click();
    assert.equal(t.calls.length, 3, key + ' DNT must suppress events');
    o[key] = '0';
  }
  t.window.gtag = undefined;
  t.links[0].click();
  assert.equal(t.calls.length, 3, 'Missing GA client must suppress event');
}
for (const lang of ['ja', '', 'ko-KR']) {
  const t = fixture(lang);
  assert.equal(t.links.filter(x => x.onClick !== null).length, 0,
    'Only the two original article locales are supported');
}
console.log('PASS no-tilt-worksheet-outbound exact host/path, real clicks only, privacy, DNT, nonblocking navigation, two locales');
