#!/usr/bin/env python3
"""SD-U1-3 批 3 G4（SD-2023-2、2024-1、2025-2、2025-3）關卡一確認後：problem.md 凍結、解析 §1 改為指向題目正本。
可重複執行（已處理者略過）。用法：python3 <本檔> <SD 科目資料夾>
不改 question_index.json（problemStatus 由批次主流程統一寫入）。
2026-11-15 使用者授權依 Claude 建議確認（pipeline 一次做完，關卡一不停）。"""
import sys, re, os
from pathlib import Path
SD = Path(sys.argv[1]); D = "2026-11-15"
IDS = ["SD-2023-2", "SD-2024-1", "SD-2025-2", "SD-2025-3"]
REDRAW = {"SD-2024-1", "SD-2025-2"}
CHOICE = {
 "SD-2023-2": "定案：#1 振態正規化採二樓（下層）分量取 1，振態質量、振態勁度、參與因子依此寫出，並註明有效質量 Γ²M* 與正規化無關",
 "SD-2025-2": "定案：#1 振態正規化採下層分量 φ1 取 1，參與係數依此寫出，並註明有效質量 Γ²M* 與正規化無關",
}
FIGCAP = {
 "SD-2024-1": ("三層剪力屋架，剛性梁，每層兩根 EI 柱、柱底固定，樓高皆 h、跨度 2h；質量由下往上 m、m、m/2，外力 p1～p3 作用於各樓版", "頂層質量是 m/2；每層兩根柱，層勁度 24EI/h³"),
 "SD-2025-2": ("兩層剪力構架（每柱 k/2）與等效串聯模型，m1、m2 為下、上層，u1、u2 向右，柱底固定", "每柱標 k/2，兩柱合計才是層勁度 k；u1 在下層"),
}
SEC1 = {
 "SD-2023-2": ("""| 層勁度 | 第 1 層（地面至二樓版）$k_1=200000$ N/m、第 2 層（二樓版至屋頂）$k_2=180000$ N/m（判讀 #2） | $k_1$、$k_2$ 對調 |
| 樓層名稱 | 本庫舊解 §1 以「地面至 1F、1F 至 2F」稱兩層，指的是同一組層勁度，不影響答案 | 依台灣樓層名稱把 $k_2$ 讀成第三層 |
| 振態正規化 | 考卷未指定；本解取二樓分量為 1，振態質量、振態勁度、參與因子依此（判讀 #1，使用者授權依建議確認） | 數值未寫明正規化 |
| Rayleigh 錨點 | $\\omega=2\\pi$、$10\\pi$ rad/s（1 Hz、5 Hz）處 $\\xi=0.03$、$0.05$（判讀 #5） | 直接把 1、5 代入當 rad/s |""",
  "$\\{\\phi\\}_n=\\{1,\\ r_n\\}$（二樓、屋頂）；$M_n^*=\\phi_n^TM\\phi_n$、$K_n^*=\\omega_n^2M_n^*$、$\\Gamma_n=\\phi_n^TM\\{1\\}/M_n^*$。"),
 "SD-2024-1": ("""| 頂層質量 | $m/2$（判讀 #2） | 三層都是 $m$ |
| 層勁度 | 每層兩根雙固端柱，$2\\times12EI/h^3=24EI/h^3$（判讀 #1） | 只算一根柱，或用懸臂 $3EI/h^3$ |
| 「3F」 | 頂樓版（質量 $m/2$ 那層），對 3F 正規化＝頂層分量取 1（判讀 #4） | 把 3F 當成一樓 |
| 跨度 $2h$ | 剛性梁下不影響側向勁度（判讀 #6） | 代入勁度計算 |""",
  "$u_1$、$u_2$、$u_3$ 由下往上（對應 $p_1\\sim p_3$）；$k=24EI/h^3$；$L_n=\\phi_n^TM\\{1\\}$、有效質量 $m_n^*=L_n^2/M_n$。"),
 "SD-2025-2": ("""| 層勁度 | 每柱 $k/2$，兩柱合計層勁度 $k_1=k_2=1500$ kN/m（判讀 #2） | 把 $k/2$ 當層勁度，或兩柱各 $k$ |
| 自由度 | $u_1$ 下層、$u_2$ 上層（判讀 #3） | 上下顛倒 |
| 振態正規化 | 考卷未指定；本解取 $\\phi_1$（下層分量）為 1，$\\Gamma_i$ 依此（判讀 #1，使用者授權依建議確認） | $\\Gamma_i$ 未寫明正規化 |
| 單位 | 質量 kN·s²/m、勁度 kN/m，$k/m$ 單位 s⁻²（判讀 #6） | 把 100 kN·s²/m 當重量 |""",
  "$\\{\\phi\\}_i=\\{1,\\ \\phi_{2i}\\}$（下層、上層）；$\\Gamma_i=\\phi_i^TM\\{1\\}/\\phi_i^TM\\phi_i$。"),
 "SD-2025-3": ("""| 頻率單位 | 題給 $\\omega_i$ 已是 rad/s（判讀 #1） | 再乘 $2\\pi$ |
| 錨點 | 第一、第三振態 $\\zeta=0.05$，求 $a_0$、$a_1$ 後代 $\\omega_2$（判讀 #2） | 用第一、第二振態當錨點 |
| 係數單位 | $a_0$ 為 1/s、$a_1$ 為 s（判讀 #3） | — |""",
  "$\\zeta_n=\\dfrac{a_0}{2\\omega_n}+\\dfrac{a_1\\omega_n}{2}$。"),
}
SEC1_PAT = [r"^## 1\. 原始題目重述.*?(?=^---\s*\n\s*## 2\.|^## 2\.)"]
def confirm_problem(qid):
    p = SD/f"raw/solutions/{qid}/{qid}-problem.md"; t = p.read_text(encoding="utf-8")
    if "判讀狀態 | **已確認**" in t: return False
    note = f"{D} 使用者授權依 Claude 建議確認" + (f"；{CHOICE[qid]}" if qid in CHOICE else "")
    t2 = re.sub(r"判讀狀態 \| \*\*待確認\*\*（", f"判讀狀態 | **已確認**（{note}。原轉錄：", t, count=1)
    assert t2 != t
    t2 = t2.replace("（影響答案，請確認）", "（影響答案）")
    t2 = re.sub(r"(\| 不確定（[^|]*?)\s\|\n", lambda m: m.group(1) + "；使用者授權依建議確認 |\n", t2)
    t2 = t2.rstrip("\n") + f"\n*確認：{D} 使用者授權依 Claude 建議確認（SD-U1-3 題目正本推廣・批 3，關卡一）*\n"
    p.write_text(t2, encoding="utf-8"); return True
