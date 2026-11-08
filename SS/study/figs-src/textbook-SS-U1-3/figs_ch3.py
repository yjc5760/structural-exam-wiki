# -*- coding: utf-8 -*-
"""第 3 章：Cm、M1/M2 符號、B1。彎矩與撓曲全部由解析式逐點計算；數字取自 calcs.py。"""
from plot import *  # noqa
from calcs import ex2014, ex2020, ex2003, Cm_exact, Cm_code, B1_tw, B1_aisc, Mmax_exact, EX2020
import math


def _arc(cx, cy, r, a0, a1, c, w=2.6):
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / 24)),
            cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / 24))) for i in range(25)]
    return curve_arrow(pts, c, w, 11)


def _defl(r, n=80):
    """一階撓曲：EI y'' = −M(x)，M(0)=1、M(1)=−r（本書符號），y(0)=y(1)=0。回傳正規化後的 y。"""
    M = lambda u: 1 + (-r - 1) * u
    # 兩次積分（數值），再扣直線使兩端為 0
    ys, sl, y = [0.0], 0.0, 0.0
    h = 1 / n
    for i in range(n):
        sl += -M(i * h + h / 2) * h
        y += sl * h
        ys.append(y)
    ys = [ys[i] - ys[-1] * i / n for i in range(n + 1)]
    m = max(abs(v) for v in ys) or 1
    return [v / m for v in ys]


def _panel(ox, r, title, sub, rule, c):
    o = ''
    xc, yt, yb = ox + 70, 110, 330
    o += T(ox + 145, 32, title, 16, c, 'middle', 'bold')
    o += T(ox + 145, 56, sub, 14, MUT, 'middle')
    o += L(xc, yt - 10, xc, yb + 10, MUT, 1.2, '6 5')
    ys = _defl(r)
    n = len(ys) - 1
    o += P([(xc + 26 * ys[i], yt + (yb - yt) * i / n) for i in range(n + 1)], STEEL, 7)
    # 端部外加力偶：r<0 反轉向、r>0 同轉向（上端固定逆時針）
    o += _arc(xc, yt, 28, 110, -60, INK)          # 上端：逆時針（螢幕）
    if r < 0:
        o += _arc(xc, yb, 28, -110, 60, INK)      # 下端：順時針 → 反轉向
    else:
        o += _arc(xc, yb, 28, 250, 60, INK)       # 下端：逆時針 → 同轉向
    # 內力彎矩圖（M2 在上端）
    mx = ox + 190
    o += L(mx, yt, mx, yb, INK, 1.3)
    Mfun = lambda u: 1 + (-r - 1) * u
    pts = [(mx + 52 * Mfun(i / 60), yt + (yb - yt) * i / 60) for i in range(61)]
    o += P([(mx, yt)] + pts + [(mx, yb)], AC, 1.5, AC2, close=True)
    o += T(mx + 52 + 6, yt + 5, '*M*_{2}', 14, AC, 'start')
    o += T(mx + 52 * Mfun(1) + (6 if Mfun(1) >= 0 else -6), yb + 5, '*M*_{1}', 14, AC, 'start' if Mfun(1) >= 0 else 'end')
    o += R(ox + 12, 352, 270, 60, COMP2 if r < 0 else AC2, c, 1.4, 8)
    o += T(ox + 147, 377, rule, 15, c, 'middle', 'bold')
    o += T(ox + 147, 400, f'*M*_{{1}}/*M*_{{2}} = {r:+.3g}，*C*_{{m}} = {Cm_code(r):.3g}', 14, INK, 'middle')
    return o


def fig3_1():
    W_, H = 900, 425
    o = _panel(0, -1.0, '兩端反轉向', 'SS-2020-3 強軸', '單曲率：*M*_{1}/*M*_{2} < 0', COMP)
    o += L(300, 20, 300, 415, GRID, 1.5)
    o += _panel(300, -0.5, '反轉向、大小不等', 'SS-2020-3 弱軸', '單曲率：*M*_{1}/*M*_{2} < 0', COMP)
    o += L(600, 20, 600, 415, GRID, 1.5)
    o += _panel(600, 70 / 110, '兩端同轉向', 'SS-2014-4（勘誤後）', '雙曲率：*M*_{1}/*M*_{2} > 0', AC)
    return svg(W_, H, o, 'M1/M2 符號')


