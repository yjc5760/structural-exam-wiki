# -*- coding: utf-8 -*-
"""第 4 章：φ 分區、設計曲線、兩個峰值。"""
from figs_col import *  # noqa
from calcs import demo, rc2015_1, phi_col

R0 = demo(); D = R0['D']


def fig4_1():
    W, H = 900, 400
    o = T(450, 26, 'φ 隨最外拉力筋應變 ε_{t} 變化：兩個端點連直線', 16, INK, 'middle', 'bold')
    pl = Plot(100, 60, 560, 270, 0, 0.008, 0.5, 1.0)
    o += pl.axes([0, 0.002, 0.005, 0.008], [0.5, 0.65, 0.75, 0.9, 1.0], 'ε_{t}', 'φ',
                 xfmt=lambda v: {0: '0', 0.002: '0.002', 0.005: '0.005', 0.008: '0.008'}[v], yfmt=lambda v: f'{v:.2f}', size=14)
    o += pl.curve(lambda e: phi_col(e), 0, 0.008, COMP, 3.4, n=400)
    o += pl.curve(lambda e: phi_col(e, True), 0, 0.008, WARN, 3, dash='8 5', n=400)
    o += T(pl.X(0.0006), pl.Y(0.65) + 22, '箍筋柱 0.65', 14, COMP, 'start', 'bold')
    o += T(pl.X(0.0006), pl.Y(0.75) - 10, '螺旋柱 0.75', 14, WARN, 'start', 'bold')
    o += T(pl.X(0.0062), pl.Y(0.9) - 10, '拉力控制 0.90', 14, TEN, 'middle', 'bold')
    o += T(pl.X(0.001), pl.Y(0.55), '壓力控制', 15, COMP, 'middle', 'bold')
    o += T(pl.X(0.0035), pl.Y(0.55), '過渡區', 15, KEY, 'middle', 'bold')
    o += pl.vline(0.002, 0.5, 1.0, MUT, 1.2)
    o += pl.vline(0.005, 0.5, 1.0, MUT, 1.2)
    o += box(680, 70, 210, 250, '記法', ['壓碎前沒警告', '→ 打最多折', '', '拉到 0.005 才碎', '→ 0.90（同梁）', '', '中間：連直線'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, 'φ 分區')


def fig4_2():
    W, H = 900, 540
    o = T(450, 26, '示範柱：標稱曲線（藍）乘上 φ、再截頂，就是設計曲線（紅）', 16, INK, 'middle', 'bold')
    pl = Plot(110, 60, 540, 410, 0, 36, -50, 600)
    o += pm_axes(pl, [0, 10, 20, 30], [0, 100, 200, 300, 400, 500, 600], '*M*（tf·m）', '*P*（tf）')
    o += pm_curve(pl, D, AC, 2.6, dash='7 4')
    o += pm_curve(pl, D, COMP, 3.4, design=True)
    st, sb, s0 = R0['st'], R0['sb'], R0['s0']
    o += pl.dot(st['phi'] * tfm(st['M']), tf(st['phi'] * st['P']), WARN, 7)
    o += T(pl.X(st['phi'] * tfm(st['M'])) + 12, pl.Y(tf(st['phi'] * st['P'])) + 5, f"φ*M*_{{n}} 峰值 {tfm(0.9*st['M']):.2f}（ε_{{t}} = 0.005）", 14, WARN, 'start', 'bold')
    o += pl.dot(sb['phi'] * tfm(sb['M']), tf(sb['phi'] * sb['P']), KEY, 7)
    o += T(pl.X(sb['phi'] * tfm(sb['M'])) - 12, pl.Y(tf(sb['phi'] * sb['P'])) - 8, f"平衡點 φ = {sb['phi']:.3f}：{tfm(sb['phi']*sb['M']):.2f}", 14, KEY, 'end', 'bold')
    o += pl.dot(tfm(sb['M']), tf(sb['P']), KEY, 6)
    o += T(pl.X(tfm(sb['M'])) - 10, pl.Y(tf(sb['P'])) - 12, f"*M*_{{n}} 峰值 {tfm(sb['M']):.2f}", 14, AC, 'end', 'bold')
    o += T(pl.X(1), pl.Y(tf(R0['phiPmax'])) - 10, f"0.80φ*P*_{{0}} = {tf(R0['phiPmax']):.1f}", 14, COMP, 'start', 'bold')
    o += box(668, 90, 220, 270, '兩條線的距離', ['上半段：只乘 0.65', '（縮 35%）', '', '下半段：乘 0.90', '（只縮 10%）', '', '所以設計曲線的', '「肚子」往下移'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '設計曲線')


def fig4_3():
    W, H = 900, 420
    C, sb, st, s0, scan = rc2015_1()
    o = T(450, 26, 'RC-2015-1：*M*_{n}（藍）和 φ*M*_{n}（紅）的峰值不在同一個 *c*', 16, INK, 'middle', 'bold')
    pl = Plot(100, 60, 560, 290, 10, 34, 50, 145)
    o += pl.axes([10, 15, 20, 25, 30], [50, 75, 100, 125], '*c*（cm）', 'tf·m', size=14)
    o += pl.curve(lambda c: tfm(C.at(c)['M']), 10, 33, AC, 3)
    o += pl.curve(lambda c: tfm(C.at(c)['M'] * C.at(c)['phi']), 10, 33, COMP, 3.4)
    o += pl.dot(st['c'], tfm(0.9 * st['M']), COMP, 7)
    o += T(pl.X(st['c']), pl.Y(tfm(0.9 * st['M'])) + 28, f"φ*M*_{{n}} 峰 {tfm(0.9*st['M']):.1f}", 14, COMP, 'middle', 'bold')
    o += T(pl.X(st['c']), pl.Y(tfm(0.9 * st['M'])) + 48, f"*c* = {st['c']:.2f}（ε_{{t}} = 0.005）", 14, COMP, 'middle')
    o += pl.dot(sb['c'], tfm(sb['M']), AC, 7)
    o += T(pl.X(sb['c']) - 10, pl.Y(tfm(sb['M'])) - 10, f"*M*_{{n}} 峰 {tfm(sb['M']):.1f}（平衡點）", 14, AC, 'end', 'bold')
    o += pl.dot(sb['c'], tfm(sb['phi'] * sb['M']), KEY, 6)
    o += T(pl.X(sb['c']) - 10, pl.Y(tfm(sb['phi'] * sb['M'])) + 20, f"平衡點的 φ*M*_{{n}} 只有 {tfm(sb['phi']*sb['M']):.1f}", 14, KEY, 'end', 'bold')
    o += pl.vline(st['c'], 50, 145, COMP, 1.2)
    o += box(680, 80, 210, 230, '為什麼', ['*c* < 19.50：', 'φ 已是 0.90 封頂，', '*M*_{n} 還在變小', '', '*c* > 19.50：', 'φ 掉得比', '*M*_{n} 漲得快'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '兩個峰值')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
