# -*- coding: utf-8 -*-
"""第 6 章：防蝕。露點以 Magnus 式、鍍層壽命以 ISO 9223 鋅腐蝕速率上限逐點計算。"""
from plot import *  # noqa
from calcs import *  # noqa
import math


def fig6_1():
    W, H = 900, 400
    o = T(450, 26, '腐蝕是一顆電池：拆掉一個零件就停', 16, INK, 'middle', 'bold')
    o += T(230, 70, '(a) 鋼表面的腐蝕電池', 16, INK, 'middle', 'bold')
    # (a) 電池
    o += R(40, 220, 380, 60, STEEL2, INK, 1.4)
    o += R(40, 190, 380, 30, AC2, AC, 1, op=0.8) + T(230, 210, '水膜（電解質）', 14, AC, 'middle', 'bold')
    o += C(120, 220, 18, COMP2, COMP, 2) + T(120, 226, '−', 18, COMP, 'middle', 'bold')
    o += C(340, 220, 18, TEN2, TEN, 2) + T(340, 226, '+', 18, TEN, 'middle', 'bold')
    o += T(120, 172, '陽極', 15, COMP, 'middle', 'bold') + T(120, 154, 'Fe → Fe²⁺ + 2e⁻', 14, COMP, 'middle')
    o += T(340, 172, '陰極', 15, TEN, 'middle', 'bold') + T(340, 154, 'O₂ + H₂O 吃電子', 14, TEN, 'middle')
    o += A(140, 262, 320, 262, WARN, 2.4, 10) + T(230, 300, '電子在鋼裡流（通路）', 14, WARN, 'middle')
    rows = [('拆電解質 → 塗裝（隔絕水與氧）', TEN), ('換陽極 → 鍍鋅、金屬噴塗（鋅先犧牲）', KEY)]
    for i, (s, c) in enumerate(rows):
        o += T(230, 336 + i * 24, s, 15, c, 'middle', 'bold')
    # (b) 電位尺
    x = 560
    o += T(720, 70, '(b) 電位尺：越負越先被腐蝕', 16, INK, 'middle', 'bold')
    pl = Plot(600, 100, 240, 220, 0, 1, -0.9, -0.3)
    o += A(pl.X(0.2), pl.Y(-0.3), pl.X(0.2), pl.Y(-0.9), INK, 2, 10)
    for v, lab, c in ((E_ZN, '鋅 Zn −0.76 V', KEY), (E_FE, '鐵 Fe −0.44 V', COMP)):
        o += L(pl.X(0.14), pl.Y(v), pl.X(0.26), pl.Y(v), c, 3) + T(pl.X(0.32), pl.Y(v) + 5, lab, 15, c, 'start', 'bold')
    o += T(pl.X(0.32), pl.Y(-0.60) + 5, '鋅比鐵更想丟電子', 14, INK, 'start')
    o += T(pl.X(0.32), pl.Y(-0.60) + 25, '→ 鍍層破了也是鋅先爛', 14, KEY, 'start', 'bold')
    o += T(pl.X(0.2), pl.Y(-0.9) + 22, '更負', 14, MUT, 'middle')
    return svg(W, H, o, '腐蝕電池')


def fig6_2():
    W, H = 900, 380
    pl = Plot(90, 56, 500, 250, 0, 40, 70, 100)
    o = T(340, 26, '§7.4.4「鋼面須高於露點 3°C」比「溼度 85%」更早咬住', 16, INK, 'middle', 'bold')
    o += pl.axes([0, 5, 10, 20, 30, 40], [70, 80, 85, 90, 100], '', 'RH (%)', size=14)
    o += T(pl.X(20), pl.y0 + pl.h + 42, '氣溫＝鋼面溫度 (°C)', 14, INK, 'middle')
    o += R(pl.X(0), pl.Y(100), pl.X(5) - pl.X(0), pl.h, COMP2, None, 0)
    o += T(pl.X(2.5), pl.Y(72), '≤5°C', 14, COMP, 'middle', 'bold')
    o += pl.area(lambda t: 100, lambda t: rh_limit_dew3(t), 5, 40, '#ffe0b2', op=0.7)
    o += pl.curve(rh_limit_dew3, 5, 40, WARN, 3.2)
    o += pl.hline(85, 5, 40, COMP, 2.2, '8 4')
    o += T(pl.X(39), pl.Y(85) - 8, 'RH 85%', 14, COMP, 'end', 'bold')
    o += T(pl.X(22), pl.Y(76), '↑ 橘線：露點＋3°C 界線（Magnus 式現算）', 14, WARN, 'middle', 'bold')
    o += T(pl.X(22), pl.Y(93), '不得塗裝', 15, COMP, 'middle', 'bold')
    for t in (10, 30):
        o += pl.dot(t, rh_limit_dew3(t), WARN, 5)
        o += T(pl.X(t), pl.Y(rh_limit_dew3(t)) + 22, f'{rh_limit_dew3(t):.0f}%', 14, WARN, 'middle', 'bold')
    o += R(620, 64, 268, 242, KEY2, KEY, 1.4, 10)
    rows = [('四項任一成立即不得塗裝', KEY, True), ('', INK, False), ('① 氣溫 ≤ 5°C', INK, False), ('② 相對溼度 ≥ 85%', INK, False),
            ('③ 鋼面未高於露點 3°C', WARN, True), ('④ 鋼面 ≥ 50°C', INK, False), ('', INK, False),
            ('鋼面＝氣溫時，③ 約在', INK, False), ('RH 82～84% 就成立', WARN, True), ('→ ③ 不是 ② 的重述', KEY, True)]
    for i, (s, c, b) in enumerate(rows):
        if s:
            o += T(754, 90 + i * 22, s, 14.5, c, 'middle', 'bold' if b else None)
    return svg(W, H, o, '塗裝露點')


def fig6_3():
    W, H = 900, 350
    o = T(450, 26, f'熱浸鍍鋅 {GALV_T:.0f} μm 能撐多久：看環境的鋅腐蝕速率', 16, INK, 'middle', 'bold')
    pl = Plot(200, 60, 560, 210, 0, 130, 0, 4)
    o += pl.axes([0, 20, 40, 60, 80, 100, 120], [], '', '', size=14, grid=True)
    o += T(pl.X(65), pl.y0 + pl.h + 42, '鍍層耗盡年數（85 μm ÷ 速率上限）', 14, INK, 'middle')
    for i, (n, r) in enumerate(ZINC_RATE):
        life = GALV_T / r
        yc = pl.Y(3.5 - i)
        o += R(pl.X(0), yc - 16, pl.X(life) - pl.X(0), 32, [TEN, AC, WARN, COMP][i], None, 0, 4)
        o += T(pl.X(0) - 10, yc + 5, n, 14.5, INK, 'end', 'bold')
        o += T(pl.X(life) + 8, yc + 5, f'約 {life:.0f} 年（{r} μm/年）', 14, INK, 'start')
    o += T(450, 342, '速率取 ISO 9223 各腐蝕類別鋅之上限值，只示量級；實際壽命依環境、鍍層厚與維護而定。', 14, MUT, 'middle')
    return svg(W, H, o, '鍍鋅壽命')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3}
