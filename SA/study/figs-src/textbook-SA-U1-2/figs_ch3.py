# -*- coding: utf-8 -*-
"""第 3 章：桁架 I（二力桿、節點法、零力桿）。所有桿力由 calcs.solve_truss 算出。"""
from draw import *  # noqa
from calcs import (N17, B17, F17, R17, N10, B10, F10, R10, N13, B13, F13, R13,
                   N164, B164, RULE_ZERO_164, S2)
import math


def sgn(v, d=1):
    """+16、−20、0 這種帶號字串（用真正的減號）。"""
    if abs(v) < 1e-9:
        return '0'
    s = f'{abs(v):.{d}f}'.rstrip('0').rstrip('.')
    return ('+' if v > 0 else '−') + s


def bar_color(v):
    if v is None:
        return STEEL
    if abs(v) < 1e-9:
        return STEEL
    return TEN if v > 0 else COMP


def truss(f, nodes, bars, F=None, fmax=None, vals=None, voff=None, wmin=2.6, wmax=8.0,
          dash_zero=True, node_r=5.5, show_nodes=True, hide=()):
    """畫桁架。F：桿力（拉正）；vals：{桿: 標籤字串}；voff：{桿: (dx, dy)} 標籤位移。"""
    o = ''
    P_ = {k: f(*v) for k, v in nodes.items()}
    fmax = fmax or (max(abs(v) for v in F.values()) if F else 1)
    for b in bars:
        b = ''.join(b) if not isinstance(b, str) else b
        p, q = _ends(b, nodes)
        if b in hide:
            continue
        v = F.get(b) if F else None
        c = bar_color(v)
        if v is None:
            o += L(*P_[p], *P_[q], STEEL, 5)
        elif abs(v) < 1e-9:
            o += L(*P_[p], *P_[q], STEEL, 2.4, '7 5' if dash_zero else None)
        else:
            o += L(*P_[p], *P_[q], c, wmin + (wmax - wmin) * abs(v) / fmax)
    if vals:
        for b, s in vals.items():
            p, q = _ends(b, nodes)
            mx, my = (P_[p][0] + P_[q][0]) / 2, (P_[p][1] + P_[q][1]) / 2
            dx, dy = (voff or {}).get(b, (0, 0))
            v = F.get(b) if F else None
            c = INK if v is None else (MUT if abs(v) < 1e-9 else bar_color(v))
            w = 9.2 * len(s) + 12
            o += R(mx + dx - w / 2, my + dy - 13, w, 24, '#fff', c, 1.1, 6)
            o += T(mx + dx, my + dy + 5, s, 15, c, 'middle', 'bold')
    if show_nodes:
        for k, (x, y) in P_.items():
            o += C(x, y, node_r, '#fff', INK, 1.6)
    return o


def _ends(b, nodes):
    """把 'L0M1'、'AB'、'ke' 拆成兩個節點名。"""
    for i in range(1, len(b)):
        if b[:i] in nodes and b[i:] in nodes:
            return b[:i], b[i:]
    raise KeyError(b)


def labels(f, nodes, off, size=16, c=KEY):
    o = ''
    for k, (dx, dy) in off.items():
        x, y = f(*nodes[k])
        o += T(x + dx, y + dy, k, size, c, 'middle', 'bold')
    return o


def legend(x, y):
    o = L(x, y, x + 34, y, TEN, 6) + T(x + 42, y + 5, '拉（＋）', 15, TEN, 'start', 'bold')
    o += L(x + 130, y, x + 164, y, COMP, 6) + T(x + 172, y + 5, '壓（−）', 15, COMP, 'start', 'bold')
    o += L(x + 260, y, x + 294, y, STEEL, 2.4, '7 5') + T(x + 302, y + 5, '零力桿', 15, MUT, 'start', 'bold')
    o += T(x + 380, y + 5, '線寬 ∝ |桿力|', 15, MUT, 'start')
    return o


