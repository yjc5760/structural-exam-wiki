# -*- coding: utf-8 -*-
"""第 8 章：斜桿與非正交構架。桿長不變 → 節點只能垂直桿軸走（S6）、剛體虛功列側移方程、SA-2020-1、SA-2014-3。"""
from sa_draw import *  # noqa
import math
import calcs

D8 = calcs.ch8()


def fmt1(v, nd=1):
    return f'{float(v):.{nd}f}'.replace('-', '−')


def fixed_at(x, y, ang, w=46, c=INK):
    """斜向固定端：ang＝桿軸方向（度，螢幕座標，指向桿件內部），剖線畫在桿件的另一側。"""
    a = math.radians(ang)
    nx, ny = -math.sin(a), math.cos(a)
    tx, ty = math.cos(a), math.sin(a)
    o = L(x - nx * w / 2, y - ny * w / 2, x + nx * w / 2, y + ny * w / 2, c, 3)
    for i in range(7):
        s = -w / 2 + w * i / 6
        px, py = x + nx * s, y + ny * s
        o += L(px, py, px - tx * 8 + nx * 6, py - ty * 8 + ny * 6, c, 1)
    return o


def fig8_1():
    W, H = 900, 500
    o = T(W / 2, 32, '種子 S6：桿長不變 → 一端不動時，另一端只能「垂直桿軸」走', 17, INK, 'middle', 'bold')
    # 斜桿 DE：E 固定在右下，D 在左上（方向同 SA-2014-3：水平 √3/2、垂直 1/2）
    s = 300
    E = (420, 330)
    Dp = (E[0] - s * math.sqrt(3) / 2, E[1] - s * 0.5)
    o += L(*Dp, *E, INK, 5)
    o += fixed_at(*E, 180 + 30, 46)
    o += joint(*Dp)
    o += T(Dp[0] - 14, Dp[1] - 12, 'D', 17, INK, 'end', 'bold') + T(E[0] + 18, E[1] + 26, 'E', 17, INK, 'start', 'bold')
    # 以 E 為圓心的圓弧
    o += P(arc_pts(E[0], E[1], s, 180 + 30 - 18, 180 + 30 + 10), STEEL, 1.4, dash='5 5')
    o += T(Dp[0] - 30, Dp[1] - 92, '以 E 為圓心的圓弧', 14, MUT, 'middle')
    # 位移：水平 u、垂直 √3u
    u = 46
    tip = (Dp[0] + u, Dp[1] - u * math.sqrt(3))
    o += A(Dp[0], Dp[1], tip[0], tip[1], DEF, 3, 12)
    o += L(Dp[0], Dp[1], Dp[0] + u, Dp[1], PUR, 1.8, '4 3') + L(Dp[0] + u, Dp[1], tip[0], tip[1], PUR, 1.8, '4 3')
    o += T(Dp[0] + u / 2, Dp[1] + 24, 'Δ', 16, PUR, 'middle', 'bold')
    o += T(Dp[0] + u + 10, Dp[1] - u * 0.9, '√3Δ', 16, PUR, 'start', 'bold')
    o += T(tip[0] + 10, tip[1] - 6, '2Δ（⟂ DE）', 16, DEF, 'start', 'bold')
    # 直角記號
    a = math.radians(-30)
    q = 14
    ex, ey = math.cos(math.radians(30)), math.sin(math.radians(30))   # D→E 方向
    px, py = math.cos(math.radians(-60)), math.sin(math.radians(-60))  # 位移方向
    o += P([(Dp[0] + ex * q, Dp[1] + ey * q), (Dp[0] + ex * q + px * q, Dp[1] + ey * q + py * q), (Dp[0] + px * q, Dp[1] + py * q)], INK, 1.2)
    o += T((Dp[0] + E[0]) / 2 + 20, (Dp[1] + E[1]) / 2 + 34, '*L*', 17, INK, 'middle', italic=True)
    o += T(E[0] - 130, E[1] + 40, 'ψ_{DE} ＝ 2Δ/*L*（D 往上翹 → 順時針）', 15, DEF, 'middle', 'bold')
    # 規則框
    bx = 520
    o += R(bx, 70, 360, 400, KEY2, PUR, 1.6, 10)
    lines = [
        ('三條規則（全部來自 S6）', PUR, 16, True),
        ('', INK, 6, False),
        ('① 桿兩端的位移，', INK, 15, False),
        ('　沿桿軸的分量相等', INK, 15, True),
        ('② 一端不動 → 另一端', INK, 15, False),
        ('　只能垂直桿軸走（小位移）', INK, 15, True),
        ('③ ψ ＝ 兩端「垂直桿軸」的', INK, 15, False),
        ('　相對位移 ÷ 桿長', INK, 15, True),
        ('', INK, 6, False),
        ('位移三角形 ∽ 桿件三角形', DEF, 15, True),
        ('（轉 90°）：水平 Δ 配垂直 √3Δ', DEF, 15, False),
        ('', INK, 6, False),
        ('兩端一起平移的桿：ψ ＝ 0', TEN, 15, True),
        ('不管它斜不斜', TEN, 15, False),
    ]
    yy = 104
    for txt, c, sz, b in lines:
        if txt:
            o += T(bx + 22, yy, txt, sz, c, 'start', 'bold' if b else None)
        yy += 30 if txt else 8
    return svg(W, H, o, '桿長不變與位移三角形')


