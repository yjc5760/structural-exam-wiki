#!/usr/bin/env python3
"""2026-11-16 SD-U1-2 組 U1-2-G1：解析 §1 改為指向題目正本（exam-problem-split 第 7 節第 4 步）。
只動 §1（「## 1.」到下一個「## 2.」之間）與頁尾加一行修正日期；其他節不動、答案不改。
可重複執行：§1 已是「題目（考卷原文見題目正本）」者略過。用法：在 repo 根目錄 python SD/scripts/fixes/2026-11-16_confirm_sec1_U1-2-G1.py"""
import os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "raw", "solutions")
HEAD = "## 1. 題目（考卷原文見題目正本）"
FOOT = "*修正日期：2026-11-16（§1 改為指向題目正本，重繪附圖 figs/{id}-fig-1-problem.svg{extra}）*"

def intro(i):
    return (f"> 考卷原文、公式／附表、附圖與判讀清單（已確認）見 [`{i}-problem.md`]({i}-problem.md)。"
            "本節只列解題時最容易讀錯的地方與本解使用的記號；題意以題目正本為準。")

NEW = {
"SD-2002-2": dict(alt="SD-2002-2 重繪題目附圖：簡支梁長 L（m, EI），左鉸右滾，跨中集中質量 M，右端軸向壓力 N",
  cap="重繪自考卷附圖，依題目正本判讀清單；本圖確認 M 在跨中、N 為作用於滾支承端的壓力。",
  rows=[("變位形狀","$\\psi(x)=\\sin(\\pi x/L)$，廣義座標取跨中撓度（判讀 #1；考卷只說「正弦函數」）","取 $\\sin(2\\pi x/L)$ 或其他正規化，㈢㈣不受影響但㈠㈡數值會差倍數"),
        ("一般勁度","含軸壓的幾何勁度折減（判讀 #2）","只算撓曲勁度 $\\pi^4EI/(2L^3)$，㈢㈣就無從求起"),
        ("$M$","跨中集中質量，只計平移慣性（判讀 #3）","把 $M$ 的重量當成額外軸力或計入轉動慣量"),
        ("軸力方向","壓力，作用於滾支承端（判讀 #5）","當成拉力，週期變短")],
  sym="$Z(t)$ 為跨中撓度；$m^*$、$k^*$ 為廣義質量、勁度；$N_{cr}$ 為臨界軸壓；$T_0$ 為 $N=0$ 時的週期。", pending=None, keep=None),
"SD-2003-4": dict(alt="SD-2003-4 重繪題目附圖：斜投影單層立體構架，正方形剛性樓版 a×a，D、A 柱 2I，B、C 柱 I，柱底固定；u1 為 C 點沿 DC 平移，u2 為 B 點、u3 為 A 點沿 DA 方向平移",
  cap="重繪自考卷附圖，依題目正本判讀清單；本圖攔下的判讀錯誤：u1、u2、u3 是三個角點的平移（C、B、A），不是質心 x、y 平移與扭轉角。",
  rows=[("自由度","$u_1$＝C 點沿 DC（$x$）平移、$u_2$＝B 點沿 CB（$y$）平移、$u_3$＝A 點沿 DA（$y$）平移（判讀 #4–#6）","本庫舊解 §1：$u_1$、$u_2$ 為質心 $x$、$y$ 平移，$u_3$ 為繞鉛直軸的扭轉角"),
        ("柱端","柱底固定、柱頂與剛性樓版剛接，$12EI_i/h^3$（判讀 #1，定案）","柱頂鉸接（係數 3）"),
        ("粗黑線 DC、CB","立體圖前緣強調，樓版整體剛性（判讀 #2）","當成較剛的梁、其餘邊可變形"),
        ("地震方向","沿 D→B 對角線（判讀 #8）","沿 DC 或 CB 單一方向")],
  sym="$k=12EI/h^3$（單根 $I$ 柱的側向勁度）；平面座標原點可取樓版中心，$x$ 沿 DC、$y$ 沿 DA。",
  pending="依題目正本的角點自由度，第二行係數與 $\\mathbf{e}$ 會與本解 §3–§5 不同（本解建立在質心 $x$、$y$、扭轉角的自由度上）；本題已列入階段 C 勘誤，§2 以下暫未改寫。", keep=None),
"SD-2004-3": dict(alt="SD-2004-3 重繪題目附圖：簡支梁 AB（m, EI，長 L），E 在 x=L/4，鉛直剛性連桿 EF 兩端鉸接；剛性桿 CD 長 L/2、質量 m0/長度，C 端鉸支承位於 A 正上方、D 端自由",
  cap="重繪自考卷附圖，依題目正本判讀清單；本圖攔下的判讀錯誤：C 端是鉸支承，CD 繞 C 轉動（F 在 CD 中點），不是整根平移。",
  rows=[("CD 的運動","C 端鉸支承、D 端自由，CD 繞 C 轉動；F 距 C 為 $L/4$（判讀 #1、#2、#4）","本庫舊解 §1、§4：CD 整根隨 F 鉛直平移（漏看 C 的鉸支承）"),
        ("EF","兩端鉸接的剛性無質量連桿，$v_F=v_E=\\phi(L/4)Z$（判讀 #3）","—"),
        ("勁度來源","只有 AB 梁撓曲（判讀 #9）","把 CD、EF 算入勁度")],
  sym="$Z(t)$ 為 AB 跨中撓度；$\\phi(x)=\\sin(\\pi x/L)$；$m^*$、$k^*$ 為廣義質量、勁度。",
  pending="依題目正本，CD 繞 C 轉動時 CD 對廣義質量的貢獻與本解 §2–§4（以整根平移計算）不同；本題已列入階段 C 勘誤，§2 以下暫未改寫。", keep=None),
"SD-2004-4": dict(alt="SD-2004-4 重繪題目附圖：倒 L 形構架，柱底固定；m1 在高 h1、m2 在柱頂高 h2，水平梁至 m3（距柱 x3）；u1 在 m1 向右、u2 在 m3 向右、u3 在 m3 向下；h1、h2 皆由柱底量起",
  cap="重繪自考卷附圖，依題目正本判讀清單；本圖攔下的判讀錯誤：h2 是柱底到 m2 的全高（不是 m1 到 m2 的段長），且 u2 同時是 m2 的水平位移。",
  rows=[("$h_2$","柱底量至 $m_2$ 的全高（判讀 #6）","當成 $m_1$ 到 $m_2$ 的段長，$\\{l_\\theta\\}$ 第二項寫成 $h_1+h_2$（本庫 2026-08-22 已勘誤）"),
        ("$u_2$","$m_2$、$m_3$ 共同的水平位移（梁軸向剛性；判讀 #1）","只給 $m_3$，質量矩陣漏掉 $m_2$"),
        ("轉動中心","柱底支承點，順時鐘為正（判讀 #2、#8）","—"),
        ("質量","集中質量，不計轉動慣量（判讀 #3）","—")],
  sym="$\\{l_x\\}$、$\\{l_\\theta\\}$ 為支承單位平移、單位轉角引起的各自由度剛體位移。", pending=None,
  keep=("![SD-2004-4 幾何重繪", "### 判讀圖解（解析自繪）")),
"SD-2009-1": dict(alt="SD-2009-1 重繪題目附圖：均佈懸臂柱高 L，柱底固定、柱頂自由，x 自柱底向上；均佈側向荷重 p(t) 沿全高向右；虛線為給定形狀 ψ(x)，柱頂位移 Z(t)",
  cap="重繪自考卷附圖，依題目正本判讀清單；柱中段向左的箭頭是 m̄ 標註的引線，不是載重。",
  rows=[("柱中段向左箭頭","「m̄＝質量/長度」的引線（判讀 #1）","當成反向集中力"),
        ("$Z(t)$","柱頂側移，$\\Psi(L)=1$（判讀 #4）","—"),
        ("形狀函數","$\\Psi(x)=(x/L)^2\\,(3/2-x/(2L))$（判讀 #5）","把 $x/2L$ 讀成 $(x/2)L$"),
        ("單位","考卷全為符號、未給單位","本庫舊 §1 圖說寫 $\\bar m$（kg/m），屬加字，不影響答案")],
  sym="$\\bar m$、$EI$、$\\bar p(t)$ 為均佈質量、撓曲勁度、荷重；$m^*$、$k^*$、$p^*(t)$ 為廣義質量、勁度、荷重。", pending=None, keep=None),
}

