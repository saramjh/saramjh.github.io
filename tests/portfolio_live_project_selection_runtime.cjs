'use strict';
// Local-only: the original provider and browser are never accessed.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const source=fs.readFileSync('assets/js/portfolio.js','utf8');
const selector='.folio-project-page .folio-project-header .folio-primary-cta[href]';
const ids=[['https://koreaves.com/','koreaves'],['https://spaceatlasedu.org/','space_atlas'],['https://spoonie.kr/','spoonie']];
class Link{
 constructor(href){this.href=href;this.listeners=[];}
 getAttribute(name){return name==='href'?this.href:null;}
 addEventListener(kind,fn){assert.equal(kind,'click');this.listeners.push(fn);}
 click(){this.listeners.forEach(fn=>fn({preventDefault(){throw Error('Navigation intercepted');}}));}
}
const allowed=ids.map(x=>new Link(x[0]));
const denied=[
 'https://koreaves.com/?ref=other','https://koreaves.com.evil.test/',
 'http://spoonie.kr/','https://spaceatlasedu.org/earth/seasons/',
 'https://example.com/','/portfolio/spoonie/'
].map(x=>new Link(x));
const calls=[];
const window={doNotTrack:'0',gtag:(...args)=>calls.push(args)};
const navigator={doNotTrack:'0',msDoNotTrack:'0'};
const document={querySelectorAll(q){
 if(q===selector)return [...allowed,...denied];
 if(['.folio-contact-cta[href^="mailto:"]','.folio-evidence-item','.folio-writing-card[data-case-id]',
 '.folio-project-page .folio-project-article a[href], .folio-project-page .folio-project-header .folio-text-cta[href]',
 '.folio-filter','#folio-records .folio-evidence-item'].includes(q))return [];
 throw Error('Unexpected selector '+q);
}};
vm.runInNewContext(source,{document,window,navigator,Array,Object},{timeout:1500});
assert.deepEqual(allowed.map(x=>x.listeners.length),[1,1,1]);
assert.ok(denied.every(x=>x.listeners.length===0));
allowed.forEach(x=>x.click());
assert.equal(calls.length,3);
for(let i=0;i<3;i++){
 assert.equal(calls[i][0],'event');
 assert.equal(calls[i][1],'portfolio_live_project_select');
 assert.deepEqual(JSON.parse(JSON.stringify(calls[i][2])),{content_type:'portfolio_live_project',item_id:ids[i][1]});
}
window.doNotTrack='1';allowed[0].click();assert.equal(calls.length,3);
window.doNotTrack='0';navigator.doNotTrack='1';allowed[1].click();assert.equal(calls.length,3);
navigator.doNotTrack='0';navigator.msDoNotTrack='1';allowed[2].click();assert.equal(calls.length,3);
navigator.msDoNotTrack='0';window.gtag=undefined;allowed[0].click();assert.equal(calls.length,3);
assert.equal(source.includes('event_callback:'),false);
console.log('PASS exact CTA, no URL/PII payload, DNT, absent GA4 and unblocked navigation');