def fig8_2():
    W, H = 900, 500
    o = T(W / 2, 32, '剛體虛功：節點先當成鉸，讓每根桿件「整根」轉 δψ', 17, INK, 'middle', 'bold')
    # 一根桿件剛體轉動
    x0, y0, Lp = 110, 250, 330
    ang = 16
    a = math.radians(ang)
    x1, y1 = x0 + Lp * math.cos(a), y0 + Lp * math.sin(a)
    o += L(x0, y0, x0 + Lp, y0, STEEL, 2, '6 5')
    o += L(x0, y0, x1, y1, DEF, 5)
    o += C(x0, y0, 6, '#fff', INK, 2) + C(x1, y1, 6, '#fff', INK, 2)
    o += moment(x0, y0, 30, True) + T(x0 - 6, y0 - 42, '*M*_{ij}', 16, MOM, 'middle', 'bold')
    o += moment(x1, y1, 30, True) + T(x1 + 6, y1 - 42, '*M*_{ji}', 16, MOM, 'middle', 'bold')
    o += angle_arc(x0, y0, 150, 0, ang, PUR, 2.4) + T(x0 + 160, y0 + 30, 'δψ', 17, PUR, 'start', 'bold')
    o += T(x0 + Lp / 2, y0 + 130, '桿件不彎（剛體），只是整根轉', 15, DEF, 'middle')
    o += T(x0 + Lp / 2, y0 + 158, '端彎矩做的功 ＝ (*M*_{ij} + *M*_{ji})·δψ', 16, MOM, 'middle', 'bold')
    o += T(x0 + Lp / 2, y0 + 186, '外力做的功 ＝ *P*·（作用點沿 *P* 方向走的距離）', 16, LOAD, 'middle', 'bold')
    bx = 500
    o += R(bx, 80, 380, 340, KEY2, PUR, 1.6, 10)
    lines = [
        ('側移方程（虛功形式）', PUR, 16, True),
        ('', INK, 6, False),
        ('Σ_{桿}(*M*_{ij}+*M*_{ji})δψ_{ij} + Σ *P*·δ ＝ 0', PUR, 16, True),
        ('', INK, 6, False),
        ('● δψ_{ij}：用第 8.2 節的位移圖求', INK, 15, False),
        ('● 只給「側移」那一個自由度', INK, 15, False),
        ('　節點轉角不動 → 節點彎矩平衡不出現', INK, 14, False),
        ('● 彎矩順時針為正、δψ 順時針為正', INK, 15, False),
        ('　→ 同號才是正功', INK, 14, False),
        ('', INK, 6, False),
        ('等號右邊是 0，不是 *P*δ！', LOAD, 15, True),
        ('（SA-2014-3 題解 2026-11-04 勘誤）', LOAD, 14, False),
    ]
    yy = 112
    for txt, c, sz, b in lines:
        if txt:
            o += T(bx + 190, yy, txt, sz, c, 'middle', 'bold' if b else None)
        yy += 29 if txt else 8
    o += T(W / 2, 484, '垂直柱、柱底同高程時：δψ 全部 ＝ δΔ/*h*，外力走 *y*·δψ → 就是第 7 章的 Σ(*M*_{上}+*M*_{下}) ＝ −Σ*P*_{x}*y*', 15, MUT, 'middle')
    return svg(W, H, o, '剛體虛功列側移方程')


