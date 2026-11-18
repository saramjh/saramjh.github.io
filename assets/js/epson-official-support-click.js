(function () {
  'use strict';

  // A reader selecting a documentation link is not evidence of a completed repair.
  // Send only an allowlisted resource category; no destination URL or reader data.
  var articleLang = document.documentElement.lang;
  if (articleLang !== 'ko' && articleLang !== 'en') return;
  // Exact official hosts and paths only; never collect link destinations or reader data.
  var resources = {
    'epson.com/support/epson-ink-pad-reset-utility-faqs': 'ink_pad_faq',
    'epson.com/support/wa00369': 'waste_ink_service',
    'www.epson.co.kr/faq/SPT_C11CG88513~EKL_FAQ_0871': 'kr_l3106_maintenance',
    'www.epson.co.kr/cs': 'kr_customer_support'
  };

  Array.from(document.querySelectorAll('main a[href]')).forEach(function (link) {
    var href = link.getAttribute('href');
    var url;
    try { url = new URL(href); } catch (_err) { return; }
    if (url.protocol !== 'https:') return;
    var path = url.pathname.replace(/\/$/, '');
    var referenceId = resources[url.hostname + path];
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