# ───────────────────────────────────────────── 3.1
def fig3_1():
    """種子 S2：二力桿只受軸力。"""
    W, H = 900, 400
    o = ''
    # (a) 斜的力會讓桿轉
    o += T(150, 32, '(a) 力若是斜的', 16, INK, 'middle', 'bold')
    ax, ay, bx, by = 55, 250, 245, 120
    o += L(ax, ay, bx, by, STEEL, 9) + C(ax, ay, 7, '#fff', INK, 2) + C(bx, by, 7, '#fff', INK, 2)
    o += T(ax - 6, ay + 28, 'i', 16, INK, 'middle', 'bold', True) + T(bx + 14, by - 12, 'j', 16, INK, 'middle', 'bold', True)
    o += A(bx, by, bx + 30, by + 72, MUT, 2.4, 11, dash='6 4')
    o += T(bx + 36, by + 86, '斜的力', 15, MUT, 'start')
    o += moment(ax, ay, 42, cw=True, c=COMP, start=70, span=110)
    o += T(150, 310, '對 *i* 取矩：斜的力有力臂', 15, COMP, 'middle')
    o += T(150, 334, '→ Σ*M*_{i} ≠ 0，桿會轉', 15, COMP, 'middle', 'bold')
    # (b) 只能沿桿：拉或壓
    o += T(450, 32, '(b) 所以兩端的力只能沿著桿', 16, INK, 'middle', 'bold')
    for k, (yy, c, out, name) in enumerate(((120, TEN, True, '拉力（向外拉）'), (230, COMP, False, '壓力（向內推）'))):
        x1, x2 = 360, 540
        o += L(x1, yy, x2, yy, STEEL, 9) + C(x1, yy, 7, '#fff', INK, 2) + C(x2, yy, 7, '#fff', INK, 2)
        if out:
            o += A(x1 - 8, yy, x1 - 58, yy, c, 3, 12) + A(x2 + 8, yy, x2 + 58, yy, c, 3, 12)
        else:
            o += A(x1 - 58, yy, x1 - 10, yy, c, 3, 12) + A(x2 + 58, yy, x2 + 10, yy, c, 3, 12)
        o += T(450, yy - 18, name, 15, c, 'middle', 'bold')
    o += T(450, 310, '大小相等、方向相反、在同一直線上', 15, INK, 'middle')
    o += T(450, 334, '一根桿只剩 1 個未知數：軸力 *F*', 15, KEY, 'middle', 'bold')
    # (c) 從節點看
    o += T(760, 32, '(c) 從節點看（全書約定）', 16, INK, 'middle', 'bold')
    jx, jy = 760, 175
    for ang, c in ((20, TEN), (160, COMP), (270, STEEL)):
        a = math.radians(ang)
        ex, ey = jx + 110 * math.cos(a), jy - 110 * math.sin(a)
        o += L(jx, jy, ex, ey, STEEL, 7)
    a = math.radians(20)
    o += A(jx + 18 * math.cos(a), jy - 18 * math.sin(a), jx + 72 * math.cos(a), jy - 72 * math.sin(a), TEN, 3, 12)
    a = math.radians(160)
    o += A(jx + 76 * math.cos(a), jy - 76 * math.sin(a), jx + 20 * math.cos(a), jy - 20 * math.sin(a), COMP, 3, 12)
    o += C(jx, jy, 9, '#fff', INK, 2)
    o += T(jx + 60, jy - 50, '離開節點', 15, TEN, 'start', 'bold') + T(jx + 60, jy - 30, '＝拉', 15, TEN, 'start', 'bold')
    o += T(jx - 60, jy - 50, '指向節點', 15, COMP, 'end', 'bold') + T(jx - 60, jy - 30, '＝壓', 15, COMP, 'end', 'bold')
    o += T(760, 310, '未知桿力一律先畫「離開節點」', 15, INK, 'middle')
    o += T(760, 334, '算出負號就是壓力', 15, KEY, 'middle', 'bold')
    o += L(300, 50, 300, 350, GRID, 1.5) + L(610, 50, 610, 350, GRID, 1.5)
    o += R(40, 356, 820, 36, KEY2, KEY, 1.3, 8)
    o += T(450, 380, '種子 S2：兩端是鉸、中間沒有載重的桿，力只能順著桿走（S1 對一端取矩就推得出來）', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '二力桿')


