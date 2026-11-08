# -*- coding: utf-8 -*-
"""第 1 章：換手鏈（S1）、SS-2012-4 最弱一環、φ 排序、保險絲預告。"""
from plot import *  # noqa
from calcs import ss2012_4, PHI, omega

D = ss2012_4()


def _station(x, y, w, h, title, lines, c, fill='#fff', tsize=16):
    o = R(x, y, w, h, fill, c, 2.2, 12)
    o += R(x, y, w, 34, c, None, 0, 12) + R(x, y + 20, w, 14, c, None)
    o += T(x + w / 2, y + 24, title, tsize, '#fff', 'middle', 'bold')
    for i, s in enumerate(lines):
        o += T(x + w / 2, y + 58 + i * 23, s, 14, INK, 'middle')
    return o


def fig1_1():
    W, H = 900, 470
    o = T(450, 28, '(a) 螺栓接合：力從構材走到接合板，一共換手五站', 16, INK, 'middle', 'bold')
    bw, gap, y, h = 160, 20, 44, 140
    st = [('構材本體', ['全斷面降伏', 'GSY　φ = 0.90'], TEN),
          ('構材的孔區', ['淨斷面斷裂 NSF', '塊狀剪力', 'φ = 0.75'], COMP),
          ('孔壁', ['孔壁承壓', '（撕出・壓扁）', 'φ = 0.75'], WARN),
          ('螺栓', ['螺栓剪斷', 'φ = 0.75'], WARN),
          ('接合板', ['再走一次：', '承壓・NSF・', 'GSY・塊剪'], AC)]
    for i, (t, ls, c) in enumerate(st):
        x = 10 + i * (bw + gap)
        o += _station(x, y, bw, h, t, ls, c)
        if i < len(st) - 1:
            o += A(x + bw + 2, y + h / 2, x + bw + gap - 2, y + h / 2, INK, 2.6, 11)
    o += T(450, y + h + 32, '每一站都是一種可能的破壞；接合的強度 = 五站裡最小的那一個', 15, KEY, 'middle', 'bold')

    o += T(450, 270, '(b) 銲接接合：換手只剩三站', 16, INK, 'middle', 'bold')
    bw2, gap2, y2, h2 = 270, 30, 286, 120
    st2 = [('構材本體', ['GSY・NSF', '（同拉力構材）'], TEN),
           ('熔合面（母材銲道邊）', ['母材剪斷', '0.6*F*_{u}・φ = 0.75'], COMP),
           ('銲喉', ['銲材剪斷', '0.6*F*_{EXX}・φ = 0.75'], WARN)]
    for i, (t, ls, c) in enumerate(st2):
        x = 10 + i * (bw2 + gap2)
        o += _station(x, y2, bw2, h2, t, ls, c)
        if i < 2:
            o += A(x + bw2 + 3, y2 + h2 / 2, x + bw2 + gap2 - 3, y2 + h2 / 2, INK, 2.6, 11)
    o += T(450, y2 + h2 + 34, '沒有孔：淨斷面、承壓、螺栓剪斷三站消失，多了「從哪個面切斷銲道」', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '螺栓與銲接的換手鏈')


