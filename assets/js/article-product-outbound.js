(function () {
  'use strict';
  // A link selection on this developer site is not a product visit or signup.
  // Keep URLs, search terms and reader information out of the event payload.
  Array.from(document.querySelectorAll('main a[href]')).forEach(function (link) {
    var href = link.getAttribute('href');
    var url;
    try { url = new URL(href); } catch (_err) { return; }
    if (url.origin !== 'https://spoonie.kr') return;
    var itemId = null;
    if (url.pathname === '/curators' || url.pathname === '/curators/') itemId = 'spoonie_curators';
    else if (url.pathname === '/search' || url.pathname === '/search/') itemId = 'spoonie_search';
    else if (/^\/recipes\/[a-f0-9-]{36}\/?$/i.test(url.pathname)) itemId = 'spoonie_recipe';
    if (!itemId) return;
    link.addEventListener('click', function () {
      if (navigator.doNotTrack === '1' || window.doNotTrack === '1' ||
          navigator.msDoNotTrack === '1') return;
      if (typeof window.gtag !== 'function') return;
      window.gtag('event', 'select_content', {
        content_type: 'developer_article_live_product',
        item_id: itemId
      });
    });
  });
})();
