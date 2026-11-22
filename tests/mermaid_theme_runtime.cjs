'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const footer = fs.readFileSync(path.join(__dirname, '../_includes/footer.html'), 'utf8');
const match = footer.match(/<script type="module">\s*([\s\S]*?)<\/script>/);
assert(match, 'existing Mermaid module must exist');
const originalImport = 'await import("https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs")';
assert.equal(match[1].split(originalImport).length, 2, 'only the existing approved Mermaid import is replaced in the test harness');
const code = match[1].replace(originalImport, 'await acquireMermaid()');
const settle = () => new Promise((resolve) => setImmediate(resolve));

async function setup({initial = 'dark', sources = ['flowchart LR; A-->B', 'flowchart TD; B-->C'], missingLibrary = false, hasObserver = true} = {}) {
  const attrs = new Map(initial === 'dark' ? [['data-theme', 'dark']] : []);
  const observerInstances = [];
  const elements = [];
  const replacements = [];
  const errors = [];
  let renderedTheme = null;
  let importCount = 0;
  const renders = [];
  const handlers = new Map();
  const body = {getAttribute: name => attrs.get(name) ?? null};
  const codeNodes = sources.map((source) => {
    const parent = {
      parentNode: {
        replaceChild(container, old) {
          assert.equal(old, parent);
          replacements.push({container, source});
        }
      }
    };
    return {textContent: source, closest: () => parent};
  });
  function createElement(tag) {
    assert.equal(tag, 'div');
    const attributes = new Map();
    const element = {
      className: '', textContent: '',
      getAttribute: name => attributes.get(name) ?? null,
      setAttribute: (name, value) => attributes.set(name, String(value)),
      removeAttribute: name => attributes.delete(name)
    };
    elements.push(element);
    return element;
  }
  const document = {
    body,
    addEventListener(event, callback) {handlers.set(event, callback);},
    querySelectorAll(selector) {
      assert.equal(selector, 'code.language-mermaid, .language-mermaid pre code');
      return codeNodes;
    },
    createElement
  };
  class FakeMutationObserver {
    constructor(callback) {this.callback = callback; observerInstances.push(this);}
    observe(target, options) {
      assert.equal(target, body);
      assert.equal(options.attributes, true);
      assert.deepEqual(Array.from(options.attributeFilter), ['data-theme']);
    }
    trigger() {this.callback([{attributeName:'data-theme'}]);}
  }
  const mermaid = {
    initialize(config) {
      assert.equal(config.startOnLoad, false);
      assert.equal(config.securityLevel, 'loose');
      renderedTheme = config.theme;
    },
    async run({nodes}) {
      assert.equal(nodes.length, sources.length);
      for (const node of nodes) {
        assert.equal(node.getAttribute('data-processed'), null, 'must remove Mermaid processed marker before redraw');
        renders.push({theme: renderedTheme, source: node.textContent});
        node.setAttribute('data-processed', 'true');
        node.textContent = `<svg data-theme="${renderedTheme}"></svg>`;
      }
    }
  };
  const ctx = {
    document,
    console: {error: (...args) => errors.push(args.map(String).join(' '))},
    acquireMermaid: async () => {importCount++; if (missingLibrary) throw Error('CDN unavailable'); return {default: mermaid};},
    ...(hasObserver ? {MutationObserver: FakeMutationObserver} : {})
  };
  vm.runInNewContext(code, ctx, {filename:'footer-mermaid-module.mjs'});
  assert.equal(typeof handlers.get('DOMContentLoaded'), 'function');
  await handlers.get('DOMContentLoaded')();
  await settle();
  const changeTheme = async (theme) => {
    if(theme==='dark')attrs.set('data-theme','dark');
    else attrs.delete('data-theme');
    observerInstances.forEach(o=>o.trigger());
    await settle();
  };
  return {elements,replacements,renders,errors,observerInstances,changeTheme,get importCount(){return importCount;}};
}

(async () => {
  const live = await setup();
  assert.equal(live.importCount, 1, 'Mermaid module must load only once');
  assert.equal(live.replacements.length, 2);
  assert.deepEqual(live.renders.map(x=>x.theme), ['dark','dark']);
  await live.changeTheme('light');
  assert.deepEqual(live.renders.map(x=>x.theme), ['dark','dark','default','default']);
  assert.equal(live.renders[2].source, live.renders[0].source, 'original graph source must survive a theme change');
  await live.changeTheme('dark');
  assert.deepEqual(live.renders.map(x=>x.theme).slice(-2), ['dark','dark']);
  assert.equal(live.importCount, 1);
  assert.deepEqual(live.errors, []);

  const light = await setup({initial:'light',sources:['graph LR; A-->B']});
  assert.equal(light.renders[0].theme, 'default', 'initial light mode must use Mermaid default');
  await light.changeTheme('light');
  assert.equal(light.renders.length, 1, 'unchanged mode must not rerender');
  await light.changeTheme('dark');
  assert.equal(light.renders.at(-1).theme, 'dark');

  const noDiagrams = await setup({sources:[]});
  assert.equal(noDiagrams.importCount, 0, 'pages without graphs must not fetch Mermaid');
  assert.equal(noDiagrams.observerInstances.length, 0);

  const offline = await setup({missingLibrary:true});
  assert.equal(offline.replacements.length, 0, 'unavailable CDN preserves original diagram source fallback');
  assert.equal(offline.errors.length, 1);

  const legacy = await setup({hasObserver:false});
  assert.equal(legacy.renders.length, 2, 'missing MutationObserver must not prevent initial Mermaid rendering');
  console.log('PASS: Mermaid first render, dark/light rerender, source restore, processed marker reset, no-op, CDN fallback');
})().catch(err => { console.error(err); process.exitCode=1; });
