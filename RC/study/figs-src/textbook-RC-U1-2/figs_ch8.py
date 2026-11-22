# -*- coding: utf-8 -*-
"""第 8 章：耐震圍束箍筋 Ash、so（精簡）。"""
from figs_col import *  # noqa
from calcs import rc2013_2

Q = rc2013_2()


def fig8_1():
    W, H = 900, 440
    o = T(450, 26, 'RC-2013-2：50×50 柱、16-D32，外箍＋3 支繫筋 → 每個方向 5 腳', 16, INK, 'middle', 'bold')
    sc = 6.4
    x0, y0 = 90, 60
    b = 50
    o += R(x0, y0, b * sc, b * sc, STEEL2, INK, 1.6)
    cc = 4
    hc = Q['hc']
    o += R(x0 + cc * sc, y0 + cc * sc, hc * sc, hc * sc, 'none', WARN, 3, 6)
    # 主筋位置
    inner = cc + 1.27 + 3.22 / 2
    span = b - 2 * inner
    pos = [inner + span * i / 4 for i in range(5)]
    bars = set()
    for p in pos:
        for q in (pos[0], pos[-1]):
            bars.add((p, q)); bars.add((q, p))
    for (px, py) in bars:
        o += C(x0 + px * sc, y0 + py * sc, 3.22 * sc / 2, INK, '#fff', 1)
    # 繫筋（垂直、水平各 3 支）
    for p in pos[1:4]:
        o += L(x0 + p * sc, y0 + (cc + 0.6) * sc, x0 + p * sc, y0 + (b - cc - 0.6) * sc, TEN, 2.4)
        o += L(x0 + (cc + 0.6) * sc, y0 + p * sc, x0 + (b - cc - 0.6) * sc, y0 + p * sc, AC, 2.4, '6 3')
    o += hdim(x0 + cc * sc, x0 + (cc + hc) * sc, y0 + b * sc + 18, f"*h*_{{c}} = {hc:.0f}（量到箍筋外緣）", WARN, 1)
    o += hdim(x0 + pos[1] * sc, x0 + pos[2] * sc, y0 - 12, f"*h*_{{x}} = {Q['hx']:.2f}", KEY, -1, size=14)
    o += box(470, 60, 420, 330, '計算', [f"*A*_{{sh}}/*s* = 0.3*h*_{{c}}(*A*_{{g}}/*A*_{{ch}} − 1)*f*′_{{c}}/*f*_{{yt}} = {Q['a1']:.3f}",
                                        f"　　　　　　0.09*h*_{{c}}*f*′_{{c}}/*f*_{{yt}} = {Q['a2']:.3f}",
                                        f"*s* ≤ min(*b*/4, 6*d*_{{b}}, *s*_{{o}}) = min({Q['b4']}, {Q['six_db']:.1f}, {Q['so']:.0f})",
                                        f"*s*_{{o}} = 10 + (35 − {Q['hx']:.2f})/3 = {Q['so_raw']:.2f} → 上限 15",
                                        f"取 *s* = {Q['s']:.0f} cm",
                                        f"*A*_{{sh}} ≥ {Q['a1']:.3f} × 12 = {Q['req']:.2f} cm²",
                                        f"D13：{Q['req']:.2f}/1.27 → {Q['legs']} 腳 = 6.35 cm² ✔",
                                        '綠實線：*x* 向腳；藍虛線：*y* 向腳'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, 'Ash 配置')


ALL = {'fig8_1': fig8_1}