def fig8_3():
    W, H = 900, 600
    o = T(W / 2, 32, 'SA-2020-1：b、c 一起往下走 Δ —— 轉的是水平桿 ab，斜桿 bc 只是平移', 17, INK, 'middle', 'bold')
    s = 50
    ox, oy = 150, 120
    X = lambda x: ox + s * x
    Y = lambda y: oy - s * y
    a_, b_, c_ = (0, 0), (4, 0), (8, -3)
    dd = 0.75   # 側移示意（m）
    o += L(X(0), Y(0), X(4), Y(0), INK, 5) + L(X(4), Y(0), X(8), Y(-3), INK, 5)
    o += L(X(0), Y(0), X(4), Y(-dd), DEF, 3, '8 5') + L(X(4), Y(-dd), X(8), Y(-3 - dd), DEF, 3, '8 5')
    o += wall(X(0), Y(0), 56, 'left')
    # c：靠垂直牆的滾支承（牆在右側）
    xc, yc = X(8), Y(-3)
    o += C(xc + 9, yc, 8, '#fff', INK, 1.6)
    o += L(xc + 17, yc - 40, xc + 17, yc + 70, INK, 2.4)
    for i in range(9):
        yy = yc - 40 + 110 * i / 8
        o += L(xc + 17, yy, xc + 25, yy + 7, INK, 1)
    o += T(X(0) - 16, Y(0) + 34, 'a', 17, INK, 'end', 'bold') + T(X(4), Y(0) - 16, 'b', 17, INK, 'middle', 'bold')
    o += T(xc - 14, yc + 8, 'c', 17, INK, 'end', 'bold')
    # 載重
    mx, my = X(6), Y(-1.5)
    o += A(mx, my - 80, mx, my - 8, LOAD, 2.6, 12) + T(mx - 10, my - 60, '68 kN', 15, LOAD, 'end', 'bold')
    # 分解（法向、軸向）
    ex, ey = 4 / 5, 3 / 5                  # b→c 方向（螢幕座標：x 右、y 下）
    nx, ny = -3 / 5, 4 / 5                 # 載重在法向的分量方向
    sc = 1.3
    o += A(mx, my, mx + nx * 54.4 * sc, my + ny * 54.4 * sc, MOM, 2.4, 11)
    o += A(mx, my, mx + ex * 40.8 * sc, my + ey * 40.8 * sc, STEEL, 2.4, 11)
    o += T(mx - 50, my + 72, f'法向 {fmt1(D8["s20_Pn"])}', 15, MOM, 'end', 'bold')
    o += T(mx + 54, my + 18, f'軸向 {fmt1(D8["s20_Pa"])}', 15, MUT, 'start', 'bold')
    o += A(X(4) - 26, Y(0) + 6, X(4) - 26, Y(-dd), PUR, 1.8, 8) + T(X(4) - 34, Y(-dd / 2) + 10, 'Δ', 16, PUR, 'end', 'bold')
    o += A(xc - 30, yc + 4, xc - 30, yc + s * dd, PUR, 1.8, 8) + T(xc - 38, yc + s * dd / 2 + 6, 'Δ', 16, PUR, 'end', 'bold')
    o += T(X(2), Y(-dd) + 34, 'ψ_{ab} ＝ Δ/4', 16, DEF, 'middle', 'bold')
    o += T(X(6.4) + 14, Y(-0.9), 'ψ_{bc} ＝ 0（平移）', 16, DEF, 'start', 'bold')
    # 下方：方程與答案
    bx, by = 40, 400
    o += R(bx, by, 820, 176, '#fff', STEEL, 1.2, 8)
    lines = [
        ('● 為什麼 b 不能水平走：ab 水平、a 不動 → *u*_{b} ＝ 0；c 靠牆 → *u*_{c} ＝ 0；bc 長度不變 → *v*_{c} ＝ *v*_{b}', INK, False),
        (f'● 斜桿上的 68 kN 只取法向 {fmt1(D8["s20_Pn"])}：*M*_{{F}} ＝ ∓{fmt1(D8["s20_Pn"])}×5/8 ＝ ∓{int(D8["s20_MF"])}；c 可轉 → *M*_{{cb}} ＝ 0', INK, False),
        (f'● 虛功：(*M*_{{ab}}+*M*_{{ba}})·δΔ/4 + 68·δΔ ＝ 0 → *M*_{{ab}} + *M*_{{ba}} ＝ {fmt1(D8["s20_vw"], 0)}（68 隨 bc 平移下降 δΔ）', PUR, True),
        (f'● 解：*EI*θ_{{b}} ＝ {int(D8["s20_t"])}、*EI*θ_{{c}} ＝ {fmt1(D8["s20_s"])}、*EI*Δ ＝ 2408/3 → *M*_{{ab}} ＝ {fmt1(D8["s20_Mab"], 0)}、*M*_{{ba}} ＝ {fmt1(D8["s20_Mba"], 0)} kN·m', MOM, True),
        (f'● c 點反力（水平）：對 a 取矩 191 + 3*C*_{{x}} − 68×6 ＝ 0 → *C*_{{x}} ＝ 217/3 ≈ {fmt1(D8["s20_Cx"], 2)} kN', TEN, True),
    ]
    for i, (txt, c, b) in enumerate(lines):
        o += T(bx + 16, by + 30 + i * 33, txt, 15, c, 'start', 'bold' if b else None)
    return svg(W, H, o, 'SA-2020-1 運動學')


