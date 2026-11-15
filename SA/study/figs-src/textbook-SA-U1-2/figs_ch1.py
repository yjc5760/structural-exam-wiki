# -*- coding: utf-8 -*-
"""第 1 章：靜定判定。所有幾何由座標算出；計數由 calcs.py 算出。"""
from draw import *  # noqa
from calcs import deg_truss, deg_frame, deg_tree
import math


def fig1_1():
    """一塊剛體在平面上只有 3 種動法 → 3 條方程。"""
    W, H = 900, 300
    o = ''
    titles = [('往右滑', 'Σ*F*_{x} = 0 擋住它', TEN), ('往上滑', 'Σ*F*_{y} = 0 擋住它', TEN), ('轉動', 'Σ*M* = 0 擋住它', KEY)]
    for i, (t, eq, c) in enumerate(titles):
        ox = 20 + i * 295
        cx, cy = ox + 120, 140
        pts = [(cx - 70, cy + 40), (cx - 40, cy - 45), (cx + 60, cy - 35), (cx + 75, cy + 30), (cx + 5, cy + 55)]
        o += P(pts, AC, 2, fill=AC2, close=True)
        if i == 0:
            o += P([(x + 50, y) for x, y in pts], AC, 1.5, fill='none', close=True, dash='6 5')
            o += A(cx + 10, cy, cx + 60, cy, c, 3, 12)
        elif i == 1:
            o += P([(x, y - 50) for x, y in pts], AC, 1.5, fill='none', close=True, dash='6 5')
            o += A(cx, cy + 10, cx, cy - 42, c, 3, 12)
        else:
            a = math.radians(25)
            rot = [(cx + (x - cx) * math.cos(a) + (y - cy) * math.sin(a), cy - (x - cx) * math.sin(a) + (y - cy) * math.cos(a)) for x, y in pts]
            o += P(rot, AC, 1.5, fill='none', close=True, dash='6 5')
            o += moment(cx, cy, 30, cw=False, c=c)
        o += T(cx, 46, f'動法 {i + 1}：{t}', 17, INK, 'middle', 'bold')
        o += T(cx, 232, eq, 16, c, 'middle', 'bold')
    o += T(W / 2, 282, '平面上的剛體只有這 3 種動法 ⇒ 一個自由體只給 3 條獨立的平衡方程，不多也不少', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '平面剛體三個自由度')


