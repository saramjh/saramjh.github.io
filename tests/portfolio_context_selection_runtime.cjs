'use strict';
// Purely local simulation of the original portfolio listener; no browser/network.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const src = fs.readFileSync(path.join(__dirname, '..', 'assets/js/portfolio.js'),'utf8');
const markup = fs.readFileSync(path.join(__dirname, '..', 'portfolio/index.html'),'utf8');
const contextScript = markup.match(/<script data-dev-context-case-tracking>([\s\S]*?)<\/script>/);
assert.ok(contextScript, 'The root portfolio page must own the context-only listener');
class Link {
  constructor(id) {this.id=id;this.listeners=new Map();}
  getAttribute(name){return name==='data-case-id'?this.id:null;}
  addEventListener(evt,fn){const a=this.listeners.get(evt)||[];a.push(fn);this.listeners.set(evt,a);}
  click(){for(const fn of this.listeners.get('click')||[])fn({preventDefault(){throw new Error('Unexpected navigation interception')}});}
}
function setup(compact=false) {
  const cards=['space_atlas_eusci_essay','koreaves_published_contributions','koreaves_resource_lists','spoonie_public_recipe_poll','utf8_caption_integrity','jekyll_dnt_analytics_loader','playwright_runner_chrome_ci'].map(id=>new Link(id));
  const contextual=new Link('jekyll_eu_consent_revocation');
  const links=[...cards,contextual];const calls=[];
  const document={
    querySelectorAll(selector) {
      if(selector==='.folio-evidence-item'||selector==='.folio-filter'||selector==='#folio-records .folio-evidence-item')return [];
      if(selector==='.folio-project-page .folio-project-article a[href], .folio-project-page .folio-project-header .folio-text-cta[href]')return [];
      if(selector==='.folio-writing-card[data-case-id]')return cards;
      throw new Error('Unexpected DOM query: '+selector);
    },
    querySelector(selector) {
      assert.equal(selector,'.folio-context-case-link[data-case-id]');
      return contextual;
    }
  };
  const navigator={doNotTrack:'0'};
  const window={doNotTrack:'0',gtag:(...args)=>calls.push(args)};
  vm.runInNewContext(src,{document,navigator,window,Array}, {timeout:1000});
  const inline = compact ? contextScript[1].replace(/\s+/g,' ') : contextScript[1];
  vm.runInNewContext(inline,{document,navigator,window}, {timeout:1000});
  return {cards,contextual,calls,navigator,window};
}
for(const compact of [false,true]) {
const x=setup(compact);
for(const card of x.cards)card.click();
x.contextual.click();
assert.equal(x.calls.length,8,'Seven original cards AND new contextual link must each emit once');
assert.equal(x.calls[7][0],'event');
assert.equal(x.calls[7][1],'select_content');
assert.equal(x.calls[7][2].content_type,'portfolio_case_study');
assert.equal(x.calls[7][2].item_id,'jekyll_eu_consent_revocation');
x.window.doNotTrack='1';x.contextual.click();
assert.equal(x.calls.length,8,'DNT must suppress contextual event');
x.window.doNotTrack='0';x.navigator.doNotTrack='1';x.contextual.click();
assert.equal(x.calls.length,8,'Navigator DNT must suppress contextual event');
x.navigator.doNotTrack='0';x.window.gtag=undefined;x.contextual.click();
assert.equal(x.calls.length,8,'Missing GA4 must not emit or break navigation');
}
console.log('PASS 7 prior cards + 1 context link, raw/compressed markup, DNT/gtag guards, no network or navigation interception');
