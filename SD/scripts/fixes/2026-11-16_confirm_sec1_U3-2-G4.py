#!/usr/bin/env python3
"""SD-U3-2 組 U3-2-G4（SD-2018-1、2018-4、2023-3、2023-4）關卡一確認後：解析 §1 改為指向題目正本。
題目正本建立時已寫成「已確認（2026-11-16，使用者授權依 Claude 建議）」，本腳本只檢查、不改 problem.md。
可重複執行（已處理者略過）。用法：python3 <本檔> <SD 科目資料夾>
不改 question_index.json（problemStatus 由總控統一寫入）。只動 §1 與頁尾一行。"""
import sys, re, os
from pathlib import Path
SD = Path(sys.argv[1]); D = "2026-11-16"
IDS = ["SD-2018-1", "SD-2018-4", "SD-2023-3", "SD-2023-4"]
REDRAW = {"SD-2018-1"}
FIGCAP = {
 "SD-2018-1": ("單層剪力屋架，剛性梁（W＝70 kN），兩柱各 EI、柱底固定，H＝3 m、L＝6 m；線性黏性阻尼器 C 由左柱底斜撐至右柱頂，兩端鉸接",
               "阻尼器是對角斜撐（傾角由 H、L 決定，cosθ＝2/√5），不是水平裝設；兩柱底固定、梁剛性"),
}
SEC1 = {
 "SD-2018-1": ("""| 阻尼器傾角 | 斜撐由左柱底至右柱頂，水平投影 $L$、垂直投影 $H$，$\\cos\\theta=L/\\sqrt{L^2+H^2}=2/\\sqrt5$（判讀 #5、#6） | 當成水平裝設（$\\cos\\theta=1$），或把 $\\cos\\theta$ 寫成 $H/\\sqrt{L^2+H^2}$ |
| 質量 | $m=W/g=70/9.8$ kN·s²/m（判讀 #7） | 把 70 kN 直接當質量 |
| 層勁度 | 剪力屋、剛性梁、柱底固定：每柱 $12EI/H^3$，兩柱合計（判讀 #2–#4） | 用懸臂 $3EI/H^3$，或只算一根柱 |
| 阻尼器最大出力 | 考卷沒指定速度；本解以擬速度 $\\omega_0 S_d$ 為最大相對速度，阻尼器軸向速度再乘 $\\cos\\theta$（判讀 #1，使用者授權依建議確認） | 用位移乘 $C$，或漏乘 $\\cos\\theta$ |
| 「對角斜稱」 | 考卷誤植，意為對角斜撐（判讀 #11） | — |""",
  "$\\omega_0=\\sqrt{k/m}$；$c_{\\text{eff}}=C\\cos^2\\theta$（等效水平阻尼係數）；$S_d$、$S_v=\\omega_0S_d$；$F_{d,\\max}=C\\,S_v\\cos\\theta$。"),
 "SD-2018-4": ("""| 傳遞設計水平加速度 $A$ | 設計位移時支承水平力除以重量：$D/R+\\mu=0.08$（判讀 #1，使用者授權依建議確認） | 只取 $D/R$（漏摩擦項），或把 $A$ 當成 $S_a$ |
| $S_a$ 式中的 $T$ | 代入有效週期 $T_e$；$S_a$ 以 $g$ 的倍數表示（判讀 #3、#4） | 用上部結構固定基座週期 |
| $B$ 表 | 表列值之間線性內插（判讀 #2，使用者授權依建議確認） | 直接取最近的表列值 |
| 單位 | $D$、$R$ 用 cm，$g=980$ cm/s²（判讀 #6） | cm 與 m 混用 |""",
  "$A=D/R+\\mu$；$T_e$ 有效週期；$\\xi_e$ 等效阻尼比；$B$ 阻尼修正係數（提示表）。"),
 "SD-2023-3": ("""| 總靜載重 | $W=5000$ kN 是重量，$m=W/g$；考卷沒給 $g$，本解取 9.81 m/s²（判讀 #1、#3，使用者授權依建議確認） | 把 5000 kN 直接當質量 |
| 等效阻尼比 | $\\beta_{eff}=W_D/(2\\pi K_{eff}D_D^2)$（判讀 #2） | 分母漏 $2\\pi$，或寫成 $W_D/(4\\pi K_{eff}D_D^2)$ |
| 遲滯迴圈面積 | 設計位移下一個完整循環的消能 50 kN·m（判讀 #4） | 當成半循環 |
| 規範依據 | ㈡、㈣依現行建築物耐震設計規範（111 年版）隔震章節（判讀 #6） | 引用舊版條文 |""",
  "本解以 $W_D$ 表示遲滯迴圈面積（題目正本記為 $E_D$），注意與重量 $W$ 區別；$D_D$ 設計位移、$K_{eff}$ 有效勁度、$T_{eff}$ 有效週期、$\\beta_{eff}$ 等效阻尼比。"),
 "SD-2023-4": ("""| 等值阻尼比定義 | $\\xi_{eq}=\\dfrac{1}{4\\pi}\\dfrac{\\omega_n}{\\omega}\\dfrac{W_D}{U_{max}}$，$\\omega$ 為外力頻率（判讀 #1，使用者授權依建議確認） | 用 $W_D/(4\\pi U_{max})$，漏乘 $\\omega_n/\\omega$（$\\omega=2\\pi$ 的 6 個答案低估一半） |
| 圖 a 的 $\\omega$ | 外力（振動）圓頻率，代 $2\\pi$ 或 $4\\pi$ rad/s（判讀 #7） | 代自然頻率 $\\omega_n$ |
| 圖 c | 力 $\\pm0.4\\pi$ N 為定值，位移範圍 $\\pm\\rho$（判讀 #6） | 把 $0.4\\pi$ 乘上 $\\rho$ |
| 座標軸 | 橫軸位移、縱軸力，$\\rho$ 為振幅 0.01／0.02 m（判讀 #2、#3） | — |""",
  "$W_D$ 每循環消能（題目正本記為 $E_D$）；$U_{max}=k\\rho^2/2$（題目正本記為 $E_{S0}$）；$\\omega_n=\\sqrt{k/m}$；$c_{eq}=W_D/(\\pi\\omega\\rho^2)$。"),
}
SEC1_PAT = r"^## 1\. 原始題目重述.*?(?=^---\s*\n\s*#{2,3} 2\.|^#{2,3} 2\.)"
def check_problem(qid):
    t = (SD/f"raw/solutions/{qid}/{qid}-problem.md").read_text(encoding="utf-8")
    assert "**已確認（2026-11-16，使用者授權依 Claude 建議）**" in t, qid
