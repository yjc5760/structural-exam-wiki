#!/usr/bin/env python3
"""RC-U1-1 題目正本批 1（2002–2015，9 題）關卡一確認後凍結。可重複執行（已確認者略過）。
用法（在 RC/ 或其上層執行皆可）：python RC/scripts/fixes/2026-11-12_confirm_sec1_RC-U1-1_B1.py [RC 資料夾]
動作：
  1. raw/solutions/<id>/<id>-problem.md：判讀狀態「待確認」→「已確認」；
     不確定項把握欄加「；使用者確認」；影響答案的三項寫明使用者選擇；頁尾加確認行
  2. raw/json/question_index.json：problemStatus draft → confirmed
（解析 §1 改寫、勘誤、重繪圖另以檔案直接寫入，見 wiki/queries/log.md 同日紀錄）"""
import re, sys, json, os
RC = sys.argv[1] if len(sys.argv) > 1 else (
    "RC" if os.path.isdir("RC/raw") else ".")
DATE = "2026-11-12"
IDS = "RC-2002-4 RC-2004-2 RC-2005-2 RC-2007-1 RC-2011-2 RC-2014-1 RC-2014-2 RC-2015-2 RC-2015-3".split()
CHOICE = {  # 影響答案項目：題號 → (判讀編號, 使用者選擇)
    "RC-2002-4": ("9", "使用者選擇：採淨拉應變體系，φ 依 εt 內插"),
    "RC-2005-2": ("3", "使用者選擇：採 εt ≥ 0.004 上限，並配 1.2D + 1.6L"),
    "RC-2011-2": ("5", "使用者選擇：採 h = 110、d = 100"),
}
HEAD_NOTE = {
    "RC-2002-4": "；影響答案項目 #9 使用者選 φ 依 εt（淨拉應變體系）",
    "RC-2005-2": "；影響答案項目 #3 使用者選 εt ≥ 0.004 上限＋1.2D + 1.6L",
    "RC-2011-2": "；#5 使用者確認 h = 110、d = 100（推翻 2026-08-21 解析定案）",
}
done = 0
for qid in IDS:
    p = os.path.join(RC, "raw", "solutions", qid, f"{qid}-problem.md")
    s = open(p, encoding="utf-8").read()
    if "| 判讀狀態 | **已確認**" in s:
        print(qid, "已確認，略過"); continue
    m = re.search(r"\| 判讀狀態 \| \*\*待確認\*\*（(轉錄 [^，]+)，", s)
    assert m, qid
    s = s.replace("| 判讀狀態 | **待確認**（", f"| 判讀狀態 | **已確認**（{DATE} 使用者確認{HEAD_NOTE.get(qid, '')}；", 1)
    s = s.replace("> 判讀清單經使用者確認前，狀態為「待確認」；確認後本檔原則上不再修改（改動須回考卷原圖並記 log）。",
                  "> 判讀清單已經使用者確認（凍結）；本檔原則上不再修改（改動須回考卷原圖並記 log）。", 1)
    if qid in CHOICE:
        no, txt = CHOICE[qid]
        pat = re.compile(r"(\n\| %s \|[^\n]*?)\| ([^|\n]*?) \|\n" % no)
        mm = pat.search(s); assert mm, (qid, no)
        s = s[:mm.start()] + mm.group(1) + f"| 確定（{txt}） |\n" + s[mm.end():]
    n0 = s.count("| 不確定（解讀） |")
    s = s.replace("| 不確定（解讀） |", "| 不確定（解讀）；使用者確認 |")
    assert "請確認" not in s, qid
    s = s.rstrip("\n") + f"\n\n*確認：{DATE} 使用者確認（RC-U1-1 題目正本推廣・批 1，關卡一）*\n"
    open(p, "w", encoding="utf-8").write(s)
    done += 1
    print(qid, "已確認", f"（不確定項 {n0}）")
ip = os.path.join(RC, "raw", "json", "question_index.json")
t = open(ip, encoding="utf-8").read()
for qid in IDS:
    pat = re.compile(r'("moduleId": "%s",.*?"problemStatus": ")draft(")' % re.escape(qid), re.S)
    t, n = pat.subn(r"\1confirmed\2", t, count=1)
    assert n == 1 or re.search(r'"moduleId": "%s",.*?"problemStatus": "confirmed"' % re.escape(qid), t, re.S), qid
q = json.loads(t)
assert sum(1 for x in q["questions"] if x["moduleId"] in IDS and x.get("problemStatus") == "confirmed") == len(IDS)
open(ip, "w", encoding="utf-8", newline="").write(t)
print("problem.md 本次確認", done, "題；索引 confirmed", len(IDS), "題")
