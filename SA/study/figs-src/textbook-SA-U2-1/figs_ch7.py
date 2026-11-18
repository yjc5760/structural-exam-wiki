# -*- coding: utf-8 -*-
"""第 7 章：只能受拉構件的判定流程、SA-2018-3 纜索鬆弛、SA-2019-1 逐步失效與 P–U 圖。"""
from sa_draw import *  # noqa
import math
import calcs

C7 = calcs.C7
TEN_C, CMP_C = AC, COMP


def _flow_box(x, y, w, h, title, sub, c, fill='#fff'):
    o = R(x, y, w, h, fill, c, 2, 10)
    o += T(x + w / 2, y + 26, title, 16, c, 'middle', 'bold')
    if sub:
        o += T(x + w / 2, y + 50, sub, 14, INK, 'middle')
    return o


def fig7_1():
    W, H = 900, 400
    o = ''
    bw, bh = 196, 68
    o += _flow_box(20, 40, bw, bh, '① 全部當作會受力', '纜索也先列成多餘力', AC)
    o += _flow_box(250, 40, bw, bh, '② 最小功求解', '∂*U*/∂*X*_{i} = 0', PUR)
    o += _flow_box(480, 40, bw, bh, '③ 每根纜索 *N* ≥ 0？', '只能拉的構件逐根檢查', LOAD)
    o += _flow_box(700, 40, 180, bh, '④ 全部 ≥ 0', '完成 ✔', FOR, '#e8f5e9')
    o += A(216, 74, 246, 74, INK, 1.8, 9) + A(446, 74, 476, 74, INK, 1.8, 9) + A(676, 74, 696, 74, FOR, 2, 9)
    o += A(578, 108, 578, 160, CMP_C, 2, 9) + T(588, 140, '有 *N* < 0', 15, CMP_C, 'start', 'bold')
    o += _flow_box(440, 164, 276, 76, '⑤ 最負的那根令 *N* = 0', '拿掉它，靜不定度 −1', CMP_C, '#ffebee')
    o += P([(440, 202), (348, 202), (348, 112)], INK, 1.8) + head(348, 110, -math.pi / 2, INK, 9)
    o += T(340, 160, '重解', 15, INK, 'end', 'bold')
    o += _flow_box(110, 280, 680, 84, '⑥ 回頭驗算：鬆掉的纜索，兩端的相對位移要「讓它變短」', '算出那根纜索兩端靠近的量 > 0，鬆弛才成立；否則換一根重來', PUR, KEY2)
    o += P([(790, 108), (790, 276)], FOR, 1.6, dash='5 4') + head(790, 278, math.pi / 2, FOR, 8)
    o += T(800, 200, '有鬆掉的', 14, FOR, 'start', 'bold') + T(800, 220, '纜索時', 14, FOR, 'start', 'bold')
    return svg(W, H, o, '只能受拉構件的判定流程')