def _ampplot(ox, r, a, title, c):
    pl = Plot(ox + 60, 70, 290, 250, 0, 1, -1.2, 1.6)
    o = T(ox + 205, 32, title, 15.5, c, 'middle', 'bold')
    o += pl.axes([0, 0.5, 1], [-1, 0, 1], '*x*/*L*', '*M*/*M*_{2}', size=14)
    o += pl.hline(0, c=MUT, dash=None, w=1)
    kL = math.pi * math.sqrt(a)
    B = (-r - math.cos(kL)) / math.sin(kL)
    o += pl.curve(lambda u: 1 + (-r - 1) * u, 0, 1, AC, 2.4, dash='7 5')
    o += pl.curve(lambda u: math.cos(kL * u) + B * math.sin(kL * u), 0, 1, COMP, 3.4)
    mm = Mmax_exact(r, a)
    o += pl.hline(mm, c=KEY, w=1.3)
    o += T(pl.X(1) + 4, pl.Y(mm) - 6, f'最大 {mm:.2f}', 14, KEY, 'end', 'bold')
    return o, pl, mm


def fig3_2():
    a = 0.3
    W_, H = 900, 440
    o1, p1, m1 = _ampplot(0, -1.0, a, '單曲率（*M*_{1}/*M*_{2} = −1）', COMP)
    o2, p2, m2 = _ampplot(450, 1.0, a, '雙曲率（*M*_{1}/*M*_{2} = +1）', AC)
    o = o1 + o2 + L(450, 20, 450, 430, GRID, 1.5)
    o += R(20, 350, 410, 78, COMP2, COMP, 1.4, 8)
    o += T(225, 376, '兩端一起推，中段被養大', 15, COMP, 'middle', 'bold')
    o += T(225, 402, f'最大值在中間，{m1:.2f} > 1 ⇒ 要放大', 14, INK, 'middle')
    o += R(470, 350, 410, 78, AC2, AC, 1.4, 8)
    o += T(675, 376, '一端推、一端拉，互相抵銷', 15, AC, 'middle', 'bold')
    o += T(675, 402, '最大值仍在端部 = 1.00 ⇒ *B*_{1} 取 1.0', 14, INK, 'middle')
    return svg(W_, H, o, '單雙曲率的二階彎矩')


