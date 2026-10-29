#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit-exam-intel / stats.py
=========================
從 raw/json/question_index.json 算出「單元命題情報頁」需要的每一個數字。

存在的唯一理由：**這些數字不可以用手打。**
手打過的教訓（SS-U1-1，2026-08-08）：頁面寫「近 6 年 6/6」，實際是 4/6
（2019–2021 三年空白），錯了將近一年沒被發現，因為沒有人會去重數 24 個年份。

用法：
    python3 scripts/stats.py SS-U1-1                    # 印出人可讀的摘要
    python3 scripts/stats.py SS-U1-1 --json > out.json  # 給後續產頁用
    python3 scripts/stats.py SS-U1-1 --index path/to/question_index.json

輸出的每個欄位都直接對應成果頁的一個區塊，不要在頁面上寫本檔沒算出來的數字。
"""

import argparse
import collections
import json
import os
import re
import sys


def load_index(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    # 最外層是 dict，題目在 'questions' 鍵下；容許少數科目直接存 list
    return d["questions"] if isinstance(d, dict) else d


def load_taxonomy(path):
    """回傳 {unitId: unitName}；找不到檔案就回空 dict（呼叫端自行處理）。"""
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    out = {}
    for subj in d.get("subjects", []):
        for unit in subj.get("units", []):
            for item in unit.get("items", []):
                out[item["id"]] = item["name"]
    return out


def year_of(module_id):
    """SS-2015-3 → 2015（西元）。題號格式 XX-YYYY-N 為六科共通。"""
    m = re.match(r"^[A-Z]{2}-(\d{4})-\d+$", module_id)
    return int(m.group(1)) if m else None


def analyse(questions, unit):
    prim = [q for q in questions if q.get("primaryTopicId") == unit]
    sec = [q for q in questions if unit in (q.get("secondaryTopicIds") or [])]
    prim.sort(key=lambda q: q["moduleId"])
    sec.sort(key=lambda q: q["moduleId"])

    all_years = sorted({year_of(q["moduleId"]) for q in questions} - {None})
    hit_years = sorted({year_of(q["moduleId"]) for q in prim} - {None})

    # ---- 排名：本單元在全科的主考點題數排第幾 ----
    rank_tbl = collections.Counter(q.get("primaryTopicId") for q in questions)
    ordered = rank_tbl.most_common()
    rank = next((i + 1 for i, (k, _) in enumerate(ordered) if k == unit), None)
    top3 = [{"unit": k, "count": v} for k, v in ordered[:3]]
    # 名次相鄰者：排在本單元「上面一名」與「下面一名」的單元
    above = ({"unit": ordered[rank - 2][0], "count": ordered[rank - 2][1]}
             if rank and rank >= 2 else None)
    below = ({"unit": ordered[rank][0], "count": ordered[rank][1]}
             if rank and rank < len(ordered) else None)

    # ---- 近 N 個考年（以考年為單位，不是以西元年為單位）----
    def recent(n):
        yrs = all_years[-n:]
        hits = [y for y in yrs if y in hit_years]
        cnt = sum(1 for q in prim if year_of(q["moduleId"]) in yrs)
        return {"span": [yrs[0], yrs[-1]], "years": n,
                "hit_years": len(hits), "questions": cnt}

    # ---- 空窗：連續沒出現的年段 ----
    gaps = []
    run = []
    for y in all_years:
        if y in hit_years:
            if len(run) >= 2:
                gaps.append([run[0], run[-1]])
            run = []
        else:
            run.append(y)
    if len(run) >= 2:
        gaps.append([run[0], run[-1]])

    # ---- 前後對切（考點漂移用）----
    half = len(prim) // 2
    early, late = prim[:half], prim[half:]

    def span(group):
        ys = [year_of(q["moduleId"]) for q in group]
        return [min(ys), max(ys)] if ys else []

    # ---- 設計法（部分科目可能沒有這個欄位）----
    def methods(group):
        return dict(collections.Counter(q.get("designMethod") or "未標註"
                                        for q in group))

    has_method = any(q.get("designMethod") for q in prim)

    # ---- 標籤頻率（給「考點結構」分群當素材，不是最終分群）----
    tag_freq = collections.Counter(t for q in prim for t in (q.get("tags") or []))

    def row(q, is_primary):
        return {
            "moduleId": q["moduleId"],
            "year": year_of(q["moduleId"]),
            "rocYear": q.get("year"),
            "designMethod": q.get("designMethod"),
            "tags": q.get("tags") or [],
            "primaryTopicId": q.get("primaryTopicId"),
            "secondaryTopicIds": q.get("secondaryTopicIds") or [],
            "verificationStatus": q.get("verificationStatus"),
            "isPrimary": is_primary,
        }

    return {
        "unit": unit,
        "totals": {
            "subject_questions": len(questions),
            "primary": len(prim),
            "secondary": len(sec),
            "listed": len(prim) + len(sec),
            "share_pct": round(len(prim) / len(questions) * 100, 1) if questions else 0.0,
            "rank": rank,
            "rank_total_units": len(ordered),
            "rank_top3": top3,
            "rank_above": above,
            "rank_below": below,
        },
        "years": {
            "exam_years": all_years,
            "exam_year_count": len(all_years),
            "hit_years": hit_years,
            "hit_year_count": len(hit_years),
            "gaps": gaps,
            "recent6": recent(6),
            "recent10": recent(10),
        },
        "drift": {
            "early": {"span": span(early), "n": len(early),
                      "ids": [q["moduleId"] for q in early]},
            "late": {"span": span(late), "n": len(late),
                     "ids": [q["moduleId"] for q in late]},
            "note": "分群數由人判定；本檔只負責把題目對切，不猜分群",
        },
        "method": {
            "available": has_method,
            "all": methods(prim),
            "early": methods(early),
            "late": methods(late),
            "recent6": methods([q for q in prim
                                if year_of(q["moduleId"]) in all_years[-6:]]),
        },
        "tags_top": tag_freq.most_common(30),
        "questions": ([row(q, True) for q in prim] + [row(q, False) for q in sec]),
    }


def human(r, unit_name=""):
    t, y, m = r["totals"], r["years"], r["method"]
    L = []
    L.append(f"單元：{r['unit']} {unit_name}")
    L.append(f"主考點 {t['primary']} 題／副考點 {t['secondary']} 題／清單合計 {t['listed']} 題")
    L.append(f"佔全科 {t['share_pct']}%（{t['primary']}／{t['subject_questions']}）"
             f"，全科排名 #{t['rank']} / {t['rank_total_units']} 個單元")
    L.append("  排名前三：" + "、".join(f"{x['unit']} {x['count']}題" for x in t["rank_top3"]))
    if t["rank_above"]:
        L.append(f"  上一名：{t['rank_above']['unit']} {t['rank_above']['count']} 題")
    if t["rank_below"]:
        L.append(f"  下一名：{t['rank_below']['unit']} {t['rank_below']['count']} 題")
    L.append(f"考年總數 {y['exam_year_count']}，出現過 {y['hit_year_count']} 年")
    rc = y["recent6"]
    L.append(f"近 6 考年（{rc['span'][0]}–{rc['span'][1]}）："
             f"{rc['hit_years']}/6 年出題，共 {rc['questions']} 題   ← KPI 只能抄這個數字")
    L.append("空窗年段：" + (", ".join(f"{a}–{b}" for a, b in y["gaps"]) or "無"))
    d = r["drift"]
    L.append(f"對切：前段 {d['early']['span']} {d['early']['n']} 題 ／ "
             f"後段 {d['late']['span']} {d['late']['n']} 題")
    if m["available"]:
        L.append(f"設計法 全期：{m['all']}")
        L.append(f"設計法 前段：{m['early']}")
        L.append(f"設計法 後段：{m['late']}")
        L.append(f"設計法 近 6 考年：{m['recent6']}")
    else:
        L.append("設計法：本科未標註 designMethod → 改用其他軸線（題型／解法／單元內主題）")
    L.append("高頻標籤：" + "、".join(f"{k}×{v}" for k, v in r["tags_top"][:12]))
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("unit", help="單元代號，如 SS-U1-1")
    ap.add_argument("--index", default="raw/json/question_index.json")
    ap.add_argument("--taxonomy", default="raw/json/syllabus_taxonomy.json")
    ap.add_argument("--json", action="store_true", help="輸出 JSON 而非人可讀摘要")
    a = ap.parse_args()

    qs = load_index(a.index)
    r = analyse(qs, a.unit)
    if r["totals"]["primary"] == 0 and r["totals"]["secondary"] == 0:
        sys.exit(f"錯誤：{a.unit} 在 {a.index} 裡一題都沒有。"
                 f"確認單元代號與目前工作資料夾的科目是否相符。")

    if a.json:
        json.dump(r, sys.stdout, ensure_ascii=False, indent=1)
    else:
        print(human(r, load_taxonomy(a.taxonomy).get(a.unit, "")))


if __name__ == "__main__":
    main()
