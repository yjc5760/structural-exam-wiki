# -*- coding: utf-8 -*-
"""第 5 章：塊狀剪力與 0.6 的來源。"""
from plot import *  # noqa
from calcs import block_shear
import math

B = block_shear()


def fig5_1():
    W, H = 900, 420
    o = ''
    # (a) 兩種受力狀態的莫爾圓
    o += T(225, 28, '(a) 莫爾圓：單軸拉 vs 純剪', 16, INK, 'middle', 'bold')
    cx, cy, R0 = 225, 200, 120   # R0 對應 Fy/2
    o += A(40, cy, 420, cy, INK, 1.4, 9) + A(cx - 60, cy + 150, cx - 60, cy - 160, INK, 1.4, 9)
    o += T(420, cy - 10, 'σ', 16, INK, 'end', italic=True) + T(cx - 52, cy - 150, 'τ', 16, INK, 'start', italic=True)
    ox = cx - 60  # 原點
    # 單軸：圓心 Fy/2、半徑 Fy/2
    o += C(ox + R0, cy, R0, 'none', TEN, 2.6)
    o += C(ox + 2 * R0, cy, 5, TEN, '#fff', 1.4) + T(ox + 2 * R0 + 6, cy + 20, '*F*_{y}', 15, TEN, 'start', 'bold')
    o += T(ox + R0 + 40, cy - R0 - 8, '單軸拉到 *F*_{y}', 14.5, TEN, 'start', 'bold')
    # 純剪：圓心 0、半徑 τ = Fy/√3
    rt = 2 * R0 / math.sqrt(3)
    o += C(ox, cy, rt, 'none', WARN, 2.6)
    o += C(ox, cy - rt, 5, WARN, '#fff', 1.4)
    o += T(ox - 10, cy - rt - 6, 'τ_{y} = *F*_{y}/√3', 15, WARN, 'end', 'bold')
    o += C(ox + rt, cy, 4, WARN, '#fff', 1.2) + C(ox - rt, cy, 4, WARN, '#fff', 1.2)
    o += T(ox - rt - 4, cy + 22, '−τ', 14, WARN, 'end') + T(ox + rt + 4, cy + 22, '+τ', 14, WARN, 'start')
    o += T(225, 400, '純剪＝一方向拉 τ、另一方向壓 τ（主應力 ±τ）', 14.5, INK, 'middle')
    o += L(450, 20, 450, 410, GRID, 1.5)
    # (b) von Mises 橢圓
    o += T(675, 28, '(b) von Mises 降伏面（σ_{1}–σ_{2} 平面）', 16, INK, 'middle', 'bold')
    pc, pcy, s = 675, 215, 105   # s px 對應 Fy
    o += A(pc - 165, pcy, pc + 175, pcy, INK, 1.4, 9) + A(pc, pcy + 160, pc, pcy - 170, INK, 1.4, 9)
    o += T(pc + 175, pcy + 22, 'σ_{1}', 15, INK, 'end') + T(pc + 8, pcy - 160, 'σ_{2}', 15, INK, 'start')
    pts = []
    for i in range(361):
        th = math.radians(i)
        # σ1² − σ1σ2 + σ2² = Fy²：主軸 45°，半軸 √2 Fy 與 √(2/3) Fy
        a, b = math.sqrt(2), math.sqrt(2 / 3)
        u, v = a * math.cos(th), b * math.sin(th)
        x1 = (u - v) / math.sqrt(2); x2 = (u + v) / math.sqrt(2)
        pts.append((pc + x1 * s, pcy - x2 * s))
    o += P(pts, KEY, 2.6, close=True)
    o += L(pc - 140, pcy + 140, pc + 140, pcy - 140, MUT, 1, '4 4') if False else ''
    o += L(pc - 130, pcy - 130, pc + 130, pcy + 130, MUT, 1.2, '5 4')
    o += T(pc - 126, pcy - 136, 'σ_{2} = −σ_{1}（純剪）', 14, MUT, 'start')
    o += C(pc + s, pcy, 6, TEN, '#fff', 1.6) + T(pc + s + 8, pcy - 10, '(*F*_{y}, 0)', 14.5, TEN, 'start', 'bold')
    t = 1 / math.sqrt(3)
    o += C(pc + t * s, pcy + t * s, 6, WARN, '#fff', 1.6)
    o += T(pc + t * s + 10, pcy + t * s + 6, '(τ, −τ)', 14.5, WARN, 'start', 'bold')
    o += R(480, 330, 390, 74, KEY2, KEY, 1.3, 8)
    o += T(675, 354, '代入 σ_{1}=τ、σ_{2}=−τ：τ² + τ² + τ² = *F*_{y}²', 14.5, KEY, 'middle', 'bold')
    o += T(675, 382, '⇒ τ_{y} = *F*_{y}/√3 = 0.577*F*_{y} ≈ 0.6*F*_{y}', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '0.6 的來源')


