#!/usr/bin/env python3
"""SD-U2-2 組 U2-2-G4（SD-2020-4、2024-3、2025-1）關卡一確認後：解析 §1 改為指向題目正本。
problem.md 建立時已直接寫為「已確認」（2026-11-16 使用者授權依 Claude 建議），本腳本只檢查不改。
可重複執行（已處理者略過）。用法：python3 <本檔> <SD 科目資料夾>
不改 question_index.json、log.md（由總控統一處理）。只動 §1，其他節不動；解析答案不改。"""
import sys, re, os
from pathlib import Path
SD = Path(sys.argv[1]); D = "2026-11-16"
IDS = ["SD-2020-4", "SD-2024-3", "SD-2025-1"]
REDRAW = {"SD-2025-1"}
FIGCAP = {
 "SD-2025-1": ("兩柱單跨八層平面構架，柱底固定，各層高 3.5 m、H＝28 m；m1～m8 在各樓版，F1～F8 作用於各樓版向右，屋頂另有 Ft；基底 V0 向左、M0 逆時針（反力方向）",
               "屋頂 Ft 與 F8 是兩個力（Ft 另外加在頂層）；m_i 在第 i 層樓版；H 由柱底 0 量到第 8 層"),
}
SEC1 = {
 "SD-2020-4": ("""| 題型 | 純論述題，考卷給三條一般工址總橫力公式，沒有任何數值（判讀 #9） | 自行假設數值當題目條件 |
| 最大考量地震分母 | 考卷 $V_M$ 分母為 $1.4\\alpha_y$（判讀 #4）；2024 年同型題（SD-2024-3）考卷也是 $1.4\\alpha_y$ | 本庫舊 §1 註記稱 SD-2024-3 考卷寫 $1.4\\alpha_{yM}$——經考卷 400 dpi 核對，2024 年卷同樣是 $1.4\\alpha_y$；本解 §4 比較 $V_M/V$ 時令 $\\alpha_{yM}=\\alpha_y$，結果等同直接用考卷式 |
| 「50 年設計年限」與「年超越機率」 | 兩者並列作答：50 年超越機率與對應回歸期（年超越機率＝1／回歸期）（判讀 #1） | 只寫 50 年機率或只寫年機率 |
| 適用範圍 | 規則性、不須動力分析的建築物，一般工址（判讀 #6） | 套用臺北盆地 $3.5\\alpha_y$ |
| 規範版本 | 現行建築物耐震設計規範（111 年版）；考卷三式與現行一般工址公式形式相同（判讀 #2） | — |""",
  "$V$、$V^*$、$V_M$ 為設計地震、中小度地震、最大考量地震水平總橫力；$(\\cdot)_m$ 為規範修正係數；$F_u$、$F_{uM}$ 為對應的結構系統地震力折減係數。"),
 "SD-2024-3": ("""| $V^*$ 兩式的適用條件 | 考卷大括號旁沒有寫條件；依現行規範 $4.2\\alpha_y$＝一般工址（含近斷層）、$3.5\\alpha_y$＝臺北盆地（判讀 #1，使用者授權依建議確認）。本解 §4（二）把兩式寫成短週期／長週期並「取較小者」，與現行規範不符，待階段 C 勘誤 | 解讀成短週期區／長週期區，或兩式取小 |
| 最大考量地震分母 | 考卷 $V_M$ 分母為 $1.4\\alpha_y$（判讀 #4） | 本庫舊 §1 寫成 $1.4\\alpha_{yM}$（考卷沒有 $\\alpha_{yM}$） |
| 「最小設計水平總橫力」 | 指設計地震公式 $V$（判讀 #2） | 當成另一條最小值檢核式 |
| ㈡「分母為何又不同」 | 涵蓋 $4.2$ 與 $3.5$ 之間、以及相對 $V$ 的 $1.4$ 的差異（判讀 #7） | 只答其中一項 |
| 題型 | 純論述題，無附圖、無數值（判讀 #10）；同頁簡支梁圖屬第四題 | 把第四題的圖當本題附圖 |""",
  "$V$、$V^*$、$V_M$ 為設計地震、中小度地震、最大考量地震設計地震力；$(\\cdot)_m$ 為規範修正係數；建築 $1.4\\alpha_y$、橋梁 $1.2\\alpha_y$。"),
 "SD-2025-1": ("""| 頂層集中力 | 屋頂另畫 $F_t$；$T=0.8\\ \\mathrm{s}>0.7\\ \\mathrm{s}$，依現行規範 $F_t=0.07TV\\le0.25V$，其餘 $V-F_t$ 依 $w_ih_i$ 分配（判讀 #1，使用者授權依建議確認） | 忘記 $F_t$，或把 $F_t$ 也放進 $\\sum w_ih_i$ 一起分配 |
| 考卷公式 | 考卷式沒有 $(\\cdot)_m$；本題 $S_{aD}/F_u=0.3$，現行規範修正係數不改值，結果相同（判讀 #2） | — |
| 樓層質量與高度 | $w_i=20$ kN 在第 $i$ 層樓版，$h_i=3.5i$ m，$h_8=H=28$ m（判讀 #4、#5） | 把 $m_1$ 標籤位置讀成柱底 |
| 週期 | 直接給 $T=0.8$ s（判讀 #9） | 再用規範經驗式算 $T$ |
| 最小總橫力檢核 | 考卷沒有給 $S_{aM}$、$F_{uM}$，只依所給公式求 $V$（判讀 #3） | 自行補 $V^*$、$V_M$ 檢核當題目要求 |""",
  "$V_0$ 基底總剪力（＝$V$）；$F_t$ 頂層集中力；$F_i=(V-F_t)\\,w_ih_i/\\sum w_jh_j$；$M_0$ 基底總彎矩（傾覆彎矩）。"),
}
SEC1_PAT = r"^## 1\. 原始題目重述.*?(?=^---\s*\n\s*## 2\.|^## 2\.)"
def check_problem(qid):
    t = (SD/f"raw/solutions/{qid}/{qid}-problem.md").read_text(encoding="utf-8")
    assert "判讀狀態 | **已確認**（2026-11-16" in t, qid
