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
  'search-article-section', 'evidence-search-results', 'search-results', 'search-more-articles', 'archive-browse-section'
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
const literalEntityRecord = {
  title: 'Literal &amp; text', description: 'The source intentionally contains &amp;',
  tags: 'literal &amp;', url: '/literal-entity-text/'
};
const fetch = async () => ({ok: true, json: async () => [...articles, ...sources, literalEntityRecord]});
vm.runInNewContext(script, {document, fetch}, {timeout: 1000});
const loaded = async () => { await new Promise(resolve => setImmediate(resolve)); };
(async () => {
  await loaded();
  const browse = elements['archive-browse-section'];
  const input = elements['search-input'];
  const more = elements['search-more-articles'];
  const status = elements['search-result-status'];
  const articleList = elements['search-results'];
  const evidenceList = elements['evidence-search-results'];
  browse.hidden = false; // Server-rendered archive is visible without JavaScript.
  input.value = 'Spoonie';
  input.listeners.input();
  assert.equal(browse.hidden, true, 'typing hides unrelated dated archive listings');
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
  assert.equal(browse.hidden, true, 'no-match message must not show unfiltered archive');
  input.value = '&amp;';
  input.listeners.input();
  assert.equal(articleList.children.length, 1, 'literal entity text should remain searchable without HTML parsing');
  assert.equal(articleList.children[0].children[0].textContent, 'Literal &amp; text',
    'public JSON is plain text, not HTML to decode');
  input.value = '';
  input.listeners.input();
  assert.equal(articleList.children.length, 0);
  assert.equal(more.hidden, true);
  assert.equal(browse.hidden, false, 'clearing search restores dated archive');
  // State belongs to the current history entry, not a URL or third-party
  // storage. Preserve unrelated history values and restore on script reload.
  const history = {
    state: {unrelated: 'keep'},
    calls: [],
    replaceState(next, unused) {
      assert.equal(unused, '');
      this.state = next;
      this.calls.push(next);
    }
  };
  const second = Object.fromEntries(Object.keys(elements).map(id => [id, element(id)]));
  second['archive-browse-section'].hidden = false;
  const secondDocument = {
    getElementById: id => second[id] || null,
    createElement: element,
    createDocumentFragment: () => element('fragment')
  };
  const secondWindow = {
    history, events: {},
    addEventListener(kind, callback) { this.events[kind] = callback; }
  };
  vm.runInNewContext(script, {document: secondDocument, window: secondWindow, fetch}, {timeout: 1000});
  await loaded();
  second['search-input'].value = 'Spoonie';
  second['search-input'].listeners.input();
  assert.equal(second['search-results'].children.length, 10);
  second['search-more-articles'].listeners.click();
  assert.equal(second['search-results'].children.length, 20);
  assert.equal(history.state.unrelated, 'keep');
  assert.equal(history.state.__devArchiveSearch.query, 'Spoonie');
  assert.equal(history.state.__devArchiveSearch.visibleArticles, 20);
  // Fresh VM/context models a full document reload with a retained
  // history entry, not a BFCache restore of the old DOM.
  const third = Object.fromEntries(Object.keys(elements).map(id => [id, element(id)]));
  third['archive-browse-section'].hidden = false;
  const thirdDocument = {
    getElementById: id => third[id] || null,
    createElement: element,
    createDocumentFragment: () => element('fragment')
  };
  vm.runInNewContext(script, {document: thirdDocument, window: secondWindow, fetch}, {timeout: 1000});
  await loaded();
  assert.equal(third['search-input'].value, 'Spoonie');
  assert.equal(third['search-results'].children.length, 20);
  assert.equal(third['archive-browse-section'].hidden, true, 'restored search hides full archive');
  assert.equal(third['evidence-search-results'].children.length, 2);
  assert.equal(history.state.unrelated, 'keep');
  third['search-input'].value = 'Article';
  third['search-input'].listeners.input();
  assert.equal(history.state.__devArchiveSearch.visibleArticles, 10);
  // Navigating between native same-document history entries must restore
  // the query and pagination associated with the entry being revisited.
  history.state = {unrelated: 'keep', __devArchiveSearch: {query:'Spoonie', visibleArticles:20}};
  assert.equal(typeof secondWindow.events.popstate, 'function',
    'archive search must subscribe to native Back/Forward state changes');
  secondWindow.events.popstate({state:history.state});
  assert.equal(third['search-input'].value, 'Spoonie');
  assert.equal(third['search-results'].children.length, 20);
  assert.equal(third['evidence-search-results'].children.length, 2);
  assert.equal(third['archive-browse-section'].hidden, true);
  assert.equal(history.state.unrelated, 'keep');
  // The preceding entry may never have been searched. It must show the
  // dated archive instead of carrying search results from a later entry.
  history.state = {unrelated: 'keep'};
  secondWindow.events.popstate({state:history.state});
  assert.equal(third['search-input'].value, '');
  assert.equal(third['search-results'].children.length, 0);
  assert.equal(third['archive-browse-section'].hidden, false);
  assert.equal(third['search-more-articles'].hidden, true);
  assert.equal(history.state.unrelated, 'keep');
  // A failed index must expose the server-rendered browse fallback.
  const fallback = Object.fromEntries(Object.keys(elements).map(id => [id, element(id)]));
  fallback['archive-browse-section'].hidden = false;
  const fallbackDoc = {
    getElementById: id => fallback[id] || null,
    createElement: element,
    createDocumentFragment: () => element('fragment')
  };
  const failWindow = {history:{state:{__devArchiveSearch:{query:'Spoonie',visibleArticles:10}}}};
  vm.runInNewContext(script, {document:fallbackDoc,window:failWindow,fetch:async()=>{throw Error('offline');}}, {timeout:1000});
  await loaded();
  assert.match(fallback['search-result-status'].textContent,/unavailable/);
  assert.equal(fallback['archive-browse-section'].hidden,false,'failed search shows normal dated archive');

  console.log('PASS archive progressive results, evidence isolation, query reset, empty query');
})().catch(error => { console.error(error); process.exitCode = 1; });
