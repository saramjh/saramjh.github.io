(function () {
  'use strict';

  // A reader selecting a documentation link is not evidence of a completed repair.
  // Send only an allowlisted resource category; no destination URL or reader data.
  var articleLang = document.documentElement.lang;
  if (articleLang !== 'ko' && articleLang !== 'en') return;
  var resources = {
    '/support/epson-ink-pad-reset-utility-faqs': 'ink_pad_faq',
    '/support/wa00369': 'waste_ink_service'
  };

  Array.from(document.querySelectorAll('main a[href]')).forEach(function (link) {
    var href = link.getAttribute('href');
    var url;
    try { url = new URL(href); } catch (_err) { return; }
    if (url.protocol !== 'https:' || url.hostname !== 'epson.com') return;
    var path = url.pathname.replace(/\/$/, '');
    var referenceId = resources[path];
    if (!referenceId) return;

    link.addEventListener('click', function () {
      if (navigator.doNotTrack === '1' || window.doNotTrack === '1' ||
          navigator.msDoNotTrack === '1') return;
      if (typeof window.gtag !== 'function') return;
      window.gtag('event', 'epson_support_reference_select', {
        reference_id: referenceId,
        article_lang: articleLang
      });
    });
  });
})();
