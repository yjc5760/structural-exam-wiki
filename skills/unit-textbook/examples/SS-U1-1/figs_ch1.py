# -*- coding: utf-8 -*-
"""第 1 章：拉與壓的根本差別。所有幾何與數值都由程式算出。"""
from plot import *  # noqa
from calcs import h100_tension, h100_comp, H100
import math


def _joint_panel(ox, tension):
    """兩根剛桿＋中間節點；畫出兩桿對節點的力向量，頭尾相接求合力。"""
    o = ''
    ya = 280                     # 軸線
    xl, xr = ox + 75, ox + 375   # 兩端
    xj, yj = (xl + xr) / 2, ya - 62
    c = TEN if tension else COMP
    title = '受拉：兩桿把節點「拉回」軸線' if tension else '受壓：兩桿把節點「推離」軸線'
    o += T(ox + 225, 30, title, 17, c, 'middle', 'bold')
    # 原本筆直位置
    o += L(xl - 20, ya, xr + 20, ya, MUT, 1.4, '6 5')
    o += T(xl + 6, ya + 22, '原本筆直', 13, MUT, 'start') if tension else T(xr - 10, ya + 22, '原本筆直', 13, MUT, 'end')
    # 兩根桿
    o += L(xl, ya, xj, yj, STEEL, 9) + L(xj, yj, xr, ya, STEEL, 9)
    o += C(xl, ya, 6, '#fff', INK, 1.6) + C(xr, ya, 6, '#fff', INK, 1.6)
    o += C(xj, yj, 8, '#fff', INK, 2)
    # 端點外力
    if tension:
        o += A(xl - 4, ya, xl - 58, ya, c, 3, 12) + A(xr + 4, ya, xr + 58, ya, c, 3, 12)
    else:
        o += A(xl - 62, ya, xl - 10, ya, c, 3, 12) + A(xr + 62, ya, xr + 10, ya, c, 3, 12)
    o += T(xl - 40, ya - 12, '*P*', 17, c, 'middle', 'bold') + T(xr + 40, ya - 12, '*P*', 17, c, 'middle', 'bold')
    # δ 標註
    o += dim(xj + 105, ya, xj + 105, yj, '', MUT) + T(xj + 115, (ya + yj) / 2 + 6, 'δ', 16, MUT, 'start', italic=True)
    # 力向量（桿對節點的力）
    Lb = math.hypot(xj - xl, ya - yj)
    ux, uy = (xl - xj) / Lb, (ya - yj) / Lb          # 由節點指向左端
    s = 125
    sgn = 1 if tension else -1
    v1 = (sgn * ux * s, sgn * uy * s)
    v2 = (-sgn * ux * s, sgn * uy * s)
    p1 = (xj + v1[0], yj + v1[1])
    p2 = (p1[0] + v2[0], p1[1] + v2[1])
    o += A(xj, yj, *p1, AC, 2.6, 12)
    o += A(p1[0], p1[1], *p2, AC, 2.2, 12, dash='6 4')
    o += A(xj, yj, *p2, KEY, 4, 15)
    mid2 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    if tension:
        o += T(p1[0] - 8, p1[1] - 8, '左桿的力', 13.5, AC, 'end')
        o += T(p2[0] + 12, p2[1] + 2, '右桿的力（平移）', 13.5, AC, 'start')
    else:
        o += T(p1[0] + 10, p1[1] + 5, '左桿的力', 13.5, AC, 'start')
        o += T(mid2[0] + 14, mid2[1] - 10, '右桿的力（平移）', 13.5, AC, 'start')
    ry = p2[1]
    o += T(xj - 12, (yj + ry) / 2 + 5, '合力', 15, KEY, 'end', 'bold')
    msg = '合力指向軸線 → 偏移自動消失' if tension else '合力背離軸線 → 越推越歪'
    o += R(ox + 30, 330, 390, 40, TEN2 if tension else COMP2, c, 1.4, 8)
    o += T(ox + 225, 356, msg, 15, c, 'middle', 'bold')
    o += T(ox + 225, 392, '穩定：沒有「挫屈」這回事' if tension else '可能失穩：這就是「挫屈」', 14, INK, 'middle')
    return o


