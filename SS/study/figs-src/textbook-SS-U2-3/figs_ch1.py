# -*- coding: utf-8 -*-
"""第 1 章：熱循環。曲線全部由 calcs.py 的 Rosenthal 模型與規範表逐點算出。"""
from plot import *  # noqa
from calcs import *  # noqa
import math

ZC = [COMP, '#e65100', '#f9a825', '#9e9d24']     # 熔融、粗晶、細晶、部分相變
ZF = ['#ef9a9a', '#ffcc80', '#fff59d', '#e6ee9c']


def fig1_1():
    W, H = 900, 400
    o = ''
    # (a) 剖面：以峰值溫度分區畫同心半圓（半徑依 r_peak，比例 22 px/mm）
    sc = 18.0
    cx, cy = 200, 120
    o += T(230, 28, '(a) 一道手銲的峰值溫度分區（剖面）', 16, INK, 'middle', 'bold')
    o += R(20, cy, 345, 250, STEEL2, None, 0)
    for (Tp, name), c, fz in reversed(list(zip(ZONES, ZC, ZF))):
        r = r_peak(E_SMAW, Tp) * sc
        o += f'<path d="M {f(cx - r)} {f(cy)} A {f(r)} {f(r)} 0 0 0 {f(cx + r)} {f(cy)} Z" fill="{fz}" stroke="{c}" stroke-width="1.4"/>'
    o += L(20, cy, 365, cy, INK, 2)
    o += T(30, cy - 10, '鋼板表面', 14, MUT, 'start')
    # 分區標籤（右側引線）
    lab_y = [cy + 30, cy + 70, cy + 110, cy + 150]
    for (Tp, name), c, ly in zip(ZONES, ZC, lab_y):
        r = r_peak(E_SMAW, Tp) * sc
        ang = math.radians(35)
        px, py = cx + (r - 4) * math.cos(ang), cy + (r - 4) * math.sin(ang)
        o += L(px, py, 372, ly - 5, c, 1.2)
        o += T(376, ly, f'{name}', 14, c, 'start', 'bold')
        o += T(376, ly + 17, f'＞{Tp}°C', 14, INK, 'start') if Tp != 1500 else T(376, ly + 17, '熔化後凝固', 14, INK, 'start')
    rm, r7 = r_peak(E_SMAW, 1500) * sc, r_peak(E_SMAW, 700) * sc
    o += dim(cx - r7, cy + r7 + 28, cx - rm, cy + r7 + 28, '', COMP, size=14)
    o += T(cx - (r7 + rm) / 2, cy + r7 + 52, f'HAZ ≈ {haz_width(E_SMAW):.1f} mm', 14, COMP, 'middle', 'bold')
    o += L(cx - r7, cy, cx - r7, cy + r7 + 32, COMP, 1, '3 3') + L(cx - rm, cy, cx - rm, cy + r7 + 32, COMP, 1, '3 3')
    # (b) 峰值溫度–距離：手銲 vs ESW
    pl = Plot(575, 70, 290, 250, 0, 60, 0, 1600)
    o += T(720, 28, '(b) 峰值溫度 vs. 離熱源距離', 16, INK, 'middle', 'bold')
    for (Tp, _), fz in zip(ZONES, ZF):
        top = 1600 if Tp == 1500 else [z[0] for z in ZONES][[z[0] for z in ZONES].index(Tp) - 1]
        o += R(pl.X(0), pl.Y(min(top, 1600)), pl.w, pl.Y(Tp) - pl.Y(min(top, 1600)), fz, None, 0, op=0.45)
    o += pl.axes([0, 20, 40, 60], [0, 700, 1500], '', '*T*_{peak} (°C)', grid=False, size=14)
    o += T(pl.X(30), pl.y0 + pl.h + 44, '離熱源距離 *r* (mm)', 14, INK, 'middle')
    o += pl.curve(lambda r: 20 + 2 / (math.pi * math.e) * E_SMAW / (RHOC * max(r, 0.1) ** 2), 2, 60, COMP, 3)
    o += pl.curve(lambda r: 20 + 2 / (math.pi * math.e) * E_ESW / (RHOC * max(r, 0.1) ** 2), 15, 60, KEY, 3)
    o += T(pl.X(10.5), pl.Y(1150), '手銲', 15, COMP, 'start', 'bold')
    o += T(pl.X(10.5), pl.Y(1150) + 18, f'{E_SMAW/1000:.1f} kJ/mm', 14, COMP, 'start')
    o += T(pl.X(20), pl.Y(1330), 'ESW', 15, KEY, 'start', 'bold')
    o += T(pl.X(20), pl.Y(1330) + 18, f'{E_ESW/1000:.0f} kJ/mm', 14, KEY, 'start')
    # HAZ 寬度棒
    for E, c, yv in ((E_SMAW, COMP, 380), (E_ESW, KEY, 240)):
        a, b = r_peak(E, 1500), r_peak(E, 700)
        o += L(pl.X(a), pl.Y(yv), pl.X(b), pl.Y(yv), c, 6, cap='butt')
    o += T(pl.X(0.3), pl.Y(380) + 22, f'{haz_width(E_SMAW):.1f} mm', 14, COMP, 'start', 'bold')
    o += T(pl.X(44), pl.Y(240) - 10, f'HAZ {haz_width(E_ESW):.0f} mm', 14, KEY, 'middle', 'bold')
    return svg(W, H, o, '銲道峰值溫度分區')


