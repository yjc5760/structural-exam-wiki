# -*- coding: utf-8 -*-
"""第 7 章（上冊總整理）：解題流程圖、上冊種子樹。"""
from plot import *  # noqa
import calcs

PUR = '#7b1fa2'


def diamond(cx, cy, w, h, txt, c=WARN, size=15):
    o = P([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)], c, 2, WARN2, close=True)
    o += T(cx, cy + 5, txt, size, INK, 'middle', 'bold')
    return o


def rbox(cx, cy, w, h, txt, c=AC, fill=AC2, size=15, sub=None):
    o = R(cx - w / 2, cy - h / 2, w, h, fill, c, 2, 10)
    if sub:
        o += T(cx, cy - 3, txt, size, INK, 'middle', 'bold') + T(cx, cy + 18, sub, 14, MUT, 'middle')
    else:
        o += T(cx, cy + 5, txt, size, INK, 'middle', 'bold')
    return o


def fig7_1():
    W, H = 900, 760
    o = ''
    cx = 330
    o += rbox(cx, 40, 360, 48, '① 本錢：*M*_{p} = *F*_{y}*Z*_{x}、*M*_{r} = (*F*_{y}−*F*_{r})*S*_{x}', TEN, TEN2, sub=None)
    o += A(cx, 64, cx, 96, INK, 2, 10)
    o += diamond(cx, 140, 300, 84, '② 翼板／腹板 λ ≤ λ_{p}？')
    o += A(cx + 150, 140, 600, 140, INK, 2, 10) + T(cx + 175, 130, '否', 15, COMP, 'middle', 'bold')
    o += rbox(720, 140, 240, 64, 'FLB 內插（第 2 章）', COMP, COMP2, sub='λ_{p}～λ_{r} 拉直線')
    o += A(cx, 182, cx, 220, INK, 2, 10) + T(cx + 16, 206, '是', 15, TEN, 'start', 'bold')
    o += diamond(cx, 266, 300, 84, '③ 弱軸彎曲？')
    o += A(cx + 150, 266, 600, 266, INK, 2, 10) + T(cx + 175, 256, '是', 15, TEN, 'middle', 'bold')
    o += rbox(720, 266, 240, 64, '無 LTB（第 11 章）', TEN, TEN2, sub='min(*F*_{y}*Z*_{y}, 1.5*F*_{y}*S*_{y})')
    o += A(cx, 308, cx, 346, INK, 2, 10) + T(cx + 16, 332, '否', 15, COMP, 'start', 'bold')
    o += diamond(cx, 392, 300, 84, '④ *L*_{b} 落在哪一段？')
    # 三個出口
    xs = [110, 330, 550]
    labs = [('*L*_{b} ≤ *L*_{p}', '*M*_{n} = *M*_{p}', TEN, TEN2), ('*L*_{p} < *L*_{b} ≤ *L*_{r}', '*C*_{b}×直線', WARN, WARN2),
            ('*L*_{b} > *L*_{r}', '*C*_{b}×*M*_{cr}', COMP, COMP2)]
    for x, (cond, res, c, fl) in zip(xs, labs):
        o += P([(cx, 434), (cx, 456), (x, 456), (x, 486)], INK, 2)
        o += head(x, 490, 1.5708, INK, 10)
        o += T(x, 476, cond, 14, c, 'middle', 'bold') if x != cx else T(x + 12, 476, cond, 14, c, 'start', 'bold')
        o += rbox(x, 524, 190, 60, res, c, fl)
    for x in xs:
        o += P([(x, 554), (x, 584), (cx, 584), (cx, 600)], INK, 2)
    o += head(cx, 604, 1.5708, INK, 10)
    o += rbox(cx, 636, 360, 56, '⑤ 取小：min(FLB, LTB) ≤ *M*_{p}', KEY, KEY2)
    o += A(cx, 664, cx, 692, INK, 2, 10)
    o += rbox(cx, 722, 360, 52, '⑥ φ_{b}*M*_{n} = 0.9*M*_{n}　（ASD：第 6 章）', PUR, KEY2)
    o += box(555, 586, 335, 168, '每一格對一章', ['① 第 1 章（S1）', '② 第 2 章（S2、S4）', '③ 第 3、11 章（S3）', '④ 第 4 章（S3、S4）', '　*C*_{b}：第 5 章（S5）', '⑤⑥ 第 4 章'], KEY2, KEY, 16, 14)
    return svg(W, H, o, '梁撓曲強度流程圖')


def fig7_2():
    W, H = 900, 330
    seeds = [('S1', '應力塊', TEN, ['*M*_{y}、*M*_{p}、*f*', 'PNA、*Z* 半面積']),
             ('S2', '板會推歪', COMP, ['λ ∝ √(*E*/*F*_{y})', '17／25／170／260']),
             ('S3', '翼板＝側向柱', COMP, ['*M*_{cr} 兩條路', '*X*_{1}、*X*_{2}、弱軸無 LTB']),
             ('S4', '平台＋直線＋曲線', KEY, ['FLB、LTB 三段', '*L*_{r}、ASD 分界']),
             ('S5', '梯度是紅利', AC, ['*C*_{b} 最大÷平均', '均勻彎矩 = 1'])]
    o = ''
    bw = 166
    for i, (sid, t, c, kids) in enumerate(seeds):
        x = 14 + i * (bw + 10)
        o += R(x, 30, bw, 70, '#fff', c, 2.4, 12)
        o += R(x, 30, bw, 30, c, None, 0, 12) + R(x, 48, bw, 12, c, None)
        o += T(x + bw / 2, 52, f'{sid}　{t}', 15, '#fff', 'middle', 'bold')
        o += T(x + bw / 2, 86, '（要記的）', 14, MUT, 'middle')
        o += A(x + bw / 2, 104, x + bw / 2, 136, c, 2, 9)
        o += R(x, 140, bw, 90, '#fafafa', STEEL, 1.2, 8)
        for j, k in enumerate(kids):
            o += T(x + bw / 2, 172 + j * 30, k, 14, INK, 'middle')
    o += T(W / 2, 272, '數字小卡：φ_{b} = 0.90、ASD ≈ LRFD÷1.5（只限塑性區）、0.66／0.6*F*_{y}、*F*_{r} = 0.7／1.16、80（*L*_{p}）、12000、840', 15, KEY, 'middle', 'bold')
    o += T(W / 2, 302, '上冊 5 顆種子 + 一張小卡 = 全部要記的東西', 15, INK, 'middle')
    return svg(W, H, o, '上冊種子樹')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}
