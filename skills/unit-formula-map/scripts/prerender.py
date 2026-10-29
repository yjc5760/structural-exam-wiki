#!/usr/bin/env python3
"""把 formula-given-XX-Un-m.html 中由 JS 動態產生的內容靜態化，供 WeasyPrint 列印。

用法:  python3 prerender.py <src.html> [work_dir]
輸出:  <work_dir>/static.html   （預設 work_dir = /tmp/pdfw）

為什麼需要這一步：WeasyPrint 不執行 JavaScript。頁面的公式卡與逐年表都是
JS 渲染的，直接丟給 WeasyPrint 只會得到一份空殼。

列印版與螢幕版的差異（刻意的，不是 bug）：
  * 卡片依主題分群，組內按「必背 → 別賭 → 通常會給」排序（螢幕版是可篩選的平鋪清單）
  * 逐年表表頭換成純文字 + colgroup 固定欄寬（表頭含 MathJax SVG 會把欄寬撐歪）
  * 剝除 emoji（WeasyPrint 無彩色 emoji 字型，會變成豆腐方框）
"""
import re, json, subprocess, sys, os

SRC = sys.argv[1]
WORK = sys.argv[2] if len(sys.argv) > 2 else '/tmp/pdfw'
os.makedirs(WORK, exist_ok=True)
OUT = os.path.join(WORK, 'static.html')
src = open(SRC, encoding='utf-8').read()

# --- 1. 用 node 把 F / MX 撈成 JSON（不要用正則手抄，會抄錯）---
js = src.split('<script>')[-1].split('</script>')[0].split('/* ---------- 渲染')[0]
open(os.path.join(WORK, 'data.js'), 'w', encoding='utf-8').write(js)
data = json.loads(subprocess.run(
    ['node', '-e',
     "const s=require('fs').readFileSync(%r,'utf8');"
     "const {F,MX}=new Function(s+'; return {F,MX};')();"
     "console.log(JSON.stringify({F,MX}))" % os.path.join(WORK, 'data.js')],
    capture_output=True, text=True, check=True).stdout)
F, MX = data['F'], data['MX']

# 列印版不用 emoji
LVN = {'must': '必背', 'half': '別賭', 'give': '通常會給'}
RANK = {'must': 0, 'half': 1, 'give': 2}

# 主題分群標題：依 F 裡出現的順序自動編號，不需寫死
groups, gt = [], {}
for f in F:
    if f['g'] not in groups:
        groups.append(f['g'])
for i, g in enumerate(groups, 1):
    gt[g] = '2-%d　%s' % (i, g)


def yrs(a, cls):
    """西元年 -> 民國年徽章"""
    return ''.join('<span class="yr %s">%d年</span>' % (cls, y - 1911) for y in a)


# --- 2. 公式卡（分群 + 組內排序）---
cards = []
for g in groups:
    cards.append('<h3 class="grph">%s</h3>' % gt[g])
    for f in sorted([x for x in F if x['g'] == g], key=lambda x: RANK[x['lv']]):
        ev = ('<b>考卷給過：</b>' + yrs(f['ok'], 'ok')) if f['ok'] \
             else '<b>考卷給過：</b><span class="never">從未</span>'
        if f['no']:
            ev += '　｜　<b>考了卻沒給：</b>' + yrs(f['no'], 'no')
        cards.append(
            '<div class="fc %s"><div class="top"><span class="nm">%s</span>'
            '<span class="tag %s">%s</span></div>'
            '<div class="eq">%s</div><p class="meta">%s</p>'
            '<div class="ev">%s</div></div>'
            % (f['lv'], f['nm'], f['lv'], LVN[f['lv']], f['eq'], f['meta'], ev))
src = src.replace('<div class="cards" id="cards"></div>',
                  '<div class="cards">' + ''.join(cards) + '</div>')