# ───────────────────────────────────────────── 3.2
def fig3_2():
    """斜桿：力三角形與幾何三角形相似。以 SA-2017-1 的 CD 桿（3-4-5、F = −20）為例。"""
    W, H = 900, 380
    o = ''
    F = abs(F17['CD'])
    # 幾何三角形（左）
    s = 44
    x0, y0 = 90, 300
    o += T(200, 34, '(a) 桿的幾何（m）', 16, AC, 'middle', 'bold')
    p0, p1, p2 = (x0, y0), (x0 + 3 * s, y0), (x0 + 3 * s, y0 - 4 * s)
    o += P([p0, p1, p2], AC, 1.6, fill=AC2, close=True)
    o += L(*p0, *p2, STEEL, 8)
    o += T(x0 + 1.5 * s, y0 + 26, 'Δ*x* = 3', 16, AC, 'middle', 'bold')
    o += T(x0 + 3 * s + 12, y0 - 2 * s + 5, 'Δ*y* = 4', 16, AC, 'start', 'bold')
    o += T(x0 + 1.5 * s - 20, y0 - 2 * s - 10, '*L* = 5', 16, AC, 'end', 'bold')
    # 力三角形（中）
    sf = 9.5
    fx, fy = F * 3 / 5, F * 4 / 5
    x1, y1 = 400, 300
    q0, q1, q2 = (x1, y1), (x1 + fx * sf, y1), (x1 + fx * sf, y1 - fy * sf)
    o += T(500, 34, '(b) 桿力的分量（kN）', 16, COMP, 'middle', 'bold')
    o += P([q0, q1, q2], None, fill=COMP2, close=True)
    o += A(*q0, *q1, COMP, 2.4, 11) + A(*q1, *q2, COMP, 2.4, 11) + A(*q0, *q2, COMP, 3.4, 13)
    o += T(x1 + fx * sf / 2, y1 + 26, f'*F*_{{x}} = {fx:g}', 16, COMP, 'middle', 'bold')
    o += T(x1 + fx * sf + 12, y1 - fy * sf / 2 + 5, f'*F*_{{y}} = {fy:g}', 16, COMP, 'start', 'bold')
    o += T(x1 + fx * sf / 2 - 22, y1 - fy * sf / 2 - 10, f'*F* = {F:g}', 16, COMP, 'end', 'bold')
    # 結論框（右）
    o += R(640, 90, 245, 210, KEY2, KEY, 1.5, 10)
    o += T(762, 122, '兩個三角形相似', 16, KEY, 'middle', 'bold')
    o += T(762, 160, '*F*/*L* = *F*_{x}/Δ*x* = *F*_{y}/Δ*y*', 15, INK, 'middle')
    o += T(762, 196, f'{F:g}/5 = {fx:g}/3 = {fy:g}/4 = {F / 5:g}', 15, INK, 'middle')
    o += T(762, 236, '不必算角度、', 15, MUT, 'middle')
    o += T(762, 260, '不必查 sin、cos', 15, MUT, 'middle')
    o += T(450, 360, '力只能順著桿走（S2）⇒ 力的方向就是桿的方向 ⇒ 力三角形是幾何三角形放大 4 倍（這根桿 *F*/*L* = 4 kN/m）', 15, INK, 'middle')
    return svg(W, H, o, '斜桿分量比例')


# ───────────────────────────────────────────── 3.3 SA-2017-1
F17_ = Frame(250, 395, 40)


def _loads17(f):
    P_ = {k: f(*v) for k, v in N17.items()}
    o = force(P_['C'], 180, 56, COMP, 2.8, '12 kN', 15, (-8, -8))
    o += force(P_['B'], 180, 56, COMP, 2.8, '9 kN', 15, (-8, -8))
    o += pin(*P_['A']) + pin(*P_['E'])
    return o