def rewrite_sec1(qid):
    p = SD/f"raw/solutions/{qid}/{qid}.md"; t = p.read_text(encoding="utf-8")
    if "## 1. 題目（考卷原文見題目正本）" in t: return False
    m = re.search(SEC1_PAT, t, re.S | re.M); assert m, qid
    old = m.group(0)
    prob = (SD/f"raw/solutions/{qid}/{qid}-problem.md").read_text(encoding="utf-8")
    for png in re.findall(r"\(([^)]*?\.png)\)", old):
        if os.path.exists(SD/f"raw/solutions/{qid}/{png}"): assert png in prob, (qid, png)
    assert not re.findall(r"\((figs/[^)]*?\.svg)\)", old), qid   # 本組舊 §1 無自繪圖
    rows, note = SEC1[qid]
    s = ["## 1. 題目（考卷原文見題目正本）", "",
         f"> 考卷原文、公式／附表、附圖與判讀清單（已確認）見 [`{qid}-problem.md`]({qid}-problem.md)。本節只列解題時最容易讀錯的地方與本解使用的記號；題意以題目正本為準。", ""]
    if qid in REDRAW:
        assert (SD/f"raw/solutions/{qid}/figs/{qid}-fig-1-problem.svg").exists()
        alt, cap = FIGCAP[qid]
        s += [f"![{qid} 重繪題目附圖：{alt}](figs/{qid}-fig-1-problem.svg)", f"*重繪自考卷附圖，依題目正本判讀清單；本圖攔下的判讀錯誤：{cap}。*", ""]
    s += ["### 常見誤讀", "", "| 項目 | 正確判讀 | 常見誤讀 |", "|------|---------|---------|", rows, "", f"**本解記號：** {note}", "", ""]
    new = "\n".join(s)
    t = t.replace(old, new, 1)
    extra = f"，重繪附圖 figs/{qid}-fig-1-problem.svg" if qid in REDRAW else ""
    t = t.rstrip("\n") + f"\n\n*修正日期：{D}（§1 改為指向題目正本{extra}）*\n"
    p.write_text(t, encoding="utf-8"); return True
if __name__ == "__main__":
    for q in IDS:
        check_problem(q); print(q, "sec1", rewrite_sec1(q))