def rewrite_sec1(qid):
    p = SD/f"raw/solutions/{qid}/{qid}.md"
    with open(p, encoding="utf-8", newline="") as f: raw = f.read()
    crlf = "\r\n" in raw; t = raw.replace("\r\n", "\n")       # SD-2018-1 為 CRLF，保留原換行
    if "## 1. 題目（考卷原文見題目正本）" in t: return False
    m = re.search(SEC1_PAT, t, re.S | re.M); assert m, qid
    old = m.group(0)
    prob = (SD/f"raw/solutions/{qid}/{qid}-problem.md").read_text(encoding="utf-8")
    for png in re.findall(r"\(([^)]*?\.png)\)", old):
        assert png in prob, (qid, png)
    assert not re.findall(r"\((figs/[^)]*?\.svg)\)", old), qid   # 本組舊 §1 無自繪圖
    if qid in REDRAW: assert (SD/f"raw/solutions/{qid}/figs/{qid}-fig-1-problem.svg").exists(), qid
    rows, note = SEC1[qid]
    s = ["## 1. 題目（考卷原文見題目正本）", "",
         f"> 考卷原文、公式／附表、附圖與判讀清單（已確認）見 [`{qid}-problem.md`]({qid}-problem.md)。本節只列解題時最容易讀錯的地方與本解使用的記號；題意以題目正本為準。", ""]
    if qid in REDRAW:
        alt, cap = FIGCAP[qid]
        s += [f"![{qid} 重繪題目附圖：{alt}](figs/{qid}-fig-1-problem.svg)", f"*重繪自考卷附圖，依題目正本判讀清單；本圖攔下的判讀錯誤：{cap}。*", ""]
    s += ["### 常見誤讀", "", "| 項目 | 正確判讀 | 常見誤讀 |", "|------|---------|---------|", rows, "", f"**本解記號：** {note}", "", ""]
    new = "\n".join(s)
    t = t.replace(old, new, 1)
    extra = f"，重繪附圖 figs/{qid}-fig-1-problem.svg" if qid in REDRAW else ""
    t = t.rstrip("\n") + f"\n\n*修正日期：{D}（§1 改為指向題目正本{extra}）*\n"
    if crlf: t = t.replace("\n", "\r\n")
    with open(p, "w", encoding="utf-8", newline="") as f: f.write(t)
    return True
if __name__ == "__main__":
    for q in IDS:
        check_problem(q); print(q, "sec1", rewrite_sec1(q))
