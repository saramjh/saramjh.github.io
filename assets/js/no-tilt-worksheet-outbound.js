(function () {
  'use strict';

  // An article-to-worksheet click is not evidence of printing, classroom use or learning.
  // Report only the language and fixed resource key; never include URL, child or device data.
  var lang = document.documentElement.lang;
  if (lang !== 'ko' && lang !== 'en') return;
  var exactOrigin = 'https://spaceatlasedu.org';
  var exactPath = '/assets/handouts/earth-seasons-no-tilt.html';

  Array.from(document.querySelectorAll('main a[href]')).forEach(function (link) {
    var url;
    try { url = new URL(link.getAttribute('href')); } catch (_err) { return; }
    if (url.origin !== exactOrigin || url.pathname !== exactPath ||
        url.username || url.password) return;

    link.addEventListener('click', function () {
      if (navigator.doNotTrack === '1' || window.doNotTrack === '1' ||
          navigator.msDoNotTrack === '1') return;
      if (typeof window.gtag !== 'function') return;
      window.gtag('event', 'no_tilt_worksheet_select', {
        resource_id: 'space_atlas_no_tilt_worksheet',
        article_lang: lang
      });
    });
  });
})();
