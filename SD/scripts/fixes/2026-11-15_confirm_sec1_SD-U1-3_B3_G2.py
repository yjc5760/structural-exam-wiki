#!/usr/bin/env python3
"""SD-U1-3 批 3 G2（SD-2020-2、2020-3、2021-1、2021-2）關卡一確認後：problem.md 凍結、解析 §1 改為指向題目正本。
索引 problemStatus 由批次主流程統一寫入（本檔不改 question_index.json）。
可重複執行（已處理者略過）。用法：python3 <本檔> <SD 科目資料夾>
2026-11-15 使用者授權依 Claude 建議確認（pipeline 一次做完，關卡一不停）。"""
import sys, re, json, os
from pathlib import Path
SD = Path(sys.argv[1]); D = "2026-11-15"
IDS = ["SD-2020-2","SD-2020-3","SD-2021-1","SD-2021-2"]
REDRAW = {"SD-2021-1","SD-2021-2"}
CHOICE = {
 "SD-2021-1": "影響答案項目定案：#1「系統從靜止開始」取 t=0 時台車位移為 0、台車絕對速度為 0（構架速度 ω/2 屬給定激振）；#2 x 取台車絕對位移",
}
FIGCAP = {
 "SD-2021-1": ("剛性構架以滾輪置於地面，受向右位移 d(t)＝sin(ωt/2)；台車 m 以輪置於構架底板，左右各一根彈簧 k 接構架內壁；x 為台車位移", "兩根彈簧都接在構架內壁、隨構架移動（彈簧力取決於台車相對構架的位移）；構架位移是給定激振，不是自由度"),
 "SD-2021-2": ("半正弦波載重 p(t)＝100 sin(πt/0.1) kN，0≤t≤0.1 s，峰值 10² kN 在 0.05 s，0.1 s 後為零", "延時 0.1 s 是整個半波（峰值在 0.05 s），不是峰值時刻"),
}
SEC1 = {
 "SD-2020-2": ("""| 振態向量排列 | 由上而下為一樓、二樓、頂樓，第三列 1.00000 為頂樓（判讀 #1） | 第一列當頂樓 |
| 振態數據 | 照錄考卷；振態 1 與振態 2、3 對等質量不精確正交（判讀 #2），有效質量比各振態分別以 $L_n^2/M_n$ 計 | 以為振態已正規化、直接用 $\\phi^T\\phi=1$ |
| $S_a$ | 以 g 計，乘 $g=9.8$ m/s²（判讀 #3）；$T_1=1.7$ s 落在 $0.5/T$ 段，$T_2$、$T_3$ 落在 0.5 平台（判讀 #4） | 直接當 m/s²；$T_1$ 套平台 |
| 振態數 | 由低頻起累加有效質量比至 ≥95% 的最少振態數（判讀 #6） | 一律取全部振態 |""",
  "$\\phi_{n}$ 分量依 (1F, 2F, 3F)；$\\Gamma_n=L_n/M_n$、$L_n=\\phi_n^T m\\{1\\}$、$M_n=\\phi_n^T m\\phi_n$；$S_{d,n}=S_{a,n}g/\\omega_n^2$。"),
 "SD-2020-3": ("""| 譜位移表的「ω」 | 是頻率 $f$（Hz），直接代入表列振態頻率，**不要乘 $2\\pi$**；以 Hz 代入時三段在 0.5、1.5 Hz 處連續（判讀 #1） | 當成 rad/s，先乘 $2\\pi$ |
| 振態 4 | 照錄考卷；一至四樓分量的正負號與其他振態不正交（等同 5F 符號誤植），疑為排版筆誤（判讀 #2） | 未發現；用全部振態驗算 $\\sum\\rho=100\\%$ 時對不起來 |
| 振態 1 一樓 | 照錄 0.160（正交規範化數列應為 0.170；判讀 #3） | — |
| 正規化 | 各振態分量平方和約為 1（等質量下即對 $m$ 正規化；考卷未明說，判讀 #4） | — |
| 樓層 | 樓層 1 最低、樓層 5 為頂樓（判讀 #5） | — |""",
  "$\\phi_{jn}$ 為第 $n$ 振態第 $j$ 樓分量；$\\Gamma_n=\\sum_j\\phi_{jn}$（等質量、正規化）；$S_{jk}$ 為 CQC 相關係數（考卷參考公式，$r=\\omega_k/\\omega_j$）。"),
 "SD-2021-1": ("""| 初始條件 | $t=0$ 時台車位移 0、台車**絕對**速度 0；構架 $\\dot d(0)=\\omega/2$ 屬給定激振（判讀 #1，使用者授權依建議確認） | 取相對構架速度為 0（台車初速 $\\omega/2$），絕對速度答案不同 |
| $x$ | 考卷未標量測基準；本解取台車絕對位移（判讀 #2） | 把 $x$ 當相對位移卻用絕對位移寫彈簧力 |
| 彈簧 | 兩根 $k$ 都接構架內壁，彈簧力 $=-2k(x-d)$（判讀 #5） | 只算一根、或右彈簧力方向相反而互相抵消 |
| 激振頻率 | $d(t)$ 的圓頻率為 $\\omega/2$，$\\omega$ 即㈡所求自然頻率（頻率比 1/2；判讀 #6） | 把 $\\omega$ 當成另給的激振頻率 |
| 阻尼 | 無（判讀 #7） | — |""",
  "$x$：台車絕對位移；$u=x-d$：台車相對構架位移；$\\omega=\\sqrt{2k/m}$。"),
 "SD-2021-2": ("""| ㈡ 系統 | 與㈠同一系統：$\\omega_n=10$ rad/s、阻尼比取㈠結果、$m=10^4$ kg（判讀 #1） | 另設勁度 |
| 半正弦波 | $p(t)=100\\sin(\\pi t/0.1)$ kN，延時 0.1 s 為整個半波、峰值在 0.05 s（判讀 #2） | 0.1 s 當峰值時刻 |
| ㈠ 兩組數據 | 同一 $p_0$；$\\bar\\omega=0.1$ rad/s 近乎靜態（頻率比 0.01）、$\\bar\\omega=10$ rad/s 共振（判讀 #3） | — |
| 最大位移 | 載重期間與結束後自由振動全程的最大值（判讀 #4） | 只看載重期間 |""",
  "$\\omega_0=\\omega_n=10$ rad/s；$r=\\bar\\omega/\\omega_0$；$t_d=0.1$ s；$x_{st}=p_0/k$。"),
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
    t = t.rstrip("\n") + f"\n\n*修正日期：{D}（§1 改為指向題目正本{extra}）*\n"
    p.write_text(t, encoding="utf-8"); return True
if __name__ == "__main__":
    for q in IDS: print(q, "problem", confirm_problem(q), "sec1", rewrite_sec1(q))
