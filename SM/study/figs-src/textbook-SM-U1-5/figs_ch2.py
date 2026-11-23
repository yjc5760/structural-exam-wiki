# -*- coding: utf-8 -*-
"""第 2 章：三角塊自由體、2θ、極點法。"""
from plot import *  # noqa
from calcs import *  # noqa
from figs_ch1 import circle


def fig2_1():
    W, H = 900, 420
    o = ''
    th = rad(35)
    # 三角塊：A 左下、B 右下、Cc 右上；斜面 A–Cc 與水平夾 θ
    sc = 260
    Ax, Ay = 90, 330
    Bx, By = Ax + sc * math.cos(th), Ay
    Cx, Cy = Bx, Ay - sc * math.sin(th)
    o += P([(Ax, Ay), (Bx, By), (Cx, Cy)], INK, 2.2, fill=STEEL2, close=True)
    # θ 標示
    o += curve_arrow([(Ax + 60 * math.cos(t), Ay - 60 * math.sin(t)) for t in [i * th / 20 for i in range(21)]], MUT, 1.4, 8)
    o += T(Ax + 70, Ay - 14, '*θ*', 16, INK, 'start')
    # 底面 σ1（向上作用於塊）
    for k in range(5):
        x = Ax + 30 + k * (Bx - Ax - 50) / 4
        o += A(x, Ay + 50, x, Ay + 4, COMP, 2, 9)
    o += T((Ax + Bx) / 2, Ay + 72, '*σ*_{1}·cos*θ*（底面）', 15, COMP, 'middle', 'bold')
    # 側面 σ3（向左作用）
    for k in range(3):
        y = Cy + 20 + k * (By - Cy - 40) / 2
        o += A(Bx + 50, y, Bx + 4, y, AC, 2, 9)
    o += T(Bx + 56, (Cy + By) / 2 + 5, '*σ*_{3}·sin*θ*', 15, AC, 'start', 'bold')
    # 斜面法線與切線方向
    mx, my = (Ax + Cx) / 2, (Ay + Cy) / 2
    nx, ny = -math.sin(th), -math.cos(th)   # 外法線（往左上）
    o += A(mx + 80 * nx, my + 80 * ny, mx + 3 * nx, my + 3 * ny, KEY, 2.6, 11) + T(mx + 84 * nx - 6, my + 84 * ny, '*σ*_{n}（壓）', 16, KEY, 'end', 'bold')
    tx, ty = -math.cos(th), math.sin(th)    # 沿斜面往左下
    o += A(mx, my, mx + 70 * tx, my + 70 * ty, WARN, 2.6, 11) + T(mx + 74 * tx - 4, my + 74 * ty + 16, '*τ*', 16, WARN, 'end', 'bold')
    o += T(mx + 14, my + 26, '斜面（面積 1）', 14, INK, 'start')
    # 右：力多邊形
    ox, oy = 640, 330
    F1 = 200 * math.cos(th)    # σ1cosθ（σ1=200）
    F3 = 80 * math.sin(th)     # σ3sinθ（σ3=80）
    p1 = (ox, oy - F1 * 1.0)
    p2 = (p1[0] - F3 * 1.0, p1[1])
    o += A(ox, oy, *p1, COMP, 2.6, 11) + A(p1[0], p1[1], *p2, AC, 2.6, 11)
    o += A(ox, oy, *p2, INK, 1.8, 10, dash='5 4')
    o += T(ox + 8, (oy + p1[1]) / 2, '*σ*_{1}cos*θ*', 15, COMP, 'start', 'bold')
    o += T((p1[0] + p2[0]) / 2, p1[1] - 10, '*σ*_{3}sin*θ*', 15, AC, 'middle', 'bold')
    o += T(ox, oy + 26, '頭尾相接 → 合力', 14, INK, 'middle')
    o += T(ox, oy + 48, '再分解成 *σ*_{n}、*τ*', 14, INK, 'middle')
    o += box(700, 40, 190, 110, '兩行平衡', ['*σ*_{n}=*σ*_{1}cos²*θ*+*σ*_{3}sin²*θ*', '*τ*=(*σ*_{1}−*σ*_{3})sin*θ*cos*θ*'], KEY2, KEY, lsize=14)
    return svg(W, H, o, '斜面平衡')


