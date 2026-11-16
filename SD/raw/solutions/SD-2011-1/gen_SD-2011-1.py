#!/usr/bin/env python3
"""
SD-2011-1 隔震結構 2DOF 反應譜分析 — 解題圖解產生腳本（struct-diagram）

用法：python3 gen_SD-2011-1.py [輸出目錄]
（structdraw 位置可用環境變數 STRUCTDRAW 指定；預設找 repo 根目錄 skills/struct-diagram/scripts）

所有數值由題目給定參數（SD-2011-1-problem.md §1）依 SD-2011-1.md 步驟一～四重算；
改任何參數重跑，圖跟著變。
"""
import sys, os, math, glob

_here = os.path.dirname(os.path.abspath(__file__))
_cands = [os.environ.get("STRUCTDRAW", ""),
          os.path.join(_here, "..", "..", "..", "..", "skills", "struct-diagram", "scripts")] + \
    glob.glob("/root/.claude/skills/synced/*/struct-diagram/scripts")
for _p in _cands:
    if _p and os.path.isfile(os.path.join(_p, "structdraw.py")):
        sys.path.insert(0, _p); break
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_here, "figs")
TAG = "SD-2011-1"

# ══════════════════════════════════════════════════════════
# 題目給定（題目正本 §1）；g 與解析一致取 9.81 m/s²
# ══════════════════════════════════════════════════════════
W = (300.0, 200.0)                         # tf：〈上部結構, 基礎層〉（判讀 #1）
MODES = [dict(T=2.0, xi=10, phi=(1.041, 1.000)),
         dict(T=0.25, xi=5, phi=(-0.641, 1.000))]
B_TABLE = {5: (1.00, 1.00), 10: (1.33, 1.25), 20: (1.60, 1.50)}   # ξ% → (B_S, B_1)
G = 9.81

def sa(T, xi):
    bs, b1 = B_TABLE[xi]
    if 0.2 < T <= 1.0: return 0.6 / bs
    if 1.0 < T <= 2.5: return 0.6 / (T * b1)
    raise ValueError("考卷未給此譜段")

for md in MODES:
    T, ph = md["T"], md["phi"]
    md["Sa"] = sa(T, md["xi"])
    md["Sd"] = md["Sa"] * G * T**2 / (4 * math.pi**2) * 100          # cm
    L = sum(w * p for w, p in zip(W, ph)); Mst = sum(w * p * p for w, p in zip(W, ph))
    md["G"] = L / Mst
    md["u"] = [md["G"] * p * md["Sd"] for p in ph]                     # cm：〈上部, 基礎〉
    md["drift"] = md["u"][0] - md["u"][1]
U_ISO = math.sqrt(sum(m["u"][1]**2 for m in MODES))
DRIFT = math.sqrt(sum(m["drift"]**2 for m in MODES))
ORTH = sum(w * a * b for w, a, b in zip(W, MODES[0]["phi"], MODES[1]["phi"]))
ORTH_REV = W[1] * MODES[0]["phi"][0] * MODES[1]["phi"][0] + W[0] * 1.0 * 1.0
# 常見選錯
SA1_BS = 0.6 / (MODES[0]["T"] * B_TABLE[10][0])     # 振態 1 誤用 B_S
SA2_10 = 0.6 / B_TABLE[10][0]                       # 振態 2 誤用 ξ=10% 的 B_S


