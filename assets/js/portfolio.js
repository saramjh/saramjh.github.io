(function(){
  'use strict';
  // Measure a visitor's selection of a public evidence link, not use of its destination.
  // Reuse the existing site's GA4 integration. No extra tracker is loaded.
  // A contact-link selection is not evidence that an email was sent or read.
  // Only the original public developer address and two existing CTA surfaces.
  Array.from(document.querySelectorAll('.folio-contact-cta[href^="mailto:"]')).forEach(function(link){
    if(link.getAttribute('href')!=='mailto:devtestudinidae@gmail.com')return;
    var surface=link.closest('.folio-hero')?'portfolio_home':
      link.closest('.folio-next')?'project_case':null;
    if(!surface)return;
    link.addEventListener('click',function(){
      if(navigator.doNotTrack==='1'||window.doNotTrack==='1'||navigator.msDoNotTrack==='1')return;
      if(typeof window.gtag!=='function')return;
      window.gtag('event','developer_contact_link_select',{contact_surface:surface});
    });
  });
  Array.from(document.querySelectorAll('.folio-evidence-item')).forEach(function(entry){
    var link=entry.querySelector('.folio-evidence-main h3 a[href]');
    if(!link)return;
    link.addEventListener('click',function(){
      if(navigator.doNotTrack==='1'||window.doNotTrack==='1'||navigator.msDoNotTrack==='1')return;
      if(typeof window.gtag!=='function')return;
      var id=entry.getAttribute('data-evidence-id');
      if(!id)return;
      window.gtag('event','select_content',{
        content_type:'portfolio_external_evidence',
        item_id:id
      });
    });
    // The source stays the primary evidence. Track the reader's selection of
    // the corresponding developer explanation as a separate on-site action.
    Array.from(entry.querySelectorAll('.folio-evidence-context a[data-case-lang]')).forEach(function(caseLink){
      caseLink.addEventListener('click',function(){
        if(navigator.doNotTrack==='1'||window.doNotTrack==='1'||navigator.msDoNotTrack==='1')return;
        if(typeof window.gtag!=='function')return;
        var id=entry.getAttribute('data-evidence-id');
        var lang=caseLink.getAttribute('data-case-lang');
        if(!id||(lang!=='ko'&&lang!=='en'))return;
        window.gtag('event','select_content',{
          content_type:'portfolio_evidence_case',
          item_id:id+':'+lang
        });
      });
    });
  });
  // Record selections of the published first-party case studies. No new tracker.
  Array.from(document.querySelectorAll('.folio-writing-card[data-case-id]')).forEach(function(link){
    link.addEventListener('click',function(){
      if(navigator.doNotTrack==='1'||window.doNotTrack==='1'||navigator.msDoNotTrack==='1')return;
      if(typeof window.gtag!=='function')return;
      var id=link.getAttribute('data-case-id');
      if(!id)return;
      window.gtag('event','select_content',{
        content_type:'portfolio_case_study',
        item_id:id
      });
    });
  });
  // Project reading links have a separate selection event from source citations.
  // Track only first-party static paths; no destination text, query or user data.
  Array.from(document.querySelectorAll('.folio-project-page .folio-project-article a[href], .folio-project-page .folio-project-header .folio-text-cta[href]')).forEach(function(link){
    var href=link.getAttribute('href');
    if(!href)return;
    // This original tagged source link measures a selection on the portfolio,
    // not a visit, session, enrolment or result on Space Atlas.
    if(href==='https://spaceatlasedu.org/earth/seasons/?utm_source=saramjh_portfolio&utm_medium=referral&utm_campaign=space_atlas_earth_seasons'){
      link.addEventListener('click',function(){
        if(navigator.doNotTrack==='1'||window.doNotTrack==='1'||navigator.msDoNotTrack==='1')return;
        if(typeof window.gtag!=='function')return;
        window.gtag('event','portfolio_space_atlas_click',{
          content_type:'portfolio_outbound_project',
          item_id:'space_atlas_earth_seasons'
        });
      });
      return;
    }
    if(!/^\/[a-z0-9][a-z0-9-]*\/$/.test(href))return;
    var slug=href.slice(1,-1);
    link.addEventListener('click',function(){
      if(navigator.doNotTrack==='1'||window.doNotTrack==='1'||navigator.msDoNotTrack==='1')return;
      if(typeof window.gtag!=='function')return;
      window.gtag('event','select_content',{
        content_type:'portfolio_project_note',
        item_id:slug
      });
    });
  });
  // This event records a portfolio CTA selection, not use of the destination.
  var originalProjects={
    'https://koreaves.com/':'koreaves',
    'https://spaceatlasedu.org/':'space_atlas',
    'https://spoonie.kr/':'spoonie'
  };
  Array.from(document.querySelectorAll('.folio-project-page .folio-project-header .folio-primary-cta[href]')).forEach(function(link){
    var href=link.getAttribute('href');
    if(!Object.prototype.hasOwnProperty.call(originalProjects,href))return;
    var id=originalProjects[href];
    link.addEventListener('click',function(){
      if(navigator.doNotTrack==='1'||window.doNotTrack==='1'||navigator.msDoNotTrack==='1')return;
      if(typeof window.gtag!=='function')return;
      window.gtag('event','portfolio_live_project_select',{
        content_type:'portfolio_live_project',
        item_id:id
      });
    });
  });
  var buttons=Array.from(document.querySelectorAll('.folio-filter'));
  var projectButtons=Array.from(document.querySelectorAll('.folio-project-filter'));
  var entries=Array.from(document.querySelectorAll('#folio-records .folio-evidence-item'));
  if(!buttons.length||!entries.length)return;
  var count=document.getElementById('folio-filter-count');
  var empty=document.getElementById('folio-filter-empty');
  var koreanArchive=!!(count&&typeof count.getAttribute==='function'&&count.getAttribute('data-recognition-lang')==='ko');
  var activeCategory='all';
  var activeProject='all';
  function hasCategory(category){return buttons.some(function(button){return button.dataset.filter===category;});}
  function hasProject(project){return project==='all'||projectButtons.some(function(button){return button.dataset.projectFilter===project;});}
  function applyFilter(category,project){
    activeCategory=hasCategory(category)?category:'all';
    activeProject=hasProject(project)?project:'all';
    var visible=0;
    entries.forEach(function(entry){
      var categoryMatch=activeCategory==='all'||entry.dataset.evidenceType===activeCategory;
      var projectMatch=activeProject==='all'||entry.dataset.evidenceProject===activeProject;
      var show=categoryMatch&&projectMatch;
      entry.hidden=!show;
      if(show)visible++;
    });
    buttons.forEach(function(button){
      var selected=button.dataset.filter===activeCategory;
      button.classList.toggle('is-active',selected);
      button.setAttribute('aria-pressed',String(selected));
    });
    projectButtons.forEach(function(button){
      var selected=button.dataset.projectFilter===activeProject;
      button.classList.toggle('is-active',selected);
      button.setAttribute('aria-pressed',String(selected));
    });
    if(count)count.textContent=koreanArchive?'출처 확인 기록 '+visible+'건 표시':visible+' documented '+(visible===1?'record':'records')+' shown';
    if(empty)empty.hidden=visible!==0;
  }
  function hashFor(category,project){
    if(project==='all')return '#'+category;
    return '#project-'+project+(category==='all'?'':'--'+category);
  }
  // Keep older #publication and #listing links, preserve browser Back/Forward,
  // and never let an unknown fragment hide source-linked records.
  function filtersFromUrl(){
    var hash=window.location.hash.slice(1);
    if(hasCategory(hash))return {category:hash,project:'all'};
    if(hash.indexOf('project-')===0){
      var parts=hash.slice(8).split('--');
      if(parts.length<=2&&hasProject(parts[0])&&(parts.length===1||hasCategory(parts[1]))){
        return {category:parts[1]||'all',project:parts[0]};
      }
    }
    return {category:'all',project:'all'};
  }
  function restoreFilter(){
    var selected=filtersFromUrl();
    applyFilter(selected.category,selected.project);
  }
  function updateHash(category,project){
    var hash=hashFor(category,project);
    if(window.location.hash!==hash)window.history.pushState(null,'',hash);
    applyFilter(category,project);
  }
  buttons.forEach(function(button){
    button.addEventListener('click',function(){updateHash(button.dataset.filter,activeProject);});
  });
  projectButtons.forEach(function(button){
    button.addEventListener('click',function(){updateHash(activeCategory,button.dataset.projectFilter);});
  });
  window.addEventListener('popstate',restoreFilter);
  window.addEventListener('hashchange',restoreFilter);
  restoreFilter();
})();
