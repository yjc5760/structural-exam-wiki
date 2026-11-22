# -*- coding: utf-8 -*-
"""第 2 章：C 線與核心。"""
from figs_ps import *  # noqa
from calcs import demo

D = demo()


def fig2_1():
    W, H = 900, 420
    o = T(450, 26, '壓力合力 *C* 從鋼腱往上移 *M*/*P*：落在核心（紫帶）內就全斷面受壓', 16, INK, 'middle', 'bold')
    sc = 4.6; y0 = 70; xc = 200
    o += ibeam(xc, y0, sc)
    yg = y0 + 30 * sc
    k = D['k']
    o += R(xc - 90, yg - k * sc, 180, 2 * k * sc, KEY2, None, 0, op=0.75)
    o += L(xc - 100, yg, xc + 100, yg, KEY, 1.2, '6 4')
    o += T(xc - 104, yg + 5, '形心', 14, KEY, 'end')
    o += T(xc - 96, yg - k * sc + 5, f"上核心點 −{k:.2f}", 14, KEY, 'end', 'bold')
    o += T(xc - 96, yg + k * sc + 5, f"下核心點 +{k:.2f}", 14, KEY, 'end', 'bold')
    ye = yg + D['e'] * sc
    o += C(xc, ye, 7, TEN, '#fff', 1.6)
    o += T(xc - 96, ye + 24, '鋼腱 *e* = 19.8', 14, TEN, 'end', 'bold')
    y1 = yg + D['yC1'] * sc; y2 = yg + D['yC2'] * sc
    o += A(xc + 30, ye, xc + 30, y1 + 4, WARN, 2.2, 10)
    o += C(xc + 30, y1, 6, WARN, '#fff', 1.4)
    o += T(xc + 112, y1 + 5, f"傳遞 *y*_{{C}} = {D['yC1']:.2f}（核心內）", 14, WARN, 'start', 'bold')
    o += A(xc + 60, ye, xc + 60, y2 + 4, AC, 2.2, 10)
    o += C(xc + 60, y2, 6, AC, '#fff', 1.4)
    o += T(xc + 112, y2 + 5, f"使用 *y*_{{C}} = {D['yC2']:.2f}（超出上核心點）".replace("-", "−"), 14, AC, 'start', 'bold')
    o += box(520, 230, 360, 170, '*y*_{C} = *e* − *M*/*P*', [f"傳遞：19.8 − 4.752/0.70 = {D['yC1']:.2f}", f"使用：19.8 − 24.552/0.60 = {D['yC2']:.2f}", '在核心內 → 上下緣都受壓', '超過上核心點 → 下緣受拉'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, 'C 線與核心')


def fig2_2():
    W, H = 900, 400
    o = T(450, 26, '上下緣應力隨 *C* 的位置直線變化：兩條線穿過零的地方就是核心點（*P* = *P*_{e}）', 16, INK, 'middle', 'bold')
    pl = Plot(100, 60, 540, 280, -30, 30, -70, 180)
    o += pl.axes([-30, -20, -10, 0, 10, 20, 30], [-60, -30, 0, 40, 80, 120, 160], '*y*_{C}（cm，下為正）', 'kgf/cm²', size=14)
    P, A, I, c = D['Pe'], D['A'], D['I'], D['c']
    ft = lambda y: P / A * (1 - y * c / D['r2'])
    fb = lambda y: P / A * (1 + y * c / D['r2'])
    o += pl.curve(ft, -30, 30, AC, 3)
    o += pl.curve(fb, -30, 30, COMP, 3)
    o += pl.hline(0, -30, 30, INK, 1.4, None)
    o += T(pl.X(-28), pl.Y(ft(-28)) + 22, '上緣 *f*_{t}', 14, AC, 'start', 'bold')
    o += T(pl.X(22), pl.Y(fb(22)) - 8, '下緣 *f*_{b}', 14, COMP, 'end', 'bold')
    k = D['k']
    o += pl.area(lambda x: 180, lambda x: -70, -k, k, KEY2, 0.5)
    o += pl.dot(-k, 0, KEY, 6); o += pl.dot(k, 0, KEY, 6)
    o += T(pl.X(0), pl.Y(165), '核心', 15, KEY, 'middle', 'bold')
    o += pl.dot(D['yC2'], D['t2'][1], AC, 7)
    o += T(pl.X(D['yC2']) + 10, pl.Y(D['t2'][1]) + 6, f"使用：下緣 {D['t2'][1]:.2f}".replace("-", "−"), 14, AC, 'start', 'bold')
    o += box(660, 80, 230, 230, '讀圖', ['*y*_{C} = −*k*_{t}：下緣 = 0', '（去壓點）', '*y*_{C} = +*k*_{b}：上緣 = 0', '', '線性關係：', '*f*_{b} = (*P*/*A*)(1 + *y*_{C}*c*_{b}/*r*^{2})'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '核心點')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2}