def fig7_2():
    W, H = 900, 520
    sc = 34
    ox, oy = 120, 120
    X = lambda m: ox + m * sc
    o = ''
    # 結構
    A_, B_, C_, D_ = (X(0), oy), (X(5), oy), (X(10), oy), (X(15), oy)
    G_ = (X(10), oy + 5 * sc); E_ = (X(0), oy + 5 * sc); F_ = (X(5), oy + 5 * sc)
    o += L(*A_, *D_, INK, 4.5) + L(*C_, *G_, INK, 4.5) + fixed_wall(G_[0], G_[1], 46)
    o += L(*A_, *E_, CMP_C, 2, '6 5') + L(*B_, *F_, TEN_C, 3, '6 5')
    o += hatch_ground(E_[0] - 20, E_[1], 40) + hatch_ground(F_[0] - 20, F_[1], 40)
    for p, nm, off in ((A_, 'A', (-10, -10, 'end')), (B_, 'B', (0, -14, 'middle')), (C_, 'C', (10, -10, 'start')),
                       (D_, 'D', (10, -10, 'start')), (G_, 'G', (28, 20, 'start')), (E_, 'E', (-24, 20, 'end')), (F_, 'F', (24, 20, 'start'))):
        o += T(p[0] + off[0], p[1] + off[1], nm, 15, INK, off[2], 'bold')
    o += A(D_[0], oy - 56, D_[0], oy - 4, LOAD, 2.6, 11) + T(D_[0] - 8, oy - 34, '100 kN', 15, LOAD, 'end', 'bold')
    o += T(E_[0] - 10, (A_[1] + E_[1]) / 2, 'AE：0（鬆弛）', 15, CMP_C, 'end', 'bold')
    o += T(F_[0] + 10, (B_[1] + F_[1]) / 2, 'BF：70.75 kN（拉）', 15, TEN_C, 'start', 'bold')
    # 位移註記
    vA, vB = float(C7['18_vA']), float(C7['18_vB'])
    o += A(A_[0] + 18, oy - 46, A_[0] + 18, oy - 14, CMP_C, 2, 9) + T(A_[0] + 26, oy - 40, f'A 下移 {vA:.3f} m', 14, CMP_C, 'start', 'bold')
    o += A(B_[0] + 18, oy - 14, B_[0] + 18, oy - 46, TEN_C, 2, 9) + T(B_[0] + 26, oy - 40, f'B 上移 {vB:.3f} m', 14, TEN_C, 'start', 'bold')
    # 右側說明
    bx = 690
    x1, x2 = C7['18_both']
    o += R(bx, 40, 200, 250, KEY2, PUR, 1.4, 10)
    yy = 68
    for s, c, wgt, sz in [('兩索都當多餘力', PUR, 'bold', 15), (f'*X*_{{AE}} = {float(x1):.3f}'.replace('-', '−'), CMP_C, 'bold', 15), ('（壓！不可能）', CMP_C, None, 14),
                          (f'*X*_{{BF}} = {float(x2):.2f}', INK, None, 15), ('', INK, None, 4),
                          ('令 AE = 0 重解', PUR, 'bold', 15), ('*X*_{BF} = 3750/53', TEN_C, 'bold', 15), ('= 70.75 kN', TEN_C, 'bold', 15), ('', INK, None, 4),
                          ('驗算：A 往下 ⇒ AE', INK, None, 14), ('變短 ⇒ 鬆弛成立 ✔', FOR, 'bold', 14)]:
        if s:
            o += T(bx + 100, yy, s, sz, c, 'middle', wgt)
        yy += sz + 8 if s else 4
    # 彎矩圖（梁 A~D）
    pl = Plot(ox, 330, 15 * sc, 150, 0, 15, -520, 40)
    X2 = float(C7['18_X2'])
    Mf = lambda s: 0.0 if s <= 5 else (-X2 * (s - 5) if s <= 10 else -100 * (15 - s))
    pts = [pl.pt(s, Mf(s)) for s in [i * 15 / 600 for i in range(601)]]
    o += P(pts + [pl.pt(15, 0), pl.pt(0, 0)], None, fill='#ef9a9a', close=True, op=0.4)
    o += L(pl.X(0), pl.Y(0), pl.X(15), pl.Y(0), INK, 1.4) + P(pts, MOM, 2.4)
    o += L(pl.X(10), pl.Y(-X2 * 5), pl.X(10), pl.Y(-500), MOM, 2.4)
    o += T(ox - 14, pl.Y(0) + 5, '*M*', 17, MOM, 'end', 'bold')
    o += T(pl.X(10) + 10, pl.Y(-X2 * 5) + 5, f'−{X2*5:.2f}', 15, MOM, 'start', 'bold')
    o += T(pl.X(10) + 8, pl.Y(-500) + 16, '−500', 15, MOM, 'start', 'bold')
    o += T(pl.X(2.5), pl.Y(0) - 10, 'AB：0', 15, MOM, 'middle', 'bold')
    o += T(pl.X(15) + 10, pl.Y(-250), 'C 點跳 146.23', 15, INK, 'start')
    o += T(pl.X(15) + 10, pl.Y(-250) + 20, '＝傳給柱 CG', 15, INK, 'start')
    return svg(W, H, o, 'SA-2018-3 纜索鬆弛')


