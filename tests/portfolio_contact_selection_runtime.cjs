'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const src = fs.readFileSync('assets/js/portfolio.js', 'utf8');
const home = fs.readFileSync('portfolio/index.html', 'utf8');
const project = fs.readFileSync('_layouts/project.html', 'utf8');
const config = fs.readFileSync('_config.yml', 'utf8');
assert.ok(config.includes('email: devtestudinidae@gmail.com # public contact email'));
for (const markup of [home, project]) {
  assert.ok(markup.includes('class="folio-contact-cta"') || markup.includes('class="folio-text-cta folio-contact-cta"'));
  assert.ok(markup.includes('href="mailto:{{ site.author.email | escape }}"'));
}
const selector = '.folio-contact-cta[href^="mailto:"]';
class Link {
  constructor(href, surface) {this.href = href;this.surface = surface;this.listeners = [];}
  getAttribute(key) {return key === 'href' ? this.href : null;}
  closest(key) {
    if (key === '.folio-hero') return this.surface === 'portfolio_home' ? {} : null;
    if (key === '.folio-next') return this.surface === 'project_case' ? {} : null;
    throw Error('Unexpected containment query: ' + key);
  }
  addEventListener(type, callback) {assert.equal(type, 'click');this.listeners.push(callback);}
  click() {
    let prevented = false;
    this.listeners.forEach(fn => fn({preventDefault() {prevented = true;}}));
    assert.equal(prevented, false, 'The original mailto: destination must work normally');
  }
}
function harness() {
  const links = [
    new Link('mailto:devtestudinidae@gmail.com', 'portfolio_home'),
    new Link('mailto:devtestudinidae@gmail.com', 'project_case'),
    new Link('mailto:wrong@example.invalid', 'project_case'),
    new Link('mailto:devtestudinidae@gmail.com', 'other'),
    new Link('https://example.invalid/contact', 'portfolio_home'),
    new Link('mailto:devtestudinidae@gmail.com?subject=From%20my%20site', 'portfolio_home')
  ];
  const calls = [];
  const document = {querySelectorAll(key) {
    if (key === selector) return links;
    if ([
      '.folio-evidence-item',
      '.folio-writing-card[data-case-id]',
      '.folio-project-page .folio-project-header .folio-primary-cta[href]',
      '.folio-project-page .folio-project-article a[href], .folio-project-page .folio-project-header .folio-text-cta[href]',
      '.folio-filter',
      '#folio-records .folio-evidence-item'
    ].includes(key)) return [];
    throw Error('Unknown DOM query: ' + key);
  }};
  const navigator={doNotTrack:'0',msDoNotTrack:'0'};
  const window={doNotTrack:'0',gtag:(...args)=>calls.push(args)};
  vm.runInNewContext(src, {document,navigator,window,Array}, {timeout:1000});
  return {links,calls,navigator,window};
}
const t = harness();
assert.deepEqual(t.links.map(l=>l.listeners.length),[1,1,0,0,0,0], 'Only two exact owner CTA surfaces are measured');
assert.equal(t.calls.length,0,'No event from page load');
t.links.forEach(l=>l.click());
assert.deepEqual(JSON.parse(JSON.stringify(t.calls)),[
  ['event','developer_contact_link_select',{contact_surface:'portfolio_home'}],
  ['event','developer_contact_link_select',{contact_surface:'project_case'}]
]);
assert.ok(t.calls.every(([, , fields]) => Object.keys(fields).length === 1), 'No email, page URL, address, source text or visitor data in payload');
for (const [obj,key] of [[t.window,'doNotTrack'],[t.navigator,'doNotTrack'],[t.navigator,'msDoNotTrack']]) {
  obj[key] = '1';
  t.links[0].click();
  assert.equal(t.calls.length, 2, key + ' DNT must suppress tracking');
  obj[key] = '0';
}
t.window.gtag=undefined;t.links[0].click();
assert.equal(t.calls.length,2,'Absent GA4 must not affect original email link');
console.log('PASS contact selection only: 2 exact CTA sources, no PII/delivery claim, DNT, no intercepted mailto');
