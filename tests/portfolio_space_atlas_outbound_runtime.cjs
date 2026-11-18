'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const original=fs.readFileSync(path.join(root,'assets/js/portfolio.js'),'utf8');
const project=fs.readFileSync(path.join(root,'_projects/space-atlas.md'),'utf8');
const exact='https://spaceatlasedu.org/earth/seasons/?utm_source=saramjh_portfolio&utm_medium=referral&utm_campaign=space_atlas_earth_seasons';
assert.ok(project.includes(exact),'Original owner project must carry exact source href');
class Link {
  constructor(href){this.href=href;this.listeners=[];}
  getAttribute(name){return name==='href'?this.href:null;}
  addEventListener(name,fn){assert.equal(name,'click');this.listeners.push(fn);}
  click(){this.listeners.forEach(fn=>fn({preventDefault(){throw Error('Navigation must not be interrupted');}}));}
}
const valid=new Link(exact);
const note=new Link('/earth-seasons-no-tilt-experiment-en/');
const wrongHost=new Link(exact.replace('spaceatlasedu.org','spaceatlasedu.org.evil.test'));
const wrongCampaign=new Link(exact.replace('space_atlas_earth_seasons','other_campaign'));
const wrongPath=new Link(exact.replace('/earth/seasons/','/moon/phases/'));
const otherProject=new Link('https://spoonie.kr/');
const all=[valid,note,wrongHost,wrongCampaign,wrongPath,otherProject];
const calls=[];
const navigator={doNotTrack:'0',msDoNotTrack:'0'};
const window={doNotTrack:'0',gtag:(...args)=>calls.push(args)};
const document={querySelectorAll(selector){
 if(selector==='.folio-contact-cta[href^="mailto:"]')return [];
 if(selector==='.folio-project-page .folio-project-article a[href], .folio-project-page .folio-project-header .folio-text-cta[href]')return all;
 if(['.folio-evidence-item','.folio-writing-card[data-case-id]','.folio-filter','#folio-records .folio-evidence-item'].includes(selector))return [];
 throw Error('Unexpected DOM query '+selector);
}};
vm.runInNewContext(original,{window,document,navigator,URL,Array},{timeout:1000});
assert.equal(valid.listeners.length,1,'One listener for the original exact destination');
assert.equal(note.listeners.length,1,'Existing first-party note tracking must survive');
for(const blocked of [wrongHost,wrongCampaign,wrongPath,otherProject])assert.equal(blocked.listeners.length,0,'No source-uncleared destination');
valid.click();note.click();
assert.equal(calls.length,2);
assert.equal(calls[0][0],'event');assert.equal(calls[0][1],'portfolio_space_atlas_click');
assert.deepEqual(JSON.parse(JSON.stringify(calls[0][2])),{content_type:'portfolio_outbound_project',item_id:'space_atlas_earth_seasons'});
assert.deepEqual(JSON.parse(JSON.stringify(calls[1][2])),{content_type:'portfolio_project_note',item_id:'earth-seasons-no-tilt-experiment-en'});
window.doNotTrack='1';valid.click();assert.equal(calls.length,2,'Window DNT must hold');
window.doNotTrack='0';navigator.doNotTrack='1';valid.click();assert.equal(calls.length,2,'Navigator DNT must hold');
navigator.doNotTrack='0';navigator.msDoNotTrack='1';valid.click();assert.equal(calls.length,2,'MS DNT must hold');
navigator.msDoNotTrack='0';window.gtag=undefined;valid.click();assert.equal(calls.length,2,'No GA4 must not throw or measure');
assert.equal(original.includes('event_callback:'),false,'Do not delay or hijack navigation');
console.log('PASS source-bound Space Atlas outbound click and existing note, no PII/URLs, no cross-project link, DNT and no GA4 guards');
