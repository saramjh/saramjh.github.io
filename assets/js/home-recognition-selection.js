(function(){
  'use strict';
  // Measure an original-homepage archive link selection. Never block navigation.
  // Both destinations are part of the same first-party blog.
  var routes={
    en:'/portfolio/recognition/',
    ko:'/portfolio/recognition/ko/'
  };
  Array.from(document.querySelectorAll('.project-showcase-proof-link[data-recognition-locale]')).forEach(function(link){
    var locale=link.getAttribute('data-recognition-locale');
    if(!Object.prototype.hasOwnProperty.call(routes,locale))return;
    if(link.getAttribute('href')!==routes[locale])return;
    link.addEventListener('click',function(){
      if(navigator.doNotTrack==='1'||window.doNotTrack==='1'||navigator.msDoNotTrack==='1')return;
      if(typeof window.gtag!=='function')return;
      window.gtag('event','select_content',{
        content_type:'homepage_recognition_archive',
        item_id:locale
      });
    });
  });
})();
