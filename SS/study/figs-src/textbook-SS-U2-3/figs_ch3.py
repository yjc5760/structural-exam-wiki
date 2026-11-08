# -*- coding: utf-8 -*-
"""第 3 章：銲道幾何與力流。幾何依 calcs.py 尺寸，曲線逐點計算。"""
from plot import *  # noqa
from calcs import *  # noqa
import math


def fig3_1():
    W, H = 900, 420
    o = T(220, 28, '(a) 等腳填角銲：最短的一刀在 45°', 16, INK, 'middle', 'bold')
    sc = 34.0
    x0, y0 = 120, 300                    # 直角頂點（根部）
    w = W_TAB * sc
    # 母材：底板（水平）與立板（垂直）
    o += R(40, y0, 360, 46, STEEL2, INK, 1.2)
    o += R(x0 - 40, 70, 40, y0 - 70, STEEL2, INK, 1.2)
    # 銲道三角
    o += P([(x0, y0), (x0 + w, y0), (x0, y0 - w)], COMP, 1.6, fill=COMPM, close=True)
    # 喉：根部到斜邊垂足
    fx, fy = x0 + w / 2, y0 - w / 2
    o += L(x0, y0, fx, fy, KEY, 3.2)
    o += T(fx + 10, fy - 26, '有效銲喉 *t*_{e}', 15, KEY, 'start', 'bold')
    o += T(fx + 10, fy - 6, f'= *w* cos45° = 0.707*w*', 15, KEY, 'start')
    o += dim(x0, y0 + 64, x0 + w, y0 + 64, '*w*', MUT, size=15)
    o += dim(x0 - 58, y0, x0 - 58, y0 - w, '*w*', MUT, size=15, side=-1)
    # 根部、趾部
    o += C(x0, y0, 5, COMP, '#fff', 1.5) + T(x0 + 6, y0 + 22, '根部', 14, COMP, 'start', 'bold')
    o += C(x0 + w, y0, 5, WARN, '#fff', 1.5) + T(x0 + w + 6, y0 + 22, '趾部', 14, WARN, 'start', 'bold')
    o += C(x0, y0 - w, 5, WARN, '#fff', 1.5) + T(x0 + 8, y0 - w - 8, '趾部', 14, WARN, 'start', 'bold')
    o += T(220, 408, f'範例 *w* = {W_TAB:.0f} mm → *t*_{{e}} = {throat(W_TAB):.2f} mm', 15, INK, 'middle')
    # (b) 強度 vs 角度
    pl = Plot(560, 70, 290, 240, 0, 90, 0, 1.6)
    o += T(705, 28, '(b) 力的方向不同，強度不同', 16, INK, 'middle', 'bold')
    o += pl.axes([0, 30, 60, 90], [0, 0.5, 1.0, 1.5], '', '強度倍數', size=14)
    o += T(pl.X(45), pl.y0 + pl.h + 42, '力與銲道軸的夾角 θ (°)', 14, INK, 'middle')
    o += pl.curve(lambda t: 1 + 0.5 * math.sin(math.radians(t)) ** 1.5, 0, 90, AC, 3.2)
    o += pl.hline(1.0, 0, 90, MUT, 1.2)
    o += pl.dot(0, 1.0, AC, 6) + pl.dot(90, 1.5, COMP, 6)
    o += T(pl.X(3), pl.Y(1.0) + 24, '平行（縱向）1.0', 14, AC, 'start', 'bold')
    o += T(pl.X(87), pl.Y(1.5) - 12, '垂直（橫向）1.5', 14, COMP, 'end', 'bold')
    o += T(pl.X(45), pl.Y(0.45), '1 + 0.5 sin^{1.5}θ（AISC 試驗式）', 14, AC, 'middle')
    return svg(W, H, o, '填角銲有效銲喉')


