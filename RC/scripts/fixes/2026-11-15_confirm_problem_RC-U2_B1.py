#!/usr/bin/env python3
"""RC-U2-1＋U2-2 批 1 關卡一：題目正本「待確認」→「已確認」，索引 draft → confirmed（可重複執行）
使用者 2026-11-15 確認（AskUserQuestion）。RC-2023-3 #1 於同日第二次詢問確認。
執行：cd RC && python scripts/fixes/2026-11-15_confirm_problem_RC-U2_B1.py"""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parents[2]
D = "2026-11-15"
CHOICE = {
 "RC-2006-1": "#1 45 cm 為有效深度 d",
 "RC-2009-3": "#8 不視為指定 ACI，依現行台灣規範解題（ACI 僅為腹筋條件）",
 "RC-2010-3": "", "RC-2014-3": "#1 均佈設計載重讀為 5 tf/m",
 "RC-2017-2": "#1 #2 沿用 RC-2017-1 已確認判讀",
 "RC-2020-2": "#3 h＝70（全高）、d＝64；#1 載重作用於翼版頂面",
 "RC-2002-3": "", "RC-2008-3": "", "RC-2011-4": "",
 "RC-2013-3": "#1 20×40 量到箍筋外緣（中心線 19.04×39.04）",
 "RC-2018-1": "#1 抗剪計 4 肢、抗扭只計外圍閉合箍；#2 #3 h＝50、d＝43",
 "RC-2025-3": "",
 "RC-2023-3": "#1 最大設計剪力 Vu＝臨界斷面（距固定端 d）由 Wu 產生的 Vu",
}
EXTRA = {  # 判讀文字定案（old, new）
 "RC-2009-3": [("是否視為本題「指定 ACI」而依 ACI 的壓拉桿條文解題（本庫規則：題目明確指定 ACI 才例外），請確認",
                "使用者定案：**不視為指定 ACI**，依現行台灣規範的壓拉桿條文解題；ACI 僅為腹筋條件")],
 "RC-2013-3": [("圖面線寬難以完全排除「量到箍筋中心線」的畫法", "使用者定案：量到**箍筋外緣**，中心線尺寸 19.04×39.04 cm")],
 "RC-2018-1": [("抗剪可計 4 肢；抗扭的閉合箍筋只有外圍一圈（$A_t$＝1 支）", "使用者定案：抗剪計 4 肢；抗扭只計外圍閉合箍（$A_t$＝1 支）")],
 "RC-2023-3": [("另一讀法為「斷面所能承受的最大剪力」（剪力上限 $\\phi V_n$）","使用者定案：臨界斷面由 $W_u$ 產生的 $V_u$（不採「斷面剪力強度上限」讀法）")],
 "RC-2014-3": [("另一讀法為全跨合計 5 tf（1 tf/m）", "使用者定案：5 tf/m（另一讀法全跨合計 5 tf 不採用）")],
}
qp = R / "raw/json/question_index.json"; qt = qp.read_text(encoding="utf-8")
for qid, ch in CHOICE.items():
    p = R / f"raw/solutions/{qid}/{qid}-problem.md"; t = p.read_text(encoding="utf-8")
    if "**已確認**" not in t:
        for o, n in EXTRA.get(qid, []):
            assert o in t, (qid, o); t = t.replace(o, n)
        sel = f"影響答案項目使用者選擇：{ch}；" if ch else ""
        assert "| 判讀狀態 | **待確認**（" in t, qid
        t = t.replace("| 判讀狀態 | **待確認**（", f"| 判讀狀態 | **已確認**（{D} 使用者確認；{sel}", 1)
        t = t.replace("判讀清單經使用者確認前，狀態為「待確認」；確認後本檔原則上不再修改",
                      "判讀清單已經使用者確認（凍結）；本檔原則上不再修改")
        # 不確定／影響答案項：把握欄加「；使用者確認」
        t = re.sub(r"\| (不確定（解讀）（影響答案，請確認）|確定（解讀）（影響答案）) \|",
                   lambda m: "| " + m.group(1).replace("，請確認", "") + "；使用者確認 |", t)
        t = t.rstrip("\n") + f"\n\n*確認：{D} 使用者確認（RC-U2-1／U2-2 題目正本推廣・批 1，關卡一）*\n"
        p.write_text(t, encoding="utf-8")
    m = re.search(r'"moduleId":\s*"%s"' % qid, qt); nxt = qt.find('"moduleId"', m.end())
    seg = qt[m.start():nxt if nxt > 0 else len(qt)]
    seg2 = seg.replace('"problemStatus": "draft"', '"problemStatus": "confirmed"')
    assert '"problemStatus": "confirmed"' in seg2, qid
    qt = qt.replace(seg, seg2, 1)
json.loads(qt); qp.write_text(qt, encoding="utf-8")
print("done", len(CHOICE))