def fig1_2():
    W, H = 900, 548
    o = T(450, 26, '(a) SS-2012-4 的換手鏈：梁剪力 *V*_{u} = 180 kN 從梁腹走到柱', 16, INK, 'middle', 'bold')
    bw, gap, y, h = 160, 20, 42, 92
    st = [('梁腹板', ['題目未給 *t*_{w}', '不檢核'], STEEL),
          ('螺栓 ×3', ['剪斷'], WARN),
          ('剪力板', ['承壓・降伏', '斷裂・塊剪'], AC),
          ('銲道', ['題目假設足夠'], STEEL),
          ('柱', ['（不在本題）'], STEEL)]
    for i, (t, ls, c) in enumerate(st):
        x = 10 + i * (bw + gap)
        o += _station(x, y, bw, h, t, ls, c)
        if i < 4:
            o += A(x + bw + 2, y + h / 2, x + bw + gap - 2, y + h / 2, INK, 2.4, 10)
    o += T(450, 172, f'(b) 板厚 *t* = {D["t_use"]:.0f} mm 時，五站各自撐得住多少（LRFD φ*R*_{{n}}，kN）', 16, INK, 'middle', 'bold')
    pl = Plot(190, 196, 600, 270, 0, 300, 0, 5)
    o += pl.axes([0, 50, 100, 150, 200, 250, 300], [], 'kN', '', grid=True, size=14)
    caps = D['cap']
    cmin = D['cap_min']
    for i, (nm, v) in enumerate(caps):
        yc = pl.Y(4.5 - i)
        hh = 34
        c = COMP if abs(v - cmin) < 1e-9 else STEEL
        fill = COMP2 if c == COMP else STEEL2
        o += R(pl.X(0), yc - hh / 2, pl.X(v) - pl.X(0), hh, fill, c, 1.8, 3)
        o += T(pl.X(0) - 10, yc + 5, nm, 15, INK, 'end', 'bold')
        o += T(pl.X(v) + 8, yc + 5, f'{v:.1f}', 15, c, 'start', 'bold')
    o += pl.vline(D['Vu'] / 1e3, 0, 5, KEY, 2.4, '7 5')
    o += T(pl.X(D['Vu'] / 1e3), pl.y0 - 4, f'需求 *V*_{{u}} = {D["Vu"]/1e3:.0f}', 15, KEY, 'middle', 'bold')
    o += T(450, 532, f'鏈子的強度 = 最短那一條 = 剪力斷裂 {cmin:.1f} kN ≥ 180 OK（需求／容量 = {D["ratio"]:.2f}）', 15, COMP, 'middle', 'bold')
    return svg(W, H, o, 'SS-2012-4 的最弱一環')


def fig1_3():
    W, H = 900, 400
    pl = Plot(70, 70, 760, 10, 0.70, 1.05, 0, 1)
    yb = 200
    o = T(450, 30, 'LRFD 的 φ：破壞前的預警越明顯、後果越輕，φ 越大', 16, INK, 'middle', 'bold')
    o += A(pl.X(0.70), yb, pl.X(1.05) + 10, yb, INK, 2, 10)
    for v in (0.75, 0.80, 0.90, 1.00):
        o += L(pl.X(v), yb - 6, pl.X(v), yb + 6, INK, 1.6)
        o += T(pl.X(v), yb + 28, f'{v:.2f}', 16, INK, 'middle', 'bold')
        o += T(pl.X(v), yb + 56, f'Ω = {omega(v):.2f}', 15, WARN, 'middle', 'bold')
    o += T(pl.X(0.70) - 4, yb + 28, 'φ', 17, INK, 'end', 'bold')
    o += T(pl.X(0.70) - 4, yb + 56, 'ASD', 15, WARN, 'end', 'bold')
    groups = [(0.75, '斷裂型（拉斷、剪斷）', ['螺栓剪斷・孔壁承壓', 'NSF・塊狀剪力', '剪力斷裂・填角銲'], COMP, 150, 220),
              (0.80, 'PJP 開槽銲', ['未全滲透，', '根部像裂縫'], WARN, 342, 120),
              (0.90, '降伏型（伸長）', ['GSY・剪力降伏', 'CJP（同母材）'], TEN, 560, 180),
              (1.00, '滑動', ['摩阻型（標準孔）', '滑了還能承壓'], AC, 770, 160)]
    for v, t, ls, c, cx, bw in groups:
        bh = 30 + 22 * len(ls)
        by = yb - 30 - bh
        o += R(cx - bw / 2, by, bw, bh, '#fff', c, 2, 9)
        o += T(cx, by + 22, t, 15, c, 'middle', 'bold')
        for i, s in enumerate(ls):
            o += T(cx, by + 44 + i * 21, s, 14, INK, 'middle')
        o += L(cx, by + bh, pl.X(v), yb - 8, c, 1.6, '4 3')
        o += C(pl.X(v), yb, 6, c, '#fff', 1.6)
    o += A(pl.X(0.74), yb + 92, pl.X(1.02), yb + 92, KEY, 3, 13)
    o += T(pl.X(0.88), yb + 84, '預警越明顯、越可預測 → φ 越大、Ω 越小', 16, KEY, 'middle', 'bold')
    o += T(450, yb + 130, 'ASD 的安全係數 Ω = 1.5 / φ（因為 1.2*D* + 1.6*L* ≈ 1.5(*D* + *L*)）', 15, MUT, 'middle')
    o += T(450, yb + 160, 'PJP 0.80 是例外：同樣是剪斷型，但規範對未熔透的根部打折較少，記成「介於兩者」即可', 14, MUT, 'middle')
    return svg(W, H, o, 'φ 值的排序')