def fig3_2():
    W, H = 900, 380
    o = T(450, 26, '同一個「4*w*」，一個是下限、一個是上限', 16, INK, 'middle', 'bold')
    # (a) 平面：搭接板＋側面銲＋回銲
    ox, oy = 60, 70
    o += R(ox, oy + 40, 330, 150, STEEL2, INK, 1.2)            # 主板
    o += R(ox + 150, oy + 70, 260, 90, STEEL3, INK, 1.2)       # 搭接板（伸出右方）
    x_end = ox + 150
    # 側面銲（上下緣）
    o += L(x_end, oy + 70, x_end + 200, oy + 70, COMP, 6, cap='butt')
    o += L(x_end, oy + 160, x_end + 200, oy + 160, COMP, 6, cap='butt')
    # 回銲：在搭接板左端角落繞過去 (2w~4w)
    rl = 36
    o += L(x_end, oy + 70, x_end, oy + 70 + rl, KEY, 6, cap='butt')
    o += L(x_end, oy + 160, x_end, oy + 160 - rl, KEY, 6, cap='butt')
    o += T(x_end - 8, oy + 96, '回銲', 14, KEY, 'end', 'bold')
    o += T(x_end - 8, oy + 114, '2*w*～4*w*', 14, KEY, 'end', 'bold')
    o += A(x_end + 264, oy + 115, x_end + 310, oy + 115, INK, 2.4, 11)
    o += T(x_end + 280, oy + 140, '*P*', 16, INK, 'start', 'bold')
    o += dim(x_end, oy + 190, x_end + 200, oy + 190, '有效長 ≥ 4*w*（含回銲）', COMP, size=14)
    o += T(220, oy + 255, '(a) 平面：側面填角銲＋轉角回銲', 15, INK, 'middle', 'bold')
    # (b) 數線：兩個 4w 的方向
    pl = Plot(560, 120, 300, 10, 0, 6, 0, 1)
    y = 170
    o += A(560, y, 880, y, INK, 1.8, 9)
    for k in range(0, 7):
        xx = 560 + k * 50
        o += L(xx, y - 5, xx, y + 5, INK, 1.2) + T(xx, y + 24, f'{k}*w*', 14, MUT, 'middle')
    o += L(560 + 100, y - 32, 560 + 200, y - 32, KEY, 8, cap='butt')
    o += T(660 + 50, y - 46, '回銲長度', 15, KEY, 'middle', 'bold')
    o += A(760, y + 50, 860, y + 50, COMP, 3, 11)
    o += L(760, y + 40, 760, y + 60, COMP, 3)
    o += T(810, y + 76, '最小有效長', 15, COMP, 'middle', 'bold')
    o += T(810, y + 96, '≥ 4*w*（下限）', 14, COMP, 'middle')
    o += T(710, y - 74, '4*w* 是上限', 14, KEY, 'middle')
    o += T(720, 330, '(b) 回銲 4*w* 是「最多」，有效長 4*w* 是「最少」', 15, INK, 'middle', 'bold')
    return svg(W, H, o, '回銲與最小長度')


