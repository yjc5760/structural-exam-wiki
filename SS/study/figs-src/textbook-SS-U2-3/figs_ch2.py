# -*- coding: utf-8 -*-
"""第 2 章：氫致冷裂。冷卻曲線由 calcs.T_at（Rosenthal 三維）逐點算出。"""
from plot import *  # noqa
from calcs import *  # noqa
import math


def fig2_1():
    W, H = 900, 470
    o = ''
    # 三角形頂點
    A_ = (450, 92); B_ = (230, 360); C_ = (670, 360)
    o += P([A_, B_, C_], COMP, 3, fill=COMP2, close=True)
    o += T(450, 255, '氫致冷裂', 20, COMP, 'middle', 'bold')
    o += T(450, 280, '（延遲裂縫）', 15, COMP, 'middle')
    o += T(450, 308, '三角同時成立才會裂', 14, INK, 'middle')
    for (x, y), lab, sub in ((A_, '① 氫', '擴散氫'), (B_, '② 硬脆組織', 'HAZ 淬硬（S1）'), (C_, '③ 拉應力', '殘留應力＋拘束')):
        o += C(x, y, 34, '#fff', COMP, 3)
        o += T(x, y + 6, lab.split(' ')[0], 18, COMP, 'middle', 'bold')
        o += T(x, y + (-62 if y < 200 else 60), lab.split(' ')[1], 16, COMP, 'middle', 'bold')
        o += T(x, y + (-42 if y < 200 else 80), sub, 14, INK, 'middle')
    # 三組對策框
    def blk(x, y, w, title, rows, c):
        h = 30 + 22 * len(rows)
        s = R(x, y, w, h, '#fff', c, 1.6, 10) + T(x + w / 2, y + 22, title, 15, c, 'middle', 'bold')
        for i, r in enumerate(rows):
            s += T(x + 12, y + 46 + i * 22, r, 14, INK, 'start')
        return s
    o += blk(560, 14, 330, '拆①：不讓氫進來', ['低氫系銲條、依規定烘乾', '溼度過高、下雨不銲', '清除油、銹、水分、舊漆'], TEN)
    o += blk(10, 14, 330, '拆②：不讓組織變硬', ['預熱（表 4.2-2）', '銲道不要太小（表 4.1-1）', '選低碳當量鋼材'], TEN)
    o += blk(310, 410, 280, '拆③：降低拉應力', ['合理銲接順序、減少拘束'], TEN)
    o += A(390, 95, 340, 70, TEN, 1.6, 9, dash='5 3') + A(510, 95, 556, 70, TEN, 1.6, 9, dash='5 3')
    o += T(812, 420, '預熱同時拆②與①', 15, KEY, 'middle', 'bold')
    o += T(812, 442, '（放慢冷卻＋讓氫逃走）', 14, KEY, 'middle')
    return svg(W, H, o, '氫致冷裂三要素')


