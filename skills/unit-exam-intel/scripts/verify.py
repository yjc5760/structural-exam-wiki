#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit-exam-intel / verify.py
===========================
把成果頁 study/study-XX-Un-m.html 跟 question_index.json 對帳。

存在的理由：命題情報頁的每個數字都可以被重算，所以每個數字都應該被重算。
人眼看不出「篩選鈕寫 (7) 但實際 8 筆」，程式看得出來。

用法：
    python3 scripts/verify.py SS-U1-1
    python3 scripts/verify.py SS-U1-1 --page study/study-SS-U1-1.html

離開碼 0 = 全過；1 = 有錯（錯誤逐條列出）。
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stats import analyse, load_index  # noqa: E402


def parse_q_array(html):
    """抽出模板裡的 Q[] 陣列，回傳 list of dict。"""
    m = re.search(r'const\s+Q\s*=\s*\[(.*?)\n\];', html, re.S)
    if not m:
        return None
    rows = []
    for line in m.group(1).splitlines():
        line = line.strip().rstrip(',')
        if not line.startswith('['):
            continue
        try:
            v = json.loads(line)
        except json.JSONDecodeError:
            return ('PARSE_ERROR', line[:80])
        rows.append({
            'moduleId': v[0], 'cat': v[1], 'summary': v[2], 'tags': v[3],
            'viz': v[4], 'designMethod': v[5] if len(v) > 5 else None,
            'isPrimary': bool(v[6]) if len(v) > 6 else None,
            'secOwner': v[7] if len(v) > 7 else '',
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('unit')
    ap.add_argument('--page')
    ap.add_argument('--index', default='raw/json/question_index.json')
    a = ap.parse_args()

    page = a.page or f'study/study-{a.unit}.html'
    if not os.path.exists(page):
        sys.exit(f'找不到成果頁：{page}')

    html = open(page, encoding='utf-8').read()
    ref = analyse(load_index(a.index), a.unit)
    errs, warns = [], []

    # ---- 1. Q[] 題號集合 ----
    rows = parse_q_array(html)
    if rows is None:
        errs.append('找不到 const Q = [...] 陣列')
        rows = []
    elif isinstance(rows, tuple):
        errs.append(f'Q[] 有一列不是合法 JSON：{rows[1]}')
        rows = []

    want = {q['moduleId']: q for q in ref['questions']}
    got = {r['moduleId']: r for r in rows}
    missing = sorted(set(want) - set(got))
    extra = sorted(set(got) - set(want))
    if missing:
        errs.append(f'Q[] 漏題 {len(missing)} 筆：{missing}')
    if extra:
        errs.append(f'Q[] 多出不屬於本單元的題目：{extra}')

    # ---- 2. 逐題欄位一致 ----
    for mid in sorted(set(want) & set(got)):
        w, g = want[mid], got[mid]
        if g['isPrimary'] is not None and g['isPrimary'] != w['isPrimary']:
            errs.append(f'{mid} 主/副旗標不符：頁面 {g["isPrimary"]}、索引 {w["isPrimary"]}')
        if w['designMethod'] and g['designMethod'] and g['designMethod'] != w['designMethod']:
            errs.append(f'{mid} designMethod 不符：頁面 {g["designMethod"]}、索引 {w["designMethod"]}')
        if not w['isPrimary'] and not g['secOwner']:
            warns.append(f'{mid} 是副考點但沒填所屬單元（Q[] 第 8 欄）')

    # ---- 3. 篩選鈕數字 ----
    cats = {}
    for r in rows:
        cats[r['cat']] = cats.get(r['cat'], 0) + 1
    n_pri = sum(1 for r in rows if r['isPrimary'])
    n_sec = len(rows) - n_pri
    btn_re = re.compile(r"""<button[^>]*onclick="filterQ\('([A-Z]+)'[^"]*"[^>]*>"""
                        r"""([^<（(]*)[（(](\d+)[）)]\s*</button>""")
    seen_btn = set()
    for code, label, n in btn_re.findall(html):
        label, n = label.strip(), int(n)
        seen_btn.add(code)
        exp = {'ALL': len(rows), 'PRI': n_pri, 'SEC': n_sec}.get(code, cats.get(code, 0))
        if n != exp:
            errs.append(f'篩選鈕「{label}」（{code}）寫 {n}，實際 {exp}')
    for code in cats:
        if code not in seen_btn:
            errs.append(f'分群 {code} 有 {cats[code]} 題，但沒有對應的篩選鈕')
    for code in ('ALL', 'PRI', 'SEC'):
        if code not in seen_btn:
            warns.append(f'缺少 {code} 篩選鈕')

    # ---- 4. KPI 數字 ----
    t, y = ref['totals'], ref['years']
    kpis = re.findall(r'<div class="n">([^<]+)</div><div class="l">([^<]*)</div>', html)
    kpi_txt = ' | '.join(f'{v} {l}' for v, l in kpis)
    checks = [
        (str(t['primary']), '主考點題數'),
        (f"{t['share_pct']}%", '佔全科比例'),
        (f"#{t['rank']}", '全科排名'),
        (f"{y['recent6']['hit_years']}/6", '近 6 考年出題年數'),
    ]
    for val, what in checks:
        if not any(v.strip() == val for v, _ in kpis):
            errs.append(f'KPI「{what}」應為 {val}，頁面上找不到（現有：{kpi_txt}）')
    # 近 6 考年題數常被寫錯，額外抓一次
    m = re.search(r'近\s*6\s*考年[^（(]*[（(][^）)]*?共\s*(\d+)\s*題', html)
    if m and int(m.group(1)) != y['recent6']['questions']:
        errs.append(f"近 6 考年題數寫 {m.group(1)}，實際 {y['recent6']['questions']}")

    # ---- 5. 題號連結 ----
    links = re.findall(r'problems-view/([A-Z]{2}-\d{4}-\d+)\.html', html)
    if 'problems-view/' in html:
        for mid in sorted(set(want)):
            p = f'study/problems-view/{mid}.html'
            if not os.path.exists(p):
                errs.append(f'{mid} 的渲染頁不存在：{p}')
    elif rows:
        warns.append('題號未連向 problems-view/（該科可能還沒建渲染層）')

    # ---- 6. 禁用寫法 ----
    for bad, why in [
        ('../index.html#md=', '舊式 .md 連結，瀏覽器不會渲染公式'),
        ('javascript:history.back()', '在 target=_blank 新分頁裡按了沒反應'),
    ]:
        if bad in html:
            errs.append(f'頁面殘留「{bad}」——{why}')
    for m in re.findall(r'<h3[^>]*>\s*(\d\.\d)\s', html):
        errs.append(f'區塊小標仍帶編號「{m}」，本版已廢除編號')

    # ---- 報告 ----
    print(f'對帳：{page}  ←→  {a.index}')
    print(f'  索引：主 {t["primary"]}、副 {t["secondary"]}、合計 {t["listed"]}')
    print(f'  頁面：Q[] {len(rows)} 筆（主 {n_pri}、副 {n_sec}），分群 {cats}')
    for w in warns:
        print('  ⚠️  ' + w)
    if errs:
        print(f'\n❌ 不通過，{len(errs)} 項：')
        for e in errs:
            print('   - ' + e)
        sys.exit(1)
    print('\n✅ 全部通過')


if __name__ == '__main__':
    main()
