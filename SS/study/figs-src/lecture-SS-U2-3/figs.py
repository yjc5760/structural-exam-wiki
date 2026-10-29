import math
from figlib import *

# =====================================================================
# F02  HAZ：峰值溫度分布 ↔ 區帶寬度（區帶邊界由溫度門檻反算，非手擺）
# =====================================================================
def fig_haz():
    f = Fig(880, 500, "haz")
    T0, TM = 20.0, 1500.0
    A1, A3, TGC, TLOW = 727.0, 850.0, 1100.0, 500.0
    Tp = lambda x: T0 + (TM - T0) / x ** 2          # x = r / r0（r0 = 熔合線位置）
    xc = lambda T: math.sqrt((TM - T0) / (T - T0))  # 反算：峰值溫度 = T 的位置
    x_gc, x_a3, x_a1, x_lo = xc(TGC), xc(A3), xc(A1), xc(TLOW)
    XMAX = 2.2
    px0, px1, py0, py1 = 96, 846, 36, 236
    X, Y = axes(f, px0, py0, px1, py1, 0, XMAX, 0, 1750)

    # grid + axes
    for T in (0, 500, 1000, 1500):
        f.line(px0, Y(T), px1, Y(T), GRID, 1)
        f.text(px0 - 8, Y(T) + 4, f"{T}", 11.5, MUT, "end")
    f.text(30, (py0 + py1) / 2, "峰值溫度 Tp (°C)", 12.5, MUT, "middle", rot=-90)
    f.line(px0, py1, px1, py1, STEEL_D, 1.4)
    f.line(px0, py0 - 6, px0, py1, STEEL_D, 1.4)
    for v in (0, 0.5, 1.0, 1.5, 2.0):
        f.line(X(v), py1, X(v), py1 + 4, STEEL_D, 1)
        f.text(X(v), py1 + 17, f"{v:g}", 11.5, MUT, "middle")
    f.text((px0 + px1) / 2, py1 + 33, "距銲道中心距離 r / r₀（r₀＝熔合線位置）", 11.5, MUT, "middle")

    # zone bands (behind curve)
    zones = [
        (0, 1.0, "#ffcdd2"), (1.0, x_gc, "#ffe0b2"), (x_gc, x_a3, "#c8e6c9"),
        (x_a3, x_a1, "#e1f5fe"), (x_a1, x_lo, "#eceff1"),
    ]
    for a, b, c in zones:
        f.rect(X(a), py0, X(b) - X(a), py1 - py0, c, "none", 0, op=0.55)

    # threshold lines
    for T, lab, col in ((TM, "熔點 ≈ 1500", RED), (TGC, "晶粒粗化 ≈ 1100", ORANGE),
                        (A3, "A3 ≈ 850", GREEN), (A1, "A1 = 727", BLUE), (TLOW, "≈ 500", MUT)):
        f.line(px0, Y(T), px1, Y(T), col, 1, dash="5,4", op=0.8)
        f.text(px1 - 4, Y(T) - 4, lab, 11, col, "end", "600")

    # curve
    pts = [(X(0), Y(1650)), (X(0.6), Y(1650)), (X(1.0), Y(TM))]
    n = 80
    for i in range(n + 1):
        x = 1.0 + (XMAX - 1.0) * i / n
        pts.append((X(x), Y(Tp(x))))
    f.path("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts[:2]) + f" Q{X(0.85):.1f},{Y(1640):.1f} {pts[2][0]:.1f},{pts[2][1]:.1f} L"
           + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts[3:]), "none", BLUE, 2.6)
    f.text(X(0.3), Y(1650) - 8, "熔池（已熔化）", 12, RED, "middle", "600")
    f.text(X(1.62), Y(1150), "Tp − T₀ ∝ 1/r²", 12, BLUE, "middle", "600")

    # crossing markers + vertical drop to strip
    sy0, sy1 = 300, 346
    for x, T, c in ((1.0, TM, RED), (x_gc, TGC, ORANGE), (x_a3, A3, GREEN), (x_a1, A1, BLUE), (x_lo, TLOW, MUT)):
        f.circle(X(x), Y(T), 3.6, c, "#fff", 1.2)
        f.line(X(x), Y(T), X(x), sy1, c, 1, dash="3,3")

    # strip = 板材剖面（真實比例）
    f.text(px0, sy0 - 10, "同一比例尺下的剖面帶（每條邊界＝上圖曲線與溫度門檻的交點）", 12, INK, weight="600")
    f.rect(X(0), sy0, X(1.0) - X(0), sy1 - sy0, "#ef9a9a", STEEL_D, 1)
    cols = ["#ffb74d", "#81c784", "#81d4fa", "#b0bec5"]
    bounds = [1.0, x_gc, x_a3, x_a1, x_lo]
    for i in range(4):
        f.rect(X(bounds[i]), sy0, X(bounds[i + 1]) - X(bounds[i]), sy1 - sy0, cols[i], STEEL_D, 1)
    f.rect(X(x_lo), sy0, X(XMAX) - X(x_lo), sy1 - sy0, "#eceff1", STEEL_D, 1)
    f.text(X(0.5), (sy0 + sy1) / 2 + 5, "銲道", 13, "#b71c1c", "middle", "700")
    f.text(X((x_lo + XMAX) / 2), (sy0 + sy1) / 2 + 5, "母材", 13, MUT, "middle", "700")
    for i, n_ in enumerate("①②③④"):
        f.text(X((bounds[i] + bounds[i + 1]) / 2), (sy0 + sy1) / 2 + 5, n_, 14, INK, "middle", "700")
    # HAZ bracket
    f.line(X(1.0), sy1 + 10, X(x_lo), sy1 + 10, ORANGE, 1.6)
    f.line(X(1.0), sy1 + 5, X(1.0), sy1 + 15, ORANGE, 1.6)
    f.line(X(x_lo), sy1 + 5, X(x_lo), sy1 + 15, ORANGE, 1.6)
    f.text(X((1.0 + x_lo) / 2), sy1 + 28, "熱影響區 HAZ（未熔化，但組織已變）", 12.5, ORANGE, "middle", "700")

    # legend table
    ly = 432
    rows = [
        ("①", "粗晶區（過熱區）", "1100～1500 °C", "沃斯田鐵晶粒長大 → 韌性最低、最易冷裂", RED),
        ("②", "細晶區（正火區）", "A3～1100 °C", "完全再結晶、晶粒細化 → 韌性常優於母材", GREEN),
        ("③", "部分相變區", "A1～A3", "只有部分組織轉變，混合組織", BLUE),
        ("④", "次臨界（回火）區", "< A1", "不相變，僅回火／析出，性質略變", MUT),
    ]
    for i, (n_, name, rng, desc, c) in enumerate(rows):
        col = i % 2; row = i // 2
        x = 40 + col * 420; y = ly + row * 36
        f.text(x, y, n_, 14, c, weight="700")
        f.text(x + 20, y, name, 13, c, weight="700")
        f.text(x + 140, y, rng, 12, INK, weight="600")
        f.text(x + 20, y + 15, desc, 11.5, MUT)
    f.text(440, 404, f"本圖數值：r₀ 以外的區帶寬度依序為 {x_gc-1:.2f}、{x_a3-x_gc:.2f}、{x_a1-x_a3:.2f}、{x_lo-x_a1:.2f} r₀ ——粗晶區就緊貼熔合線", 11.5, MUT, "middle")
    return f.svg()


