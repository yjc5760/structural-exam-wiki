# -*- coding: utf-8 -*-
"""unit-textbook：組裝教科書講義。

工作資料夾（study/figs-src/textbook-XX-Un-m/）內需有：
  textbook.json   設定（科目、單元、分冊、各冊章節）
  chN.html        各章 HTML 片段，內含 {{FIG:figN_k|圖說}} 佔位
  figs_chN.py     各章向量圖，ALL = {'figN_k': 函式}
  calcs.py        全部數值（圖與內文共用）
  lib.py、plot.py SVG 原件（本 skill 的 scripts/ 複製過來）

用法：python3 build.py <冊 key> [輸出路徑]
      python3 build.py all            # 依 textbook.json 每一冊都輸出到 ../../（即 study/）
"""
import re, sys, os, json, importlib, datetime

CSS = r'''
:root{
  --ac:#1565c0; --ac2:#e3f2fd; --tension:#2e7d32; --tension2:#e8f5e9;
  --comp:#c62828; --comp2:#ffebee; --warn:#ef6c00; --warn2:#fff3e0;
  --key:#6a1b9a; --key2:#f3e5f5;
  --bg:#f6f7f4; --card:#fff; --ink:#1f2a30; --mut:#5b6e78; --bd:#d9e0e4;
}
*{box-sizing:border-box}
html{font-size:18px}
body{margin:0;font-family:"Microsoft JhengHei","Noto Sans CJK TC","Noto Sans TC",-apple-system,sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.9}
header{background:linear-gradient(135deg,#1b5e20,#2e7d32 55%,#558b2f);color:#fff;padding:38px 28px 30px}
header.c{background:linear-gradient(135deg,#7f0000,#b71c1c 55%,#c62828)}
header.a{background:linear-gradient(135deg,#0d47a1,#1565c0 55%,#1e88e5)}
header.k{background:linear-gradient(135deg,#4a148c,#6a1b9a 55%,#8e24aa)}
header h1{margin:0 0 10px;font-size:1.7rem;letter-spacing:.5px;line-height:1.4}
header .sub{opacity:.95;font-size:1.02rem;margin:0;max-width:880px}
header .meta{margin-top:14px;font-size:.85rem;opacity:.85}
nav{position:sticky;top:0;z-index:20;background:#fff;border-bottom:2px solid var(--bd);
  padding:9px 14px;display:flex;flex-wrap:wrap;gap:7px;box-shadow:0 2px 6px rgba(0,0,0,.05)}
nav a{text-decoration:none;color:var(--ac);font-size:.86rem;padding:4px 12px;border-radius:15px;background:var(--ac2)}
nav a:hover{background:var(--ac);color:#fff}
nav a.vol{background:#fff3e0;color:#e65100}
main{max-width:940px;margin:0 auto;padding:26px 20px 90px}
section{margin-bottom:60px}
h2{font-size:1.45rem;border-left:8px solid var(--ac);padding:4px 0 4px 14px;margin:56px 0 20px;line-height:1.45;background:#fff;border-radius:0 8px 8px 0}
h2.t{border-color:var(--tension)} h2.c{border-color:var(--comp)} h2.k{border-color:var(--key)}
h3{font-size:1.18rem;margin:38px 0 12px;color:#0d47a1;border-bottom:2px solid #e3e8eb;padding-bottom:4px}
h3.t{color:#1b5e20} h3.c{color:#b71c1c}
h4{font-size:1.05rem;margin:26px 0 8px;color:#37474f}
p{margin:12px 0}
b.g{color:var(--tension)} b.b{color:var(--ac)} b.r{color:var(--comp)}
.kw{display:inline-block;background:var(--key2);color:var(--key);font-weight:700;padding:0 8px;border-radius:6px;margin:0 2px}
.lead{font-size:1.04rem;background:#fff;border:1px solid var(--bd);border-left:6px solid var(--ac);
  border-radius:0 12px 12px 0;padding:16px 20px;margin:18px 0}
.box{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:16px 20px;margin:18px 0}
.why,.trap,.check,.seed{border-radius:0 12px 12px 0;padding:14px 19px;margin:18px 0}
.why{background:var(--key2);border:1px solid #ce93d8;border-left:6px solid var(--key)}
.why>b:first-child{color:var(--key)}
.trap{background:var(--warn2);border:1px solid #ffcc80;border-left:6px solid var(--warn)}
.trap>b:first-child{color:#e65100}
.check{background:#e8f5e9;border:1px solid #a5d6a7;border-left:6px solid var(--tension)}
.check>b:first-child{color:#1b5e20}
.seed{background:#fffde7;border:2px solid #fbc02d;border-radius:14px;text-align:center}
.seed-h{font-weight:700;color:#f57f17;font-size:1.05rem}
.derive{background:#fff;border:1px solid var(--bd);border-radius:12px;padding:12px 20px;margin:18px 0}
.derive p{margin:10px 0}
.st{display:inline-block;min-width:1.8em;text-align:center;background:var(--ac);color:#fff;border-radius:7px;
  font-weight:700;font-size:.9rem;padding:0 6px;margin-right:8px}
.rebuild{background:#fff;border:3px dashed var(--key);border-radius:16px;padding:14px 22px;margin:24px 0}
.rb-h{font-weight:700;color:var(--key);font-size:1.08rem;margin-bottom:4px}
.rebuild ol{margin:6px 0}
.tg{display:inline-block;font-size:.78rem;font-weight:700;padding:1px 9px;border-radius:10px;vertical-align:2px;color:#fff}
.tg.must{background:#c62828} .tg.half{background:#ef6c00} .tg.give{background:#2e7d32}
.sd{display:inline-block;font-weight:700;color:#fff;border-radius:8px;padding:0 9px}
.sd.t{background:var(--tension)} .sd.w{background:var(--warn)} .sd.c{background:var(--comp)} .sd.k{background:var(--key)}
.fig{background:#fff;border:1px solid var(--bd);border-radius:12px;padding:18px 14px 12px;margin:24px 0;overflow-x:auto}
.fig>svg{display:block;margin:0 auto;max-width:100%;height:auto}
.fig svg text{font-family:"Microsoft JhengHei","Noto Sans CJK TC","Noto Sans TC",sans-serif}
.fig .cap{font-size:.9rem;color:var(--mut);text-align:left;margin:12px 6px 0;line-height:1.7}
table{width:100%;border-collapse:collapse;margin:18px 0;font-size:.95rem;background:#fff}
th,td{border:1px solid var(--bd);padding:9px 11px;text-align:left;vertical-align:top}
th{background:#eceff1;font-weight:700}
ul,ol{margin:10px 0 10px 4px;padding-left:26px}
li{margin:6px 0}
ol.big>li,ul.big>li{margin:10px 0}
.note{font-size:.88rem;color:var(--mut)}
details{background:#fff;border:1px solid var(--bd);border-radius:10px;padding:12px 16px;margin:14px 0}
summary{cursor:pointer;font-weight:700;color:var(--ac)}
details[open] summary{margin-bottom:8px}
details>p{border-left:4px solid #c5e1a5;padding-left:14px;margin:8px 0}
.katex{font-size:1.08em}
.katex-display{margin:16px 0!important;overflow-x:auto;overflow-y:hidden;padding:4px 0}
.chmap td:first-child{text-align:center;font-weight:700}
footer{text-align:center;color:var(--mut);font-size:.85rem;padding:28px;border-top:1px solid var(--bd)}
@media print{
  html{font-size:12pt}
  body{background:#fff}
  nav{display:none}
  header{-webkit-print-color-adjust:exact;print-color-adjust:exact;padding:24px 22px}
  main{max-width:none;padding:0 4mm}
  h2{break-before:page;break-after:avoid;margin-top:0}
  main>section:first-child>h2{break-before:auto}
  h3,h4{break-after:avoid}
  .fig,table,.why,.trap,.check,.derive,.rebuild,.seed,details{break-inside:avoid}
  details{border:1px dashed #bbb}
  details>*{display:block}
  .fig,.why,.trap,.check,.tg,.sd,.kw,.st,.seed{-webkit-print-color-adjust:exact;print-color-adjust:exact}
  @page{size:A4;margin:14mm 13mm 16mm}
}
'''


