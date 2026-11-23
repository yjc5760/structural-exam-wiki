# -*- coding: utf-8 -*-
"""第 1 章：三相柱、夯實前後柱、土方帳本。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig1_1():
    W, H = 900, 430
    o = ''
    x, w = 330, 170
    sc = 160            # 每 1 單位體積的像素
    e, wGs = 0.80, 0.54  # 示意值（S=0.675）
    y_bot = 390
    y_s = y_bot - sc * 1
    y_w = y_s - sc * wGs
    y_top = y_s - sc * e
    o += R(x, y_s, w, sc, '#d7ccc8', INK, 1.6) + T(x + w / 2, y_s + sc / 2 + 6, '土粒', 17, INK, 'middle', 'bold')
    o += R(x, y_w, w, y_s - y_w, ACM, INK, 1.6) + T(x + w / 2, (y_w + y_s) / 2 + 6, '水', 17, AC, 'middle', 'bold')
    o += R(x, y_top, w, y_w - y_top, '#fff', INK, 1.6) + T(x + w / 2, (y_top + y_w) / 2 + 6, '空氣', 16, MUT, 'middle')
    # 左側體積
    o += T(x - 150, y_top - 18, '體積', 17, INK, 'middle', 'bold')
    o += dim(x - 20, y_bot, x - 20, y_s, '', INK) + T(x - 32, (y_bot + y_s) / 2 + 6, '*V*_{s}=1', 16, INK, 'end')
    o += dim(x - 20, y_s, x - 20, y_w, '', AC) + T(x - 32, (y_s + y_w) / 2 + 6, '*V*_{w}=*wG*_{s}', 16, AC, 'end')
    o += dim(x - 110, y_s, x - 110, y_top, '', KEY) + T(x - 122, (y_s + y_top) / 2 + 6, '*V*_{v}=*e*', 16, KEY, 'end')
    o += dim(x - 200, y_bot, x - 200, y_top, '', INK) + T(x - 212, (y_bot + y_top) / 2 + 6, '1+*e*', 16, INK, 'end')
    # 右側重量
    o += T(x + w + 150, y_top - 18, '重量', 17, INK, 'middle', 'bold')
    o += T(x + w + 24, (y_bot + y_s) / 2 + 6, '*W*_{s}=*G*_{s}*γ*_{w}', 16, INK)
    o += T(x + w + 24, (y_s + y_w) / 2 + 6, '*W*_{w}=*wG*_{s}*γ*_{w}', 16, AC)
    o += T(x + w + 24, (y_top + y_w) / 2 + 6, '≈ 0', 16, MUT)
    o += R(x + w + 20, 300, 230, 70, KEY2, KEY, 1.4, 8)
    o += T(x + w + 135, 326, '*S*=*V*_{w}/*V*_{v}', 16, KEY, 'middle', 'bold')
    o += T(x + w + 135, 354, '⇒ *Se*=*wG*_{s}', 17, KEY, 'middle', 'bold')
    return svg(W, H, o, '三相柱')


def _col(x, ybot, sc, e, label, eh, H_txt, c):
    o = R(x, ybot - sc, 120, sc, '#d7ccc8', INK, 1.5) + T(x + 60, ybot - sc / 2 + 6, '土粒 1', 16, INK, 'middle', 'bold')
    o += R(x, ybot - sc - sc * e, 120, sc * e, ACM if c == AC else KEY2, INK, 1.5)
    o += T(x + 60, ybot - sc - sc * e / 2 + 6, eh, 16, c, 'middle', 'bold')
    o += T(x + 60, ybot + 28, label, 16, INK, 'middle', 'bold')
    o += T(x + 60, ybot - sc - sc * e - 12, H_txt, 15, INK, 'middle')
    return o


def fig1_2():
    d = ex2019_3()
    W, H = 900, 420
    sc = 150
    ybot = 375
    o = _col(180, ybot, sc, d['e0'], '夯實前', f"*e*_{{0}}={d['e0']:.3f}", f"*H*_{{0}}={d['H0']:.3f} m", AC)
    Hf = d['H0'] - d['dH']
    o += _col(440, ybot, sc, d['ef'], '夯實後', f"*e*_{{f}}={d['ef']:.3f}", f"*H*={Hf:.3f} m", KEY)
    o += L(150, ybot - sc, 600, ybot - sc, INK, 1.3, '5 4')
    o += T(610, ybot - sc + 5, '土粒頂面對齊（不動）', 14, MUT)
    yt0 = ybot - sc - sc * d['e0']
    ytf = ybot - sc - sc * d['ef']
    o += L(300, yt0, 440, yt0, COMP, 1.2, '4 3') + L(560, yt0, 600, yt0, COMP, 1.2, '4 3') + L(560, ytf, 600, ytf, COMP, 1.2, '4 3')
    o += dim(600, yt0, 600, ytf, '', COMP) + T(612, (yt0 + ytf) / 2 + 6, f"Δ*e*={d['e0'] - d['ef']:.4f}", 16, COMP, 'start', 'bold')
    o += R(620, 270, 262, 84, KEY2, KEY, 1.4, 8)
    o += T(751, 298, 'Δ*H*=*H*_{0}·Δ*e*/(1+*e*_{0})', 16, KEY, 'middle', 'bold')
    o += T(751, 328, f"= {d['dH']:.3f} m", 17, KEY, 'middle', 'bold')
    o += T(751, 378, f"誤用 1+*e*_{{f}}：{d['dH_wrong']:.4f} m", 14, COMP, 'middle')
    return svg(W, H, o, '夯實前後三相柱')


def fig1_3():
    d = ex2008_1()
    W, H = 900, 360
    o = T(450, 30, '1 m³ 夯實土的兩本帳', 17, INK, 'middle', 'bold')
    sc = 24   # 每 kN 像素
    x0 = 170
    # 土粒帳
    o += T(x0 - 16, 92, '土粒重', 16, TEN, 'end', 'bold')
    wa, wb = d['gdA'] * d['VA'], d['gdB'] * d['VB']
    o += R(x0, 70, wa * sc, 34, TEN2, TEN, 1.4) + T(x0 + wa * sc / 2, 93, f'甲 {wa:.3f} kN（{d["VA"]:.3f} m³）', 15, TEN, 'middle', 'bold')
    o += R(x0 + wa * sc, 70, wb * sc, 34, TENM, TEN, 1.4) + T(x0 + wa * sc + wb * sc / 2, 93, f'乙 {wb:.2f}', 14, TEN, 'middle', 'bold')
    o += T(x0 + (wa + wb) * sc + 10, 93, f'= {d["Ws"]:.1f} kN ✓', 15, TEN, 'start', 'bold')
    o += T(x0, 128, f'甲 *γ*_{{d}}={d["gdA"]:.2f}、乙 *γ*_{{d}}={d["gdB"]:.2f}；體積 4:1 ⇒ 17.98(4*V*_{{B}})+18.56*V*_{{B}}=20', 14, MUT)
    # 水帳（放大 6 倍）
    sw = sc * 6
    o += T(x0 - 16, 202, '水重', 16, AC, 'end', 'bold')
    o += T(x0 - 16, 222, '（另一比例尺）', 14, MUT, 'end')
    a, b, c = d['WwA'], d['WwB'], d['dWw']
    s = 200
    o += R(x0, 180, a * s, 34, AC2, AC, 1.4) + T(x0 + a * s / 2, 203, f'甲帶來 {a:.3f}', 14, AC, 'middle', 'bold')
    o += R(x0 + a * s, 180, b * s, 34, ACM, AC, 1.4) + T(x0 + a * s + b * s / 2, 203, f'乙 {b:.3f}', 14, AC, 'middle', 'bold')
    o += R(x0 + (a + b) * s, 180, c * s, 34, COMP2, COMP, 1.6) + T(x0 + (a + b + c / 2) * s, 203, f'加 {c:.3f}', 14, COMP, 'middle', 'bold')
    o += T(x0 + (a + b + c) * s + 10, 203, f'= {d["Ww"]:.1f} kN', 15, AC, 'start', 'bold')
    o += T(x0, 240, '目標水重 = 20 × 0.12 = 2.4 kN；借土自帶的水不夠，差額加水', 14, MUT)
    o += R(170, 272, 560, 56, KEY2, KEY, 1.4, 8)
    o += T(450, 306, '唯一守恆：土粒重 *W*_{s}；水是「目標 − 自帶」', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '土方調配兩本帳')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3}