def fig1_2():
    W, H = 900, 400
    pl = Plot(90, 56, 520, 262, 8, 60, 0, 26)
    o = T(470, 22, '800→500°C 的冷卻時間 *t*_{8/5}：板越厚、銲道越小，冷得越快', 16, INK, 'middle', 'bold')
    # 危險帶（示意）
    o += R(pl.X(8), pl.Y(3.5), pl.w, pl.Y(0) - pl.Y(3.5), COMP2, None, 0)
    o += T(pl.X(59), pl.Y(0.9), '淬硬危險帶（示意；臨界值隨碳當量上升）', 14, COMP, 'end')
    o += pl.axes([10, 20, 30, 40, 50, 60], [0, 5, 10, 15, 20, 25], '', '*t*_{8/5} (s)', size=14)
    o += T(pl.X(34), pl.y0 + pl.h + 42, '板厚 *d* (mm)', 14, INK, 'middle')
    o += pl.curve(lambda d: t85(E_SMAW, d), 8, 60, AC, 3.2)
    o += pl.curve(lambda d: t85(E_SMALL, d), 8, 60, COMP, 3.2)
    o += pl.curve(lambda d: t85(E_SMALL, d, 66), 8, 60, TEN, 2.6, dash='8 5')
    o += T(pl.X(15.2), pl.Y(21.5), f'正常一道 {E_SMAW/1000:.2f} kJ/mm', 15, AC, 'start', 'bold')
    o += T(pl.X(11.4), pl.Y(8.5), '小銲腳一道（熱減半）', 15, COMP, 'start', 'bold')
    o += T(pl.X(36), pl.Y(t85(E_SMALL, 60, 66)) - 10, '同小銲腳＋預熱 66°C', 14, TEN, 'start', 'bold')
    # 轉換厚度
    dt = d_trans(E_SMAW)
    o += pl.vline(dt, 0, 26, MUT, 1.2)
    o += T(pl.X(dt) + 6, pl.Y(16), f'≈{dt:.0f} mm 以後', 14, MUT, 'start')
    o += T(pl.X(dt) + 6, pl.Y(16) + 18, '再厚也一樣（三維散熱）', 14, MUT, 'start')
    o += pl.dot(50, t85(E_SMAW, 50), AC, 6) + pl.dot(50, t85(E_SMALL, 50), COMP, 6)
    # 右側說明
    o += R(640, 60, 248, 270, KEY2, KEY, 1.4, 10)
    lines = [('薄板：熱只能沿板面走', INK), ('→ 二維散熱，冷得慢', INK), ('', INK),
             ('厚板：上下左右都能散', INK), ('→ 三維散熱，冷得快', INK), ('', INK),
             ('冷得越快 → 越容易', COMP), ('變成硬脆的麻田散鐵', COMP), ('', INK),
             ('對策：銲道別太小、', TEN), ('或預熱把起點抬高', TEN)]
    for i, (s, c) in enumerate(lines):
        if s:
            o += T(764, 88 + i * 22, s, 14.5, c, 'middle', 'bold' if c != INK else None)
    o += T(350, 392, '模型：Rosenthal 移動點熱源（λ = 25 W/m·K、ρc = 5 J/cm³·K），數值只代表趨勢', 14, MUT, 'middle')
    return svg(W, H, o, '冷卻時間與板厚')


