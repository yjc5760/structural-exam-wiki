#!/usr/bin/env python3
"""RC-U1-2 批 1 關卡一確認：題目正本凍結（待確認 → 已確認）、索引 draft → confirmed。
可重複執行：已確認者略過。在 RC/ 資料夾執行：python scripts/fixes/2026-11-14_confirm_sec1_RC-U1-2_B1.py
（重繪附圖、§1 改寫、勘誤為後續步驟，另寫腳本／另記 log。）"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # RC/
DATE = "2026-11-14"
CHOICES = {
    "RC-2002-2": "影響答案項目使用者選擇：#3 6-#9 為左右兩縱列各 3 根（沿彎曲深度兩層，7／33 cm）",
    "RC-2005-1": "影響答案項目使用者選擇：#3、#4 沿 60 cm 方向彎曲，三層 3／2／3 根在 7／30／53 cm；不確定項照草稿判讀定案",
    "RC-2008-2": "影響答案項目使用者選擇：#1 彎矩對幾何形心（圖上 Y 軸）取矩",
    "RC-2010-1": "不確定項照草稿判讀定案（#1 螺距須自行假設；#2 採讀法①）",
    "RC-2011-1": "無不確定項",
    "RC-2011-3": "影響答案項目使用者選擇：#1 讀法②（作用標稱軸力 Pn＝0.9Pb）；#4 6-#10 為左右兩排各 3 根（d'＝6、d＝54 cm，無中排）；#2 照草稿判讀定案",
    "RC-2015-1": "不確定項照草稿判讀定案（#1 最大設計彎矩 φMn）",
    "RC-2017-1": "影響答案項目使用者選擇：#1 擴柱後共 16 根（原 8＋新 8）；#2 保護層 6.5 cm 量至鋼筋中心；#3 原柱鋼筋位置須自行假設",
    "RC-2019-2": "無不確定項",
    "RC-2021-2": "無不確定項",
    "RC-2024-3": "無不確定項",
}
OLD_NOTE = "> 判讀清單經使用者確認前，狀態為「待確認」；確認後本檔原則上不再修改（改動須回考卷原圖並記 log）。"
NEW_NOTE = "> 判讀清單已經使用者確認（凍結）；本檔原則上不再修改（改動須回考卷原圖並記 log）。"
FOOT = f"\n*確認：{DATE} 使用者確認（RC-U1-2 題目正本推廣・批 1，關卡一）*\n"

done = 0
for qid, choice in CHOICES.items():
    p = ROOT / f"raw/solutions/{qid}/{qid}-problem.md"
    s = p.read_text(encoding="utf-8")
    if "| 判讀狀態 | **已確認**" in s:
        print(qid, "已確認，略過"); continue
    assert "| 判讀狀態 | **待確認**（" in s, qid
    s = s.replace("| 判讀狀態 | **待確認**（", f"| 判讀狀態 | **已確認**（{DATE} 使用者確認；{choice}；", 1)
    if OLD_NOTE in s:
        s = s.replace(OLD_NOTE, NEW_NOTE, 1)
    head, sep, tail = s.partition("## 4. 判讀清單")
    assert sep, qid
    lines = tail.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("| ") and not ln.startswith("| #") and not ln.startswith("|---"):
            cells = ln.rstrip().rstrip("|").rsplit("|", 1)
            if "不確定" in cells[-1] and "使用者確認" not in cells[-1]:
                lines[i] = cells[0] + "|" + cells[-1].rstrip() + "；使用者確認 |"
    s = head + sep + "\n".join(lines)
    s = s.rstrip("\n") + "\n" + FOOT
    p.write_text(s, encoding="utf-8")
    done += 1
    print(qid, "→ 已確認")

ip = ROOT / "raw/json/question_index.json"
t = ip.read_text(encoding="utf-8")
for qid in CHOICES:
    m = re.search(r'"moduleId":\s*"%s"' % qid, t); assert m, qid
    end = t.find("\n    }", m.end())
    blk = t[m.start():end]
    assert '"problemStatus"' in blk, qid
    t = t[:m.start()] + blk.replace('"problemStatus": "draft"', '"problemStatus": "confirmed"', 1) + t[end:]
d = json.loads(t)
Q = d["questions"] if isinstance(d, dict) else d
assert all(x.get("problemStatus") == "confirmed" for x in Q if x["moduleId"] in CHOICES)
ip.write_text(t, encoding="utf-8")
print("problem.md 確認", done, "題；索引 confirmed", len(CHOICES), "題")
