# -*- coding: utf-8 -*-
"""第 5 章：銲道——45° 最窄（S4）、方向性、銲腳上下限。"""
from plot import *  # noqa
from calcs import directional, WMIN, ss2015_2_weld, ss2024_2
import math

W15 = ss2015_2_weld()
W24 = ss2024_2()


def fig5_1():
    W, H = 900, 420
    o = T(215, 28, '(a) 等腳填角銲：從根部往斜邊，哪條路最短？', 16, INK, 'middle', 'bold')
    ox, oy, w = 90, 330, 230
    # 母材：豎板與平板
    o += R(ox - 40, oy - w - 50, 40, w + 50, STEEL2, INK, 1.4)
    o += R(ox - 40, oy, w + 120, 36, STEEL2, INK, 1.4)
    o += P([(ox, oy), (ox, oy - w), (ox + w, oy)], INK, 2, fill=WARN2, close=True)
    # 不同角度的路徑
    for deg, c, dash in [(15, MUT, '5 4'), (30, MUT, '5 4'), (60, MUT, '5 4'), (75, MUT, '5 4')]:
        th = math.radians(deg)
        Lp = w / (math.cos(th) + math.sin(th))
        o += L(ox, oy, ox + Lp * math.cos(th), oy - Lp * math.sin(th), c, 1.6, dash)
    th = math.radians(45)
    Lp = w / math.sqrt(2)
    o += L(ox, oy, ox + Lp * math.cos(th), oy - Lp * math.sin(th), COMP, 4)
    o += T(ox + Lp * 0.5 + 18, oy - Lp * 0.5 + 34, '*t*_{e} = *w*/√2', 16, COMP, 'start', 'bold')
    o += dim(ox, oy + 52, ox + w, oy + 52, '*w*', INK, 0, 16)
    o += dim(ox - 58, oy - w, ox - 58, oy, '*w*', INK, 0, 16, side=-1)
    o += T(ox + 8, oy - w + 22, '熔合面（母材）', 14, AC, 'start', 'bold')
    o += T(ox + w - 4, oy - 10, '熔合面', 14, AC, 'end', 'bold')
    # (b) 路徑長 vs 角度
    o += T(660, 28, '(b) 路徑長 ÷ *w*：45° 最短', 16, INK, 'middle', 'bold')
    pl = Plot(480, 70, 330, 260, 0, 90, 0.6, 1.05)
    o += pl.axes([0, 15, 30, 45, 60, 75, 90], [0.6, 0.707, 0.8, 0.9, 1.0], 'θ（°）', '長度／*w*', size=14,
                 yfmt=lambda v: {0.707: '0.707'}.get(v, f(v)))
    o += pl.curve(lambda d: 1 / (math.cos(math.radians(d)) + math.sin(math.radians(d))), 0, 90, INK, 3)
    o += pl.dot(45, 1 / math.sqrt(2), COMP, 6)
    o += T(pl.X(45), pl.Y(0.707) + 28, '45°：1/√2 = 0.707', 15, COMP, 'middle', 'bold')
    o += T(660, 396, '長度 = *w* / (cosθ + sinθ)；cosθ + sinθ 在 45° 最大（√2）', 15, MUT, 'middle')
    return svg(W, H, o, '填角銲的喉厚')


def fig5_2():
    W, H = 900, 380
    pl = Plot(110, 50, 520, 260, 0, 90, 0.8, 1.6)
    o = pl.axes([0, 15, 30, 45, 60, 75, 90], [0.8, 1.0, 1.2, 1.4, 1.5, 1.6], '力與銲軸夾角 θ（°）', '強度倍數', size=14)
    o += pl.curve(directional, 0, 90, AC, 3.2)
    o += pl.hline(1.0, c=COMP, w=3, dash=None)
    o += T(pl.X(88), pl.Y(1.0) + 22, '台灣規範：一律 1.0', 15, COMP, 'end', 'bold')
    o += T(pl.X(52), pl.Y(directional(52)) - 14, 'AISC：1 + 0.5 sin^{1.5}θ', 15, AC, 'end', 'bold')
    o += pl.dot(0, 1.0, KEY, 5) + T(pl.X(0) + 10, pl.Y(1.0) - 12, '縱向銲（剪）', 14, KEY, 'start', 'bold')
    o += pl.dot(90, 1.5, KEY, 5) + T(pl.X(90) - 10, pl.Y(1.5) - 14, '橫向銲 1.5', 14, KEY, 'end', 'bold')
    o += R(650, 80, 240, 170, '#fff', KEY, 1.6, 10)
    for i, s in enumerate(['為什麼可以忽略？', '橫向銲較強但較脆', '變形能力只有縱向的', '一小部分；混合配置時', '先斷的是橫向銲 → 保守取 1.0']):
        o += T(770, 106 + i * 30, s, 15 if i == 0 else 14, KEY if i == 0 else INK, 'middle', 'bold' if i == 0 else None)
    return svg(W, H, o, '銲道方向性')


def fig5_3():
    W, H = 900, 400
    pl = Plot(110, 50, 520, 270, 0, 40, 0, 16)
    o = pl.axes([0, 6, 12, 19, 25, 32, 38], [0, 3, 5, 6, 8, 12, 16], '較厚板 *t*（mm）', '*w*（mm）', size=14)
    prev = 0
    for tt, wm in WMIN:
        o += L(pl.X(prev), pl.Y(wm), pl.X(tt), pl.Y(wm), TEN, 3.2)
        if prev:
            o += L(pl.X(prev), pl.Y(pwm), pl.X(prev), pl.Y(wm), TEN, 1.4, '3 3')
        prev, pwm = tt, wm
    o += T(pl.X(31), pl.Y(8) - 10, '最小銲腳（表，>19 → 8）', 15, TEN, 'middle', 'bold')
    o += pl.curve(lambda t: t if t < 6 else t - 2, 0, 18, COMP, 2.4, dash='7 4')
    o += T(pl.X(0.8), pl.Y(15.2), '最大（沿板緣）：', 14, COMP, 'start', 'bold')
    o += T(pl.X(0.8), pl.Y(15.2) + 18, '*t* < 6 取 *t*；否則 *t* − 2', 14, COMP, 'start', 'bold')
    o += pl.dot(16, W15['w_req'] * 10, WARN, 6)
    o += L(pl.X(16), pl.Y(W15['w_req'] * 10), pl.X(20.5), pl.Y(5.3) - 5, WARN, 1.2) + T(pl.X(21), pl.Y(5.3), f'SS-2015-2 需 {W15["w_req"]*10:.2f} → 8（強度控制）', 14, WARN, 'start', 'bold')
    o += pl.dot(20, W24['w_req'] * 10, AC, 6)
    o += T(pl.X(20) + 10, pl.Y(W24['w_req'] * 10) + 6, f'SS-2024-2 需 {W24["w_req"]*10:.1f} → 8（最小值控制）', 14, AC, 'start', 'bold')
    o += R(650, 80, 240, 170, '#fff', KEY, 1.6, 10)
    for i, s in enumerate(['為什麼有最小值？', '厚板吸熱快，小銲道', '冷得太快 → 淬硬、冷裂', '為什麼有最大值？', '板緣要留 2 mm 看得到']):
        o += T(770, 106 + i * 30, s, 15 if i in (0, 3) else 14, KEY if i in (0, 3) else INK, 'middle', 'bold' if i in (0, 3) else None)
    return svg(W, H, o, '銲腳尺寸上下限')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3}
