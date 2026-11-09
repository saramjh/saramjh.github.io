(function(){
  'use strict';
  // Measure a visitor's selection of a public evidence link, not use of its destination.
  // The existing site's GA4 setup owns consent and transport. No extra tracker is loaded.
  Array.from(document.querySelectorAll('.folio-evidence-item')).forEach(function(entry){
    var link=entry.querySelector('.folio-evidence-main h3 a[href]');
    if(!link)return;
    link.addEventListener('click',function(){
      if(navigator.doNotTrack==='1'||window.doNotTrack==='1')return;
      if(typeof window.gtag!=='function')return;
      var id=entry.getAttribute('data-evidence-id');
      if(!id)return;
      window.gtag('event','select_content',{
        content_type:'portfolio_external_evidence',
        item_id:id
      });
    });
  });
  var buttons=Array.from(document.querySelectorAll('.folio-filter'));
  var entries=Array.from(document.querySelectorAll('#folio-records .folio-evidence-item'));
  if(!buttons.length||!entries.length)return;
  var count=document.getElementById('folio-filter-count');
  var empty=document.getElementById('folio-filter-empty');
  function applyFilter(category){
    var visible=0;
    entries.forEach(function(entry){var show=category==='all'||entry.dataset.evidenceType===category;entry.hidden=!show;if(show)visible++;});
    buttons.forEach(function(button){var selected=button.dataset.filter===category;button.classList.toggle('is-active',selected);button.setAttribute('aria-pressed',String(selected));});
    if(count)count.textContent=visible+' documented '+(visible===1?'record':'records')+' shown';
    if(empty)empty.hidden=visible!==0;
  }
  buttons.forEach(function(button){button.addEventListener('click',function(){applyFilter(button.dataset.filter);});});
  applyFilter('all');
})();