def fig2_2():
    d = ex2024_1()
    W, H = 900, 420
    pl = Plot(80, 50, 600, 300, 0, 400, 0, 200)
    o = pl.axes([0, 100, 200, 300, 400], [0, 50, 100, 150, 200], '*σ* (kPa)', '*τ*')
    o += circle(pl, d['s1'], d['s3'], COMP, 3)
    Cc, R = d['C'], d['R']
    th = 30
    px, py = Cc + R * cos(180 - 2 * th + 180), 0
    # 從 σ1 點逆時針轉 2θ：角度從 0 起算
    ang = 2 * th
    ptx, pty = Cc + R * cos(ang), R * sin(ang)
    o += L(pl.X(Cc), pl.Y(0), pl.X(d['s1']), pl.Y(0), INK, 1.6)
    o += L(pl.X(Cc), pl.Y(0), pl.X(ptx), pl.Y(pty), KEY, 2.2)
    o += curve_arrow([pl.pt(Cc + 40 * cos(a), 40 * sin(a) * (pl.w / pl.h) * (200 / 400)) for a in [i * ang / 20 for i in range(21)]], KEY, 1.6, 8)
    o += T(pl.X(Cc + 52), pl.Y(14), '2*θ*', 16, KEY, 'start', 'bold')
    o += C(pl.X(ptx), pl.Y(pty), 6, KEY, '#fff', 1.8)
    o += T(pl.X(ptx) + 10, pl.Y(pty) - 10, f'*θ*=30°：({ptx:.0f}, {pty:.1f})', 15, KEY, 'start', 'bold')
    o += C(pl.X(d['s1']), pl.Y(0), 5, COMP, '#fff', 1.6) + T(pl.X(d['s1']), pl.Y(0) - 10, '*σ*_{1}=340（水平面）', 14, COMP, 'middle', 'bold')
    o += C(pl.X(d['s3']), pl.Y(0), 5, COMP, '#fff', 1.6) + T(pl.X(d['s3']), pl.Y(0) - 10, '*σ*_{3}=100', 14, COMP, 'middle', 'bold')
    o += C(pl.X(Cc), pl.Y(R), 6, WARN, '#fff', 1.8) + T(pl.X(Cc), pl.Y(R) - 12, '圓頂：45° 面，*τ*_{max}=120', 15, WARN, 'middle', 'bold')
    o += L(pl.X(Cc), pl.Y(0), pl.X(Cc), pl.Y(R), WARN, 1.3, '5 4')
    o += T(pl.X(Cc) + 4, pl.Y(0) + 34, '圓心 220', 14, INK, 'middle')
    o += box(700, 70, 185, 130, '實際 *θ* ↔ 圓上 2*θ*', ['*θ*=0：*σ*_{1} 點', '*θ*=45°：圓頂', '*θ*=90°：*σ*_{3} 點'], KEY2, KEY)
    return svg(W, H, o, '莫爾圓 2θ')


def fig2_3():
    d = ex2018_2()
    W, H = 900, 430
    pl = Plot(80, 50, 600, 300, 0, 140, 0, 70)
    o = pl.axes([0, 20, 40, 60, 80, 100, 120, 140], [0, 20, 40, 60], '*σ*′ (kPa)', '*τ*')
    s1, s3 = d['s1e'], d['s3e']
    phi = d['phi_e']
    o += circle(pl, s1, s3, TEN, 3)
    xe = min(140, 70 / tan(phi))
    o += L(pl.X(0), pl.Y(0), pl.X(xe), pl.Y(xe * tan(phi)), WARN, 2, '7 4')
    Cc, R = (s1 + s3) / 2, (s1 - s3) / 2
    tx, ty = Cc - R * sin(phi), R * cos(phi)
    o += L(pl.X(Cc), pl.Y(0), pl.X(tx), pl.Y(ty), INK, 1.4, '4 3')
    o += C(pl.X(tx), pl.Y(ty), 6, KEY, '#fff', 1.8)
    o += L(pl.X(s3), pl.Y(0), pl.X(tx), pl.Y(ty), KEY, 2.6)
    o += C(pl.X(s3), pl.Y(0), 6.5, AC, '#fff', 2)
    o += T(pl.X(s3) - 8, pl.Y(0) + 46, '極點 *P*＝(*σ*_{3}′, 0)', 15, AC, 'start', 'bold')
    o += L(pl.X(s3), pl.Y(0), pl.X(s3) + 120, pl.Y(0), MUT, 1)
    ang = deg(math.atan2(pl.Y(0) - pl.Y(ty), pl.X(tx) - pl.X(s3)))  # 像素角
    o += curve_arrow([(pl.X(s3) + 46 * math.cos(rad(a)), pl.Y(0) - 46 * math.sin(rad(a))) for a in [i * ang / 20 for i in range(21)]], KEY, 1.6, 8)
    o += T(pl.X(s3) + 54, pl.Y(0) - 18, '*θ*_{f}', 16, KEY, 'start', 'bold')
    o += T(pl.X(tx) - 8, pl.Y(ty) - 12, '切點＝破壞面', 15, KEY, 'end', 'bold')
    o += box(700, 70, 185, 160, '圓周角＝圓心角/2', ['圓心角 90°+*φ*′', '→ *θ*_{f}=45°+*φ*′/2', f"本例 {d['theta']:.2f}°", '（*φ*′=34.26°）'], KEY2, KEY)
    o += T(700, 270, '（縱橫軸等比例，', 14, MUT)
    o += T(700, 292, '角度可直接量）', 14, MUT)
    return svg(W, H, o, '極點法')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3}
