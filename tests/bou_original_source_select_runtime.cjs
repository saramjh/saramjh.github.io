'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('assets/js/bou-original-source-select.js','utf8');
const originalURL = 'https://bou.org.uk/blog-oh-when-records-become-maps/';

function harness(lang, pathname, dnt = '0', enabled = true) {
  const events = [];
  const links = [
    originalURL,
    originalURL,
    'https://bou.org.uk/blog-oh-when-records-become-maps/?ref=tracking',
    originalURL + '#foo',
    'https://bou.org.uk.evil.example/blog-oh-when-records-become-maps/',
    'http://bou.org.uk/blog-oh-when-records-become-maps/',
    'https://bou.org.uk/blog-oh-when-records-become-maps-attacker/',
    'https://www.bou.org.uk/blog-oh-when-records-become-maps/',
    'https://user:pass@bou.org.uk/blog-oh-when-records-become-maps/',
    'https://koreaves.com/methodology/',
    '/portfolio/recognition/',
    'javascript:alert(1)'
  ].map(href=>({
    href,listeners:[],
    getAttribute(name){ assert.equal(name,'href');return this.href; },
    addEventListener(type, callback){ assert.equal(type,'click');this.listeners.push(callback); },
    click(){ let prevented=false;this.listeners.forEach(fn=>fn({preventDefault(){prevented=true;}}));assert.equal(prevented,false); }
  }));
  const document={
    documentElement:{lang},
    querySelectorAll(selector){assert.equal(selector,'main a[href]');return links;}
  };
  const navigator={doNotTrack:dnt,msDoNotTrack:'0'};
  const window={
    location:{pathname},
    doNotTrack:'0',
    gtag:enabled ? (...args)=>events.push(args) : undefined
  };
  vm.runInNewContext(source,{document,navigator,window,URL,Array},{timeout:1000});
  return {links,events,navigator,window};
}
for (const lang of ['ko','en']) {
  const path='/koreaves-bou-when-records-become-maps-'+lang+'/';
  const h=harness(lang,path);
  assert.equal(h.events.length,0,'Never fire on page render');
  assert.deepEqual(h.links.map(l=>l.listeners.length),[1,1,0,0,0,0,0,0,0,0,0,0]);
  h.links.forEach(l=>l.click());
  assert.deepEqual(h.events.map(a=>JSON.parse(JSON.stringify(a))),[
    ['event','bou_original_source_select',{source_id:'bou_when_records_become_maps',article_lang:lang}],
    ['event','bou_original_source_select',{source_id:'bou_when_records_become_maps',article_lang:lang}]
  ]);
  for (const [obj,field] of [['navigator','doNotTrack'],['navigator','msDoNotTrack'],['window','doNotTrack']]) {
    h[obj][field]='1';
    h.links[0].click();
    assert.equal(h.events.length,2,obj+'.'+field+' must suppress');
    h[obj][field]='0';
  }
  h.window.gtag=undefined;
  h.links[0].click();
  assert.equal(h.events.length,2,'No global analytics, no new event');
  assert.deepEqual(h.events.flatMap(e=>Object.keys(e[2])),['source_id','article_lang','source_id','article_lang']);
}
for (const [lang,page] of [
 ['ko','/koreaves-bou-when-records-become-maps-en/'],
 ['en','/koreaves-bou-when-records-become-maps-ko/'],
 ['ko','/portfolio/recognition/'],['en','/'],['en','/koreaves-bou-when-records-become-maps-en'],
 ['en','/koreaves-bou-when-records-become-maps-en/attacker']
]) {
  const h=harness(lang,page);
  h.links.forEach(l=>l.click());
  assert.equal(h.events.length,0,'No event outside matching article and HTML lang');
}
const unavailable=harness('en','/koreaves-bou-when-records-become-maps-en/','1');
unavailable.links[0].click();
assert.equal(unavailable.events.length,0);
assert.ok(!/sendBeacon|fetch\(|XMLHttpRequest|preventDefault\(|document\.cookie|localStorage|sessionStorage|setTimeout/.test(source));
console.log('PASS BOU source original-only: 2 langs, no first-load event, strict host/path/source, scoped URL, DNT and no gtag, no navigation changes or PII');