def fig1_1():
    W, H = 900, 410
    o = _joint_panel(0, True) + L(450, 20, 450, 395, GRID, 1.5) + _joint_panel(450, False)
    return svg(W, H, o, '拉與壓：節點力向量合成')


def fig1_2():
    W, H = 900, 400
    o = ''
    # (a) 彈簧模型
    ya = 300; xl, xr = 40, 400; xj, yj = 220, 230
    o += T(220, 30, '(a) 在節點裝一支側向彈簧', 16, INK, 'middle', 'bold')
    o += L(xl - 10, ya, xr + 10, ya, MUT, 1.3, '6 5')
    o += L(xl, ya, xj, yj, STEEL, 9) + L(xj, yj, xr, ya, STEEL, 9)
    o += C(xl, ya, 6, '#fff', INK, 1.6) + C(xr, ya, 6, '#fff', INK, 1.6) + C(xj, yj, 8, '#fff', INK, 2)
    o += A(xl - 60, ya, xl - 10, ya, COMP, 3, 12) + A(xr + 60, ya, xr + 10, ya, COMP, 3, 12)
    o += T(xl - 36, ya - 12, '*P*', 16, COMP, 'middle', 'bold') + T(xr + 36, ya - 12, '*P*', 16, COMP, 'middle', 'bold')
    # 彈簧（天花板在上）
    yt = 72
    o += fixed_wall(xj, yt, 90, INK, top=True)
    zz = [(xj, yt)]
    n = 9; top, bot = yt + 14, yj - 22
    for i in range(n + 1):
        yy = top + (bot - top) * i / n
        xx = xj + (0 if i in (0, n) else (13 if i % 2 else -13))
        zz.append((xx, yy))
    zz.append((xj, yj - 8))
    o += P(zz, TEN, 2.2)
    o += T(xj - 24, (top + bot) / 2 + 4, '*k*', 18, TEN, 'end', 'bold')
    # 力
    o += A(xj + 34, yj, xj + 34, yj - 72, COMP, 3.2, 13)
    o += T(xj + 44, yj - 46, '推：4*P*δ/*L*', 15, COMP, 'start', 'bold')
    o += A(xj - 34, yj - 72, xj - 34, yj - 4, TEN, 3.2, 13)
    o += T(xj - 44, yj - 30, '拉回：*k*δ', 15, TEN, 'end', 'bold')
    o += dim(xj + 120, ya, xj + 120, yj, '', MUT) + T(xj + 130, (ya + yj) / 2 + 6, 'δ', 16, MUT, 'start', italic=True)
    o += dim(xl, ya + 30, xj, ya + 30, '*L*/2', MUT, size=14)
    o += dim(xj, ya + 30, xr, ya + 30, '*L*/2', MUT, size=14)
    # (b) 力–δ 圖
    pl = Plot(530, 70, 320, 250, 0, 1, 0, 1.6)
    o += T(690, 30, '(b) 兩個力都和 δ 成正比', 16, INK, 'middle', 'bold')
    o += pl.axes([], [], 'δ', '力', grid=False)
    o += P([pl.pt(0, 0), pl.pt(1, 1)], TEN, 4)
    o += T(pl.X(1) + 6, pl.Y(1) + 5, '*k*δ', 15, TEN, 'start', 'bold')
    for m, lab, dash in ((0.55, '*P* < *P*_{cr}', '7 5'), (1.0, None, None), (1.45, '*P* > *P*_{cr}', '7 5')):
        if lab is None:
            continue
        o += P([pl.pt(0, 0), pl.pt(1, m)], COMP, 2.4, dash=dash)
        o += T(pl.X(1) + 6, pl.Y(m) + 5, lab, 14, COMP, 'start')
    o += T(pl.X(0.03), pl.Y(1.5), '紅虛線＝「推」4*P*δ/*L*，斜率隨 *P* 變大', 13.5, COMP, 'start')
    o += T(pl.X(0.03), pl.Y(1.5) + 20, '*P* = *P*_{cr} 時紅線與綠線重合', 13.5, INK, 'start')
    o += R(530, 340, 340, 46, KEY2, KEY, 1.4, 8)
    o += T(700, 361, '紅線斜率 ＝ 綠線斜率 時就是臨界', 14.5, KEY, 'middle', 'bold')
    o += T(700, 380, '4*P*_{cr}/*L* = *k*　⇒　*P*_{cr} = *kL*/4', 14.5, KEY, 'middle', 'bold')
    return svg(W, H, o, '彈簧模型')


