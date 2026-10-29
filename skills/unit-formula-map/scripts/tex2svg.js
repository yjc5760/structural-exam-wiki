// TeX -> SVG（供 WeasyPrint 使用；沙盒無 Chromium，這是唯一可行路徑）
// 用法: node tex2svg.js <in.json> <out.json>
//   in.json  : [{tex:"...", display:true|false}, ...]
//   out.json : ["<mjx-container>...</mjx-container>", ...]
//
// 需先安裝: npm install mathjax-full --prefix /tmp/mj
// fontCache:'local' 讓每個 SVG 自帶字形定義 —— WeasyPrint 不支援跨元素的全域字形快取。
const fs = require('fs');
const M = (process.env.MJ_PREFIX || '/tmp/mj') + '/node_modules/mathjax-full/js/';
const {mathjax} = require(M + 'mathjax.js');
const {TeX} = require(M + 'input/tex.js');
const {SVG} = require(M + 'output/svg.js');
const {liteAdaptor} = require(M + 'adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require(M + 'handlers/html.js');
const {AllPackages} = require(M + 'input/tex/AllPackages.js');

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const doc = mathjax.document('', {
  InputJax: new TeX({packages: AllPackages}),
  OutputJax: new SVG({fontCache: 'local'})
});

const items = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = items.map(it => adaptor.outerHTML(
  doc.convert(it.tex, {display: it.display, em: 16, ex: 8, containerWidth: 800})));
fs.writeFileSync(process.argv[3], JSON.stringify(out), 'utf8');
console.log('converted ' + out.length);