# =====================================================================
# F04  層狀撕裂
# =====================================================================
def fig_lamellar():
    f = Fig(880, 360, "lam")
    f.line(440, 14, 440, 346, "#b0bec5", 2, dash="6,5")
    # ---- left: in-plane tension
    f.text(220, 34, "一般受力：拉力平行板面", 15, GREEN, "middle", "700")
    x0, y0, w, h = 70, 120, 300, 70
    f.rect(x0, y0, w, h, STEEL, STEEL_D, 1.4)
    import random
    rnd = random.Random(3)
    for i in range(16):
        yy = y0 + 10 + rnd.random() * (h - 20); xx = x0 + 10 + rnd.random() * (w - 70)
        f.line(xx, yy, xx + 30 + rnd.random() * 25, yy, "#78909c", 2.2)
    f.line(x0 - 6, y0 + h / 2, x0 - 50, y0 + h / 2, GREEN, 3, arrow=GREEN)
    f.line(x0 + w + 6, y0 + h / 2, x0 + w + 50, y0 + h / 2, GREEN, 3, arrow=GREEN)
    f.text(220, y0 - 14, "拉力 ∥ 夾雜物條帶 → 條帶只是細長小洞，不構成連續弱面", 12.5, GREEN, "middle")
    f.text(220, y0 + h + 22, "灰色短線＝軋延時被壓扁拉長的 MnS 夾雜物", 12, MUT, "middle")
    f.rect(70, 262, 300, 56, "#e8f5e9", "#a5d6a7", 1, rx=8)
    f.text(220, 285, "板面方向（X、Y）延性充足", 13.5, GREEN, "middle", "700")
    f.text(220, 306, "一般 SN-A／B 即可", 12.5, GREEN, "middle")

    # ---- right: T-joint, Z-direction
    f.text(660, 34, "T 型接頭：拉力垂直板面（Z 向）", 15, RED, "middle", "700")
    bx, by, bw, bh = 520, 170, 290, 76        # 厚板（柱面板）
    vx, vw = 645, 40                           # 立板
    f.rect(bx, by, bw, bh, STEEL, STEEL_D, 1.4)
    for i in range(14):
        yy = by + 10 + rnd.random() * (bh - 20); xx = bx + 8 + rnd.random() * (bw - 50)
        f.line(xx, yy, xx + 22 + rnd.random() * 18, yy, "#78909c", 2.2)
    f.rect(vx, 104, vw, by - 104, STEEL, STEEL_D, 1.4)
    # double-bevel CJP + reinforcing fillets
    f.poly([(vx, by - 26), (vx - 22, by), (vx, by)], WELD, "#d84315", 1.2)
    f.poly([(vx + vw, by - 26), (vx + vw + 22, by), (vx + vw, by)], WELD, "#d84315", 1.2)
    # stepped tear: terraces (along inclusions) + shear walls
    ty = [by + 14, by + 24, by + 33]
    d = (f"M{vx-30},{ty[0]} L{vx+2},{ty[0]} L{vx+6},{ty[1]} L{vx+40},{ty[1]} L{vx+44},{ty[2]} L{vx+78},{ty[2]}")
    f.path(d, "none", RED, 2.6)
    f.text(vx + 82, ty[2] + 4, "階梯狀撕裂", 12, RED, weight="700")
    f.text(bx + bw / 2, by + bh + 20, "平台＝沿夾雜物層撕開；豎牆＝層與層間剪斷", 11.5, RED, "middle")
    # Z arrows
    f.line(vx + vw / 2, 100, vx + vw / 2, 56, RED, 3, arrow=RED)
    f.text(vx + vw / 2 + 14, 74, "銲道收縮＋拘束", 12, RED, weight="600")
    f.text(vx + vw / 2 + 14, 90, "→ Z 向拉力", 12, RED, weight="600")
    f.text(bx - 6, by + bh / 2 + 4, "t ≥ 40", 11.5, MUT, "end")
    f.line(bx - 4, by, bx - 4, by + bh, MUT, 1)
    f.rect(500, 274, 330, 66, "#ffebee", "#ef9a9a", 1, rx=8)
    f.text(665, 296, "板厚方向沒有延性儲備；換銲材無效", 13.5, RED, "middle", "700")
    f.text(665, 316, "對策：SN-C（Z 向斷面收縮率 RA ≥ 25%）", 12.5, RED, "middle")
    f.text(665, 333, "銲接箱型柱板厚 ≥ 40 mm 時須用 SN400C／SN490C", 11.5, "#b71c1c", "middle")
    return f.svg()


