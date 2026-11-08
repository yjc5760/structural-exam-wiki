#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
subject-frequency-map / build_frequency.py
==========================================
產生「全科出題頻率熱圖」單一自包含 HTML：study/frequency-XX.html

一句話：把整科的題目攤在「所有子項 × 所有考年」的格子上，回答「整科該從哪裡開始讀」。

用法：
    python3 skills/subject-frequency-map/scripts/build_frequency.py            # 自動偵測科目
    python3 skills/subject-frequency-map/scripts/build_frequency.py --subject SS
    python3 .../build_frequency.py --index raw/json/question_index.json \
                                   --taxonomy raw/json/syllabus_taxonomy.json \
                                   --study-dir study --out study/frequency-SS.html
    python3 .../build_frequency.py --check      # 只跑對帳，不寫檔

設計鐵律（跟 unit-exam-intel 一致）：
    頁面上出現的每個數字都由本檔從 question_index.json 算出，一律不手打、不憑印象。
    科目名稱、子項名稱、單元劃分一律取自 syllabus_taxonomy.json。
"""

import argparse
import collections
import glob
import json
import os
import re
import sys

MODULE_RE = re.compile(r"^([A-Z]{2})-(\d{4})-(\d+)$")


# ------------------------------------------------------------------ 讀檔
def load_index(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d["questions"] if isinstance(d, dict) else d


def load_taxonomy(path, subject):
    """回傳 (科目全名, [(子項id, 子項名, 單元id)], {單元id: 單元名})"""
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    subj = next((s for s in d.get("subjects", []) if s["id"] == subject), None)
    if subj is None:
        sys.exit(f"錯誤：syllabus_taxonomy.json 裡找不到科目 {subject}。"
                 f"現有科目：{[s['id'] for s in d.get('subjects', [])]}")
    items, unames = [], {}
    for u in subj.get("units", []):
        unames[u["id"]] = u.get("name", u["id"])
        for it in u.get("items", []):
            items.append((it["id"], it["name"], u["id"]))
    return subj.get("name", subject), items, unames


def detect_subject(questions):
    codes = collections.Counter(m.group(1) for q in questions
                                for m in [MODULE_RE.match(q["moduleId"])] if m)
    if not codes:
        sys.exit("錯誤：無法從 moduleId 判斷科目代碼（預期格式 XX-YYYY-N）。")
    if len(codes) > 1:
        print(f"⚠️  索引裡出現多個科目代碼 {dict(codes)}，取最多的那個。")
    return codes.most_common(1)[0][0]


def yr(mid):
    m = MODULE_RE.match(mid)
    return int(m.group(2)) if m else None


def qno(mid):
    m = MODULE_RE.match(mid)
    return int(m.group(3)) if m else None


# ------------------------------------------------------------------ 教材偵測
def scan_materials(study_dir, subject, tids):
    """掃描 study/，回傳 {子項id: [已存在的教材種類]}。不硬編任何清單。"""
    have = {t: [] for t in tids}
    for t in tids:
        checks = [
            ("study",   os.path.join(study_dir, f"study-{t}.html")),
            ("lecture", os.path.join(study_dir, f"lecture-{t}.html")),
            ("formula", os.path.join(study_dir, f"formula-given-{t}.html")),
        ]
        for kind, p in checks:
            if os.path.exists(p):
                have[t].append(kind)
        # 記憶片檔名含中文主題，用 glob 比對前綴＋尾綴，避免硬編名稱
        deck = sorted(glob.glob(os.path.join(study_dir, f"{t}_*記憶片.pdf")))
        if deck:
            have[t].append("deck")
            have[t + "__deckfile"] = os.path.basename(deck[0])
    return have


# ------------------------------------------------------------------ 統計
def analyse(questions, items, unames, materials):
    years = sorted({yr(q["moduleId"]) for q in questions} - {None})
    recent6 = years[-6:]
    total = len(questions)
    tids = [t for t, _, _ in items]

    per_year_total = collections.Counter(yr(q["moduleId"]) for q in questions)
    uniform = len(set(per_year_total.values())) == 1
    per_year = per_year_total[years[0]] if uniform else None

    grid = {t: {y: {"p": [], "s": []} for y in years} for t in tids}
    orphan = collections.Counter()
    for q in questions:
        y, mid = yr(q["moduleId"]), q["moduleId"]
        pt = q.get("primaryTopicId")
        if pt in grid:
            grid[pt][y]["p"].append(mid)
        else:
            orphan[pt] += 1
        for t in (q.get("secondaryTopicIds") or []):
            if t in grid:
                grid[t][y]["s"].append(mid)

    pri = collections.Counter(q.get("primaryTopicId") for q in questions)
    sec = collections.Counter(t for q in questions for t in (q.get("secondaryTopicIds") or []))
    ordered = [(k, v) for k, v in pri.most_common() if k in grid]
    rank = {k: i + 1 for i, (k, _) in enumerate(ordered)}

    rows = []
    for tid, name, uid in items:
        hits = [y for y in years if grid[tid][y]["p"]]
        best, run, span = 0, [], None
        for y in years:
            if y in hits:
                if len(run) > best:
                    best, span = len(run), (run[0], run[-1])
                run = []
            else:
                run.append(y)
        if len(run) > best:
            best, span = len(run), (run[0], run[-1])
        r6h = sum(1 for y in recent6 if grid[tid][y]["p"])
        r6q = sum(len(grid[tid][y]["p"]) for y in recent6)
        pos = collections.Counter(qno(m) for y in years for m in grid[tid][y]["p"])
        rows.append({
            "id": tid, "short": tid.split("-", 1)[1], "name": name, "unit": uid,
            "p": pri.get(tid, 0), "s": sec.get(tid, 0),
            "share": round(pri.get(tid, 0) / total * 100, 1) if total else 0.0,
            "rank": rank.get(tid), "hit": len(hits), "last": (hits[-1] if hits else None),
            "gap": best, "gapSpan": list(span) if span else None,
            "r6h": r6h, "r6q": r6q, "pos": dict(sorted(pos.items())),
            "mat": [k for k in ("study", "lecture", "formula", "deck") if k in materials.get(tid, [])],
            "deckFile": materials.get(tid + "__deckfile", ""),
            "cells": [{"p": len(grid[tid][y]["p"]), "s": len(grid[tid][y]["s"]),
                       "ids": grid[tid][y]["p"] + ["(副)" + m for m in grid[tid][y]["s"]]}
                      for y in years],
        })

    maxP = max((c["p"] for r in rows for c in r["cells"]), default=1) or 1
    maxA = max((c["p"] + c["s"] for r in rows for c in r["cells"]), default=1) or 1

    unit_tot = collections.Counter()
    unit_items = collections.defaultdict(list)
    for r in rows:
        unit_tot[r["unit"]] += r["p"]
        unit_items[r["unit"]].append(r["name"])

    return {
        "years": years, "recent6": recent6, "total": total, "rows": rows,
        "perYear": per_year, "uniform": uniform, "maxP": maxP, "maxA": maxA,
        "ordered": ordered, "unitTot": dict(unit_tot),
        "unitItems": {k: v for k, v in unit_items.items()}, "unames": unames,
        "orphan": dict(orphan),
    }


# ------------------------------------------------------------------ 對帳
def check(A):
    """回傳 (致命錯誤, 警告)。算術對不上是致命；孤兒 topicId 只警告（頁面會出紅框）。"""
    errs, warns = [], []
    rows, years = A["rows"], A["years"]
    cell_p = sum(c["p"] for r in rows for c in r["cells"])
    if cell_p + sum(A["orphan"].values()) != A["total"]:
        errs.append(f"熱圖主考點格子總和 {cell_p} ＋ 孤兒 {sum(A['orphan'].values())} "
                    f"≠ 題庫總題數 {A['total']}")
    for r in rows:
        if sum(c["p"] for c in r["cells"]) != r["p"]:
            errs.append(f"{r['id']} 列總和 {sum(c['p'] for c in r['cells'])} ≠ 主考點數 {r['p']}")
        if sum(c["s"] for c in r["cells"]) != r["s"]:
            errs.append(f"{r['id']} 副考點列總和不符")
    if sum(A["unitTot"].values()) != cell_p:
        errs.append("單元小計加總 ≠ 主考點總數")
    if A["orphan"]:
        warns.append(f"索引有 taxonomy 沒有的 primaryTopicId：{A['orphan']}"
                     f"（未畫進熱圖，頁面會顯示紅色警告框）")
    return errs, warns


# ------------------------------------------------------------------ 版型
CSS = """<style>
:root{--ac:#1565c0;--ac2:#e3f2fd;--bg:#f7f9fb;--card:#fff;--ink:#263238;--mut:#78909c;--bd:#e0e6ea;--warn:#c62828}
*{box-sizing:border-box}body{margin:0;font-family:"Microsoft JhengHei","Noto Sans TC",sans-serif;background:var(--bg);color:var(--ink);line-height:1.6}
header{background:linear-gradient(135deg,#0d47a1,#1976d2);color:#fff;padding:28px 24px}
header h1{margin:0 0 6px;font-size:1.5em}header p{margin:0;opacity:.85;font-size:.92em}
nav{position:sticky;top:0;z-index:9;background:#fff;border-bottom:2px solid var(--bd);padding:8px 16px;display:flex;flex-wrap:wrap;gap:6px}
nav a{text-decoration:none;color:var(--ac);font-size:.88em;padding:5px 10px;border-radius:16px;background:var(--ac2)}
nav a:hover{background:var(--ac);color:#fff}
main{max-width:1240px;margin:0 auto;padding:20px 16px 60px}
h2{font-size:1.25em;border-left:5px solid var(--ac);padding-left:10px;margin:26px 0 14px}
h3{font-size:1.05em;margin:30px 0 10px;padding-bottom:5px;border-bottom:2px solid var(--ac2)}
.role{background:#fffde7;border:1px solid #ffe082;border-left:5px solid #f9a825;border-radius:8px;padding:12px 16px;font-size:.88em;margin-bottom:12px}
.role b{color:#e65100}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.kpi{background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:14px;text-align:center}
.kpi .n{font-size:1.9em;font-weight:700;color:var(--ac)}.kpi .l{font-size:.82em;color:var(--mut)}
.note{font-size:.85em;color:var(--mut);background:#fff;border:1px dashed var(--bd);border-radius:8px;padding:10px 14px;margin-top:12px}
.tw{overflow-x:auto;background:#fff;border:1px solid var(--bd);border-radius:10px;padding:10px}
table{border-collapse:collapse;width:100%;background:#fff;font-size:.88em}
th,td{border:1px solid var(--bd);padding:6px 8px;text-align:left;vertical-align:middle}
th{background:var(--ac2);position:sticky;top:0}
td.num,th.num{text-align:center;font-variant-numeric:tabular-nums}
#hm td,#hm th{border:1px solid #eceff1;padding:0;text-align:center}
#hm th.rowh{text-align:left;padding:4px 8px;white-space:nowrap;background:#fff;position:sticky;left:0;z-index:3;border-right:2px solid var(--bd)}
#hm th.yr{font-size:.72em;font-weight:600;color:var(--mut);background:#fff;padding:3px 0;min-width:26px}
#hm th.yr.r6{background:#fff8e1;color:#e65100}
#hm td.c{width:26px;height:26px;font-size:.78em;font-weight:700;cursor:default}
#hm td.c.r6{outline:1px solid #ffcc80;outline-offset:-1px}
#hm tr.usep td,#hm tr.usep th{background:#f2f5f8;height:6px;padding:0;border:none}
.sec-dot{position:absolute;right:2px;bottom:1px;width:5px;height:5px;border-radius:50%;background:#ef6c00}
.cellwrap{position:relative;width:100%;height:100%;display:flex;align-items:center;justify-content:center}
.legend{display:flex;flex-wrap:wrap;gap:14px;align-items:center;font-size:.84em;color:var(--mut);margin:10px 0 0}
.sw{display:inline-block;width:20px;height:16px;border:1px solid #cfd8dc;vertical-align:middle;margin-right:4px}
.btns{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}
.fbtn{border:1px solid var(--bd);background:#fff;border-radius:18px;padding:6px 14px;cursor:pointer;font-size:.88em;font-family:inherit}
.fbtn.on{background:var(--ac);color:#fff;border-color:var(--ac)}
.bar{display:inline-block;height:13px;border-radius:3px;vertical-align:middle;background:var(--ac)}
.bar2{display:inline-block;height:13px;border-radius:3px;vertical-align:middle;background:#ffcc80}
.tag{font-size:.72em;border-radius:9px;padding:1px 7px;margin-right:3px;white-space:nowrap;display:inline-block}
a.tag{text-decoration:none}
.t-y{background:#e8f5e9;color:#1b5e20}a.t-y:hover{background:#1b5e20;color:#fff}
.t-n{background:#fafafa;color:#bdbdbd}
.zero{background:#fce4ec !important}
footer{text-align:center;color:var(--mut);font-size:.8em;padding:20px}
@media(max-width:760px){#hm td.c{width:20px;height:22px;font-size:.7em}}
</style>"""

JS = """<script>
const D = __DATA__;
const YEARS = D.years, R6 = new Set(D.recent6);
let MODE = 'p';

function shade(v, max){
  if(!v) return '#f7fafc';
  const t = Math.min(1, v / max);
  const a=[227,242,253], b=[13,71,161];
  const c=a.map((x,i)=>Math.round(x+(b[i]-x)*(0.25+0.75*t)));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}
function fg(v, max){ return (!v) ? '#cfd8dc' : ((v/max)>0.45 ? '#fff' : '#0d47a1'); }

function drawHeat(){
  const max = MODE==='p' ? D.maxP : D.maxA;
  let h = '<table id="hm"><thead><tr><th class="rowh">子項</th>';
  YEARS.forEach(y=>{ h += `<th class="yr${R6.has(y)?' r6':''}">${String(y).slice(2)}</th>`; });
  h += '<th class="yr" style="min-width:42px">合計</th></tr></thead><tbody>';
  let lastUnit = null;
  D.rows.forEach(r=>{
    if(lastUnit && r.unit!==lastUnit) h += `<tr class="usep"><td colspan="${YEARS.length+2}"></td></tr>`;
    lastUnit = r.unit;
    const tot = MODE==='p' ? r.p : (r.p + r.s);
    h += `<tr><th class="rowh"><b>${r.short}</b> ${r.name}</th>`;
    r.cells.forEach((c,i)=>{
      const v = MODE==='p' ? c.p : (c.p + c.s);
      const y = YEARS[i];
      const tip = c.ids.length ? `${y}：${c.ids.join('、')}` : `${y}：無`;
      h += `<td class="c${R6.has(y)?' r6':''}" style="background:${shade(v,max)};color:${fg(v,max)}" title="${tip}">`
         + `<div class="cellwrap">${v||''}${(MODE==='p'&&c.s)?'<span class="sec-dot"></span>':''}</div></td>`;
    });
    h += `<td class="c" style="background:#fff;color:#0d47a1;font-weight:700;min-width:42px">${tot||'0'}</td></tr>`;
  });
  h += '</tbody></table>';
  document.getElementById('heat').innerHTML = h;
  let lg = '';
  for(let v=0; v<=max; v++) lg += `<span><span class="sw" style="background:${shade(v,max)}"></span>${v} 題</span>`;
  lg += (MODE==='p' ? '<span>🟠 右下角橘點 ＝ 該年該子項還有副考點</span>'
                    : '<span>此模式的格值 ＝ 主考點 ＋ 副考點</span>');
  lg += `<span>黃框欄位 ＝ 近 ${D.recent6.length} 考年（${D.recent6[0]}–${D.recent6[D.recent6.length-1]}）</span>`;
  document.getElementById('lg').innerHTML = lg;
}
function setMode(m, btn){
  MODE = m;
  document.querySelectorAll('#modebtns .fbtn').forEach(b=>b.classList.remove('on'));
  btn.classList.add('on');
  drawHeat();
}
function drawRank(){
  const maxP = Math.max(1, ...D.rows.map(r=>r.p));
  const sorted = [...D.rows].sort((a,b)=> (a.rank||9999)-(b.rank||9999) || b.s-a.s);
  const lbl = {study:'命題分析',lecture:'講義',formula:'給／背',deck:'記憶片'};
  let h = '<table><thead><tr><th class="num">#</th><th>子項</th><th class="num">主</th><th>主考點量</th>'
        + '<th class="num">副</th><th class="num">佔全科</th><th class="num">出現<br>年數</th>'
        + '<th class="num">最長<br>空窗</th><th class="num">最後<br>出現</th>'
        + `<th class="num">近 ${D.recent6.length} 考年</th>`
        + '<th>常見題號位置</th><th>現有教材</th></tr></thead><tbody>';
  sorted.forEach(r=>{
    const w = r.p/maxP*150, w2 = r.s/maxP*150;
    const pos = Object.entries(r.pos).map(([k,v])=>`第${k}題×${v}`).join('、') || '—';
    const href = {study:`study-${r.id}.html`, lecture:`lecture-${r.id}.html`,
                  formula:`formula-given-${r.id}.html`, deck:r.deckFile};
    const tags = ['study','lecture','formula','deck'].map(m=> r.mat.includes(m)
        ? `<a class="tag t-y" href="${encodeURI(href[m])}" target="_blank">${lbl[m]}</a>`
        : `<span class="tag t-n">${lbl[m]}</span>`).join('');
    const nm = r.mat.includes('study')
        ? `<a href="study-${r.id}.html" target="_blank" style="color:var(--ac);text-decoration:none"><b>${r.short}</b> ${r.name}</a>`
        : `<b>${r.short}</b> ${r.name}`;
    h += `<tr${r.p===0?' class="zero"':''}><td class="num">${r.p? (r.rank||'') : '—'}</td>`
      + `<td>${nm}</td><td class="num"><b>${r.p}</b></td>`
      + `<td><span class="bar" style="width:${w}px"></span><span class="bar2" style="width:${w2}px"></span></td>`
      + `<td class="num">${r.s}</td><td class="num">${r.share}%</td>`
      + `<td class="num">${r.hit}/${YEARS.length}</td>`
      + `<td class="num">${r.gap?`${r.gap} 年<br><span style="font-size:.82em;color:#90a4ae">${r.gapSpan[0]}–${r.gapSpan[1]}</span>`:'—'}</td>`
      + `<td class="num">${r.last||'—'}</td>`
      + `<td class="num">${r.r6h}/${D.recent6.length}<br><span style="font-size:.82em;color:#90a4ae">${r.r6q} 題</span></td>`
      + `<td style="font-size:.82em;color:#78909c">${pos}</td><td>${tags}</td></tr>`;
  });
  h += '</tbody></table>';
  document.getElementById('rank').innerHTML = h;
}
drawHeat(); drawRank();
</script>"""


def build_html(subject, subj_name, A, today):
    rows, years, N = A["rows"], A["years"], A["total"]
    ordered = A["ordered"]
    appeared = sum(1 for r in rows if r["p"] > 0)
    top = ordered[0] if ordered else (None, 0)
    topN = lambda n: [k for k, _ in ordered[:n]]
    sumN = lambda n: sum(v for _, v in ordered[:n])
    by_id = {r["id"]: r for r in rows}
    zero = [f'{r["short"]} {r["name"]}' for r in rows if r["p"] == 0]
    tools = sorted([r for r in rows if r["s"] > r["p"]], key=lambda r: -r["s"])[:4]

    # ---- 單元權重列 ----
    ur = ""
    for uid, name in A["unames"].items():
        t = A["unitTot"].get(uid, 0)
        ur += (f'<tr><td><b>{uid}</b> {name}</td><td class="num">{t}</td>'
               f'<td class="num">{round(t / N * 100, 1) if N else 0}%</td>'
               f'<td>{"、".join(A["unitItems"].get(uid, []))}</td></tr>\n')
    tot_sorted = sorted(A["unitTot"].items(), key=lambda kv: -kv[1])
    if len(tot_sorted) >= 2 and tot_sorted[-1][1] > 0:
        hi, lo = tot_sorted[0], tot_sorted[-1]
        ratio = (f'最重的 <b>{hi[0]}</b>（{hi[1]} 題）是最輕的 <b>{lo[0]}</b>（{lo[1]} 題）的 '
                 f'<b>{round(hi[1] / lo[1], 1)} 倍</b>')
    else:
        ratio = "各單元題數分布請見上表"
    unit_note = f'📌 換算成投資：{ratio}。'
    if zero:
        unit_note += f'　另外注意：<b>{"、".join(zero)}</b> {len(years)} 個考年 <b>0 題</b>——命題大綱裡有、考卷上從沒以它為主考點出現過，可以直接跳過。'

    # ---- 讀書順序表（全部由資料生成）----
    def chain(ids):
        return " → ".join(f'{by_id[i]["short"]}' for i in ids)

    n5, n3 = min(5, len(ordered)), min(3, len(ordered))
    full5 = sum(1 for i in topN(n5) if len(by_id[i]["mat"]) == 4)
    minhit3 = min((by_id[i]["hit"] for i in topN(n3)), default=0)
    read = ""
    if ordered:
        read += (f'<tr><td><b>時間充裕，要拿高分</b></td><td>{chain(topN(n5))}</td>'
                 f'<td>這 {n5} 個合計 {sumN(n5)} 題，佔全科 {round(sumN(n5) / N * 100, 1)}%'
                 f'{f"。其中 {full5} 個已有完整教材（講義＋給／背＋命題分析＋記憶片）" if full5 else ""}</td></tr>\n')
        read += (f'<tr><td><b>只剩一個月</b></td><td>'
                 + "、".join(f'{by_id[i]["short"]}（{by_id[i]["p"]} 題）' for i in topN(n3)) + '</td>'
                 f'<td>合計 {sumN(n3)} 題、佔 {round(sumN(n3) / N * 100, 1)}%；'
                 f'三者的出現年數都在 {minhit3} 年以上，是最穩定的柱子</td></tr>\n')
    if tools:
        read += ('<tr><td><b>想補「每題都用得到」的基本功</b></td><td>'
                 + "、".join(f'{r["short"]}（副 {r["s"]}）' for r in tools) + '</td>'
                 '<td>切到「主＋副」模式，這幾列會整片變深——副考點題數全科最高，'
                 '而且都超過自己的主考點題數，是別人的入口</td></tr>\n')
    read += (f'<tr><td><b>想押近年趨勢</b></td><td>看熱圖黃框那 {len(A["recent6"])} 欄</td>'
             f'<td>近 {len(A["recent6"])} 考年（{A["recent6"][0]}–{A["recent6"][-1]}）共 '
             f'{sum(r["r6q"] for r in rows)} 題，集中在少數幾列。空窗最久的反而常是下一次的回歸點</td></tr>\n')
    read += (f'<tr><td><b>想知道哪些可以不讀</b></td><td>{"、".join(zero) if zero else "（無：每個子項都考過）"}</td>'
             f'<td>{"".join([f"{len(years)} 年 0 題。命題大綱有列，但考卷上從沒以它為主考點出現過"]) if zero else "本科每個子項都至少當過一次主考點，沒有可以整段跳過的"}</td></tr>\n')

    col_note = (f'每一欄一定剛好 {A["perYear"]} 題（一年 {A["perYear"]} 題），所以某一年某個子項考了 2 題，就代表那年別的子項被擠掉了。'
                if A["uniform"] else '每一欄的總和等於該年的題數，可以直接讀出各子項之間的排擠關係。')
    year_desc = (f'{len(years)} 個考年 × 每年 {A["perYear"]} 題 = {N} 題'
                 if A["uniform"] else f'{len(years)} 個考年、共 {N} 題')
    kpi4 = "／".join(str(A["unitTot"].get(u, 0)) for u in A["unames"])
    kpi4l = "／".join(u.split("-")[-1] for u in A["unames"]) + " 各單元的題數分配"

    orphan_html = ""
    if A["orphan"]:
        orphan_html = ('<div class="role" style="background:#ffebee;border-color:#ef9a9a;border-left-color:#c62828">'
                       '⚠️ <b>資料異常</b>：索引裡有 taxonomy 找不到的 <code>primaryTopicId</code>：'
                       + "、".join(f"<code>{k}</code>×{v}" for k, v in A["orphan"].items())
                       + '。這些題目<b>沒有</b>畫進熱圖，總數會對不上——請先修正 <code>question_index.json</code> 或 '
                         '<code>syllabus_taxonomy.json</code>。</div>')

    data_json = json.dumps({
        "years": years, "recent6": A["recent6"], "rows": rows,
        "maxP": A["maxP"], "maxA": A["maxA"],
    }, ensure_ascii=False, separators=(",", ":"))

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{subject} 全科出題頻率熱圖｜{subj_name}</title>
{CSS}
</head>
<body>
<header>
<h1>{subject} {subj_name} — 全科出題頻率熱圖</h1>
<p>{years[0]}–{years[-1]}，{year_desc}｜資料來源：raw/json/question_index.json｜更新日期 {today}</p>
</header>
<nav>
<a href="#s-heat">頻率熱圖</a><a href="#s-rank">排名總表</a><a href="#s-unit">各單元的權重</a><a href="#s-read">怎麼用這張表</a>
</nav>
<main>

{orphan_html}
<div class="role">
📊 <b>這張表只回答一件事：整科該從哪裡開始讀。</b>
它把 {N} 題逐題攤在「{len(rows)} 個子項 × {len(years)} 個考年」的格子上，
讓你一眼看出誰是主力、誰是工具型、誰空窗很久、誰根本沒考過。
每個子項的細節（考點結構、漂移、風險排序）看該子項的 <code>study-{subject}-Un-m.html</code> 命題分析頁。<br>
所有數字都可以用 <code>python3 skills/unit-exam-intel/scripts/stats.py {subject}-Un-m</code> 逐項複算。
</div>

<h2>出題概況</h2>
<div class="kpis">
<div class="kpi"><div class="n">{N}</div><div class="l">總題數（{year_desc}）</div></div>
<div class="kpi"><div class="n">{appeared}/{len(rows)}</div><div class="l">曾當過主考點的子項</div></div>
<div class="kpi"><div class="n">{top[1]}</div><div class="l">第一名 {by_id[top[0]]["short"] if top[0] else "—"} 的題數（佔 {round(top[1] / N * 100, 1) if N else 0}%）</div></div>
<div class="kpi"><div class="n">{kpi4}</div><div class="l">{kpi4l}</div></div>
</div>

<h3 id="s-heat">頻率熱圖（滑過格子看題號）</h3>
<div class="btns" id="modebtns">
  <button class="fbtn on" onclick="setMode('p',this)">只看主考點</button>
  <button class="fbtn" onclick="setMode('a',this)">主考點 ＋ 副考點</button>
</div>
<div class="tw" id="heat"></div>
<div class="legend" id="lg"></div>
<div class="note">
📌 <b>看熱圖的三個切入點</b>：
① <b>橫著看</b>——一整列都很淡代表這個子項很少當主考點；有連續空白就是空窗年段。
② <b>直著看</b>——{col_note}
③ <b>切到「主＋副」模式</b>——顏色會整片變深的那幾列，就是「工具型子項」：它們本身很少單獨成題，卻是別人的第一步。
</div>

<h3 id="s-rank">排名總表</h3>
<div class="tw" id="rank"></div>
<div class="note">
藍色長條＝主考點題數，橘色接續段＝副考點題數。「常見題號位置」是該子項的主考點落在該年第幾題——
題號靠前多半是短題與名詞解釋，靠後多半是長計算題，這會影響你要練的答題節奏。
「現有教材」綠色可點、灰色表示尚未製作。
</div>

<h3 id="s-unit">各單元的權重</h3>
<div class="tw">
<table>
<thead><tr><th>單元</th><th class="num">主考點題數</th><th class="num">佔全科</th><th>包含的子項</th></tr></thead>
<tbody>
{ur}</tbody>
</table>
</div>
<div class="note">{unit_note}</div>

<h3 id="s-read">怎麼用這張表排讀書順序</h3>
<div class="tw">
<table>
<thead><tr><th>如果你…</th><th>先讀哪幾個子項</th><th>理由（可從熱圖直接驗證）</th></tr></thead>
<tbody>
{read}</tbody>
</table>
</div>
<div class="note">
📌 <b>一句話</b>：這張表告訴你「該讀哪裡」，各子項的 <code>study-{subject}-Un-m.html</code> 命題分析頁告訴你「那裡該先練哪幾題」，
<code>formula-given-{subject}-Un-m.html</code> 告訴你「那裡哪些公式非背不可」。三層一起用才完整。<br>
⚠️ <b>使用提醒</b>：頻率高不等於一定會再考，頻率低也不等於不會考——這張表的用途是<b>分配時間</b>，不是預測考題。
真正的押題請看各子項命題分析頁最後那張「命題風險排序」，那裡有空窗年數與近年趨勢的交叉判斷。
</div>

</main>
<footer>{subject} 全科出題頻率熱圖｜exam-wiki-{subject} 知識庫｜統計基準 raw/json/question_index.json（{N} 題／{len(years)} 考年）｜每個數字都可用 <code>scripts/stats.py</code> 複算</footer>
{JS.replace('__DATA__', data_json)}
</body>
</html>
"""


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", help="科目代碼（SS/RC/SA/SD/SM/MM）。不給就從 moduleId 自動偵測")
    ap.add_argument("--index", default="raw/json/question_index.json")
    ap.add_argument("--taxonomy", default="raw/json/syllabus_taxonomy.json")
    ap.add_argument("--study-dir", default="study")
    ap.add_argument("--out", help="輸出路徑，預設 <study-dir>/frequency-XX.html")
    ap.add_argument("--date", help="頁面上的更新日期，預設今天")
    ap.add_argument("--check", action="store_true", help="只跑對帳與摘要，不寫檔")
    a = ap.parse_args()

    for p in (a.index, a.taxonomy):
        if not os.path.exists(p):
            sys.exit(f"錯誤：找不到 {p}。請在知識庫根目錄執行，或用 --index / --taxonomy 指定。")

    qs = load_index(a.index)
    subject = a.subject or detect_subject(qs)
    subj_name, items, unames = load_taxonomy(a.taxonomy, subject)
    if not os.path.isdir(a.study_dir):
        print(f"⚠️  找不到 {a.study_dir}/，教材欄位會全部顯示為未製作。")
    materials = scan_materials(a.study_dir, subject, [t for t, _, _ in items])
    A = analyse(qs, items, unames, materials)

    errs, warns = check(A)
    print(f"科目 {subject} {subj_name}｜{len(A['years'])} 考年（{A['years'][0]}–{A['years'][-1]}）｜"
          f"{A['total']} 題｜{len(items)} 個子項（{sum(1 for r in A['rows'] if r['p'])} 個出現過）")
    print("單元權重：" + "　".join(
        f"{u} {A['unitTot'].get(u, 0)} ({round(A['unitTot'].get(u, 0) / A['total'] * 100, 1)}%)"
        for u in unames))
    if A["ordered"]:
        print("前五名：" + "、".join(f"{k.split('-', 1)[1]} {v}" for k, v in A["ordered"][:5])
              + f"　合計 {sum(v for _, v in A['ordered'][:5])} 題 "
                f"({round(sum(v for _, v in A['ordered'][:5]) / A['total'] * 100, 1)}%)")
    tools = [r for r in A["rows"] if r["s"] > r["p"]]
    print("副>主 的工具型子項：" + ("、".join(f"{r['short']}({r['p']}/{r['s']})" for r in tools) or "無"))
    print("0 題子項：" + ("、".join(r["short"] for r in A["rows"] if r["p"] == 0) or "無"))
    mat_full = [r["short"] for r in A["rows"] if len(r["mat"]) == 4]
    print(f"教材齊全（四種都有）的子項：{'、'.join(mat_full) or '無'}")

    for w in warns:
        print("⚠️  " + w)
    if errs:
        print("\n❌ 對帳不通過（算術對不上，先修資料再產頁）：")
        for e in errs:
            print("   - " + e)
        sys.exit(1)
    print("\n✅ 對帳通過（格子總和＝題庫總題數、每列總和＝該子項題數、單元小計相符）"
          + ("　※ 有警告，請看上面" if warns else ""))

    if a.check:
        return

    if a.date:
        today = a.date
    else:
        import datetime
        today = datetime.date.today().isoformat()

    out = a.out or os.path.join(a.study_dir, f"frequency-{subject}.html")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    html = build_html(subject, subj_name, A, today)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n寫出 {out}（{len(html):,} 字元）")


if __name__ == "__main__":
    main()
