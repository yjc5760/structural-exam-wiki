#!/usr/bin/env python3
"""RC-U4-1 批 1（2003–2023，13 題）關卡一確認：題目正本凍結、索引 problemStatus／tags 同步。
用法：在 RC/ 底下執行  python scripts/fixes/2026-11-14_confirm_sec1_RC-U4-1_B1.py
可重複執行（已處理過的題目略過）；每一步 assert。
解析 .md 的 §1 改寫與勘誤由同批另行寫入（見 wiki/queries/log.md PROBLEM-SPLIT-CONFIRM-RC-U4-1-B1）。"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # RC/
DATE = "2026-11-14"
IDS = ("RC-2003-1 RC-2004-5 RC-2006-4 RC-2007-4 RC-2008-4 RC-2009-4 RC-2011-5 "
       "RC-2012-1 RC-2013-4 RC-2014-4 RC-2018-4 RC-2021-4 RC-2023-4").split()
CHOICE = {
    "RC-2006-4": "影響答案項目使用者選擇：#2 梁中心距 100 cm（解析原用 200 cm，另行勘誤）",
    "RC-2007-4": "影響答案項目使用者選擇：#1 斷面性質照考卷數據，版置於 c_t＋c_b＝114.3 cm 頂面（與圖上總高 112.5 的矛盾於解析 §5 註明）；#7 澆版無支撐（版重由梁單獨承受）",
    "RC-2014-4": "影響答案項目使用者選擇：#1 S 依 I_c/c 修正為 1.563×10⁴ cm³；#4 工作載重 1.1 tf/m 為自重以外的外加載重（合計 1.364 tf/m）",
    "RC-2021-4": "影響答案項目使用者選擇：#7 讀法①——預力與全部載重皆以合成斷面計算",
    "RC-2023-4": "影響答案項目使用者選擇：#1 普通鋼筋取規範無握裹預力版最少握裹鋼筋量 0.004A_ct",
}
TAGS = {
    "RC-2006-4": ["梁距100cm", "尺寸線判讀"],
    "RC-2007-4": ["斷面數據矛盾"],
    "RC-2014-4": ["S指數筆誤"],
    "RC-2023-4": ["普通鋼筋量未給"],
}
UNC = re.compile(r"不確定（影響答案，請確認[^|]*?） \|")

done = 0
for q in IDS:
    p = ROOT / f"raw/solutions/{q}/{q}-problem.md"
    s = p.read_text(encoding="utf-8")
    if "判讀狀態 | **已確認**" in s:
        print(q, "已確認，略過"); continue
    assert "| 判讀狀態 | **待確認**（轉錄 2026-11-14；" in s, q
    extra = f"；{CHOICE[q]}" if q in CHOICE else ""
    s = s.replace("| 判讀狀態 | **待確認**（轉錄 2026-11-14；",
                  f"| 判讀狀態 | **已確認**（{DATE} 使用者確認{extra}；轉錄 2026-11-14；", 1)
    old_head = "> 判讀清單經使用者確認前，狀態為「待確認」；確認後本檔原則上不再修改（改動須回考卷原圖並記 log）。"
    assert old_head in s, q
    s = s.replace(old_head, "> 判讀清單已經使用者確認（凍結）；本檔原則上不再修改（改動須回考卷原圖並記 log）。", 1)
    n = len(UNC.findall(s))
    s = UNC.sub("不確定（影響答案）；使用者確認（選擇見頭表判讀狀態） |", s)
    assert "請確認" not in s, q
    assert "待確認" not in s, q
    s = s.rstrip() + f"\n\n*確認：{DATE} 使用者確認（RC-U4-1 題目正本推廣・批 1，關卡一）*\n"
    p.write_text(s, encoding="utf-8", newline="")
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
idx = json.loads(t)
Q = idx["questions"] if isinstance(idx, dict) else idx
for x in Q:
    if x.get("moduleId") in IDS:
        assert x.get("problemStatus") == "confirmed", x["moduleId"]
        assert x.get("verificationStatus") != "verified", x["moduleId"]
ip.write_text(t, encoding="utf-8", newline="")
print(f"索引：{len(IDS)} 題 confirmed；tags 已補；本次確認 {done} 題")
