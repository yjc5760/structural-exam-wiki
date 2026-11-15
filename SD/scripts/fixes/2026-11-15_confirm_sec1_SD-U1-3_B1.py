#!/usr/bin/env python3
"""SD-U1-3 批 1（2002–2008，12 題）關卡一確認後：problem.md 凍結、索引 problemStatus、解析 §1 改為指向題目正本。
可重複執行（已處理者略過）。用法：python3 <本檔> <SD 科目資料夾>
2026-11-15 使用者授權依 Claude 建議確認（pipeline 一次做完，關卡一不停）。"""
import sys, re, json, os
from pathlib import Path
SD = Path(sys.argv[1]); D = "2026-11-15"
IDS = ["SD-2002-1","SD-2003-2","SD-2003-3","SD-2003-5","SD-2004-5","SD-2005-2","SD-2005-4","SD-2006-2","SD-2007-2","SD-2007-3","SD-2008-1","SD-2008-3"]
REDRAW = {"SD-2002-1","SD-2003-2","SD-2003-5","SD-2004-5","SD-2005-2","SD-2005-4","SD-2007-2","SD-2007-3","SD-2008-1"}
CHOICE = {"SD-2003-2": "影響答案項目定案：#1 峰值時刻採 0.02 s（下降段為同一直線，由 ta、tb、−500N 推得）",
          "SD-2005-4": "影響答案形式項目定案：#1 主解採圖上黏滯阻尼器 c，題文「遲滯阻尼」型式於 §5 附註"}
