'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const src = fs.readFileSync('assets/js/article-product-outbound.js', 'utf8');

function makeHarness() {
  const calls = [];
  const links = [
    'https://spoonie.kr/curators',
    'https://spoonie.kr/search?sort=latest',
    'https://spoonie.kr/recipes/6eaa37a1-6c0f-4841-aadd-7a2d980fbdbf',
    'https://spoonie.kr.evil.example/curators',
    'http://spoonie.kr/curators',
    'https://spoonie.kr/admin'
  ].map(href => ({
    href, listener:null, navigated: false,
    getAttribute(name) { return name === 'href' ? this.href : null; },
    addEventListener(type, callback) { assert.equal(type,'click'); this.listener = callback; },
    click() { let prevented=false; this.listener?.({preventDefault(){prevented=true;}}); assert.equal(prevented,false); }
  }));
  const document={querySelectorAll(selector){assert.equal(selector,'main a[href]');return links;}};
  const navigator={doNotTrack:'0',msDoNotTrack:'0'};
  const window={doNotTrack:'0',gtag:(...args)=>calls.push(args)};
  vm.runInNewContext(src,{document,navigator,window,URL},{timeout:1000});
  return {calls,links,navigator,window};
}
const h=makeHarness();
assert.equal(h.calls.length,0,'No event before a real user click');
h.links.forEach(a=>a.click());
assert.deepEqual(h.calls.map(a=>JSON.parse(JSON.stringify(a))),[
 ['event','select_content',{content_type:'developer_article_live_product',content_id:'spoonie_curators'}],
 ['event','select_content',{content_type:'developer_article_live_product',content_id:'spoonie_search'}],
 ['event','select_content',{content_type:'developer_article_live_product',content_id:'spoonie_recipe'}]
]);
for(const flag of [['window','doNotTrack'],['navigator','doNotTrack'],['navigator','msDoNotTrack']]){
 const obj=h[flag[0]];obj[flag[1]]='1';h.links[0].click();assert.equal(h.calls.length,3,flag.join('.'));obj[flag[1]]='0';
}
h.window.gtag=undefined;h.links[0].click();assert.equal(h.calls.length,3,'No GA loader means no tracking');
console.log('article-product-outbound: PASS click-only allowlist, DNT, no navigation changes');

assert.ok(h.calls.every(([_, event, data]) => !Object.hasOwn(data, 'item_id')), 'Reserved ecommerce item_id must not leak into select_content');