def fig3_3():
    d14, d20 = ex2014(), ex2020()
    W_, H = 900, 470
    pl = Plot(90, 50, 560, 340, -1, 1, 0, 1.2)
    o = pl.axes([-1, -0.5, 0, 0.5, 1], [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], '*M*_{1}/*M*_{2}', '*C*_{m}', size=14)
    o += T(pl.X(-0.75), pl.Y(0) + 44, '← 單曲率（負）', 14, COMP, 'middle', 'bold')
    o += T(pl.X(0.75), pl.Y(0) + 44, '雙曲率（正）→', 14, AC, 'middle', 'bold')
    for a, dash in ((0.1, '3 4'), (0.3, '8 5')):
        o += pl.hline(1 - a, c=MUT, w=1.2, dash='2 4')
        o += pl.curve(lambda r: Cm_exact(r, a), -1, 1, KEY, 2.2, dash=dash, n=120)
    o += T(pl.X(0.98), pl.Y(0.7) - 8, '1 − α（α = 0.3）', 14, MUT, 'end')
    o += T(pl.X(0.98), pl.Y(0.9) - 8, '1 − α（α = 0.1）', 14, MUT, 'end')
    o += pl.curve(lambda r: 0.64 - 0.32 * r, -1, 1, WARN, 2.2, dash='10 4')
    o += pl.curve(Cm_code, -1, 1, COMP, 3.6)
    pts = [(-1, Cm_code(-1), '2020-3 強軸'), (-0.5, Cm_code(-0.5), '2020-3 弱軸'),
           (d14['M1M2'], d14['Cm'], f'2014-4：{d14["Cm"]:.3f}'), (1.0, 0.2, '2003-4：0.2')]
    for r, cm, lab in pts:
        o += pl.dot(r, cm, INK, 5)
    o += T(pl.X(-0.97), pl.Y(1.13), '2020-3 強軸 1.0', 14, INK, 'start')
    o += T(pl.X(-0.47), pl.Y(0.6), '弱軸 0.8', 14, INK, 'start') + L(pl.X(-0.5), pl.Y(0.8), pl.X(-0.47), pl.Y(0.63), INK, 1)
    o += T(pl.X(d14['M1M2']) - 10, pl.Y(d14['Cm']) + 24, f'2014-4：{d14["Cm"]:.3f}', 14, INK, 'end')
    o += T(pl.X(1.0) - 10, pl.Y(0.2) + 22, '2003-4：0.2', 14, INK, 'end')
    # 圖例
    lx = 668
    o += R(lx, 60, 222, 236, '#fff', GRID, 1.2, 8)
    o += L(lx + 12, 88, lx + 52, 88, COMP, 3.6) + T(lx + 60, 93, '規範 0.6 − 0.4*r*', 14, COMP, 'start', 'bold')
    o += L(lx + 12, 122, lx + 52, 122, WARN, 2.2, '10 4') + T(lx + 60, 127, '台灣 (8.2-3)', 14, WARN, 'start')
    o += T(lx + 60, 148, '的分子（α→0）', 14, WARN, 'start')
    o += L(lx + 12, 180, lx + 52, 180, KEY, 2.2, '8 5') + T(lx + 60, 185, '精確解 α = 0.3', 14, KEY, 'start')
    o += L(lx + 12, 212, lx + 52, 212, KEY, 2.2, '3 4') + T(lx + 60, 217, '精確解 α = 0.1', 14, KEY, 'start')
    o += L(lx + 12, 248, lx + 52, 248, MUT, 1.2, '2 4') + T(lx + 60, 253, '1 − α：低於它', 14, MUT, 'start')
    o += T(lx + 60, 274, '⇒ *B*_{1} < 1，取 1.0', 14, MUT, 'start')
    o += R(668, 316, 222, 70, KEY2, KEY, 1.4, 8)
    o += T(779, 343, '直線 0.6 − 0.4*r*', 15, KEY, 'middle', 'bold')
    o += T(779, 368, '是精確曲線的簡化', 14, INK, 'middle')
    return svg(W_, H, o, 'Cm 與 M1/M2')


def _diamond(cx, cy, w, h, txt, c=AC):
    o = P([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)], c, 2, '#fff', close=True)
    return o + T(cx, cy + 5, txt, 15, c, 'middle', 'bold')


def _rbox(x, y, w, h, t1, t2, c, fill):
    o = R(x, y, w, h, fill, c, 1.8, 10)
    o += T(x + w / 2, y + 26, t1, 16, c, 'middle', 'bold')
    if t2:
        o += T(x + w / 2, y + 50, t2, 14, INK, 'middle')
    return o


def fig3_4():
    W_, H = 900, 400
    o = _diamond(160, 80, 250, 84, '柱端能側移嗎？')
    o += A(285, 80, 400, 80, INK, 2, 9) + T(342, 70, '能', 15, INK, 'middle', 'bold')
    o += _rbox(404, 46, 230, 68, '*C*_{m} = 0.85', 'ASD 可側移構架（款一）', WARN, WARN2)
    o += T(650, 74, 'LRFD：側移那份交給 *B*_{2}', 14, MUT, 'start')
    o += T(650, 96, '（第 4 章）', 14, MUT, 'start')
    o += A(160, 122, 160, 166, INK, 2, 9) + T(172, 150, '不能（有斜撐）', 14, INK, 'start', 'bold')
    o += _diamond(160, 212, 270, 84, '兩端之間有橫向載重？')
    o += A(160, 254, 160, 296, INK, 2, 9) + T(172, 282, '沒有', 14, INK, 'start', 'bold')
    o += _rbox(30, 300, 260, 76, '*C*_{m} = 0.6 − 0.4 *M*_{1}/*M*_{2}', '款二：看單／雙曲率（本章主角）', COMP, COMP2)
    o += A(295, 212, 400, 212, INK, 2, 9) + T(346, 202, '有', 15, INK, 'middle', 'bold')
    o += _diamond(520, 212, 230, 84, '端部受轉動束制？')
    o += A(635, 212, 690, 168, INK, 2, 9) + T(668, 178, '有', 14, INK, 'end', 'bold')
    o += _rbox(694, 128, 186, 68, '*C*_{m} = 0.85', '款三：端部有負彎矩', WARN, WARN2)
    o += A(635, 212, 690, 262, INK, 2, 9) + T(668, 262, '沒有', 14, INK, 'end', 'bold')
    o += _rbox(694, 236, 186, 68, '*C*_{m} = 1.0', '款三：簡支，不打折', COMP, COMP2)
    o += T(600, 360, '有橫向載重時，最大彎矩本來就在中間，', 14, MUT, 'middle')
    o += T(600, 382, '和放大的撓曲同一處 ⇒ 幾乎不能打折', 14, MUT, 'middle')
    return svg(W_, H, o, 'Cm 三款')


