'use strict';
// Local event simulation. No browser profile, network, GA4 request or navigation.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const src=fs.readFileSync(path.join(__dirname,'../assets/js/portfolio.js'),'utf8');
const selector='.folio-project-page .folio-project-article a[href], .folio-project-page .folio-project-header .folio-text-cta[href]';
class Link {
  constructor(href){this.href=href;this.handlers=[];}
  getAttribute(name){return name==='href'?this.href:null;}
  addEventListener(event,fn){assert.equal(event,'click');this.handlers.push(fn);}
  click(){for(const fn of this.handlers)fn({preventDefault(){throw Error('Navigation intercepted');}});}
}
function setup(){
  const links=[
    new Link('/space-atlas-eusci-diagrams-en/'),
    new Link('/space-atlas-eusci-diagrams-ko/'),
    new Link('/koreaves-oneearth-author-achievement-en/'),
    new Link('/spoonie-privacy-cache-transition-en/'),
    new Link('https://www.oneearth.org/koreaves/'),
    new Link('/portfolio/recognition/?ref=dev'),
    new Link('/private/path/'),
    new Link('#project')
  ];
  const calls=[];
  const document={querySelectorAll(query){
    if(query===selector)return links;
    if(query==='.folio-evidence-item'||query==='.folio-writing-card[data-case-id]'||query==='.folio-filter'||query==='#folio-records .folio-evidence-item')return [];
    throw Error('Unexpected selector: '+query);
  }};
  const navigator={doNotTrack:'0',msDoNotTrack:'0'};
  const window={doNotTrack:'0',gtag:(...args)=>calls.push(args)};
  vm.runInNewContext(src,{document,window,navigator,Array},{timeout:1000});
  return {links,calls,window,navigator};
}
const a=setup();
for(const link of a.links)link.click();
assert.equal(a.calls.length,4,'Only exact local article paths emit');
const expected=['space-atlas-eusci-diagrams-en','space-atlas-eusci-diagrams-ko','koreaves-oneearth-author-achievement-en','spoonie-privacy-cache-transition-en'];
for(let i=0;i<a.calls.length;i++){
  assert.equal(a.calls[i][0],'event');
  assert.equal(a.calls[i][1],'select_content');
  assert.equal(a.calls[i][2].content_type,'portfolio_project_note');
  assert.equal(a.calls[i][2].item_id,expected[i]);
  assert.equal(Object.keys(a.calls[i][2]).length,2,'No visitor, query or referrer data');
}
a.window.doNotTrack='1';a.links[0].click();assert.equal(a.calls.length,4,'Window DNT');
a.window.doNotTrack='0';a.navigator.doNotTrack='1';a.links[0].click();assert.equal(a.calls.length,4,'Navigator DNT');
a.navigator.doNotTrack='0';a.navigator.msDoNotTrack='1';a.links[0].click();assert.equal(a.calls.length,4,'IE DNT');
a.navigator.msDoNotTrack='0';a.window.gtag=undefined;a.links[0].click();assert.equal(a.calls.length,4,'No analytics available');
assert.deepEqual(a.links.map(x=>x.handlers.length),[1,1,1,1,0,0,0,0],'No handlers on external or dynamic URLs');
console.log('PASS project-case tracking: 4 exact slugs, external/dynamic excluded, DNT and missing GA4 guards, no navigation interception');
