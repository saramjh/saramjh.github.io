'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.join(__dirname,'..');
const src=fs.readFileSync(path.join(root,'assets/js/portfolio.js'),'utf8');
const ledger=fs.readFileSync(path.join(root,'_data/recognitions.yml'),'utf8');
const records=ledger.split(/(?=^- id: )/m).filter(b=>b.startsWith('- id: ')).map(block=>{
  const project=block.match(/^  project: ([a-z-]+)$/m)?.[1];
  const type=block.match(/^  type: ([a-z_]+)$/m)?.[1];
  assert.ok(project&&type);
  return {project,type};
});
assert.equal(records.length,32);
assert.equal(records.filter(x=>x.project==='koreaves').length,17);
assert.equal(records.filter(x=>x.project==='space-atlas').length,11);
assert.equal(records.filter(x=>x.project==='spoonie').length,3);
assert.equal(records.filter(x=>x.project==='scratch-lottery').length,1);
function setup(hash,ko=false){
  const callbacks={};
  const mkBtn=(key,value)=> {
    const attrs={'aria-pressed':value==='all'?'true':'false'};
    const btn={dataset:{[key]:value},listeners:{},classList:{toggle(){}},getAttribute(n){return attrs[n];},
      setAttribute(n,v){attrs[n]=v;},addEventListener(n,cb){this.listeners[n]=cb;}};
    return btn;
  };
  const categories=['all','publication','coverage','citation','listing','dataset_record','collaboration'].map(x=>mkBtn('filter',x));
  const projects=['all','koreaves','space-atlas','spoonie','scratch-lottery'].map(x=>mkBtn('projectFilter',x));
  const entries=records.map(r=>({dataset:{evidenceProject:r.project,evidenceType:r.type},hidden:false}));
  const count={textContent:'',getAttribute(n){return n==='data-recognition-lang'&&ko?'ko':null;}};
  const empty={hidden:true};
  const dom={
    querySelectorAll(q){
      if(q==='.folio-filter')return categories;
      if(q==='.folio-project-filter')return projects;
      if(q==='#folio-records .folio-evidence-item')return entries;
      if(q==='.folio-contact-cta[href^="mailto:"]'||q==='.folio-project-page .folio-project-header .folio-primary-cta[href]'||q==='.folio-evidence-item'||q==='.folio-project-page .folio-project-article a[href], .folio-project-page .folio-project-header .folio-text-cta[href]'||q==='.folio-writing-card[data-case-id]')return [];
      throw Error('Unexpected selector '+q);
    },
    getElementById(id){return {'folio-filter-count':count,'folio-filter-empty':empty}[id]||null;}
  };
  const location={hash}, historyCalls=[];
  const window={location,history:{pushState(state,title,next){assert.equal(state,null);assert.equal(title,'');historyCalls.push(next);location.hash=next;}},addEventListener(n,cb){callbacks[n]=cb;}};
  vm.runInNewContext(src,{document:dom,window,navigator:{doNotTrack:'1'},Array},{timeout:1500});
  const active=(group,key)=>group.filter(b=>b.getAttribute('aria-pressed')==='true').map(b=>b.dataset[key]);
  const click=(group,key,value)=>{const btn=group.find(b=>b.dataset[key]===value);assert.ok(btn);btn.listeners.click();};
  return {window,callbacks,historyCalls,entries,count,empty,categories,projects,
    visible:()=>entries.filter(e=>!e.hidden).length,
    category:()=>active(categories,'filter'),
    project:()=>active(projects,'projectFilter'),
    clickCategory:v=>click(categories,'filter',v),
    clickProject:v=>click(projects,'projectFilter',v)
  };
}
const view=setup('#project-koreaves');
assert.equal(view.visible(),17);
assert.deepEqual(view.category(),['all']);
view.clickCategory('citation');
assert.equal(view.window.location.hash,'#project-koreaves--citation');
assert.equal(view.visible(),1);
assert.deepEqual(view.category(),['citation']);
view.clickCategory('all');
assert.equal(view.visible(),17);
assert.deepEqual(view.project(),['koreaves']);
view.clickCategory('listing');
assert.equal(view.window.location.hash,'#project-koreaves--listing');
assert.equal(view.visible(),10);
assert.deepEqual(view.category(),['listing']);
assert.deepEqual(view.project(),['koreaves']);
view.clickProject('spoonie');
assert.equal(view.window.location.hash,'#project-spoonie--listing');
assert.equal(view.visible(),2);
assert.equal(view.count.textContent,'2 documented records shown');
view.clickCategory('publication');
assert.equal(view.visible(),1);
assert.equal(view.window.location.hash,'#project-spoonie--publication');
const saved=view.historyCalls.length;
view.clickCategory('publication');
assert.equal(view.historyCalls.length,saved);
view.window.location.hash='#project-space-atlas--listing';
view.callbacks.popstate();
assert.equal(view.visible(),9);
assert.deepEqual(view.category(),['listing']);
assert.deepEqual(view.project(),['space-atlas']);
view.window.location.hash='#publication';
view.callbacks.hashchange();
assert.equal(view.visible(),8);
assert.deepEqual(view.project(),['all']);
assert.deepEqual(view.category(),['publication']);
view.window.location.hash='#project-spoonie--dataset_record';
view.callbacks.popstate();
assert.equal(view.visible(),0);
assert.equal(view.empty.hidden,false);
view.window.location.hash='#project-unknown--publication';
view.callbacks.hashchange();
assert.equal(view.visible(),32);
view.window.location.hash='#evidence-beary-resource';
view.callbacks.hashchange();
assert.equal(view.visible(),32);
view.clickProject('scratch-lottery');
view.clickCategory('coverage');
assert.equal(view.visible(),1);
const ko=setup('#project-spoonie--listing',true);
assert.equal(ko.visible(),2);
assert.equal(ko.count.textContent,'출처 확인 기록 2건 표시');
ko.clickProject('all');
assert.equal(ko.window.location.hash,'#listing');
assert.equal(ko.visible(),21);
ko.clickCategory('all');
assert.equal(ko.visible(),32);
console.log('PASS combined source project/category filters, original 30 plus 1 citation and 1 BOU byline, KO/EN count, URL Back/Forward, zero-results, old category fragments, evidence deep links, no network');