def fig3_5():
    d = ex2020()
    W_, H = 900, 450
    pl = Plot(90, 50, 540, 330, 0, 0.3, 0.8, 1.6)
    o = pl.axes([0, 0.1, 0.2, 0.3], [0.8, 1.0, 1.2, 1.4], 'α = *P*_{u}/*P*_{e1}', '*B*_{1}', size=14)
    o += pl.area(lambda a: 1.0, lambda a: 0.8, 0, 0.3, STEEL2, 0.8)
    o += pl.hline(1.0, c=INK, w=1.6, dash=None)
    o += T(pl.X(0.295), pl.Y(0.9), '低於 1.0 一律取 1.0', 14, MUT, 'end')
    for r, c in ((-1.0, COMP), (-0.5, AC)):
        o += pl.curve(lambda a: Mmax_exact(r, a, 200), 0.001, 0.3, KEY, 2, dash='3 4', n=60)
        o += pl.curve(lambda a: B1_aisc(r, a), 0, 0.3, c, 2.6, dash='9 5')
        o += pl.curve(lambda a: B1_tw(r, a), 0, 0.3, c, 3.4)
    o += pl.dot(d['ax'], d['B1x_tw'], COMP, 6) + pl.dot(d['ay'], d['B1y_tw'], AC, 6)
    o += T(pl.X(d['ax']) + 10, pl.Y(d['B1x_tw']) + 24, f'2020-3 強軸 {d["B1x_tw"]:.3f}', 14, COMP, 'start', 'bold')
    o += T(pl.X(d['ay']) + 10, pl.Y(d['B1y_tw']) + 22, f'2020-3 弱軸 {d["B1y_tw"]:.3f} → 1.0', 14, AC, 'start', 'bold')
    lx = 655
    o += R(lx, 60, 235, 150, '#fff', GRID, 1.2, 8)
    o += L(lx + 12, 88, lx + 52, 88, INK, 3.4) + T(lx + 60, 93, '台灣 (8.2-3)', 14, INK, 'start', 'bold')
    o += L(lx + 12, 124, lx + 52, 124, INK, 2.6, '9 5') + T(lx + 60, 129, 'AISC *C*_{m}/(1 − α)', 14, INK, 'start')
    o += L(lx + 12, 160, lx + 52, 160, KEY, 2, '3 4') + T(lx + 60, 165, '精確解', 14, KEY, 'start')
    o += T(lx + 60, 188, '（紅＝*r* = −1，藍＝−0.5）', 14, MUT, 'start')
    o += R(lx, 230, 235, 120, KEY2, KEY, 1.4, 8)
    o += T(lx + 117, 256, '兩式不同，但外殼一樣', 15, KEY, 'middle', 'bold')
    o += T(lx + 117, 284, '都是 1/(1 − α) 乘上', 14, INK, 'middle')
    o += T(lx + 117, 308, '一個「打折係數」', 14, INK, 'middle')
    o += T(lx + 117, 332, '考卷印哪條就用哪條', 14, COMP, 'middle', 'bold')
    return svg(W_, H, o, '台灣 B1 與 AISC B1')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3, 'fig3_4': fig3_4, 'fig3_5': fig3_5}
