# -*- coding: utf-8 -*-
"""第 8 章：總整理。種子樹沿用第 0 章的圖；解題流程圖。"""
from figs_common import *  # noqa
import figs_ch0


def fig8_1():
    return figs_ch0.fig0_1()


def _box(x, y, w, h, lines, c=AC, fill=AC2, bold_first=True, size=15):
    o = R(x, y, w, h, fill, c, 1.8, 10)
    n = len(lines)
    for k, s in enumerate(lines):
        yy = y + h / 2 + (k - (n - 1) / 2) * (size + 8) + 5
        o += T(x + w / 2, yy, s, size, c if (k == 0 and bold_first) else INK, 'middle', 'bold' if (k == 0 and bold_first) else None)
    return o


def _arr(x1, y1, x2, y2, c=INK, label='', lx=0, ly=0, anchor='middle'):
    o = A(x1, y1, x2, y2, c, 2, 10)
    if label:
        o += T((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, 15, c, anchor, 'bold')
    return o


def fig8_2():
    """解題流程：問力還是問位移 → 拆掉束制後是不是機構 → 求最大效應。"""
    W, H = 900, 820
    o = ''
    o += _box(250, 14, 400, 60, ['① 讀圖', '支承種類、內鉸、所求斷面、載重走哪一弦'], INK, '#eceff1')
    o += _arr(450, 74, 450, 104)
    o += _box(270, 104, 360, 56, ['② 問的是「力」還是「位移」？'], KEY, KEY2)
    # 位移分支
    o += _arr(630, 132, 700, 132, KEY, '位移', 0, -8)
    o += _box(700, 104, 186, 112, ['位移影響線', '在該點施 1', '撓度曲線就是答案', '不除・m/kN（第 6 章）'], WARN, WARN2, size=14)
    # 力分支
    o += _arr(450, 160, 450, 196, KEY, '力', 16, 4, 'start')
    o += _box(220, 196, 460, 56, ['③ 拆掉所求量的束制後，是不是「機構」？'], KEY, KEY2)
    o += _arr(330, 252, 200, 300, AC, '是（靜定）', -40, -4, 'end')
    o += _arr(570, 252, 700, 300, COMP, '否（靜不定）', 40, -4, 'start')
    # 靜定
    o += _box(20, 300, 360, 150, ['靜定 → 折線', '梁：Müller-Breslau，逐段問「繞哪點轉」', 'Gerber 梁先分主從（第 2 章）', '桁架：*N* = ±*M*_{矩心}/力臂、±*V*/sinθ', '節點值連直線（第 3 章）'], AC, AC2, size=14)
    # 靜不定
    o += _box(520, 300, 360, 150, ['靜不定 → 曲線', '拆、推 1：*v*(*x*)（積分／單位力／共軛梁）', 'IL = *v*(*x*) / *f*_{*ii*}　← 一定要除', '等跨連續梁：三彎矩 *M*_{*B*}(*u*)', '其他量再用平衡（第 5、7 章）'], COMP, COMP2, size=14)
    o += _arr(200, 450, 380, 500, INK)
    o += _arr(700, 450, 520, 500, INK)
    o += _box(220, 500, 460, 96, ['④ 自我檢查', '反力相加 = 1・剪力跳 1・束制點縱距 = 1', '挑一個載重位置用平衡驗正負號'], TEN, TEN2, size=14)
    o += _arr(450, 596, 450, 630)
    o += _box(120, 630, 660, 170, ['⑤ 要最大效應嗎？（第 4 章）', '集中力：放在 |η| 最大處', '均布：*w* × 同號面積（負區不相連就分開鋪）', '輪壓列：輪流讓每一輪壓在峰頂，或 *W*_{*L*}/*a* ≤ *W*/*L* ≤ (*W*_{*L*}+*P*)/*a*', '同一根桿：拉、壓兩個極值都要找'], KEY, KEY2, size=14)
    return svg(W, H, o, '解題流程')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2}