def fig3_3():
    W, H = 900, 380
    pl = Plot(90, 60, 470, 250, 2.0, 4.0, 0, 3.0)
    o = T(330, 28, '螺栓中心距 3*d* 從哪裡來：撕出強度追上承壓上限', 16, INK, 'middle', 'bold')
    o += pl.axes([2.0, 2.5, 8 / 3, 3.0, 3.5, 4.0], [0, 1.2, 2.4], '', '*R*_{n}／(*d t F*_{u})', size=14,
                 xfmt=lambda v: '8/3' if abs(v - 8 / 3) < 1e-6 else f(v))
    o += T(pl.X(3.0), pl.y0 + pl.h + 42, '中心距 *s*／*d*', 14, INK, 'middle')
    o += pl.curve(lambda s: 1.2 * (s - 1), 2.0, 3.5, AC, 3.2)
    o += pl.hline(2.4, 2.0, 4.0, COMP, 3, None)
    o += pl.dot(3.0, 2.4, KEY, 7)
    o += T(pl.X(2.05), pl.Y(2.4) - 12, '承壓上限 2.4*d t F*_{u}（孔壁壓壞）', 14, COMP, 'start', 'bold')
    o += T(pl.X(3.55), pl.Y(1.95) + 22, '撕出 1.2*L*_{c}*t F*_{u}', 14, AC, 'middle', 'bold')
    o += T(pl.X(3.55), pl.Y(1.95) + 40, '*L*_{c} = *s* − *d*', 14, AC, 'middle')
    o += pl.vline(8 / 3, 0, 3.0, MUT, 1.2)
    o += T(pl.X(8 / 3) + 4, pl.Y(0.5), '絕對下限', 14, MUT, 'start')
    o += T(pl.X(3.0) + 10, pl.Y(2.4) + 22, '交點 *s* = 3*d*', 15, KEY, 'start', 'bold')
    # 右側示意
    o += R(600, 70, 285, 240, '#fff', INK, 1.2, 10)
    cy = 170
    o += R(615, cy - 40, 255, 80, STEEL2, INK, 1.2)
    for xx in (680, 800):
        o += C(xx, cy, 16, '#fff', INK, 1.5)
    o += L(696, cy - 10, 784, cy - 10, AC, 2.4, '5 3') + L(696, cy + 10, 784, cy + 10, AC, 2.4, '5 3')
    o += dim(680, cy + 60, 800, cy + 60, '*s*', MUT, size=15)
    o += dim(696, cy - 58, 784, cy - 58, '*L*_{c}', AC, size=15)
    o += A(830, cy, 870, cy, INK, 2.2, 10)
    o += T(742, 290, '孔與孔之間被撕開的兩條線', 14, AC, 'middle')
    o += T(450, 368, '用標準孔近似 *d*_{h} ≈ *d*；規範絕對下限 8/3 *d*，3*d* 為沿力方向的建議／強制值（容許應力法 §10.3.9）。', 14, MUT, 'middle')
    return svg(W, H, o, '螺栓中心距')


def fig3_4():
    W, H = 900, 300
    o = T(450, 26, 'SS-2009-4㈠：Single V 與 Single Bevel——開槽型式由「接頭幾何」決定', 16, INK, 'middle', 'bold')
    # Single V：對接
    y0, t = 200, 70
    o += P([(60, y0 - t), (200, y0 - t), (225, y0), (60, y0)], INK, 1.4, fill=STEEL2, close=True)
    o += P([(275, y0 - t), (420, y0 - t), (420, y0), (250, y0)], INK, 1.4, fill=STEEL2, close=True)
    o += P([(200, y0 - t), (275, y0 - t), (250, y0), (225, y0)], COMP, 1.4, fill=COMPM, close=True)
    o += T(240, y0 + 34, '(a) Single V：兩片都開斜角', 15, INK, 'middle', 'bold')
    o += T(240, y0 + 56, '對接接頭（兩側都磨得到）', 14, MUT, 'middle')
    # Single Bevel：T 接
    bx = 560
    o += R(bx, y0, 300, 26, STEEL2, INK, 1.4)
    o += P([(bx + 120, y0 - 150), (bx + 170, y0 - 150), (bx + 170, y0), (bx + 155, y0), (bx + 120, y0 - 45)], INK, 1.4, fill=STEEL2, close=True)
    o += P([(bx + 120, y0 - 45), (bx + 155, y0), (bx + 105, y0)], COMP, 1.4, fill=COMPM, close=True)
    o += T(bx + 150, y0 + 56, '(b) Single Bevel：只有一片開斜角', 15, INK, 'middle', 'bold')
    o += T(bx + 150, y0 + 78, 'T 形接頭（底板不能磨）', 14, MUT, 'middle')
    return svg(W, H, o, '開槽型式')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3, 'fig3_4': fig3_4}
