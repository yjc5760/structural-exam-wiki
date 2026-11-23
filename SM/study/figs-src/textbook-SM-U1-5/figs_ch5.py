# -*- coding: utf-8 -*-
"""第 5 章：圓頂軌跡、AC/LE、2008-2 有效應力路徑。"""
from plot import *  # noqa
from calcs import *  # noqa
from figs_ch1 import circle


def fig5_1():
    W, H = 900, 400
    pl = Plot(80, 50, 600, 300, 0, 300, 0, 150)
    o = pl.axes([0, 50, 100, 150, 200, 250, 300], [0, 50, 100, 150], '*σ*、*p*', '*τ*、*q*')
    s3 = 80.0
    pts = []
    for k, s1 in enumerate([80, 120, 160, 200, 240]):
        o += circle(pl, s1, s3, COMP if k == 4 else MUT, 2.2 if k == 4 else 1.4, None if k == 4 else '5 4')
        pc, qc = (s1 + s3) / 2, (s1 - s3) / 2
        pts.append(pl.pt(pc, qc))
        o += C(*pl.pt(pc, qc), 5.5, KEY, '#fff', 1.6)
    o += curve_arrow(pts, KEY, 2.6, 12)
    o += T(pts[-1][0] + 10, pts[-1][1] - 8, '斜率 1（AC）', 15, KEY, 'start', 'bold')
    o += T(pl.X(s3), pl.Y(0) + 40, '*σ*_{3}=80 不變', 14, INK, 'middle')
    o += box(700, 70, 185, 130, '圓 → 點', ['*p*＝圓心', '*q*＝半徑', '連起來＝路徑'], KEY2, KEY)
    return svg(W, H, o, '圓頂軌跡')


def fig5_2():
    d = ex2013_3()
    W, H = 900, 470
    pl = Plot(80, 50, 600, 340, 0, 480, 0, 272)
    o = pl.axes([0, 80, 160, 240, 320, 400, 480], [0, 50, 100, 150, 200, 250], '*p*、*p*′ (kPa)', '*q*')
    for phi, c, nm, dash in ((d['phi_e'], TEN, "*K*_{f}′（*φ*′=28.04°）", '7 4'), (d['phi_AC'], COMP, '*φ*_{AC}=19.23°', '3 4'), (d['phi_LE'], AC, '*φ*_{LE}=31.59°', '3 4')):
        ta = sin(phi)
        xe = min(480, 272 / ta)
        o += L(pl.X(0), pl.Y(0), pl.X(xe), pl.Y(xe * ta), c, 1.6, dash)
        o += T(pl.X(xe) - 4, pl.Y(xe * ta) - 8, nm, 14, c, 'end', 'bold')
    o += A(*pl.pt(d['p0'], d['q0']), *pl.pt(d['pAC'], d['qf']), COMP, 3, 12)
    o += A(*pl.pt(d['p0'], d['q0']), *pl.pt(d['pLE'], d['qf']), AC, 3, 12)
    # ESP：二次曲線向左彎
    P0 = (d['p0'], d['q0']); P2 = (d['pE'], d['qf']); P1 = (d['p0'] + 5, d['qf'] * 0.85)
    esp = [pl.pt((1 - t) ** 2 * P0[0] + 2 * (1 - t) * t * P1[0] + t * t * P2[0], (1 - t) ** 2 * P0[1] + 2 * (1 - t) * t * P1[1] + t * t * P2[1]) for t in [i / 40 for i in range(41)]]
    o += curve_arrow(esp, TEN, 3.2, 12)
    for (p, q, c, nm, anc, dx, dy) in ((d['p0'], d['q0'], INK, '起點 (340, 60)', 'start', 10, 20),
                                       (d['pAC'], d['qf'], COMP, 'AC (417.5, 137.5)', 'middle', 0, 26),
                                       (d['pLE'], d['qf'], AC, 'LE (262.5, 137.5)', 'end', -10, 4),
                                       (d['pE'], d['qf'], TEN, '(292.5, 137.5)', 'middle', 0, -14)):
        o += C(*pl.pt(p, q), 5.5, c, '#fff', 1.6)
        o += T(pl.X(p) + dx, pl.Y(q) + dy, nm, 14, c, anc, 'bold')
    yy = pl.Y(d['qf']) - 44
    o += A(pl.X(d['pE']), yy, pl.X(d['pAC']), yy, COMP, 1.6, 8, both=True) + T((pl.X(d['pE']) + pl.X(d['pAC'])) / 2, yy - 6, '+125', 14, COMP, 'middle', 'bold')
    o += A(pl.X(d['pLE']), yy, pl.X(d['pE']), yy, AC, 1.6, 8, both=True) + T((pl.X(d['pLE']) + pl.X(d['pE'])) / 2, yy - 6, '−30', 14, AC, 'middle', 'bold')
    o += box(700, 70, 185, 160, 'ESP 唯一', ['紅 AC：+1', '藍 LE：−1', '綠：共用有效路徑', f"*A*_{{f}}={d['Af']:.3f}"], KEY2, KEY)
    return svg(W, H, o, 'AC 與 LE 應力路徑')


def fig5_3():
    d = ex2008_2()
    W, H = 900, 420
    pl = Plot(80, 50, 560, 300, 0, 80, 0, 80 * 300 / 560)
    o = pl.axes([0, 20, 40, 60, 80], [0, 10, 20, 30, 40], "*p*′ (kPa)", '*q*')
    o += L(pl.X(0), pl.Y(0), pl.X(80), pl.Y(80 * 0.5), WARN, 2.4) + T(pl.X(79), pl.Y(39) + 40, "*K*_{f}：*q*=0.5*p*′", 15, WARN, 'end', 'bold')
    pts = []
    for i in range(41):
        dq = d['dq'] * i / 40
        s1 = d['sv0'] + d['a1'] * dq
        s3 = d['sh0'] + d['a3'] * dq
        pts.append(pl.pt((s1 + s3) / 2, (s1 - s3) / 2))
    o += curve_arrow(pts, TEN, 3, 12)
    p0, q0 = (d['sv0'] + d['sh0']) / 2, (d['sv0'] - d['sh0']) / 2
    o += C(*pl.pt(p0, q0), 6, INK, '#fff', 1.6) + T(pl.X(p0) + 10, pl.Y(q0) + 20, f'*K*_{{0}} 起點 ({p0:.2f}, {q0:.2f})', 14, INK, 'start', 'bold')
    o += C(*pts[-1], 6.5, KEY, '#fff', 1.8)
    o += T(pts[-1][0] - 10, pts[-1][1] - 12, f"破壞：Δ*q*={d['dq']:.2f}", 15, KEY, 'end', 'bold')
    # 錯：不扣 Δu（總應力路徑）
    wr = [pl.pt(p0 + 0.5 * dq, q0 + dq / 6) for dq in [d['dq'] * i / 40 for i in range(41)]]
    o += P(wr, MUT, 2, dash='7 4') + T(wr[-1][0] + 8, wr[-1][1] + 18, '不扣 Δ*u*（錯）', 14, MUT, 'start')
    o += box(670, 70, 215, 160, '孔壓吃掉 *p*′', ['Δ*u*=0.567Δ*q*', '*σ*_{1}′=66.90+0.100Δ*q*', '*σ*_{3}′=33.45−0.233Δ*q*', f"*H*={d['H']:.2f} m"], KEY2, KEY, lsize=14)
    return svg(W, H, o, '2008-2 有效應力路徑')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3}
