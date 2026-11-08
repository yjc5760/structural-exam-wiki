# -*- coding: utf-8 -*-
"""第 5 章：高強度螺栓。數值由 calcs.bolt_calc() 算出。"""
from plot import *  # noqa
from calcs import *  # noqa
import math

B = bolt_calc()


def _joint(ox, gap):
    o = ''
    cx = ox + 200
    yt, yb = 120, 220
    if not gap:
        o += R(ox + 40, yt, 320, 50, STEEL2, INK, 1.4) + R(ox + 40, yt + 50, 320, 50, STEEL3, INK, 1.4)
    else:
        # 上板被拱起：左右兩端貼合，中間有縫
        o += P([(ox + 40, yt), (ox + 360, yt), (ox + 360, yt + 50), (cx + 40, yt + 40), (cx - 40, yt + 40), (ox + 40, yt + 50)],
               INK, 1.4, fill=STEEL2, close=True)
        o += R(ox + 40, yt + 60, 320, 40, STEEL3, INK, 1.4)
        o += R(ox + 200, yt + 40, 120, 20, '#fff', None, 0)
    # 螺栓
    o += R(cx - 11, yt - 22, 22, yb - yt + 44, '#b0bec5', INK, 1.2)
    o += R(cx - 26, yt - 34, 52, 14, '#78909c', INK, 1.2) + R(cx - 26, yb + 20, 52, 14, '#78909c', INK, 1.2)
    o += A(cx, yt - 40, cx, yt - 80, WARN, 3, 11) + A(cx, yb + 40, cx, yb + 80, WARN, 3, 11)
    o += T(cx + 10, yt - 60, '*T*（預拉力）', 15, WARN, 'start', 'bold')
    if not gap:
        for k in (-1, 1):
            o += A(cx + k * 30, yt + 18, cx + k * 30, yt + 46, TEN, 2.4, 9) + A(cx + k * 30, yt + 82, cx + k * 30, yt + 54, TEN, 2.4, 9)
        o += T(cx + 60, yt + 54, '夾緊力＝*T*', 14, TEN, 'start', 'bold')
        o += A(ox + 360, yt + 25, ox + 400, yt + 25, INK, 2.4, 10) + A(ox + 40, yt + 75, ox + 0, yt + 75, INK, 2.4, 10)
        o += T(ox + 200, yb + 112, '(a) 板面密接：*T* 全部壓在接觸面上', 15, TEN, 'middle', 'bold')
        o += T(ox + 200, yb + 134, '摩擦 *R* = μ*T*', 15, INK, 'middle')
    else:
        o += T(cx + 60, yt + 54, '縫：沒壓到', 14, COMP, 'start', 'bold')
        o += T(ox + 200, yb + 112, '(b) 板面有縫：*T* 被拿去把板壓彎', 15, COMP, 'middle', 'bold')
        o += T(ox + 200, yb + 134, '接觸面夾緊力 < *T* → 摩擦不足', 15, INK, 'middle')
    return o


def fig5_1():
    W, H = 900, 380
    o = T(450, 26, '種子 S5：摩阻接合的強度＝μ × 夾緊力', 16, INK, 'middle', 'bold')
    o += _joint(20, False) + L(450, 50, 450, 360, GRID, 1.5) + _joint(470, True)
    return svg(W, H, o, '夾緊力')


def fig5_2():
    W, H = 900, 380
    pl = Plot(90, 56, 520, 250, 0, 1.0, 0, 1100)
    o = T(350, 26, 'M22 F10T 的螺栓拉應力：0.70*F*_{u} 還在彈性，轉角法才推過降伏', 16, INK, 'middle', 'bold')
    def sig(x):           # 示意的應力–伸長（彈性斜線＋降伏後硬化），x：無因次伸長
        xe = 0.18
        if x <= xe:
            return B['Fy'] / xe * x
        return B['Fy'] + (B['Fu'] - B['Fy']) * (1 - math.exp(-(x - xe) / 0.25))
    o += pl.axes([], [0, 700, 900, 1000], '', 'MPa', size=14)
    o += T(pl.X(0.5), pl.y0 + pl.h + 30, '螺栓伸長（示意）→', 14, INK, 'middle')
    o += pl.curve(sig, 0, 1.0, AC, 3.2)
    o += pl.hline(B['sig_T0'], 0, 1.0, WARN, 1.6) + pl.hline(B['Fy'], 0, 1.0, COMP, 1.4)
    x70 = B['sig_T0'] / B['Fy'] * 0.18
    o += pl.dot(x70, B['sig_T0'], WARN, 7)
    o += T(pl.X(x70) + 10, pl.Y(B['sig_T0']) + 22, f'0.70*F*_{{u}} = {B["sig_T0"]:.0f}（{B["ratio_y"]*100:.0f}% *F*_{{y}}）彈性段', 14, WARN, 'start', 'bold')
    o += T(pl.X(0.98), pl.Y(B['Fy']) - 8, f'*F*_{{y}} = {B["Fy"]:.0f}', 14, COMP, 'end', 'bold')
    o += R(pl.X(0.3), pl.Y(1080), pl.X(0.7) - pl.X(0.3), pl.Y(900) - pl.Y(1080), COMP2, None, 0, op=0.6)
    o += T(pl.X(0.5), pl.Y(1050), '轉角法鎖緊常落在這裡（已降伏）', 14, COMP, 'middle', 'bold')
    o += R(640, 64, 248, 242, KEY2, KEY, 1.4, 10)
    rows = [('為什麼不能重用？', KEY, True), ('', INK, False), ('初鎖已推過降伏', INK, False), ('→ 永久伸長', INK, False),
            ('再鎖一次，塑性伸長', INK, False), ('在舊的上面累加', INK, False), ('→ 延性餘裕不足', COMP, True), ('', INK, False),
            ('次因：螺紋狀態改變', MUT, False), ('扭力係數 *K* 偏移', MUT, False)]
    for i, (s, c, b) in enumerate(rows):
        if s:
            o += T(764, 90 + i * 21, s, 14.5, c, 'middle', 'bold' if b else None)
    o += T(350, 366, f'規範 *T*_{{0}} = 0.70*F*_{{u}}*A*_{{t}} = 0.70×1000×303 = {B["T0"]:.0f} kN（M22，*A*_{{t}} 為螺紋有效面積）', 14, MUT, 'middle')
    return svg(W, H, o, '螺栓應力')