FIGCAP = {
 "SD-2002-1": ("基座灰塊以旋轉彈簧 kθ 繞基座質心轉動，兩柱各 k，樓版 M2、I2；L＝3 m 量自基座質心至樓版質心", "L 是兩個質心之間的距離（題文定義），考卷圖上的尺寸線下端畫在基座厚度內，不是地表"),
 "SD-2003-2": ("外力歷時：0→0.02 s 升至 2000 N，同一直線下降於 ta＝0.10 s 過零、tb＝0.12 s 達 −500 N，維持到 tc＝0.20 s，td＝0.25 s 回零", "ta 是零交點而不是峰值時刻；峰值時刻考卷沒標，由下降直線推得 0.02 s"),
 "SD-2003-5": ("五層剪力屋架，每層兩柱各 ki/2，右側列出 ki 與層間變位 δi", "ki 是樓層勁度（兩柱合計），δi 是層間變位不是樓層位移"),
 "SD-2004-5": ("三層剪力屋架，樓高各 3 m，由下而上 5000、4000、3000 kg，層勁度皆 4×10⁶ N/m", "頂層是 3000 kg，質量由下往上遞減"),
 "SD-2005-2": ("一樓三柱：左右柱底固定、中柱底鉸支承；二樓只在右跨兩柱；一樓樓版 35000＋40000 kg、二樓 20000 kg；樓高 4.2 m、3.2 m", "中柱底是鉸支承，側向勁度為 3EI/h³ 而非 12EI/h³"),
 "SD-2005-4": ("剛體 (M−m) 內含偏心質量 m（偏心 e、角度 Ωt 由水平量起），下方兩彈簧各 k/2 與阻尼器 c 接地，u 向上", "總質量 M 已含馬達 m；圖上 c 是黏滯阻尼器符號"),
 "SD-2007-2": ("天花板—k1—m1—k2—m2 串接，兩質量各受向下 Fi cos ωf t，y1、y2 向下為正", "k2 連在兩質量之間，不是接地"),
 "SD-2007-3": ("牆以彈簧 k、阻尼器 c 並聯連到 m，外力 p0 sin Ωt 作用在 m，u 向右，R 為支承反力", "外力作用在質量上，不是支承運動；R 是反力"),
 "SD-2008-1": ("兩層剪力屋架，每層 m，層勁度皆 k；u1 在頂層、u2 在下層", "u1 是頂層，正規化「u1 分量為 1」是頂層為 1"),
}
SEC1 = {
 "SD-2002-1": ("""| 尺寸 $L$ | 樓版質心至基座質心 3 m（題文定義；判讀 #3） | 「地表至樓版」高度（本庫 2026-08-22 舊註） |
| $I_2$ | 對**樓版質心**的轉動慣量；基座轉動時樓版隨之轉動 | 對基座質心 |
| 柱勁度 | 每根 $k$，兩根並聯共 $2k$（判讀 #2） | 把 $k$ 當成整層勁度 |
| 基座 | 只能繞基座質心轉動，不平移 | 基座可水平平移 |""",
  "基座轉角 $\\theta_1$（樓版轉角 $\\theta_2=\\theta_1$）、樓版相對柱頂側移 $u_2$；Ton 為質量（1000 kg）。"),
 "SD-2003-2": ("""| 峰值時刻 | 考卷未標；下降段為同一直線（斜率 $-500/0.02=-25000$ N/s），峰值在 $t=0.1-2000/25000=0.02$ s（判讀 #1，使用者授權依建議確認） | 把 $t_a=0.1$ s 當峰值時刻（本庫舊解 §1、§4 的讀法） |
| $t_a$ | 力的零交點 0.1 s | 峰值結束時刻 |
| $t_a\\to t_b$ | 由 0 直線降到 −500 N（與上一段同一直線） | 由 2000 N 陡降到 −500 N |
| 所求 | 全歷時（含 $t>t_d$ 自由振動）的最大位移 | 只看強迫段 |""",
  "$m=100$ kg、$k=100$ N/m、$\\xi=0.30$、$\\omega_n=1$ rad/s；$x(t)$ 為位移。"),
 "SD-2003-3": ("""| 錨定振態 | 第 1、第 **3** 振態（$T_1=2$ s、$T_3=1$ s 皆 5%） | 第 1、第 2 振態 |
| 給的量 | 週期 $T$（秒），推導要寫成 $\\xi$–$T$ 關係 | 直接把 $T$ 代入 $\\omega$ 的位置 |
| 所求 | 優點、推導、$\\xi_2$（$T_2=1.5$ s） | 只算數值 |""",
  "雷利阻尼 $\\mathbf{C}=a_0\\mathbf{M}+a_1\\mathbf{K}$，$\\xi_n=\\dfrac{a_0}{2\\omega_n}+\\dfrac{a_1\\omega_n}{2}$，$\\omega_n=2\\pi/T_n$。"),
 "SD-2003-5": ("""| $k_i$ | 第 $i$ 層樓層勁度（圖上兩柱各 $k_i/2$） | 每根柱勁度 |
| $\\delta_i$ | **層間**變位（題文加引號） | 樓層絕對位移 |
| $\\delta_5$ | 3.333 mm（$\\approx 10/3$） | — |""",
  "樓層位移 $u_i=\\sum_{j\\le i}\\delta_j$；側力 $F_i$；各層 $m=5000$ kg。"),
 "SD-2004-5": ("""| 樓版質量 | 由下而上 $m_1=5000$、$m_2=4000$、$m_3=3000$ kg | 上下排反 |
| $T_2$ | 0.162 s 為題給，照用 | 自行重算 |
| 譜加速度 | $S_a=C(T)\\times0.2g$ | 直接用 $C$ 當 $S_a$ |""",
  "$\\phi_1$、$\\phi_2$ 照題給（頂層分量 1.0、−0.937）；$\\Gamma_n$ 參與因子。"),
 "SD-2005-2": ("""| 中柱底 | **鉸支承**（判讀 #2）：一樓中柱側向勁度 $3EI/h^3$ | 三柱皆固定、一律 $12EI/h^3$（本庫舊解 §1、§4 的讀法） |
| 二樓 | 只在右跨，兩柱（中柱線、右柱線），柱頂底皆固定（剪力屋架） | 三柱 |
| 一樓質量 | $35000+40000=75000$ kg | 只取一跨 |
| $E$ 單位 | kgf/cm²（重力單位，換 SI 乘 $g$） | 直接當 N/cm² |""",
  "$y_1$、$y_2$ 為一、二樓樓版側移；$k_1$、$k_2$ 為一、二樓樓層勁度；$h_1=4.2$ m、$h_2=3.2$ m。"),
 "SD-2005-4": ("""| 阻尼型式 | 題文寫「遲滯阻尼」、圖上畫黏滯阻尼器 $c$；主解採黏滯 $c\\dot u$，遲滯型式另於 §5 說明（判讀 #1，使用者授權依建議確認） | 只依題文或只依圖而未說明 |
| 質量 | 總質量 $M$ 已含馬達 $m$（方框標 $M-m$） | $M+m$ |
| 偏心角 | $\\Omega t$ 由水平線量起；垂直分量為 $e\\sin\\Omega t$ | 用 $\\cos$ |
| 位移 | $u$ 向上為正 | — |""",
  "$u$ 垂直位移（向上正）；$\\omega_n=\\sqrt{k/M}$、$r=\\Omega/\\omega_n$、$\\xi=c/(2M\\omega_n)$。"),
 "SD-2006-2": ("""| 等效橫力向量 | 分量順序（一樓, 二樓）：第一振態 11358/18377＝0.618、第二振態 3997/(−2470)＝−1.618 | 上下顛倒 |
| ㈣ | 不加頂層集中力 $F_t$；基底剪力取同一基底振動結果 | 另外加 $F_t$ |
| 樓高 | 考卷未給，㈣依等樓高解讀 | 自行假設不等樓高 |""",
  "$m=2000$ kg、$k=4\\times10^6$ N/m（兩層相同）；$V_1$、$V_2$ 為一、二樓樓層剪力。"),
 "SD-2007-2": ("""| 串接 | 天花板—$k_1$—$m_1$—$k_2$—$m_2$ | $k_2$ 接地 |
| 正向 | $y_1$、$y_2$、外力皆向下為正 | 力與位移方向不一致 |
| 阻尼 | 無 | — |""",
  "$y_1$、$y_2$ 自靜平衡位置量起；$\\omega_f$ 為外力頻率。"),
 "SD-2007-3": ("""| 外力 | 作用在質量上的 $p_0\\sin\\Omega t$ | 支承運動 |
| ㈢ | 考卷沒有給 $\\Omega$ 數值，答案以 $\\Omega$ 表示 | 自行代入 ㈣ 的 $\\Omega=2\\pi$ |
| ㈢㈣ | 不考慮阻尼 | — |
| $R$ | 支承反力，各小題未問 | 當成外力 |""",
  "$r=\\Omega/\\omega_n$、$\\omega_n=\\sqrt{k/m}$；$u_{max}$、$\\ddot u_{max}$ 為穩態振幅。"),
 "SD-2008-1": ("""| 自由度編號 | **$u_1$ 在頂層、$u_2$ 在下層** | 由下往上編號 |
| 正規化 | 「$u_1$ 分量為 1」＝頂層分量為 1 | 下層為 1 |
| 週期 | $T_1=0.197$ s、$T_2=0.0752$ s 為系統識別結果，照用 | — |""",
  "$m=1500$ kg、樓層勁度 $k=p\\times10^q$ N/m；$[C]$ 為阻尼係數矩陣（依 $u_1$、$u_2$ 順序）。"),
 "SD-2008-3": ("""| 橫軸 | $T_n/T_f$（＝$\\Omega/\\omega_n$） | $T_f/T_n$ |
| ㈠計算 | 以考卷給的 MF 公式計算（圖只作示意） | 由圖目測 |
| 條件 | $T_n$ 不變、$\\xi$ 0.02→0.20；兩個工況 1 與 1.5 | — |""",
  "$MF(r,\\xi)$，$r=T_n/T_f$。"),
}
def confirm_problem(qid):
    p = SD/f"raw/solutions/{qid}/{qid}-problem.md"; t = p.read_text(encoding="utf-8")
    if "判讀狀態 | **已確認**" in t: return False
    note = f"{D} 使用者授權依 Claude 建議確認" + (f"；{CHOICE[qid]}" if qid in CHOICE else "")
    t2 = re.sub(r"判讀狀態 \| \*\*待確認\*\*（", f"判讀狀態 | **已確認**（{note}。原轉錄：", t, count=1)
    assert t2 != t
    t2 = t2.replace("（影響答案，請確認）", "（影響答案）").replace("（影響答案形式，請確認）", "（影響答案形式）")
    t2 = re.sub(r"(\| 不確定（[^|]*?)\s\|\n", lambda m: m.group(1) + "；使用者授權依建議確認 |\n", t2)
    t2 = t2.rstrip("\n") + f"\n*確認：{D} 使用者授權依 Claude 建議確認（SD-U1-3 題目正本推廣・批 1，關卡一）*\n"
    p.write_text(t2, encoding="utf-8"); return True
