# -*- coding: utf-8 -*-
"""第 4 章：土方調配（鎖 Ws）、粗料修正、2008-1 可行性檢核。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig4_1():
    d = ex2016_2()
    W_, H = 900, 360
    o = ''
    boxes = [(30, '疏濬取土處', [f"*V* = {d['Vborrow']:.0f} m³", f"γ_{{d}} = {d['gd']:.2f}", f"*w* = {d['w'] * 100:.2f}%"], AC),
             (330, '加水', [f"Δ*W*_{{w}} = {d['dWw']:.0f} kN", f"= {d['Vw']:.1f} m³ 水", f"*w*：{d['w'] * 100:.2f}% → 8%"], AC),
             (630, '夯實填土', [f"*V* = {d['Vfill']:.0f} m³", f"γ_{{d,max}} = {d['gdmax']:.2f}", '*w* = OMC = 8%'], KEY)]
    for x, t, ls, c in boxes:
        o += R(x, 60, 240, 160, '#fff', c, 2, 10)
        o += R(x, 60, 240, 38, c, None, 0, 10) + R(x, 84, 240, 14, c, None)
        o += T(x + 120, 86, t, 16, '#fff', 'middle', 'bold')
        for i, s in enumerate(ls):
            o += T(x + 120, 130 + i * 30, s, 15, INK, 'middle')
    o += A(272, 140, 326, 140, INK, 2.4, 11)
    o += A(572, 140, 626, 140, INK, 2.4, 11)
    o += R(30, 250, 840, 50, TEN2, TEN, 2, 10)
    o += T(450, 282, f"不變的只有乾土重 *W*_{{s}} = 19.50 × 10000 = {d['Ws']:.0f} kN", 17, TEN, 'middle', 'bold')
    o += T(450, 336, '體積不守恆（11725 → 10000 m³），水不守恆，只有土粒守恆', 15, MUT, 'middle')
    return svg(W_, H, o, 'SM-2016-2 土方調配')


def fig4_2():
    d = ex2005_2()
    W_, H = 900, 380
    o = T(220, 34, '(a) 315 cm³ 洞裡的體積帳', 16, INK, 'middle', 'bold')
    x0, y0, wbar = 80, 60, 280
    sc = 0.9
    y = y0
    h = d['Vf'] * sc
    o += R(x0, y, wbar, h, '#d7ccc8', INK, 1.2)
    o += T(x0 + wbar / 2, y + h / 2 + 5, f"細料（< #4）{d['Vf']:.2f}", 15, INK, 'middle', 'bold')
    y += h
    for i, r_ in enumerate(d['rows']):
        hh = r_[5] * sc
        o += R(x0, y, wbar, hh, WARN2, INK, 1.2)
        ly = y0 + d['Vf'] * sc - 40 + i * 30
        o += L(x0 + wbar, y + hh / 2, x0 + wbar + 30, ly - 5, MUT, 1)
        o += T(x0 + wbar + 34, ly, f"{r_[0]} 粗料 {r_[5]:.2f}", 14, WARN, 'start', 'bold')
        y += hh
    o += T(x0 + wbar / 2, y + 26, '粗料體積 = 乾重 ÷ (*G*_{s}ρ_{w})', 14, WARN, 'middle', 'bold')
    pl = Plot(560, 70, 300, 240, 0, 3, 0, 2.4)
    o += T(710, 34, '(b) 乾密度（g/cm³）', 16, INK, 'middle', 'bold')
    o += pl.axes([], [0, 0.6, 1.2, 1.8, 2.4], '', '')
    for i, (v, c, lab) in enumerate([(d['rho_df'], KEY2, '扣粗料（正解）'), (d['rho_wrong'], COMPM, '沒扣體積（錯）'), (d['rho_d_all'], STEEL2, '全部土')]):
        x = 0.5 + i
        o += R(pl.X(x - 0.32), pl.Y(v), pl.X(x + 0.32) - pl.X(x - 0.32), pl.Y(0) - pl.Y(v), c, INK, 1.2)
        o += T(pl.X(x), pl.Y(v) - 8, f'{v:.2f}', 15, KEY if i == 0 else INK, 'middle', 'bold')
        o += T(pl.X(x), pl.Y(0) + 22, lab, 14, INK, 'middle')
    return svg(W_, H, o, 'SM-2005-2 過大顆粒修正')


def fig4_3():
    d = ex2008_1()
    W_, H = 900, 380
    pl = Plot(100, 50, 480, 270, 0.09, 0.15, 18.5, 21.5)
    o = pl.axes([0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15], [18.5, 19.5, 20.5, 21.5], '*w*', 'γ_{d}', xfmt=lambda t: f'{t * 100:.0f}%')
    o += pl.curve(lambda w: zav(w, d['GsB']), 0.09, 0.15, MUT, 2, '6 4')
    o += pl.curve(lambda w: zav(w, d['Gs_mix']), 0.09, 0.15, AC, 3)
    o += T(pl.X(0.093), pl.Y(18.95), '灰虛線：*G*_{s} = 2.70 的 ZAV', 14, MUT, 'start')
    o += T(pl.X(0.093), pl.Y(18.7), f"藍線：混合後 *G*_{{s}} = {d['Gs_mix']:.4f} 的 ZAV", 14, AC, 'start', 'bold')
    o += pl.dot(0.12, 20.0, COMP, 7)
    o += T(pl.X(0.12) + 12, pl.Y(20.0) - 10, '目標 (12%, 20.00)', 15, COMP, 'start', 'bold')
    o += pl.dot(0.12, d['zav_mix'], AC, 5)
    o += T(pl.X(0.12) - 12, pl.Y(d['zav_mix']) + 18, f"上限 {d['zav_mix']:.2f}", 14, AC, 'end', 'bold')
    o += R(610, 70, 280, 190, KEY2, KEY, 1.4, 8)
    o += T(750, 98, '目標在天花板上面', 15, KEY, 'middle', 'bold')
    o += T(750, 128, f"*V*_{{s}} + *V*_{{w}} = {d['Vs'] + d['Vw']:.4f} m³", 15, INK, 'middle')
    o += T(750, 156, '> 1 m³（塞不下）', 15, COMP, 'middle', 'bold')
    o += T(750, 186, f"等效 *S* = {d['S'] * 100:.1f}%", 15, COMP, 'middle', 'bold')
    o += T(750, 218, '*G*_{s} 不是干擾項', 15, INK, 'middle')
    o += T(750, 244, '是檢核可行性用的', 15, INK, 'middle')
    return svg(W_, H, o, 'SM-2008-1 夯實目標可行性')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
