const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const mainScript = fs.readFileSync(path.join(root, 'assets/js/main.js'), 'utf8');
const layouts = ['default', 'page', 'post', '404', 'portfolio'];

function exercise(layout, storedPreference, storageBlocked = false) {
  const html = fs.readFileSync(path.join(root, '_layouts', layout + '.html'), 'utf8');
  const bootstrap = html.match(/<body[^>]*>\s*<script>([\s\S]*?)<\/script>/);
  assert(bootstrap, layout + ': body theme bootstrap must exist');

  const attrs = new Map([['data-theme', 'dark']]);
  const written = [];
  const classes = new Set(['notransition']);
  const handlers = {};
  const body = {
    getAttribute: key => attrs.get(key) ?? null,
    setAttribute: (key, value) => attrs.set(key, value),
    removeAttribute: key => attrs.delete(key),
    classList: { remove: key => classes.delete(key) },
  };
  const storage = {
    getItem(key) {
      if (storageBlocked) throw new Error('SecurityError: storage blocked');
      assert.equal(key, 'theme');
      return storedPreference;
    },
    setItem(key, value) {
      if (storageBlocked) throw new Error('SecurityError: storage blocked');
      assert.equal(key, 'theme');
      storedPreference = value;
      written.push(value);
    },
  };
  const buttonAttrs = new Map();
  const lamp = {
    addEventListener: (event, callback) => { handlers[event] = callback; },
    setAttribute: (name, value) => buttonAttrs.set(name, value),
    getAttribute: name => buttonAttrs.get(name),
  };
  const context = vm.createContext({
    document: {
      body,
      getElementById: id => id === 'mode' ? lamp : null,
      querySelectorAll: () => [],
    },
    localStorage: storage,
    window: { addEventListener: () => {} },
    setTimeout: callback => callback(),
  });

  assert.doesNotThrow(() => vm.runInContext(bootstrap[1], context), layout + ': bootstrap');
  assert.doesNotThrow(() => vm.runInContext(mainScript, context), layout + ': common script');
  assert.equal(typeof handlers.click, 'function', layout + ': theme button handler');

  const initialDark = body.getAttribute('data-theme') === 'dark';
  assert.equal(initialDark, storedPreference !== 'light', layout + ': initial preference');
  assert.equal(lamp.getAttribute('aria-pressed'), String(initialDark), layout + ': initial accessibility state');
  assert.doesNotThrow(() => handlers.click(), layout + ': first click');
  assert.equal(body.getAttribute('data-theme') === 'dark', !initialDark, layout + ': first toggle');
  assert.equal(lamp.getAttribute('aria-pressed'), String(!initialDark), layout + ': first accessibility toggle');
  assert.doesNotThrow(() => handlers.click(), layout + ': second click');
  assert.equal(body.getAttribute('data-theme') === 'dark', initialDark, layout + ': second toggle');
  assert.equal(lamp.getAttribute('aria-pressed'), String(initialDark), layout + ': second accessibility toggle');
  if (!storageBlocked) {
    assert.equal(written.at(-1), initialDark ? 'dark' : 'light');
  }
}

for (const layout of layouts) {
  exercise(layout, null, false);
  exercise(layout, 'light', false);
  exercise(layout, null, true);
}
const navbar = fs.readFileSync(path.join(root, '_includes/navbar.html'), 'utf8');
assert.match(navbar, /id="mode" aria-label="\{% if page\.lang == 'ko' %\}다크 모드\{% else %\}Dark mode\{% endif %\}" aria-pressed="\{% if site\.mode == 'dark' %\}true\{% else %\}false\{% endif %\}"/);
console.log('PASS: 5 layouts × 3 storage states × 2 theme clicks with accessible state');
