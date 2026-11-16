'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const src = fs.readFileSync(path.join(__dirname, '../assets/js/main.js'), 'utf8');
const portfolio = fs.readFileSync(path.join(__dirname, '../_layouts/portfolio.html'), 'utf8');
assert.match(portfolio, /\{\% include navbar\.html \%\}/, 'portfolio has theme button');
assert.doesNotMatch(portfolio, /\b(initTheme)\s*[(=]/, 'portfolio does not declare normal-page initTheme');

function openPage(stored, initialDark) {
  let value = stored;
  const attrs = new Map(initialDark ? [['data-theme', 'dark']] : []);
  const listeners = {};
  const body = {
    getAttribute(name) {return attrs.has(name) ? attrs.get(name) : null;},
    setAttribute(name, next) {attrs.set(name, next);},
    removeAttribute(name) {attrs.delete(name);}
  };
  const lamp = {addEventListener(name, cb) {listeners[name] = cb;}};
  const document = {
    body,
    getElementById(id) {return id === 'mode' ? lamp : null;},
    querySelectorAll(query) {
      assert.equal(query, 'main img:not(.author-avatar)');
      return [];
    }
  };
  const localStorage = {
    getItem(name) {assert.equal(name, 'theme');return value;},
    setItem(name, next) {assert.equal(name, 'theme');value = next;}
  };
  vm.runInNewContext(src, {document, localStorage, window:{}}, {timeout:1000});
  assert.equal(typeof listeners.click, 'function');
  return {
    click() {listeners.click();},
    get dark() {return body.getAttribute('data-theme') === 'dark';},
    get stored() {return value;}
  };
}

// Fresh first visit on the standalone portfolio layout: there is no
// inline initTheme() on this layout, so fallback must use actual body state.
for (const dark of [true,false]) {
  const ui=openPage(null,dark);
  ui.click();
  assert.equal(ui.dark,!dark,'first click changes the visible color theme');
  assert.equal(ui.stored,dark?'light':'dark','first click persists the new setting');
  ui.click();
  assert.equal(ui.dark,dark,'second click reverses the change');
  assert.equal(ui.stored,dark?'dark':'light');
}

// Existing visitor state must continue to work independently of the markup.
for (const [saved,dark] of [['dark',true],['light',false]]) {
  const ui=openPage(saved,dark);
  ui.click();
  assert.equal(ui.dark,!dark,'existing stored theme toggles');
  assert.equal(ui.stored,dark?'light':'dark');
}
console.log('PASS first portfolio click with no stored theme and existing theme preferences');