def fig5_3():
    W, H = 900, 380
    pl = Plot(90, 56, 500, 250, 0, 4.0, 0, 1.15)
    o = T(340, 26, '荷重–變形（示意）：誰和銲道在同一個變形範圍出力', 16, INK, 'middle', 'bold')
    o += pl.axes([0, 1, 2, 3, 4], [], '', '荷重', size=14)
    o += T(pl.X(2), pl.y0 + pl.h + 42, '接頭滑移／變形 (mm)', 14, INK, 'middle')
    weld = lambda x: min(1.0, x / 0.25) if x <= 0.9 else max(0.0, 1.0 - (x - 0.9) * 6)
    slip = lambda x: min(0.55, x / 0.05 * 0.55) if x < 0.6 else 0.55
    def bear(x):
        if x < 1.5:
            return min(0.12, x * 2)
        return min(0.95, 0.12 + (x - 1.5) * 0.9)
    o += pl.curve(weld, 0, 1.06, COMP, 3.2)
    o += pl.curve(lambda x: slip(x) if x < 1.5 else bear(x), 0, 4.0, TEN, 3, dash='8 4')
    o += pl.curve(bear, 0, 4.0, WARN, 3)
    o += T(pl.X(0.32), pl.Y(1.1), '銲道（勁、小變形就到頂）', 14, COMP, 'start', 'bold')
    o += T(pl.X(0.8), pl.Y(0.6), '摩阻型：滑動前就以摩擦傳力', 14, TEN, 'start', 'bold')
    o += T(pl.X(2.3), pl.Y(0.5), '承壓型：先滑過孔隙', 14, WARN, 'start', 'bold')
    o += T(pl.X(2.3), pl.Y(0.5) + 18, '螺桿頂到孔壁才出力', 14, WARN, 'start')
    o += R(pl.X(0), pl.Y(1.15), pl.X(0.9) - pl.X(0), pl.h, KEY2, None, 0, op=0.35)
    o += T(pl.X(0.5), pl.Y(0.8), '同一變形區', 14, KEY, 'middle', 'bold')
    o += R(620, 64, 268, 242, '#fff', INK, 1.2, 10)
    rows = [('極限設計法 10.1.8', KEY, True), ('', INK, False), ('摩阻型＋銲接：可共擔', TEN, True), ('（先鎖緊螺栓再銲）', INK, False), ('', INK, False),
            ('承壓型＋銲接：不可', COMP, True), ('全部由銲接承擔', INK, False), ('', INK, False), ('理由：變形相容', KEY, True)]
    for i, (s, c, b) in enumerate(rows):
        if s:
            o += T(754, 92 + i * 23, s, 14.5, c, 'middle', 'bold' if b else None)
    return svg(W, H, o, '混合接合')


def fig5_4():
    W, H = 900, 200
    o = T(450, 26, 'SS-2004-1㈡ 螺栓穿不進孔：先後順序就是配分', 16, INK, 'middle', 'bold')
    steps = [(AC, '① 沖梢校正', '鐵鎚 < 2.5 kg'), (WARN, '② 鉸孔擴孔', f'孔徑 ≤ 設計孔 + 2 mm'),
             (COMP, '③ 仍超出', '該孔不得使用'), (KEY, '④ 補救', '增設螺栓／換板＋驗算')]
    bw = 190; x = 30
    for i, (c, a, b) in enumerate(steps):
        o += R(x, 60, bw, 90, '#fff', c, 2, 10)
        o += T(x + bw / 2, 92, a, 16, c, 'middle', 'bold') + T(x + bw / 2, 122, b, 14.5, INK, 'middle')
        if i < 3:
            o += A(x + bw + 2, 105, x + bw + 22, 105, MUT, 2, 8)
        x += bw + 24
    o += T(450, 182, f'M22 標準孔 {B["hole"]} mm → 鉸孔後上限 {B["ream_max"]} mm；鉸孔須疊合後一次鉸、清除毛邊（施工規範 §5.3.1）', 14, MUT, 'middle')
    return svg(W, H, o, '孔位校正')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3, 'fig5_4': fig5_4}