def build(i, d, old):
    out = [HEAD, "", intro(i), "", f"![{d['alt']}](figs/{i}-fig-1-problem.svg)", f"*{d['cap']}*", ""]
    if d["pending"]:
        out += [f"> ⚠️ **題意與本解不符（待階段 C 勘誤）：** {d['pending']}", ""]
    if d["keep"]:
        key, title = d["keep"]
        m = re.search(r"(!\[" + re.escape(key[2:]) + r".*?\n\n\*圖 1[^\n]*)", old, re.S)
        assert m, (i, "keep fig")
        out += [title, "", m.group(1), ""]
    out += ["### 常見誤讀", "", "| 項目 | 正確判讀 | 常見誤讀 |", "|------|---------|---------|"]
    out += [f"| {a} | {b} | {c} |" for a, b, c in d["rows"]]
    out += ["", f"**本解記號：** {d['sym']}", "", "---", "", ""]
    return "\n".join(out)

for i, d in NEW.items():
    p = os.path.join(ROOT, i, f"{i}.md"); s = open(p, encoding="utf-8").read()
    if HEAD in s: print(i, "略過（已處理）"); continue
    m = re.search(r"^## 1\..*?(?=^## 2\.)", s, re.S | re.M); assert m, i
    old = m.group(0)
    prob = open(os.path.join(ROOT, i, f"{i}-problem.md"), encoding="utf-8").read()
    assert "已確認" in prob
    for png in set(re.findall(r"\(([^()]*?\.png)\)", old)):
        assert os.path.basename(png) in prob, (i, png)
    for svg in re.findall(r"\((figs/[^()]*?\.svg)\)", old):
        assert d["keep"] and svg in build(i, d, old), (i, svg)
    assert os.path.exists(os.path.join(ROOT, i, "figs", f"{i}-fig-1-problem.svg"))
    s = s[:m.start()] + build(i, d, old) + s[m.end():]
    extra = "；§1 標註題意與本解不符，待階段 C 勘誤" if d["pending"] else ""
    s = s.rstrip("\n") + "\n\n" + FOOT.format(id=i, extra=extra) + "\n"
    open(p, "w", encoding="utf-8").write(s); print(i, "OK")