def fig7_3():
    W, H = 900, 420
    sc = 26
    ox, oy = 150, 330
    pt = lambda X, Y: (ox + X * sc, oy - Y * sc)
    N = {'C': pt(0, 0), 'A': pt(12, 0), 'D': pt(0, 9), 'B': pt(12, 9)}
    F1 = {k: float(v) for k, v in C7['19_stage1'].items()}
    mem = {'DA': ('D', 'A'), 'BC': ('B', 'C'), 'DB': ('D', 'B'), 'AC': ('A', 'C'), 'DC': ('D', 'C'), 'AB': ('A', 'B')}
    cap = {'DA': '壓強 144', 'BC': '壓強 144', 'DB': '壓強 225', 'AC': '壓強 225', 'DC': '壓強 400', 'AB': '壓強 400'}
    o = T(ox + 6 * sc, 30, '第一階段（彈性、一度靜不定），*P* = 327.41 kN 時', 16, INK, 'middle', 'bold')
    for nm, (p, q) in mem.items():
        v = F1[nm]
        c = TEN_C if v > 0 else CMP_C
        (x1, y1), (x2, y2) = N[p], N[q]
        w = 2 + abs(v) / 30
        if nm in ('DA', 'BC'):
            # 兩斜桿交叉不相連：BC 在交叉處留白
            o += L(x1, y1, x2, y2, c, w, op=0.85)
        else:
            o += L(x1, y1, x2, y2, c, w, op=0.85)
        lab = f'{v:+.1f}'.replace('-', '−')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        off = {'DA': (-78 + 12, -39 - 12), 'BC': (78 - 12, -39 - 12), 'DB': (0, -12), 'AC': (0, 26), 'DC': (-12, 5), 'AB': (12, 5)}[nm]
        anc = {'DA': 'start', 'BC': 'end', 'DB': 'middle', 'AC': 'middle', 'DC': 'end', 'AB': 'start'}[nm]
        if nm == 'DA':
            o += T(*pt(10.6, 0.55), f'{nm} {lab}', 15, c, 'end', 'bold')
        elif nm == 'BC':
            o += T(*pt(1.4, 0.55), f'{nm} {lab}', 15, c, 'start', 'bold')
        else:
            o += T(mx + off[0], my + off[1], f'{nm} {lab}', 15, c, anc, 'bold')
    o += C((N['D'][0] + N['A'][0]) / 2, (N['D'][1] + N['A'][1]) / 2, 7, '#fff', None) + \
        L(*N['D'], *N['A'], CMP_C, 2 + 144 / 30, op=0.85)
    for k, (x, y) in N.items():
        o += C(x, y, 6, '#fff', INK, 1.8)
    o += pin(*N['C']) + roller(*N['A'])
    bx_, by_ = N['B']
    o += A(bx_ + 6, by_, bx_ + 66, by_, LOAD, 2.6, 11) + T(bx_ + 72, by_ + 5, '*P*', 16, LOAD, 'start', 'bold')
    for k, (x, y) in N.items():
        off = {'C': (-14, 6, 'end'), 'A': (14, 6, 'start'), 'D': (-12, -10, 'end'), 'B': (-2, -14, 'end')}[k]
        o += T(x + off[0], y + off[1], k, 16, INK, off[2], 'bold')
    bx = 600
    o += R(bx, 52, 288, 300, KEY2, PUR, 1.4, 10)
    yy = 80
    lim = C7['19_lim1']
    for s, c, wgt, sz in [('各桿「到強度」時的 *P*', PUR, 'bold', 15), ('', INK, None, 2),
                          (f'DA（壓，144）：{float(lim["DA"]):.2f} ← 最小', CMP_C, 'bold', 15),
                          (f'AB（壓，400）：{float(lim["AB"]):.2f}', INK, None, 15),
                          (f'BC（拉，1250）：{float(lim["BC"]):.2f}', INK, None, 15), ('', INK, None, 6),
                          ('DA 先壓挫 ⇒ 內力歸零', PUR, 'bold', 15), ('剩下靜定：BC = 1.25*P*、AB = −0.75*P*', INK, None, 14),
                          ('AB 到 400：*P* = 533.33', PUR, 'bold', 15), ('第二根退出 ⇒ 機構', MOM, 'bold', 15),
                          ('（*n* + 1 = 2 根）', MUT, None, 14)]:
        if s:
            o += T(bx + 144, yy, s, sz, c, 'middle', wgt)
        yy += sz + 9 if s else 4
    o += T(450, 400, '藍：拉；紅：壓；線寬 ∝ |力|。兩根斜桿交叉但不相連（一度靜不定）', 15, MUT, 'middle')
    return svg(W, H, o, 'SA-2019-1 第一階段桿力')


