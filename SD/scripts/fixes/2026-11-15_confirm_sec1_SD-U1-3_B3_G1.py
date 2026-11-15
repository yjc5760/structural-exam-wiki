#!/usr/bin/env python3
"""SD-U1-3 批 3 G1（SD-2017-1、2019-1、2019-2、2019-3）關卡一確認後：problem.md 凍結、解析 §1 改為指向題目正本。
不改 question_index.json（problemStatus 由批次主流程統一寫入）。可重複執行（已處理者略過）。
用法：python3 <本檔> <SD 科目資料夾>
2026-11-15 使用者授權依 Claude 建議確認（pipeline 一次做完，關卡一不停）。"""
import sys, re, os
from pathlib import Path
SD = Path(sys.argv[1]); D = "2026-11-15"
IDS = ["SD-2017-1", "SD-2019-1", "SD-2019-2", "SD-2019-3"]
REDRAW = set(IDS)
CHOICE = {
 "SD-2019-1": "影響答案項目定案：#1 圓球質量主解採圖上標示 (2/3)m（兩張圖一致），題文「質量為 m」的結果於解析 §5 對照",
}
FIGCAP = {
 "SD-2017-1": ("固定牆以彈簧 k、阻尼器（ξ＝0.05）並聯接質塊 M，質塊在滾輪上；虛線為初始位移 v0（向右）的位置，初速 0", "初始位移 v0 向右、初速 0，為自由振動；考卷的 ω＝k/M 少了根號"),
 "SD-2019-1": ("左右兩圖：長 2L 的剛性梁左端鉸支、右端自由；距鉸 L 處以彈簧 2k 接上方固定面；自由端以彈簧 k 懸吊圓球 (2/3)m；㈠梁總質量 0、㈡梁總質量 m", "2k 在梁中點、k 在自由端；圓球質量圖上標 (2/3)m，與題文 m 不一致"),
 "SD-2019-2": ("兩層剪力屋架：下層 m1＝40 kg、k1＝2000 N/m，上層 m2＝20 kg、k2＝1000 N/m；起始位移 u1(0)＝0.1 m、u2(0)＝0.2 m，初速 0", "下層質量、勁度較大；起始位移 0.2 m 在屋頂"),
 "SD-2019-3": ("兩層構架，兩層質量皆 5×10⁴ kg，u1 在二樓、u2 在屋頂，φ1＝{0.5, 1.0}；反應譜為曲線圖，不重繪（見題目正本證據圖）", "φ1 分量依 u1（二樓）、u2（屋頂）排列"),
}
SEC1 = {
 "SD-2017-1": ("""| 考卷公式 | 括號內「$\\omega=k/M$」少了根號，視為 $\\omega=\\sqrt{k/M}$（判讀 #3）；答案為 $v_0$ 的倍數，不受影響 | 照抄成 $\\omega=k/M$ 帶入週期 |
| 「來回震動 3 次」 | 3 個完整週期，$t=3T_D\\approx6\\pi/\\omega$（判讀 #1） | 3 個半週期或 3 次通過平衡位置 |
| 振幅 | 包絡線 $\\sqrt{A^2+B^2}\\,e^{-\\xi\\omega t}$，題給 $\\sqrt{1+\\xi^2}\\approx1$、$\\tan^{-1}\\xi\\approx0$（判讀 #2） | 只取 $A=v_0$ 而忽略 $B$ 項的意義 |
| 初始條件 | 初始位移 $v_0$ 向右、初速 0（判讀 #5） | 把 $v_0$ 當初速 |""",
  "$x(t)$ 為質塊位移，$x(0)=v_0$；$T_D=2\\pi/\\omega_D$；$A_n$ 為第 $n$ 週後振幅。"),
 "SD-2019-1": ("""| 圓球質量 | 題文寫 $m$、圖上標 $\\frac{2}{3}m$；主解採圖上 $\\frac{2}{3}m$（判讀 #1，使用者授權依建議確認），題文 $m$ 的結果見 §5 | 未察覺矛盾，兩者混用 |
| 彈簧位置 | $2k$ 在距鉸 $L$ 處（梁中點）、$k$ 在自由端（距鉸 $2L$）懸吊圓球（判讀 #3、#4） | $2k$ 放在自由端 |
| 梁質量 | ㈠ 0；㈡ 總質量 $m$ 均布於 $2L$，對鉸 $I_O=\\frac{1}{3}m(2L)^2$（判讀 #5） | 用 $\\frac{1}{12}mL^2$ 或梁長取 $L$ |
| 自由度 | 梁轉角（或自由端位移）＋圓球鉛直位移，共 2 個；重力不入運動方程式（判讀 #6、#7） | ㈠ 漏掉梁端自由度的約束條件 |""",
  "$u_1$ 為梁自由端鉛直位移（$\\theta=u_1/2L$）、$u_2$ 為圓球鉛直位移，向下為正。"),
 "SD-2019-2": ("""| 質量勁度位置 | 下層 $m_1=40$ kg、$k_1=2000$ N/m，上層 $m_2=20$ kg、$k_2=1000$ N/m（判讀 #1） | 上下對調 |
| 起始條件 | $u_1(0)=0.1$ m、$u_2(0)=0.2$ m，初速 0（判讀 #4） | 把位移向量當成振態 |
| 阻尼 | 考卷未提，無阻尼自由振動（判讀 #5） | — |""",
  "$u_1$、$u_2$ 為二樓、屋頂側移（m）；$q_n(t)$ 為振態座標。"),
 "SD-2019-3": ("""| $S_a(T=1.0)$ | $0.50g$（題目正本數位化 0.506；判讀 #1） | 讀成峰值 1.27 g 或 0.6 g |
| 週期 | 1 秒為基本振態週期（判讀 #2） | — |
| 振態順序 | $\\phi_1=\\{0.5,1.0\\}$ 依 $u_1$（二樓）、$u_2$（屋頂）（判讀 #3） | 上下顛倒 |
| 位移不變法則 | 非彈性位移＝彈性位移，$R=\\mu=5$（判讀 #5） | 層間位移再除以 5 |""",
  "$\\Gamma_1=L_1/M_1$；$S_d=S_a/\\omega^2$；$\\Delta_i$ 為第 $i$ 層層間位移。"),
}
SEC1_PAT = [r"^## 1\. 原始題目重述.*?(?=^---\s*\n\s*## 2\.|^## 2\.)",
            r"^## 1\. 題目重述.*?(?=^---\s*\n\s*## 2\.|^## 2\.)"]
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
    for x in svgs:
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
    t = t.rstrip("\n") + f"\n\n*修正日期：{D}（§1 改為指向題目正本{extra}）*\n"
    p.write_text(t, encoding="utf-8"); return True
if __name__ == "__main__":
    for q in IDS: print(q, "problem", confirm_problem(q), "sec1", rewrite_sec1(q))