def rewrite_sec1(qid):
    p = SD/f"raw/solutions/{qid}/{qid}.md"; t = p.read_text(encoding="utf-8")
    if "## 1. 題目（考卷原文見題目正本）" in t: return False
    m = re.search(r"^## 1\. 原始題目重述.*?(?=^---\s*\n\s*## 2\.|^## 2\.)", t, re.S | re.M); assert m, qid
    old = m.group(0)
    prob = (SD/f"raw/solutions/{qid}/{qid}-problem.md").read_text(encoding="utf-8")
    for png in re.findall(r"\(([^)]*?\.png)\)", old):
        if os.path.exists(SD/f"raw/solutions/{qid}/{png}"): assert png in prob, (qid, png)
    svgs = [s for s in re.findall(r"\((figs/[^)]*?\.svg)\)", old)]
    rows, note = SEC1[qid]
    s = ["## 1. 題目（考卷原文見題目正本）", "",
         f"> 考卷原文、公式／附表、附圖與判讀清單（已確認）見 [`{qid}-problem.md`]({qid}-problem.md)。本節只列解題時最容易讀錯的地方與本解使用的記號；題意以題目正本為準。", ""]
    if qid in REDRAW:
        alt, cap = FIGCAP[qid]
        s += [f"![{qid} 重繪題目附圖：{alt}](figs/{qid}-fig-1-problem.svg)", f"*重繪自考卷附圖，依題目正本判讀清單；本圖攔下的判讀錯誤：{cap}。*", ""]
    s += ["### 常見誤讀", "", "| 項目 | 正確判讀 | 常見誤讀 |", "|------|---------|---------|", rows, "", f"**本解記號：** {note}", ""]
    if svgs:
        s += ["### 判讀圖解（解析自繪）", ""] + [f"![{qid} 解析自繪圖]({x})" for x in svgs] + [""]
    t = t.replace(old, "\n".join(s) + "\n")
    extra = f"，重繪附圖 figs/{qid}-fig-1-problem.svg" if qid in REDRAW else ""
    if qid == "SD-2008-3": extra = "；移除失效的附圖連結 SD-2008-3-chart-1.png（考卷關係圖見題目正本 SD-2008-3-fig-1.png）"
    if qid == "SD-2002-1": extra += "；刪除 §1「L 標於地表至樓版」模型化說明（題文定義 L 為兩質心距離）"
    t = t.rstrip("\n") + f"\n\n*修正日期：{D}（§1 改為指向題目正本{extra}）*\n"
    p.write_text(t, encoding="utf-8"); return True
def index():
    p = SD/"raw/json/question_index.json"; raw = p.read_text(encoding="utf-8"); q = json.loads(raw)
    if "tagSystem" not in q:
        raw = raw.replace('  "questions": [', '  "tagSystem": {\n    "problemStatus": "題目正本 raw/solutions/<id>/<id>-problem.md 的判讀狀態：draft（待確認）／confirmed（使用者已確認）；欄位不存在＝尚未建立題目正本（SD 2026-11-15 起，SD-U1-3 批 1）"\n  },\n  "questions": [', 1)
    for qid in IDS:
        pat = re.compile(r'(\{\s*"moduleId": "%s",.*?"verificationStatus": "[^"]*")(,\s*"problemStatus": "[^"]*")?' % qid, re.S)
        m = pat.search(raw); assert m, qid
        ind = re.search(r'\n(\s*)"verificationStatus"', m.group(1)).group(1)
        raw = raw[:m.start()] + m.group(1) + f',\n{ind}"problemStatus": "confirmed"' + raw[m.end():]
    json.loads(raw); p.write_text(raw, encoding="utf-8")
if __name__ == "__main__":
    for q in IDS: print(q, "problem", confirm_problem(q), "sec1", rewrite_sec1(q))
    index(); print("index ok")
