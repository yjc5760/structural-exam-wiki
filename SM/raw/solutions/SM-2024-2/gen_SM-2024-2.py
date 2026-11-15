# -*- coding: utf-8 -*-
"""SM-2024-2 圖解。
fig-1-problem：題目圖 1–圖 3 重繪，幾何只取自題目正本 SM-2024-2-problem.md §4 判讀清單（#2–#6），不含任何解題結果。
用法：python gen_SM-2024-2.py [輸出資料夾]（預設本題 figs/）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
wt = lambda cv, x, y, s: wt_symbol(cv, x, y + 2.4 * s, C["deform"], s)   # ▽ 尖端落在水面線上

# ── 題目正本 §4 判讀清單 ─────────────────────────────
BETA  = 42.0    # #6
THETA = 30.0    # #4（圖 3）
tb, tt = math.tan(math.radians(BETA)), math.tan(math.radians(THETA))
HS = 6.0        # 示意坡高（考卷未給尺寸）
D  = 1.4        # 示意滑動深度 d（考卷未給數值）

def slope_panel(title, sub, submerged):
    W, H = 400, 380
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-2.6, 9.6), (-1.0, HS + 1.8), 24, 24, 74, 40))
    cv.panel(title, sub)
    xt = HS / tb
    if submerged:
        cv.polygon([(-1, 0), (9.4, 0), (9.4, HS), (-1, HS)], "rgba(29,78,216,0.10)")
        cv.line((-0.8, HS), (9.4, HS), C["deform"], 1.8)
        wt(cv, 0.6, HS, 0.13)
        cv.text_px(cv.X(1.0), cv.Y(HS + 0.45), "水位面（全浸）", 11.5, C["deform"], anchor="start", weight="700")
    cv.polygon([(0, 0), (xt, HS), (9.4, HS), (9.4, 0)], "rgba(180,83,9,0.18)")
    cv.line((-0.8, 0), (9.4, 0), C["member"], 2.2)
    cv.line((0, 0), (xt, HS), C["member"], 2.6)
    cv.line((xt, HS), (9.4, HS), C["member"], 2.0)
    # 平行坡面的滑動面（虛線），鉛直深度 D
    x0 = D / tb
    cv.line((x0, 0), (x0 + (HS - 0.0) / tb, HS), C["load"], 2.0, dash="7 4")
    # 切片：寬 a（水平）、深 d（鉛直）
    xa, a = 2.2, 1.6
    pts = [(xa, xa * tb), (xa + a, (xa + a) * tb), (xa + a, (xa + a) * tb - D), (xa, xa * tb - D)]
    cv.polygon(pts, "rgba(63,74,90,0.35)", C["member"], 1.6)
    cv.dim((xa, (xa + a) * tb + 0.5), (xa + a, (xa + a) * tb + 0.5), "a", 0, C["dim"], 12, label_off=-12)
    xr = xa + a + 0.9
    cv.dim((xr, xr * tb - D), (xr, xr * tb), "d", 0, C["dim"], 12, label_off=12)
    cx, cy = xa + a / 2, (xa + a / 2) * tb - D / 2
    cv.arrow((cx, cy + 0.2), (cx, cy - 0.9), C["load"], 2.0, 7)
    cv.text_px(cv.X(cx) + 8, cv.Y(cy + 0.1), "W", 12, C["load"], anchor="start", weight="700")
    cv.text_px(cv.X(-0.2), cv.Y(0.55), "β = 42°", 12.5, C["dim"], weight="700", anchor="end")
    if not submerged:
        wt(cv, 8.2, 0.0, 0.13)
        cv.text_px(cv.X(8.2), cv.Y(1.1), "水位面", 11.5, C["deform"])
    return cv

def flow_panel():
    W, H = 400, 380
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-2.6, 9.6), (-1.0, HS + 1.8), 24, 24, 74, 40))
    cv.panel("圖 3", "自由水層流向與水平夾 θ")
    xt = HS / tb
    x1 = 2.2
    cv.polygon([(0, 0), (xt, HS), (9.4, HS), (9.4, 0)], "rgba(180,83,9,0.18)")
    cv.line((-0.8, 0), (9.4, 0), C["member"], 2.2)
    cv.line((0, 0), (xt, HS), C["member"], 2.6)
    cv.line((xt, HS), (9.4, HS), C["member"], 2.0)
    xe = 9.2
    cv.line((x1, 0), (xe, (xe - x1) * tt), C["deform"], 2.2)
    wt(cv, 7.6, (7.6 - x1) * tt, 0.13)
    cv.arrow((8.0, (8.0 - x1) * tt - 0.7), (6.6, (6.6 - x1) * tt - 0.7), C["deform"], 3.0, 9)
    cv.text_px(cv.X(5.4), cv.Y(1.2), "自由水層流動方向", 11.5, C["deform"], anchor="start", weight="700")
    cv.text_px(cv.X(-0.2), cv.Y(0.55), "β = 42°", 12.5, C["dim"], weight="700", anchor="end")
    cv.text_px(cv.X(x1 + 2.2), cv.Y(0.45), "θ = 30°", 12.5, C["deform"], weight="700")
    return cv

compose([slope_panel("圖 1", "乾砂邊坡", False), slope_panel("圖 2", "浸水邊坡（靜水）", True), flow_panel()],
        title="SM-2024-2 題目圖 1–圖 3 重繪",
        sub="依題目正本判讀清單；滑動面平行坡面，d 為鉛直深度、a 為水平寬（考卷未給數值，圖上尺寸示意）",
        note="攔錯用：圖 2 是靜水全浸（無滲流），圖 3 的 θ = 30° 是自由水面／流向，不是坡角。",
        path=os.path.join(OUT, "SM-2024-2-fig-1-problem.svg"))


# ═══ fig-2-gradient：解題圖解（階段 E，2026-11-15）════════════════════
# 數值取自解析 §4（三）（盲解一致，2026-11-15）：θ = 30°，i = sin θ = 0.5（Dupuit 近似 tan θ = 0.577 只作對照）。
import math
TH = 30.0
I_SIN = math.sin(math.radians(TH)); I_TAN = math.tan(math.radians(TH))
def fig_gradient():
    W, H = 900, 520
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-1.0, 13.0), (-1.5, 8.0), 30, 30, 30, 30))
    t = math.radians(TH); s = (math.cos(t), math.sin(t)); n = (-math.sin(t), math.cos(t))
    top = lambda u: (12 - u * s[0], 7.0 - u * s[1])        # 自由水面，由右上往左下
    # 流線（平行自由水面）與等勢線（垂直）
    for d in (0.0, 1.0, 2.0, 3.0):
        p0 = (top(0)[0] - n[0] * d, top(0)[1] - n[1] * d); p1 = (top(12)[0] - n[0] * d, top(12)[1] - n[1] * d)
        cv.line(p0, p1, C["deform"], 2.6 if d == 0 else 1.6, dash=None if d == 0 else "8 5")
    for u in (2.0, 5.0, 8.0, 11.0):
        a = top(u); b = (a[0] - n[0] * 3.0, a[1] - n[1] * 3.0)
        cv.line(a, b, C["bmd"], 1.6, dash="3 4")
    cv.text_px(cv.X(top(1)[0]), cv.Y(top(1)[1]) - 14, "自由水面（u = 0）＝最上一條流線", 12.5, C["deform"], anchor="end", weight="700")
    cv.text_px(cv.X(top(11)[0] - n[0] * 3.0) - 6, cv.Y(top(11)[1] - n[1] * 3.0) + 14, "等勢線 ⊥ 流線", 12, C["bmd"], anchor="start")
    # Δs 與高程差
    A_ = top(5.0); B_ = top(8.0)
    cv.arrow(A_, B_, C["load"], 3.2)
    cv.text_px(cv.X((A_[0] + B_[0]) / 2) - 4, cv.Y((A_[1] + B_[1]) / 2) - 16, "Δs（沿流線，水由右上往左下流）", 12.5, C["load"], anchor="end", weight="700")
    cv.line(B_, (A_[0], B_[1]), C["dim"], 1.2, dash="2 3")
    cv.line(A_, (A_[0], B_[1]), C["dim"], 1.2, dash="2 3")
    cv.text_px(cv.X(A_[0]) + 8, cv.Y((A_[1] + B_[1]) / 2), "Δz = Δs sinθ", 12, C["text"], anchor="start")
    cv.text_px(cv.X((A_[0] + B_[0]) / 2), cv.Y(B_[1]) + 16, "Δx = Δs cosθ", 12, C["muted"])
    cv.text_px(cv.X(B_[0]) + 44, cv.Y(B_[1]) - 9, "θ = %g°" % TH, 12.5, C["text"], anchor="start", weight="700")
    cv.text_px(cv.X(-0.5), cv.Y(7.4), "自由水面上 h = z（壓力水頭 0）→ Δh = Δz = Δs sinθ", 13, C["text"], anchor="start", weight="700")
    cv.text_px(cv.X(-0.5), cv.Y(6.7), "i = Δh / Δs = sin %g° = %.2f" % (TH, I_SIN), 14, C["load"], anchor="start", weight="700")
    cv.text_px(cv.X(-0.5), cv.Y(6.0), "對照：Dupuit（流線水平）i = tanθ = %.3f，不合題意「與水平夾 θ 流動」" % I_TAN, 11.5, C["muted"], anchor="start")
    return cv

compose([fig_gradient()],
        title="SM-2024-2 ㈢ 自由水層的水力坡降",
        sub="流線平行自由水面（與水平夾 θ），水頭損失沿流線量測",
        note="攔錯用：分母是沿流線的 Δs（i = sinθ），不是水平距離（tanθ）；也不是坡角 β = 42°。",
        path=os.path.join(OUT, "SM-2024-2-fig-2-gradient.svg"))
