# -*- coding: utf-8 -*-
"""第 7 章：連續梁（三彎矩方程、共軛梁）。所有曲線取自 calcs.py 的閉合解，已與有限元素逐點比對。"""
from figs_common import *  # noqa
import calcs as K

DEF = KEY


def dense(fn, x1, x2, n=300, breaks=()):
    return il_curve(None, 0, 0, fn, x1, x2, n=n, breaks=breaks)


def fig7_1():
    """三彎矩方程的來源：B 處兩側轉角諧和。"""
    W, H = 900, 600
    ax = Ax(110, 34)          # 20 m → 680 px
    o = ''
    yb = 120
    o += T(14, 26, '(a) 兩跨連續梁：B 處梁是連續的 → 左右兩跨在 B 的切線轉角相同', 16, INK, 'start', 'bold')
    o += beam(ax, yb, 0, 20, [(0, 'roller'), (10, 'pin'), (20, 'roller')], labels=[(0, 'A', -14), (10, 'B'), (20, 'C', 14)])
    o += unit_load(ax(3.5), yb - 3)
    o += dim(ax(0), yb - 70, ax(3.5), yb - 70, '*u*', MUT, size=15)
    o += dim(ax(0), yb + 48, ax(10), yb + 48, '*L*_{1}', MUT, size=15) + dim(ax(10), yb + 48, ax(20), yb + 48, '*L*_{2}', MUT, size=15)
    # (b) 拆成兩根簡支梁 + M_B
    y2 = 330
    o += T(14, 222, '(b) 在 B 切開：兩根簡支梁，切口補上一對 *M*_{*B*}（未知）', 16, INK, 'start', 'bold')
    ts = np.linspace(0, 10, 101)
    dm = max(K.ss_defl(3.5, t) for t in ts)
    sc = 42 / dm
    X1 = lambda t: ax(t * 9.7 / 10)
    o += L(ax(0), y2, ax(9.7), y2, STEEL3, 3, '8 6') + L(ax(10.3), y2, ax(20), y2, STEEL3, 3, '8 6')
    o += P([(X1(t), y2 + sc * K.ss_defl(3.5, t)) for t in ts], COMP, 3.5)
    o += roller(ax(0), y2 + 3) + pin(ax(9.7), y2 + 3) + pin(ax(10.3), y2 + 3) + roller(ax(20), y2 + 3)
    o += unit_load(X1(3.5), y2 + sc * K.ss_defl(3.5, 3.5) - 3, h=36)
    # B 端切線（由曲線末端斜率外插）
    x9, y9 = X1(9.0), y2 + sc * K.ss_defl(3.5, 9.0)
    xb, ybb = X1(10), y2
    kx, ky = xb - x9, ybb - y9
    nn = (kx ** 2 + ky ** 2) ** 0.5
    o += L(xb - 60 * kx / nn, ybb - 60 * ky / nn, xb + 90 * kx / nn, ybb + 90 * ky / nn, COMP, 1.6, '5 4')
    o += T(xb + 96 * kx / nn + 4, ybb + 96 * ky / nn - 2, 'θ_{*P*}（B 端轉角）', 15, COMP, 'start', 'bold')
    o += moment(ax(9.7) - 8, y2 - 40, 16, cw=False, c=KEY, start=330, span=200)
    o += moment(ax(10.3) + 8, y2 - 40, 16, cw=True, c=KEY, start=210, span=200)
    o += T(ax(10), y2 - 76, '*M*_{*B*}', 16, KEY, 'middle', 'bold')
    o += R(40, 400, 820, 186, KEY2, KEY, 1.4, 10)
    o += T(450, 430, '左跨在 B 的轉角 ＝ 載重造成的 θ_{*P*} ＋ *M*_{*B*} 造成的 *M*_{*B*}*L*_{1}/3*EI* ＋ *M*_{*A*} 造成的 *M*_{*A*}*L*_{1}/6*EI*', 15, INK, 'middle', 'bold')
    o += T(450, 460, '簡支梁端轉角（1 在距「遠端」*u* 處）：θ_{*P*} = *u*(*L*² − *u*²) / 6*EIL*', 15, INK, 'middle')
    o += T(450, 490, '連續 ⇒ 兩跨在 B 的轉角相加 ＝ 0，整理（乘 6*EI*）：', 15, INK, 'middle')
    o += T(450, 526, '*M*_{*A*}*L*_{1} + 2*M*_{*B*}(*L*_{1}+*L*_{2}) + *M*_{*C*}*L*_{2} = − Σ *u*(*L*² − *u*²)/*L*', 18, KEY, 'middle', 'bold')
    o += T(450, 562, '「2」來自 *ML*/3 對 *ML*/6 的兩倍；「6」來自轉角公式裡的 6*EI*', 15, MUT, 'middle')
    return svg(W, H, o, '三彎矩方程的來源')


