#!/usr/bin/env python3
"""交叉驗證：公式卡的 ok 年份清單 與 逐年證據表的 ✔ 必須完全一致。

用法:  python3 verify.py <html路徑> <對照表.json>

對照表格式（把矩陣欄位對應到卡片名稱，欄位索引從 3 起算）：
    {"3": ["λc 定義"], "4": ["Fcr 舊版", "Fcr 新版", "Fcr 彈性"], ...}

這一關不能用眼睛看。SS-U1-1 那輪就是靠它抓到 2 筆矛盾
（2008 整區參考公式漏標、2009 把「叫你自己算」誤標成「有給」）。
"""
import json, subprocess, sys, tempfile, os

HTML, MAPFILE = sys.argv[1], sys.argv[2]
src = open(HTML, encoding='utf-8').read()
js = src.split('<script>')[-1].split('</script>')[0].split('/* ---------- 渲染')[0]

tmp = os.path.join(tempfile.gettempdir(), 'ufm_data.js')
open(tmp, 'w', encoding='utf-8').write(js)
data = json.loads(subprocess.run(
    ['node', '-e',
     "const s=require('fs').readFileSync(%r,'utf8');"
     "const {F,MX}=new Function(s+'; return {F,MX};')();"
     "console.log(JSON.stringify({F,MX}))" % tmp],
    capture_output=True, text=True, check=True).stdout)
F, MX = data['F'], data['MX']
mapping = json.load(open(MAPFILE, encoding='utf-8'))

by = {f['nm']: f for f in F}
bad = 0

for col, names in mapping.items():
    col = int(col)
    ok = set()
    for n in names:
        if n not in by:
            print('✗ 對照表指到不存在的卡片：%s' % n); bad += 1; continue
        ok |= set(by[n]['ok'])
    for r in MX:
        flag, has = r[col] == 1, r[0] in ok
        if flag != has:
            print('✗ 欄 %d 年 %d：矩陣=%d 卡片=%d（%s）'
                  % (col, r[0], flag, has, names[0]))
            bad += 1

# 級別統計 + 基本健檢
lv = {}
for f in F:
    lv[f['lv']] = lv.get(f['lv'], 0) + 1
    if not f['eq'].strip().startswith('$$'):
        print('✗ 公式非顯示模式（應以 $$ 包住）：%s' % f['nm']); bad += 1
    if '$' in f['meta'].replace('$$', ''):
        print('✗ 說明含單一 $（KaTeX 不會渲染，請改 \\\\( \\\\)）：%s' % f['nm']); bad += 1
    if not f['ok'] and not f['no']:
        print('⚠ 無任何年份證據：%s' % f['nm'])

print('公式 %d 條 %s ｜ 逐年 %d 列' % (len(F), lv, len(MX)))
print('✗ %d 處不一致' % bad if bad else '✓ 全部一致')
sys.exit(1 if bad else 0)
