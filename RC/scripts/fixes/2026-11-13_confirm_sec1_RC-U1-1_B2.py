#!/usr/bin/env python3
"""RC-U1-1 題目正本批 2（2016–2024，10 題）關卡一確認後凍結。可重複執行（已確認者略過）。
用法（在 RC/ 或其上層執行皆可）：python RC/scripts/fixes/2026-11-13_confirm_sec1_RC-U1-1_B2.py [RC 資料夾]
動作：
  1. raw/solutions/<id>/<id>-problem.md：判讀狀態「待確認」→「已確認」；
     影響答案項目寫明使用者選擇；其餘不確定（解讀）項加「；使用者確認」；頁尾加確認行
  2. raw/json/question_index.json：problemStatus draft → confirmed
（解析勘誤、§1 改寫、重繪圖另以檔案直接寫入，見 wiki/queries/log.md 同日紀錄）"""
import re, sys, json, os
RC = sys.argv[1] if len(sys.argv) > 1 else (
    "RC" if os.path.isdir("RC/raw") else ".")
DATE = "2026-11-13"
IDS = ("RC-2016-1 RC-2019-1 RC-2020-1 RC-2021-1 RC-2022-1 "
       "RC-2022-2 RC-2023-1 RC-2023-2 RC-2024-1 RC-2024-2").split()
CHOICE = {  # 題號 → [(判讀編號, 新把握欄)]
    "RC-2020-1": [("1", "確定（使用者選擇：70 為版頂到梁腹底，h = 70、d = 64）")],
    "RC-2023-1": [("1", "確定（使用者選擇：假設 fy = 4200 kgf/cm²）")],
    "RC-2023-2": [("1", "確定（使用者選擇：照原卷 4+4 兩排；間距不合規範於解析註明）"),
                  ("2", "確定（使用者選擇：d' = 6 cm）")],
    "RC-2024-1": [("2", "確定（使用者選擇：d = 80）")],
    "RC-2024-2": [("1", "確定（使用者選擇：44 cm 為兩排鋼筋中心距）"),
                  ("3", "確定（使用者選擇：d = 52、d' = 8）"),
                  ("9", "不確定（解讀）；使用者確認：Mn 與 φMn 並列作答")],
}
HEAD_NOTE = {
    "RC-2020-1": "；#1 使用者確認 h = 70、d = 64（推翻解析 h = 80、d = 74）",
    "RC-2023-1": "；#1 使用者選 fy = 4200 假設",
    "RC-2023-2": "；#1 使用者選 4+4 兩排、#2 d' = 6 cm",
    "RC-2024-1": "；#2 使用者確認 d = 80（推翻解析假設 d = 74）",
    "RC-2024-2": "；#1、#3 使用者確認 d = 52（推翻解析 d = 44）",
}
done = 0
for qid in IDS:
    p = os.path.join(RC, "raw", "solutions", qid, f"{qid}-problem.md")
    s = open(p, encoding="utf-8").read()
    if "| 判讀狀態 | **已確認**" in s:
        print(qid, "已確認，略過"); continue
    assert "| 判讀狀態 | **待確認**（轉錄 " in s, qid
    s = s.replace("| 判讀狀態 | **待確認**（", f"| 判讀狀態 | **已確認**（{DATE} 使用者確認{HEAD_NOTE.get(qid, '')}；", 1)
    old = "> 判讀清單經使用者確認前，狀態為「待確認」；確認後本檔原則上不再修改（改動須回考卷原圖並記 log）。"
    assert old in s, qid
    s = s.replace(old, "> 判讀清單已經使用者確認（凍結）；本檔原則上不再修改（改動須回考卷原圖並記 log）。", 1)
    for no, txt in CHOICE.get(qid, []):
        pat = re.compile(r"(\n\| %s \|[^\n]*?)\| ([^|\n]*?) \|\n" % no)
        mm = pat.search(s); assert mm, (qid, no)
        s = s[:mm.start()] + mm.group(1) + f"| {txt} |\n" + s[mm.end():]
    n0 = s.count("| 不確定（解讀） |")
    s = s.replace("| 不確定（解讀） |", "| 不確定（解讀）；使用者確認 |")
    assert "請確認" not in s, qid
    s = s.rstrip("\n") + f"\n\n*確認：{DATE} 使用者確認（RC-U1-1 題目正本推廣・批 2，關卡一）*\n"
    open(p, "w", encoding="utf-8").write(s)
    done += 1
    print(qid, "已確認", f"（其餘不確定項 {n0}）")
ip = os.path.join(RC, "raw", "json", "question_index.json")
t = open(ip, encoding="utf-8").read()
for qid in IDS:
    pat = re.compile(r'("moduleId": "%s",[^{}]*?"problemStatus": ")draft(")' % re.escape(qid), re.S)
    t, n = pat.subn(r"\1confirmed\2", t, count=1)
    assert n == 1 or re.search(r'"moduleId": "%s",[^{}]*?"problemStatus": "confirmed"' % re.escape(qid), t, re.S), qid
q = json.loads(t)
assert sum(1 for x in q["questions"] if x["moduleId"] in IDS and x.get("problemStatus") == "confirmed") == len(IDS)
open(ip, "w", encoding="utf-8", newline="").write(t)
print("problem.md 本次確認", done, "題；索引 confirmed", len(IDS), "題")