def fig_html(name, cap, mods):
    for m in mods:
        if name in m.ALL:
            return f'<div class="fig" id="{name}">\n{m.ALL[name]()}\n<div class="cap">{cap}</div>\n</div>'
    raise KeyError(f'找不到圖 {name}：請在 figs_chN.py 的 ALL 加入')


def build(cfg, V, out=None):
    mods = []
    for ch in V['chapters']:
        try:
            mods.append(importlib.import_module('figs_' + ch))
        except ModuleNotFoundError:
            pass
    body, navs = [], []
    for ch in V['chapters']:
        src = open(ch + '.html', encoding='utf8').read()
        src = re.sub(r'\{\{FIG:([\w]+)\|(.*?)\}\}', lambda m: fig_html(m.group(1), m.group(2), mods), src, flags=re.S)
        body.append(src)
        m = re.search(r'<h2[^>]*>(.*?)</h2>', src, re.S)
        t = re.sub(r'<[^>]+>', '', m.group(1)) if m else ch
        num = re.match(r'第\s*(\d+)\s*章', t)
        short = re.sub(r'\\\(.*?\\\)', '', t.split('　', 1)[-1].split('：')[0]).strip()
        navs.append(f'<a href="#{ch}">{num.group(1) if num else ""} {short}</a>')
    assert '{{FIG:' not in ''.join(body), '還有未解析的 {{FIG:}}'
    links = ''.join(f'<a href="{h}">{t}</a>' for h, t in cfg.get('nav_links', []))
    for o in cfg['volumes']:
        if o['key'] != V['key']:
            links += f'<a class="vol" href="{o["file"]}">{o.get("nav_label", o["h1"])}</a>'
    today = datetime.date.today().isoformat()
    theme = V.get('theme', 'a')
    hcls = f' class="{theme}"' if theme in ('c', 'a', 'k') else ''
    html = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{V['title']}</title>
