'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

const footer = fs.readFileSync(path.join(__dirname, '..', '_includes', 'footer.html'), 'utf8');
const found = footer.match(/<script>\s*(\(function \(\) \{[\s\S]*?\}\)\(\);)\s*<\/script>/);
assert.ok(found, 'Expected exact footer privacy-choices IIFE');
const source = found[1];

function scenario({gdprApplies, ok=true, tcf=true, revocation=true, linkExists=true}={}) {
  const events = new Map(), calls=[];
  let clickCount=0, prevented=0;
  const link = {
    hidden: true,
    addEventListener(name, cb) {events.set(name, cb);}
  };
  const window = {googlefc: {}};
  if (revocation) window.googlefc.showRevocationMessage = () => {clickCount++};
  if (tcf) window.__tcfapi = (cmd, version, cb) => {
    calls.push([cmd, version]);
    cb({gdprApplies}, ok);
  };
  const document = {getElementById(id) {assert.equal(id,'privacy-choices'); return linkExists ? link : null;}};
  vm.runInNewContext(source, {window, document}, {timeout:1000});
  const queue = window.googlefc.callbackQueue || [];
  assert.ok(linkExists === false || queue.length === 1, 'Expected exactly one API readiness callback');
  if (queue.length) queue[0].CONSENT_API_READY();
  if (events.has('click')) events.get('click')({preventDefault(){prevented++}});
  return {hidden:link.hidden, calls, clickCount, prevented, hasListener:events.has('click'), queueLength:queue.length};
}

const inScope=scenario({gdprApplies:true});
assert.equal(inScope.hidden,false, 'GDPR=true with API must expose control');
assert.equal(inScope.clickCount,1, 'Click must call official revocation method once');
assert.equal(inScope.prevented,1,'Footer link must not navigate to #');
assert.equal(inScope.calls[0][0],'addEventListener');
assert.equal(inScope.calls[0][1],0);

const outOfScope=scenario({gdprApplies:false});
assert.equal(outOfScope.hidden,true, 'Non-GDPR message must stay hidden');

const failure=scenario({gdprApplies:true,ok:false});
assert.equal(failure.hidden,true, 'Failed TCF callback must not show link');

const noApi=scenario({gdprApplies:true,tcf:false});
assert.equal(noApi.hidden,true, 'Missing TCF API must not show link');

const noRevocation=scenario({gdprApplies:true,revocation:false});
assert.equal(noRevocation.hidden,true, 'Missing revocation function must not show link');

const noLink=scenario({linkExists:false});
assert.equal(noLink.hasListener,false);
assert.equal(noLink.queueLength,0);
console.log('PASS 6 mocked footer cases; browser/provider side effects: 0');