def fig1_2():
    """支承與內部釋放：每種擋住幾種動法。"""
    W, H = 900, 470
    o = ''
    cells = [
        ('滾支承', 1, '只擋垂直'), ('貼牆的滾支承', 1, '只擋水平'), ('鉸支承', 2, '擋水平＋垂直'),
        ('固定端', 3, '全部擋住'), ('彈簧支承', 1, '擋垂直（會縮）'), ('連桿', 1, '沿桿方向'),
    ]
    cw, ch = 290, 190
    for k, (name, n, note) in enumerate(cells):
        ox = 15 + (k % 3) * (cw + 5)
        oy = 18 + (k // 3) * (ch + 22)
        o += R(ox, oy, cw, ch, '#fff', GRID, 1.4, 10)
        o += T(ox + 14, oy + 28, name, 16, INK, 'start', 'bold')
        o += R(ox + cw - 92, oy + 10, 80, 28, KEY2, KEY, 1.2, 8)
        o += T(ox + cw - 52, oy + 30, f'r = {n}', 16, KEY, 'middle', 'bold')
        bx, by = ox + 105, oy + 95
        if k not in (1, 3):
            o += L(bx - 70, by, bx + 30, by, INK, 4.5)
        if k == 0:
            o += roller(bx, by)
            o += A(bx + 40, by + 52, bx + 40, by + 8, TEN, 2.6, 11)
        elif k == 1:
            o += L(bx - 70, by, bx, by, INK, 4.5)
            o += roller_wall(bx + 2, by)
            o += A(bx + 64, by + 40, bx + 20, by + 40, TEN, 2.6, 11)
        elif k == 2:
            o += pin(bx, by)
            o += A(bx + 40, by + 52, bx + 40, by + 8, TEN, 2.6, 11)
            o += A(bx - 50, by + 40, bx - 14, by + 40, TEN, 2.6, 11)
        elif k == 3:
            o += L(bx - 70, by, bx, by, INK, 4.5)
            o += L(bx, by - 30, bx, by + 30, INK, 3)
            for i in range(7):
                yy = by - 30 + i * 10
                o += L(bx, yy, bx + 8, yy - 7, INK, 1)
            o += A(bx + 50, by + 52, bx + 50, by + 14, TEN, 2.6, 11)
            o += A(bx - 60, by + 42, bx - 22, by + 42, TEN, 2.6, 11)
            o += moment(bx - 34, by, 24, cw=False, c=TEN, start=20, span=140)
        elif k == 4:
            o += spring_v(bx, by, by + 50)
            o += A(bx + 40, by + 52, bx + 40, by + 8, TEN, 2.6, 11)
        else:
            o += L(bx, by, bx + 40, by + 52, INK, 2.2) + C(bx, by, 4, '#fff', INK, 1.4) + C(bx + 40, by + 52, 4, '#fff', INK, 1.4)
            o += hatch_ground(bx + 22, by + 56, 36)
            o += A(bx + 82, by + 52, bx + 52, by + 13, TEN, 2.6, 11)
        o += T(ox + 14, oy + ch - 14, note, 15, MUT, 'start')
    # 內部釋放說明
    y = 440
    o += C(70, y - 6, 7, '#fff', INK, 2) + L(30, y - 6, 63, y - 6, INK, 4.5) + L(77, y - 6, 110, y - 6, INK, 4.5)
    o += T(126, y, '內鉸接兩根桿：c = 1（多送一條 *M* = 0）；一個鉸接 *k* 根桿：c = *k* − 1', 16, AC, 'start', 'bold')
    return svg(W, H, o, '支承與釋放')


def _frame2016(ox, E_fixed):
    f = Frame(ox + 70, 250, 62)
    A_, B_, C_, D_, E_ = f(0, 0), f(0, 2), f(2, 2), f(4, 2), f(4, 0)
    o = member(A_, B_) + member(B_, C_) + member(C_, D_) + member(D_, E_)
    o += hinge(*C_)
    o += pin(*A_)
    if E_fixed:
        o += fixed_bottom(E_[0], E_[1], 52)
    else:
        o += pin(*E_)
    o += A(D_[0] + 4, D_[1], D_[0] + 54, D_[1], COMP, 2.6, 11) + T(D_[0] + 30, D_[1] - 10, '50 kN', 15, COMP, 'middle', 'bold')
    for p, s in ((A_, 'A'), (B_, 'B'), (C_, 'C'), (D_, 'D'), (E_, 'E')):
        dx = -16 if s in 'AB' else (16 if s in 'DE' else 0)
        dy = -14 if s in 'BC' else (24 if s == 'D' else 0)
        o += T(p[0] + dx, p[1] + dy + (0 if s in 'BCD' else -6), s, 16, INK, 'middle', 'bold')
    # 反力箭頭
    o += A(A_[0] - 48, A_[1] + 30, A_[0] - 14, A_[1] + 30, TEN, 2.4, 10) + A(A_[0], A_[1] + 66, A_[0], A_[1] + 30, TEN, 2.4, 10)
    o += A(E_[0] + 48, E_[1] + 30, E_[0] + 14, E_[1] + 30, TEN, 2.4, 10) + A(E_[0], E_[1] + 66, E_[0], E_[1] + 30, TEN, 2.4, 10)
    r = 5 if E_fixed else 4
    if E_fixed:
        o += moment(E_[0] + 40, E_[1] - 32, 16, cw=False, c=TEN)
    i = deg_tree(r, 1)
    c = COMP if E_fixed else MUT
    title = '考卷：E 是固定端（直接接剖線）' if E_fixed else '誤讀：把 E 看成鉸支承'
    o += T(ox + 195, 38, title, 16, c, 'middle', 'bold')
    o += R(ox + 30, 336, 330, 70, COMP2 if E_fixed else STEEL2, c, 1.4, 8)
    o += T(ox + 195, 362, f'r = {r}，c = 1：i = {r} − 3 − 1 = {i}', 16, c, 'middle', 'bold')
    o += T(ox + 195, 390, '一度靜不定 → 要變形諧合（U2-2）' if E_fixed else '算出 0 → 誤當靜定題，彎矩全錯', 15, INK, 'middle')
    return o


def fig1_3():
    W, H = 900, 420
    o = _frame2016(10, True) + L(450, 20, 450, 405, GRID, 1.5) + _frame2016(460, False)
    return svg(W, H, o, 'SA-2016-1 支承判讀與靜不定度')


def fig1_4():
    """閉合環：樹狀式失效，完整式抓得到。"""
    W, H = 900, 470
    o = ''
    f = Frame(80, 340, 46)
    a, b, c, d = f(0, 0), f(0, 4), f(5, 4), f(5, 0)
    o += T(195, 34, '(a) 一個封閉的方框', 16, INK, 'middle', 'bold')
    o += member(a, b) + member(b, c) + member(c, d) + member(d, a)
    o += pin(*a) + roller(*d)
    o += T(195, 130, '外面只有 3 個反力，整體可解', 15, TEN, 'middle')
    o += T(195, 410, '樹狀式：r − 3 − c = 3 − 3 − 0 = 0（錯）', 15, MUT, 'middle')
    g = Frame(500, 340, 46)
    a2, b2, c2, d2 = g(0, 0), g(0, 4), g(5, 4), g(5, 0)
    o += T(615, 34, '(b) 從頂梁剪一刀', 16, INK, 'middle', 'bold')
    mx = (b2[0] + c2[0]) / 2
    y0 = b2[1]
    o += member(a2, b2) + L(b2[0], y0, mx - 10, y0, INK, 4.5) + L(mx + 10, y0, c2[0], y0, INK, 4.5) + member(c2, d2) + member(d2, a2)
    o += pin(*a2) + roller(*d2)
    o += A(mx - 12, y0 + 18, mx - 70, y0 + 18, WARN, 2.6, 11) + T(mx - 76, y0 + 24, '*N*', 16, WARN, 'end', 'bold')
    o += A(mx - 12, y0 - 58, mx - 12, y0 - 8, WARN, 2.6, 11) + T(mx - 20, y0 - 46, '*V*', 16, WARN, 'end', 'bold')
    o += moment(mx - 10, y0, 26, cw=True, c=KEY, start=120, span=200) + T(mx + 22, y0 + 40, '*M*', 16, KEY, 'start', 'bold')
    o += T(mx + 30, y0 - 70, '切口兩側各有 3 個內力，', 15, WARN, 'start')
    o += T(mx + 30, y0 - 48, '平衡方程一條也沒多', 15, WARN, 'start')
    m, r, j, cc = 4, 3, 4, 0
    o += R(470, 392, 410, 60, KEY2, KEY, 1.4, 8)
    o += T(675, 417, f'完整式：3m + r − 3j − c = {3*m} + {r} − {3*j} − {cc} = {deg_frame(m, r, j, cc)}', 16, KEY, 'middle', 'bold')
    o += T(675, 441, '三度靜不定：每一個閉合環多 3 度', 15, INK, 'middle')
    return svg(W, H, o, '閉合環與完整式')


PTS0202 = dict(A=(0, 0), B=(32, 0), D=(0, 12), F=(8, 12), C=(16, 12), H=(24, 12), I=(32, 12), E=(8, 6), G=(24, 6))
BARS0202 = ['DA', 'IB', 'DF', 'FC', 'CH', 'HI', 'DE', 'FE', 'EC', 'AE', 'CG', 'HG', 'GI', 'GB']


def fig1_5():
    W, H = 900, 450
    f = Frame(110, 360, 21)
    P_ = {k: f(*v) for k, v in PTS0202.items()}
    o = T(W / 2, 30, 'SA-2002-2 數一數：節點 j、桿件 m、反力 r', 17, INK, 'middle', 'bold')
    o += L(P_['A'][0], P_['A'][1], P_['B'][0], P_['B'][1], MUT, 1.6, '8 6')
    o += T((P_['A'][0] + P_['B'][0]) / 2, P_['A'][1] - 8, 'A–B 是虛線，不是桿件', 15, MUT, 'middle')
    for i, bar in enumerate(BARS0202):
        p, q = P_[bar[0]], P_[bar[1]]
        o += L(p[0], p[1], q[0], q[1], STEEL, 5)
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        o += C(mx, my, 11, '#fff', AC, 1.2) + T(mx, my + 5, str(i + 1), 14, AC, 'middle', 'bold')
    for k, (x, y) in P_.items():
        o += C(x, y, 6, KEY, '#fff', 1.4)
    lab = dict(A=(-28, 6), B=(28, 6), D=(-16, -8), F=(0, -14), C=(0, -14), H=(0, -14), I=(16, -8), E=(-16, 18), G=(16, 18))
    for k, (dx, dy) in lab.items():
        o += T(P_[k][0] + dx, P_[k][1] + dy, k, 16, KEY, 'middle', 'bold')
    o += pin(*P_['A']) + pin(*P_['B'])
    m, r, j = len(BARS0202), 4, len(PTS0202)
    o += R(40, 400, 820, 40, KEY2, KEY, 1.4, 8)
    o += T(450, 426, f'j = {j}（紫點）、m = {m}（藍號）、r = 2 + 2 = {r}　⇒　i = m + r − 2j = {m} + {r} − {2*j} = {deg_truss(m, r, j)}　靜定', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2002-2 計數')


def fig1_6():
    """數字對了、幾何不行：四種退化。"""
    W, H = 900, 520
    o = ''
    cw, ch = 435, 240
    panels = ['(a) 三個反力全平行', '(b) 三個反力交於一點', '(c) 三個鉸排成一直線', '(d) 桿數對、位置錯']
    for k, t in enumerate(panels):
        ox = 10 + (k % 2) * (cw + 10)
        oy = 10 + (k // 2) * (ch + 20)
        o += R(ox, oy, cw, ch, '#fff', GRID, 1.4, 10)
        o += T(ox + 16, oy + 30, t, 16, INK, 'start', 'bold')
        if k == 0:
            y = oy + 120
            o += L(ox + 50, y, ox + 385, y, INK, 4.5)
            for x in (ox + 70, ox + 220, ox + 365):
                o += roller(x, y)
                o += A(x, y + 70, x, y + 26, TEN, 2.2, 10)
            o += A(ox + 230, y - 32, ox + 330, y - 32, COMP, 3, 12) + T(ox + 280, y - 42, '一推就滑走', 15, COMP, 'middle', 'bold')
            o += T(ox + 16, oy + ch - 14, 'r = 3，i = 0，但水平方向沒人擋', 15, MUT, 'start')
        elif k == 1:
            y = oy + 120
            xa, xb = ox + 80, ox + 330
            o += L(xa, y, xb, y, INK, 4.5)
            o += pin(xa, y) + roller_wall(xb + 2, y)
            o += L(xa - 30, y, xb + 30, y, KEY, 1.4, '6 5')
            o += C(xa, y, 9, 'none', KEY, 2)
            o += A(xa + 150, y - 56, xa + 150, y - 6, COMP, 3, 12) + T(xa + 160, y - 40, '載重', 15, COMP, 'start', 'bold')
            o += moment(xa, y, 40, cw=True, c=COMP, start=150, span=110)
            o += T(xa + 6, y - 50, '繞 A 轉', 15, COMP, 'start', 'bold')
            o += T(ox + 16, oy + ch - 38, '三條反力線都通過 A：', 15, MUT, 'start')
            o += T(ox + 16, oy + ch - 14, '對 A 取矩，反力全是 0，擋不住轉動', 15, MUT, 'start')
        elif k == 2:
            y = oy + 120
            xa, xc, xb = ox + 70, ox + 220, ox + 370
            o += L(xa, y, xc, y, INK, 4.5) + L(xc, y, xb, y, INK, 4.5)
            o += pin(xa, y) + pin(xb, y) + hinge(xc, y)
            o += P([(xa, y), (xc, y + 34), (xb, y)], AC, 1.6, dash='6 5')
            o += A(xc, y - 52, xc, y - 10, COMP, 3, 12)
            o += T(ox + 16, oy + ch - 38, 'r = 4、c = 1，i = 0；但 C 往下掉時', 15, MUT, 'start')
            o += T(ox + 16, oy + ch - 14, '兩桿起初不會伸長 → 瞬時不穩定', 15, MUT, 'start')
        else:
            f = Frame(ox + 50, oy + 205, 40)
            pts = [f(i * 2.4, 0) for i in range(3)] + [f(i * 2.4, 2.2) for i in range(3)]
            bars = [(0, 1), (1, 2), (3, 4), (4, 5), (0, 3), (1, 4), (2, 5), (0, 4), (1, 3)]
            for a, b in bars:
                o += L(pts[a][0], pts[a][1], pts[b][0], pts[b][1], STEEL, 4.5)
            for p in pts:
                o += C(p[0], p[1], 5, KEY, '#fff', 1.2)
            o += pin(*pts[0]) + roller(*pts[2])
            o += P([pts[1], pts[2], (pts[5][0] + 30, pts[5][1]), (pts[4][0] + 30, pts[4][1])], AC, 1.6, dash='6 5')
            o += T(ox + 270, oy + 150, '右格沒有斜桿', 15, COMP, 'start', 'bold')
            o += T(ox + 270, oy + 172, '會歪成平行四邊形', 15, COMP, 'start')
            o += T(ox + 16, oy + 62, 'm = 9、r = 3、j = 6：i = 0', 15, MUT, 'start')
            o += T(ox + 16, oy + 84, '左格兩根斜桿（多一根）', 15, MUT, 'start')
    return svg(W, H, o, '幾何不穩定四型')


def fig1_7():
    W, H = 900, 300
    o = ''
    o += R(20, 110, 170, 70, KEY2, KEY, 1.8, 10) + T(105, 140, '先數', 16, KEY, 'middle', 'bold') + T(105, 164, 'i = 未知 − 方程', 15, INK, 'middle')
    rows = [(30, 'i < 0', '不穩定（國考不會出）→ 回頭找漏看的支承或桿', COMP, COMP2),
            (120, 'i = 0', '再看幾何：反力不平行、不共點、三鉸不共線 → 靜定', TEN, TEN2),
            (210, 'i > 0', '本單元少見 → 先回頭再讀一次支承（2016-1）', WARN, WARN2)]
    for y, a, b, c, c2 in rows:
        o += A(192, 145, 268, y + 30, INK, 2, 10)
        o += R(272, y, 600, 60, c2, c, 1.6, 10)
        o += T(296, y + 37, a, 17, c, 'start', 'bold')
        o += T(370, y + 37, b, 15, INK, 'start')
    return svg(W, H, o, '判定流程')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3, 'fig1_4': fig1_4,
       'fig1_5': fig1_5, 'fig1_6': fig1_6, 'fig1_7': fig1_7}