def fig1_3():
    W, H = 900, 400
    pl = Plot(90, 52, 520, 270, 0, 100, 0, 170)
    o = T(380, 24, '施工規範 表 4.2-2 最低預熱溫度（逐列畫出）', 16, INK, 'middle', 'bold')
    o += pl.axes([0, 19, 38, 64, 100], [0, 21, 66, 110, 150], '', '°C', size=14)
    o += T(pl.X(50), pl.y0 + pl.h + 42, '板厚 *t* (mm)', 14, INK, 'middle')
    cols = {'甲': COMP, '乙': AC, '丙': KEY}
    offs = {'甲': 2.0, '乙': -2.0, '丙': 0.0}
    for cat, c in cols.items():
        pts = []
        for (a, b), T_ in zip(PREHEAT_BANDS, PREHEAT[cat]['T']):
            yv = (T_ if T_ is not None else 0) + offs[cat]
            pts += [pl.pt(max(a, 3), yv), pl.pt(min(b, 100), yv)]
        o += P(pts, c, 3.4 if cat != '丙' else 2.6, dash='9 5' if cat == '丙' else None)
    o += T(pl.X(67), pl.Y(42), '0 線＝不需預熱', 14, MUT, 'start')
    o += T(pl.X(67), pl.Y(42) + 19, '（母材 <0°C 先熱到 21°C）', 14, MUT, 'start')
    o += T(pl.X(66), pl.Y(150) - 10, '甲：一般鋼＋非低氫', 14, COMP, 'start', 'bold')
    o += T(pl.X(66), pl.Y(110) + 22, '乙：490 級＋低氫系', 14, AC, 'start', 'bold')
    o += T(pl.X(40), pl.Y(124) - 4, '丙：570 級', 14, KEY, 'start', 'bold')
    # 範例點
    o += pl.dot(50, 66, AC, 7)
    o += T(pl.X(50) - 8, pl.Y(66) - 12, '範例柱板 50 mm → 66°C', 14, AC, 'end', 'bold')
    # 右側讀表心得
    o += R(640, 58, 250, 268, '#fff', INK, 1.2, 10)
    rows = [('① 往右走（板厚↑）', COMP, True), ('每一列都升溫 → S1', INK, False), ('', INK, False),
            ('② 甲 → 乙', AC, True), ('換低氫系，整列降一級', INK, False), ('→ S2（氫少了）', INK, False), ('', INK, False),
            ('③ 丙比乙高一級', KEY, True), ('強度高、碳當量高', INK, False), ('→ 更容易淬硬', INK, False)]
    for i, (s, c, b) in enumerate(rows):
        if s:
            o += T(765, 86 + i * 23, s, 14.5, c, 'middle', 'bold' if b else None)
    o += T(350, 392, '甲、乙兩線上下微移 2°C 以免重疊；丙除第一格外與甲相同。', 14, MUT, 'middle')
    return svg(W, H, o, '預熱溫度表')


def fig1_4():
    W, H = 900, 380
    pl = Plot(90, 50, 500, 260, 0, 40, 0, 10)
    o = T(380, 24, '最小銲腳尺寸：由「較厚」那片板決定', 16, INK, 'middle', 'bold')
    o += pl.axes([0, 6, 12, 19, 30, 40], [0, 3, 5, 6, 8, 10], '', '*w*_{min} (mm)', size=14)
    o += T(pl.X(20), pl.y0 + pl.h + 40, '較厚板 *t* (mm)', 14, INK, 'middle')
    pts = []
    lo = 0
    for tu, w in FILLET_MIN:
        hi = tu if tu is not None else 40
        pts += [pl.pt(lo, w), pl.pt(hi, w)]
        lo = hi
    o += P(pts, COMP, 3.6)
    k = fillet_trend_k()
    o += pl.curve(lambda t: k * math.sqrt(t), 1, 19, KEY, 2.4, dash='7 5')
    o += pl.curve(lambda t: k * math.sqrt(t), 19, 40, KEY, 1.6, dash='2 5')
    o += T(pl.X(31), pl.Y(6.5), f'趨勢 *w* ≈ {k:.2f}√*t*', 15, KEY, 'middle', 'bold')
    o += T(pl.X(1.5), pl.Y(8.9), '施工規範 表 4.1-1（紅）', 15, COMP, 'start', 'bold')
    o += T(pl.X(20.5), pl.Y(9.55), '19 mm 以上固定 8 mm：', 14, COMP, 'start')
    o += T(pl.X(20.5), pl.Y(9.55) + 18, '再厚改靠預熱控制（圖 1-3）', 14, COMP, 'start')
    o += pl.dot(12, 5, AC, 7)
    o += T(pl.X(12) + 10, pl.Y(5) + 22, '範例剪力板 12 mm → 5 mm', 14, AC, 'start', 'bold')
    o += R(620, 60, 270, 250, KEY2, KEY, 1.4, 10)
    rows = ['為什麼長成 √*t*？（記法）', '', '薄板冷卻：*t*_{8/5} ∝ *E*²/*d*²',
            '要 *t*_{8/5} 不變 → *E* ∝ *d*', '一道熱量 *E* ∝ 銲道面積 ∝ *w*²', '→ *w*² ∝ *d* → *w* ∝ √*d*',
            '', '表中三列都貼著這條線']
    for i, s in enumerate(rows):
        if s:
            o += T(755, 88 + i * 25, s, 14.5, KEY if i in (0, 7) else INK, 'middle', 'bold' if i in (0, 7) else None)
    o += T(340, 372, '紫虛線是簡化模型的記法，不是規範公式；規範以表 4.1-1 為準。', 14, MUT, 'middle')
    return svg(W, H, o, '最小銲腳尺寸')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3, 'fig1_4': fig1_4}
