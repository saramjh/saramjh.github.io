'use strict';
// Original archive category/filter behavior without browser or network.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const src=fs.readFileSync(path.join(__dirname,'../assets/js/portfolio.js'),'utf8');
const ledger=fs.readFileSync(path.join(__dirname,'../_data/recognitions.yml'),'utf8');
const types=[...ledger.matchAll(/^  type: (publication|listing|dataset_record|collaboration)$/gm)].map(m=>m[1]);
assert.equal(types.length,16,'source archive count');
function setup(initialHash){
 const events={};
 const categories=['all','publication','listing','dataset_record','collaboration'];
 const buttons=categories.map(filter=>{
   const attrs={'aria-pressed':filter==='all'?'true':'false'};
   const button={dataset:{filter},classes:new Set(filter==='all'?['is-active']:[]),
     listeners:{},getAttribute(n){return attrs[n];},
     setAttribute(n,v){attrs[n]=v;},
     addEventListener(n,fn){this.listeners[n]=fn;},
     classList:{toggle(n,value){if(value)button.classes.add(n);else button.classes.delete(n);}}};
   return button;
 });
 const entries=types.map(evidenceType=>({dataset:{evidenceType},hidden:false}));
 const count={textContent:''},empty={hidden:true};
 const document={
   querySelectorAll(selector){
     if(selector==='.folio-evidence-item')return [];
     if(selector==='.folio-writing-card[data-case-id]')return [];
     if(selector==='.folio-filter')return buttons;
     if(selector==='#folio-records .folio-evidence-item')return entries;
     throw Error('Unexpected selector '+selector);
   },
   getElementById(id){return {'folio-filter-count':count,'folio-filter-empty':empty}[id]||null;}
 };
 const location={hash:initialHash};
 const historyCalls=[];
 const window={location,history:{pushState(state,title,hash){
   assert.equal(state,null);assert.equal(title,'');
   historyCalls.push(hash);location.hash=hash;
 }},addEventListener(name,fn){events[name]=fn;}};
 vm.runInNewContext(src,{document,window,navigator:{doNotTrack:'1'},Array},{timeout:1000});
 const visible=()=>entries.filter(e=>!e.hidden).length;
 const active=()=>buttons.filter(b=>b.getAttribute('aria-pressed')==='true').map(b=>b.dataset.filter);
 const click=(category)=>{const b=buttons.find(b=>b.dataset.filter===category);b.listeners.click();};
 return {window,events,buttons,entries,count,empty,historyCalls,visible,active,click};
}
const initial=setup('#listing');
assert.equal(initial.visible(),8);
assert.deepEqual(initial.active(),['listing']);
assert.equal(initial.count.textContent,'8 documented records shown');
initial.click('publication');
assert.equal(initial.window.location.hash,'#publication');
assert.equal(initial.visible(),7);
assert.deepEqual(initial.active(),['publication']);
initial.click('collaboration');
assert.equal(initial.visible(),0);
assert.equal(initial.empty.hidden,false);
assert.equal(initial.count.textContent,'0 documented records shown');
initial.window.location.hash='#publication';
initial.events.popstate();
assert.equal(initial.visible(),7);
assert.deepEqual(initial.active(),['publication']);
initial.window.location.hash='#dataset_record';
initial.events.hashchange();
assert.equal(initial.visible(),1);
const prior=initial.historyCalls.length;
initial.click('dataset_record');
assert.equal(initial.historyCalls.length,prior,'no duplicate history entry for same category');
initial.click('all');
assert.equal(initial.visible(),16);
assert.equal(initial.window.location.hash,'#all');
const invalid=setup('#not-a-filter');
assert.equal(invalid.visible(),16);
assert.deepEqual(invalid.active(),['all']);
const noHash=setup('');
assert.equal(noHash.visible(),16);
assert.deepEqual(noHash.active(),['all']);
console.log('PASS archive deep link, exact source counts, selected state, empty category, history, unknown hash, no duplicate navigation and no network');