def fig3_3():
    """SA-2017-1：節點法的順序（每一站只剩兩個未知）。"""
    W, H = 900, 470
    f = F17_
    o = T(W / 2, 30, 'SA-2017-1：從「只剩兩個未知」的節點開始，一站一站往下走', 17, INK, 'middle', 'bold')
    o += truss(f, N17, B17)
    o += _loads17(f)
    o += labels(f, N17, dict(A=(-30, 0), B=(-18, 26), C=(-18, -12), D=(18, -12), E=(30, 0)))
    P_ = {k: f(*v) for k, v in N17.items()}
    # 尺寸
    o += dim(P_['A'][0] - 150, P_['A'][1], P_['B'][0] - 150, P_['B'][1], '4 m', MUT, 0, 14, side=1)
    o += dim(P_['B'][0] - 150, P_['B'][1], P_['C'][0] - 150, P_['C'][1], '4 m', MUT, 0, 14, side=1)
    o += dim(P_['A'][0], P_['A'][1] + 48, P_['D'][0], P_['A'][1] + 48, '3 m', MUT, 0, 14)
    o += dim(P_['D'][0], P_['A'][1] + 48, P_['E'][0], P_['A'][1] + 48, '3 m', MUT, 0, 14)
    # 順序徽章
    order = [('C', '①', (30, -6)), ('E', '②', (34, -26)), ('D', '③', (30, -26)), ('B', '④', (30, 30)), ('A', '⑤', (-36, -30))]
    for k, n, (dx, dy) in order:
        x, y = P_[k][0] + dx, P_[k][1] + dy
        o += C(x, y, 15, KEY, None) + T(x, y + 6, n, 16, '#fff', 'middle', 'bold')
    # 右側說明
    rows = ['① C：接 BC、CD 兩根 → 2 個未知', '② E：DE ＋ 反力 *E*_{x}（*E*_{y} 已由整體求得）',
            '③ D：剩 AD、BD 兩根', '④ B：剩 AB 一根', '⑤ A：全部已知 → 拿來驗算']
    o += R(560, 70, 330, 196, '#fff', GRID, 1.4, 10)
    o += T(725, 96, '每一站只解 2 個未知', 16, KEY, 'middle', 'bold')
    for i, s in enumerate(rows):
        o += T(574, 128 + i * 30, s, 15, INK, 'start')
    o += R(560, 280, 330, 96, KEY2, KEY, 1.4, 10)
    o += T(725, 306, '先用整體：Σ*M*_{A} = 0', 15, KEY, 'middle', 'bold')
    o += T(725, 334, f'*E*_{{y}} = (12·8 + 9·4)/6 = {R17[("E", 1)]:g} kN ↑', 15, INK, 'middle')
    o += T(725, 360, '*A*_{x}、*E*_{x} 整體分不開 → 交給節點', 15, INK, 'middle')
    return svg(W, H, o, 'SA-2017-1 節點順序')


def fig3_4():
    """節點 C 的力多邊形：三個力頭尾相接成封閉三角形。"""
    W, H = 900, 400
    o = ''
    # (a) 節點 C 自由體
    o += T(200, 32, '(a) 節點 C 的自由體', 16, INK, 'middle', 'bold')
    cx, cy = 210, 150
    o += C(cx, cy, 9, '#fff', INK, 2)
    # CD 朝向 D (3,-4)/5；BC 朝向 B (0,-1)
    ux, uy = 3 / 5, 4 / 5           # SVG: 向右、向下
    o += L(cx, cy, cx + 140 * ux, cy + 140 * uy, STEEL, 7, '0') + L(cx, cy, cx, cy + 150, STEEL, 7)
    o += A(cx - 70, cy, cx - 12, cy, COMP, 3, 12) + T(cx - 76, cy + 5, '12 kN', 15, COMP, 'end', 'bold')
    o += A(cx + 14 * ux, cy + 14 * uy, cx + 80 * ux, cy + 80 * uy, MUT, 2.6, 12)
    o += T(cx + 92 * ux + 8, cy + 80 * uy + 4, '*F*_{CD}', 16, INK, 'start', 'bold')
    o += A(cx, cy + 14, cx, cy + 80, MUT, 2.6, 12)
    o += T(cx - 10, cy + 72, '*F*_{BC}', 16, INK, 'end', 'bold')
    o += T(200, 340, '兩個未知都先畫「離開節點」（假設拉）', 15, MUT, 'middle')
    # (b) 力多邊形（比例尺 8 px/kN）
    o += T(620, 32, '(b) 頭尾相接，一定要繞回起點', 16, INK, 'middle', 'bold')
    s = 8.0
    p0 = (575, 255)
    p1 = (p0[0] + 12 * s, p0[1])                       # 12 kN →
    Fcd = F17['CD']                                     # −20：實際方向指向 C（向左上）
    p2 = (p1[0] + Fcd * ux * s, p1[1] + Fcd * uy * s)  # 沿 C→D 方向乘負號 = 往左上
    o += P([p0, p1, p2], None, fill=KEY2, close=True)
    o += A(*p0, *p1, COMP, 3, 12) + T((p0[0] + p1[0]) / 2, p0[1] + 24, '12 kN（已知）', 15, COMP, 'middle', 'bold')
    o += A(*p1, *p2, COMP, 3, 12)
    o += T((p1[0] + p2[0]) / 2 + 14, (p1[1] + p2[1]) / 2 - 4, f'*F*_{{CD}} = {abs(Fcd):g}', 15, COMP, 'start', 'bold')
    o += T((p1[0] + p2[0]) / 2 + 14, (p1[1] + p2[1]) / 2 + 18, '指向節點 → 壓', 15, COMP, 'start')
    Fbc = F17['BC']
    o += A(*p2, *p0, TEN, 3, 12)
    o += T(p0[0] - 12, (p0[1] + p2[1]) / 2 + 5, f'*F*_{{BC}} = {Fbc:g}', 15, TEN, 'end', 'bold')
    o += T(p0[0] - 12, (p0[1] + p2[1]) / 2 + 27, '向下＝離開 C → 拉', 15, TEN, 'end')
    o += R(470, 300, 410, 64, '#fff', GRID, 1.3, 8)
    o += T(675, 326, '這個三角形就是 3-4-5：12 是「3」那一邊', 15, INK, 'middle')
    o += T(675, 350, f'⇒ 每份 4，*F*_{{BC}} = 4×4 = {Fbc:g}，*F*_{{CD}} = 4×5 = {abs(Fcd):g}', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '節點 C 力多邊形')