# --- 3. 逐年證據表列 ---
NCOL = len(MX[0]) - 4          # 中間的 0/1 欄數
rows = []
for r in MX:
    has = r[2] != '(—)'
    cells = ''.join('<td class="c">%s</td>'
                    % ('<span class="y">✔</span>' if v else '<span class="n">·</span>')
                    for v in r[3:3 + NCOL])
    rows.append('<tr class="%s"><td><b>%s</b><br><span class="ynote">%s年</span></td>'
                '<td class="qq">%s</td>%s<td class="rm">%s</td></tr>'
                % ('hl' if has else '', r[0], r[1], r[2], cells, r[-1]))
src = re.sub(r'(<table id="mx">.*?<tbody>)(</tbody>)',
             lambda m: m.group(1) + ''.join(rows) + m.group(2), src, flags=re.S)

# --- 4. 列印版表頭：純文字 + colgroup 固定欄寬 ---
#     （表頭若含 MathJax SVG 會把欄寬撐歪，表格只佔 60% 頁寬還爆頁）
GREEK = {'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε',
         'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'lambda': 'λ', 'mu': 'μ',
         'nu': 'ν', 'xi': 'ξ', 'pi': 'π', 'rho': 'ρ', 'sigma': 'σ', 'tau': 'τ',
         'phi': 'φ', 'chi': 'χ', 'psi': 'ψ', 'omega': 'ω', 'Delta': 'Δ',
         'Sigma': 'Σ', 'Omega': 'Ω', 'Phi': 'Φ', 'le': '≤', 'ge': '≥',
         'times': '×', 'cdot': '·', 'sqrt': '√', 'frac': '/', 'pm': '±'}


def tex2plain(t):
    """把表頭裡的簡單數學式轉成純文字（表頭若含 MathJax SVG 會把欄寬撐歪）"""
    t = re.sub(r'\\\((.*?)\\\)', r'\1', t, flags=re.S)   # 去 \( \)
    t = t.replace('$', '')
    t = re.sub(r'\\bar\{(.)\}', lambda m: m.group(1) + '\u0304', t)  # \bar{x} -> x̄
    t = re.sub(r'\\([a-zA-Z]+)', lambda m: GREEK.get(m.group(1), m.group(1)), t)
    t = re.sub(r'[_^]\{(.*?)\}', r'\1', t)
    t = re.sub(r'[_^]', '', t)
    return re.sub(r'[{}\\]', '', t).strip()


heads = re.findall(r'<th[^>]*class="c"[^>]*>(.*?)</th>',
                   re.search(r'<thead>.*?</thead>', src, re.S).group(0), re.S)
plain = [tex2plain(re.sub(r'<br\s*/?>', ' ', re.sub(r'<[^>]+>', '', h))) for h in heads]
mid = (100 - 6.5 - 11.5 - 32) / NCOL
PRINT_HEAD = ('<colgroup><col style="width:6.5%"><col style="width:11.5%">'
              + ('<col style="width:%.2f%%">' % mid) * NCOL
              + '<col style="width:32%"></colgroup><thead><tr>'
              '<th>考卷年</th><th>單元題號</th>'
              + ''.join('<th class="c">%s</th>' % h for h in plain)
              + '<th>備註</th></tr></thead>')
src = re.sub(r'<thead>.*?</thead>', lambda m: PRINT_HEAD, src, count=1, flags=re.S)

# --- 5. 移除互動元件與 KaTeX / JS ---
src = re.sub(r'<nav>.*?</nav>', '', src, flags=re.S)
src = re.sub(r'<div class="filters">.*?</div>\s*(?=<div class="cards")', '', src, flags=re.S)
src = re.sub(r'<link[^>]*katex[^>]*>', '', src)
src = re.sub(r'<script\b.*?</script>', '', src, flags=re.S)
src = re.sub(r'<a href="[^"]*\.(html|pdf)"[^>]*>.*?</a>', '', src, flags=re.S)

# --- 6. 剝除 emoji（WeasyPrint 無彩色 emoji 字型）---
for e in ('🔴 ', '🟠 ', '🟢 ', '🔴', '🟠', '🟢', '▶ ', '📄 ', '🖨️ ', '⚠️ ', '⚠️'):
    src = src.replace(e, '')

open(OUT, 'w', encoding='utf-8').write(src)
print('static -> %s | cards %d | rows %d | flag-cols %d' % (OUT, len(F), len(MX), NCOL))