def fig7_2():
    """SA-2005-3：D 點彎矩影響線，每 2.5 m 一點。"""
    W, H = 900, 480
    ax = Ax(110, 34)
    o = ''
    yb = 60
    o += beam(ax, yb, 0, 20, [(0, 'roller'), (10, 'pin'), (20, 'roller')], labels=[(0, 'A', -14), (10, 'B'), (20, 'C', 14)])
    o += L(ax(15), yb - 12, ax(15), yb + 12, KEY, 3) + T(ax(15), yb - 18, 'D', 16, KEY, 'middle', 'bold')
    base, sy = 330, 95
    o += P([(ax(x), base - sy * v) for x, v in ((10, 0), (15, 2.5), (20, 0))], STEEL, 2, dash='6 5')
    o += T(ax(15) + 12, base - sy * 2.5 + 4, '簡支 2.5', 15, MUT, 'start')
    pts = dense(K.md05, 0, 20)
    labs = {2.5: ('−75/256', 's'), 5.0: ('−15/32', 's'), 7.5: ('−105/256', 's'), 12.5: ('215/256', (-36, 0)),
            15.0: ('65/32', (-40, -6)), 17.5: ('245/256', (40, 0))}
    vals = [(x, v, labs[x][0], labs[x][1]) for x, v in K.MD05_TAB if x in labs]
    o += il(ax, base, sy, pts, ticks=[x for x, _ in K.MD05_TAB], vals=vals, name='IL *M*_{*D*}', name_x=8, vsize=14)
    o += T(14, base + 24, '（m）', 14, MUT, 'start')
    o += T(ax(5), base - 50, 'AB 跨：*M*_{*B*}/2（負）', 15, COMP, 'middle', 'bold')
    o += T(ax(15), 430, 'BC 跨：簡支三角形 ＋ *M*_{*B*}/2', 15, AC, 'middle', 'bold')
    return svg(W, H, o, 'SA-2005-3 M_D 影響線')


def fig7_3():
    """SA-2011-3：M_B 與 M_C 影響線；均布只鋪 BD 跨。"""
    W, H = 900, 770
    ax = Ax(110, 11.5)        # 60 m → 690 px
    o = ''
    yb = 60
    o += beam(ax, yb, 0, 60, [(0, 'roller'), (30, 'roller'), (60, 'pin')], labels=[(0, 'A', -14), (30, 'B'), (60, 'D', 14)])
    o += L(ax(45), yb - 12, ax(45), yb + 12, KEY, 3) + T(ax(45), yb - 18, 'C', 16, KEY, 'middle', 'bold')
    tk = (0, 15, 30, 45, 60)
    base, sy = 160, 26
    o += il(ax, base, sy, dense(K.mb11, 0, 60), ticks=tk, name='IL *M*_{*B*}', name_x=8,
            vals=[(K.XMIN11, K.MB11_MIN, '−2.887', 's'), (60 - K.XMIN11, K.MB11_MIN, '−2.887', 's')])
    o += T(ax(30), base - 14, '全線為負：任何向下載重都讓 B 上側受拉', 15, COMP, 'middle', 'bold')
    base, sy = 470, 26
    o += il(ax, base, sy, dense(K.mc11, 0, 60, breaks=()), ticks=tk, name='IL *M*_{*C*}', name_x=8,
            vals=[(45, K.MC11_PEAK, '195/32 = 6.094', 'n'), (K.XMIN11, K.MC11_AB, '−1.443', 's')])
    o += T(ax(45), base - 50, '+84.375 m²', 15, AC, 'middle', 'bold')
    o += T(ax(15), base + 22, '−28.125 m²', 15, COMP, 'middle', 'bold')
    o += udl(ax(30), ax(60), 610, AC, 22, n=15)
    o += T(ax(45), 580, '*w* = 2 kN/m 只鋪 BD 跨', 15, AC, 'middle', 'bold')
    o += R(40, 650, 820, 106, KEY2, KEY, 1.4, 10)
    o += T(450, 680, '正面積 = *L*²/8（簡支三角形）＋ ½ × (−*L*²/16)（*M*_{*B*} 那一跨）= 3*L*²/32 = 84.375', 16, KEY, 'middle', 'bold')
    o += T(450, 712, '*M*_{*C*,max} = 2 × 84.375 = 168.75 kN·m；鋪滿 60 m 只有 112.5（少三分之一）', 16, INK, 'middle', 'bold')
    o += T(450, 740, '極值都在 *u* = *L*/√3 = 17.32 m：所有曲線段都正比於 *M*_{*B*}(*u*)', 15, MUT, 'middle')
    return svg(W, H, o, 'SA-2011-3 M_B、M_C')


