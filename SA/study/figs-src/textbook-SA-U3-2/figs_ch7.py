# -*- coding: utf-8 -*-
"""第 7 章：總整理。種子樹沿用第 0 章；種子 × 考題矩陣；解題流程圖。"""
from figs_common import *  # noqa
from figs_ch0 import SEEDS, fig0_1

# 每題用到的種子（依第 1～6 章的推導整理）
QS = [('2022-4', '剪力棟架', (0, 1, 2, 3, 4), '2'),
      ('2020-4', '牆＋構架', (0, 1, 2, 3, 4, 5), '1–3'),
      ('2018-1', '互制定性', (1, 3, 5), '3'),
      ('2021-4', '剛性樓板', (0, 1, 3, 4, 6), '4'),
      ('2019-2', '范倫迪爾', (2, 4), '5'),
      ('2023-4', '偏心斜撐', (1, 2, 3, 6), '6')]


def fig7_0():
    return fig0_1()


def fig7_1():
    W = 900
    x0, y0 = 300, 118
    cw, rh = 96, 48
    H = y0 + len(SEEDS) * rh + 70
    o = T(450, 30, '種子 × 考題：每一題都只用到其中幾顆', 16, INK, 'middle', 'bold')
    for j, (q, nm, used, ch) in enumerate(QS):
        cx = x0 + j * cw + cw / 2
        o += T(cx, y0 - 46, q, 15, INK, 'middle', 'bold')
        o += T(cx, y0 - 24, nm, 14, MUT, 'middle')
    for i, (sid, txt, c) in enumerate(SEEDS):
        y = y0 + i * rh
        o += R(14, y + 4, 276, rh - 8, '#fff', c, 1.8, 8)
        o += R(14, y + 4, 44, rh - 8, c, None, 0, 8) + R(40, y + 4, 18, rh - 8, c, None)
        o += T(36, y + 30, sid, 14, '#fff', 'middle', 'bold')
        o += T(66, y + 30, txt, 14, INK, 'start')
        o += L(x0, y + rh, x0 + cw * len(QS), y + rh, GRID, 1)
        for j, (q, nm, used, ch) in enumerate(QS):
            cx = x0 + j * cw + cw / 2
            if i in used:
                o += C(cx, y + rh / 2, 11, c, None)
    for j in range(len(QS) + 1):
        o += L(x0 + j * cw, y0, x0 + j * cw, y0 + len(SEEDS) * rh, GRID, 1)
    yb = y0 + len(SEEDS) * rh
    o += T(x0 - 10, yb + 30, '本書章', 14, MUT, 'end', 'bold')
    for j, (q, nm, used, ch) in enumerate(QS):
        o += T(x0 + j * cw + cw / 2, yb + 30, f'第 {ch} 章', 14, MUT, 'middle')
    o += T(450, yb + 58, 'S2（並聯／串聯）和 S4（剛性＝刪自由度）幾乎每題都用：它們是這個單元的地基', 14, KEY, 'middle', 'bold')
    return svg(W, int(H), o, '種子與考題對照')


def fig7_2():
    W, H = 900, 640
    o = T(450, 30, '解題流程：先翻譯題目的關鍵字，再走共同的主線', 16, INK, 'middle', 'bold')
    o += R(250, 50, 400, 44, INK, None, 0, 10)
    o += T(450, 78, '① 讀題：圈出「剛性」「反曲點」「連桿」「不需精確」', 15, '#fff', 'middle', 'bold')
    rows = [('梁 *I* = ∞、柱底固定', '每根柱＝彈簧 12*EI*/*h*^{3}；*M* = *Vh*/2', '1', AC),
            ('剛性樓板（平面內剛度 ∞）', '只剩 *u*、*v*、θ → 剛心、*K*_{θ}、柱位移', '4', KEY),
            ('剪力牆＋連桿（只傳軸力）', '[*K*] = [*K*_{f}] + [*K*_{w}]；定性：互制形狀', '3', BROWN),
            ('反曲點在中點／沒有斜桿', '中點放鉸 → 切面力偶、節點平衡', '5', TEAL),
            ('三角形剛性區域＋連梁', '三角形繞底角轉 θ → γ = (*L*/*e*)θ', '6', WARN)]
    y = 122
    for kw, act, ch, c in rows:
        o += R(40, y, 300, 56, '#fff', c, 2, 10)
        o += T(190, y + 34, kw, 15, c, 'middle', 'bold')
        o += A(344, y + 28, 400, y + 28, c, 2.4, 11)
        o += R(404, y, 380, 56, '#fafafa', c, 1.4, 10)
        o += T(594, y + 34, act, 15, INK, 'middle')
        o += R(796, y + 12, 70, 32, c, None, 0, 8)
        o += T(831, y + 34, f'第{ch}章', 14, '#fff', 'middle', 'bold')
        y += 70
    o += A(450, y - 4, 450, y + 24, INK, 2.4, 11)
    o += R(170, y + 28, 560, 56, AC2, AC, 2, 10)
    o += T(450, y + 52, '② 共同主線（第 2 章）：切一刀求層剪力 → 層勁度並聯', 15, AC, 'middle', 'bold')
    o += T(450, y + 74, '→ 層間位移串聯（或組 [*K*] 解聯立）', 15, AC, 'middle', 'bold')
    o += A(450, y + 88, 450, y + 112, INK, 2.4, 11)
    o += R(170, y + 116, 560, 50, TEN2, TEN, 2, 10)
    o += T(450, y + 147, '③ 交卷前：力平衡（Σ反力 = 外力）＋代極端值檢查', 15, TEN, 'middle', 'bold')
    return svg(W, H, o, '解題流程圖')


ALL = {'fig7_0': fig7_0, 'fig7_1': fig7_1, 'fig7_2': fig7_2}
