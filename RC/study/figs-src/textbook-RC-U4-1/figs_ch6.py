# -*- coding: utf-8 -*-
"""第 6 章：三道門檻；fps。"""
from figs_ps import *  # noqa
from calcs import demo, rc2004_5, rc2023_4, fps_unbonded

D = demo(); B = rc2004_5(); U = rc2023_4()


def fig6_1():
    W, H = 900, 400
    o = T(450, 26, '彎矩一路加上去，下緣依序經過三道門檻（RC-2004-5，40×90 先拉梁）', 16, INK, 'middle', 'bold')
    Pe, A = B['Pe'], 3600.0
    S = 54000.0; e = 35.0
    Mdec = (Pe / A + Pe * e / S) * S
    vals = [('只有預力', 0.0), ('① 去壓', Mdec), ('② 開裂', B['Mcr'])]
    hp, y0, k = 150, 90, 1.1
    for i, (lab, M) in enumerate(vals):
        xa = 150 + i * 200
        top = Pe / A - Pe * e / S + M / S
        bot = Pe / A + Pe * e / S - M / S
        o += sblock(xa, y0, hp, top, bot, k)
        o += T(xa, y0 + hp + 48, lab, 15, INK, 'middle', 'bold')
        o += T(xa, y0 + hp + 70, f'*M* = {tfm(M):.2f} tf·m', 14, MUT, 'middle')
    o += T(150 + 200 * 1, y0 + hp + 92, '下緣 = 0', 14, KEY, 'middle', 'bold')
    o += T(150 + 200 * 2, y0 + hp + 92, f"下緣 = −*f*_{{r}} = −{B['fr']:.2f}", 14, KEY, 'middle', 'bold')
    o += box(700, 80, 190, 250, '③ 極限', [f"*M*_{{n}} = {tfm(B['Mn']):.2f}", f"φ*M*_{{n}} = {tfm(B['phiMn']):.2f}", '應力圖不再是', '直線（混凝土', '已開裂、壓碎）', f"φ*M*_{{n}}/*M*_{{cr}} = {B['ratio']:.2f}", '≥ 1.2 ✔'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '三道門檻')


def fig6_2():
    W, H = 900, 520
    o = T(450, 26, '*f*_{ps} 四式怎麼選：考卷會印式子，要你自己判斷該用哪一條', 16, INK, 'middle', 'bold')
    o += node(450, 80, 300, 54, ['鋼腱有握裹（灌漿／先拉）？'], WARN2, WARN, 15, shape='dia', weight='bold')
    o += node(220, 190, 300, 60, ['*f*_{se} ≥ 0.5*f*_{pu}？'], WARN2, WARN, 15, shape='dia', weight='bold')
    o += node(680, 190, 300, 60, ['跨深比 ℓ/*h* ≤ 35？'], WARN2, WARN, 15, shape='dia', weight='bold')
    o += arrow_path([(330, 80), (220, 80), (220, 158)], INK, '是', 270, 72)
    o += arrow_path([(570, 80), (680, 80), (680, 158)], INK, '否（無握裹）', 640, 72)
    o += node(110, 330, 210, 96, ['近似式', '*f*_{pu}(1 − γ_{p}/β_{1}·ρ_{p}*f*_{pu}/*f*′_{c})', '（0.5 版 = γ_{p}/β_{1} 取 0.5）'], TEN2, TEN, 14)
    o += node(340, 330, 200, 96, ['不可用近似式', '→ 應變相容法', '（RC-2018-4）'], COMP2, COMP, 14)
    o += node(570, 330, 210, 96, ['*f*_{se} + 700 + *f*′_{c}/(100ρ_{p})', '≤ *f*_{py}', '≤ *f*_{se} + 4200'], AC2, AC, 14)
    o += node(800, 330, 190, 96, ['*f*_{se} + 700 + *f*′_{c}/(300ρ_{p})', '≤ *f*_{py}', '≤ *f*_{se} + 2100'], AC2, AC, 14)
    o += arrow_path([(150, 190), (110, 190), (110, 282)], TEN, '是', 128, 240)
    o += arrow_path([(290, 220), (340, 220), (340, 282)], COMP, '否', 356, 252)
    o += arrow_path([(610, 220), (570, 220), (570, 282)], AC, '是', 588, 252)
    o += arrow_path([(750, 220), (800, 220), (800, 282)], AC, '否', 818, 252)
    o += T(110, 400, 'RC-2004-5、2013-4', 14, TEN, 'middle', 'bold')
    o += T(340, 400, 'RC-2003-1（考卷限用）', 14, COMP, 'middle', 'bold')
    o += T(570, 400, '107 年考卷印過', 14, AC, 'middle', 'bold')
    o += T(800, 400, 'RC-2023-4', 14, AC, 'middle', 'bold')
    o += node(450, 470, 760, 50, ['然後一律：*a* = *A*_{ps}*f*_{ps}/(0.85*f*′_{c}*b*)，*M*_{n} = *A*_{ps}*f*_{ps}(*d*_{p} − *a*/2)；用 *c* = *a*/β_{1} 算 ε_{t} 定 φ'], KEY2, KEY, 15, weight='bold')
    return svg(W, H, o, 'fps 選擇')


def fig6_3():
    W, H = 900, 360
    o = T(450, 26, '種子 P4：鋼腱的應變 ＝ 本來就拉著 ＋ 混凝土去壓 ＋ 撓曲新增', 16, INK, 'middle', 'bold')
    segs = [('ε_{pe} = *f*_{se}/*E*_{p}', '預力本來就拉著', 0.006, TEN), ('ε_{decomp}', '鋼腱位置混凝土壓應變歸零', 0.0004, WARN), ('ε_{ps,f} = 0.003(*d*_{p} − *c*)/*c*', '和 U1-1 一樣的相似三角形', 0.008, AC)]
    x = 100; k = 650 / 0.0144
    for lab, sub, v, col in segs:
        o += R(x, 140, v * k, 46, col, None, 0, op=0.85)
        o += T(x + v * k / 2, 120 if v > 0.001 else 230, lab, 15, col, 'middle', 'bold')
        o += T(x + v * k / 2, 214 if v > 0.001 else 254, sub, 14, INK, 'middle')
        x += v * k
    o += A(100, 290, x, 290, KEY, 2.2, 10, both=True)
    o += T((100 + x) / 2, 316, 'ε_{ps}（查鋼腱應力–應變曲線得 *f*_{ps}）', 15, KEY, 'middle', 'bold')
    o += T(450, 345, '（長度僅示意；中間那段通常很小，約 0.0003～0.0005）', 14, MUT, 'middle')
    return svg(W, H, o, '三段應變')


def fig6_4():
    W, H = 900, 400
    o = T(450, 26, '無握裹 *f*_{ps}：公式和上限是一對，不能拆開用（*f*_{se} = 11,000、*f*′_{c} = 420）', 16, INK, 'middle', 'bold')
    pl = Plot(110, 60, 540, 280, 0.001, 0.008, 11500, 16500)
    o += pl.axes([0.002, 0.004, 0.006, 0.008], [12000, 13100, 14000, 15200, 16150], 'ρ_{p}', '*f*_{ps}', xfmt=lambda v: f'{v:.3f}', yfmt=lambda v: f'{v:,.0f}', size=14)
    f100 = lambda r: min(fps_unbonded(r, k=100), 15200, 16150)
    f300 = lambda r: min(fps_unbonded(r, k=300), 13100, 16150)
    o += pl.curve(f100, 0.001, 0.008, AC, 3)
    o += pl.curve(f300, 0.001, 0.008, COMP, 3)
    o += T(pl.X(0.0045), pl.Y(15200) - 10, 'ℓ/*h* ≤ 35：/100ρ_{p}，上限 *f*_{se} + 4200', 14, AC, 'start', 'bold')
    o += T(pl.X(0.0045), pl.Y(13100) - 10, 'ℓ/*h* > 35：/300ρ_{p}，上限 *f*_{se} + 2100', 14, COMP, 'start', 'bold')
    o += pl.dot(U['rho'], U['fps'], KEY, 7)
    o += T(pl.X(U['rho']) + 10, pl.Y(U['fps']) + 26, f"RC-2023-4：ρ_{{p}} = {U['rho']:.5f} → {U['fps']:,.0f}", 14, KEY, 'start', 'bold')
    o += box(670, 80, 220, 230, '為什麼長跨更小', ['無握裹鋼腱的伸長', '分散在整根梁長', '跨越長 → 平均應變', '越被稀釋', '→ 增量公式壓低', '　上限也壓低'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '無握裹 fps')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3, 'fig6_4': fig6_4}
