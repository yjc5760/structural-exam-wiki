#!/usr/bin/env python3
"""RC-U3-3 批 1（2003–2012，10 題）關卡一確認：題目正本凍結、索引 problemStatus／tags 同步。
用法：在 RC/ 底下執行  python scripts/fixes/2026-11-14_confirm_sec1_RC-U3-3_B1.py
可重複執行（已處理過的題目略過）；每一步 assert。
解析 .md 的 §1 改寫與勘誤由同批另行寫入（見 wiki/queries/log.md PROBLEM-SPLIT-CONFIRM-RC-U3-3-B1）。"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # RC/
DATE = "2026-11-14"
IDS = "RC-2003-3 RC-2003-4 RC-2004-1 RC-2004-3 RC-2005-3 RC-2009-1 RC-2010-2 RC-2012-2 RC-2012-3 RC-2012-4".split()
CHOICE = {
    "RC-2003-3": "影響答案項目使用者選擇：#1 柱 X 向 40／Y 向 50、#2 X 向梁上緣與柱面齊平（偏心）",
    "RC-2003-4": "影響答案項目使用者選擇：#1 900 為邊界構材中心距（l_w＝930）、#4 層高 350＋450、#6 兩端各一 P（50 靜＋25 活）；腹版厚 15、屋頂 w 一併採用",
}
TAGS = {
    "RC-2003-3": ["偏心梁", "1.25fy", "一雙對面圍束", "柱方向判讀"],
    "RC-2003-4": ["尺寸鏈判讀", "邊界構材中心距", "腹版厚15", "層高350+450"],
    "RC-2012-3": ["bc量至箍筋外緣", "6db控制"],
    "RC-2012-4": ["bc量至箍筋外緣"],
}

done = 0
for q in IDS:
    p = ROOT / f"raw/solutions/{q}/{q}-problem.md"
    s = p.read_text(encoding="utf-8")
    if "判讀狀態 | **已確認**" in s:
        print(q, "已確認，略過"); continue
    old = re.search(r"\| 判讀狀態 \| \*\*待確認\*\*（轉錄 2026-11-14；", s)
    assert old, q
    extra = f"；{CHOICE[q]}" if q in CHOICE else ""
    s = s.replace("| 判讀狀態 | **待確認**（轉錄 2026-11-14；",
                  f"| 判讀狀態 | **已確認**（{DATE} 使用者確認{extra}；轉錄 2026-11-14；", 1)
    s = s.replace("> 判讀清單經使用者確認前，狀態為「待確認」；確認後本檔原則上不再修改（改動須回考卷原圖並記 log）。",
                  "> 判讀清單已經使用者確認（凍結）；本檔原則上不再修改（改動須回考卷原圖並記 log）。", 1)
    n = s.count("（影響答案，請確認）")
    s = s.replace("（影響答案，請確認）", "（影響答案）；使用者確認")
    assert "待確認" not in s.split("## 4.")[0] or q == "", q
    s = s.rstrip() + f"\n\n*確認：{DATE} 使用者確認（RC-U3-3 題目正本推廣・批 1，關卡一）*\n"
    p.write_text(s, encoding="utf-8")
    print(q, f"已確認（影響答案項 {n}）"); done += 1

ip = ROOT / "raw/json/question_index.json"
t = ip.read_text(encoding="utf-8")
for q in IDS:
    m = re.search(r'"moduleId":\s*"%s"' % q, t); assert m, q
    end = t.find("}", m.start())
    blk = t[m.start():end]
    if '"problemStatus": "draft"' in blk:
        t = t[:m.start()] + blk.replace('"problemStatus": "draft"', '"problemStatus": "confirmed"', 1) + t[end:]
    else:
        assert '"problemStatus": "confirmed"' in blk, q
idx = json.loads(t)
Q = idx["questions"] if isinstance(idx, dict) else idx
for x in Q:
    q = x.get("moduleId")
    if q in IDS:
        assert x.get("problemStatus") == "confirmed", q
        assert x.get("verificationStatus") != "verified", q
for q, new in TAGS.items():
    m = re.search(r'"moduleId":\s*"%s"' % q, t)
    tm = re.search(r'"tags":\s*\[(.*?)\]', t[m.start():], re.S)
    a, b = m.start() + tm.start(1), m.start() + tm.end(1)
    cur = t[a:b]
    have = json.loads("[" + cur + "]")
    add = [g for g in new if g not in have]
    if add:
        sep = cur.rstrip()
        ins = (", " if sep.strip() else "") + ", ".join(json.dumps(g, ensure_ascii=False) for g in add)
        t = t[:a] + sep + ins + t[a + len(sep):]
json.loads(t)
ip.write_text(t, encoding="utf-8", newline="")
print("索引：10 題 confirmed；tags 已補", done)
