#!/usr/bin/env python3
"""SD-U3-2 組 U3-2-G1（SD-2004-2、2005-1、2006-4、2008-4）關卡一確認後：解析 §1 改為指向題目正本。
題目正本建立時即已寫為「已確認」（2026-11-16 使用者授權依 Claude 建議），本腳本只檢查它，不改 problem.md。
不改 question_index.json（problemStatus 由總控統一寫入）。只動 §1 與頁尾一行修正日期。可重複執行（已處理者略過）。
用法：python3 <本檔> <SD 科目資料夾>"""
import sys, re, os
from pathlib import Path
SD = Path(sys.argv[1]); D = "2026-11-16"
IDS = ["SD-2004-2", "SD-2005-1", "SD-2006-4", "SD-2008-4"]
REDRAW = {"SD-2004-2"}
FIGCAP = {
 "SD-2004-2": ("左側為立在小滾輪上的直立桿（地面運動輸入端，u_g(t) 向右），彈簧 k_b 接隔震層方塊 m_b，彈簧 k 再接原結構方塊 m；兩方塊各有兩輪；x1(t)、x2(t) 向右；圖上無阻尼器",
               "x1、x2 為絕對位移，左側直立桿是隨地表移動的輸入端（不是固定牆）；考卷沒有阻尼器"),
}
SEC1 = {
 "SD-2004-2": ("""| 座標 | $x_1$、$x_2$ 為絕對位移（判讀 #8）；相對位移 $v_2=x_2-u_g$ 是推導時自訂的記號（判讀 #1） | 把 $x_2$ 當相對位移，漏掉地面輸入項 |
| 左側直立桿 | 隨地表移動的輸入端，位移 $u_g(t)$（判讀 #2） | 當成固定牆，$k_b$ 恢復力寫成 $-k_b x_1$ |
| $m_b=0$ | 隔震層方程式變成靜力平衡（束制條件），用來消去 $x_1$（判讀 #5） | 直接刪掉該式，或只取 $k$ 或 $k_b$ 當勁度 |
| 彈簧連接 | $k_b$ 接地面端與 $m_b$、$k$ 接 $m_b$ 與 $m$，兩者串聯（判讀 #3、#4） | 當成並聯 |
| 阻尼 | 考卷沒有給（圖上無阻尼器；判讀 #11）；舊圖說「底部為滑動支承」實為輪子（判讀 #7） | 自行加入隔震阻尼寫進主線 |""",
  "$v_2=x_2-u_g$ 為原結構質量相對地面位移；$k_{eq}=kk_b/(k+k_b)$；$T$ 為自然振動周期。"),
 "SD-2005-1": ("""| ㈠「那一類」 | 考卷沒有指定分類法；本解以位移相依型（遲滯型、金屬降伏）作答，並對照速度相依型（判讀 #1） | 與速度型的黏滯阻尼器混淆 |
| ㈣「發揮最大效果」 | 指 BRB 在構架中的設計與配置（勁度、降伏強度、配置位置、接合與周邊構材容量設計）（判讀 #2） | 只寫「適當配置」 |
| 題型 | 四小題皆為論述，沒有數值、沒有附圖（判讀 #3、#4） | — |""",
  "BRB＝挫屈拘束支撐（內芯＋無黏結層＋外管）；$P_y$ 為內芯降伏軸力。"),
 "SD-2006-4": ("""| 「減震」範圍 | 考卷沒有指定外力；本解說明 TMD 抑制主結構（基本振態）反應的原理，風與地震皆適用（判讀 #1） | 只談地震或只談風 |
| 「阻尼器選用的質量」 | TMD 附加質量，以質量比 $\\mu=m_d/M$ 表示（判讀 #3） | — |
| 配分 | 減震原理與質量過輕缺點兩部分合計 25 分，不分小題（判讀 #2） | — |""",
  "$M$、$K$、$\\omega_n$ 為主結構質量、勁度、頻率；$m_d$、$k_d$、$\\omega_d$ 為 TMD；$\\mu=m_d/M$；$f=\\omega_d/\\omega_n$；$\\xi_d$ 為 TMD 阻尼比。"),
 "SD-2008-4": ("""| 公式分組 | 考卷 $\\sqrt{W/K_{eD}\\,g}$ 讀為 $\\sqrt{W/(K_{eD}g)}$（量綱為 s²；判讀 #1） | 讀成 $\\sqrt{(W/K_{eD})\\,g}$ |
| $W$ | 隔震系統上方之結構總靜載重（重量，不是質量），$m=W/g$ | 把 $W$ 當質量 |
| 規範版本 | 考卷指當年規範；本庫主線用現行建築物耐震設計規範及解說，該式未變（判讀 #2） | — |
| 同頁曲線圖 | 屬第三題，不屬本題（題目正本 §3） | 把 MF 曲線當本題資料 |""",
  "$W$ 為總靜載重、$m=W/g$；$K_{eD}$ 為設計位移下有效（割線）勁度；$T_{eD}$ 為有效振動週期；$D_D$ 為設計位移；$B_D$ 為阻尼修正係數。"),
}
SEC1_PAT = [r"^## 1\. 原始題目重述.*?(?=^---\s*\n\s*## 2\.|^## 2\.)",
            r"^## 1\. 題目重述.*?(?=^---\s*\n\s*## 2\.|^## 2\.)"]
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
        assert (SD/f"raw/solutions/{qid}/figs/{qid}-fig-1-problem.svg").exists(), qid
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
