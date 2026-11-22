# -*- coding: utf-8 -*-
"""第 8 章：四控制條件 → 偏心窗口。"""
from figs_ps import *  # noqa
from calcs import rc2010_4, rc2025_4

R10 = rc2010_4(); W10 = R10['W']; W25 = rc2025_4()


def _window(o, y, Wd, title, k, xmap):
    o += T(70, y - 64, title, 15, INK, 'start', 'bold')
    o += A(xmap(-40), y, xmap(90) + 10, y, INK, 1.6, 10)
    for v in range(-40, 91, 10):
        o += L(xmap(v), y - 5, xmap(v), y + 5, INK, 1.1)
        o += T(xmap(v), y + 22, f'{v}'.replace('-', '−'), 14, MUT, 'middle')
    o += R(xmap(Wd['emin']), y - 14, xmap(Wd['emax']) - xmap(Wd['emin']), 28, TEN2, TEN, 1.6)
    marks = [(Wd['e1'], '① 傳遞頂拉（上限）', COMP, -1), (Wd['e2'], '② 傳遞底壓', MUT, 1),
             (Wd['e3'], '③ 使用頂壓', MUT, 1), (Wd['e4'], '④ 使用底拉（下限）', AC, 1)]
    for v, lab, col, s in marks:
        if v < -40 or v > 90:
            o += T(xmap(90 if v > 90 else -40), y + (-30 if s < 0 else 70), f'{lab} {v:.1f}（畫面外）'.replace('-', '−'), 14, col, 'end' if v > 90 else 'start')
            continue
        o += L(xmap(v), y - 22, xmap(v), y + 22, col, 3)
        o += T(xmap(v), y + (-30 if s < 0 else 46), f'{lab} {v:.2f}'.replace('-', '−'), 14, col, 'middle', 'bold')
    return o


def fig8_1():
    W, H = 900, 460
    o = T(450, 26, '四條不等式各給 *e* 一個邊界，交集（綠）就是偏心窗口（cm，形心以下為正）', 16, INK, 'middle', 'bold')
    xmap = lambda v: 80 + (v + 40) * 5.8
    o = _window(o, 140, W10, f"RC-2010-4（50×90、15 m、*P*_{{i}} = 200 tf）：{W10['emin']:.2f} ≤ *e* ≤ {W10['emax']:.2f}", None, xmap)
    o = _window(o, 340, W25, f"RC-2025-4（40×120、12 m、*P*_{{i}} = 200 tf）：{W25['emin']:.2f} ≤ *e* ≤ {W25['emax']:.2f}".replace('-1', '−1'), None, xmap)
    return svg(W, H, o, '偏心窗口')


def fig8_2():
    W, H = 900, 380
    o = T(450, 26, 'RC-2010-4：拉應力一律取 0（舊解）會把窗口算得太窄', 16, INK, 'middle', 'bold')
    xmap = lambda v: 100 + v * 18
    y = 170
    o += A(xmap(0), y, xmap(40) + 10, y, INK, 1.6, 10)
    for v in range(0, 41, 5):
        o += L(xmap(v), y - 5, xmap(v), y + 5, INK, 1.1)
        o += T(xmap(v), y + 22, f'{v}', 14, MUT, 'middle')
    o += R(xmap(W10['emin']), y - 40, xmap(W10['emax']) - xmap(W10['emin']), 28, TEN2, TEN, 1.6)
    o += T((xmap(W10['emin']) + xmap(W10['emax'])) / 2, y - 50, f"現行規範（U 類 2.0√*f*′_{{c}}、0.8√*f*′_{{ci}}）：{W10['emin']:.2f}～{W10['emax']:.2f}", 14, TEN, 'middle', 'bold')
    e1_0 = (200000 / W10['A'] + W10['MG'] / W10['S']) * W10['S'] / 200000
    o += R(xmap(W10['e4_0']), y + 40, xmap(e1_0) - xmap(W10['e4_0']), 28, COMP2, COMP, 1.6)
    o += T((xmap(W10['e4_0']) + xmap(e1_0)) / 2, y + 92, f"拉應力取 0：{W10['e4_0']:.2f}～{e1_0:.2f}", 14, COMP, 'middle', 'bold')
    o += T(450, 330, '拉應力取 0 是「完全預力」的條件；考卷沒寫就依現行規範，只有明寫 *f*_{ta} = 0（如 RC-2015-4）才用 0。', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '拉應力取 0')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2}