# =====================================================================
# F05  CVN–溫度：tanh 轉換曲線，0 °C / 27 J 判定點
# =====================================================================
def fig_cvn():
    f = Fig(880, 400, "cvn")
    px0, px1, py0, py1 = 90, 690, 30, 320
    X, Y = axes(f, px0, py0, px1, py1, -60, 60, 0, 240)
    cv = lambda T, LS, US, T0, C: LS + (US - LS) / 2 * (1 + math.tanh((T - T0) / C))
    A = dict(LS=5, US=200, T0=-25, C=12)    # 有韌性保證（SN-B／C 類）
    B = dict(LS=5, US=150, T0=15, C=12)     # 無韌性保證（示意）
    for v in range(0, 241, 40):
        f.line(px0, Y(v), px1, Y(v), GRID, 1)
        f.text(px0 - 8, Y(v) + 4, f"{v}", 11.5, MUT, "end")
    for t in range(-60, 61, 20):
        f.line(X(t), py1, X(t), py1 + 4, STEEL_D, 1)
        f.text(X(t), py1 + 18, f"{t}", 11.5, MUT, "middle")
    f.line(px0, py1, px1, py1, STEEL_D, 1.4); f.line(px0, py0, px0, py1, STEEL_D, 1.4)
    f.text(px0 + (px1 - px0) / 2, py1 + 38, "試驗溫度 T (°C)", 12.5, MUT, "middle")
    f.text(34, (py0 + py1) / 2, "CVN 吸收能 (J)", 12.5, MUT, "middle", rot=-90)
    # requirement
    f.line(px0, Y(27), px1, Y(27), RED, 1.3, dash="6,4")
    f.text(px1 - 4, Y(27) - 5, "門檻 27 J", 12, RED, "end", "700")
    f.line(X(0), py0, X(0), py1, ORANGE, 1.3, dash="6,4")
    f.text(X(0) + 5, py0 + 12, "0 °C", 12, ORANGE, weight="700")
    # acceptable quadrant shading
    f.rect(X(0) - 2, py0, 4, Y(27) - py0, ORANGE, "none", 0, op=0.25)

    def curve(p, col, sw, dash=None):
        pts = [(X(t), Y(cv(t, **p))) for t in [-60 + i * 0.5 for i in range(241)]]
        f.path("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts), "none", col, sw, dash)
    curve(A, BLUE, 2.8); curve(B, MUT, 2.4, "7,4")
    a0, b0 = cv(0, **A), cv(0, **B)
    f.circle(X(0), Y(a0), 5, BLUE, "#fff", 1.5)
    f.circle(X(0), Y(b0), 5, MUT, "#fff", 1.5)
    f.text(X(0) + 9, Y(a0) + 16, f"{a0:.0f} J ≥ 27 ✓", 12.5, BLUE, weight="700")
    f.text(X(0) - 10, Y(b0) - 6, f"{b0:.0f} J < 27 ✗", 12.5, "#455a64", "end", "700")
    # T27 of each curve (solve)
    def t27(p):
        LS, US, T0, C = p["LS"], p["US"], p["T0"], p["C"]
        return T0 + C * math.atanh(2 * (27 - LS) / (US - LS) - 1)
    for p, col in ((A, BLUE), (B, MUT)):
        t = t27(p)
        f.circle(X(t), Y(27), 3.5, col, "#fff", 1)
        if col == BLUE:
            f.text(X(t) + 8, Y(27) + 16, f"T27J = {t:.0f} °C", 11.5, col, "start", "700")
        else:
            f.text(X(t) + 12, Y(27) + 16, f"T27J = {t:.0f} °C", 11.5, "#455a64", "start", "700")
    f.text(X(-50), Y(50), "脆性平台", 12, MUT, "middle")
    f.text(X(-40), Y(205), "韌性平台", 12, BLUE, "middle")
    f.text(X(A['T0']) - 8, Y(cv(A['T0'], **A)), "轉換區", 12, PURPLE, "end", "700")
    # side panel
    sx = 712
    f.rect(sx, 40, 156, 270, "#fafcfd", "#cfd8dc", 1, rx=8)
    f.lines(sx + 12, 64, [("判定方式", INK, "700"),
                          ("在 0 °C 這條垂直線上，", MUT), ("曲線必須高於 27 J。", MUT),
                          ("", MUT),
                          ("等價說法：", INK, "700"), ("T27J ≤ 0 °C", BLUE, "700"),
                          ("（轉換溫度要夠低）", MUT), ("", MUT),
                          ("SN-B、SN-C：", INK, "700"), ("0 °C 下 CVN ≥ 27 J", RED, "700"),
                          ("SN-A：無此要求", MUT)], 12.5, lh=20)
    f.text(390, 388, "兩條為 tanh 模型示意曲線（數值非特定爐號實測）；藍＝有衝擊韌性保證、灰虛＝無保證", 11.5, MUT, "middle")
    return f.svg()


# =====================================================================
# F06  填角銲：任意斷面角 θ 的破壞面長度 w/(sinθ+cosθ)，最短在 45°
# =====================================================================
def fig_fillet():
    f = Fig(880, 392, "fw")
    # left: geometry
    s = 20.0          # px per mm
    W = 8.0           # mm
    ox, oy = 150, 250  # root
    f.rect(ox - 60, 40, 60, oy - 40 + 60, STEEL, STEEL_D, 1.3)          # 立板
    f.rect(ox, oy, 250, 60, STEEL, STEEL_D, 1.3)                          # 底板
    A_ = (ox, oy - W * s); B_ = (ox + W * s, oy)
    f.poly([(ox, oy), A_, B_], "#ffe0b2", ORANGE, 1.6)
    f.line(A_[0], A_[1], B_[0], B_[1], RED, 2.4)
    # theta=30° plane & 45°
    for th, col, lab in ((30, MUT, "θ = 30°"), (45, BLUE, "θ = 45°")):
        r = W / (math.sin(math.radians(th)) + math.cos(math.radians(th)))
        ex, ey = ox + r * s * math.cos(math.radians(th)), oy - r * s * math.sin(math.radians(th))
        f.line(ox, oy, ex, ey, col, 2.2 if th == 45 else 1.6, dash=None if th == 45 else "5,3")
        R = 46 if th == 45 else 70
        f.path(f"M{ox+R:.1f},{oy:.1f} A{R},{R} 0 0 0 {ox+R*math.cos(math.radians(th)):.1f},{oy-R*math.sin(math.radians(th)):.1f}", "none", col, 1.2)
        la, lr = (62, 54) if th == 45 else (12, 96)
        lx = ox + lr * math.cos(math.radians(la)); ly = oy - lr * math.sin(math.radians(la))
        f.text(lx, ly + 4, lab, 11.5, col, weight="700")
    # right-angle mark at throat foot
    fx, fy = ox + W / 2 * s, oy - W / 2 * s
    u = 9 / math.sqrt(2)
    f.path(f"M{fx-u:.1f},{fy-u:.1f} L{fx:.1f},{fy-2*u:.1f} L{fx+u:.1f},{fy-u:.1f}", "none", BLUE, 1.2)
    f.circle(ox, oy, 4.5, RED, "#fff", 1.2); f.text(ox - 10, oy + 22, "銲根", 12.5, RED, "end", "700")
    f.circle(*B_, 4.5, PURPLE, "#fff", 1.2); f.text(B_[0] + 4, B_[1] - 10, "銲趾", 12.5, PURPLE, weight="700")
    f.circle(*A_, 4.5, PURPLE, "#fff", 1.2); f.text(A_[0] + 8, A_[1] - 2, "銲趾", 12.5, PURPLE, weight="700")
    f.dim(ox, oy + 78, B_[0], oy + 78, "w = 8 mm", MUT, lpos=((ox + B_[0]) / 2, oy + 96))
    f.line(ox, oy + 62, ox, oy + 84, MUT, 0.8); f.line(B_[0], oy + 62, B_[0], oy + 84, MUT, 0.8)
    f.dim(ox - 78, A_[1], ox - 78, oy, "w", MUT, lpos=(ox - 88, (A_[1] + oy) / 2 + 4), anchor="end")
    f.text(fx - 34, fy - 26, "tₑ", 14, BLUE, weight="700")
    f.text(240, 30, "等腳填角銲斷面（1 mm = 20 px）", 13, INK, "middle", "700")

    # right: plot of r(θ)/w
    px0, px1, py0, py1 = 500, 840, 60, 270
    X, Y = axes(f, px0, py0, px1, py1, 0, 90, 0.6, 1.05)
    for v in (0.6, 0.7, 0.8, 0.9, 1.0):
        f.line(px0, Y(v), px1, Y(v), GRID, 1)
        f.text(px0 - 6, Y(v) + 4, f"{v:.1f}", 11, MUT, "end")
    for t in (0, 15, 30, 45, 60, 75, 90):
        f.text(X(t), py1 + 16, f"{t}°", 11, MUT, "middle")
    f.line(px0, py1, px1, py1, STEEL_D, 1.3); f.line(px0, py0, px0, py1, STEEL_D, 1.3)
    pts = [(X(t), Y(1 / (math.sin(math.radians(t)) + math.cos(math.radians(t))))) for t in range(0, 91)]
    f.path("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts), "none", BLUE, 2.6)
    tmin = 1 / math.sqrt(2)
    f.circle(X(45), Y(tmin), 5, RED, "#fff", 1.4)
    f.line(X(45), Y(tmin), X(45), py1, RED, 1, dash="4,3")
    f.text(X(45), Y(tmin) + 22, f"最短 = 1/√2 = {tmin:.4f}", 12.5, RED, "middle", "700")
    r30 = 1 / (math.sin(math.radians(30)) + math.cos(math.radians(30)))
    f.circle(X(30), Y(r30), 3.5, MUT, "#fff", 1)
    f.text(X(30) - 4, Y(r30) - 8, f"θ=30°：{r30:.3f}", 11, MUT, "end")
    f.text((px0 + px1) / 2, 36, "破壞面長度 r(θ) / w = 1 / (sin θ + cos θ)", 13, INK, "middle", "700")
    f.text((px0 + px1) / 2, py1 + 36, "破壞面與水平腳的夾角 θ", 12, MUT, "middle")
    f.text(440, 384, "裂縫會走最短的路：所有通過銲根的斷面中，45° 那一條最短 → 有效銲喉 tₑ = 0.707 w 是幾何極小值，不是規範係數", 12, INK, "middle")
    return f.svg()


# ---------- shared box/diamond helpers for flowcharts ----------
def box(f, cx, cy, w, h, title, sub=(), fill="#eceff1", stroke="#546e7a", tcol=INK, scol=MUT, rx=9, ts=14):
    f.rect(cx - w / 2, cy - h / 2, w, h, fill, stroke, 1.7, rx=rx)
    n = 1 + len(sub)
    y = cy - (n - 1) * 10 + 5
    f.text(cx, y, title, ts, tcol, "middle", "700")
    for i, s in enumerate(sub):
        f.text(cx, y + 20 * (i + 1), s, 12, scol, "middle")


def diamond(f, cx, cy, w, h, rows, fill="#fff3e0", stroke=ORANGE, tcol="#e65100"):
    f.poly([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)], fill, stroke, 1.8)
    y = cy - (len(rows) - 1) * 9 + 5
    for i, s in enumerate(rows):
        f.text(cx, y + 18 * i, s, 13.5 if i == 0 else 12, tcol, "middle", "700" if i == 0 else None)


def conn(f, pts, col="#546e7a", label=None, lpos=None, lcol=None):
    f.poly(pts, "none", col, 1.9, close=False, arrow=col)
    if label:
        f.text(lpos[0], lpos[1], label, 12.5, lcol or col, "middle", "700")


# =====================================================================
# F07  回銲：角鋼剪力接合（立面＋頂部俯視），長度依比例
# =====================================================================
def fig_end_return():
    f = Fig(880, 430, "er")
    S = 1.15                 # px / mm
    w = 8.0                  # mm
    LEG_W, LEG_H = 90.0, 200.0
    ell = 3 * w              # 繪示 3w
    for k, (x0, title, col) in enumerate(((20, "① 無回銲：銲道停在角點", RED), (300, "② 回銲 2w ≤ ℓ ≤ 4w", GREEN))):
        f.text(x0 + 120, 28, title, 14.5, col, "middle", "700")
        # column flange face
        f.rect(x0 + 10, 44, 240, 320, "#eceff1", STEEL_D, 1.2)
        f.text(x0 + 18, 60, "柱翼板面（立面）", 11.5, MUT)
        lx, ly = x0 + 64, 96
        lw, lh = LEG_W * S, LEG_H * S
        f.rect(lx, ly, lw, lh, STEEL, STEEL_D, 1.4)            # 角鋼貼柱之肢
        f.rect(lx - 13, ly, 13, lh, "#b0bec5", STEEL_D, 1.2)   # 外伸肢（側視）
        f.text(lx + lw / 2, ly + lh / 2, "角鋼肢", 12.5, INK, "middle", "600")
        f.text(lx - 7, ly + lh + 18, "↑ 外伸肢（接梁腹板）", 10.5, MUT)
        # weld along toe (right vertical edge)
        f.rect(lx + lw, ly, w * S, lh, "#ef6c00", "none", 0)
        f.text(lx + lw + w * S + 6, ly + lh / 2 + 20, "銲道", 11.5, ORANGE, weight="700")
        f.text(lx + lw + w * S + 6, ly + lh / 2 + 36, f"w = {w:g} mm", 11, ORANGE)
        if k == 0:
            f.circle(lx + lw + 4, ly, 12, "none", RED, 2)
            f.lines(lx + lw - 6, ly - 20, [("弧坑＋應力集中", RED, "700")], 11.5, anchor="end")
            f.line(lx + lw + 4, ly + 10, lx + lw + 4, ly + 40, RED, 1.6, dash="3,2")
            f.text(lx + 6, ly + 26, "頂端受剝離拉力", 11.5, RED, weight="600")
        else:
            f.rect(lx + lw + w * S - ell * S, ly, ell * S, w * S, "#2e7d32", "none", 0)
            # allowable band 2w..4w
            for m, lab in ((2, "2w"), (4, "4w")):
                xx = lx + lw + w * S - m * w * S
                f.line(xx, ly - 4, xx, ly - 20, GREEN, 1.2)
                f.text(xx, ly - 24, lab, 11, GREEN, "middle", "700")
            f.rect(lx + lw + w * S - 4 * w * S, ly - 16, 2 * w * S, 8, GREEN, "none", 0, op=0.25)
            f.text(lx + lw - 46, ly + 30, "例：ℓ = 3w = 24 mm", 11.5, GREEN, "end", "700")
            f.line(lx + lw - 42, ly + 24, lx + lw - 12, ly + 10, GREEN, 1, arrow=GREEN)
            f.text(lx + 6, ly + lh - 10, "起弧／收弧搬離角點", 11.5, GREEN, weight="600")
    f.text(260, 392, f"立面依比例：1 mm = {S} px；角鋼肢 {LEG_W:g} × {LEG_H:g} mm、w = {w:g} mm → 2w～4w = 16～32 mm", 11.5, MUT, "middle")

    # ---- ③ plan at top level: leg flexes as beam end rotates
    x0 = 590
    f.text(x0 + 140, 28, "③ 為什麼還有上限 4w", 14.5, PURPLE, "middle", "700")
    f.text(x0 + 140, 48, "接合頂部斷面（俯視）", 11.5, MUT, "middle")
    cf = x0 + 30
    f.rect(cf - 20, 70, 20, 230, "#b0bec5", STEEL_D, 1.2)       # column flange (plan)
    f.text(cf - 10, 316, "柱翼板", 11, MUT, "middle")
    yc = 185
    # beam web
    f.rect(cf + 22, yc - 5, 230, 10, "#cfd8dc", STEEL_D, 1.1)
    f.text(cf + 200, yc - 12, "梁腹板", 11, MUT, "middle")
    for sgn in (-1, 1):
        # leg on flange: from web outwards 90mm*0.9
        L = 90 * 0.95
        y_heel = yc + sgn * 5; y_toe = yc + sgn * (5 + L)
        f.rect(cf, min(y_heel, y_toe), 9, abs(y_toe - y_heel), "#90a4ae", STEEL_D, 1)
        # outstanding leg along web
        f.rect(cf, yc + (5 if sgn > 0 else -14), 90, 9, "#90a4ae", STEEL_D, 1)
        # weld at toe
        f.poly([(cf, y_toe), (cf + 10, y_toe + sgn * 0), (cf, y_toe + sgn * 10)], ORANGE, ORANGE, 1)
        # deformed leg (dashed): heel pulled away by delta
        d = 26
        f.path(f"M{cf+4:.1f},{y_toe:.1f} C{cf+4:.1f},{(y_toe+y_heel)/2:.1f} {cf+4+d:.1f},{(y_toe+2*y_heel)/3:.1f} {cf+4+d:.1f},{y_heel:.1f}",
               "none", PURPLE, 1.8, dash="5,3")
    f.line(cf + 110, yc + 30, cf + 140, yc + 30, PURPLE, 2, arrow=PURPLE)
    f.text(cf + 146, yc + 34, "梁端轉動", 11.5, PURPLE, weight="700")
    f.text(cf + 146, yc + 50, "腹板拉離柱面", 11.5, PURPLE)
    f.lines(x0 + 10, 340, [("角鋼肢靠「彎曲」吸收梁端轉角（虛線）。", INK),
                           ("回銲沿頂邊愈長，這段彎曲愈被鎖死 →", INK),
                           ("鉸接變半剛接、產生未計入的端彎矩，", INK),
                           ("回銲段自己先被拉裂。", RED, "700")], 11.5, lh=18)
    return f.svg()


# =====================================================================
# F09  NDT 決策流程
# =====================================================================
def fig_ndt_flow():
    f = Fig(880, 560, "ndt")
    box(f, 440, 36, 220, 46, "銲道完工")
    conn(f, [(440, 59), (440, 82)])
    box(f, 440, 112, 380, 58, "VT 目視（100%，無條件）", ("量銲腳、看咬邊與餘高、確認幾何",), "#e8f5e9", GREEN, "#1b5e20")
    conn(f, [(440, 141), (440, 166)])
    diamond(f, 440, 218, 340, 104, ["是全滲透銲（CJP）嗎？", "＝力流要靠整個斷面傳遞"])
    # yes -> right
    conn(f, [(610, 218), (660, 218), (660, 286)], label="是", lpos=(640, 210), lcol=GREEN)
    box(f, 660, 318, 300, 62, "UT 超音波（內部）", ("怕的是未熔合／未滲透（面積型）",), "#f3e5f5", PURPLE, "#4a148c")
    conn(f, [(660, 349), (660, 372)])
    diamond(f, 660, 420, 300, 94, ["耐震梁柱接頭 CJP？", "（韌性抗彎構架）"], tcol="#e65100")
    conn(f, [(660, 467), (660, 497)], label="是", lpos=(676, 488), lcol=GREEN)
    box(f, 660, 520, 230, 44, "UT 100% 全數，不得抽驗", (), "#ffcdd2", RED, "#b71c1c")
    conn(f, [(810, 420), (836, 420), (836, 497)])
    f.text(822, 412, "否", 12.5, RED, "middle", "700")
    f.rect(800, 498, 72, 44, "#eceff1", "#546e7a", 1.5, rx=8)
    f.lines(836, 516, [("依規範", INK, "700"), ("比例抽驗", INK, "700")], 12, anchor="middle", lh=17)
    # no -> left : surface crack methods
    conn(f, [(270, 218), (190, 218), (190, 286)], label="否（填角銲／PJP）", lpos=(232, 208), lcol=RED)
    box(f, 190, 318, 300, 62, "表面裂縫檢測", ("填角銲幾何不規則，RT 難用；重點在銲趾",), "#e3f2fd", BLUE, "#0d47a1")
    conn(f, [(190, 349), (190, 372)])
    diamond(f, 190, 420, 280, 94, ["母材是鐵磁性的嗎？", "（碳鋼是；沃斯田鐵不鏽鋼否）"], tcol="#e65100")
    conn(f, [(190, 467), (190, 492)], label="是", lpos=(176, 485), lcol=GREEN)
    box(f, 190, 520, 140, 44, "MT 磁粒", (), "#e8f5e9", GREEN, "#1b5e20")
    conn(f, [(330, 420), (360, 420), (360, 497)])
    f.text(345, 412, "否", 12.5, RED, "middle", "700")
    box(f, 360, 520, 110, 44, "PT 液滲", (), "#fff8e1", ORANGE, "#e65100")
    return f.svg()


# =====================================================================
# F10  高拉力螺栓三困境（SS-2004-1）
# =====================================================================
def fig_bolt3():
    f = Fig(880, 470, "b3")
    for x in (293, 587):
        f.line(x, 16, x, 456, "#cfd8dc", 2)
    # ---------- ① 板面不密接 ----------
    cx = 146
    f.text(cx, 30, "① 板面不密接（板厚差）", 15, RED, "middle", "700")
    S = 2.5  # px/mm（依比例）
    # 左板 t=22，右板 t=19 → Δ=3 mm；上蓋板 t=12
    y_base = 160
    f.rect(20, y_base - 22 * S, 122, 22 * S, "#b0bec5", STEEL_D, 1.1)
    f.rect(150, y_base - 19 * S, 122, 19 * S, "#b0bec5", STEEL_D, 1.1)
    top_l = y_base - 22 * S; top_r = y_base - 19 * S
    f.rect(30, top_l - 12 * S, 232, 12 * S, STEEL, STEEL_D, 1.1)
    gap = top_r - top_l
    f.rect(150, top_l, 122, gap, "#ff9800", "#e65100", 1)
    f.line(240, top_l + gap / 2, 262, top_l - 12 * S - 16, "#e65100", 1)
    f.text(262, top_l - 12 * S - 20, "墊片（厚 Δ）", 11.5, "#e65100", "end", "700")
    f.text(35, top_l - 12 * S / 2 + 4, "蓋板", 11, MUT)
    f.text(20, y_base + 16, "t = 22", 10.5, MUT); f.text(272, y_base + 16, "t = 19", 10.5, MUT, "end")
    f.text(cx, y_base + 34, "Δ = 3 mm ≥ 1 mm → 須加墊片", 12, RED, "middle", "700")
    f.text(cx, y_base + 52, "（依比例：1 mm = 2.5 px）", 10.5, MUT, "middle")
    f.rect(16, 222, 262, 92, "#ffebee", "#ef9a9a", 1, rx=8)
    f.lines(28, 244, [("板厚差 < 1 mm：不必處理", INK, "700"),
                      ("板厚差 ≥ 1 mm：加墊片（filler／shim）", INK, "700"),
                      ("（§5.2 只有這一個門檻）", MUT)], 12.5, lh=22)
    f.rect(16, 326, 262, 120, "#fafafa", "#cfd8dc", 1, rx=8)
    f.lines(cx, 350, [("為什麼有縫就不行", INK, "700"),
                      ("夾緊力先拿去把上板壓彎，", MUT), ("真正壓在接觸面的正向力變小", MUT),
                      ("墊片須與母材同等表面處理", RED, "700"), ("否則等於夾入一片低 μ 介面", MUT)],
            12, anchor="middle", lh=19)

    # ---------- ② 孔位偏差 ----------
    cx = 440
    f.text(cx, 30, "② 孔位偏差（M22，標準孔 d+1.5）", 15, ORANGE, "middle", "700")
    s = 3.2         # px/mm
    d, d0, e = 22.0, 23.5, 3.0
    clear = d0 - e
    c1 = (cx - e * s / 2, 100); c2 = (cx + e * s / 2, 100)
    f.circle(*c1, d0 * s / 2, "#e3f2fd", BLUE, 1.6, op=0.85)
    f.circle(*c2, d0 * s / 2, "#fff3e0", ORANGE, 1.6, op=0.75)
    f.circle(cx, 100, d * s / 2, "none", RED, 1.6)
    f.text(cx, 160, "藍／橙＝上、下板孔 Ø23.5（相錯 e）　紅＝螺桿 Ø22", 10.5, MUT, "middle")
    # clear width dim
    xl = c2[0] - d0 * s / 2; xr = c1[0] + d0 * s / 2
    f.line(xl, 100, xr, 100, PURPLE, 1.3, arrow=PURPLE, arrow_start=PURPLE)
    f.text(cx, 94, f"淨開口 {clear:.1f}", 11.5, PURPLE, "middle", "700")
    f.text(cx, 186, f"偏差 e = {e:g} mm：淨開口 {d0:g} − {e:g} = {clear:g} < 22 → 穿不過", 11.5, INK, "middle", "600")
    f.text(cx, 204, f"徒手可穿：e ≤ {d0-d:g} mm；鉸孔 +2 mm 後：e ≤ {d0+2-d:g} mm", 11.5, MUT, "middle")
    f.rect(310, 222, 262, 92, "#fff3e0", "#ffcc80", 1, rx=8)
    f.lines(322, 244, [("❶ 沖梢校正：不得用 ≥ 2.5 kg 鐵鎚", INK, "700"),
                       ("❷ 仍不行 → 鉸孔（reaming）", INK, "700"),
                       ("    擴孔後孔徑 ≤ 設計孔徑 + 2 mm", RED, "700")], 12.5, lh=22)
    f.rect(310, 326, 262, 120, "#ffebee", "#ef9a9a", 1, rx=8)
    f.lines(cx, 350, [("絕對禁止", RED, "700"), ("氣割擴孔（孔壁硬化、粗糙）", INK),
                      ("重鎚強行敲入螺栓", INK), ("以螺栓本身充當沖梢", INK),
                      ("→ 傷螺紋、K 值失準、孔壁受損", MUT)], 12, anchor="middle", lh=19)

    # ---------- ③ 重複使用：拉力–伸長 ----------
    cx = 733
    f.text(cx, 30, "③ 螺栓重複使用", 15, PURPLE, "middle", "700")
    px0, px1, py0, py1 = 620, 860, 56, 196
    X, Y = axes(f, px0, py0, px1, py1, 0, 10, 0, 1.12)
    Fy = 0.9                      # F10T：降伏比約 0.9（以 Fu = 1 正規化）
    T07 = 0.7
    f.line(px0, py1, px1, py1, STEEL_D, 1.2); f.line(px0, py0, px0, py1, STEEL_D, 1.2)
    for v, lab, c in ((1.0, "Fu", MUT), (Fy, "Fy≈0.9Fu", ORANGE), (T07, "0.7Fu", GREEN)):
        f.line(px0, Y(v), px1, Y(v), c, 1, dash="4,3")
        f.text(px0 - 4, Y(v) + 4, lab, 10, c, "end", "700")
    ey = 2.0   # elastic limit elongation (arbitrary units)
    pts = [(X(0), Y(0)), (X(ey), Y(Fy))]
    for i in range(1, 41):
        u = ey + 8 * i / 40
        pts.append((X(u), Y(Fy + (1.0 - Fy) * (1 - math.exp(-(u - ey) / 2.2)))))
    f.path("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts), "none", BLUE, 2.4)
    xA = ey * T07 / Fy
    f.circle(X(xA), Y(T07), 4, GREEN, "#fff", 1.2)
    f.text(X(xA) + 8, Y(T07) + 5, "A", 12, GREEN, weight="700")
    uB = 4.5; vB = Fy + (1.0 - Fy) * (1 - math.exp(-(uB - ey) / 2.2))
    f.circle(X(uB), Y(vB), 4, RED, "#fff", 1.2)
    f.text(X(uB) + 2, Y(vB) + 18, "B", 12, RED, weight="700")
    uP = uB - ey * vB / Fy
    f.line(X(uB), Y(vB), X(uP), Y(0), RED, 1.4, dash="4,3")
    f.line(X(0), py1 + 6, X(uP), py1 + 6, RED, 3)
    f.text(X(uP) + 4, py1 + 11, "永久伸長", 10.5, RED, weight="700")
    f.text(cx + 10, py1 + 28, "螺栓伸長量 →（示意，F10T 以 Fu 正規化）", 10.5, MUT, "middle")
    f.rect(604, 236, 262, 78, "#f3e5f5", "#ce93d8", 1, rx=8)
    f.lines(616, 256, [("A＝規定最小 0.7Fu：仍在彈性段（≈0.78Fy）", INK),
                       ("B＝轉角法實際落點：已推過降伏", INK),
                       ("拆下後留下永久伸長、螺紋已咬合變形", PURPLE, "700")], 11.5, lh=19)
    f.rect(604, 326, 262, 120, "#ffebee", "#ef9a9a", 1, rx=8)
    f.lines(cx + 2, 350, [("結論（施工規範 §5.3.1）", RED, "700"),
                          ("已使用過之螺栓或帶有", INK), ("傷痕銹蝕者，不得再使用", INK, "700"),
                          ("再鎖：K 值偏移 → 扭矩法失準", MUT), ("延性餘裕已用掉 → 轉角法失準", MUT)],
            12, anchor="middle", lh=19)
    return f.svg()


# =====================================================================
# F11  銲道 vs 螺栓：荷重–變形（依文獻曲線形狀，正規化）
# =====================================================================
def fig_weld_bolt():
    f = Fig(880, 440, "wb")
    px0, px1, py0, py1 = 86, 600, 40, 340
    X, Y = axes(f, px0, py0, px1, py1, 0, 10, 0, 1.6)
    w = 8.0
    # --- fillet weld, AISC 360 J2.4 (Lesik–Kennedy) ---
    def weld(theta):
        dm = 0.209 * (theta + 2) ** -0.32 * w
        du = min(1.087 * (theta + 6) ** -0.65 * w, 0.17 * w)
        k = 1.0 + 0.5 * math.sin(math.radians(theta)) ** 1.5
        pts = []
        n = 120
        for i in range(n + 1):
            d = du * i / n
            p = d / dm
            pts.append((d, k * (p * (1.9 - 0.9 * p)) ** 0.3))
        return pts, du, k
    # --- bolt: slip at Rs, then bearing (Fisher curve) after hole clearance ---
    Rs = 0.39          # 滑動荷重 / 承壓極限（M22 A325：0.35×176 / (0.5×825×380) ≈ 0.39）
    dslip0, dc = 0.10, 1.0
    def bolt(d):
        if d <= dslip0:
            return Rs * d / dslip0
        if d <= dc:
            return Rs
        x = d - dc
        return max(Rs, (1 - math.exp(-0.394 * x)) ** 0.55)
    for v in (0, 0.4, 0.8, 1.2, 1.6):
        f.line(px0, Y(v), px1, Y(v), GRID, 1)
        f.text(px0 - 8, Y(v) + 4, f"{v:.1f}", 11, MUT, "end")
    for t in range(0, 11, 2):
        f.text(X(t), py1 + 17, f"{t}", 11, MUT, "middle")
    f.line(px0, py1, px1, py1, STEEL_D, 1.4); f.line(px0, py0, px0, py1, STEEL_D, 1.4)
    f.text((px0 + px1) / 2, py1 + 36, "接合面相對變形 δ (mm)", 12, MUT, "middle")
    f.text(30, (py0 + py1) / 2, "R / 縱向銲極限強度（或螺栓承壓極限）", 11.5, MUT, "middle", rot=-90)
    # bolt curve
    bp = [(X(i * 0.02), Y(bolt(i * 0.02))) for i in range(0, 431)]
    f.path("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in bp), "none", GREEN, 2.6, "7,4")
    f.circle(X(8.6), Y(bolt(8.6)), 4, GREEN, "#fff", 1.2)
    f.text(X(8.6), Y(bolt(8.6)) - 10, "承壓極限 δ≈8.6", 11, GREEN, "middle", "700")
    f.text(X(0.3), Y(Rs) - 8, "滑動", 11, GREEN, weight="700")
    f.text(X(2.3), Y(0.62), "孔隙吃完 → 螺桿頂到孔壁開始承壓", 11, GREEN)
    # welds
    for th, col, lab in ((0, BLUE, "縱向填角銲 θ=0°"), (90, PURPLE, "橫向填角銲 θ=90°")):
        pts, du, k = weld(th)
        f.path("M" + " L".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in pts), "none", col, 2.8)
        ex, ey = X(du), Y(pts[-1][1])
        f.line(ex, ey, ex, py1, col, 1.2, dash="3,3")
        f.text(ex + 5, ey - 4, f"{lab}：δu = {du:.2f} mm 斷裂", 11.5, col, weight="700")
        f.text(ex - 3, ey + 4, "✕", 15, col, "end", "700")
    # what bolts give at weld fracture
    _, du0, _ = weld(0)
    f.circle(X(du0), Y(bolt(du0)), 5, RED, "#fff", 1.6)
    f.text(X(du0) + 8, Y(bolt(du0)) + 28, f"銲道斷時，螺栓只出到 {bolt(du0):.2f}", 11.5, RED, weight="700")
    f.text(X(du0) + 8, Y(bolt(du0)) + 44, "（仍在滑動段，承壓還沒開始）", 11, RED)
    # side panel
    sx = 622
    f.rect(sx, 40, 244, 300, "#fff8e1", "#ffcc80", 1, rx=9)
    f.lines(sx + 14, 64, [("讀圖", "#e65100", "700"),
                          ("銲道在 δ < 1.4 mm 就到頂並斷裂；", INK),
                          ("螺栓的承壓強度要到 δ ≈ 數 mm", INK),
                          ("才發揮。兩者峰值錯開，", INK),
                          ("強度不能直接相加。", RED, "700"), ("", INK),
                          ("銲道斷的那一刻，螺栓只剩", INK),
                          ("滑動抗力（約承壓極限的 4 成），", INK),
                          ("其餘載重瞬間甩給螺栓 → 衝擊滑移。", INK), ("", INK),
                          ("→ 國內規範：新設接合中", INK, "700"),
                          ("   兩者不得共同分擔載重", INK, "700")], 12, lh=20)
    f.text(440, 400, "銲道曲線：AISC 360 §J2.4 的 Lesik–Kennedy 荷重–變形關係（w = 8 mm）；螺栓：滑動荷重取承壓極限之 0.39（M22，μ = 0.35），", 11, MUT, "middle")
    f.text(440, 418, "孔隙 1 mm 後依 Fisher 承壓曲線 R = (1 − e^(−0.394Δ))^0.55。皆為正規化示意，用來看「峰值出現在哪個 δ」，不是用來查強度。", 11, MUT, "middle")
    return f.svg()


# =====================================================================
# F12  防蝕：塗裝屏障 vs 鍍鋅犧牲陽極（電子流向＋電位軸）
# =====================================================================
def fig_corrosion():
    f = Fig(880, 430, "cor")
    f.line(440, 14, 440, 300, "#cfd8dc", 2, dash="6,5")
    for k, (x0, title, col) in enumerate(((20, "油漆：只有屏障", RED), (460, "熱浸鍍鋅：屏障＋犧牲陽極", GREEN))):
        f.text(x0 + 200, 30, title, 15, col, "middle", "700")
        sy = 150; sw = 400
        cx = x0 + 200
        # steel
        f.rect(x0, sy, sw, 70, "#b0bec5", STEEL_D, 1.2)
        f.text(x0 + 12, sy + 58, "鋼材 Fe", 12, INK, weight="600")
        coat = "#90caf9" if k == 0 else "#c5e1a5"
        cs = "#1565c0" if k == 0 else "#558b2f"
        th = 18
        # coating with scratch gap 24px
        f.rect(x0, sy - th, sw / 2 - 12, th, coat, cs, 1)
        f.rect(cx + 12, sy - th, sw / 2 - 12, th, coat, cs, 1)
        f.text(x0 + 12, sy - 5, "漆膜" if k == 0 else "鋅層 Zn", 11.5, cs, weight="700")
        f.rect(cx - 12, sy - th, 24, th, "#e1f5fe", "none", 0)
        # water droplet (electrolyte)
        f.path(f"M{cx-70},{sy-th} Q{cx},{sy-th-60} {cx+70},{sy-th}", "#e1f5fe", "#4fc3f7", 1.2, op=0.9)
        f.text(cx, sy - th - 34, "水膜（電解質）＋ O₂", 11, "#0277bd", "middle", "600")
        if k == 0:
            # pit at scratch
            f.path(f"M{cx-12},{sy} Q{cx},{sy+22} {cx+12},{sy}", "#a1887f", "#6d4c41", 1.2)
            # undercut rust spreading below coating
            for sgn in (-1, 1):
                f.path(f"M{cx+sgn*12},{sy} Q{cx+sgn*40},{sy+6} {cx+sgn*70},{sy}", "#bcaaa4", "#6d4c41", 1)
                f.line(cx + sgn * 44, sy - th - 2, cx + sgn * 44, sy - th - 10, "#6d4c41", 1)
                f.path(f"M{cx+sgn*20},{sy-th} Q{cx+sgn*45},{sy-th-14} {cx+sgn*70},{sy-th}", "none", "#6d4c41", 1.2)
            f.text(cx, sy + 40, "陽極：Fe → Fe²⁺ + 2e⁻（刮傷處開始爛）", 11.5, RED, "middle", "700")
            f.text(cx, sy + 104, "鏽體積膨脹，把兩側漆膜頂起（膜下腐蝕、起泡）", 11.5, RED, "middle")
            f.text(cx, sy + 122, "→ 損傷由刮痕向外擴大", 11.5, RED, "middle", "700")
        else:
            # zinc dissolves around scratch; steel exposed is cathode
            for sgn in (-1, 1):
                xa = cx + sgn * 40
                f.text(xa, sy - th - 4, "Zn²⁺", 10.5, "#33691e", "middle", "700")
                f.line(cx + sgn * 30, sy - 6, cx + sgn * 14, sy - 6, "#33691e", 1.6, arrow="#33691e")
            f.text(cx, sy + 40, "鋅（較負）當陽極：Zn → Zn²⁺ + 2e⁻", 11.5, GREEN, "middle", "700")
            f.text(cx, sy + 58, "電子流入裸露的鐵 → 鐵成為陰極，不溶解", 11.5, GREEN, "middle")
            f.text(cx, sy + 104, "鋅腐蝕產物還會回填刮痕（自癒）", 11.5, GREEN, "middle")
            f.text(cx, sy + 122, "→ 數 mm 級的小刮傷，鐵仍受保護", 11.5, GREEN, "middle", "700")
        if k == 0:
            f.text(cx, sy + 58, "陰極：O₂ + 2H₂O + 4e⁻ → 4OH⁻（周圍鐵面）", 11.5, MUT, "middle")
    # potential axis
    ay = 362
    X = lambda v: 120 + (v + 1.0) / 1.4 * 640    # -1.0 .. +0.4 V
    f.line(X(-1.0), ay, X(0.4), ay, STEEL_D, 1.5, arrow=STEEL_D)
    for v in (-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4):
        f.line(X(v), ay - 4, X(v), ay + 4, STEEL_D, 1)
        f.text(X(v), ay + 18, f"{v:+.1f}" if v else "0", 10.5, MUT, "middle")
    for v, lab, c in ((-0.76, "Zn  −0.76", GREEN), (-0.44, "Fe  −0.44", RED), (0.0, "H₂  0", MUT), (0.34, "Cu  +0.34", ORANGE)):
        f.circle(X(v), ay, 6, c, "#fff", 1.4)
        f.text(X(v), ay - 12, lab, 12, c, "middle", "700")
    f.text(X(-1.0), ay - 34, "標準電極電位 E°（V，vs SHE）：愈負愈活潑", 12, INK, "start", "700")
    f.line(X(-0.76), ay + 30, X(-0.44), ay + 30, PURPLE, 1.6, arrow=PURPLE)
    f.text((X(-0.76) + X(-0.44)) / 2, ay + 46, "電位較負者先被犧牲：鋅保護鐵（ΔE = 0.32 V）", 12, PURPLE, "middle", "700")
    f.text(X(0.34), ay + 46, "銅比鐵正 → 接觸反而害鐵先爛", 11, ORANGE, "middle")
    return f.svg()


# =====================================================================
# F13  不予塗裝五部位（§7.4.5）：每列一個依比例的部位小圖
# =====================================================================
def fig_nopaint():
    f = Fig(880, 500, "np")
    NO = "#e53935"
    hatch = f.hatch(NO, 6, "no")
    rows = [
        ("① 高拉力螺栓「摩阻型」接合之接觸面",
         "理由：塗膜使滑動係數 μ 由 0.35（A 類）掉到約 0.15，摩擦強度不足。承壓型不在此列。", None),
        ("② 工地銲接部位，及其兩側各 100 mm 範圍",
         "理由：漆膜高溫分解 → 氣孔等缺陷、電弧不穩、有害燻煙。", None),
        ("③ 埋入混凝土之構件與埋件",
         "理由：混凝土 pH > 12 使鋼面鈍化；塗膜反而降低握裹力（SRC、鋼承板）。",
         "但書：距混凝土表面 100 mm 深度內仍須塗裝（表層會碳化、開裂進水）。"),
        ("④ 軸件、滾輪等密著接觸面或迴轉面",
         "理由：機件功能面，塗膜妨礙轉動與精確密貼，且易被碾壓剝落。", None),
        ("⑤ 密閉空間之內露面（如封閉箱型斷面內部）",
         "理由：密閉無氧、腐蝕極慢；且密閉空間塗裝之揮發物難排除，有工安風險。", None),
    ]
    y0, dy = 26, 92
    for i, (t, r1, r2) in enumerate(rows):
        y = y0 + i * dy
        ix, iw, ih = 24, 170, 70
        f.rect(ix - 6, y - 4, iw + 12, ih + 8, "#fafcfd", "#e0e0e0", 1, rx=6)
        if i == 0:   # section through lap splice, faying surface hatched
            f.rect(ix + 10, y + 14, 150, 16, STEEL, STEEL_D, 1)
            f.rect(ix + 10, y + 34, 150, 16, STEEL, STEEL_D, 1)
            f.rect(ix + 10, y + 30, 150, 4, hatch, NO, 1)
            for bx in (ix + 50, ix + 120):
                f.rect(bx - 5, y + 6, 10, 52, "#78909c", STEEL_D, 1)
                f.rect(bx - 9, y + 6, 18, 8, "#78909c", STEEL_D, 1)
                f.rect(bx - 9, y + 50, 18, 8, "#78909c", STEEL_D, 1)
            f.text(ix + 85, y + 68, "接觸面", 10, NO, "middle", "700")
        elif i == 1:  # plate with field weld + 100mm each side (to scale 0.6 px/mm)
            s = 0.6
            f.rect(ix + 4, y + 18, 162, 26, STEEL, STEEL_D, 1)
            cx = ix + 85
            f.rect(cx - 100 * s, y + 18, 200 * s, 26, hatch, NO, 1)
            f.rect(cx - 3, y + 18, 6, 26, ORANGE, "#d84315", 1)
            f.dim(cx - 100 * s, y + 56, cx, y + 56, "", NO)
            f.dim(cx, y + 56, cx + 100 * s, y + 56, "", NO)
            f.text(cx - 50 * s, y + 70, "100", 10, NO, "middle", "700")
            f.text(cx + 50 * s, y + 70, "100", 10, NO, "middle", "700")
            f.text(cx, y + 12, "工地銲道", 10, "#d84315", "middle", "700")
        elif i == 2:  # column embedded in concrete
            f.rect(ix + 4, y + 30, 162, 40, "#d7ccc8", "#8d6e63", 1)
            f.text(ix + 10, y + 64, "混凝土", 10, "#5d4037")
            f.rect(ix + 70, y + 2, 30, 68, STEEL, STEEL_D, 1)
            f.rect(ix + 70, y + 54, 30, 16, hatch, NO, 1)
            f.rect(ix + 70, y + 30, 30, 24, "#64b5f6", "#1565c0", 1, op=0.75)
            f.text(ix + 104, y + 46, "須塗 100", 10, BLUE, weight="700")
            f.text(ix + 104, y + 66, "免塗", 10, NO, weight="700")
            f.text(ix + 66, y + 14, "鋼構件", 10, MUT, "end")
        elif i == 3:  # pin through plates (rotating surface)
            f.rect(ix + 10, y + 10, 150, 20, STEEL, STEEL_D, 1)
            f.rect(ix + 10, y + 40, 150, 20, STEEL, STEEL_D, 1)
            f.circle(ix + 85, y + 35, 22, hatch, NO, 1.2)
            f.circle(ix + 85, y + 35, 16, "#90a4ae", STEEL_D, 1)
            f.text(ix + 85, y + 39, "銷", 11, INK, "middle", "700")
            f.path(f"M{ix+118},{y+20} A30,30 0 0 1 {ix+118},{y+50}", "none", PURPLE, 1.4, arrow=PURPLE)
        else:          # closed box section
            f.rect(ix + 50, y + 4, 70, 62, STEEL, STEEL_D, 1)
            f.rect(ix + 58, y + 12, 54, 46, hatch, NO, 1)
            f.text(ix + 85, y + 39, "內面", 11, NO, "middle", "700")
            f.text(ix + 128, y + 30, "外面", 10, MUT)
            f.text(ix + 128, y + 44, "照常塗", 10, MUT)
        tx = 220
        f.text(tx, y + 20, t, 14.5, "#b71c1c", weight="700")
        f.text(tx, y + 42, r1, 12, INK)
        if r2:
            f.text(tx, y + 62, r2, 12, RED, weight="700")
    f.rect(240, 484 - 14, 14, 10, hatch, NO, 1)
    f.text(260, 479, "＝不予塗裝範圍　（小圖 ② 依比例 1 mm = 0.6 px）", 11, MUT)
    return f.svg()


# =====================================================================
# F15  梁柱接頭（SS-2024-4 型式）：立面依比例 ＋ A–A 斷面 ＋ 四部位
# =====================================================================
def fig_joint():
    f = Fig(880, 560, "jt")
    s = 0.42                                    # px / mm
    B, tw_c = 500, 25                           # 箱型柱 □500×25
    d, bf, tf, twb = 600, 200, 25, 12           # H600×200×12×25
    tdia = 28                                   # 內橫隔板厚（≥ 梁翼板厚）
    cx0 = 70; cx1 = cx0 + B * s                 # column outer faces
    yt = 120                                    # beam top
    yb = yt + d * s
    f.text(290, 26, "立面（依比例 1 mm = 0.42 px：□500×25 箱型柱、H600×200×12×25 梁）", 12.5, INK, "middle", "700")
    # column walls
    f.rect(cx0, 44, tw_c * s, 470, STEEL, STEEL_D, 1.2)
    f.rect(cx1 - tw_c * s, 44, tw_c * s, 470, STEEL, STEEL_D, 1.2)
    f.rect(cx0 + tw_c * s, 44, (B - 2 * tw_c) * s, 470, "#f5f7f8", "none", 0)
    f.text((cx0 + cx1) / 2, 506, "箱型柱", 12, MUT, "middle")
    # diaphragms aligned with beam flange centrelines
    for yc in (yt + tf * s / 2, yb - tf * s / 2):
        f.rect(cx0 + tw_c * s, yc - tdia * s / 2, (B - 2 * tw_c) * s, tdia * s, "#b0bec5", STEEL_D, 1)
        for xe in (cx0 + tw_c * s, cx1 - tw_c * s):
            f.rect(xe - 4, yc - tdia * s / 2 - 1, 8, tdia * s + 2, PURPLE, "none", 0)
    f.text((cx0 + cx1) / 2, yt + tf * s / 2 + 26, "內橫隔板（對齊梁翼板）", 11, MUT, "middle")
    # beam
    bx0 = cx1; bx1 = 560
    f.rect(bx0, yt, bx1 - bx0, tf * s, STEEL, STEEL_D, 1.2)
    f.rect(bx0, yb - tf * s, bx1 - bx0, tf * s, STEEL, STEEL_D, 1.2)
    f.rect(bx0 + 6, yt + tf * s, bx1 - bx0 - 6, (d - 2 * tf) * s, "#e3e8eb", STEEL_D, 0.8)
    # break line
    f.path(f"M{bx1},{yt-8} L{bx1},{yt+120} L{bx1-8},{yt+128} L{bx1+8},{yt+136} L{bx1},{yt+144} L{bx1},{yb+8}", "none", STEEL_D, 1.2)
    # weld access holes (r = 35 mm)
    r = 35 * s
    for yy, sgn in ((yt + tf * s, 1), (yb - tf * s, -1)):
        f.path(f"M{bx0+6},{yy} L{bx0+6+r},{yy} A{r},{r} 0 0 {1 if sgn>0 else 0} {bx0+6},{yy+sgn*r} Z", "#fff", STEEL_D, 1)
    # flange CJP (single bevel 35°) + backing bar
    for yy, sgn in ((yt, 1), (yb, -1)):
        tt = tf * s
        if sgn > 0:
            f.poly([(bx0, yy), (bx0 + tt * math.tan(math.radians(35)) + 2, yy), (bx0 + 2, yy + tt), (bx0, yy + tt)], "#ff7043", "#bf360c", 1)
            f.rect(bx0, yy + tt, 22, 4, "#5d4037", "none", 0)
        else:
            f.poly([(bx0, yy - tt), (bx0 + tt * math.tan(math.radians(35)) + 2, yy - tt), (bx0 + 2, yy), (bx0, yy)], "#ff7043", "#bf360c", 1)
            f.rect(bx0, yy - tt - 4, 22, 4, "#5d4037", "none", 0)
    # shear tab + bolts (5 × M22 @ 75)
    tab_y0 = yt + tf * s + 40; tab_h = 360 * s
    f.rect(bx0, tab_y0, 100 * s, tab_h, "none", ORANGE, 1.4, dash="4,3")
    f.rect(bx0, tab_y0, 3, tab_h, "#ff7043", "none", 0)
    for i in range(5):
        f.circle(bx0 + 55 * s, tab_y0 + (30 + 75 * i) * s, 24 * s / 2, "#fff", STEEL_D, 1.2)
    f.text(bx0 + 170, tab_y0 + tab_h - 10, "H 型鋼梁", 12, MUT)
    # numbered markers
    def tag(x, y, n, col):
        f.circle(x, y, 11, col, "#fff", 1.5); f.text(x, y + 4.5, n, 12.5, "#fff", "middle", "700")
    tag(bx0 + 30, yt - 18, "1", RED); f.line(bx0 + 22, yt - 10, bx0 + 8, yt + 2, RED, 1.2)
    tag(bx0 + 30, yb + 20, "1", RED); f.line(bx0 + 22, yb + 12, bx0 + 8, yb - 2, RED, 1.2)
    tag(cx0 - 22, yt + 4, "2", PURPLE); f.line(cx0 - 12, yt + 6, cx0 + tw_c * s, yt + tf * s / 2, PURPLE, 1.2)
    tag(cx0 - 22, yb - 4, "2", PURPLE); f.line(cx0 - 12, yb - 6, cx0 + tw_c * s, yb - tf * s / 2, PURPLE, 1.2)
    tag(bx0 + 120, tab_y0 + 40, "3", ORANGE); f.line(bx0 + 109, tab_y0 + 42, bx0 + 44, tab_y0 + 44, ORANGE, 1.2)
    tag(cx1 - 34, yt + 150, "4", INK); f.line(cx1 - 24, yt + 150, cx1 - 4, yt + 150, INK, 1.2)
    f.text(bx0 + 34, yt + tf * s + r + 14, "扇形銲接孔", 10.5, MUT)
    f.text(bx0 + 26, yt + tf * s + 9, "背襯板", 10, "#5d4037")
    # section mark A–A
    ya = yt + tf * s / 2
    for xx in (cx0 - 46, cx1 + 6):
        pass

    # ---------- plan A–A ----------
    ps = 0.30
    px, py = 640, 64
    f.text(px + B * ps / 2 + 20, 48, "A–A 斷面（隔板高程，俯視）", 12.5, INK, "middle", "700")
    f.rect(px, py, B * ps, B * ps, STEEL, STEEL_D, 1.2)
    f.rect(px + tw_c * ps, py + tw_c * ps, (B - 2 * tw_c) * ps, (B - 2 * tw_c) * ps, "#b0bec5", STEEL_D, 1)
    f.text(px + B * ps / 2, py + B * ps / 2 + 4, "內橫隔板", 11.5, INK, "middle", "600")
    # ESW on left/right sides (closing plates), arc weld on top/bottom sides
    for xe in (px + tw_c * ps, px + B * ps - tw_c * ps):
        f.rect(xe - 3, py + tw_c * ps, 6, (B - 2 * tw_c) * ps, PURPLE, "none", 0)
    for ye in (py + tw_c * ps, py + B * ps - tw_c * ps):
        f.rect(px + tw_c * ps + 3, ye - 2, (B - 2 * tw_c) * ps - 6, 4, "#ff7043", "none", 0)
    # beam flange stub
    f.rect(px + B * ps, py + B * ps / 2 - bf * ps / 2, 60, bf * ps, "#cfd8dc", STEEL_D, 1)
    f.text(px + B * ps + 30, py + B * ps / 2 + 4, "梁翼板", 10.5, MUT, "middle")
    f.text(px - 6, py + B * ps + 22, "紫＝ESW：封板後無法自柱內施銲的兩側", 11, PURPLE, weight="700")
    f.text(px - 6, py + B * ps + 40, "橙＝合攏前自柱內以電弧銲完成", 11, "#d84315", weight="600")

    # ---------- legend of four locations ----------
    lx, ly = 600, 270
    items = [
        ("1", RED, "梁翼板 CJP（工地銲）", "根部未熔合、背襯板缺口、HAZ 脆斷", "UT 100% 全數＋VT；背襯板移除後補銲"),
        ("2", PURPLE, "內橫隔板 ESW（工廠銲）", "大熱輸入 → HAZ 晶粒粗大、未熔合", "自柱外 UT（RT 進不去）＋MT"),
        ("3", ORANGE, "腹板剪力板高拉力螺栓（工地）", "預拉力不足、滑動、漏鎖", "扭矩抽查／TC 螺栓看斷尾／DTI"),
        ("4", INK, "柱壁母材（Z 向受拉）", "翼板拉力穿過板厚 → 層狀撕裂", "板厚 ≥ 40 mm 用 SN-C；必要時 UT"),
    ]
    for i, (n, c, t, risk, chk) in enumerate(items):
        y = ly + i * 68
        f.circle(lx + 10, y - 4, 11, c, "#fff", 1.5); f.text(lx + 10, y + 0.5, n, 12.5, "#fff", "middle", "700")
        f.text(lx + 28, y, t, 13, c, weight="700")
        f.text(lx + 28, y + 19, "風險：" + risk, 11.5, INK)
        f.text(lx + 28, y + 37, "檢測：" + chk, 11.5, MUT)
    return f.svg()


# =====================================================================
# F16  U2-3 說明題答題流程
# =====================================================================
def fig_answer_flow():
    f = Fig(880, 600, "af")
    box(f, 440, 34, 260, 44, "看到一題 U2-3 說明題")
    conn(f, [(440, 56), (440, 80)])
    diamond(f, 440, 130, 420, 100, ["題目問的是「怎麼做」", "還是「為什麼不能這樣做」？"])
    conn(f, [(230, 130), (190, 130), (190, 190)], label="怎麼做", lpos=(206, 120), lcol=BLUE)
    conn(f, [(650, 130), (690, 130), (690, 190)], label="為什麼不行", lpos=(682, 120), lcol=PURPLE)
    f.rect(30, 192, 320, 108, "#e3f2fd", BLUE, 1.7, rx=9)
    f.lines(190, 218, [("用「三道防線」開架構", "#0d47a1", "700")], 14, anchor="middle")
    f.lines(46, 244, ["① 事前：材料／銲材／表面處理／程序書", "② 事中：溫度、尺寸、順序、環境條件", "③ 事後：VT → MT/PT → UT/RT，附理由"], 12.5, lh=20)
    f.rect(530, 192, 320, 108, "#f3e5f5", PURPLE, 1.7, rx=9)
    f.lines(690, 218, [("先指出「被破壞的設計假設」", "#4a148c", "700")], 14, anchor="middle")
    f.lines(546, 244, ["μ？夾緊力 Tb？斷面連續性？", "韌性儲備？塑鉸位置？握裹力？", "→ 再說規範怎麼把它守回來"], 12.5, lh=20)
    # merge into diamond 2 from top
    f.poly([(190, 300), (190, 330), (690, 330), (690, 300)], "none", "#546e7a", 1.9, close=False)
    conn(f, [(440, 330), (440, 352)])
    diamond(f, 440, 400, 380, 92, ["題目牽涉「耐震」", "或「梁柱接頭」嗎？"])
    conn(f, [(440, 446), (440, 472)], label="是", lpos=(456, 464), lcol=GREEN)
    box(f, 440, 498, 420, 50, "補上容量設計＋Northridge 因果鏈", ("SN 鋼材 Fy 上限 · RBS · CJP UT 100% · 40 mm 門檻",), "#ffcdd2", RED, "#b71c1c")
    conn(f, [(630, 400), (800, 400), (800, 560), (652, 560)], label="否", lpos=(716, 392), lcol=RED)
    conn(f, [(440, 523), (440, 538)])
    box(f, 440, 562, 420, 44, "收尾：每一項都補「一句話理由」", ("只列名稱通常每項扣一半分",), "#e8f5e9", GREEN, "#1b5e20")
    return f.svg()
