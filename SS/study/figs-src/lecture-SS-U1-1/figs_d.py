from lib import *


def box(cx, y, w, lines, fill, stroke, head_col=None, rx=8, lh=21, pad=12, bold_first=True):
    h = pad * 2 + lh * len(lines) - 6
    o = [R(cx - w / 2, y, w, h, fill, stroke, 1.6, rx=rx)]
    for i, ln in enumerate(lines):
        txt, col, wt = (ln + (None, None))[:3] if isinstance(ln, tuple) else (ln, None, None)
        col = col or INK
        wt = wt or ('bold' if (i == 0 and bold_first) else None)
        o.append(T(cx, y + pad + 12 + i * lh, txt, 13 if i == 0 else 12.5, col, 'middle', wt))
    return ''.join(o), y + h


def diamond(cx, cy, w, h, lines, fill=WARN2, stroke=WARN):
    o = [P([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)], stroke, 1.6, fill=fill, close=True)]
    n = len(lines)
    for i, t in enumerate(lines):
        o.append(T(cx, cy + 5 + (i - (n - 1) / 2) * 20, t, 13 if i == 0 else 12, '#e65100' if i == 0 else MUT, 'middle', 'bold' if i == 0 else None))
    return ''.join(o)


def fig9_1():
    W, H = 790, 740
    o = []
    G = '#546e7a'
    # top
    o.append(R(255, 12, 280, 40, AC, None, rx=20))
    o.append(T(395, 38, '讀題：軸力是拉還是壓？', 15, '#fff', 'middle', 'bold'))
    xl, xr = 190, 590
    o.append(P([(395, 52), (395, 66), (xl, 66), (xl, 84)], G, 2)); o.append(head(xl, 86, 1.5708, G, 10))
    o.append(P([(395, 66), (xr, 66), (xr, 84)], G, 2)); o.append(head(xr, 86, 1.5708, G, 10))
    # ---------------- tension
    o.append(R(xl - 140, 88, 280, 36, TEN, None, rx=6)); o.append(T(xl, 112, '拉力 → 面積帳本', 14.5, '#fff', 'middle', 'bold'))
    y = 124
    W1 = 320
    steps = [
        [('① 全斷面降伏 GSY', TEN, 'bold'), 'φ = 0.90，*F*_{y}·*A*_{g}'],
        [('② 淨斷面斷裂 NSF', TEN, 'bold'), '*A*_{n}：扣 *d*_{b} + 0.3 cm；交錯加 *s*²/4*g*',
         ('*U* = 1 − *x̄*/*L*（銲接也要乘）', COMP, 'bold'), ('板類縱向銲：*U* 查 *l*/*w*，且 *l* ≥ *w*', COMP, None), 'φ = 0.75，*F*_{u}·*U*·*A*_{n}'],
        [('③ 塊狀剪力 BSR', TEN, 'bold'), '先畫塊體 → 數剪力面、拉力面的孔', '主式、上限式取小，φ = 0.75'],
        [('④ 螺栓本身（螺栓接合時）', TEN, 'bold'), '螺栓剪力、孔承壓 2.4*dtF*_{u}', ('SS-2005-1：螺栓剪力 71.8 vs 控制 68.5 tf', MUT, None)],
    ]
    for st in steps:
        o.append(L(xl, y, xl, y + 14, G, 2)); o.append(head(xl, y + 16, 1.5708, G, 9))
        b, y = box(xl, y + 16, W1, st, TEN2, TEN)
        o.append(b)
    o.append(L(xl, y, xl, y + 14, G, 2)); o.append(head(xl, y + 16, 1.5708, G, 9))
    o.append(R(xl - 130, y + 16, 260, 40, '#1b5e20', None, rx=6))
    o.append(T(xl, y + 42, '取最小 → 控制模式', 14.5, '#fff', 'middle', 'bold'))
    # ---------------- compression
    o.append(R(xr - 140, 88, 280, 36, COMP, None, rx=6)); o.append(T(xr, 112, '壓力 → 幾何帳本', 14.5, '#fff', 'middle', 'bold'))
    o.append(L(xr, 124, xr, 138, G, 2)); o.append(head(xr, 140, 1.5708, G, 9))
    W2 = 360
    b, y = box(xr, 140, W2, [('⓪ 斷面性質', COMP, 'bold'), '型錄標準件 → 直接查 *A*、*I*、*r*', ('組合柱／SRC → 先做 §8（平行軸、*F*_{my}、*E*_{m}）', MUT, None)], '#fff', COMP)
    o.append(b)
    csteps = [
        [('① 定 *K*：有側移？無側移？', COMP, 'bold'), '兩個平面各自判讀邊界（SS-2013-3）', '端部條件表／對位圖 *G* = Σ(*I*_{c}/*L*_{c})/Σ(*I*_{b}/*L*_{b})', ('基礎固接 *G* = 1、鉸接 *G* = 10；有靠桿要放大', COMP, None)],
        [('② 強、弱軸都算 *KL*/*r*', COMP, 'bold'), '分段側撐逐段算，取最大者控制'],
        [('③ 寬厚比（是否細長肢）', COMP, 'bold'), ('非細長 → *Q* = 1；細長 → 折減 *Q*', MUT, None)],
    ]
    for st in csteps:
        o.append(L(xr, y, xr, y + 14, G, 2)); o.append(head(xr, y + 16, 1.5708, G, 9))
        b, y = box(xr, y + 16, W2, st, COMP2, COMP)
        o.append(b)
    o.append(L(xr, y, xr, y + 14, G, 2)); o.append(head(xr, y + 16, 1.5708, G, 9))
    dy2 = y + 16 + 38
    o.append(diamond(xr, dy2, 330, 76, ['題目要 LRFD 還是 ASD？', '（決定載重要不要放大）']))
    bxL, bxR, bw = xr - 95, xr + 95, 180
    yb = dy2 + 72
    o.append(P([(xr, dy2 + 38), (xr, dy2 + 50), (bxL, dy2 + 50), (bxL, yb - 2)], G, 2)); o.append(head(bxL, yb, 1.5708, G, 9))
    o.append(P([(xr, dy2 + 50), (bxR, dy2 + 50), (bxR, yb - 2)], G, 2)); o.append(head(bxR, yb, 1.5708, G, 9))
    b, _ = box(bxL, yb, bw, [('LRFD（φ_{c} = 0.85）', COMP, 'bold'), 'λ_{c} = (*KL*/*r*π)√(*F*_{y}/*E*)', 'λ_{c} ≤ 1.5：0.658^{λc²}·*F*_{y}', 'λ_{c} > 1.5：0.877*F*_{y}/λ_{c}²', ('φ_{c}*P*_{n} = 0.85*F*_{cr}*A*_{g}', COMP, 'bold')], '#ffcdd2', COMP)
    o.append(b)
    b, _ = box(bxR, yb, bw, [('ASD', COMP, 'bold'), '*C*_{c} = √(2π²*E*/*F*_{y})', '≤ *C*_{c}：拋物線 ÷ FS', '> *C*_{c}：12π²*E*/23(*KL*/*r*)²', ('*P*_{a} = *F*_{a}*A*_{g}', COMP, 'bold')], '#ffcdd2', COMP)
    o.append(b)
    return svg(W, H, '\n'.join(o), '拉力與壓力桿件解題流程')
