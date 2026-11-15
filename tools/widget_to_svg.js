// Turn a diagram written as a small JSX component (how the original Claude Doc stored its figures) into a plain SVG file.
// Usage: NODE_PATH=$(npm root -g) node tools/widget_to_svg.js <folder of .jsx files> content/figures   (needs the typescript package)
const ts = require('typescript'); const fs = require('fs'); const path = require('path');
const KEBAB = { fontSize: 'font-size', fontWeight: 'font-weight', strokeWidth: 'stroke-width', strokeDasharray: 'stroke-dasharray',
  textAnchor: 'text-anchor', markerEnd: 'marker-end', fillOpacity: 'fill-opacity' };
const VARS = { '--cds-chart-axis': '--fig-line, #6b7280', '--cds-chart-grid': '--fig-grid, #c9cdd3', '--cds-chart-categorical-1': '--fig-accent, #0f9d7a',
  '--cds-text-primary': '--fig-ink, #1a1c20', '--cds-text-secondary': '--fig-muted, #5b616b', '--cds-chart-reference-tint': '--fig-tint, #e8ebef' };
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const escAttr = s => esc(s).replace(/"/g, '&quot;');
function h(tag, props, ...kids) {
  const attrs = [];
  for (const [k, v] of Object.entries(props || {})) {
    if (k.startsWith('data-claude')) continue;
    let val = String(v).replace(/var\((--cds-[\w-]+)\)/g, (_, n) => `var(${VARS[n] || n})`);
    attrs.push(`${KEBAB[k] || k}="${escAttr(val)}"`);
  }
  if (tag === 'svg') attrs.unshift('xmlns="http://www.w3.org/2000/svg"', 'font-family="Inter, system-ui, sans-serif"');
  const body = kids.flat(Infinity).filter(k => k !== null && k !== undefined && k !== false).map(k => typeof k === 'object' && k.__svg ? k.__svg : esc(k)).join('');
  const out = body ? `<${tag}${attrs.length ? ' ' + attrs.join(' ') : ''}>${body}</${tag}>` : `<${tag}${attrs.length ? ' ' + attrs.join(' ') : ''}/>`;
  return { __svg: out };
}
const dir = process.argv[2], outDir = process.argv[3];
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.jsx'))) {
  const src = fs.readFileSync(path.join(dir, f), 'utf8');
  const js = ts.transpileModule(src, { compilerOptions: { jsx: ts.JsxEmit.React, jsxFactory: '__jsx', module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2019 } }).outputText;
  const mod = { exports: {} }; new Function('__jsx', 'module', 'exports', js)(h, mod, mod.exports);
  let svg = mod.exports.default().__svg;
  svg = svg.replace(/></g, '>\n<');
  fs.writeFileSync(path.join(outDir, f.replace('.jsx', '.svg')), svg + '\n');
  console.log(f, '->', svg.length, 'chars;', (svg.match(/<text/g) || []).length, 'text nodes');
}