def fig7_4():
    W, H = 900, 430
    P1, P2 = float(C7['19_P1']), float(C7['19_P2'])
    U1, U1b, U2 = float(C7['19_U1']), float(C7['19_U1b']), float(C7['19_U2'])
    pl = Plot(110, 50, 560, 290, 0, 17000, 0, 600)
    o = pl.axes([0, U1, U1b, U2], [0, P1, P2], '*U*_{B}·*EA*', '*P*（kN）', size=14,
                xfmt=lambda t: f'{t:.0f}' if t != U1b else f'{t:.1f}', yfmt=lambda t: f'{t:.2f}' if t else '0')
    o += P([pl.pt(0, 0), pl.pt(U1, P1)], AC, 3)
    o += P([pl.pt(U1, P1), pl.pt(U1b, P1)], MOM, 3, dash='7 5')
    o += P([pl.pt(U1b, P1), pl.pt(U2, P2)], AC, 3)
    o += P([pl.pt(U2, P2), pl.pt(U2, 0)], MOM, 2.4, dash='7 5')
    for (u, p, c) in ((U1, P1, PUR), (U1b, P1, PUR), (U2, P2, MOM)):
        o += pl.dot(u, p, c)
    o += T(pl.X(U1 / 2) - 8, pl.Y(P1 / 2) - 10, '斜率 *EA*/18.47', 15, AC, 'end', 'bold')
    o += T(pl.X(U1 / 2) - 8, pl.Y(P1 / 2) + 12, '（一度靜不定，較硬）', 14, MUT, 'end')
    o += T(pl.X((U1 + U1b) / 2), pl.Y(P1) + 24, 'DA 壓挫：力重分配', 14, MOM, 'middle', 'bold')
    o += T(pl.X((U1 + U1b) / 2), pl.Y(P1) + 44, '位移跳一段', 14, MOM, 'middle')
    o += T(pl.X(12600), pl.Y(480), '斜率 *EA*/28.5（靜定，較軟）', 15, AC, 'end', 'bold')
    o += T(pl.X(U2) + 8, pl.Y(P2) - 10, '*P*_{u} = 533.33：AB 壓挫 ⇒ 機構', 15, MOM, 'start', 'bold')
    o += R(110, 376, 680, 44, KEY2, PUR, 1.4, 8)
    o += T(450, 404, '三個轉折點都是算出來的：(6048, 327.41)、(9331.2, 327.41)、(15200, 533.33)', 15, PUR, 'middle', 'bold')
    return svg(W, H, o, 'SA-2019-1 P–U 圖')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2, 'fig7_3': fig7_3, 'fig7_4': fig7_4}
