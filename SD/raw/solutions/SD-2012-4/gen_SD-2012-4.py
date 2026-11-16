#!/usr/bin/env python3
"""
SD-2012-4 隔震設計位移修正 D'_D — 解題圖解產生腳本（struct-diagram）

用法：python3 gen_SD-2012-4.py [輸出目錄]
（structdraw 位置可用環境變數 STRUCTDRAW 指定；預設找 repo 根目錄 skills/struct-diagram/scripts）

圖中所有數值由下方常數區的串聯模型閉合式算出（與 SD-2012-4.md ㈡ ①②③ 及
SD/scripts/fixes/2026-11-16_verify_SD-2012-4.py 同一套關係）；改 T_{eD}、T 重跑，圖跟著變。
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
TAG = "SD-2012-4"

# ══════════════════════════════════════════════════════════
# 常數區 —— 取自 SD-2012-4.md ㈡「數值核對」例：T_{eD} = 3.0 s、T = 1.0 s，D_D 取 1
# ══════════════════════════════════════════════════════════
T_ED, T_FIX = 3.0, 1.0
R = T_FIX / T_ED                                  # T/T_{eD}

def tot(r):  return math.sqrt(1 + r*r)            # ② 總位移 / D_D
def iso(r):  return 1 / math.sqrt(1 + r*r)        # ③ 隔震層 D'_D / D_D（考卷公式）
def sup(r):  return iso(r) * r*r                  # 上部變形 / D_D = D'_D (T/T_{eD})^2
def old_sup(r): return iso(r) * r                 # 舊解（錯）：D'_D·T/T_{eD}
T_SYS = math.sqrt(T_ED**2 + T_FIX**2)             # ① 系統週期
assert abs(iso(R) + sup(R) - tot(R)) < 1e-12      # 串聯：隔震層 + 上部 = 總位移


def stick(cv, x0, yg, yb, yt, d_iso, d_sup, scale, flexible, title, sub):
    """剪力型示意：地面 yg、隔震層頂（基礎版）yb、上部頂 yt；位移以 scale px / D_D 放大"""
    cv.panel(title, sub)
    xb = x0 + d_iso * scale; xt = xb + d_sup * scale
    # 地面
    cv.line((x0 - 90, yg), (x0 + 210, yg), C["member"], 2.4)
    for i in range(11):
        xx = x0 - 85 + i * 28
        cv.line((xx, yg), (xx - 10, yg - 10), C["member2"], 1.2)
    # 原始位置（灰虛線）
    cv.line((x0, yg), (x0, yt), C["ghost"], 2, dash="6 5")
    cv.line((x0 - 60, yb), (x0 + 60, yb), C["ghost"], 2, dash="6 5")
    # 隔震層（剪切變形，畫成斜向的支承）
    for dx in (-40, 0, 40):
        cv.line((x0 + dx, yg), (xb + dx, yb), C["accent"], 5)
    cv.text_px(cv.X(x0 - 70), cv.Y((yg + yb) / 2), "隔震層", 12.5, C["accent"], "end", weight="700")
    cv.math_px(cv.X(x0 - 70), cv.Y((yg + yb) / 2) + 17, "k_{i}", 13, C["accent"], "end")
    # 基礎版
    cv.line((xb - 62, yb), (xb + 62, yb), C["member"], 6)
    # 上部結構
    n = 40
    if flexible:
        pts = [(xb + d_sup * scale * (3*(k/n)**2 - 2*(k/n)**3), yb + (yt - yb) * k / n) for k in range(n + 1)]
        cv.poly(pts, C["deform"], 4)
        cv.text_px(cv.X(xt + 16), cv.Y((yb + yt) / 2), "上部結構", 12.5, C["deform"], "start", weight="700")
        cv.math_px(cv.X(xt + 16), cv.Y((yb + yt) / 2) + 18, "k_{s}", 13, C["deform"], "start")
        cv.text_px(cv.X(xt + 16), cv.Y((yb + yt) / 2) + 36, "固定基礎週期 T", 12, C["deform"], "start")
    else:
        cv.polygon([(xb - 34, yb), (xb + 34, yb), (xt + 34, yt), (xt - 34, yt)], C["fill_c"], C["deform"], 2.5)
        cv.text_px(cv.X(xt + 46), cv.Y((yb + yt) / 2), "上部結構", 12.5, C["deform"], "start", weight="700")
        cv.text_px(cv.X(xt + 46), cv.Y((yb + yt) / 2) + 17, "視為剛體", 12.5, C["deform"], "start")
    cv.dot((xt, yt), 10, fill=C["member"])
    cv.math((xt, yt), "m", 15, C["text"], dx=24, dy=-16)
    return xb, xt


def fig1_series():
    PW, PH = 470, 470
    S = 190                                   # px / D_D
    YG, YB, YT, X0 = 70, 125, 335, 125
    # (a) 剛體假設
    a = Canvas(PW, PH)
    xb, xt = stick(a, X0, YG, YB, YT, 1.0, 0.0, S, False,
                   "(a) 靜力法：上部結構視為剛體", f"週期 T_{{eD}} = {T_ED:.1f} s，全部變形在隔震層")
    a.dim((X0, YB), (xb, YB), "D_{D}", off=-118, color=C["accent"])
    a.text_px(PW / 2, PH - 34, "隔震層位移 = 總位移 = D_D，上部變形 0", 12.5, C["muted"])
    # (b) 上部柔性（串聯）
    b = Canvas(PW, PH)
    xb, xt = stick(b, X0, YG, YB, YT, iso(R), sup(R), S, True,
                   "(b) 實際：隔震層與上部結構串聯",
                   f"T/T_{{eD}} = {T_FIX:.1f}/{T_ED:.1f}，系統週期 √(T_{{eD}}²+T²) = {T_SYS:.3f} s".replace("²", "^{2}"))
    b.dim((X0, YB), (xb, YB), f"D'_{{D}} = {iso(R):.3f}", off=-118, color=C["accent"], size=13)
    b.dim((X0, YT), (xt, YT), f"{tot(R):.3f}", off=46, color=C["member"], size=13)
    b.text_px((b.X(X0) + b.X(xt)) / 2 - 30, b.Y(YT) + 59, "總位移", 12, C["member"], "end")
    b.line((xb, YB), (xb, YT + 52), C["accent"], 1.2, dash="3 3")      # 基礎版位置延伸線
    b.dim((xb, YT + 40), (xt, YT + 40), "", off=0, color=C["deform"], size=13)
    b.text_px(b.X(xt + 14), b.Y(YT + 40), f"上部變形 {sup(R):.3f}", 12.5, C["deform"], "start", weight="700")
    b.text_px(PW / 2, PH - 34, f"以 D_D = 1 計：{iso(R):.3f} + {sup(R):.3f} = {tot(R):.3f}（總位移大於 D_D，隔震層小於 D_D）", 12, C["muted"])
    compose([a, b], title="圖 1　剛體假設與串聯模型：隔震層只分到總位移的一部分",
            note="位移放大繪製；數值以設計位移 DD 為單位，取解析例 TeD = 3.0 s、T = 1.0 s",
            path=f"{OUT}/{TAG}-fig-1-series.svg")


def fig2_ratio():
    W, H = 820, 500
    cv = Canvas(W, H, bg="#FFFFFF")
    cv.text_px(W / 2, 30, "圖 2　各位移與 D_D 之比隨 T/T_{eD} 的變化：舊解的上部變形式只在 T = T_{eD} 時碰巧對", 16, C["text"], weight="700")
    x0, y0, wp, hp = 90, 420, 500, 320             # 像素（SVG 座標，y 向下）
    rmax, vmax = 1.0, 1.5
    X = lambda r: x0 + r / rmax * wp
    Y = lambda v: y0 - v / vmax * hp
    # 典型設計範圍
    cv.parts.append(f'<rect x="{X(0.1):.1f}" y="{y0-hp}" width="{X(0.4)-X(0.1):.1f}" height="{hp}" fill="{C["fill_m"]}" opacity="0.45"/>')
    cv.text_px(X(0.1) + 4, y0 - hp + 14, "常見設計範圍 0.1–0.4", 11.5, C["bmd"], "start")
    for v in (0.25, 0.5, 0.75, 1.0, 1.25, 1.5):
        cv.parts.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x0+wp}" y2="{Y(v):.1f}" stroke="{C["border"]}" stroke-width="1"/>')
        cv.text_px(x0 - 8, Y(v), f"{v:.2f}", 11.5, C["muted"], "end")
    for r in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        cv.text_px(X(r), y0 + 16, f"{r:.1f}", 11.5, C["muted"])
    cv.parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x0+wp+6}" y2="{y0}" stroke="{C["muted"]}" stroke-width="1.6"/>')
    cv.parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-hp-6}" stroke="{C["muted"]}" stroke-width="1.6"/>')
    cv.math_px(x0 + wp / 2, y0 + 38, "T / T_{eD}", 13.5, C["muted"])
    cv.text_px(x0 - 66, y0 - hp / 2, "÷ D_D", 12.5, C["muted"])
    rs = [i / 200 * rmax for i in range(201)]
    def path(f): return " ".join(f"{'M' if i == 0 else 'L'} {X(r):.1f} {Y(f(r)):.1f}" for i, r in enumerate(rs))
    series = [(tot, C["member"], "", 3.0, "總位移 √(1+r²)"),
              (iso, C["accent"], "", 3.2, "隔震層 D'_D（考卷公式）"),
              (sup, C["deform"], "", 3.0, "上部變形 D'_D r²（正解）"),
              (old_sup, C["load"], "7 5", 2.6, "上部變形 D'_D r（舊解，錯）"),
              (lambda r: 1.0, C["member2"], "7 5", 2.2, "總位移 = D_D（舊解，錯）")]
    for f, col, dash, w, _ in series:
        d = f' stroke-dasharray="{dash}"' if dash else ""
        cv.parts.append(f'<path d="{path(f)}" fill="none" stroke="{col}" stroke-width="{w}"{d}/>')
    # 解析例 r = 1/3
    cv.parts.append(f'<line x1="{X(R):.1f}" y1="{y0}" x2="{X(R):.1f}" y2="{Y(1.36):.1f}" stroke="{C["muted"]}" stroke-width="1.3" stroke-dasharray="3 3"/>')
    cv.text_px(X(R) + 6, Y(1.30), f"解析例 r = {R:.3f}", 11.5, C["muted"], "start")
    for f, col in ((tot, C["member"]), (iso, C["accent"]), (sup, C["deform"]), (old_sup, C["load"])):
        cv.parts.append(f'<circle cx="{X(R):.1f}" cy="{Y(f(R)):.1f}" r="4.5" fill="{col}" stroke="#FFFFFF" stroke-width="1.4"/>')
    cv.text_px(X(R) + 8, Y(tot(R)) - 12, f"{tot(R):.3f}", 11.5, C["member"], "start", weight="700")
    cv.text_px(X(R) + 8, Y(iso(R)) + 13, f"{iso(R):.3f}", 11.5, C["accent"], "start", weight="700")
    cv.text_px(X(R) - 8, Y(old_sup(R)) - 12, f"{old_sup(R):.3f}（舊）", 11.5, C["load"], "end", weight="700")
    cv.text_px(X(R) + 8, Y(sup(R)) + 12, f"{sup(R):.3f}", 11.5, C["deform"], "start", weight="700")
    # r = 1 巧合點
    cv.parts.append(f'<circle cx="{X(1.0):.1f}" cy="{Y(sup(1.0)):.1f}" r="7" fill="none" stroke="{C["load"]}" stroke-width="2"/>')
    cv.parts.append(f'<line x1="{X(1.0)-4:.1f}" y1="{Y(sup(1.0))+7:.1f}" x2="{X(0.96):.1f}" y2="{Y(0.30):.1f}" stroke="{C["load"]}" stroke-width="1.2"/>')
    cv.text_px(X(0.96), Y(0.27), f"r = 1：兩式同為 {sup(1.0):.3f}", 11.5, C["load"], "end")
    # 圖例
    lx, ly = x0 + wp + 26, y0 - hp + 30
    for i, (_, col, dash, w, lab) in enumerate(series):
        yy = ly + i * 30
        d = f' stroke-dasharray="{dash}"' if dash else ""
        cv.parts.append(f'<line x1="{lx}" y1="{yy}" x2="{lx+26}" y2="{yy}" stroke="{col}" stroke-width="{w+0.6}"{d}/>')
        cv.text_px(lx + 34, yy, lab.replace("²", "^{2}"), 12, C["text"], "start")
    cv.text_px(lx, ly + 5 * 30 + 16, "r = T/T_{eD}", 12, C["muted"], "start")
    cv.text_px(lx, ly + 5 * 30 + 36, "隔震層 + 上部 = 總位移", 12, C["muted"], "start")
    cv.text_px(W / 2, H - 22, "在常見設計範圍內，舊解的上部變形是正解的 T_{eD}/T 倍（例：3 倍），且誤把總位移當成 D_D", 12.5, C["muted"])
    cv.save(f"{OUT}/{TAG}-fig-2-ratio.svg")


if __name__ == "__main__":
    print(f"r={R:.4f} T_sys={T_SYS:.4f} tot={tot(R):.4f} iso={iso(R):.4f} sup={sup(R):.4f} old_sup={old_sup(R):.4f}")
    fig1_series(); fig2_ratio()
    print("done →", OUT)
