'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const source=fs.readFileSync(path.resolve(__dirname,'../assets/js/home-recognition-selection.js'),'utf8');
function setup({dnt='0',ga=true}={}){
  const calls=[];
  const elements=[
    {locale:'en',href:'/portfolio/recognition/'},
    {locale:'ko',href:'/portfolio/recognition/ko/'},
    {locale:'ko',href:'/portfolio/recognition/invalid/'},
    {locale:'fr',href:'/portfolio/recognition/fr/'}
  ].map(attrs=>({
    attrs,handlers:{},
    getAttribute(name){
      return name==='data-recognition-locale'?this.attrs.locale:name==='href'?this.attrs.href:null;
    },
    addEventListener(name,callback){this.handlers[name]=callback;}
  }));
  const document={
    querySelectorAll(selector){
      assert.equal(selector,'.project-showcase-proof-link[data-recognition-locale]');
      return elements;
    }
  };
  const window={
    doNotTrack:'0',
    gtag:ga?(...args)=>calls.push(args):undefined
  };
  vm.runInNewContext(source,{window,document,navigator:{doNotTrack:dnt,msDoNotTrack:'0'},Array,Object},{timeout:1000});
  return {elements,calls,window};
}
{
  const s=setup();
  assert.equal(s.elements.filter(x=>x.handlers.click).length,2,'only exact owner archive links instrumented');
  s.elements[0].handlers.click();
  s.elements[1].handlers.click();
  assert.deepEqual(JSON.parse(JSON.stringify(s.calls)),[['event','select_content',{content_type:'homepage_recognition_archive',item_id:'en'}],['event','select_content',{content_type:'homepage_recognition_archive',item_id:'ko'}]]);
}
{
  const s=setup({dnt:'1'});
  s.elements[0].handlers.click();s.elements[1].handlers.click();
  assert.deepEqual(s.calls,[],'DNT must suppress all events');
}
{
  const s=setup({ga:false});
  s.elements[0].handlers.click();s.elements[1].handlers.click();
  assert.deepEqual(s.calls,[],'no GA4 must not cause tracking or failure');
}
{
  const s=setup();
  s.window.doNotTrack='1';
  s.elements[0].handlers.click();
  assert.deepEqual(s.calls,[],'browser window DNT guard');
}
console.log('PASS exact first-party Korean/English links, fixed event scope, DNT, missing GA4 and no navigation interception');
