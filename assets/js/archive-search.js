/* One source-bound index, two independently visible result groups.
 * External records are never hidden behind the blog's ten-result limit. */
(function () {
  'use strict';
  const MAX_ARTICLES = 10;
  const input = document.getElementById('search-input');
  const status = document.getElementById('search-result-status');
  const evidenceSection = document.getElementById('search-evidence-section');
  const articleSection = document.getElementById('search-article-section');
  const evidenceList = document.getElementById('evidence-search-results');
  const articleList = document.getElementById('search-results');
  if (!input || !status || !evidenceSection || !articleSection ||
      !evidenceList || !articleList) return;

  const EVIDENCE_PREFIX = '/portfolio/recognition/#evidence-';
  let records = null;
  let failed = false;
  const decoder = document.createElement('textarea');

  function readable(value) {
    // The original Jekyll search JSON entity-escapes some post titles.
    decoder.innerHTML = String(value == null ? '' : value);
    return decoder.value;
  }

  function validLocalUrl(value) {
    return typeof value === 'string' && value.startsWith('/') &&
      !value.startsWith('//') && !value.includes('\\') &&
      !/[\u0000-\u001f\u007f]/.test(value);
  }

  function renderList(list, items) {
    const fragment = document.createDocumentFragment();
    items.forEach(function (item) {
      const li = document.createElement('li');
      const link = document.createElement('a');
      link.href = item.url;
      link.textContent = readable(item.title);
      link.title = readable(item.description);
      li.appendChild(link);
      fragment.appendChild(li);
    });
    list.replaceChildren(fragment);
  }

  function isEvidence(item) {
    return item.url.startsWith(EVIDENCE_PREFIX);
  }

  function render() {
    const words = input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    evidenceSection.hidden = true;
    articleSection.hidden = true;
    if (words.length === 0) {
      status.textContent = '';
      evidenceList.replaceChildren();
      articleList.replaceChildren();
      return;
    }
    if (failed) {
      status.textContent = 'Search is currently unavailable. Browse the dated articles below.';
      return;
    }
    if (!records) {
      status.textContent = 'Loading search results…';
      return;
    }
    const matched = records.filter(function (item) {
      const text = [item.title, item.description, item.tags].join(' ').toLocaleLowerCase();
      return words.every(function (word) { return text.includes(word); });
    });
    const evidenceMatches = matched.filter(isEvidence);
    const articleMatches = matched.filter(function (item) { return !isEvidence(item); });
    renderList(evidenceList, evidenceMatches);
    renderList(articleList, articleMatches.slice(0, MAX_ARTICLES));
    evidenceSection.hidden = evidenceMatches.length === 0;
    articleSection.hidden = articleMatches.length === 0;
    if (matched.length === 0) {
      status.textContent = 'No matching articles or verified external records.';
      return;
    }
    status.textContent = 'Verified external records: ' + evidenceMatches.length +
      '. Articles: ' + Math.min(articleMatches.length, MAX_ARTICLES) +
      ' of ' + articleMatches.length + '.';
  }

  input.addEventListener('input', render);
  fetch('/assets/search.json', { credentials: 'same-origin' })
    .then(function (response) {
      if (!response.ok) throw new Error('Search index unavailable');
      return response.json();
    })
    .then(function (items) {
      if (!Array.isArray(items)) throw new Error('Search index is not an array');
      records = items.filter(function (item) {
        return item && typeof item === 'object' && validLocalUrl(item.url);
      });
      render();
    })
    .catch(function () {
      failed = true;
      render();
    });
}());