def fig8_4():
    W, H = 900, 560
    o = T(W / 2, 30, 'SA-2014-3：B 右移 Δ → D 沿垂直 DE 方向走 2Δ → 四根桿的 ψ ＝ −1：+1：−2：+2', 17, INK, 'middle', 'bold')
    s = 24
    r3 = math.sqrt(3)
    ox, oy = 110, 290
    X = lambda x: ox + s * x
    Y = lambda y: oy - s * y
    Lm = 8
    A_, B_, C_ = (0, Lm), (0, 0), (0, -Lm)
    D_ = (r3 / 2 * Lm, 0)
    E_ = (r3 * Lm, -Lm / 2)
    for p, q in ((A_, B_), (B_, C_), (B_, D_), (D_, E_)):
        o += L(X(p[0]), Y(p[1]), X(q[0]), Y(q[1]), INK, 5)
    o += fixed_wall(X(0), Y(Lm), 46, top=True) + fixed_wall(X(0), Y(-Lm), 46)
    o += fixed_at(X(E_[0]), Y(E_[1]), 180 + 30, 46)
    # 變形（剛體位移示意，放大）
    dd = 1.6
    Bn = (dd, 0)
    Dn = (D_[0] + dd, r3 * dd)
    for p, q in ((A_, Bn), (Bn, C_), (Bn, Dn), (Dn, E_)):
        o += L(X(p[0]), Y(p[1]), X(q[0]), Y(q[1]), DEF, 2.6, '8 5')
    o += A(X(0), Y(0), X(dd), Y(0), PUR, 2.2, 10)
    o += A(X(D_[0]), Y(0), X(Dn[0]), Y(Dn[1]), PUR, 2.2, 10)
    o += T(X(0) - 14, Y(Lm) + 26, 'A', 17, INK, 'end', 'bold') + T(X(0) - 12, Y(0) - 14, 'B', 17, INK, 'end', 'bold')
    o += T(X(0) - 14, Y(-Lm) - 12, 'C', 17, INK, 'end', 'bold')
    o += T(X(D_[0]) - 6, Y(0) + 28, 'D', 17, INK, 'middle', 'bold') + T(X(E_[0]) + 20, Y(E_[1]) + 30, 'E', 17, INK, 'start', 'bold')
    o += A(X(0) - 90, Y(0), X(0) - 8, Y(0), LOAD, 2.6, 12) + T(X(0) - 56, Y(0) + 24, '66 kN', 15, LOAD, 'middle', 'bold')
    o += T(X(dd) + 12, Y(Lm / 2), 'ψ_{AB} ＝ −*R*', 15, DEF, 'start', 'bold')
    o += T(X(dd) + 10, Y(-Lm / 2), 'ψ_{BC} ＝ +*R*', 15, DEF, 'start', 'bold')
    o += T(X(D_[0] / 2) + 10, Y(0) + 26, 'ψ_{BD} ＝ −2*R*', 15, DEF, 'middle', 'bold')
    o += T(X((D_[0] + E_[0]) / 2) - 10, Y(-2) + 30, 'ψ_{DE} ＝ +2*R*', 15, DEF, 'end', 'bold')
    o += T(X(Dn[0]) + 8, Y(Dn[1]) - 6, '√3Δ↑', 15, PUR, 'start', 'bold')
    o += T(X(0) + 40, Y(Lm) + 18, '*R* ＝ Δ/*L*（*L* ＝ 8 m）', 15, PUR, 'start', 'bold')
    bx = 560
    o += R(bx, 54, 320, 494, '#fff', STEEL, 1.2, 9)
    f2 = lambda k: fmt1(D8[k], 2)
    lines = [
        ('*K* ＝ *EI*/*L*；勁度倍數 2、2、2、1', INK, 15, False),
        ('（BD：√3*I* ÷ (√3*L*/2) ＝ 2*I*/*L*）', MUT, 14, False),
        ('', INK, 6, False),
        ('虛功（B 右移 *L*δ*R*）：', INK, 15, False),
        ('*PL* − (*M*_{AB}+*M*_{BA}) + (*M*_{BC}+*M*_{CB})', PUR, 15, True),
        ('　− 2(*M*_{BD}+*M*_{DB}) + 2(*M*_{DE}+*M*_{ED}) ＝ 0', PUR, 15, True),
        ('', INK, 6, False),
        ('θ_{B} ＝ −15*R*/17、θ_{D} ＝ −12*R*/17', INK, 15, False),
        ('*KR* ＝ 374/115 ≈ 3.252', INK, 15, False),
        ('', INK, 6, False),
        (f'*M*_{{AB}} ＝ +{f2("s14_MAB")}　*M*_{{BA}} ＝ +{f2("s14_MBA")}', MOM, 15, True),
        (f'*M*_{{BC}} ＝ {f2("s14_MBC")}　*M*_{{CB}} ＝ {f2("s14_MCB")}', MOM, 15, True),
        (f'*M*_{{BD}} ＝ +{f2("s14_MBD")}　*M*_{{DB}} ＝ +{f2("s14_MDB")}', MOM, 15, True),
        (f'*M*_{{DE}} ＝ {f2("s14_MDE")}　*M*_{{ED}} ＝ {f2("s14_MED")}', MOM, 15, True),
        ('', INK, 6, False),
        (f'水平力：上柱 {fmt1(D8["s14_VAB"], 2)}＋下柱 {fmt1(D8["s14_VBC"], 2)}', TEN, 15, False),
        (f'＋BD–DE 路徑 {fmt1(D8["s14_rest"], 2)} ＝ 66 ✔', TEN, 15, True),
    ]
    yy = 84
    for txt, c, sz, b in lines:
        if txt:
            o += T(bx + 14, yy, txt, sz, c, 'start', 'bold' if b else None)
        yy += 29 if txt else 8
    return svg(W, H, o, 'SA-2014-3 位移圖')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2, 'fig8_3': fig8_3, 'fig8_4': fig8_4}
