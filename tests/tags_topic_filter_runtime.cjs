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

function setup({state = null, rejectHistory = false} = {}) {
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
  const topicLinks={listeners:{},contains(x){return anchors.includes(x);},
    addEventListener(name,fn){this.listeners[name]=fn;}};
  const doc = {
    getElementById(id) {
      return {'tag-topic-filter':panel, 'tag-topic-query':input, 'tag-topic-status':status,
              'tag-topic-links':topicLinks}[id] || null;
    },
    querySelectorAll(selector) {
      assert.equal(selector,'#tag-topic-links .tag-item');
      return anchors;
    }
  };
  const history = {
    state,
    writes:0,
    replaceState(next, title, ...args) {
      assert.equal(title, '');
      assert.equal(args.length,0,'URL fragments and query parameters are not changed');
      if(rejectHistory) throw Error('History not writable');
      this.state=next;
      this.writes++;
    }
  };
  const events={};
  const window = {history,location:{hash:''},addEventListener(name,fn){events[name]=fn;}};
  vm.runInNewContext(source,{document:doc,window,Array,String}, {timeout:1000});
  const type = value => {
    input.value = value;
    input.callbacks.input();
  };
  const visible = () => anchors.filter(x=>!x.hidden).map(x=>x.textContent);
  return {panel,input,status,anchors,type,visible,events,history,window,topicLinks,
          reload:()=>setup({state:history.state})};
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

// Original user intent survives a real document reload in the same history entry.
const preserved=setup({state:{unrelated:{owner:'keep'},previousDate:'2026-11-19'}});
preserved.type('koreaves');
assert.equal(preserved.history.writes,1);
assert.equal(preserved.history.state.unrelated.owner,'keep');
assert.equal(preserved.history.state.__devTagTopicSearch.query,'koreaves');
const restored=preserved.reload();
assert.equal(restored.input.value,'koreaves');
assert.deepEqual(restored.visible(),['KoreAves']);
assert.equal(restored.status.textContent,'1 of 4 topics');
assert.equal(restored.history.writes,0,'render must not write history');
restored.type('한국어');
assert.deepEqual(restored.reload().visible(),['한국어 학습']);
restored.type('');
assert.equal(Object.hasOwn(restored.history.state,'__devTagTopicSearch'),false);
assert.equal(restored.history.state.unrelated.owner,'keep');
assert.equal(restored.reload().input.value,'');
// A different script's primitive state and a restricted history environment remain untouched.
const primitive=setup({state:'peer-string'});
primitive.type('KoreAves');
assert.deepEqual(primitive.visible(),['KoreAves']);
assert.equal(primitive.history.state,'peer-string');
assert.equal(primitive.history.writes,0);
const denied=setup({state:{peer:1},rejectHistory:true});
denied.type('Spoonie');
assert.deepEqual(denied.visible(),['Spoonie']);
assert.equal(denied.history.writes,0);
// Invalid/oversize values cannot silently restore a false, corrupted prior query.
const oldOversized=setup({state:{__devTagTopicSearch:{query:'z'.repeat(121)}}});
assert.equal(oldOversized.input.value,'');
const oldMalformed=setup({state:{__devTagTopicSearch:{query:200}}});
assert.equal(oldMalformed.input.value,'');
const longValue=setup({state:{peer:'preserve'}});
longValue.type('koreaves'.repeat(16));
assert.equal(longValue.history.state.peer,'preserve');
assert.equal(longValue.history.state.__devTagTopicSearch,undefined);
console.log('PASS topic finder reload state, scoped history, clear/unknown/error fallback and URL privacy');

// Native fragment navigation creates a distinct history entry. Save search
// state there without changing the URL; Back restores the prior entry.
const fragment=setup({state:{unrelated:2}});
fragment.type('koreaves');
const priorState=fragment.history.state;
fragment.topicLinks.listeners.click({
 target:{closest:()=>fragment.anchors[1]},
 ctrlKey:false,metaKey:false,shiftKey:false,altKey:false,defaultPrevented:false
});
fragment.window.location.hash='#KoreAves';
fragment.history.state=null;
fragment.events.popstate();
fragment.events.hashchange();
assert.equal(fragment.history.state.__devTagTopicSearch.query,'koreaves');
fragment.type('Spoonie');
const newState=fragment.history.state;
fragment.history.state=priorState;
fragment.events.popstate();
fragment.events.hashchange();
assert.equal(fragment.input.value,'koreaves');
assert.deepEqual(fragment.visible(),['KoreAves']);
fragment.history.state=newState;
fragment.events.popstate();
fragment.events.hashchange();
assert.equal(fragment.input.value,'Spoonie');
assert.deepEqual(fragment.visible(),['Spoonie']);
console.log('PASS native hash navigation and Back/Forward restore each history entry');
