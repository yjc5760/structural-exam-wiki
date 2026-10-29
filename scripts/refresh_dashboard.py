#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refresh_dashboard.py — REFRESH-DASHBOARD（「更新儀表板資料」）的通用實作

從 XX/raw/json/question_index.json 重新產生 XX/dashboard-data.js，供 XX/index.html 讀取。
五科共用同一份 index.html 樣板（scripts/templates/dashboard-index.html），科目差異全部放在
dashboard-data.js 的 window.KB_SUBJECT。

用法（在知識庫根目錄執行）：
    python scripts/refresh_dashboard.py SS          # 單科
    python scripts/refresh_dashboard.py --all       # 所有已建立的科目資料夾
    python scripts/refresh_dashboard.py SS --check  # 只印摘要，不寫檔

資料列格式（與舊版 SS_QUESTIONS 相同，index.html 依位置讀取）：
    [moduleId, 主考點(去掉本科前綴), [副考點...], designMethod, [viz 內容碼...], [tags...], [補充 PDF 檔名...]]
"""
import argparse, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAXONOMY = os.path.join(ROOT, "syllabus_taxonomy.json")
PROFILES = os.path.join(ROOT, "scripts", "subject_profiles.json")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def strip(code, subj):
    return code[len(subj) + 1:] if code.startswith(subj + "-") else code


def build(subj, check=False):
    tax = load(TAXONOMY)
    prof = load(PROFILES)["subjects"].get(subj)
    if prof is None:
        sys.exit(f"錯誤：scripts/subject_profiles.json 沒有科目 {subj}")
    sdir = os.path.join(ROOT, subj)
    qi = load(os.path.join(sdir, "raw", "json", "question_index.json"))
    qs = qi["questions"] if isinstance(qi, dict) else qi
    subjects = {s["id"]: s for s in tax["subjects"]}
    me = subjects[subj]

    rows, used = [], {subj}
    for q in qs:
        mid = q["moduleId"]
        sec = q.get("secondaryTopicIds") or []
        for t in [q.get("primaryTopicId", "")] + sec:
            used.add(t.split("-")[0])
        folder = os.path.join(sdir, "raw", "solutions", mid)
        viz, pdf = [], []
        if os.path.isdir(folder):
            for f in sorted(os.listdir(folder)):
                m = re.match(re.escape(mid) + r"-(.+)-viz\.html$", f)
                if m:
                    viz.append(m.group(1))
                elif f.lower().endswith(".pdf"):
                    pdf.append(f)
        rows.append([mid, strip(q.get("primaryTopicId", ""), subj), [strip(s, subj) for s in sec],
                     q.get("designMethod", ""), viz, q.get("tags", []), pdf])
    for t in prof.get("relatedTopics", []):
        used.add(t.split("-")[0])

    units, topics = {}, {}
    for sid in [subj] + sorted(u for u in used if u != subj and u in subjects):
        for u in subjects[sid]["units"]:
            units[strip(u["id"], subj)] = u["name"] if sid == subj else f'{sid} {subjects[sid]["name"]}｜{u["name"]}'
            for it in u["items"]:
                topics[strip(it["id"], subj)] = it["name"]

    years = sorted({int(r[0].split("-")[1]) for r in rows})
    meta = {
        "code": subj,
        "name": me["name"],
        "nameEn": me.get("nameEn", ""),
        "examFile": prof["examFile"],
        "methodAxis": prof["methodAxis"],
        "methods": prof["methods"],
        "viz": prof.get("viz", {}),
        "layers": {k: v["title"] for k, v in prof["layers"].items()},
        "unitOrder": [strip(u["id"], subj) for u in me["units"]],
    }
    print(f"[{subj}] {me['name']}：{len(rows)} 題"
          + (f"（{years[0]}–{years[-1]}，{len(years)} 考年）" if years else "（尚未收錄題目）")
          + f"；有互動圖 {sum(1 for r in rows if r[4])} 題；有補充 PDF {sum(1 for r in rows if r[6])} 題")
    bad = [r[0] for r in rows if r[1] not in topics]
    if bad:
        print(f"  ⚠️ 主考點不在 taxonomy：{bad}")
    if check:
        return
    dump = lambda o: json.dumps(o, ensure_ascii=False, indent=2)
    js = ("// 自動生成：請勿手動修改\n"
          "// 生成指令：REFRESH-DASHBOARD（更新儀表板資料）→ python scripts/refresh_dashboard.py " + subj + "\n\n"
          f"window.KB_SUBJECT = {dump(meta)};\n\n"
          f"window.KB_UNITS = {dump(units)};\n\n"
          f"window.KB_TOPICS = {dump(topics)};\n\n"
          f"window.KB_QUESTIONS = {json.dumps(rows, ensure_ascii=False)};\n")
    with open(os.path.join(sdir, "dashboard-data.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write(js)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subject", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    subs = list(load(PROFILES)["subjects"]) if a.all else [a.subject]
    if not subs or subs == [None]:
        ap.error("請指定科目代碼或 --all")
    for s in subs:
        if os.path.isfile(os.path.join(ROOT, s, "raw", "json", "question_index.json")):
            build(s, a.check)
        elif not a.all:
            sys.exit(f"錯誤：找不到 {s}/raw/json/question_index.json")


if __name__ == "__main__":
    main()