def fig5_2():
    W, H = 900, 400
    o = T(450, 26, '角鋼連接肢展開（依 2.5 節範例比例）：沿螺栓線剪開＋往肢趾拉開', 16, INK, 'middle', 'bold')
    sc = 26
    ox, oy = 130, 70
    Lm = 24  # 畫出的角鋼長度 cm
    o += R(ox - 90, oy - 14, 90 + 19 * sc, 10 * sc + 28, STEEL2, STEEL, 1.2)   # 節點板
    o += T(ox - 84, oy + 10 * sc + 38, '節點板', 14, MUT, 'start')
    o += R(ox, oy, Lm * sc, 10 * sc, STEEL3, INK, 1.6)
    o += T(ox + Lm * sc + 6, oy + 12, '肢背', 14, MUT, 'start') + T(ox + Lm * sc + 6, oy + 10 * sc, '肢趾', 14, MUT, 'start')
    yb = oy + 5.5 * sc
    xs = [ox + (3.5 + 7 * i) * sc for i in range(3)]
    # 塊體
    xe = xs[-1]
    o += R(ox, yb, xe - ox, 4.5 * sc, COMPM, None, 0, op=0.6)
    for x in xs:
        o += C(x, yb, 1.15 * sc, '#fff', INK, 1.5)
    o += L(ox, yb, xe, yb, COMP, 3.6)
    o += L(xe, yb, xe, oy + 10 * sc, AC, 3.6)
    o += T((ox + xe) / 2, yb - 40, '剪力面（紅）：長 3.5 + 2 × 7 = 17.5，穿過 2.5 個孔', 15, COMP, 'middle', 'bold')
    o += T(xe + 12, yb + 2.6 * sc, '拉力面（藍）：4.5，半個孔', 15, AC, 'start', 'bold')
    o += T((ox + xe) / 2, yb + 2.8 * sc, '被撕下的塊體', 15, COMP, 'middle', 'bold')
    o += A(ox + Lm * sc + 20, oy + 5 * sc, ox + Lm * sc + 80, oy + 5 * sc, TEN, 3, 12)
    o += T(ox + Lm * sc + 50, oy + 5 * sc - 12, '*T*', 16, TEN, 'middle', 'bold')
    o += dim(ox, oy + 10 * sc + 18, xs[0], oy + 10 * sc + 18, '3.5', INK, size=14)
    o += dim(xs[0], oy + 10 * sc + 18, xs[1], oy + 10 * sc + 18, '7', INK, size=14)
    o += dim(xs[1], oy + 10 * sc + 18, xs[2], oy + 10 * sc + 18, '7', INK, size=14)
    o += dim(ox - 30, oy, ox - 30, yb, '5.5', INK, size=14, side=-1)
    o += dim(ox - 30, yb, ox - 30, oy + 10 * sc, '4.5', INK, size=14, side=-1)
    return svg(W, H, o, '塊狀剪力幾何')


