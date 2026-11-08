# -*- coding: utf-8 -*-
"""第 8 章：總整理。"""
from plot import *  # noqa
from calcs import *  # noqa
import figs_ch0
from figs_ch0 import SEEDC, SEEDL


def fig8_1():
    W, H = 900, 560
    o = T(450, 26, '說明題的解題流程：從「部位」找到「種子」，再長出規定', 16, INK, 'middle', 'bold')
    def box(x, y, w, h, t1, t2, c, fill='#fff'):
        s = R(x, y, w, h, fill, c, 2, 10) + T(x + w / 2, y + 26, t1, 15.5, c, 'middle', 'bold')
        if t2:
            s += T(x + w / 2, y + 50, t2, 14, INK, 'middle')
        return s
    o += box(250, 46, 400, 64, '① 圈出題目問的「部位／工法／材料」', '例：梁翼 CJP、摩阻螺栓、工地塗裝', AC, AC2)
    o += A(450, 112, 450, 138, MUT, 2, 9)
    # 菱形
    cx, cy = 450, 178
    o += P([(cx, cy - 38), (cx + 190, cy), (cx, cy + 38), (cx - 190, cy)], KEY, 2, fill=KEY2, close=True)
    o += T(cx, cy - 4, '② 這裡會出什麼事？', 15.5, KEY, 'middle', 'bold') + T(cx, cy + 18, '（破壞來自哪個機制）', 14, INK, 'middle')
    seeds = [('S1', '熱', '淬硬／粗晶'), ('S2', '氫', '冷裂'), ('S3', '幾何', '最弱那一刀'), ('S4', '看不見', '要檢測'),
             ('S5', '滑動', '夾緊力'), ('S6', '腐蝕', '電池'), ('S7', '脆斷', '弱環不對')]
    bw, gap = 112, 10
    x = (W - (7 * bw + 6 * gap)) / 2
    for sid, a, b in seeds:
        c = SEEDC[sid]
        o += L(cx, cy + 38, x + bw / 2, 250, c, 1.4)
        o += R(x, 250, bw, 78, SEEDL[sid], c, 1.8, 8)
        o += T(x + bw / 2, 272, sid, 15, c, 'middle', 'bold') + T(x + bw / 2, 294, a, 15, c, 'middle', 'bold') + T(x + bw / 2, 316, b, 14, INK, 'middle')
        o += L(x + bw / 2, 328, 450, 360, c, 1.4)
        x += bw + gap
    o += box(200, 360, 500, 56, '③ 寫規定（含數字）＋④ 反過來會怎樣', '數字卡＋「不遵守 → 什麼瑕疵／破壞」', COMP)
    o += A(450, 418, 450, 438, MUT, 2, 9)
    o += box(200, 440, 500, 56, '⑤ 對策＋檢測方法', '預防（事前）→ 管制（事中）→ NDT（事後）', TEN)
    o += A(450, 498, 450, 512, MUT, 2, 9)
    o += box(200, 514, 500, 40, '⑥ 加分：國外規範差異、方向相反的另一條規定', '', KEY)
    return svg(W, H, o, '說明題流程')


def fig8_2():
    return figs_ch0.fig0_1()


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2}
