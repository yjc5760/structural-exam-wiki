# -*- coding: utf-8 -*-
"""第 0 章的向量圖：種子家族樹、六步流程、貫穿範例接頭。座標全部由程式算出。"""
from plot import *  # noqa
from calcs import *  # noqa
import math

# 種子顏色＝單元總覽考點群的顏色（銲接紅、檢測藍、螺栓橘、防蝕綠、耐震紫）
SEEDC = {'S1': COMP, 'S2': COMP, 'S3': AC, 'S4': AC, 'S5': WARN, 'S6': TEN, 'S7': KEY}
SEEDL = {'S1': COMP2, 'S2': COMP2, 'S3': AC2, 'S4': AC2, 'S5': WARN2, 'S6': TEN2, 'S7': KEY2}


def tw(s, size):
    """估文字寬度：中文≈字級，ASCII≈0.56 字級。"""
    return sum(size if ord(ch) > 255 else 0.56 * size for ch in s)


SEEDS = [
    ('S1', '熱循環', '局部熔化＋急冷',
     ['HAZ 韌性最差', '最小銲腳依厚板', '預熱隨板厚↑', '入熱／層間溫度上限', '碳當量', 'ESW 晶粒粗化']),
    ('S2', '氫三要素', '氫＋硬脆＋拉應力',
     ['銲條烘烤', '溼度／風速門檻', '預熱（＋S1）', '延遲裂縫', '低氫系降一級預熱']),
    ('S3', '力流', '力走最短的那一刀',
     ['銲喉 0.707*w*', '最大銲腳 *t*−2', '最小長 4*w*', '回銲 2*w*～4*w*', '間距 3*d*／邊距 1.5*d*', '層狀撕裂（板厚向）']),
    ('S4', '瑕疵形狀', '形狀決定用哪種波',
     ['NDT 五法配對', 'MT 只限磁性', 'CJP 用 UT 不用 RT', '開槽型式']),
    ('S5', '摩擦', '*R* = μ × 夾緊力',
     ['預拉力 0.70*F*_{u}', '間隙 1 mm 加墊片', '孔位：沖梢→鉸孔', '不可重用', '摩擦面不塗（＋S6）', '摩阻可併銲']),
    ('S6', '腐蝕電池', '拆掉一個零件就停',
     ['銹蝕 A～D、Sa 2½', '熱浸鍍鋅（犧牲陽極）', '金屬噴塗', '塗裝四禁止', '不予塗裝五部位']),
    ('S7', '弱環', '讓你指定的那環先降伏',
     ['SN-C／Z 向', 'Charpy 27 J', '降伏比 0.80', '節點域 *t*_{z}', '背銲條移除', 'UT 100%', '0.03 rad']),
]


def fig0_1():
    W = 900
    row_h, top = 74, 46
    H = top + row_h * len(SEEDS) + 14
    o = T(110, 28, '要記的 7 顆種子', 16, INK, 'middle', 'bold')
    o += T(560, 28, '從種子長出來的規定（考場上自己寫得出方向與理由）', 16, INK, 'middle', 'bold')
    x0 = 238; xmax = W - 10
    for i, (sid, name, line, rules) in enumerate(SEEDS):
        y = top + i * row_h
        c, c2 = SEEDC[sid], SEEDL[sid]
        o += R(8, y + 4, 205, row_h - 12, c2, c, 1.8, 10)
        o += R(16, y + 14, 38, 26, c, None, 0, 6) + T(35, y + 33, sid, 15, '#fff', 'middle', 'bold')
        o += T(62, y + 33, name, 16, c, 'start', 'bold')
        o += T(110, y + 56, line, 14, INK, 'middle')
        # chips：自動換行，最多兩行
        cx, cy = x0, y + 10
        for r in rules:
            plain = r.replace('*', '').replace('_{', '').replace('}', '')
            w = tw(plain, 14) + 16
            if cx + w > xmax:
                cx, cy = x0, cy + 30
            o += R(cx, cy, w, 24, '#fff', c, 1.3, 12)
            o += T(cx + w / 2, cy + 17, r, 14, INK, 'middle')
            cx += w + 8
        o += L(213, y + row_h / 2 - 4, x0 - 6, y + row_h / 2 - 4, c, 2.2)
        o += C(x0 - 6, y + row_h / 2 - 4, 3.5, c, c, 1)
    return svg(W, H, o, '種子家族樹')


