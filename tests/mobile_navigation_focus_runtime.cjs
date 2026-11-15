'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const script = fs.readFileSync(path.join(__dirname, '../assets/js/main.js'), 'utf8');

function makeUI(isMobile = true) {
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
  const lamp = {listeners:{}, addEventListener(name, cb) {this.listeners[name] = cb;}};
  const wrapper = {
    inert: false,
    classList: {
      add(name) {classes.add(name);},
      remove(name) {classes.delete(name);},
      toggle(name, force) {
        if (force) classes.add(name);
        else classes.delete(name);
      }
    }
  };
  const media = {
    matches: isMobile, listeners: {},
    addEventListener(name, cb) {this.listeners[name] = cb;}
  };
  const document = {
    body,
    getElementById(id) {
      return {'mode':lamp,'menu-trigger':input}[id] || null;
    },
    querySelector(selector) {
      assert.equal(selector, '.wrapper');
      return wrapper;
    },
    querySelectorAll(selector) {
      assert.equal(selector, 'main img:not(.author-avatar)');
      return [];
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
  return {input,wrapper,classes,media,listeners};
}

const mobile = makeUI();
mobile.input.checked = true;
mobile.input.listeners.change.call(mobile.input);
assert.equal(mobile.classes.has('blurry'), true, 'existing visual blur preserved');
assert.equal(mobile.wrapper.inert, true, 'open full-screen nav must not leave background focusable');
assert.equal(mobile.input.attrs['aria-expanded'], 'true', 'expanded nav state is announced');

let prevented = false;
mobile.listeners.keydown({key:'Escape', preventDefault() {prevented=true;}});
assert.equal(prevented, true);
assert.equal(mobile.input.checked, false, 'Esc should close the mobile menu');
assert.equal(mobile.wrapper.inert, false, 'background focus restored after closing');
assert.equal(mobile.classes.has('blurry'), false, 'blur removed after closing');
assert.equal(mobile.input.attrs['aria-expanded'], 'false');
assert.equal(mobile.input.focusCount, 1, 'keyboard focus returned to menu toggle');

mobile.input.checked = true;
mobile.input.listeners.change.call(mobile.input);
mobile.media.matches = false;
mobile.media.listeners.change();
assert.equal(mobile.input.checked, false, 'crossing desktop breakpoint closes open overlay');
assert.equal(mobile.wrapper.inert, false, 'resizing cannot strand entire page inert');

const desktop = makeUI(false);
assert.equal(desktop.wrapper.inert, false);
assert.equal(desktop.input.attrs['aria-expanded'], 'false');
console.log('PASS mobile nav inert focus isolation, Escape close, state and responsive reset');
