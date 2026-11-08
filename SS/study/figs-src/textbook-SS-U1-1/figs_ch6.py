# -*- coding: utf-8 -*-
"""第 6 章：拉力篇總整理——解題流程圖、種子→公式樹。"""
from plot import *  # noqa


def _rbox(x, y, w, h, lines, c, fill, bold_first=True, size=14.5):
    o = R(x, y, w, h, fill, c, 1.8, 9)
    n = len(lines)
    for i, s in enumerate(lines):
        o += T(x + w / 2, y + h / 2 + (i - (n - 1) / 2) * 21 + 5, s, size, c if (i == 0 and bold_first) else INK, 'middle',
               'bold' if (i == 0 and bold_first) else None)
    return o


def _dia(cx, cy, w, h, lines, c=INK):
    o = P([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)], c, 2, fill='#fff', close=True)
    for i, s in enumerate(lines):
        o += T(cx, cy + (i - (len(lines) - 1) / 2) * 20 + 5, s, 14.5, c, 'middle', 'bold')
    return o


def fig6_1():
    W, H = 900, 760
    o = ''
    o += _rbox(320, 14, 260, 46, ['⓪ 先寫：LRFD 還是 ASD？'], KEY, KEY2, size=15)
    o += A(450, 60, 450, 84, INK, 2)
    o += _dia(450, 122, 250, 76, ['接合方式？'])
    o += A(325, 122, 200, 122, INK, 2) + A(200, 122, 200, 160, INK, 2)
    o += A(575, 122, 700, 122, INK, 2) + A(700, 122, 700, 160, INK, 2)
    o += T(262, 112, '螺栓', 15, INK, 'middle', 'bold') + T(638, 112, '銲接', 15, INK, 'middle', 'bold')
    o += _rbox(40, 160, 320, 92, ['① 淨斷面 *A*_{n}（第 3 章）', '扣除寬 *d* = *d*_{b} + 0.3 cm', '錯列：每段斜線 + *s*^{2}/4*g*，取最小路徑'], AC, AC2)
    o += _rbox(540, 160, 320, 92, ['① *A*_{n} = *A*_{g}（沒有孔）', '但剪力遲滯照樣存在！', '板類縱向銲 → 看 *l*/*w*'], AC, AC2)
    o += A(200, 252, 200, 290, INK, 2) + A(700, 252, 700, 290, INK, 2)
    o += _rbox(40, 290, 820, 92, ['② 剪力遲滯 *U*（第 4 章）→ *A*_{e} = *U* *A*_{n}',
                                  '能算 x̄ → *U* = 1 − x̄/*L*（*L* 沿受力方向）；只知構材類型 → 查表 0.90／0.85／0.75',
                                  '板類兩側縱向銲 → *l* ≥ 2*w*：1.00、≥ 1.5*w*：0.87、≥ *w*：0.75，且 *l* ≥ *w*'], WARN, WARN2)
    o += A(450, 382, 450, 410, INK, 2)
    cols = [('③ GSY', ['0.90*F*_{y}*A*_{g}', 'ASD 0.6*F*_{y}*A*_{g}'], TEN, TEN2),
            ('④ NSF', ['0.75*F*_{u}*A*_{e}', 'ASD 0.5*F*_{u}*A*_{e}'], COMP, COMP2),
            ('⑤ 塊狀剪力', ['0.75 min(式①, 式②)', 'ASD 0.3*F*_{u}*A*_{nv}+0.5*F*_{u}*A*_{nt}'], COMP, COMP2),
            ('⑥ 接合本身', ['螺栓剪力、孔承壓', '銲道強度（U1-4）'], MUT, STEEL2)]
    for i, (t, ls, c, f_) in enumerate(cols):
        x = 40 + i * 207
        o += _rbox(x, 410, 196, 110, [t] + ls, c, f_, size=14)
    o += L(138, 520, 138, 546, INK, 2) + L(345, 520, 345, 546, INK, 2) + L(552, 520, 552, 546, INK, 2) + L(759, 520, 759, 546, INK, 2)
    o += L(138, 546, 759, 546, INK, 2) + A(450, 546, 450, 574, INK, 2)
    o += _rbox(260, 574, 380, 56, ['⑦ 全部取最小 → 控制模式'], KEY, KEY2, size=16)
    o += A(450, 630, 450, 656, INK, 2)
    o += _rbox(130, 656, 640, 90, ['⑧ 自我檢查', '臨界比 *A*_{e}/*A*_{g} = 1.2*F*_{y}/*F*_{u}（A36：0.738）猜 GSY 或 NSF',
                                   'GSY、NSF 的 LRFD／ASD 比值必為 1.5；塊剪由上限式控制時會小於 1.5'], TEN, '#fff')
    return svg(W, H, o, '拉力桿件解題流程')


def fig6_2():
    W, H = 900, 400
    o = ''
    seeds = [('S1', '應力 = 力 ÷ 面積', TEN, 70), ('S2', 'τ_{y} = *F*_{y}/√3 ≈ 0.6*F*_{y}', WARN, 200), ('S3', '力要走路：坡度 x̄/*L*', TEN, 330)]
    kids = [(0, '*F*_{y}*A*_{g}（長區段→怕伸長）', 40), (0, '*F*_{u}*A*_{e}（短區段→只怕斷）', 86), (0, '*A*_{n} = *A*_{g} − Σ*dt* + Σ*s*^{2}*t*/4*g*', 132),
            (1, '塊剪：0.6*F*_{u}*A*_{nv} 或 0.6*F*_{y}*A*_{gv}', 178), (0, '塊剪：＋ *U*_{bs}*F*_{u}*A*_{nt}', 224),
            (2, '*U* = 1 − x̄/*L*、*A*_{e} = *UA*_{n}', 270), (2, '*L*_{opt} = x̄/(1 − 1.2*F*_{y}/*F*_{u})', 316)]
    spos = {}
    for i, (sid, txt, c, y) in enumerate(seeds):
        o += R(20, y - 24, 330, 50, '#fff', c, 2.2, 10)
        o += R(20, y - 24, 52, 50, c, None, 0, 10) + R(52, y - 24, 20, 50, c, None)
        o += T(46, y + 6, sid, 16, '#fff', 'middle', 'bold')
        o += T(84, y + 6, txt, 15, INK, 'start', 'bold')
        spos[i] = (350, y, c)
    for si, txt, y in kids:
        x1, y1, c = spos[si]
        x2 = 470
        mx = (x1 + x2) / 2
        o += f'<path d="M{f(x1)},{f(y1)} C{f(mx)},{f(y1)} {f(mx)},{f(y)} {f(x2 - 6)},{f(y)}" fill="none" stroke="{c}" stroke-width="2" opacity=".8"/>'
        o += head(x2, y, 0, c, 9)
        o += R(x2, y - 18, 410, 36, '#fafafa', STEEL, 1.1, 7)
        o += T(x2 + 12, y + 6, txt, 14.5, INK, 'start')
    o += R(20, 360, 860, 34, KEY2, KEY, 1.2, 8)
    o += T(450, 383, '再加四個規範數字：φ = 0.90／0.75、ASD = ÷1.5、扣孔 *d*_{b}+0.3、*U* 表 0.90／0.85／0.75', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '拉力篇種子樹')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2}