def fig1_3():
    W, H = 900, 330
    o = T(225, 30, '(a) 柱子自己就是一根「彈簧」', 16, INK, 'middle', 'bold')
    x0, x1, yb = 50, 400, 150
    # 簡支梁中央受力 F，撓度形狀（三次曲線，依公式）
    def defl(xx):
        u = (xx - x0) / (x1 - x0)
        u = u if u <= 0.5 else 1 - u
        return (3 * u - 4 * u ** 3)  # 正規化，u=0.5 時 = 1
    o += L(x0, yb, x1, yb, MUT, 1.3, '6 5')
    pts = [(x0 + (x1 - x0) * i / 120, yb + 52 * defl(x0 + (x1 - x0) * i / 120)) for i in range(121)]
    o += P(pts, STEEL, 9)
    o += pin(x0, yb + 6) + pin(x1, yb + 6)
    xm = (x0 + x1) / 2
    o += A(xm, yb - 70, xm, yb + 44, TEN, 3.2, 13)
    o += T(xm + 10, yb - 52, '側向力 *F*', 15, TEN, 'start', 'bold')
    o += dim(xm + 70, yb, xm + 70, yb + 52, '', MUT) + T(xm + 80, yb + 32, 'δ', 16, MUT, 'start', italic=True)
    o += T(225, 255, '材料力學：δ = *FL*^{3} / 48*EI*', 16, INK, 'middle')
    o += T(225, 284, '⇒ 等效彈簧常數 *k* = *F*/δ = 48*EI* / *L*^{3}', 16, TEN, 'middle', 'bold')
    o += L(450, 20, 450, 310, GRID, 1.5)
    # (b) 代回
    o += T(675, 30, '(b) 代回 *P*_{cr} = *kL*/4', 16, INK, 'middle', 'bold')
    o += T(675, 72, '*P*_{cr} = (48*EI*/*L*^{3})·*L*/4 = 12 *EI*/*L*^{2}', 16, KEY, 'middle', 'bold')
    bx, bw = 540, 220
    for i, (lab, v, c) in enumerate((('彈簧模型（粗估）', 12.0, KEY), ('精確解 Euler（第 7 章）', math.pi ** 2, AC))):
        y = 112 + i * 62
        o += T(bx, y, lab, 14, INK, 'start')
        o += R(bx, y + 8, bw * v / 12.0, 26, c, None, 0, 4, op=0.85)
        o += T(bx + bw * v / 12.0 + 8, y + 27, f'{v:.2f} *EI*/*L*^{{2}}', 15, c, 'start', 'bold')
    o += R(480, 248, 390, 58, KEY2, KEY, 1.3, 8)
    o += T(675, 271, '只差 22%，而且「*EI* 在分子、*L*^{2} 在分母」', 14.5, KEY, 'middle', 'bold')
    o += T(675, 294, '這個樣子完全對了 —— *L*^{2} 不用背', 14.5, KEY, 'middle', 'bold')
    return svg(W, H, o, '柱是彈簧')