def fig3_5():
    """SA-2017-1 全部桿力。"""
    W, H = 900, 480
    f = Frame(230, 350, 38)
    o = T(W / 2, 30, 'SA-2017-1 全部桿力（kN，由節點法算出）', 17, INK, 'middle', 'bold')
    vals = {b: sgn(F17[b]) for b in B17}
    voff = dict(AB=(-34, 0), BC=(-34, 0), BD=(0, -18), AD=(18, 20), CD=(28, -6), DE=(30, 6))
    o += truss(f, N17, B17, F17, vals=vals, voff=voff)
    o += _loads17(f)
    o += labels(f, N17, dict(A=(-30, 0), B=(-18, 26), C=(-18, -12), D=(18, -14), E=(30, 0)))
    P_ = {k: f(*v) for k, v in N17.items()}
    ax, ay = P_['A']; ex, ey = P_['E']
    o += A(ax + 10, ay + 46, ax + 10, ay + 92, TEN, 2.6, 11) + T(ax + 18, ay + 84, f'{abs(R17[("A", 1)]):g} ↓', 15, TEN, 'start', 'bold')
    o += A(ax - 22, ay + 30, ax - 70, ay + 30, TEN, 2.6, 11) + T(ax - 74, ay + 35, f'{abs(R17[("A", 0)]):g} ←', 15, TEN, 'end', 'bold')
    o += A(ex, ey + 70, ex, ey + 28, TEN, 2.6, 11) + T(ex + 10, ey + 64, f'{R17[("E", 1)]:g} ↑', 15, TEN, 'start', 'bold')
    o += A(ex + 64, ey + 30, ex + 18, ey + 30, TEN, 2.6, 11) + T(ex + 70, ey + 35, f'{abs(R17[("E", 0)]):g} ←', 15, TEN, 'start', 'bold')
    o += legend(400, 462)
    o += R(560, 160, 330, 150, KEY2, KEY, 1.4, 10)
    o += T(725, 188, '檢查（用沒用過的方程）', 16, KEY, 'middle', 'bold')
    o += T(574, 220, f'節點 A：Σ*F*_{{y}} = −22 + 16 + 0.8×7.5 = 0', 15, INK, 'start')
    o += T(574, 250, f'整體：*A*_{{x}} + *E*_{{x}} = −4.5 − 16.5 = −21', 15, INK, 'start')
    o += T(574, 280, '＝ −(12 + 9)，水平也平衡', 15, INK, 'start')
    o += T(725, 340, 'BD = −9 剛好頂住 B 點的 9 kN', 15, COMP, 'middle', 'bold')
    o += T(725, 364, '（D 接四根桿，零力桿口訣用不上）', 15, MUT, 'middle')
    return svg(W, H, o, 'SA-2017-1 桿力')