def fig7_4():
    """SA-2015-2：解除 F 剪力的基本結構、反力與彎矩圖（共軛載重）。"""
    W, H = 900, 600
    ax = Ax(90, 9)          # 80 m → 720 px
    o = ''
    yb = 120
    o += T(14, 30, '(a) 題目：A 鉸、B、D、E 滾、C 內鉸；F 在 AB 中點 → 1 度靜不定', 16, INK, 'start', 'bold')
    o += beam(ax, yb, 0, 80, [(0, 'pin'), (30, 'roller'), (50, 'roller'), (80, 'roller')], hinges=[40],
              labels=[(0, 'A', -14), (15, 'F'), (30, 'B'), (40, 'C'), (50, 'D'), (80, 'E', 14)])
    o += L(ax(15), yb - 10, ax(15), yb + 10, KEY, 3)
    # 剪力對與反力
    o += A(ax(15) - 8, yb - 50, ax(15) - 8, yb - 4, COMP, 2.4, 10) + A(ax(15) + 8, yb - 4, ax(15) + 8, yb - 50, COMP, 2.4, 10)
    o += T(ax(15) - 14, yb - 34, '1', 15, COMP, 'end', 'bold') + T(ax(15) + 14, yb - 34, '1', 15, COMP, 'start', 'bold')
    o += T(ax(15), yb - 58, 'F 切成滑塊、施剪力對', 15, COMP, 'middle', 'bold')
    for x, r in ((0, 1), (30, -4), (50, 4), (80, -1)):
        o += T(ax(x), yb + 60, f'{r:+d}', 16, TEN, 'middle', 'bold')
    o += T(ax(65), yb + 60, '反力（↑ 為正）', 15, TEN, 'middle')
    o += dim(ax(0), yb + 84, ax(15), yb + 84, '15', MUT, size=14) + dim(ax(15), yb + 84, ax(30), yb + 84, '15', MUT, size=14)
    o += dim(ax(30), yb + 84, ax(40), yb + 84, '10', MUT, size=14) + dim(ax(40), yb + 84, ax(50), yb + 84, '10', MUT, size=14)
    o += dim(ax(50), yb + 84, ax(80), yb + 84, '30 m', MUT, size=14)
    # (b) 彎矩圖
    base, sy = 370, 2.1
    o += T(14, 260, '(b) 彎矩 *M*(*x*)（= 共軛梁的載重 ×*EI*）：C 是內鉸，*M*(40) 必須是 0 ← 反力的檢查', 16, INK, 'start', 'bold')
    pts = [(0, 0), (30, 30), (40, 0), (50, -30), (80, 0)]
    o += il(ax, base, sy, pts, c=WARN, pfill=WARN2, nfill='#ffe0b2', ticks=(0, 15, 30, 40, 50, 80),
            vals=[(30, 30, '30', 'n'), (40, 0, '0', (0, -12)), (50, -30, '−30', 's')])
    o += R(40, 492, 820, 96, KEY2, KEY, 1.4, 10)
    o += T(450, 520, '共軛梁換邊界：端鉸 → 端鉸；中間支承 B、D → 內鉸；內鉸 C → 中間支承', 15, KEY, 'middle', 'bold')
    o += T(450, 548, '滑塊 F（位移跳、轉角連續）→ 共軛梁上一個集中力矩 *M*_{0}（*M*^{*} 跳、*V*^{*} 連續）', 15, KEY, 'middle', 'bold')
    o += T(450, 576, f'4 條方程解出：*EI*·Δ_{{*F*}} = *M*_{{0}} = {int(K.CONJ15["dF"])}；*EI*·*y*(*F*⁻) = −{-K.CONJ15["yFm"]}；*EI*·*y*(*C*) = −{-int(K.CONJ15["yC"])}', 15, INK, 'middle')
    return svg(W, H, o, 'SA-2015-2 基本結構')


def fig7_5():
    """SA-2015-2：V_F 影響線。"""
    W, H = 900, 420
    ax = Ax(90, 9)
    o = ''
    yb = 50
    o += beam(ax, yb, 0, 80, [(0, 'pin'), (30, 'roller'), (50, 'roller'), (80, 'roller')], hinges=[40],
              labels=[(0, 'A', -14), (30, 'B'), (40, 'C'), (50, 'D'), (80, 'E', 14)])
    o += L(ax(15), yb - 10, ax(15), yb + 10, KEY, 3) + T(ax(15), yb - 16, 'F', 16, KEY, 'middle', 'bold')
    base, sy = 270, 200
    pts = dense(K.vf15, 0, 80, n=400, breaks=())
    pts = [p for p in pts if abs(p[0] - 15) > 1e-6]
    pts = [p for p in pts if p[0] < 15] + [(15, K.VF15_L), (15, K.VF15_R)] + [p for p in pts if p[0] > 15]
    vals = [(15, K.VF15_L, '−73/128', (-44, 18)), (15, K.VF15_R, '+55/128', (46, -4)), (40, K.VF15_C, '−1/6', 's'),
            (K.VF15_DE_MAX[0], K.VF15_DE_MAX[1], '+0.072', 'n')]
    o += il(ax, base, sy, pts, ticks=(0, 15, 30, 40, 50, 80), vals=vals, name='IL *V*_{*F*}', name_x=8)
    o += T(ax(40), base - 14, 'C 處轉折（內鉸）', 15, AC, 'middle', 'bold')
    o += T(ax(18), 392, '跳躍 55/128 + 73/128 = 1 ✔', 15, KEY, 'start', 'bold')
    return svg(W, H, o, 'SA-2015-2 V_F 影響線')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2, 'fig7_3': fig7_3, 'fig7_4': fig7_4, 'fig7_5': fig7_5}