def rewrite_sec1(qid):
    p = SD/f"raw/solutions/{qid}/{qid}.md"; t = p.read_text(encoding="utf-8")
    if "## 1. 題目（考卷原文見題目正本）" in t: return False
    m = None
    for pat in SEC1_PAT:
        m = re.search(pat, t, re.S | re.M)
        if m: break
    assert m, qid
    old = m.group(0)
    prob = (SD/f"raw/solutions/{qid}/{qid}-problem.md").read_text(encoding="utf-8")
    for png in re.findall(r"\(([^)]*?\.png)\)", old):
        if os.path.exists(SD/f"raw/solutions/{qid}/{png}"): assert png in prob, (qid, png)
    assert not re.findall(r"\((figs/[^)]*?\.svg)\)", old), qid   # 本組舊 §1 無自繪圖
    rows, note = SEC1[qid]
    s = ["## 1. 題目（考卷原文見題目正本）", "",
         f"> 考卷原文、公式／附表、附圖與判讀清單（已確認）見 [`{qid}-problem.md`]({qid}-problem.md)。本節只列解題時最容易讀錯的地方與本解使用的記號；題意以題目正本為準。", ""]
    if qid in REDRAW:
        alt, cap = FIGCAP[qid]
        s += [f"![{qid} 重繪題目附圖：{alt}](figs/{qid}-fig-1-problem.svg)", f"*重繪自考卷附圖，依題目正本判讀清單；本圖攔下的判讀錯誤：{cap}。*", ""]
    s += ["### 常見誤讀", "", "| 項目 | 正確判讀 | 常見誤讀 |", "|------|---------|---------|", rows, "", f"**本解記號：** {note}", ""]
    new = "\n".join(s) + "\n"
    t = t.replace(old, new)
    extra = f"，重繪附圖 figs/{qid}-fig-1-problem.svg" if qid in REDRAW else ""
    t = t.rstrip("\n") + f"\n\n*修正日期：{D}（§1 改為指向題目正本{extra}）*\n"
    p.write_text(t, encoding="utf-8"); return True
if __name__ == "__main__":
    for q in IDS: print(q, "problem", confirm_problem(q), "sec1", rewrite_sec1(q))