# ───────────────────────────────────────────── SA-2010-1
F10_ = Frame(95, 365, 58)


def fig3_6():
    """SA-2010-1：節點鏈 A→E→B，未知數帶著走。"""
    W, H = 900, 470
    f = F10_
    o = T(W / 2, 30, 'SA-2010-1：沒有節點只剩兩個未知 → 讓未知數「帶著走」', 17, INK, 'middle', 'bold')
    vals = {b: sgn(F10[b] / S2) + '√2' if abs(abs(F10[b]) - 10 * S2) < 1e-6 or abs(abs(F10[b]) - 20 * S2) < 1e-6 else sgn(F10[b]) for b in B10}
    voff = dict(AB=(0, -18), AC=(-34, -4), AE=(-30, 8), EB=(30, 8), BF=(36, 0), CD=(0, -16), DE=(0, -16), EF=(0, -16),
                CG=(-30, 0), GD=(-36, 4), DH=(36, 4), GH=(0, 18), HF=(40, 14))
    o += truss(f, N10, B10, F10, vals=vals, voff=voff)
    P_ = {k: f(*v) for k, v in N10.items()}
    o += pin(*P_['G']) + roller_wall(P_['B'][0] + 2, P_['B'][1])
    hx, hy = P_['H']
    o += A(hx, hy + 8, hx, hy + 56, COMP, 2.8, 11) + T(hx + 10, hy + 50, '30 kN', 15, COMP, 'start', 'bold')
    o += labels(f, N10, dict(G=(-20, 22), H=(-16, 24), C=(-18, -8), D=(-8, -14), E=(8, -14), F=(16, 22), A=(-4, -14), B=(-6, -16)))
    o += legend(40, 446)
    o += R(520, 70, 370, 260, '#fff', GRID, 1.4, 10)
    o += T(705, 96, '節點鏈（拉為正，以 *F*_{AC} 當變數）', 16, KEY, 'middle', 'bold')
    rows = ['A：Σ*F*_{y} → *F*_{AE} = −*F*_{AC}', '　　Σ*F*_{x} → *F*_{AB} = √2 *F*_{AC}',
            'E：Σ*F*_{y} → *F*_{EB} = −*F*_{AE} = *F*_{AC}', 'B：Σ*F*_{x}（牆的反力 30 ←）',
            '　　−(√2 + 1/√2)*F*_{AC} = 30', f'⇒ *F*_{{AC}} = −10√2（壓）', 'B：Σ*F*_{y} → *F*_{BF} = +10（拉）']
    for i, s in enumerate(rows):
        o += T(536, 128 + i * 28, s, 15, KEY if i == 5 else INK, 'start', 'bold' if i == 5 else None)
    o += R(520, 344, 370, 76, KEY2, KEY, 1.4, 10)
    o += T(705, 372, 'G 接 CG、GD、GH 三根桿', 15, KEY, 'middle', 'bold')
    o += T(705, 398, '漏看 GH 就會誤判出一串零力桿', 15, INK, 'middle')
    return svg(W, H, o, 'SA-2010-1 節點鏈')


