# -*- coding: utf-8 -*-
"""第 4 章：水平力帳本、φ=0 vs 摩擦、P_av 放哪。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig4_1():
    d = ex2016_4()
    W, H = 900, 300
    o = ''
    x0, sc = 220, 1.4
    fric = d['V'] * tan(d['deltaF'])
    coh = d['ca'] * d['B']
    o += T(x0 - 14, 86, '驅動', 16, TEN, 'end', 'bold')
    o += R(x0, 64, d['Pah'] * sc, 36, TEN2, TEN, 1.6) + T(x0 + d['Pah'] * sc / 2, 88, f"*P*_{{ah}}={d['Pah']:.2f}", 15, TEN, 'middle', 'bold')
    o += T(x0 - 14, 166, '抵抗', 16, COMP, 'end', 'bold')
    o += R(x0, 144, fric * sc, 36, COMP2, COMP, 1.6) + T(x0 + fric * sc / 2, 168, f"Σ*V*tan18°={fric:.2f}", 15, COMP, 'middle', 'bold')
    o += R(x0 + fric * sc, 144, coh * sc, 36, '#ffcdd2', COMP, 1.6) + T(x0 + fric * sc + coh * sc / 2, 168, f"*c*_{{a}}*B*={coh:.0f}", 14, COMP, 'middle', 'bold')
    o += T(x0 + (fric + coh) * sc + 10, 168, f"= {fric + coh:.2f}", 15, COMP, 'start', 'bold')
    o += T(x0, 222, f"Σ*V*=*W*_{{1}}+*W*_{{2}}+*P*_{{av}}=564.0+188.0+115.97={d['V']:.2f}", 15, INK)
    o += T(x0, 256, f"*FS*_{{SL}}={fric + coh:.2f}/{d['Pah']:.2f}={d['FS_SL']:.2f} ≥ 1.5", 16, KEY, 'start', 'bold')
    return svg(W, H, o, '水平力帳本')


def fig4_2():
    d = ex2025_3()
    W, H = 900, 400
    pl = Plot(90, 50, 560, 290, 0, 1000, 0, 3)
    o = pl.axes([0, 200, 400, 600, 800, 1000], [0, 1, 2, 3], 'Σ*V* (kN/m)', '*FS*_{SL}')
    o += pl.curve(lambda v: d['R'] / d['Pa'], 0, 1000, COMP, 3)
    o += pl.curve(lambda v: v * tan(20) / d['Pa'], 0, 1000, TEN, 2.4, dash='7 4')
    o += pl.hline(1.5, 0, 1000, WARN, 1.3) + T(pl.X(990), pl.Y(1.5) - 6, '門檻 1.5', 14, WARN, 'end', 'bold')
    o += T(pl.X(980), pl.Y(d['FS']) + 22, f"*φ*=0：*S*_{{u}}*B*/*P*_{{a}}={d['FS']:.2f}（水平）", 15, COMP, 'end', 'bold')
    o += T(pl.X(700), pl.Y(700 * tan(20) / d['Pa']) - 12, '砂底 *δ*=20°（示意）', 15, TEN, 'end', 'bold')
    o += box(670, 70, 215, 140, '2025-3', [f"*P*_{{a}}={d['Pa']:.2f}", f"*R*=30×6={d['R']:.0f}", '牆重是干擾項'], KEY2, KEY)
    return svg(W, H, o, 'φ=0 底土')


def fig4_3():
    d = ex2016_4()
    W, H = 900, 300
    o = ''
    x0 = 300
    Mw = d['W1'] * d['x1'] + d['W2'] * d['x2']
    Mpav = d['Pav'] * d['xpa']
    sc = 0.17
    o += T(x0 - 14, 80, '*P*_{av} 進 Σ*M*_{R}', 15, KEY, 'end', 'bold')
    o += R(x0, 60, Mw * sc, 30, AC2, AC, 1.4) + R(x0 + Mw * sc, 60, Mpav * sc, 30, TEN2, TEN, 1.4)
    o += R(x0, 96, d['MO'] * sc, 30, COMP2, COMP, 1.4)
    o += T(x0 + (Mw + Mpav) * sc + 10, 82, f"{d['MR']:.1f}", 14, AC, 'start', 'bold')
    o += T(x0 + d['MO'] * sc + 10, 118, f"{d['MO']:.1f}　→ *FS*={d['FS_OT']:.2f}", 15, KEY, 'start', 'bold')
    o += T(x0 - 14, 190, '*P*_{av} 從 Σ*M*_{O} 扣', 15, MUT, 'end', 'bold')
    o += R(x0, 170, Mw * sc, 30, AC2, AC, 1.4)
    o += R(x0, 206, (d['MO'] - Mpav) * sc, 30, COMP2, COMP, 1.4)
    o += T(x0 + Mw * sc + 10, 192, f"{Mw:.1f}", 14, AC, 'start', 'bold')
    o += T(x0 + (d['MO'] - Mpav) * sc + 10, 228, f"{d['MO'] - Mpav:.1f}　→ *FS*={d['FS_OT_alt']:.2f}", 15, MUT, 'start', 'bold')
    o += T(x0, 272, '淨力矩相同（1480.8），FS 差七倍 → 寫明定義', 15, COMP, 'start', 'bold')
    return svg(W, H, o, 'P_av 放哪')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