<link rel="stylesheet" href="assets/katex/katex.min.css">
<script defer src="assets/katex/katex.min.js"></script>
<script defer src="assets/katex/auto-render.min.js"
  onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'\\\\(',right:'\\\\)',display:false}}],throwOnError:false}});document.body.dataset.katex='done';"></script>
<style>{CSS}</style>
</head>
<body>
<header{hcls}>
<h1>{V['h1']}</h1>
<p class="sub">{V.get('sub', '')}</p>
<div class="meta">{cfg.get('meta', '')}｜{today}</div>
</header>
<nav>{''.join(navs)}{links}</nav>
<main>
{''.join(body)}
</main>
<footer>{cfg['code']} 教科書講義（{V['h1']}）｜由 study/figs-src/textbook-{cfg['code']}/build.py 組裝；圖全部由 figs_ch*.py 依 calcs.py 數值以程式繪製｜{today}</footer>
</body>
</html>
'''
    out = out or os.path.join('..', '..', V['file'])
    open(out, 'w', encoding='utf8').write(html)
    print('wrote', out, len(html))
    return out


if __name__ == '__main__':
    cfg = json.load(open('textbook.json', encoding='utf8'))
    key = sys.argv[1] if len(sys.argv) > 1 else cfg['volumes'][0]['key']
    vols = cfg['volumes'] if key == 'all' else [v for v in cfg['volumes'] if v['key'] == key]
    assert vols, f'textbook.json 沒有冊 {key}'
    for V in vols:
        build(cfg, V, sys.argv[2] if len(sys.argv) > 2 and key != 'all' else None)