STEPS = [('①', '看圖', '先畫出機制'), ('②', '白話', '這條在防什麼'), ('③', '推方向', '推上限或下限'),
         ('④', '反例檢查', '拿掉它會怎樣'), ('⑤', '標籤', '必背／別賭'), ('⑥', '答題骨架', '寫哪幾格有分')]


def fig0_2():
    W, H = 900, 300
    o = ''
    n = len(STEPS); bw, gap = 128, 18
    x = (W - (n * bw + (n - 1) * gap)) / 2
    for i, (num, a, b) in enumerate(STEPS):
        c = KEY if i == 5 else AC
        o += R(x, 26, bw, 96, KEY2 if i == 5 else AC2, c, 1.6, 10)
        o += T(x + bw / 2, 52, num, 17, c, 'middle', 'bold')
        o += T(x + bw / 2, 78, a, 16, c, 'middle', 'bold')
        o += T(x + bw / 2, 104, b, 14, INK, 'middle') if tw(b, 14) < bw - 8 else (
            T(x + bw / 2, 100, b[:len(b) // 2 + 1], 14, INK, 'middle') + T(x + bw / 2, 117, b[len(b) // 2 + 1:], 14, INK, 'middle'))
        if i < n - 1:
            o += A(x + bw + 2, 74, x + bw + gap - 2, 74, MUT, 2, 8)
        x += bw + gap
    # 下排：數字的三種身分
    o += T(W / 2, 160, '第 ③ 步推到哪裡為止？每個數字屬於下面三種之一，講義會標明', 15, INK, 'middle', 'bold')
    cats = [(TEN, '可以推出數值', '例：銲喉 0.707*w*、中心距 3*d*'),
            (WARN, '推得出方向，數值要背', '例：最小銲腳由厚板定、預熱隨板厚↑'),
            (COMP, '純規範數字（進數字卡）', '例：0.70*F*_{u}、100 mm、分母 90')]
    bw2 = 272; x = (W - 3 * bw2 - 2 * 14) / 2
    for c, a, b in cats:
        o += R(x, 178, bw2, 92, '#fff', c, 2, 10)
        o += T(x + bw2 / 2, 208, a, 16, c, 'middle', 'bold')
        o += T(x + bw2 / 2, 240, b, 14, INK, 'middle')
        x += bw2 + 14
    return svg(W, H, o, '六步流程與數字的三種身分')


def fig0_3():
    """貫穿範例接頭的立面示意（比例依 EX 尺寸，約 0.33 px/mm）。"""
    W, H = 900, 560
    s = 0.33
    o = ''
    cx0 = 150                      # 柱左外緣
    bcol = 550 * s; tw_ = EX['col_t'] * s
    cx1 = cx0 + bcol
    ytop, ybot = 40, 520
    d = 600 * s; tf = EX['bf_t'] * s
    yf1 = 190; yf2 = yf1 + d       # 梁上緣、下緣
    # 柱（剖面：兩片柱壁）
    o += R(cx0, ytop, tw_, ybot - ytop, STEEL3, INK, 1.2)
    o += R(cx1 - tw_, ytop, tw_, ybot - ytop, STEEL3, INK, 1.2)
    o += L(cx0 + tw_, ytop, cx1 - tw_, ytop, MUT, 1, '4 4') + L(cx0 + tw_, ybot, cx1 - tw_, ybot, MUT, 1, '4 4')
    # 內橫隔板（對齊梁翼）＋ ESW 銲道（隔板兩端）
    for yy in (yf1, yf2 - tf):
        o += R(cx0 + tw_, yy - 1, bcol - 2 * tw_, tf + 2, STEEL, INK, 1)
        o += R(cx0 + tw_ - 3, yy - 3, 7, tf + 6, COMP, None, 0) + R(cx1 - tw_ - 4, yy - 3, 7, tf + 6, COMP, None, 0)
    # 梁
    bx1 = 600
    o += R(cx1, yf1, bx1 - cx1, tf, STEEL, INK, 1.2)
    o += R(cx1, yf2 - tf, bx1 - cx1, tf, STEEL, INK, 1.2)
    o += R(cx1 + 14, yf1 + tf, bx1 - cx1 - 14, d - 2 * tf, STEEL2, INK, 1)
    o += L(bx1, yf1, bx1 + 18, yf1, MUT, 1, '4 3') + L(bx1, yf2, bx1 + 18, yf2, MUT, 1, '4 3')
    # 梁翼 CJP（開槽三角）＋背銲條
    for yy, down in ((yf1, True), (yf2 - tf, False)):
        o += P([(cx1, yy), (cx1 + 10, yy), (cx1, yy + tf)] if down else [(cx1, yy + tf), (cx1 + 10, yy + tf), (cx1, yy)],
               None, fill=COMP, close=True)
        by = yy + tf if down else yy - 5
        o += R(cx1, by, 16, 5, KEY, None, 0)
    # 剪力板＋螺栓
    tx0, tx1 = cx1, cx1 + 110
    ty0, ty1 = yf1 + tf + 22, yf2 - tf - 22
    o += R(tx0, ty0, tx1 - tx0, ty1 - ty0, '#ffffff', WARN, 1.6, 2)
    o += L(tx0 + 2, ty0, tx0 + 2, ty1, COMP, 3)   # 填角銲
    nb = 4
    for k in range(nb):
        yb = ty0 + 22 + k * (ty1 - ty0 - 44) / (nb - 1)
        o += C(tx0 + 75, yb, 6.5, WARN, INK, 1.2)
    # 不予塗裝帶：工地銲接兩側各 100 mm
    z = 100 * s
    o += R(cx1, yf1 - 12, z, 10, TEN2, TEN, 1.2) + T(cx1 + z / 2, yf1 - 18, '100', 14, TEN, 'middle', 'bold')
    # 標註（右側）
    cxl = 640
    notes = [
        (150, cx1 + z / 2 + 8, yf1 - 7, TEN, '綠帶：兩側各 100 mm 不塗', '工地銲接部位｜第 6 章'),
        (208, cx1 + 8, yf1 + tf / 2, COMP, '梁翼 CJP（工地銲）', '預熱、氫、UT 100%｜第 1、2、4 章'),
        (266, cx1 + 14, yf1 + tf + 3, KEY, '背銲條', '人工缺口→移除修磨｜第 7 章'),
        (324, tx0 + 75, ty0 + 22, WARN, '剪力板＋M22 摩阻螺栓', '夾緊力、摩擦面不塗｜第 5、6 章'),
        (382, tx0 + 3, (ty0 + ty1) / 2 + 20, COMP, '剪力板填角銲', '最小銲腳依厚板｜第 1、3 章'),
    ]
    for ly, px, py, c, a, b in notes:
        o += L(cxl - 6, ly - 5, px, py, c, 1.3, '5 3') + C(px, py, 3, c, c, 1)
        o += T(cxl, ly, a, 15, c, 'start', 'bold') + T(cxl, ly + 21, b, 14, INK, 'start')
    # 左側：柱
    o += T(75, 70, '箱型柱', 15, INK, 'middle', 'bold') + T(75, 92, '□550×50', 14, INK, 'middle')
    o += T(75, 114, 'SN490C', 14, KEY, 'middle', 'bold') + T(75, 136, '第 7 章', 14, MUT, 'middle')
    o += T(75, yf1 + 60, '內橫隔板', 15, COMP, 'middle', 'bold') + T(75, yf1 + 82, 'ESW 銲（紅）', 14, COMP, 'middle')
    o += T(75, yf1 + 104, '熱輸入大', 14, INK, 'middle') + T(75, yf1 + 126, '第 1、4 章', 14, MUT, 'middle')
    o += L(118, yf1 + 66, cx0 + tw_ - 2, yf1 + tf / 2, COMP, 1.3, '5 3')
    o += dim(cx0, 532, cx1, 532, '550', MUT, size=14)
    o += T(cx1 + (bx1 - cx1) / 2, yf2 + 34, '梁 H600×200×11×17（SN490B）', 14, INK, 'middle')
    return svg(W, H, o, '貫穿範例接頭')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2, 'fig0_3': fig0_3}
