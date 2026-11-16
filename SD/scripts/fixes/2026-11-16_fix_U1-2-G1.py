#!/usr/bin/env python3
"""2026-11-16 FIX-SD-U1-2-G1：SD-2003-4、SD-2004-3 解析勘誤（判讀錯誤），SD-2002-2 標頭主分類改合法 topicId（非勘誤）。
可重複執行（已處理者略過）；每個替換 assert 找得到。驗算腳本：2026-11-16_verify_SD-2003-4.py、2026-11-16_verify_SD-2004-3.py。
SD-2003-4 §2–§5 全文改寫，新內容讀自同目錄 2026-11-16_fix_U1-2-G1_SD-2003-4_body.md。"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SOL = os.path.join(HERE, "..", "..", "raw", "solutions")
def rd(i): return open(os.path.join(SOL, i, f"{i}.md"), encoding="utf-8").read()
def wr(i, s): open(os.path.join(SOL, i, f"{i}.md"), "w", encoding="utf-8").write(s)
def rep(s, a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a)); return s.replace(a, b)
def foot(s, line): return s.rstrip("\n") + "\n\n" + line + "\n"

# ---------- SD-2003-4 ----------
i = "SD-2003-4"; s = rd(i)
if "FIX-SD-U1-2-G1" not in s:
    s = rep(s, "**主分類：** `SD-U1` 結構動力學基礎", "**主分類：** `SD-U1-2` 運動方程式推導")
    s = re.sub(r"> ⚠️ \*\*題意與本解不符（待階段 C 勘誤）：\*\*[^\n]*\n\n", "", s, count=1)
    body = open(os.path.join(HERE, "2026-11-16_fix_U1-2-G1_SD-2003-4_body.md"), encoding="utf-8").read()
    m = re.search(r"^## 2\..*?(?=^\*修正日期)", s, re.S | re.M); assert m
    s = s[:m.start()] + body.rstrip("\n") + "\n\n" + s[m.end():]
    s = foot(s, "*修正日期：2026-11-16（FIX-SD-U1-2-G1 解析勘誤（判讀：自由度定義）：考卷 u1、u2、u3 為角點 C、B、A 的平移，舊解誤作質心 x、y 與扭轉角；k12、k22、k32 由 0、72EI/h³、−12EIa/h³ 改為 −36EI/h³、60EI/h³、−36EI/h³；m12、m22、m32 由 0、m、0 改為 −m/2、2m/3、−m/6；e 由 {1,1,0}/√2 改為 {1,1,1}/√2；§2–§5 全文改寫，舊值移 §5.2 對照；移除 §1 待勘誤警示；標頭主分類 SD-U1 改 SD-U1-2（非勘誤，依索引）。證據：2003 年第 2 頁第四題附圖（500 dpi，三個平移箭頭分別在 C、B、A）。驗證：scripts/fixes/2026-11-16_verify_SD-2003-4.py 能量法、座標轉換、平衡法三路一致，MISMATCHES: 0；與盲解比對一致）*")
    wr(i, s); print(i, "OK")
else: print(i, "略過")

# ---------- SD-2004-3 ----------
i = "SD-2004-3"; s = rd(i)
if "FIX-SD-U1-2-G1" not in s:
    s = re.sub(r"> ⚠️ \*\*題意與本解不符（待階段 C 勘誤）：\*\*[^\n]*\n\n", "", s, count=1)
    # §2
    s = rep(s, "3. 考查形函數的幾何傳遞：E 在 $x = L/4$，所以 CD 的運動幅度為 $\\phi(L/4) = \\sin(\\pi/4) = \\frac{\\sqrt{2}}{2}$",
               "3. 考查形函數的幾何傳遞與**支承判讀**：E 在 $x = L/4$，F 點位移為 $\\phi(L/4)Z=\\frac{\\sqrt{2}}{2}Z$；C 端是鉸支承，CD 繞 C 轉動 $\\theta=v_F/(L/4)$，D 端位移是 F 的兩倍")
    s = rep(s, "- ⚠ **CD 的廣義位移不是 $Z(t)$**，而是 $\\phi(L/4) \\cdot Z(t)$——因為 EF 為剛性，CD 的位移等於 E 點的梁撓度",
               "- ⚠ **CD 不是整根平移**：C 端為鉸支承（題目正本判讀 #1、#4），CD 繞 C 轉動，各點位移 $v(s)=s\\,\\theta$ 與距 C 的距離 $s$ 成正比；F 點（$s=L/4$）的位移才是 $\\phi(L/4)Z$")
    # §3 作戰計畫
    s = rep(s, "Step 1：確認幾何——CD 的位移 = φ(L/4)·Z(t)（透過剛性桿 EF 傳遞）",
               "Step 1：確認幾何——F 點位移 = φ(L/4)·Z(t)（透過剛性桿 EF 傳遞）；CD 繞 C 鉸轉動 θ = v_F/(L/4)")
    s = rep(s, "       m*_CD = m₀·(L/2)·[φ(L/4)]² = m₀·(L/2)·(1/2) = m₀L/4",
               "       m*_CD = I_C·(θ/Z)² = [m₀(L/2)³/3]·(2√2/L)² = m₀L/3")
    s = rep(s, "1. ⚠ **形函數傳遞**：EF 為剛性，E 點位移 = F 點位移。CD 為剛性水平桿，整根 CD 做同樣的垂直平移，位移幅度均為 $\\phi(L/4) = \\sin(\\pi/4) = \\sqrt{2}/2$",
               "1. ⚠ **形函數傳遞與支承**：EF 為剛性，E 點位移 = F 點位移 $=\\frac{\\sqrt2}{2}Z$。CD 的 C 端是鉸支承，CD 繞 C 轉動 $\\theta=\\frac{\\sqrt2 Z/2}{L/4}=\\frac{2\\sqrt2}{L}Z$，D 端位移 $\\sqrt2 Z$——**不是**整根平移")
    # §3.5
    s = rep(s, "$$\\text{Step 3：} \\quad m^*_{CD} = m_0 \\cdot \\frac{L}{2} \\cdot \\left[\\phi\\!\\left(\\frac{L}{4}\\right)\\right]^2 = m_0 \\cdot \\frac{L}{2} \\cdot \\frac{1}{2} = \\frac{m_0 L}{4}$$",
               "$$\\text{Step 3：} \\quad \\theta = \\frac{v_F}{L/4} = \\frac{2\\sqrt{2}}{L}Z,\\qquad m^*_{CD} = \\int_0^{L/2} m_0\\left(\\frac{s\\,\\theta}{Z}\\right)^2 ds = I_C\\left(\\frac{2\\sqrt2}{L}\\right)^2 = \\frac{m_0L^3}{24}\\cdot\\frac{8}{L^2} = \\frac{m_0 L}{3}$$")
    s = rep(s, "$$\\text{Step 4：} \\quad m^* = m^*_{AB} + m^*_{CD} = \\frac{mL}{2} + \\frac{m_0 L}{4}$$",
               "$$\\text{Step 4：} \\quad m^* = m^*_{AB} + m^*_{CD} = \\frac{mL}{2} + \\frac{m_0 L}{3}$$")
    s = rep(s, "| E 位置 | $x = L/4$ | EF 在梁上的連接點 |",
               "| E 位置 | $x = L/4$ | EF 在梁上的連接點 |\n| C 端 | 鉸支承（在 A 正上方） | CD 只能繞 C 轉動；F 距 C 為 $L/4$ |")
    s = rep(s, "| $v_{CD}$ | EF 剛性 → $v_{CD} = v_E = \\frac{\\sqrt{2}}{2}Z$（CD 整體平移） | |\n| CD 形函數幅值 | $\\phi_{CD} = \\sin(\\pi/4) = \\frac{\\sqrt{2}}{2}$ | |",
               "| $v_F$ | EF 剛性 → $v_F = v_E = \\frac{\\sqrt{2}}{2}Z$ | |\n| CD 轉角 | $\\theta = v_F/(L/4) = \\frac{2\\sqrt{2}}{L}Z$（C 為鉸支承） | ⚠ |\n| CD 上距 C 為 $s$ 的點 | $v(s) = s\\,\\theta$（D 端 $s=L/2$：$\\sqrt2 Z$） | |")
    s = rep(s, "| $m^*_{CD}$ | $m_0 \\cdot (L/2) \\cdot [\\sin(\\pi/4)]^2 = m_0 L/4$ | |",
               "| $I_C$ | $m_0(L/2)^3/3 = m_0L^3/24$（CD 對 C 的轉動慣量） | |\n| $m^*_{CD}$ | $I_C(2\\sqrt2/L)^2 = m_0 L/3$ | |")
    s = rep(s, "| 剛性桿的動力貢獻 | 剛性桿有質量（貢獻 $m^*$）但無彈性（不貢獻 $k^*$） | |",
               "| 剛性桿的動力貢獻 | 剛性桿有質量（貢獻 $m^*$）但無彈性（不貢獻 $k^*$）；繞固定鉸轉動的剛性桿，動能 $\\tfrac12 I_C\\dot\\theta^2$ | |")
    # §4 Step 1
    s = rep(s, "因 CD 為水平剛性桿，與 EF 在 F 點連接，CD 整體做**垂直平移**（無轉動），CD 上各點的垂直位移均為：\n\n$$v_{CD}(t) = \\frac{\\sqrt{2}}{2}\\, Z(t)$$\n\n> **策略註解：** CD 上任意一點的位移幅值（相對於廣義座標 $Z$）均為常數 $\\phi_{CD} = \\sqrt{2}/2$。",
               "CD 為剛性桿，C 端為**鉸支承**（題目正本判讀 #1、#4），F 距 C 為 $L/4$（判讀 #2），所以 CD 繞 C 轉動：\n\n$$\\theta(t) = \\frac{v_F}{L/4} = \\frac{2\\sqrt{2}}{L}\\, Z(t)$$\n\nCD 上距 C 為 $s$（$0\\le s\\le L/2$）的點，垂直位移為\n\n$$v_{CD}(s,t) = s\\,\\theta(t) = \\frac{2\\sqrt{2}\\,s}{L}\\, Z(t),\\qquad v_D = \\sqrt{2}\\,Z(t)$$\n\n> **策略註解：** CD 上各點的位移幅值與距 C 的距離成正比（C 端 0、F 點 $\\sqrt2/2$、D 端 $\\sqrt2$），不是常數。")
    # §4 Step 2
    s = rep(s, "$$m^* = \\underbrace{\\int_0^L m\\,[\\phi(x)]^2\\,dx}_{m^*_{AB}} + \\underbrace{m_0 \\cdot \\frac{L}{2} \\cdot [\\phi_{CD}]^2}_{m^*_{CD}}$$",
               "$$m^* = \\underbrace{\\int_0^L m\\,[\\phi(x)]^2\\,dx}_{m^*_{AB}} + \\underbrace{\\int_0^{L/2} m_0\\left[\\frac{2\\sqrt2\\,s}{L}\\right]^2 ds}_{m^*_{CD}}$$")
    s = rep(s, "$$m^*_{CD} = m_0 \\cdot \\frac{L}{2} \\cdot \\left[\\sin\\!\\left(\\frac{\\pi}{4}\\right)\\right]^2 = m_0 \\cdot \\frac{L}{2} \\cdot \\left(\\frac{\\sqrt{2}}{2}\\right)^2 = m_0 \\cdot \\frac{L}{2} \\cdot \\frac{1}{2}$$\n\n$$\\boxed{m^*_{CD} = \\frac{m_0 L}{4}}$$",
               "$$m^*_{CD} = m_0\\,\\frac{8}{L^2}\\int_0^{L/2} s^2\\,ds = m_0\\,\\frac{8}{L^2}\\cdot\\frac{L^3}{24} = \\frac{m_0 L}{3}$$\n\n交叉驗算（轉動慣量）：$I_C = m_0(L/2)^3/3 = m_0L^3/24$，$m^*_{CD} = I_C\\,(2\\sqrt2/L)^2 = m_0L/3$ ✓\n\n$$\\boxed{m^*_{CD} = \\frac{m_0 L}{3}}$$")
    s = rep(s, "$$\\boxed{m^* = \\frac{mL}{2} + \\frac{m_0 L}{4}}$$", "$$\\boxed{m^* = \\frac{mL}{2} + \\frac{m_0 L}{3}}$$", 2)
    s = rep(s, "$$\\omega_n = \\sqrt{\\frac{k^*}{m^*}} = \\sqrt{\\frac{\\pi^4 EI / (2L^3)}{mL/2 + m_0 L/4}}$$",
               "$$\\omega_n = \\sqrt{\\frac{k^*}{m^*}} = \\sqrt{\\frac{\\pi^4 EI / (2L^3)}{mL/2 + m_0 L/3}} = \\pi^2\\sqrt{\\frac{3EI}{L^4(3m+2m_0)}}$$")
    # §5 對照
    s = rep(s, "**廣義運動方程式的形式**",
               "**與「CD 整根平移」讀法的對照（本庫舊解）**\n\n本庫舊解漏看 C 端的鉸支承，把 CD 當成隨 F 整根平移（各點位移均為 $\\frac{\\sqrt2}{2}Z$），得 $m^*_{CD} = m_0(L/2)(1/2) = m_0L/4$、$m^* = mL/2 + m_0L/4$。考卷附圖 C 端有三角形鉸支承＋地面剖線（與 A 端同符號），CD 只能繞 C 轉動；整根平移的模型需要 C 端不受約束。正確的 $m^*_{CD}=m_0L/3$ 比平移讀法大 $4/3$ 倍：遠端 D 的位移是 F 的兩倍，而動能與位移平方成正比。$k^*$ 兩種讀法相同。\n\n**廣義運動方程式的形式**")
    s = foot(s, "*修正日期：2026-11-16（FIX-SD-U1-2-G1 解析勘誤（判讀：漏看 C 端鉸支承）：CD 由「整根平移」改為「繞 C 轉動」，m*_CD 由 m0L/4 改為 m0L/3，m* 由 mL/2＋m0L/4 改為 mL/2＋m0L/3；k* 不變；改 §2、§3、§3.5、§4 Step 1–2 與 ω 式、§5 加舊讀法對照；移除 §1 待勘誤警示。證據：2004 年第 1 頁第三題附圖 C 端三角形鉸支承＋剖線（400–500 dpi）。驗證：scripts/fixes/2026-11-16_verify_SD-2004-3.py 積分法、I_Cθ² 法、數值積分三路一致，MISMATCHES: 0；與盲解比對一致）*")
    wr(i, s); print(i, "OK")
else: print(i, "略過")

# ---------- SD-2002-2 標頭（非勘誤） ----------
i = "SD-2002-2"; s = rd(i)
if "**主分類：** `SD-U1` 結構動力學基礎" in s:
    s = rep(s, "**主分類：** `SD-U1` 結構動力學基礎", "**主分類：** `SD-U1-2` 運動方程式推導")
    s = rep(s, "*修正日期：2026-11-16（§1 改為指向題目正本，重繪附圖 figs/SD-2002-2-fig-1-problem.svg）*",
               "*修正日期：2026-11-16（§1 改為指向題目正本，重繪附圖 figs/SD-2002-2-fig-1-problem.svg；標頭主分類 SD-U1 改 SD-U1-2，依索引）*")
    wr(i, s); print(i, "OK")
else: print(i, "略過")

# ---------- 階段 E：圖解補繪（非勘誤） ----------
FIGS = {
 "SD-2002-2": ("\n---\n\n## 5.", "![SD-2002-2 週期比與軸壓比關係：T/T0＝1/√(1−N/Ncr) 隨軸壓比上升、N/Ncr＝0.5 時 1.414、0.75 時 2.000，頻率平方比 1−N/Ncr 線性下降至挫屈時為零](figs/SD-2002-2-fig-2-period-axial.svg)\n*圖 2　軸壓比對週期的影響（依 §4 結果繪製）。軸壓使廣義勁度線性下降，週期按 $1/\\sqrt{1-N/N_{cr}}$ 延長；$M$ 只改變 $T_0$。*\n",
   "figs/SD-2002-2-fig-2-period-axial.svg"),
 "SD-2003-4": ("\n### Step 4：質量矩陣第二行", "![SD-2003-4 u2＝1 時樓版繞 D 轉動 θ＝1/a：A 位移 (−1,0)、B (−1,+1)、C (0,+1)；需施加於 C、B、A 的廣義力 k12＝−3k、k22＝5k、k32＝−3k](figs/SD-2003-4-fig-2-u2-unit.svg)\n*圖 2　勁度矩陣第二行的物理意義：$u_2$ 是 B 點平移（不是質心 $y$），令 $u_2=1$、$u_1=u_3=0$ 時樓版繞 D 轉動，第二行就是此時 C、B、A 三處需施加的力。*\n",
   "figs/SD-2003-4-fig-2-u2-unit.svg"),
 "SD-2004-3": ("\n---\n\n### Step 2：計算廣義質量", "![SD-2004-3 假設變形下 AB 梁正弦撓曲、E、F 位移 √2/2·Z，CD 繞 C 鉸轉動、D 端位移 √2·Z；紅虛線為整根平移的誤讀](figs/SD-2004-3-fig-2-cd-rotation.svg)\n*圖 2　CD 的運動：C 端為鉸支承，CD 繞 C 轉動，位移由 C 端 0 線性增加到 D 端 $\\sqrt2 Z$；紅虛線為整根平移的誤讀（$m^*_{CD}$ 少算 25%）。*\n",
   "figs/SD-2004-3-fig-2-cd-rotation.svg"),
}
for i, (anchor, block, svg) in FIGS.items():
    s = rd(i)
    if svg in s: print(i, "圖已插入，略過"); continue
    assert os.path.exists(os.path.join(SOL, i, svg)) and s.count(anchor) == 1, (i, anchor)
    s = s.replace(anchor, "\n" + block + anchor)
    s = foot(s, f"*修正日期：2026-11-16（非勘誤）圖解補繪：{svg}（腳本 gen_{i}.py，數值取自已驗證正本）*")
    wr(i, s); print(i, "圖 OK")
