'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const archive = fs.readFileSync(path.join(root, 'archive.html'), 'utf8');
const script = fs.readFileSync(path.join(root, 'assets/js/archive-search.js'), 'utf8');
assert.match(archive, /<button\b[^>]*id="search-more-articles"[^>]*aria-controls="search-results"/);
function element(type) {
  return {
    type, hidden: true, value: '', textContent: '', title: '', href: '', children: [], listeners: {},
    set innerHTML(html) { this.value = String(html).replace(/&amp;/g, '&').replace(/&lt;/g, '<'); },
    appendChild(node) { this.children.push(...(node.type === 'fragment' ? node.children : [node])); },
    replaceChildren(...nodes) { this.children = nodes.flatMap(node => node.type === 'fragment' ? node.children : [node]); },
    addEventListener(kind, callback) { this.listeners[kind] = callback; }
  };
}
const elements = Object.fromEntries([
  'search-input', 'search-result-status', 'search-evidence-section',
  'search-article-section', 'evidence-search-results', 'search-results', 'search-more-articles'
].map(id => [id, element(id)]));
const document = {
  getElementById: id => elements[id] || null,
  createElement: element,
  createDocumentFragment: () => element('fragment')
};
const articles = Array.from({length: 25}, (_, i) => ({
  title: 'Spoonie Article ' + (i + 1), description: 'Spoonie performance', tags: 'Spoonie', url: '/spoonie-' + (i + 1) + '/'
}));
const sources = Array.from({length: 2}, (_, i) => ({
  title: 'Spoonie source ' + (i + 1), description: 'verified source', tags: 'Spoonie',
  url: '/portfolio/recognition/#evidence-spoonie-' + (i + 1)
}));
const fetch = async () => ({ok: true, json: async () => [...articles, ...sources]});
vm.runInNewContext(script, {document, fetch}, {timeout: 1000});
const loaded = async () => { await new Promise(resolve => setImmediate(resolve)); };
(async () => {
  await loaded();
  const input = elements['search-input'];
  const more = elements['search-more-articles'];
  const status = elements['search-result-status'];
  const articleList = elements['search-results'];
  const evidenceList = elements['evidence-search-results'];
  input.value = 'Spoonie';
  input.listeners.input();
  assert.equal(articleList.children.length, 10, 'initial page stays compact');
  assert.equal(evidenceList.children.length, 2, 'all evidence rows stay visible');
  assert.equal(more.hidden, false, 'readers can discover additional matches');
  assert.match(status.textContent, /10 of 25/);
  assert.match(more.textContent, /10 more articles/);
  more.listeners.click();
  assert.equal(articleList.children.length, 20);
  assert.match(status.textContent, /20 of 25/);
  more.listeners.click();
  assert.equal(articleList.children.length, 25);
  assert.equal(more.hidden, true, 'final page hides the exhausted action');
  assert.match(status.textContent, /25 of 25/);
  input.value = 'Article';
  input.listeners.input();
  assert.equal(articleList.children.length, 10, 'new query resets pagination');
  assert.equal(evidenceList.children.length, 0);
  assert.equal(more.hidden, false);
  input.value = 'unmatched-keyword';
  input.listeners.input();
  assert.equal(articleList.children.length, 0);
  assert.equal(more.hidden, true);
  input.value = '';
  input.listeners.input();
  assert.equal(articleList.children.length, 0);
  assert.equal(more.hidden, true);
  console.log('PASS archive progressive results, evidence isolation, query reset, empty query');
})().catch(error => { console.error(error); process.exitCode = 1; });