# ───────────────────────────────────────────── 3.4 零力桿
def fig3_7():
    """零力桿兩條規則＝垂直方向的 ΣF。"""
    W, H = 900, 400
    o = ''
    for k, (title, sub) in enumerate((('規則 1：兩桿、不共線、沒有外力', '⇒ 兩根都是 0'),
                                      ('規則 2：三桿、其中兩根共線、沒有外力', '⇒ 第三根是 0'))):
        ox = 15 + k * 445
        o += R(ox, 15, 425, 370, '#fff', GRID, 1.4, 10)
        o += T(ox + 212, 44, title, 16, INK, 'middle', 'bold')
        o += T(ox + 212, 70, sub, 16, KEY, 'middle', 'bold')
        jx, jy = ox + 200, 220
        if k == 0:
            o += L(jx, jy, jx + 170, jy, STEEL, 7) + L(jx, jy, jx - 80, jy - 110, STEEL, 7)
            o += T(jx + 150, jy + 26, '桿 1', 15, INK, 'middle') + T(jx - 92, jy - 112, '桿 2', 15, INK, 'end')
            o += L(jx, jy - 120, jx, jy + 110, AC, 1.6, '6 5')
            o += A(jx + 120, jy + 60, jx + 120, jy + 14, AC, 2.4, 11)
            o += T(jx + 130, jy + 62, '垂直於桿 1', 15, AC, 'start')
            o += T(ox + 20, 330, '垂直於桿 1：只有桿 2 有分量 ⇒ *F*_{2} = 0', 15, INK, 'start')
            o += T(ox + 20, 356, '再沿桿 1：剩 *F*_{1} 自己 ⇒ *F*_{1} = 0', 15, INK, 'start')
        else:
            o += L(jx - 170, jy, jx + 170, jy, STEEL, 7) + L(jx, jy, jx + 70, jy - 120, STEEL, 7)
            o += T(jx - 150, jy + 26, '桿 1', 15, INK, 'middle') + T(jx + 150, jy + 26, '桿 2', 15, INK, 'middle')
            o += T(jx + 82, jy - 120, '桿 3', 15, INK, 'start')
            o += A(jx - 150, jy - 10, jx - 150, jy - 70, AC, 2.4, 11)
            o += T(jx - 140, jy - 54, '取垂直於 1、2 的方向', 15, AC, 'start')
            o += T(ox + 20, 330, '垂直於 1、2：只有桿 3 有分量 ⇒ *F*_{3} = 0', 15, INK, 'start')
            o += T(ox + 20, 356, '1、2 不一定是 0：*F*_{1} = *F*_{2}', 15, INK, 'start')
        o += C(jx, jy, 9, '#fff', INK, 2)
    return svg(W, H, o, '零力桿規則')


F13_ = Frame(110, 400, 9.4)


def fig3_8():
    """SA-2013-1：隱藏的零力桿 bl、kb。"""
    W, H = 900, 480
    f = F13_
    o = T(W / 2, 30, 'SA-2013-1：l 點的 a–l–k 共線 → bl = 0；接著 b 點 → kb = 0', 17, INK, 'middle', 'bold')
    ask = ['ke', 'dk', 'ck', 'bk', 'lk']
    vals = {'ke': '−7√2', 'dk': sgn(F13['dk']), 'ck': '+√2', 'bk': '0', 'lk': '−8√5', 'bl': '0'}
    voff = dict(ke=(30, 16), dk=(-30, -4), ck=(-10, -30), bk=(0, -16), lk=(34, 2), bl=(-6, 16))
    o += truss(f, N13, B13, F13, fmax=20, vals=vals, voff=voff)
    P_ = {k: f(*v) for k, v in N13.items()}
    o += pin(*P_['a']) + pin(*P_['i'])
    for k, w in dict(c=5, d=10, e=10, f=10, g=5).items():
        o += force(P_[k], 90, 38, COMP, 2.4, str(w), 15, (12, 4), 'start')
    o += labels(f, N13, dict(a=(-18, 6), l=(16, 18), b=(-16, 6), k=(18, 22), c=(-16, -6), d=(-14, 24),
                             e=(0, 28), f=(-14, 24), j=(-16, 20), g=(16, -10), h=(16, 6), i=(18, 8)), 16, KEY)
    # 共線提示
    o += L(*P_['a'], *f(12, 24), KEY, 1.4, '4 4')
    o += legend(40, 458)
    o += R(520, 300, 370, 140, KEY2, KEY, 1.4, 10)
    o += T(705, 326, '題目問的 5 根全部圍著 k', 15, KEY, 'middle', 'bold')
    o += T(536, 354, f'反力（三鉸，對 e 取矩）：*A*_{{x}} = {R13[("a", 0)]:g}、*A*_{{y}} = {R13[("a", 1)]:g}', 15, INK, 'start')
    o += T(536, 382, 'a → al；l → lk = al、bl = 0；b → kb = 0', 15, INK, 'start')
    o += T(536, 410, 'd → dk；c → ck；k 剩 ke 一根', 15, INK, 'start')
    return svg(W, H, o, 'SA-2013-1 零力桿')


