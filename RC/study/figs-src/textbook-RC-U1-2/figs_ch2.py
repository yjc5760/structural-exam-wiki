# -*- coding: utf-8 -*-
"""第 2 章：互制圖上解一個點——四種入口。"""
from figs_col import *  # noqa
from calcs import demo, rc2021_2, rc2008_2, rc2019_2, rc2002_2

R0 = demo(); D = R0['D']


def fig2_1():
    W, H = 900, 520
    o = T(450, 26, '四種入口在互制圖上的意思（示範柱的標稱 *P*–*M* 曲線）', 16, INK, 'middle', 'bold')
    pl = Plot(110, 60, 520, 390, 0, 40, -200, 600)
    o += pm_axes(pl, [0, 10, 20, 30, 40], [-200, 0, 200, 400, 600])
    o += pm_curve(pl, D, AC, 3.2)
    # 給 c：c = 15
    s15 = D.at(15.0)
    o += pl.dot(tfm(s15['M']), tf(s15['P']), KEY, 7)
    o += T(pl.X(tfm(s15['M'])) - 12, pl.Y(tf(s15['P'])) + 5, '① 給 *c* = 15：就是一個點', 14, KEY, 'end', 'bold')
    # εt = 0
    s = R0['s32']
    o += pl.dot(tfm(s['M']), tf(s['P']), COMP, 7)
    o += T(pl.X(tfm(s['M'])) + 12, pl.Y(tf(s['P'])) - 6, '② ε_{t} = 0 → *c* = 32', 14, COMP, 'start', 'bold')
    # 給 P = 200
    Pg = 200e3
    cP = D.c_for_P(Pg); sP = D.at(cP)
    o += pl.hline(200, 0, 40, WARN, 1.8, '7 4')
    o += pl.dot(tfm(sP['M']), 200, WARN, 7)
    o += T(pl.X(1), pl.Y(200) - 8, '③ 給 *P*：一條水平線', 14, WARN, 'start', 'bold')
    # 給 e = 10 cm
    e = 10.0
    ce = D.c_for_e(e); se = D.at(ce)
    Mline = 36
    o += L(pl.X(0), pl.Y(0), pl.X(min(Mline, 600 * e / 100)), pl.Y(min(600, Mline * 100 / e)), TEN, 1.8, '7 4')
    o += pl.dot(tfm(se['M']), tf(se['P']), TEN, 7)
    o += T(pl.X(5.4) + 6, pl.Y(540), '④ 給 *e* = 10 cm：', 14, TEN, 'start', 'bold')
    o += T(pl.X(5.4) + 6, pl.Y(540) + 20, '一條過原點的射線', 14, TEN, 'start', 'bold')
    o += box(650, 80, 235, 300, '交點就是答案', [f'① *P* = {tf(s15["P"]):.1f}, *M* = {tfm(s15["M"]):.1f}', f'② *P* = {tf(s["P"]):.1f}, *M* = {tfm(s["M"]):.1f}',
                                                 f'③ *c* = {cP:.2f} → *M* = {tfm(sP["M"]):.1f}', f'④ *c* = {ce:.2f} → *P* = {tf(se["P"]):.1f}',
                                                 '', '①② 直接代引擎', '③ 解 *P*(*c*) = 給定值', '④ 試誤到 *M*/*P* = *e*'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '四種入口')


def fig2_2():
    C, s = rc2021_2()
    return tri_panel(C, s, [3, 2, 3], 'RC-2021-2：給 *c* = 14.5 cm（50×50 方柱，3-2-3 D25）', sc=5.0,
                     note=f"*P*_{{n}} = {tf(s['P']):.2f} tf　*M*_{{n}} = {tfm(s['M']):.2f} tf·m　*e* = {s['e']:.2f} cm")


def fig2_3():
    C, s = rc2008_2()
    return tri_panel(C, s, [4, 2, 2], 'RC-2008-2：拉力排應變為零 → *c* = *d*_{t} = 48 cm（40×56，*f*′_{c} = 350）', sc=4.5,
                     note=f"*P*_{{n}} = {tf(s['P']):.2f} tf　*M*_{{n}} = {tfm(s['M']):.2f} tf·m")


def fig2_4():
    C, s, Pn = rc2019_2()
    return tri_panel(C, s, [5, 5], f'RC-2019-2：給 *P*_{{u}} = 291 tf、φ = 0.65 → *P*_{{n}} = {tf(Pn):.1f} tf，解出 *c* = {s["c"]:.2f}', sc=3.6,
                     note=f"*M*_{{n}} = {tfm(s['M']):.2f} tf·m　φ*M*_{{n}} = 0.65 × {tfm(s['M']):.2f} = {0.65*tfm(s['M']):.2f} tf·m")


def fig2_5():
    W, H = 900, 400
    C, s, sb = rc2002_2()
    o = T(450, 26, 'RC-2002-2：給 *e* = 10 cm，畫出 *e*(*c*) 就看得到要試到哪裡', 16, INK, 'middle', 'bold')
    pl = Plot(100, 60, 520, 280, 15, 45, 0, 60)
    o += pl.axes([15, 20, 25, 30, 35, 40, 45], [0, 10, 20, 30, 40, 50, 60], '*c*（cm）', '*e*（cm）', size=14)
    def ef(c):
        st = C.at(c)
        return st['M'] / st['P']
    o += pl.curve(ef, 16.0, 45, AC, 3)
    o += pl.hline(10, 15, 45, TEN, 1.8, '7 4')
    o += pl.dot(s['c'], 10, TEN, 7)
    o += T(pl.X(s['c']) + 10, pl.Y(10) - 12, f"*c* = {s['c']:.2f}", 15, TEN, 'start', 'bold')
    o += pl.dot(sb['c'], sb['e'], KEY, 7)
    o += T(pl.X(sb['c']) + 10, pl.Y(sb['e']) - 4, f"平衡點 *c*_{{b}} = {sb['c']:.2f}、*e*_{{b}} = {sb['e']:.1f}", 14, KEY, 'start', 'bold')
    o += box(650, 80, 235, 220, '讀法', ['*e* 越小 → *c* 越大', f'*e* = 10 < *e*_{{b}} = {sb["e"]:.1f}', '→ 壓力控制，*c* > *c*_{b}', '先猜 *c*，算 *M*/*P*', '大了就加大 *c*', '小了就減小 *c*'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, 'e(c) 試誤')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3, 'fig2_4': fig2_4, 'fig2_5': fig2_5}