def fig2_2():
    W, H = 900, 400
    pl = Plot(90, 64, 520, 256, 0, 300, 0, 600)
    o = T(470, 22, '熔合線附近（*r* = 6 mm）的冷卻曲線：預熱讓銲道在 100°C 以上待得更久', 16, INK, 'middle', 'bold')
    o += R(pl.X(0), pl.Y(600), pl.w, pl.Y(100) - pl.Y(600), '#fff8e1', None, 0)
    o += T(pl.X(296), pl.Y(560), '100°C 以上：氫擴散較快，可逃出銲道', 14, '#8d6e63', 'end')
    o += pl.axes([0, 50, 100, 150, 200, 250, 300], [0, 100, 200, 300, 400, 500, 600], '', '°C', size=14)
    o += T(pl.X(150), pl.y0 + pl.h + 42, '時間 (s)', 14, INK, 'middle')
    cs = [(20, AC, '不預熱（20°C）'), (66, TEN, '預熱 66°C'), (110, KEY, '預熱 110°C')]
    for T0, c, lab in cs:
        o += pl.curve(lambda t, T0=T0: T_at(E_SMAW, 6.0, max(t, 0.5), T0), 1.2, 300, c, 3)
    o += pl.hline(100, 0, 300, COMP, 1.6, '7 4')
    t1, t2 = t_to(E_SMAW, 100, 20), t_to(E_SMAW, 100, 66)
    o += pl.dot(t1, 100, AC, 6) + pl.dot(t2, 100, TEN, 6)
    o += pl.vline(t1, 0, 100, AC, 1.2) + pl.vline(t2, 0, 100, TEN, 1.2)
    o += T(pl.X(t1) + 5, pl.Y(12), f'{t1:.0f} s', 15, AC, 'start', 'bold')
    o += T(pl.X(t2) + 5, pl.Y(12), f'{t2:.0f} s', 15, TEN, 'start', 'bold')
    for i, (T0, c, lab) in enumerate(cs):
        yy = pl.Y(480) + i * 24
        o += L(pl.X(150), yy - 5, pl.X(172), yy - 5, c, 3) + T(pl.X(176), yy, lab, 14.5, c, 'start', 'bold')
    o += T(pl.X(176), pl.Y(480) + 3 * 24, '（110°C：局部散熱冷不到 100°C）', 14, KEY, 'start')
    o += R(640, 60, 250, 262, KEY2, KEY, 1.4, 10)
    rows = [('100°C 以上的時間', KEY, True), (f'不預熱　{t1:.0f} s', AC, True), (f'預熱 66°C　{t2:.0f} s', TEN, True),
            (f'→ 約 {t2 / t1:.1f} 倍', KEY, True), ('', INK, False), ('氫在熱的時候跑得快，', INK, False),
            ('冷了就卡在 HAZ 裡，', INK, False), ('慢慢往應力集中處聚，', INK, False), ('數小時～數天後才裂。', COMP, True)]
    for i, (s, c, b) in enumerate(rows):
        if s:
            o += T(765, 88 + i * 25, s, 14.5, c, 'middle', 'bold' if b else None)
    o += T(350, 392, f'模型：Rosenthal 厚板、一道手銲 {E_SMAW / 1000:.2f} kJ/mm；數值只代表趨勢。', 14, MUT, 'middle')
    return svg(W, H, o, '預熱與冷卻曲線')


def fig2_3():
    W, H = 900, 250
    o = T(450, 28, '「延遲」裂縫的時間軸：太早檢查就會漏掉', 16, INK, 'middle', 'bold')
    x0, x1, y = 70, 850, 120
    o += A(x0, y, x1, y, INK, 2.2, 10)
    marks = [(90, '銲接完成', AC), (230, '冷到 100°C 以下', AC), (420, '氫往應力集中處聚集', COMP), (640, '裂縫出現', COMP)]
    for x, lab, c in marks:
        o += C(x, y, 7, c, '#fff', 2) + T(x, y - 18, lab, 15, c, 'middle', 'bold')
    o += T(160, y + 32, '數分鐘', 14, MUT, 'middle') + T(330, y + 32, '數小時', 14, MUT, 'middle') + T(530, y + 32, '數小時～數天', 14, MUT, 'middle')
    o += R(110, 170, 300, 56, COMP2, COMP, 1.4, 8)
    o += T(260, 194, '銲完馬上做 NDT', 15, COMP, 'middle', 'bold') + T(260, 214, '裂縫還沒長出來 → 判定合格', 14, INK, 'middle')
    o += R(520, 170, 330, 56, TEN2, TEN, 1.4, 8)
    o += T(685, 194, '等一段時間再做最終檢查', 15, TEN, 'middle', 'bold') + T(685, 214, '（AWS 對部分高強度鋼規定 48 h）', 14, INK, 'middle')
    return svg(W, H, o, '延遲裂縫時間軸')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3}
