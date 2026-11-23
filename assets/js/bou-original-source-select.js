(function () {
  'use strict';

  // Count a reader selecting the original BOU article, not an external visit or endorsement.
  // The event contains only a fixed publication ID and this article's language.
  var pageLang = document.documentElement.lang;
  var pages = {
    '/koreaves-bou-when-records-become-maps-ko/': 'ko',
    '/koreaves-bou-when-records-become-maps-en/': 'en'
  };
  if (pages[window.location.pathname] !== pageLang) return;

  Array.from(document.querySelectorAll('main a[href]')).forEach(function (link) {
    var url;
    try { url = new URL(link.getAttribute('href')); } catch (_err) { return; }
    if (url.origin !== 'https://bou.org.uk' ||
        url.pathname !== '/blog-oh-when-records-become-maps/' ||
        url.search !== '' || url.hash !== '' ||
        url.username !== '' || url.password !== '') return;

    link.addEventListener('click', function () {
      if (navigator.doNotTrack === '1' || window.doNotTrack === '1' ||
          navigator.msDoNotTrack === '1') return;
      if (typeof window.gtag !== 'function') return;
      window.gtag('event', 'bou_original_source_select', {
        source_id: 'bou_when_records_become_maps',
        article_lang: pageLang
      });
    });
  });
})();
