(function(){
  'use strict';
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