def fig1_4():
    W, H = 900, 430
    pl = Plot(90, 60, 650, 300, 0, 6, 0, 55)
    o = pl.axes([0, 1, 2, 3, 4, 5, 6], [0, 10, 20, 30, 40, 50], '長度 *L*（m）', '設計強度（tf）')
    # KL/r > 200 區
    Llim = 200 * H100['ry'] / 100
    o += R(pl.X(Llim), pl.y0, pl.X(6) - pl.X(Llim), pl.h, '#eceff1', None, 0, op=0.8)
    o += T((pl.X(Llim) + pl.X(6)) / 2, pl.Y(40), '*KL*/*r* > 200', 13, MUT, 'middle')
    o += T((pl.X(Llim) + pl.X(6)) / 2, pl.Y(40) + 18, '構造上', 13, MUT, 'middle')
    o += T((pl.X(Llim) + pl.X(6)) / 2, pl.Y(40) + 36, '不允許', 13, MUT, 'middle')
    t = h100_tension()
    o += pl.hline(t, 0, 6, TEN, 3.5, None)
    o += T(pl.X(2.2), pl.Y(t) - 12, f'當拉桿：φ_{{t}}*P*_{{n}} = {t:.1f} tf（和長度無關）', 15, TEN, 'start', 'bold')
    o += pl.curve(lambda Lm: h100_comp(Lm * 100)[0], 0.05, 6, COMP, 3.5)
    o += T(pl.X(0.15), pl.Y(30), '當壓桿：φ_{c}*P*_{n}', 15, COMP, 'start', 'bold')
    for Lm in (3, 6):
        v = h100_comp(Lm * 100)[0]
        o += pl.dot(Lm, v, COMP, 6)
        o += T(pl.X(Lm) + (10 if Lm == 3 else -10), pl.Y(v) - 12, f'{v:.1f} tf', 15, COMP, 'start' if Lm == 3 else 'end', 'bold')
    v3, v6 = h100_comp(300)[0], h100_comp(600)[0]
    bx0, by0 = pl.X(2.75), pl.Y(45.5)
    o += R(bx0, by0, 270, 88, '#fff', KEY, 1.4, 8)
    o += T(bx0 + 135, by0 + 24, '長度 3 m → 6 m（加倍）', 14.5, KEY, 'middle', 'bold')
    o += T(bx0 + 135, by0 + 48, f'{v3:.1f} → {v6:.1f} tf，只剩 {v6 / v3 * 100:.0f}%', 14.5, KEY, 'middle', 'bold')
    o += T(bx0 + 135, by0 + 72, '≈ 1/4：*L* 在分母而且是平方', 14, INK, 'middle')
    return svg(W, H, o, '同一支 H100 當拉桿與壓桿')


def fig1_5():
    W, H = 900, 290
    o = ''
    o += P([(450, 20), (560, 62), (450, 104), (340, 62)], INK, 2, fill='#fff', close=True)
    o += T(450, 58, '構材受拉？', 16, INK, 'middle', 'bold') + T(450, 80, '還是受壓？', 16, INK, 'middle', 'bold')
    o += A(340, 62, 220, 62, TEN, 2.4) + A(220, 62, 220, 120, TEN, 2.4)
    o += A(560, 62, 680, 62, COMP, 2.4) + A(680, 62, 680, 120, COMP, 2.4)
    o += T(280, 52, '拉', 16, TEN, 'middle', 'bold') + T(620, 52, '壓', 16, COMP, 'middle', 'bold')
    o += box(30, 124, 380, 156, '面積帳本（材料強度問題）',
             ('① 畫出可能斷開的那個面', '② 數一數那個面的面積', '　 *A*_{g}、*A*_{n}、*A*_{e}、塊體面積', '③ 面積 × 應力（*F*_{y} 或 *F*_{u}），取最小',
              '長度 *L* 完全不出現'), TEN2, TEN, 16, 14.5)
    o += box(490, 124, 380, 156, '幾何帳本（穩定問題）',
             ('① 先找有效長度 *KL*（兩軸都找）', '② 算 *KL*/*r*（細長比），取大', '③ 換成 λ_{c}，決定在哪一段曲線', '④ 才輪到 *F*_{cr} × *A*_{g}',
              '長度是第一個數字'), COMP2, COMP, 16, 14.5)
    return svg(W, H, o, '兩本帳')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3, 'fig1_4': fig1_4, 'fig1_5': fig1_5}