F164_ = Frame(80, 440, 100)


def fig3_9():
    """SA-2016-4：口訣只抓到 3 根；試解＋檢查找出 24 根。"""
    W, H = 900, 540
    f = F164_
    o = T(W / 2, 30, 'SA-2016-4：四個 100 kN 各走最短的路；只有 AE 受力，其餘 24 根是零力桿', 17, INK, 'middle', 'bold')
    F = {b: (100.0 if b == 'AE' else 0.0) for b in B164}
    vals = {'AE': '+100'}
    o += truss(f, N164, B164, F, fmax=100, vals=vals, voff=dict(AE=(30, 0)), show_nodes=False, wmax=7)
    P_ = {k: f(*v) for k, v in N164.items()}
    # 口訣抓到的三根：紫色圈
    for b in RULE_ZERO_164:
        p, q = _ends(b, N164)
        mx, my = (P_[p][0] + P_[q][0]) / 2, (P_[p][1] + P_[q][1]) / 2
        o += C(mx, my, 13, 'none', KEY, 2.2)
    # 梁 MNO 與彈簧
    m, n, oo = P_['M'], P_['N'], P_['O']
    o += R(m[0], m[1] - 6, oo[0] - m[0], 12, STEEL3, INK, 1.4, 2)
    hx, hy = P_['H']
    zz = [(hx, hy)]
    for i in range(1, 8):
        t = i / 8
        x = hx + (m[0] - hx) * t + (10 if i % 2 else -10) * 0.7
        y = hy + (m[1] - hy) * t + (0 if i % 2 else 0)
        zz.append((x, y))
    zz.append(m)
    o += P(zz, INK, 1.6)
    o += T((hx + m[0]) / 2 + 22, (hy + m[1]) / 2 + 2, '*k*', 16, INK, 'start', 'bold', True)
    for k in N164:
        if k not in ('M', 'N', 'O'):
            o += C(*P_[k], 5, '#fff', INK, 1.5)
    o += pin(m[0], m[1] + 6) + roller(oo[0], oo[1] + 6)
    # 支承 A、C 倒掛，D 正立
    for k in ('A', 'C'):
        x, y = P_[k]
        o += P([(x, y), (x - 11, y - 16), (x + 11, y - 16)], INK, 1.5, fill='#fff', close=True) + hatch_ground(x - 17, y - 16, 34, INK, down=False)
    o += pin(*P_['D'])
    # 載重
    o += force(P_['A'], 180, 54, COMP, 2.6, '100', 15, (-6, -8))
    o += force(P_['D'], 180, 54, COMP, 2.6, '100', 15, (-6, -8))
    o += A(P_['E'][0], P_['E'][1] + 6, P_['E'][0], P_['E'][1] + 60, COMP, 2.6, 11)
    o += T(P_['E'][0] - 8, P_['E'][1] + 56, '100', 15, COMP, 'end', 'bold')
    o += force(P_['N'], 90, 50, COMP, 2.6, '100', 15, (0, -8))
    lab = dict(A=(16, 24), B=(0, -28), C=(4, 34), D=(4, -14), E=(16, 22), F=(14, -10), G=(16, -10), H=(4, -16),
               I=(-16, 6), J=(18, 6), K=(-16, 6), L=(18, 22), P=(14, 22), M=(-14, -14), N=(16, 22), O=(16, -14))
    o += labels(f, N164, lab, 15, KEY)
    o += legend(40, 520)
    o += R(640, 70, 250, 120, '#fff', GRID, 1.4, 10)
    o += T(765, 96, '紫圈：口訣抓到的 3 根', 15, KEY, 'middle', 'bold')
    o += T(654, 124, 'P：兩桿 → LP、NP', 15, INK, 'start')
    o += T(654, 150, 'B：AB、BC 共線 → BF', 15, INK, 'start')
    o += T(654, 176, '其餘 21 根口訣管不到', 15, COMP, 'start')
    return svg(W, H, o, 'SA-2016-4 零力桿')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3, 'fig3_4': fig3_4, 'fig3_5': fig3_5,
       'fig3_6': fig3_6, 'fig3_7': fig3_7, 'fig3_8': fig3_8, 'fig3_9': fig3_9}