def fig1_spectrum():
    W_, H_ = 860, 520
    cv = Canvas(W_, H_, bg="#FFFFFF")
    cv.text_px(W_ / 2, 30, "圖 1　兩個振態各查各的譜段與阻尼：振態 1 用 B_1（ξ = 10%），振態 2 用 B_S（ξ = 5%）", 15.5, C["text"], weight="700")
    x0, y0, wp, hp = 90, 440, 560, 340
    Tmax, Smax = 2.6, 0.70
    X = lambda t: x0 + t / Tmax * wp
    Y = lambda s: y0 - s / Smax * hp
    cv.parts.append(f'<rect x="{X(0.2):.1f}" y="{y0-hp}" width="{X(1.0)-X(0.2):.1f}" height="{hp}" fill="{C["fill_c"]}" opacity="0.30"/>')
    cv.parts.append(f'<rect x="{X(1.0):.1f}" y="{y0-hp}" width="{X(2.5)-X(1.0):.1f}" height="{hp}" fill="{C["fill_s"]}" opacity="0.30"/>')
    cv.text_px((X(0.2) + X(1.0)) / 2, y0 - hp + 16, "0.2–1.0 s：0.6 ÷ B_S", 12, C["compr"], weight="700")
    cv.text_px((X(1.0) + X(2.5)) / 2, y0 - hp + 16, "1.0–2.5 s：0.6 ÷ (T·B_1)", 12, C["sfd"], weight="700")
    for s in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7):
        cv.parts.append(f'<line x1="{x0}" y1="{Y(s):.1f}" x2="{x0+wp}" y2="{Y(s):.1f}" stroke="{C["border"]}" stroke-width="1"/>')
        cv.text_px(x0 - 8, Y(s), f"{s:.1f}", 11.5, C["muted"], "end")
    for t in (0, 0.5, 1.0, 1.5, 2.0, 2.5):
        cv.text_px(X(t), y0 + 16, f"{t:.1f}", 11.5, C["muted"])
    cv.parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x0+wp+6}" y2="{y0}" stroke="{C["muted"]}" stroke-width="1.6"/>')
    cv.parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-hp-6}" stroke="{C["muted"]}" stroke-width="1.6"/>')
    cv.math_px(x0 + wp / 2, y0 + 40, "T (s)", 13.5, C["muted"])
    cv.math_px(x0 - 56, y0 - hp / 2, "S_{aD}", 14, C["muted"])
    ts = [0.2005 + i * (2.5 - 0.2005) / 300 for i in range(301)]
    def path(xi): return " ".join(f"{'M' if i == 0 else 'L'} {X(t):.1f} {Y(sa(t, xi)):.1f}" for i, t in enumerate(ts))
    cv.parts.append(f'<path d="{path(5)}" fill="none" stroke="{C["member"]}" stroke-width="2.8"/>')
    cv.parts.append(f'<path d="{path(10)}" fill="none" stroke="{C["load"]}" stroke-width="2.8"/>')
    m1, m2 = MODES
    def mark(T, s, col, hollow=False):
        if hollow:
            cv.parts.append(f'<circle cx="{X(T):.1f}" cy="{Y(s):.1f}" r="5.5" fill="#FFFFFF" stroke="{col}" stroke-width="2.2"/>')
        else:
            cv.parts.append(f'<circle cx="{X(T):.1f}" cy="{Y(s):.1f}" r="6" fill="{col}" stroke="#FFFFFF" stroke-width="1.6"/>')
    for md in MODES:
        cv.parts.append(f'<line x1="{X(md["T"]):.1f}" y1="{y0}" x2="{X(md["T"]):.1f}" y2="{Y(md["Sa"]):.1f}" stroke="{C["accent"]}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    mark(m2["T"], m2["Sa"], C["member"]); mark(m2["T"], SA2_10, C["muted"], True)
    mark(m1["T"], m1["Sa"], C["load"]); mark(m1["T"], SA1_BS, C["muted"], True)
    cv.text_px(X(m2["T"]) + 12, Y(m2["Sa"]) - 14, f"振態 2：T = {m2['T']} s，ξ = 5% → {m2['Sa']:.3f}", 12.5, C["member"], "start", weight="700")
    cv.text_px(X(m2["T"]) + 12, Y(SA2_10) + 20, f"誤用 ξ = 10% 的 B_S：{SA2_10:.3f}", 12, C["muted"], "start")
    cv.text_px(X(m1["T"]) - 12, Y(m1["Sa"]) - 18, f"振態 1：T = {m1['T']} s，÷ B_1 = 1.25 → {m1['Sa']:.3f}", 12.5, C["load"], "end", weight="700")
    cv.text_px(X(m1["T"]) - 12, Y(SA1_BS) + 18, f"誤用 B_S = 1.33：{SA1_BS:.3f}", 12, C["muted"], "end")
    cv.text_px(X(m1["T"]), y0 + 32, "T_1", 12.5, C["accent"], weight="700")
    cv.text_px(X(m2["T"]) + 8, y0 + 32, "T_2", 12.5, C["accent"], weight="700")
    lx, ly = x0 + wp + 30, y0 - hp + 50
    cv.legend(lx, ly, [(C["member"], "ξ = 5% 設計譜"), (C["load"], "ξ = 10% 設計譜")], 12, 24)
    cv.parts.append(f'<circle cx="{lx+11}" cy="{ly+60}" r="5.5" fill="#FFFFFF" stroke="{C["muted"]}" stroke-width="2.2"/>')
    cv.text_px(lx + 30, ly + 60, "常見選錯", 12, C["muted"], "start")
    cv.text_px(lx, ly + 100, "考卷只給兩段", 12, C["muted"], "start")
    cv.text_px(lx, ly + 120, "（0.2–2.5 s）", 12, C["muted"], "start")
    cv.text_px(W_ / 2, H_ - 20, "各振態用自己的阻尼比查表；振態 2 的 5% 阻尼不能套振態 1 的 10%（S_{aD} 會低估約 25%）", 12.5, C["muted"])
    cv.save(f"{OUT}/{TAG}-fig-1-spectrum.svg")


def fig2_modes():
    PW, PH = 400, 470
    panels = []
    HB, HT, XC, SC = 155, 345, 170, 70        # 基礎層高、上部高、未變形 x、φ 每 1 的像素
    for n, md in enumerate(MODES, 1):
        cv = Canvas(PW, PH)
        cv.panel(f"({'ab'[n-1]}) 振態 {n}：T = {md['T']} s，ξ = {md['xi']}%",
                 f"Γ_{n} = {md['G']:.4f}，S_d = {md['Sd']:.3f} cm")
        ph = md["phi"]
        yg = 95
        cv.line((XC - 110, yg), (XC + 160, yg), C["member"], 2.4)
        for i in range(10):
            xx = XC - 105 + i * 28
            cv.line((xx, yg), (xx - 10, yg - 10), C["member2"], 1.2)
        cv.line((XC, yg), (XC, HT), C["ghost"], 2, dash="6 5")
        xb, xt = XC + ph[1] * SC, XC + ph[0] * SC
        cv.line((XC, yg), (xb, HB), C["accent"], 4)            # 隔震層
        cv.line((xb, HB), (xt, HT), C["deform"], 4)            # 上部結構
        cv.line((xb - 40, HB), (xb + 40, HB), C["member"], 6)
        cv.dot((xt, HT), 9, fill=C["member"]); cv.dot((xb, HB), 7, fill=C["member"])
        u = md["u"]
        cv.text_px(cv.X(xt) + (14 if ph[0] > 0 else -14), cv.Y(HT) - 22,
                   f"上部 φ = {ph[0]:+.3f}", 12.5, C["deform"], "start" if ph[0] > 0 else "end", weight="700")
        cv.text_px(cv.X(xt) + (14 if ph[0] > 0 else -14), cv.Y(HT) - 4,
                   f"u = {u[0]:+.4g} cm", 12, C["deform"], "start" if ph[0] > 0 else "end")
        cv.text_px(cv.X(xb) + 48, cv.Y(HB) - 8, f"基礎層 φ = {ph[1]:+.3f}", 12.5, C["accent"], "start", weight="700")
        cv.text_px(cv.X(xb) + 48, cv.Y(HB) + 10, f"u = {u[1]:+.4g} cm", 12, C["accent"], "start")
        cv.text_px(PW / 2, PH - 58, f"層間（上部 − 基礎）= {md['drift']:+.4g} cm", 12.5, C["text"], weight="700")
        cv.text_px(PW / 2, PH - 36, "隔震振態：幾乎剛體平移" if n == 1 else "上部振態：上部與基礎反向", 12, C["muted"])
        panels.append(cv)
    # (c) 判讀檢核與 SRSS
    cv = Canvas(PW, PH)
    cv.panel("(c) 分量順序檢核與 SRSS", "振態向量 〈上部, 基礎〉 才互相正交")
    rows = [("Σ W φ_1 φ_2，〈上部, 基礎〉", f"{ORTH:+.2f} tf ≈ 0", C["bmd"]),
            ("Σ W φ_1 φ_2，〈基礎, 上部〉", f"{ORTH_REV:+.1f} tf ≠ 0", C["load"]),
            ("㈠ 隔震層位移 SRSS", f"{U_ISO:.2f} cm", C["accent"]),
            ("㈡ 層間位移 SRSS", f"{DRIFT:.3f} cm", C["deform"])]
    for i, (lab, val, col) in enumerate(rows):
        y = 110 + i * 78
        cv.rect_px(26, y - 4, PW - 52, 62, "#FFFFFF", 10, C["border"], 1)
        cv.text_px(42, y + 16, lab, 12.5, C["text"], "start")
        cv.text_px(PW - 42, y + 40, val, 14, col, "end", weight="700")
    cv.text_px(PW / 2, PH - 36, "層間位移：每個振態先相減，再做 SRSS", 12, C["muted"])
    panels.append(cv)
    compose(panels, title="圖 2　振態形狀與各振態位移（振態向量 φ 按比例繪，位移值為 Γ·φ·Sd）",
            note="振態 1 貢獻幾乎全部位移；振態 2 的層間分量最大但量級只有 0.04 cm",
            path=f"{OUT}/{TAG}-fig-2-modes.svg")


if __name__ == "__main__":
    for n, m in enumerate(MODES, 1):
        print(n, f"Sa={m['Sa']:.4f} Sd={m['Sd']:.4f}cm G={m['G']:.5f} u={m['u'][0]:.5f},{m['u'][1]:.5f} drift={m['drift']:.5f}")
    print(f"U_iso={U_ISO:.4f} drift={DRIFT:.5f} orth={ORTH:.3f} rev={ORTH_REV:.2f} Sa1_Bs={SA1_BS:.4f} Sa2_10={SA2_10:.4f}")
    fig1_spectrum(); fig2_modes()
    print("done →", OUT)
