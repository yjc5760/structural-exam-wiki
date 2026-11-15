#!/usr/bin/env python3
"""SD-U1-3 批 3 G3（SD-2021-3、2021-4、2022-1、2022-3）關卡一確認後：problem.md 凍結、解析 §1 改為指向題目正本。
不改 question_index.json（problemStatus 由批次統一寫入）。可重複執行（已處理者略過）。用法：python3 <本檔> <SD 科目資料夾>
2026-11-15 使用者授權依 Claude 建議確認（pipeline 一次做完，關卡一不停）。"""
import sys, re, json, os
from pathlib import Path
SD = Path(sys.argv[1]); D = "2026-11-15"
IDS = ["SD-2021-3","SD-2021-4","SD-2022-1","SD-2022-3"]
REDRAW = {"SD-2021-3","SD-2022-1"}
CHOICE = {
 "SD-2021-3": "影響答案項目定案：#1 初始位移採粗索只拉一樓版、上兩層隨之平移，{v1,v2,v3}＝{6,6,6} cm（本庫舊解採 {6,0,0}，交階段 C）；#2 主解寫頂層層間剪力的時間函數並求其最大值",
 "SD-2021-4": "影響答案項目定案：#1 取週期 0.1–0.3 s 範圍內的最不利值；#2 ㈠ 主解先求線彈性穩態反應，結構降伏時說明所用的近似法則及其限制",
 "SD-2022-1": "影響答案項目定案：#1 忽略軸向變形，B 點質量同時隨自由度 1（水平）與自由度 2（垂直）運動",
}
EXTRA = {
 "SD-2021-3": "；§1 舊重述的初始位移 {6,0,0} 與考卷不符、圖說把 v 寫成速度，改列常見誤讀（正文勘誤見階段 C）",
 "SD-2021-4": "；§1 舊重述的地表加速度振幅 0.75 g 與考卷圖 0.50 g 不符，改列常見誤讀（正文勘誤見階段 C）",
}
FIGCAP = {
 "SD-2021-3": ("三層剪力構架，由下往上質量 m、m、m/2、層勁度皆 k；粗索拉一樓版 6 cm，只有一層柱變形、上兩層隨之平移；右側照錄考卷給的 ω 與 φ", "粗索只拉一樓版、上兩層樓版隨之平移，初始位移不是 {6,0,0}"),
 "SD-2022-1": ("倒 L 形剛構架，柱底固定、柱與梁長皆 3 m，B 為懸臂自由端；自由度 1 為 A 水平、2 為 B 垂直、3／4 為 A／B 轉角（逆時針）；p(t)＝sin(5t) 向上作用於 B", "B 點水平位移等於自由度 1，m_B 也有水平慣性；轉角逆時針為正"),
}
SEC1 = {
 "SD-2021-3": ("""| 初始位移 | 粗索只拉一樓版：一樓版相對地面 6 cm，上兩層隨之平移，$\\{v_1,v_2,v_3\\}=\\{6,6,6\\}$ cm、初速 0（判讀 #1、#4，使用者授權依建議確認） | $\\{6,0,0\\}$ cm：只有一樓有初始位移、上兩層不動（本庫舊解） |
| 所求 | 頂層（第三層）層間剪力 $V_3=k(v_3-v_2)$；主解寫時間函數並求最大值（判讀 #2，使用者授權依建議確認） | 只寫時間函數，或以 SRSS 估自由振動的最大值 |
| 振態分量順序 | 由上而下依序為 $v_1$（一樓）、$v_2$、$v_3$（頂樓）（判讀 #5） | 反序 |
| $v_i$ | 各樓版側向位移，向右為正（判讀 #11） | 當成速度（本庫舊解 §1 圖說） |
| 阻尼 | 考卷未給，視為無阻尼自由振動（判讀 #3） | — |""",
  "$x_1,x_2,x_3$（即題圖 $v_1,v_2,v_3$）為一、二、三樓版側移；$A_i$ 為振態展開係數；$V_3=k(x_3-x_2)$。"),
 "SD-2021-4": ("""| 地表加速度振幅 | 0.50 g（圖上峰谷對齊 ±0.50 刻度；判讀 #3） | 0.75 g（本庫舊解 §1，把縱軸上限當振幅） |
| 地動波形 | 正弦波、週期 0.3 s、自零以正斜率起始，共 9 秒（30 個週期）（判讀 #3、#4） | — |
| 週期不確定 | 取 0.1–0.3 s 範圍內的最不利值（判讀 #1，使用者授權依建議確認） | 取平均週期 0.2 s |
| ㈠ 反應型態 | 主解先求線彈性穩態反應；結構降伏時說明所用近似法則及其限制（判讀 #2，使用者授權依建議確認） | 未說明是彈性或非彈性位移 |
| 單位 | $1g=980$ cm/s²（題給）；$R_y$ 單位 kN | 改用 9.81 m/s² |""",
  "$a_g$ 地表加速度振幅、$T_g$ 地動週期；$u_{el}$ 彈性位移、$u_y=R_y/k$ 降伏位移、$\\mu$ 位移韌性比。"),
 "SD-2022-1": ("""| B 點質量 | 忽略軸向變形，$m_B$ 隨自由度 1 水平運動、也隨自由度 2 垂直運動（判讀 #1，使用者授權依建議確認） | 質量矩陣 $M_{11}$ 只放 $m_A$ |
| 自由度 3、4 | A、B 轉角，逆時針為正（判讀 #6） | 順時針為正 |
| B 點 | 懸臂自由端，無支承（判讀 #2） | 當成有支承 |
| EI 單位 | 考卷寫 N/m²，應為 N·m²，數值照用（判讀 #8） | — |
| 外力 | $p(t)=\\sin(5t)$ 作用於自由度 2、向上為正，激振圓頻率 5 rad/s（判讀 #7） | 把 5 當成 Hz |""",
  "$K^*$、$M^*$ 為濃縮後（自由度 1、2）的勁度與質量矩陣；$\\Omega=5$ rad/s；$q_n$ 為振態座標。"),
 "SD-2022-3": ("""| 自由度順序 | 第 1 列為下層、第 2 列為頂樓（$K_{22}=k_2$；判讀 #1） | 顛倒 |
| 反應譜 | $S_a=\\min(0.45/T,\\ 0.7)\\,g$（判讀 #2） | 忘了 0.7 g 上限，或把它當下限 |
| 質量單位 | kN·s²/m（＝t），不是重量（判讀 #4） | 當成 kN 重量再除以 g |
| ㈠ | 依現行建築物耐震設計規範作答（判讀 #5） | 照考試當年的規範版本 |""",
  "$\\Gamma_i$ 振態參與因子、$S_{di}=S_a(T_i)/\\omega_i^2$、$X_{2i}$ 第 $i$ 振態頂樓位移。"),
}
SEC1_PAT = [r"^## 1\. 原始題目重述.*?(?=^---\s*\n\s*## 2\.|^## 2\.)",
            r"^## 1\. 題目重述.*?(?=^---\s*\n\s*## 2\.|^## 2\.)",
            r"^## §1 題目重述.*?(?=^---\s*\n\s*## §2|^## §2)",
            r"^## 題目敘述.*?(?=^---\s*\n\s*## 解題步驟|^## 解題步驟)"]
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
    svgs = re.findall(r"\((figs/[^)]*?\.svg)\)", old)
    svg_blocks = []
    for x in svgs:   # 保留解析自繪圖與其圖說
        mm = re.search(r"(!\[[^\]]*\]\(" + re.escape(x) + r"\)\s*\n(?:\s*\n)?(\*[^\n]*\*)?)", old)
        svg_blocks.append(mm.group(1).strip() if mm else f"![{qid} 解析自繪圖]({x})")
    rows, note = SEC1[qid]
    s = ["## 1. 題目（考卷原文見題目正本）", "",
         f"> 考卷原文、公式／附表、附圖與判讀清單（已確認）見 [`{qid}-problem.md`]({qid}-problem.md)。本節只列解題時最容易讀錯的地方與本解使用的記號；題意以題目正本為準。", ""]
    if qid in REDRAW:
        alt, cap = FIGCAP[qid]
        s += [f"![{qid} 重繪題目附圖：{alt}](figs/{qid}-fig-1-problem.svg)", f"*重繪自考卷附圖，依題目正本判讀清單；本圖攔下的判讀錯誤：{cap}。*", ""]
    s += ["### 常見誤讀", "", "| 項目 | 正確判讀 | 常見誤讀 |", "|------|---------|---------|", rows, "", f"**本解記號：** {note}", ""]
    if svg_blocks:
        s += ["### 判讀圖解（解析自繪）", ""] + sum(([b, ""] for b in svg_blocks), [])
    new = "\n".join(s) + "\n"
    t = t.replace(old, new)
    extra = f"，重繪附圖 figs/{qid}-fig-1-problem.svg" if qid in REDRAW else ""
    extra += EXTRA.get(qid, "")
    t = t.rstrip("\n") + f"\n\n*修正日期：{D}（§1 改為指向題目正本{extra}）*\n"
    p.write_text(t, encoding="utf-8"); return True
if __name__ == "__main__":
    for q in IDS: print(q, "problem", confirm_problem(q), "sec1", rewrite_sec1(q))