def fig1_4():
    W, H = 900, 380
    o = ''
    names = ['銲道', '螺栓', '梁本體', '柱']
    # (a) 一般設計：需求線以上都可以，最弱的一站決定
    pa = Plot(70, 70, 330, 220, 0, 4, 0, 1.6)
    va = [1.30, 1.15, 1.45, 1.55]
    o += T(235, 30, '(a) 一般設計：每一站 ≥ 需求即可', 16, INK, 'middle', 'bold')
    o += L(pa.x0, pa.y0 + pa.h, pa.x0 + pa.w, pa.y0 + pa.h, INK, 1.4)
    for i, v in enumerate(va):
        x = pa.X(i + 0.5)
        c = COMP if v == min(va) else STEEL
        o += R(x - 28, pa.Y(v), 56, pa.Y(0) - pa.Y(v), COMP2 if c == COMP else STEEL2, c, 1.8, 3)
        o += T(x, pa.Y(0) + 24, names[i], 15, INK, 'middle', 'bold')
    o += pa.hline(1.0, c=KEY, w=2.2, dash='7 5') + T(pa.X(4), pa.Y(1.0) + 22, '需求', 15, KEY, 'end', 'bold')
    o += T(pa.X(1.5), pa.Y(1.15) - 10, '最先壞的是誰？碰運氣', 14, COMP, 'middle', 'bold')
    o += T(235, 352, '最弱一環是「剛好」最弱的那一個', 15, MUT, 'middle')
    # (b) 耐震：指定保險絲
    pb = Plot(520, 70, 330, 220, 0, 4, 0, 1.6)
    vb = [1.42, 1.38, 1.0, 1.50]
    o += T(685, 30, '(b) 耐震設計：指定梁先降伏（保險絲）', 16, INK, 'middle', 'bold')
    o += L(pb.x0, pb.y0 + pb.h, pb.x0 + pb.w, pb.y0 + pb.h, INK, 1.4)
    for i, v in enumerate(vb):
        x = pb.X(i + 0.5)
        c = KEY if i == 2 else STEEL
        o += R(x - 28, pb.Y(v), 56, pb.Y(0) - pb.Y(v), KEY2 if c == KEY else STEEL2, c, 1.8, 3)
        o += T(x, pb.Y(0) + 24, names[i], 15, INK, 'middle', 'bold')
    o += pb.hline(1.0, c=KEY, w=2.2, dash='7 5')
    o += T(pb.X(2.5), pb.Y(1.0) - 10, '保險絲', 15, KEY, 'middle', 'bold')
    o += A(pb.X(3.5) + 40, pb.Y(1.0), pb.X(3.5) + 40, pb.Y(1.32), KEY, 2, 9)
    o += T(pb.X(4) + 4, pb.Y(1.16), '留餘裕', 14, KEY, 'start', 'bold')
    o += T(685, 352, '其他站的強度 ≥ 保險絲「真的」能出的力', 15, MUT, 'middle')
    return svg(W, H, o, '一般設計與保險絲設計')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3, 'fig1_4': fig1_4}
