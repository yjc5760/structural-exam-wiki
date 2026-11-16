#!/usr/bin/env python3
"""SD-U1-2 組 U1-2-G2（SD-2010-1、2011-3、2013-3、2016-2）關卡一確認後：解析 §1 改為指向題目正本。
problem.md 已於建立時直接寫成「已確認」（2026-11-16 使用者授權依 Claude 建議）；本檔只檢查其狀態。
索引 problemStatus 由總控統一寫入（本檔不改 question_index.json）。只動 §1 與頁尾。
可重複執行（已處理者略過）。用法：python3 <本檔> <SD 科目資料夾>"""
import sys, re, os
from pathlib import Path
SD = Path(sys.argv[1]); D = "2026-11-16"
IDS = ["SD-2010-1", "SD-2011-3", "SD-2013-3", "SD-2016-2"]
REDRAW = {"SD-2010-1", "SD-2013-3", "SD-2016-2"}
FIGCAP = {
 "SD-2010-1": ("倒單擺，B 端鉸支承在下、剛性無質量桿 BA 長 L，A 端集中質量 m；水平彈簧 k 左端接牆、右端接 m；θ 為桿與通過 B 的鉛垂線夾角",
               "鉸在下、質量在上（倒單擺），重力為傾覆作用；彈簧水平，伸縮量為 m 的水平位移"),
 "SD-2013-3": ("左端固定的均勻懸臂梁，長 L、EI、單位長度質量 m；重量 W 的重量塊位於中點 L/2",
               "重量塊在中點而非自由端；W 是重量（質量 W/g）"),
 "SD-2016-2": ("兩支剛性梁各長 l、總質量 m；左梁左端鉸支，中點與右端各一根彈簧 k 接頂部固定面，右端再以彈簧 k 向下接右梁左端；右梁中點一根彈簧 k 接頂部固定面，右端鉸支",
               "左梁右端一點兩簧（上方接固定面、下方接右梁），全系統共四根彈簧"),
}
SEC1 = {
 "SD-2010-1": ("""| 重力 | 計入 $mg$；質量在鉸 $B$ 正上方，重力是傾覆（負勁度）作用（判讀 #1） | 題文沒寫重力就略去 $mg$，㈠穩定條件變成只要 $k>0$ |
| 系統型式 | 倒單擺：$B$ 鉸在下、$A$ 端質量在上（判讀 #3、#4） | 看成一般下垂單擺，重力變成恢復力 |
| 彈簧 | 水平，左端固定於牆；$\\theta$ 甚小時伸縮量 $\\approx L\\theta$，對 $B$ 的力臂 $\\approx L$（判讀 #2） | 力臂與重力的水平偏距互換 |
| 傾斜方向 | 考卷圖上桿向左（彈簧側）傾斜，屬示意；本解取向右為正，正負號慣例不影響結果（判讀 #7） | — |
| 質量 | 集中質量，不計轉動慣量；桿不計質量（判讀 #5、#6） | 加入桿件質量 |""",
  "$\\theta$：桿 $AB$ 偏離鉛垂線的角度（本解向右為正）；$k_{\\text{eff}}=kL^2-mgL$；$\\omega$：振動圓頻率（rad/s）。"),
 "SD-2011-3": ("""| 起始狀態 | $t=0$ 時電梯靜止於靜平衡位置，$u(0)=0$、$\\dot u(0)=0$；彈簧上端自 $t=0$ 起以等速 $v$ 上升，上端位移 $vt$（判讀 #1，使用者授權依建議確認） | 把上端速度 $v$ 當成電梯初速 |
| 重力 | $u$ 自靜平衡位置量起，$mg$ 與彈簧靜伸長 $k\\delta_{st}$ 抵銷，不出現在運動方程式（判讀 #2） | 方程式右端多寫 $mg$ |
| 彈簧變形 | 上端位移減下端位移：$vt-u$（加靜伸長） | 只寫 $u$，漏掉上端運動 |
| $u$ | 電梯向上的絕對位移（判讀 #3） | 當成相對彈簧上端的位移 |
| 阻尼 | 無（判讀 #5） | — |""",
  "$u$：電梯自起始靜止位置向上的位移；$\\omega_0=\\sqrt{k/m}$；$\\delta_{st}=mg/k$。"),
 "SD-2013-3": ("""| 重量塊位置 | 在中點 $x=L/2$，不是自由端（判讀 #2、#5） | 放在自由端套 $3EI/L^3$ |
| $W$ | 重量，質量為 $W/g$（判讀 #3） | 直接把 $W$ 當質量 |
| 梁質量 | 計入梁本身均佈質量 $m$（判讀 #6） | 只算集中質量，忽略梁質量 |
| 分析方法 | 考卷未指定；Rayleigh 法須註明所用形狀函數（判讀 #1，使用者授權依建議確認） | 未說明形狀函數就給近似值 |
| 重量塊尺寸 | 視為質點，不計轉動慣量與寬度（判讀 #2） | — |""",
  "$x$ 自固定端量起；$\\varphi(x)$：假設形狀函數；$W/g$：重量塊質量；$\\omega$：基本振動圓頻率（rad/s）。"),
 "SD-2016-2": ("""| 彈簧數量 | 共四根：左梁中點、左梁右端各一根接頂部固定面，左梁右端另一根向下接右梁左端（連接彈簧），右梁中點一根接頂部固定面（判讀 #5–#9） | 漏掉左梁右端上方的彈簧，$K_{11}$ 由 $9kl^2/4$ 誤為 $5kl^2/4$，得出 $\\omega_2=3\\omega_1$ 這種漂亮但錯誤的答案 |
| 左梁右端 | 一點兩簧：上方接固定面、下方接右梁左端，兩端點在同一鉛垂線上（判讀 #7） | 以為結構左右對稱、$K_{11}=K_{22}$ |
| 支承 | 左梁左端、右梁右端各為鉸支承（判讀 #3、#4、#10） | — |
| 自由度 | 考卷未指定；本解取兩梁各繞鉸的轉角（判讀 #1，使用者授權依建議確認），矩陣隨自由度選法而異、頻率不變 | 以為矩陣只有一種正確形式 |
| 質量 | 每支梁總質量 $m$ 均勻分布，繞端點鉸的轉動慣量 $ml^2/3$ | 當成集中於梁端或梁中點 |""",
  "$\\theta_1$：左梁（上梁）繞左端鉸 A 的轉角，正＝右端向下；$\\theta_2$：右梁（下梁）繞右端鉸 D 的轉角，正＝左端向下；B 為左梁右端、C 為右梁左端。"),
}
SEC1_PAT = [r"^## 1\. 原始題目重述.*?(?=^---\s*\n\s*## 2\.|^## 2\.)"]
def check_problem(qid):
    t = (SD/f"raw/solutions/{qid}/{qid}-problem.md").read_text(encoding="utf-8")
    assert "判讀狀態 | **已確認**" in t, qid
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
        assert (SD/f"raw/solutions/{qid}/figs/{qid}-fig-1-problem.svg").exists()
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
    for q in IDS:
        check_problem(q); print(q, "sec1", rewrite_sec1(q))
