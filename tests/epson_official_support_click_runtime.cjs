'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('assets/js/epson-official-support-click.js', 'utf8');

function fixture(lang) {
  const calls = [];
  const hrefs = [
    'https://epson.com/support/epson-ink-pad-reset-utility-faqs',
    'https://epson.com/support/wa00369?utm_source=article',
    'https://epson.com/support/wa00369/',
    'https://www.epson.co.kr/faq/SPT_C11CG88513~EKL_FAQ_0871',
    'https://www.epson.co.kr/cs?lang=ko',
    'https://www.epson.co.kr/cs.evil',
    'https://www.epson.co.kr.evil.example/cs',
    'http://www.epson.co.kr/cs',
    'https://www.epson.co.kr/faq/other',
    'https://epson.com/support/wa00369.evil',
    'https://epson.com.evil.example/support/wa00369',
    'https://example.org/?next=https://epson.com/support/wa00369',
    'http://epson.com/support/wa00369',
    'https://epson.com/support/other',
    '/portfolio/',
    'javascript:alert(1)'
  ];
  const links = hrefs.map(href => ({
    href,
    handler: null,
    getAttribute(key) { return key === 'href' ? this.href : null; },
    addEventListener(type, cb) { assert.equal(type, 'click'); this.handler = cb; },
    click() {
      let prevented = false;
      this.handler?.({preventDefault() { prevented = true; }});
      assert.equal(prevented, false, 'Never block link navigation');
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
for (const lang of ['ko','en']) {
  const h = fixture(lang);
  assert.equal(h.calls.length, 0, 'No impression or synthetic event');
  h.links.forEach(a => a.click());
  assert.deepEqual(JSON.parse(JSON.stringify(h.calls)), [
    ['event', 'epson_support_reference_select', {reference_id:'ink_pad_faq', article_lang:lang}],
    ['event', 'epson_support_reference_select', {reference_id:'waste_ink_service', article_lang:lang}],
    ['event', 'epson_support_reference_select', {reference_id:'waste_ink_service', article_lang:lang}],
    ['event', 'epson_support_reference_select', {reference_id:'kr_l3106_maintenance', article_lang:lang}],
    ['event', 'epson_support_reference_select', {reference_id:'kr_customer_support', article_lang:lang}]
  ]);
  assert.ok(h.calls.every(([, , payload]) => Object.keys(payload).sort().join(',') === 'article_lang,reference_id'),
    'GA4 payload contains only an allowlisted category and a source language');
  for (const [object,key] of [[h.window,'doNotTrack'],[h.navigator,'doNotTrack'],[h.navigator,'msDoNotTrack']]) {
    object[key]='1';
    h.links[0].click();
    assert.equal(h.calls.length,5, key+' DNT must suppress events');
    object[key]='0';
  }
  h.window.gtag=undefined;
  h.links[0].click();
  assert.equal(h.calls.length,5,'No GA4 client means no event');
}
console.log('epson-official-support-click: PASS scoped link selection, private payload, DNT, no navigation blocking');
