#!/usr/bin/env python3
"""SD 組 U3-1-G2 階段 E：把解題圖解插回解析（2026-11-16，非勘誤）。可重複執行；保留原檔換行格式。
SD-2019-4 fig-1-short-column、SD-2022-2 fig-1-hoop-zones、SD-2022-4 fig-1-distributions（腳本 gen_<id>.py）。"""
import os
SOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "raw", "solutions")
JOBS = {
"SD-2019-4": ("### (2) 老舊建築物容易出現短柱破壞的位置",
 "![SD-2019-4 短柱效應：同一層間位移下，無窗台牆的柱以全淨高 H 變形，有窗台牆的柱只有窗台以上 he 段變形，勁度放大 (H/he)^3 倍、撓曲降伏時剪力放大 H/he 倍](figs/SD-2019-4-fig-1-short-column.svg)\n\n"
 "*圖 1　短柱效應示意（柱淨高 3.0 m 為示意、窗台牆約 1 m）：同一層間位移 $\\Delta$ 下，可變形長度由 $H$ 縮為 $h_e$，側向勁度 $\\propto 1/h_e^3$（本例 ×3.38）、柱端撓曲降伏時的剪力 $2M_p/h_e$ 也放大（×1.50），而剪力強度不變。本圖攔下「短柱是柱本身很短」與「只看強度、不看勁度與降伏剪力」兩種誤解。*\n\n",
 "（非勘誤）圖解補繪：§4 ㈠ 加 figs/SD-2019-4-fig-1-short-column.svg（腳本 gen_SD-2019-4.py，可重跑）"),
"SD-2022-2": ("#### (D) 規定圖示說明（文字化）",
 "![SD-2022-2 特殊抗彎矩構架梁：立面標出兩端 2h 閉合箍筋區、第一道 5 cm、間距 15 cm、其他區段 d/2，搭接禁區與可搭接區；平面標出梁寬上限為柱寬加每側 min(c2, 0.75c1)](figs/SD-2022-2-fig-1-hoop-zones.svg)\n\n"
 "*圖 1　以 §5.1 示例（柱 60×60 cm、梁 $h=70$ cm、$d=64$ cm、D25）畫出 18.3 節的配筋規定：閉合箍筋區與搭接禁區都量 $2h=140$ cm（舊解的 $2d=128$ cm 偏短），區內間距 15 cm；梁寬上限 150 cm（舊式 165 cm 已不適用）。本圖攔下 $2d$／$2h$ 混淆與套用舊版數值。*\n\n",
 "（非勘誤）圖解補繪：§4 ㈢ 加 figs/SD-2022-2-fig-1-hoop-zones.svg（腳本 gen_SD-2022-2.py，可重跑）"),
"SD-2022-4": ("## 5. 各方法應用局限性（子題二）",
 "![SD-2022-4 五種側推力豎向分布的 3 層算例並排：均勻 200/200/200、倒三角 100/200/300、指數 42.9/171.4/385.7、經驗（規範式）82.5/165.0/352.5、SRSS 121.4/165.3/313.3 kN](figs/SD-2022-4-fig-1-distributions.svg)\n\n"
 "*圖 1　同一組算例假設（$V=600$ kN）下五種分布的各層側力，箭頭長度與力成正比。經驗分布用規範式（頂層含 $F_t=105$ kN），SRSS 為振態層剪力組合後差分的單一分布。本圖攔下「經驗分布＝一階振態」「SRSS 沒有側力數值（多次側推）」兩種舊解誤讀。*\n\n---\n\n",
 "（非勘誤）圖解補繪：§4 彙整表後加 figs/SD-2022-4-fig-1-distributions.svg（腳本 gen_SD-2022-4.py，可重跑）"),
}
for q, (anchor, block, foot) in JOBS.items():
    p = os.path.join(SOL, q, f"{q}.md")
    raw = open(p, encoding="utf-8", newline="").read(); nl = "\r\n" if "\r\n" in raw else "\n"; s = raw.replace("\r\n", "\n")
    if "圖解補繪：" in s and f"figs/{q}-fig-1-" in s: print(q, "已處理，略過"); continue
    assert s.count(anchor) == 1, q
    svg = block.split("](")[1].split(")")[0]; assert os.path.exists(os.path.join(SOL, q, svg)), svg
    if q == "SD-2022-4":   # 插在彙整表後、--- 分隔之前
        i = s.index(anchor); j = s.rindex("\n---\n", 0, i); s = s[:j] + "\n\n" + block.rstrip("\n").rstrip("-").rstrip("\n") + "\n" + s[j:]
    else:
        s = s.replace(anchor, block + anchor)
    s = s.rstrip("\n") + "\n" + f"*修正日期：2026-11-16{foot}*" + "\n"
    open(p, "w", encoding="utf-8", newline="").write(s.replace("\n", nl)); print(q, "已插圖")
