# -*- coding: utf-8 -*-
"""第 14 章（下冊總整理）：整梁三線檢核流程、下冊種子樹。"""
from plot import *  # noqa
import calcs
from figs_ch7 import diamond, rbox

PUR = '#7b1fa2'


def fig14_1():
    W, H = 900, 520
    o = ''
    cx = 450
    o += rbox(cx, 40, 420, 50, '載重組合：*w*_{u} = 1.2*D* + 1.6*L* → *M*_{u}、*V*_{u}', INK, '#fafafa')
    for k, (x, title, lines, c, fl) in enumerate((
            (150, '① 強度', ['上冊流程圖（第 7 章）', '*M*_{u} ≤ φ_{b}*M*_{n}', '弱軸／雙軸：第 11 章', '合成梁：第 12 章'], COMP, COMP2),
            (450, '② 剪力', ['*V*_{u} ≤ φ_{v}*V*_{n}', '*h*/*t*_{w} 判三段（第 8 章）', '接合：*q* = *VQ*/*I*（第 9 章）', ''], WARN, WARN2),
            (750, '③ 撓度', ['工作載重、只用活載', 'δ_{L} ≤ *L*/360', '5/384、1/48、23/648', '（第 10 章）'], AC, AC2))):
        o += P([(cx, 65), (cx, 90), (x, 90), (x, 118)], INK, 2) + head(x, 122, 1.5708, INK, 10)
        o += R(x - 135, 126, 270, 190, fl, c, 2, 12)
        o += T(x, 156, title, 17, c, 'middle', 'bold')
        for j, s in enumerate(lines):
            o += T(x, 190 + j * 28, s, 14, INK, 'middle')
        o += P([(x, 316), (x, 346), (cx, 346), (cx, 360)], INK, 2)
    o += head(cx, 364, 1.5708, INK, 10)
    o += diamond(cx, 410, 340, 84, '三條都 ≤ 1.0？')
    o += A(cx + 170, 410, 700, 410, INK, 2, 10) + T(cx + 196, 400, '否', 15, COMP, 'middle', 'bold')
    o += rbox(790, 410, 170, 56, '換斷面、加自重重算', COMP, COMP2, size=14)
    o += A(cx, 452, cx, 478, INK, 2, 10) + T(cx + 14, 470, '是', 15, TEN, 'start', 'bold')
    o += rbox(cx, 500, 260, 36, '完成：寫出三行使用率', PUR, KEY2)
    return svg(W, H + 10, o, '整梁三線檢核')


def fig14_2():
    W, H = 900, 300
    seeds = [('S6', '0.6*F*_{y}', WARN, ['*V*_{n} = 0.6*F*_{y}*A*_{w}', '銲道 0.6*F*_{EXX}']),
             ('S2', '板會推歪', COMP, ['τ_{cr} ≈ 1860*k*_{v}/λ^{2}', '50、62、*k*_{v}']),
             ('S7', '切一刀平衡', WARN, ['*q* = *VQ*/*I*', '*q*·*s* ≤ 接合強度']),
             ('S8', '曲率積分', AC, ['5/384、1/48、23/648', '*L*/360']),
             ('S1', '應力塊', TEN, ['1.5*F*_{y}*S*_{y}、合成梁', '虛功 11.66'])]
    o = ''
    bw = 166
    for i, (sid, t, c, kids) in enumerate(seeds):
        x = 14 + i * (bw + 10)
        o += R(x, 30, bw, 52, '#fff', c, 2.4, 12)
        o += R(x, 30, bw, 30, c, None, 0, 12) + R(x, 48, bw, 12, c, None)
        o += T(x + bw / 2, 52, f'{sid}　{t}', 15, '#fff', 'middle', 'bold')
        o += A(x + bw / 2, 86, x + bw / 2, 116, c, 2, 9)
        o += R(x, 120, bw, 90, '#fafafa', STEEL, 1.2, 8)
        for j, k in enumerate(kids):
            o += T(x + bw / 2, 152 + j * 30, k, 14, INK, 'middle')
    o += T(W / 2, 252, '數字小卡（下冊）：φ_{v} = 0.90、*k*_{v} = 5 + 5/(*a*/*h*)^{2}、*L*/360、0.85*f*′_{c}、8／11.66／16', 15, KEY, 'middle', 'bold')
    o += T(W / 2, 282, '下冊新增 3 顆種子（S6、S7、S8），其餘沿用上冊', 15, INK, 'middle')
    return svg(W, H, o, '下冊種子樹')


ALL = {'fig14_1': fig14_1, 'fig14_2': fig14_2}
