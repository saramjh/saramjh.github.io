'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const source = fs.readFileSync(
  path.join(__dirname, '../assets/js/tags-topic-filter.js'), 'utf8'
);
const template = fs.readFileSync(
  path.join(__dirname, '../tags.html'), 'utf8'
);
assert.match(template, /id="tag-topic-filter"/);
assert.match(template, /id="tag-topic-query"/);
assert.match(template, /id="tag-topic-status"/);
assert.match(template, /id="tag-topic-links"/);
assert.match(template, /tags-topic-filter\.js/);
assert.match(template, /<h2 id=/, 'original tag deep links are retained');
assert.match(template, /site\.tags\[name\]/, 'original grouped article list remains');

function setup() {
  const panel = {hidden:true};
  const status = {textContent:''};
  const input = {
    value:'', callbacks:{},
    addEventListener(type, fn) {this.callbacks[type] = fn;}
  };
  function makeAnchor(name, href) {
    return {
      textContent:name, hidden:false,
      getAttribute(key) {assert.equal(key,'href');return href;}
    };
  }
  const anchors = [
    makeAnchor('all','#'),
    makeAnchor('KoreAves','#KoreAves'),
    makeAnchor('Spoonie','#Spoonie'),
    makeAnchor('한국어 학습','#한국어-학습'),
    makeAnchor('Data engineering','#Data-engineering')
  ];
  const doc = {
    getElementById(id) {
      return {'tag-topic-filter':panel, 'tag-topic-query':input, 'tag-topic-status':status}[id] || null;
    },
    querySelectorAll(selector) {
      assert.equal(selector,'#tag-topic-links .tag-item');
      return anchors;
    }
  };
  vm.runInNewContext(source,{document:doc,Array,String}, {timeout:1000});
  const type = value => {
    input.value = value;
    input.callbacks.input();
  };
  const visible = () => anchors.filter(x=>!x.hidden).map(x=>x.textContent);
  return {panel,input,status,anchors,type,visible};
}

const ui=setup();
assert.equal(ui.panel.hidden,false,'enhancement only appears with JS ready');
assert.equal(ui.status.textContent,'4 topics');
assert.deepEqual(ui.visible(),['all','KoreAves','Spoonie','한국어 학습','Data engineering']);
ui.type('KOREAVES');
assert.deepEqual(ui.visible(),['KoreAves']);
assert.equal(ui.status.textContent,'1 of 4 topics');
ui.type('한 국 어');
assert.deepEqual(ui.visible(),[]);
ui.type('한국어');
assert.deepEqual(ui.visible(),['한국어 학습']);
ui.type('  DAta   ');
assert.deepEqual(ui.visible(),['Data engineering']);
ui.type('___no_existing_topic___');
assert.deepEqual(ui.visible(),[]);
assert.equal(ui.status.textContent,'0 of 4 topics');
ui.type('');
assert.deepEqual(ui.visible(),['all','KoreAves','Spoonie','한국어 학습','Data engineering']);
assert.equal(ui.status.textContent,'4 topics');
console.log('PASS topic filter progressive disclosure, source anchors, case/KO match, zero result, clear restore');
