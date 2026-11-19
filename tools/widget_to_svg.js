// Turn a diagram written as a small JSX component (how the original Claude Doc stored its figures) into a plain SVG file.
// Usage: NODE_PATH=$(npm root -g) node tools/widget_to_svg.js <folder of .jsx files> content/figures   (needs the typescript package)
const ts = require('typescript'); const fs = require('fs'); const path = require('path');
// SVG attributes that really are camelCase; every other camelCase prop is written kebab-case (strokeWidth -> stroke-width).
const CAMEL = new Set(['viewBox', 'preserveAspectRatio', 'markerWidth', 'markerHeight', 'markerUnits', 'refX', 'refY', 'gradientUnits',
  'gradientTransform', 'patternUnits', 'patternContentUnits', 'patternTransform', 'textLength', 'lengthAdjust', 'stdDeviation', 'pathLength',
  'startOffset', 'spreadMethod', 'clipPathUnits', 'maskUnits', 'maskContentUnits', 'filterUnits', 'primitiveUnits', 'baseFrequency', 'numOctaves']);
const attrName = k => k === 'className' ? 'class' : CAMEL.has(k) ? k : k.replace(/[A-Z]/g, c => '-' + c.toLowerCase());
// The doc's theme variables, mapped onto the guide's figure variables (theme/style.css, .figure). Each keeps a fallback.
const VARS = { '--cds-chart-axis': '--fig-line, #6b7280', '--cds-chart-grid': '--fig-grid, #c9cdd3', '--cds-chart-categorical-1': '--fig-accent, #0f9d7a',
  '--cds-text-primary': '--fig-ink, #1a1c20', '--cds-text-secondary': '--fig-muted, #5b616b', '--cds-chart-reference-tint': '--fig-tint, #e8ebef',
  '--cds-chart-categorical-2': '--fig-cat-2, #a1561d', '--cds-chart-categorical-3': '--fig-cat-3, #3c3c83', '--cds-chart-categorical-4': '--fig-cat-4, #6b6b1c',
  '--cds-chart-categorical-5': '--fig-cat-5, #ad3a4b', '--cds-chart-categorical-6': '--fig-cat-6, #235f9c', '--cds-chart-categorical-7': '--fig-cat-7, #7d5187' };
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const escAttr = s => esc(s).replace(/"/g, '&quot;');
const FRAGMENT = Symbol('fragment');
const unknown = new Set();
const themed = v => String(v).replace(/var\((--cds-[\w-]+)\)/g, (_, n) => { if (!VARS[n]) unknown.add(n); return `var(${VARS[n] || n})`; });
function h(tag, props, ...kids) {
  const body = kids.flat(Infinity).filter(k => k !== null && k !== undefined && k !== false && k !== true)
    .map(k => typeof k === 'object' && k.__svg !== undefined ? k.__svg : esc(k)).join('');
  if (tag === FRAGMENT) return { __svg: body };
  const attrs = [];
  for (const [k, v] of Object.entries(props || {})) {
    if (k.startsWith('data-claude') || k === 'key' || v === null || v === undefined || v === false) continue;
    const val = k === 'style' && typeof v === 'object'
      ? Object.entries(v).map(([p, x]) => `${attrName(p)}: ${x}`).join('; ')
      : v;
    attrs.push(`${attrName(k)}="${escAttr(themed(val))}"`);
  }
  if (tag === 'svg') attrs.unshift('xmlns="http://www.w3.org/2000/svg"', 'font-family="Inter, system-ui, sans-serif"');
  const open = `<${tag}${attrs.length ? ' ' + attrs.join(' ') : ''}`;
  return { __svg: body ? `${open}>${body}</${tag}>` : `${open}/>` };
}
const dir = process.argv[2], outDir = process.argv[3];
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.jsx')).sort()) {
  const src = fs.readFileSync(path.join(dir, f), 'utf8');
  const js = ts.transpileModule(src, { compilerOptions: { jsx: ts.JsxEmit.React, jsxFactory: '__jsx', jsxFragmentFactory: '__frag',
    module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2019 } }).outputText;
  const mod = { exports: {} }; new Function('__jsx', '__frag', 'module', 'exports', js)(h, FRAGMENT, mod, mod.exports);
  let svg = mod.exports.default().__svg;
  if (unknown.size) throw new Error(`${f}: no figure variable for ${[...unknown].join(', ')}; add it to VARS`);
  svg = svg.replace(/></g, '>\n<');
  fs.writeFileSync(path.join(outDir, f.replace('.jsx', '.svg')), svg + '\n');
  console.log(f, '->', svg.length, 'chars;', (svg.match(/<text/g) || []).length, 'text nodes');
}