def fig5_3():
    W, H = 900, 390
    Fu, Fy = B['Fu'], B['Fy']
    sv_r = 0.6 * Fu * B['Anv']; sv_y = 0.6 * Fy * B['Agv']; tt = Fu * B['Ant']
    o = ''
    x0, sc = 260, 12.5
    rows = [('式①：剪力面斷裂＋拉力面斷裂', sv_r, '0.6*F*_{u}*A*_{nv}', COMP, B['rup']),
            ('式②：剪力面降伏＋拉力面斷裂', sv_y, '0.6*F*_{y}*A*_{gv}', WARN, B['cap'])]
    for i, (lab, sv, svl, c, tot) in enumerate(rows):
        y = 70 + i * 120
        o += T(x0, y - 14, lab, 16, c, 'start', 'bold')
        o += R(x0, y, sv * sc, 44, c, None, 0, 4, op=0.85)
        o += T(x0 + sv * sc / 2, y + 28, f'{svl} = {sv:.1f}', 15, '#fff', 'middle', 'bold')
        o += R(x0 + sv * sc, y, tt * sc, 44, AC, None, 0, 4, op=0.85)
        o += T(x0 + sv * sc + tt * sc / 2, y + 28, f'{tt:.1f}', 15, '#fff', 'middle', 'bold')
        o += T(x0 + (sv + tt) * sc + 10, y + 28, f'= {tot:.1f} tf', 16, c, 'start', 'bold')
        o += T(x0 - 14, y + 28, '剪力面 ＋ 拉力面', 14, MUT, 'end')
    o += T(x0 + sv_r * sc + tt * sc / 2, 60 + 120 + 44 + 30, '拉力面都是 *F*_{u}*A*_{nt}', 14, AC, 'middle')
    o += R(120, 296, 660, 80, KEY2, KEY, 1.4, 8)
    o += T(450, 322, f'取小：min({B["rup"]:.1f}, {B["cap"]:.1f}) = {min(B["rup"], B["cap"]):.1f}　→　φ*R*_{{n}} = 0.75 × {min(B["rup"], B["cap"]):.1f} = {B["BS"]:.1f} tf', 16, KEY, 'middle', 'bold')
    o += T(450, 352, '式② 較小：剪力面「先降伏」就已經撐不住，不必等到它斷裂（本例由上限式控制）', 14.5, INK, 'middle')
    return svg(W, H, o, '塊狀剪力兩式')


def fig5_4():
    W, H = 900, 360
    rows = [('GSY 全斷面降伏', B['GSY'], B['GSY_a']), ('NSF 淨斷面斷裂', B['NSF'], B['NSF_a']), ('BS 塊狀剪力', B['BS'], B['BS_a'])]
    o = ''
    x0, sc = 230, 11
    o += T(x0, 34, 'LRFD φ*R*_{n}（實心）', 15, AC, 'start', 'bold')
    o += T(x0 + 400, 34, 'ASD 容許值（空心）', 15, WARN, 'start', 'bold')
    for i, (lab, lr, ad) in enumerate(rows):
        y = 64 + i * 88
        ctl = i == 2
        c = COMP if ctl else STEEL
        o += T(x0 - 14, y + 30, lab, 15, COMP if ctl else INK, 'end', 'bold')
        o += R(x0, y, lr * sc, 26, c, None, 0, 4, op=0.9)
        o += T(x0 + lr * sc + 8, y + 19, f'{lr:.1f}', 15, c if ctl else INK, 'start', 'bold')
        o += R(x0, y + 32, ad * sc, 24, '#fff', WARN if ctl else STEEL, 2, 4)
        o += T(x0 + ad * sc + 8, y + 50, f'{ad:.1f}', 15, WARN if ctl else INK, 'start', 'bold')
    o += R(150, 324 - 6, 650, 34, KEY2, KEY, 1.3, 8)
    o += T(475, 340, f'兩套都是塊狀剪力控制：LRFD {B["BS"]:.1f} tf、ASD {B["BS_a"]:.1f} tf（比值 {B["BS"] / B["BS_a"]:.2f}）', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '三種極限狀態總比較')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3, 'fig5_4': fig5_4}
