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
  const moreArticles = document.getElementById('search-more-articles');
  const archiveBrowse = document.getElementById('archive-browse-section');
  if (!input || !status || !evidenceSection || !articleSection ||
      !evidenceList || !articleList || !moreArticles || !archiveBrowse) return;

  const EVIDENCE_PREFIX = '/portfolio/recognition/#evidence-';
  let records = null;
  let failed = false;
  let visibleArticles = MAX_ARTICLES;
  // Keep this tab's search in its current history entry, not a URL, storage,
  // or analytics event. Back/Forward and reload restore it without a new visit.
  const SEARCH_ENTRY_KEY = '__devArchiveSearch';
  function currentHistory() {
    return typeof window === 'object' && window.history ? window.history : null;
  }
  function restoreEntrySearch() {
    const history = currentHistory();
    const state = history && history.state;
    const saved = state && typeof state === 'object' && !Array.isArray(state) &&
      state[SEARCH_ENTRY_KEY];
    if (!saved || typeof saved.query !== 'string' || saved.query.length > 2048 ||
        typeof saved.visibleArticles !== 'number' ||
        !Number.isInteger(saved.visibleArticles) ||
        saved.visibleArticles < MAX_ARTICLES || saved.visibleArticles > 10000 ||
        saved.visibleArticles % MAX_ARTICLES !== 0) return false;
    input.value = saved.query;
    visibleArticles = saved.visibleArticles;
    return true;
  }
  function rememberEntrySearch() {
    const history = currentHistory();
    if (!history || typeof history.replaceState !== 'function' ||
        input.value.length > 2048) return;
    const previous = history.state;
    // Do not overwrite an unrelated primitive or array state.
    if (previous !== null && (typeof previous !== 'object' ||
        Array.isArray(previous))) return;
    try {
      history.replaceState(Object.assign({}, previous || {}, {
        [SEARCH_ENTRY_KEY]: {
          query: input.value,
          visibleArticles: Math.min(10000, visibleArticles)
        }
      }), '');
    } catch (_) {
      // Search remains functional even if history state is unavailable.
    }
  }
  restoreEntrySearch();
  function readable(value) {
    return String(value == null ? '' : value);
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
    // The dated archive is the no-query/no-JS fallback. Keep it visible if
    // the search index fails, but do not mix it with filtered results.
    archiveBrowse.hidden = words.length > 0 && !failed;
    evidenceSection.hidden = true;
    articleSection.hidden = true;
    moreArticles.hidden = true;
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
      return words.every(function (word) { return item.searchText.includes(word); });
    });
    const evidenceMatches = matched.filter(isEvidence);
    const articleMatches = matched.filter(function (item) { return !isEvidence(item); });
    renderList(evidenceList, evidenceMatches);
    const shownArticles = Math.min(articleMatches.length, visibleArticles);
    renderList(articleList, articleMatches.slice(0, shownArticles));
    moreArticles.hidden = shownArticles === articleMatches.length;
    moreArticles.textContent = 'Show ' + Math.min(MAX_ARTICLES, articleMatches.length - shownArticles) + ' more articles';
    evidenceSection.hidden = evidenceMatches.length === 0;
    articleSection.hidden = articleMatches.length === 0;
    if (matched.length === 0) {
      status.textContent = 'No matching articles or verified external records.';
      return;
    }
    status.textContent = 'Verified external records: ' + evidenceMatches.length +
      '. Articles: ' + shownArticles +
      ' of ' + articleMatches.length + '.';
  }

  input.addEventListener('input', function () {
    visibleArticles = MAX_ARTICLES;
    rememberEntrySearch();
    render();
  });
  moreArticles.addEventListener('click', function () {
    visibleArticles += MAX_ARTICLES;
    rememberEntrySearch();
    render();
  });
  if (typeof window === 'object' && window &&
      typeof window.addEventListener === 'function') {
    window.addEventListener('popstate', function () {
      if (!restoreEntrySearch()) {
        input.value = '';
        visibleArticles = MAX_ARTICLES;
      }
      render();
    });
  }
  // Hide the unfiltered archive immediately for a restored search entry.
  render();
  fetch('/assets/search.json', { credentials: 'same-origin' })
    .then(function (response) {
      if (!response.ok) throw new Error('Search index unavailable');
      return response.json();
    })
    .then(function (items) {
      if (!Array.isArray(items)) throw new Error('Search index is not an array');
      records = items.filter(function (item) {
        return item && typeof item === 'object' && validLocalUrl(item.url);
      }).map(function (item) {
        item.searchText = [item.title, item.description, item.tags]
          .map(readable).join(' ').toLocaleLowerCase();
        return item;
      });
      render();
    })
    .catch(function () {
      failed = true;
      render();
    });
}());
