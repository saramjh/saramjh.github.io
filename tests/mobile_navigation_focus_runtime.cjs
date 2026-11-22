'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const script = fs.readFileSync(path.join(__dirname, '../assets/js/main.js'), 'utf8');

function makeUI(isMobile = true, layout = 'default') {
  const listeners = {};
  const classes = new Set();
  const body = {
    attrs: {'data-theme': 'dark'},
    getAttribute(k) {return this.attrs[k];},
    setAttribute(k, v) {this.attrs[k] = v;},
    removeAttribute(k) {delete this.attrs[k];},
    classList: {remove() {}}
  };
  const input = {
    checked: false, attrs: {}, listeners: {}, focusCount: 0,
    addEventListener(name, cb) {this.listeners[name] = cb;},
    setAttribute(name, value) {this.attrs[name] = String(value);},
    focus() {this.focusCount++;}
  };
  const lamp = {
    attrs: {}, listeners: {},
    addEventListener(name, cb) {this.listeners[name] = cb;},
    setAttribute(name, value) {this.attrs[name] = String(value);}
  };
  function region(name) {
    return {
      name, inert: false,
      classList: {
        contains(key) {return key === name;},
        add(key) {classes.add(key);},
        remove(key) {classes.delete(key);},
        toggle(key, force) {
          if (force) classes.add(key);
          else classes.delete(key);
        }
      }
    };
  }
  const wrapper = region('wrapper');
  const siteSkip = region('site-skip-link');
  const portfolio = [region('folio'), region('folio-footer'), region('folio-skip-link')];
  const backgrounds = layout === 'portfolio' ? portfolio : [wrapper, siteSkip];
  const media = {
    matches: isMobile, listeners: {},
    addEventListener(name, cb) {this.listeners[name] = cb;}
  };
  const document = {
    body,
    getElementById(id) {
      return {'mode':lamp,'menu-trigger':input}[id] || null;
    },
    querySelectorAll(selector) {
      if (selector === 'main img:not(.author-avatar)') return [];
      assert.equal(selector, 'body > .wrapper, body > .folio, body > .folio-footer, body > .folio-skip-link, body > .site-skip-link');
      return backgrounds;
    }
  };
  const window = {
    matchMedia(query) {
      assert.equal(query, '(max-width: 768px)');
      return media;
    },
    addEventListener(name, cb) {listeners[name] = cb;}
  };
  const localStorage = {getItem() {return 'dark';}, setItem() {}};
  vm.runInNewContext(script, {document, window, localStorage, setTimeout() {}}, {timeout:1000});
  return {input,wrapper,siteSkip,backgrounds,classes,media,listeners,lamp};
}

const mobile = makeUI();
assert.equal(mobile.lamp.attrs['aria-pressed'], 'true', 'menu scripts preserve initial dark-mode accessible state');
mobile.input.checked = true;
mobile.input.listeners.change.call(mobile.input);
assert.equal(mobile.classes.has('blurry'), true, 'existing visual blur preserved');
assert.equal(mobile.wrapper.inert, true, 'open full-screen nav must not leave background focusable');
assert.equal(mobile.siteSkip.inert, true, 'new bypass link must stay inside focus trap');
assert.equal(mobile.input.attrs['aria-expanded'], 'true', 'expanded nav state is announced');

let prevented = false;
mobile.listeners.keydown({key:'Escape', preventDefault() {prevented=true;}});
assert.equal(prevented, true);
assert.equal(mobile.input.checked, false, 'Esc should close the mobile menu');
assert.equal(mobile.wrapper.inert, false, 'background focus restored after closing');
assert.equal(mobile.siteSkip.inert, false, 'new bypass link focus restored after closing');
assert.equal(mobile.classes.has('blurry'), false, 'blur removed after closing');
assert.equal(mobile.input.attrs['aria-expanded'], 'false');
assert.equal(mobile.input.focusCount, 1, 'keyboard focus returned to menu toggle');

mobile.input.checked = true;
mobile.input.listeners.change.call(mobile.input);
mobile.media.matches = false;
mobile.media.listeners.change();
assert.equal(mobile.input.checked, false, 'crossing desktop breakpoint closes open overlay');
assert.equal(mobile.wrapper.inert, false, 'resizing cannot strand entire page inert');

const portfolioPage = makeUI(true, 'portfolio');
portfolioPage.input.checked = true;
portfolioPage.input.listeners.change.call(portfolioPage.input);
assert.equal(portfolioPage.backgrounds.length, 3, 'portfolio includes main, footer and keyboard skip link');
assert.equal(portfolioPage.backgrounds[2].name, 'folio-skip-link', 'new bypass link protected by full-screen nav');
for (const area of portfolioPage.backgrounds) {
  assert.equal(area.inert, true, 'portfolio main, footer and bypass cannot stay focusable');
}
portfolioPage.listeners.keydown({key:'Escape', preventDefault() {}});
for (const area of portfolioPage.backgrounds) {
  assert.equal(area.inert, false, 'portfolio main, footer and bypass recover after close');
}

const desktop = makeUI(false);
assert.equal(desktop.wrapper.inert, false);
assert.equal(desktop.input.attrs['aria-expanded'], 'false');
console.log('PASS normal and portfolio mobile nav focus isolation, Escape, state and responsive reset');
