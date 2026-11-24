"""lecture-SD-U2-3.html 的全部 SVG 圖（座標全部由 calcs.py 的數值算出）。
用法：python gen_figs.py ../../../study/lecture-SD-U2-3.html"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common')); sys.path.insert(0, HERE)
from figkit import *  # noqa
import calcs as K

BLUE, RED, GRN, ORG, PUR, GRY = '#1565C0', '#C62828', '#2E7D32', '#EF6C00', '#6A1B9A', '#78909C'

def beam_panel(cv, x0, y0, Lpx, title, loads, defl, amp, lcol, sub):
    """簡支梁：x0,y0 左支承像素；loads(ξ)→相對大小；defl(ξ)→撓度形狀（已正規化）"""
    T(cv, x0 + Lpx/2, y0 - 118, title, 14, C['text'], 'middle', '700')
    T(cv, x0 + Lpx/2, y0 - 98, sub, 12, C['muted'])
    xi = np.linspace(0, 1, 13)
    for s in xi[1:-1]:
        h = 52 * loads(s)
        px_arrow(cv, x0 + s*Lpx, y0 - 22 - h, x0 + s*Lpx, y0 - 6, lcol, 2, 8)
    ss = np.linspace(0, 1, 160)
    px_line(cv, x0, y0, x0 + Lpx, y0, C['ghost'], 3)
    px_poly(cv, [(x0 + s*Lpx, y0 + amp*defl(s)) for s in ss], BLUE, 3)
    for X, kind in ((x0, 'pin'), (x0 + Lpx, 'roll')):
        px_polygon(cv, [(X, y0), (X - 9, y0 + 15), (X + 9, y0 + 15)], '#fff', C['member'], 1.6)
        if kind == 'roll':
            px_line(cv, X - 12, y0 + 21, X + 12, y0 + 21, C['member'], 1.6)
        else:
            px_line(cv, X - 13, y0 + 15, X + 13, y0 + 15, C['member'], 1.6)

def fig_two_roles():
    cv = new(900, 330)
    st = lambda s: float(np.interp(s, K.x, K.ust_n))
    beam_panel(cv, 60, 190, 340, '振動時：慣性力 ∝ (w/g)·ω²·φ(x)', lambda s: math.sin(math.pi*s),
               lambda s: math.sin(math.pi*s), 70, PUR, '中間大、兩端零（形狀＝振態）')
    beam_panel(cv, 500, 190, 340, '規範的做法：把重量 w 當外力推一次', lambda s: 0.62,
               st, 70, RED, '均勻分佈（就是自重，轉到所求方向）')
    T(cv, 230, 290, '藍線：真正的第一振態 sin(πx/L)', 12, BLUE)
    T(cv, 670, 290, f'藍線：w 推出的靜變位（正規化）', 12, BLUE)
    T(cv, 450, 318, f'兩組力的分佈不同，推出的形狀幾乎一樣：正規化後最大差 {K.dmax*100:.2f}%  → 拿靜變位當振態',
      13, C['text'], 'middle', '700')
    return cv.svg()

def fig_shapes():
    cv = new(900, 300)
    p = Plot(cv, 300, 50, 520, 190, (0.88, 1.02), (0, 4))
    rows = [('靜變位代入規範式（γ/β）', K.ratio_code, BLUE),
            ('跨中集中載重的撓度形狀', K.r_point, GRN),
            ('拋物線 x(L−x)', K.r_para, ORG),
            ('精確振態 sin(πx/L)', K.r_sine, C['member'])]
    for v in (0.88, 0.90, 0.92, 0.94, 0.96, 0.98, 1.00, 1.02):
        X = p.X(v); px_line(cv, X, 50, X, 240, '#E6EBF1', 1); T(cv, X, 256, f'{v:.2f}', 11.5, C['muted'])
    px_line(cv, p.X(1.0), 40, p.X(1.0), 244, RED, 1.6, '5 4')
    T(cv, p.X(1.0) + 6, 34, 'T = T₁（精確）', 12, RED, 'start', '700')
    for i, (lab, v, col) in enumerate(rows):
        yc = 50 + 190 * (i + 0.5) / 4
        px_rect(cv, p.X(0.88), yc - 13, p.X(v) - p.X(0.88), 26, col, 'none', 0, 3)
        T(cv, 290, yc, lab, 12.5, C['text'], 'end')
        T(cv, p.X(v) + 6 if v < 0.99 else p.X(v) - 6, yc, f'{v:.4f}', 12.5, '#fff' if v >= 0.99 else C['text'],
          'start' if v < 0.99 else 'end', '700')
    T(cv, 560, 282, '假設形狀算出的週期 T_R / T₁（簡支梁）：全部 ≤ 1，形狀越像振態越接近 1', 12.5, C['text'], 'middle', '700')
    return cv.svg()

def fig_weights():
    cv = new(900, 270)
    items = list(K.case_T.items())
    p = Plot(cv, 90, 40, 760, 160, (0, 4), (0, 1.6))
    for v in (0, 0.5, 1.0, 1.5):
        Y = p.Y(v); px_line(cv, 90, Y, 850, Y, '#E6EBF1', 1); T(cv, 82, Y, f'{v:g}', 11.5, C['muted'], 'end')
    T(cv, 90, 26, '週期 T / T₀', 12.5, C['text'], 'start')
    cols = [BLUE, RED, GRN, GRY]
    notes = ['質量 w/g、推力 w', 'γ×4、β×2：高估 41%', '質量不變 → 週期不變', '質量、推力都 ×2']
    for i, ((lab, v), col, nt) in enumerate(zip(items, cols, notes)):
        xc = 90 + 760 * (i + 0.5) / 4
        px_rect(cv, xc - 55, p.Y(v), 110, p.Y(0) - p.Y(v), col, 'none', 0, 3)
        T(cv, xc, p.Y(v) - 10, f'{v:.3f}', 13, col, 'middle', '700')
        T(cv, xc, 220, lab, 12, C['text'])
        T(cv, xc, 240, nt, 11.5, C['muted'])
    px_line(cv, 90, p.Y(0), 850, p.Y(0), C['member'], 1.4)
    return cv.svg()

def fig_bridge():
    cv = new(900, 400)
    L = 150; X0 = 110; yd = 120; yb = yd + L          # 墩高 = 跨長 = L
    xs = [X0 + i*L for i in range(4)]
    # 振動單元底色
    px_rect(cv, xs[0] + 6, yd - 46, 2*L - 12, L + 74, 'rgba(21,101,192,0.08)', BLUE, 1.4, 10, '6 4')
    T(cv, xs[1], yd - 58, '振動單元：第 2 墩（雙鉸）＋兩跨上構（質量 2mL）', 12.5, BLUE, 'middle', '700')
    # 上構（梁縫在墩頂）
    gap = 7
    segs = [(xs[0] - 70, xs[0] - gap, True), (xs[0] + gap, xs[1] - gap, False), (xs[1] + gap, xs[2] - gap, False),
            (xs[2] + gap, xs[3] - gap, False), (xs[3] + gap, xs[3] + 70, True)]
    for a, b, ext in segs:
        px_line(cv, a, yd - 10, b, yd - 10, C['member'], 6)
        if ext:
            xe = a if a < xs[0] else b
            T(cv, xe + (-6 if a < xs[0] else 6), yd - 10, '≈', 18, C['muted'], 'end' if a < xs[0] else 'start')
    kinds = ['roll', 'pin', 'roll', 'pin']                 # 墩頂兩側支承（判讀 #2、#3）
    for X, k in zip(xs, kinds):
        for side in (-1, 1):
            cx = X + side*gap*1.9
            if k == 'pin':
                px_polygon(cv, [(cx, yd - 6), (cx - 5, yd + 2), (cx + 5, yd + 2)], '#fff', C['member'], 1.4)
            else:
                cv.parts.append(f'<circle cx="{cx:.1f}" cy="{yd-2:.1f}" r="4" fill="#fff" stroke="{C["member"]}" stroke-width="1.4"/>')
        px_line(cv, X - 12, yd + 3, X + 12, yd + 3, C['member'], 3)
        # 墩柱
        px_line(cv, X, yd + 3, X, yb, C['member2'] if k == 'roll' else C['member'], 4)
        for j in range(5):
            px_line(cv, X - 14 + j*7, yb + 8, X - 8 + j*7, yb, C['member'], 1.2)
        px_line(cv, X - 16, yb, X + 16, yb, C['member'], 2)
        T(cv, X, yb + 26, {'roll': '雙滾：不受縱向力', 'pin': '雙鉸：承接兩側上構'}[k], 11.5,
          C['muted'] if k == 'roll' else C['text'])
    for i in range(3):
        T(cv, (xs[i] + xs[i+1]) / 2, yd - 26, 'L', 13, C['muted'], 'middle', '400', True)
    T(cv, xs[3] + 34, (yd + yb) / 2, '墩高 L', 12, C['muted'], 'start')
    # 縱向慣性力：跨 1、跨 2 → 第 2 墩；跨 3、右延續段 → 第 4 墩
    for a, b, tgt in ((xs[0], xs[1], xs[1]), (xs[1], xs[2], xs[1]), (xs[2], xs[3], xs[3])):
        mid = (a + b) / 2
        px_arrow(cv, mid - 30 if tgt > mid else mid + 30, yd - 32, mid + 20 if tgt > mid else mid - 20, yd - 32, RED, 2.2, 8)
    # 第 2 墩撓曲（懸臂、頂端可轉）：u = U0(3η² − η³)/2
    U0 = 34; eta = np.linspace(0, 1, 60)
    px_poly(cv, [(xs[1] + U0*(3*e*e - e**3)/2, yb - e*L) for e in eta], BLUE, 2.4, '5 3')
    px_arrow(cv, xs[1], yd + 40, xs[1] + U0, yd + 40, BLUE, 1.8, 7)
    T(cv, xs[1] - 12, yd + 70, 'U₀ = W/k，k = 3EI/L³', 12, BLUE, 'end')
    # 右側：係數比較
    T(cv, 790, 92, 'T = 係數 × L²√(m/EI)', 12.5, C['text'], 'middle', '700')
    for i, (lab, v, col) in enumerate((('正確：1 墩 + 2 跨', K.coef_unit, BLUE), ('舊解：4 墩並聯 + 3 跨', K.coef_old, GRY))):
        yy = 130 + i*70
        px_rect(cv, 712, yy, 22*v, 26, col, 'none', 0, 3)
        T(cv, 712 + 22*v + 6, yy + 13, f'{v:.3f}', 13, col, 'start', '700')
        T(cv, 712, yy + 42, lab, 11.5, C['muted'], 'start')
    T(cv, 450, 386, '縱向：每跨上構的慣性力只經「鉸」那一端傳到墩頂；滾支承的墩縱向不出力 → 不能把四墩當並聯', 12.5, C['text'], 'middle', '700')
    return cv.svg()

def fig_tripartite():
    cv = new(900, 470)
    p = Plot(cv, 90, 40, 560, 370, (0.01, 10), (1, 1000), True, True)
    for v in (0.01, 0.03, 0.1, 0.3, 1, 3, 10):
        X = p.X(v); px_line(cv, X, 40, X, 410, '#EEF1F5', 1); T(cv, X, 426, f'{v:g}', 11.5, C['muted'])
    for v in (1, 3, 10, 30, 100, 300, 1000):
        Y = p.Y(v); px_line(cv, 90, Y, 650, Y, '#EEF1F5', 1); T(cv, 82, Y, f'{v:g}', 11.5, C['muted'], 'end')
    # 等 Spa 線（斜率 +1）與等 Sd 線（斜率 −1），只畫在框內
    def clip_line(f, col, lab, at):
        Ts = np.logspace(-2, 1, 300); pts = [(t, f(t)) for t in Ts if 1 <= f(t) <= 1000]
        if len(pts) > 1:
            px_poly(cv, [p.P(t, v) for t, v in pts], col, 1, '3 3', op=0.8)
            t = at if any(abs(math.log10(q[0]/at)) < .2 for q in pts) else pts[len(pts)//2][0]
            X, Y = p.P(t, f(t)); T(cv, X + 3, Y - 6, lab, 10.5, col, 'start')
    for g_ in (0.1, 1, 10):
        clip_line(lambda t, a=g_*981: K.spv_from_spa(t, a), RED, f'S_pa={g_:g}g', 0.05 if g_ == 10 else (0.2 if g_ == 1 else 2))
    for d in (1, 10, 100):
        clip_line(lambda t, s=d: K.spv_from_sd(t, s), GRN, f'S_d={d}cm', {1: 0.02, 10: 0.08, 100: 1.0}[d])
    pts = [p.P(t, v) for t, v in K.tri]
    px_poly(cv, pts, BLUE, 3.2)
    for (X, Y), nm in zip(pts, 'abcdef'):
        cv.parts.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="4.5" fill="{BLUE}" stroke="#fff" stroke-width="1.5"/>')
        T(cv, X - 6 if nm == 'f' else X - 8, Y + 18 if nm == 'f' else Y - 10, nm, 13, BLUE, 'end', '700')
    seg = [('常數 S_pa＝PGA', 0, 1, 10, 16, 'start'), ('過渡', 1, 2, 10, 8, 'start'), ('常數 S_pa＝α_A·PGA', 2, 3, 12, 14, 'start'),
           ('常數 S_pv＝α_V·PGV', 3, 4, 0, -14, 'middle'), ('常數 S_d', 4, 5, 6, -12, 'start')]
    for lab, i, j, dx, dy, anc in seg:
        (X1, Y1), (X2, Y2) = pts[i], pts[j]
        T(cv, (X1 + X2) / 2 + dx, (Y1 + Y2) / 2 + dy, lab, 11, C['text'], anc)
    T(cv, 370, 452, '週期 T（s，對數）', 12.5, C['text'])
    T(cv, 90, 26, 'S_pv（cm/s，對數）', 12.5, C['text'], 'start')
    # 軸向：等 Spa 線往左上變大、等 Sd 線往右上變大
    px_arrow(cv, 760, 240, 712, 192, RED, 2, 8); T(cv, 706, 182, 'S_pa 增大', 12, RED, 'end', '700')
    px_arrow(cv, 790, 240, 838, 192, GRN, 2, 8); T(cv, 844, 182, 'S_d 增大', 12, GRN, 'start', '700')
    T(cv, 775, 270, 'log S_pv = log S_pa + log T − log 2π', 11, C['muted'])
    T(cv, 775, 288, '→ 等 S_pa 線斜率 +1', 11, RED)
    T(cv, 775, 312, 'log S_pv = log S_d + log 2π − log T', 11, C['muted'])
    T(cv, 775, 330, '→ 等 S_d 線斜率 −1', 11, GRN)
    T(cv, 775, 366, '示意：PGA = 1 g', 11, C['muted'])
    T(cv, 775, 382, 'Newmark–Hall 比例', 11, C['muted'])
    return cv.svg()

def fig_codespec():
    cv = new(900, 345)
    p = Plot(cv, 70, 40, 520, 230, (0, 3), (0, 0.7))
    p.frame([0, 0.5, 1, 1.5, 2, 2.5, 3], [0, 0.2, 0.4, 0.6], '週期 T（s）', 'S_aD', yfmt='{:.1f}')
    T0 = K.T0
    segs = [(np.linspace(0, 0.2*T0, 30), ORG, '② 較短週期 ↔ b→c（過渡）'),
            (np.linspace(0.2*T0, T0, 30), RED, '③ 短週期 S_DS ↔ c→d（常數 S_pa）'),
            (np.linspace(T0, 3, 200), GRN, '④ 中長週期 S_D1/T ↔ d→e（常數 S_pv）')]
    for Ts, col, lab in segs: p.curve(Ts, K.SaD(Ts), col, 3)
    p.dot(0, K.SDS*0.4, 6, PUR)
    T(cv, p.X(0.30), p.Y(0.66), 'S_DS', 12, RED, 'start', '700')
    T(cv, p.X(1.6), p.Y(0.27), 'S_D1/T', 12, GRN, 'start', '700')
    for Tm, lab in ((0.2*T0, '0.2T₀'), (T0, 'T₀')):
        px_line(cv, p.X(Tm), p.Y(0), p.X(Tm), p.Y(K.SDS), C['dim'], 1, '3 3')
        T(cv, p.X(Tm) + 4, p.Y(0) - 10, lab, 11, C['muted'], 'start')
    T(cv, 610, 44, '● ① 零週期 0.4S_DS ↔ a→b（PGA）', 11.5, PUR, 'start', '700')
    for i, (Ts, col, lab) in enumerate(segs):
        T(cv, 610, 70 + i*26, lab, 11.5, col, 'start', '700')
    T(cv, 610, 70 + 3*26, '（無）↔ e→f（常數 S_d）', 11.5, GRY, 'start', '700')
    T(cv, 610, 70 + 4*26 + 6, '表中沒有位移控制段：', 11.5, C['muted'], 'start')
    T(cv, 610, 70 + 5*26, 'S_D1/T 一路延伸 → 長週期偏保守', 11.5, C['muted'], 'start')
    T(cv, 330, 334, f'示意值 S_DS = {K.SDS}、S_D1 = {K.SD1}（T₀ = {T0:.3f} s）', 12, C['muted'])
    return cv.svg()

def fig_flow():
    cv = new(900, 560)
    BX, BW = 300, 300
    box(cv, BX, 40, 260, 44, ['讀題：要「推導」還是「算 T」？'], '#ECEFF1', '#546E7A', bold_first=True)
    diamond(cv, BX, 120, 230, 70, ['只要推導 2.01？'])
    edge(cv, [(BX, 62), (BX, 85)])
    box(cv, 760, 120, 240, 58, ['T_max = V_max', '½ω²∫(w/g)u² = ½∫w u → §1'], '#F3E5F5', '#6A1B9A')
    edge(cv, [(BX + 115, 120), (640, 120)], '是', (BX + 128, 108))
    diamond(cv, BX, 220, 250, 70, ['所求方向？', '（縱向／橫向）'])
    edge(cv, [(BX, 155), (BX, 185)], '否', (BX + 8, 172))
    box(cv, BX, 312, 300, 58, ['看支承：滾的不傳該向力、鉸的傳', '→ 圈出振動單元（§3）'])
    edge(cv, [(BX, 255), (BX, 283)])
    diamond(cv, BX, 400, 230, 70, ['上構在該向', '可視為剛體？'])
    edge(cv, [(BX, 341), (BX, 365)])
    box(cv, 120, 490, 210, 58, ['等位移 U₀ = W/k', 'γ/β = U₀ → T = 2π√(M/k)'], '#E8F5E9', '#2E7D32')
    box(cv, 480, 490, 230, 58, ['求 w 推出的 u(x)（撓度曲線）', '積分 β、γ（§4）'], '#E8F5E9', '#2E7D32')
    edge(cv, [(BX - 115, 400), (120, 400), (120, 461)], '是', (BX - 128, 388), anchor='end')
    edge(cv, [(BX + 115, 400), (480, 400), (480, 461)], '否', (BX + 128, 388))
    box(cv, 760, 470, 230, 96, ['收尾檢查', '① u 用 m（係數 2.006）', '② 施加力 ≠ 質量時改權重', '③ T 約 0.3–1.5 s？'],
        '#FFF8E1', '#F9A825', bold_first=True)
    edge(cv, [(595, 490), (645, 490)])
    edge(cv, [(120, 519), (120, 545), (760, 545), (760, 518)])
    edge(cv, [(760, 149), (760, 422)])
    return cv.svg()

FIGS = dict(f0=fig_two_roles, f1=fig_weights, f2=fig_bridge, f3=fig_shapes, f4=fig_tripartite, f5=fig_codespec, f6=fig_flow)

if __name__ == '__main__':
    html = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..', '..', 'study', 'lecture-SD-U2-3.html')
    embed(html, {k: f() for k, f in FIGS.items()})
