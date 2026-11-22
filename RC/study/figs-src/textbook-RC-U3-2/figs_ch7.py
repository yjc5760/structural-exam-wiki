# -*- coding: utf-8 -*-
"""第 7 章：單向版版帶與彎矩係數、雙向版角隅配筋。"""
from figs_common import *  # noqa
from calcs import p2013_1
import math

S13 = p2013_1()


def fig7_1():
    W, H = 900, 500
    o = T(450, 24, '單向版 = 一排 1 m 寬的連續梁', 16, INK, 'middle', 'bold')
    x0, x1, y0 = 80, 820, 60
    span = (x1 - x0) / 4
    o += R(x0, y0, x1 - x0, 140, STEEL2, INK, 1.4)
    for i in range(5):
        xx = x0 + i * span
        o += R(xx - 6, y0, 12, 140, STEEL3, INK, 1)
    o += R(x0, y0 + 50, x1 - x0, 36, TEN2, TEN, 2)
    o += T(x0 + span * 2, y0 + 74, '1 m 寬版帶', 15, TEN, 'middle', 'bold')
    o += T(x0 + span / 2, y0 + 128, '外跨', 14, MUT, 'middle')
    o += T(x0 + span * 1.5, y0 + 128, '內跨', 14, MUT, 'middle')
    o += T(x0 + span * 2.5, y0 + 128, '內跨', 14, MUT, 'middle')
    o += T(x0 + span * 3.5, y0 + 128, '外跨', 14, MUT, 'middle')
    # 係數圖
    yb = 320
    o += L(x0, yb, x1, yb, INK, 1.4)
    k = 900
    sup = [-1 / 24, -1 / 10, -1 / 11, -1 / 10, -1 / 24]
    mid = [1 / 14, 1 / 16, 1 / 16, 1 / 14]
    labs_s = ['1/24', '1/10', '1/11', '1/10', '1/24']
    labs_m = ['1/14', '1/16', '1/16', '1/14']
    pts = []
    for i in range(4):
        xa, xb = x0 + i * span, x0 + (i + 1) * span
        ma, mb, mm = sup[i], sup[i + 1], mid[i]
        for j in range(41):
            t = j / 40
            # 拋物線通過 (0,ma)、(0.5,mm)、(1,mb)
            m = ma * (1 - t) * (1 - 2 * t) + mm * 4 * t * (1 - t) + mb * t * (2 * t - 1)
            pts.append((xa + span * t, yb - m * k))
    o += P([(x0, yb)] + pts + [(x1, yb)], KEY, 2.4, fill=KEY2, close=True)
    for i in range(5):
        xx = x0 + i * span
        o += T(xx, yb - sup[i] * k + 22, '−' + labs_s[i], 15, COMP, 'middle', 'bold')
    for i in range(4):
        xx = x0 + (i + 0.5) * span
        o += T(xx, yb - mid[i] * k - 10, '+' + labs_m[i], 15, TEN, 'middle', 'bold')
    o += T(x0 - 10, yb - 4, '0', 14, MUT, 'end')
    o += T(450, 488, f"簡支梁對照 1/8；RC-2013-1 外支承：*M*_{{u}} = *w*_{{u}}ℓ_{{n}}^{{2}}/24 = {S13['Mcoef']['外支承 1/24']:.3f} tf·m/m", 15, INK, 'middle', 'bold')
    return svg(W, H, o, '單向版係數')


def fig7_2():
    W, H = 900, 400
    o = T(450, 24, '雙向版外角隅：想翹起來、被邊梁壓住', 16, INK, 'middle', 'bold')
    # 左：示意碟形
    cx, cy = 210, 220
    o += P([(cx - 150, cy - 40), (cx + 60, cy - 110), (cx + 170, cy - 30), (cx - 40, cy + 40)], INK, 1.6, fill=STEEL2, close=True)
    o += P([(cx - 120, cy - 30), (cx + 50, cy - 86), (cx + 140, cy - 24), (cx - 30, cy + 28)], MUT, 1, dash='4 3', close=True)
    o += A(cx - 150, cy - 40, cx - 150, cy - 90, COMP, 2.4, 10)
    o += T(cx - 142, cy - 80, '角落想翹起', 15, COMP, 'start', 'bold')
    o += T(cx, cy + 90, '碟形下沉（虛線）', 14, MUT, 'middle')
    o += T(cx, cy + 112, '邊梁把角落壓住 → 角隅產生扭轉彎矩', 14, MUT, 'middle')
    # 右：角隅平面
    px, py, sz = 520, 70, 300
    o += R(px, py, sz, sz, STEEL2, INK, 1.6)
    o += L(px, py, px + sz, py, INK, 5) + L(px, py, px, py + sz, INK, 5)
    q = sz * 0.42
    o += R(px, py, q, q, WARN2, WARN, 2, dash='6 3')
    # 版頂：平行對角線（＼）
    for i in range(0, 6):
        t = i / 6
        o += L(px + q * t, py, px + q, py + q * (1 - t), COMP, 1.8)
        if i:
            o += L(px, py + q * t, px + q * (1 - t), py + q, COMP, 1.8)
    # 版底：垂直對角線（／）
    for i in range(1, 12):
        t = i / 6
        if t <= 1:
            o += L(px + q * t, py, px, py + q * t, AC, 1.8, '6 3')
        else:
            o += L(px + q, py + q * (t - 1), px + q * (t - 1), py + q, AC, 1.8, '6 3')
    o += hdim(px, px + q, py + q + 22, 'ℓ/5', WARN, 1, 15)
    o += vdim(px + q + 14, py, py + q, 'ℓ/5', WARN, 1, 15)
    o += T(px + sz / 2 + 60, py + sz - 70, '紅：版頂，平行對角線', 15, COMP, 'middle', 'bold')
    o += T(px + sz / 2 + 60, py + sz - 46, '藍：版底，垂直對角線', 15, AC, 'middle', 'bold')
    o += T(px + sz / 2 + 60, py + sz - 22, '量 = 最大正彎矩筋（ℓ＝長跨）', 14, INK, 'middle')
    o += T(px - 8, py - 8, '外角隅', 15, INK, 'end', 'bold')
    return svg(W, H, o, '角隅配筋')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}
