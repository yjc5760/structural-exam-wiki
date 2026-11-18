# -*- coding: utf-8 -*-
"""第 3 章：數靜不定度、U(R) 拋物線、疊加柔度式、沉陷修正、貫穿範例完成、二度靜不定 2013-2、斜桿 ds。"""
from sa_draw import *  # noqa
import math
import calcs

C2, C3, CX = calcs.C2, calcs.C3, calcs.C3X
ENE = PUR
RED = '#d32f2f'


# ------------------------------------------------------------------ 共用：沿桿件畫彎矩圖
def member_bmd(p0, p1, fn, scale, side=1, c=MOM, fill='#ef9a9a', n=60, op=0.4):
    """p0→p1 桿件；fn(t) t∈[0,1] 為彎矩值；畫在桿件法向（side=+1 為 p0→p1 的左手邊，螢幕座標）。"""
    (x0, y0), (x1, y1) = p0, p1
    Lp = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / Lp, (y1 - y0) / Lp
    nx, ny = uy * side, -ux * side
    pts = []
    for i in range(n + 1):
        t = i / n
        v = fn(t) * scale
        pts.append((x0 + ux * Lp * t + nx * v, y0 + uy * Lp * t + ny * v))
    o = P(pts + [p1, p0], None, fill=fill, close=True, op=op)
    o += P(pts, c, 2.2)
    return o, pts


def deflect_pts(fixed_left_x, y0, Lpx, Mfun, Lm, EI, scale, n=120):
    """左端固定的水平梁：s 自固定端量（m），Mfun(s)；回傳 (像素點, v(L), θ(L))，v 向上為正。"""
    ds = Lm / n
    th = v = 0.0
    vs, ths = [0.0], [0.0]
    for i in range(n):
        s = (i + 0.5) * ds
        k = Mfun(s) / EI            # 正彎矩（下緣受拉）→ 向上凹 → θ 增加
        th_new = th + k * ds
        v += (th + th_new) / 2 * ds
        th = th_new
        vs.append(v); ths.append(th)
    pts = [(fixed_left_x + Lpx * i / n, y0 - scale * vs[i]) for i in range(n + 1)]
    return pts, vs[-1], ths[-1]


def _lframe(x0, y0, wb, hc, cpart='roller'):
    """SA-2014-4 型 L 形剛架：A 固定在左（牆）、AC 水平、CD 向下。回傳 (svg, C, D)。"""
    o = wall(x0, y0, 40, 'left') + L(x0, y0, x0 + wb, y0, INK, 4) + L(x0 + wb, y0, x0 + wb, y0 + hc, INK, 4)
    C_ = (x0 + wb, y0); D_ = (x0 + wb, y0 + hc)
    if cpart == 'roller':
        o += roller(D_[0], D_[1], s=9)
    o += T(x0 - 8, y0 - 24, 'A', 15, INK, 'end', 'bold') + T(C_[0] + 8, C_[1] - 8, 'C', 15, INK, 'start', 'bold')
    o += T(D_[0] + 16, D_[1] + 8, 'D', 15, INK, 'start', 'bold')
    return o, C_, D_


# ------------------------------------------------------------------ 圖 3-1 數靜不定度
def fig3_1():
    W, H = 900, 400
    o = ''
    pw = 225
    titles = ['(a) SA-2014-4', '(b) SA-2013-2', '(c) SA-2017-2', '(d) 選錯：變成機構']
    for k in range(4):
        cx = k * pw + pw / 2
        o += T(cx, 30, titles[k], 16, RED if k == 3 else INK, 'middle', 'bold')
        if k:
            o += L(k * pw, 46, k * pw, 380, GRID, 1.2)
    # (a)
    s, Cp, Dp = _lframe(40, 90, 140, 110)
    o += s
    o += A(110, 46, 110, 86, LOAD, 2.2, 9)
    o += T(pw / 2, 262, '未知：A 3 個＋D 1 個 = 4', 15, INK, 'middle')
    o += T(pw / 2, 288, '方程：3', 15, INK, 'middle')
    o += T(pw / 2, 322, '*n* = 4 − 3 = 1', 17, PUR, 'middle', 'bold')
    o += T(pw / 2, 352, '多餘力：D 的 *R*', 15, FOR, 'middle', 'bold')
    # (b) A 固定在下、AB 柱、BC 梁、C 鉸
    bx, by = pw + 50, 90
    o += L(bx, by, bx, by + 120, INK, 4) + fixed_wall(bx, by + 120, 44) + L(bx, by, bx + 130, by, INK, 4)
    o += pin(bx + 130, by)
    o += A(bx + 65, 46, bx + 65, 86, LOAD, 2.2, 9)
    o += T(bx - 26, by + 112, 'A', 15, INK, 'end', 'bold') + T(bx - 10, by - 6, 'B', 15, INK, 'end', 'bold')
    o += T(bx + 146, by - 8, 'C', 15, INK, 'start', 'bold')
    o += T(pw * 1.5, 262, '未知：A 3 個＋C 2 個 = 5', 15, INK, 'middle')
    o += T(pw * 1.5, 288, '方程：3', 15, INK, 'middle')
    o += T(pw * 1.5, 322, '*n* = 5 − 3 = 2', 17, PUR, 'middle', 'bold')
    o += T(pw * 1.5, 352, '多餘力：*C*_{x}、*C*_{y}', 15, FOR, 'middle', 'bold')
    # (c) 兩端固定＋內鉸
    x0, x1, yb = 2 * pw + 22, 3 * pw - 22, 140
    o += wall(x0, yb, 40, 'left') + wall(x1, yb, 40, 'right')
    hx = x0 + 0.4 * (x1 - x0)
    o += L(x0, yb, hx - 6, yb, INK, 4) + L(hx + 6, yb, x1, yb, INK, 4) + hinge(hx, yb)
    o += udl(x0 + 4, x1 - 4, yb - 6, 20, 8, LOAD)
    o += T(hx, yb + 28, 'c（內鉸）', 14, MUT, 'middle')
    o += T(pw * 2.5, 262, '未知：*R*_{a}、*M*_{a}、*R*_{b}、*M*_{b} = 4', 15, INK, 'middle')
    o += T(pw * 2.5, 288, '方程：2（平衡）＋1（*M*_{c} = 0）', 15, INK, 'middle')
    o += T(pw * 2.5, 322, '*n* = 4 − 3 = 1', 17, PUR, 'middle', 'bold')
    o += T(pw * 2.5, 352, '有鉸，還是靜不定', 15, FOR, 'middle', 'bold')
    # (d) 拿掉 A 的水平反力
    x0 = 3 * pw + 34
    o += L(x0, 90, x0 + 140, 90, INK, 4) + L(x0 + 140, 90, x0 + 140, 200, INK, 4) + roller(x0 + 140, 200, s=9)
    o += L(x0, 64, x0, 116, INK, 3)                       # 可上下不動、但左右可滑的「導槽」
    for yy in (70, 84, 98, 112):
        o += C(x0 - 6, yy, 3.5, '#fff', INK, 1.2)
    o += L(x0 - 11, 62, x0 - 11, 118, INK, 1.5)
    o += A(x0 + 40, 220, x0 + 110, 220, RED, 2.6, 11)
    o += A(x0 + 110, 236, x0 + 40, 236, RED, 2.6, 11)
    o += T(x0 + 75, 168, '整個滑走', 15, RED, 'middle', 'bold')
    o += T(pw * 3.5, 262, '把 A 的水平力當多餘力', 15, INK, 'middle')
    o += T(pw * 3.5, 288, '剩下的支承都不擋水平', 15, INK, 'middle')
    o += T(pw * 3.5, 322, '基本結構＝機構 ✗', 17, RED, 'middle', 'bold')
    o += T(pw * 3.5, 352, '只能拿掉「拿掉後仍站得住」的力', 14, MUT, 'middle')
    return svg(W, H, o, '數靜不定度與選多餘力')


# ------------------------------------------------------------------ 圖 3-2 U(R) 拋物線
def fig3_2():
    W, H = 900, 430
    pl = Plot(110, 50, 520, 300, 0, 12.5, 0, 15500)
    o = pl.axes([0, 2.5, 5, 6.25, 7.5, 10, 12.5], [0, 5000, 10000, 15000], '*R*（kN）', '*EI*·*U*', size=14,
                xfmt=lambda t: f(t), yfmt=lambda t: f'{int(t)}')
    U = CX['U_EI']; dU = CX['dUdR_EI']
    o += pl.curve(U, 0, 12.5, PUR, 3)
    # 切線
    for R0, c, lab, dx in ((0.0, MOM, '斜率 = −3600', 2.6), (10.0, AC, '斜率 = +2160', 1.8)):
        y0 = U(R0); s = dU(R0)
        o += L(pl.X(R0 - (0 if R0 == 0 else dx)), pl.Y(y0 - s * (0 if R0 == 0 else dx)), pl.X(R0 + dx), pl.Y(y0 + s * dx), c, 2, '7 4')
        o += pl.dot(R0, y0, c)
    o += T(pl.X(0.3), pl.Y(U(0)) - 12, '*R* = 0：斜率 = −3600', 15, MOM, 'start', 'bold')
    o += T(pl.X(10) - 6, pl.Y(U(10)) - 16, '*R* = 10：斜率 = +2160', 15, AC, 'end', 'bold')
    Rm = 6.25
    o += pl.dot(Rm, U(Rm), FOR, 6) + pl.vline(Rm, 0, U(Rm), FOR, 1.4)
    o += T(pl.X(Rm), pl.Y(U(Rm)) + 32, '谷底：斜率 = 0', 15, FOR, 'middle', 'bold')
    o += T(pl.X(Rm) + 8, pl.Y(U(Rm)) + 54, '*R* = 6.25，*EI*·*U* = 3150', 15, FOR, 'start')
    # 右側說明框
    bx = 660
    o += R(bx, 60, 228, 270, KEY2, PUR, 1.4, 10)
    lines = [('斜率 ∂*U*/∂*R*', PUR, 'bold', 16), ('= C 點沿 *R* 方向的位移', INK, None, 15), ('（種子 S4）', MUT, None, 14),
             ('', INK, None, 8), ('斜率 < 0：C 往下掉', MOM, 'bold', 15), ('（*R* 頂得不夠）', MUT, None, 14),
             ('斜率 > 0：C 被頂起', AC, 'bold', 15), ('（*R* 頂太多）', MUT, None, 14),
             ('斜率 = 0：C 不動', FOR, 'bold', 15), ('＝ 真正的 *R*', FOR, 'bold', 15)]
    yy = 92
    for s, c, wgt, sz in lines:
        if s:
            o += T(bx + 114, yy, s, sz, c, 'middle', wgt)
        yy += sz + 9 if s else 6
    o += R(110, 382, 680, 38, KEY2, PUR, 1.2, 8)
    o += T(450, 407, '*EI*·*U*(*R*) = ½(576*R*^{2} − 7200*R* + 28800)：一條開口向上的拋物線，谷底就是答案', 15, PUR, 'middle', 'bold')
    return svg(W, H, o, 'U(R) 拋物線')


# ------------------------------------------------------------------ 圖 3-3 疊加：基本結構＋R×單位力
def _cant_curve(x0, y0, Lp, vend, shape):
    """shape(t) 0..1，0 在固定端；vend 為自由端像素位移（向下為正）。"""
    return [(x0 + Lp * t, y0 + vend * shape(t)) for t in [i / 60 for i in range(61)]]


def fig3_3():
    W, H = 900, 420
    o = ''
    Lp = 220
    cols = [(30, '原結構（D 頂住 C）'), (330, '基本結構＋載重'), (630, '基本結構＋*R*×向上單位力')]
    y0 = 120
    for i, (x0, t) in enumerate(cols):
        o += T(x0 + Lp / 2 + 10, 34, t, 16, INK, 'middle', 'bold')
        o += wall(x0, y0, 44, 'left')
        o += L(x0, y0, x0 + Lp, y0, STEEL, 1.3, '5 4')
        if i < 2:
            o += A(x0 + Lp / 2, y0 - 50, x0 + Lp / 2, y0 - 4, LOAD, 2.4, 10) + T(x0 + Lp / 2 + 8, y0 - 30, '20 kN', 15, LOAD, 'start', 'bold')
    # 原結構：C 不動（示意曲線：兩端位移 0）
    pts = [(30 + Lp * t, y0 + 22 * math.sin(math.pi * t) * (1 - 0.35 * t)) for t in [i / 60 for i in range(61)]]
    o += P(pts, AC, 3)
    o += roller(30 + Lp, y0 + 4, s=8)
    o += T(30 + Lp + 14, y0 - 10, 'C', 15, INK, 'start', 'bold')
    o += T(30 + Lp / 2 + 10, y0 + 72, 'C 點位移 = 0', 15, FOR, 'middle', 'bold')
    # 基本結構＋載重：C 下垂
    sh = lambda t: (3 * t * t - t ** 3) / 2
    pts = _cant_curve(330, y0, Lp, 66, sh)
    o += P(pts, AC, 3)
    o += dim(330 + Lp + 22, y0, 330 + Lp + 22, y0 + 66, '', AC)
    o += T(330 + Lp / 2 + 10, y0 + 104, 'δ_{10} = −3600/*EI*', 16, MOM, 'middle', 'bold')
    o += T(330 + Lp / 2 + 10, y0 + 128, '（向下，第 2 章）', 14, MUT, 'middle')
    # 基本結構＋R：C 上翹
    pts = _cant_curve(630, y0, Lp, -48, sh)
    o += P(pts, AC, 3)
    o += A(630 + Lp, y0 + 2, 630 + Lp, y0 - 40, FOR, 2.4, 10) + T(630 + Lp - 8, y0 - 46, '*R*', 16, FOR, 'end', 'bold')
    o += T(630 + Lp / 2 + 10, y0 + 104, '*R*·*f*_{11} = 576*R*/*EI*', 16, FOR, 'middle', 'bold')
    o += T(630 + Lp / 2 + 10, y0 + 128, '（向上，第 2 章伏筆）', 14, MUT, 'middle')
    o += T(300, y0 + 20, '=', 30, INK, 'middle', 'bold') + T(600, y0 + 20, '+', 30, INK, 'middle', 'bold')
    o += R(110, 300, 680, 104, KEY2, PUR, 1.4, 10)
    o += T(450, 330, 'C 點總位移 = δ_{10} + *R*·*f*_{11} = 0', 17, PUR, 'middle', 'bold')
    o += T(450, 360, '−3600 + 576*R* = 0　⇒　*R* = 6.25 kN', 17, PUR, 'middle', 'bold')
    o += T(450, 388, '和 ∂*U*/∂*R* = 0 是同一條式子（∂*U*/∂*R* = δ_{10} + *R* *f*_{11}）', 15, INK, 'middle')
    return svg(W, H, o, '疊加柔度式')


# ------------------------------------------------------------------ 圖 3-4 沉陷
def fig3_4():
    W, H = 900, 400
    pl = Plot(110, 50, 500, 270, 0, 4.4, -1.5, 7)
    o = pl.axes([0, 0.576, 1, 2, 3, 3.6, 4], [0, 2, 4, 6.25], 'D 下沉 Δ（m）', '*R*（kN）', size=14,
                xfmt=lambda t: {0.576: '0.576', 3.6: '3.6'}.get(t, f(t)), yfmt=lambda t: f(t))
    fR = CX['settle']
    o += L(pl.X(0), pl.Y(0), pl.X(4.4), pl.Y(0), INK, 1.2)
    o += pl.curve(fR, 0, 3.6, FOR, 3)
    o += pl.curve(fR, 3.6, 4.4, FOR, 2, dash='6 5')
    o += pl.dot(0, 6.25, FOR) + T(pl.X(0) + 12, pl.Y(6.25) - 6, '沒沉陷：6.25', 15, FOR, 'start', 'bold')
    o += pl.dot(0.576, 5.25, AC) + pl.vline(0.576, 0, 5.25, AC, 1.2) + T(pl.X(0.576) + 12, pl.Y(5.25) - 8, '沉 0.576 m：5.25', 15, AC, 'start', 'bold')
    o += pl.dot(3.6, 0, MOM) + T(pl.X(3.6) - 6, pl.Y(0) - 16, '3.6 m：*R* = 0', 15, MOM, 'end', 'bold')
    o += T(pl.X(4.3), pl.Y(2.2), '*R* < 0：滾支承要能拉', 14, MUT, 'end')
    o += T(pl.X(4.3), pl.Y(2.2) + 20, '（實際會脫開）', 14, MUT, 'end')
    bx = 640
    o += R(bx, 56, 248, 252, KEY2, PUR, 1.4, 10)
    yy = 86
    for s, c, wgt, sz in [('多餘力方向的位移', PUR, 'bold', 16), ('不是 0，就寫已知值', PUR, 'bold', 16), ('', INK, None, 6),
                          ('∂*U*/∂*R* = δ（沿 *R* 方向）', INK, 'bold', 15), ('*R* 向上、D 下沉 Δ', INK, None, 15), ('⇒ δ = −Δ', MOM, 'bold', 15),
                          ('', INK, None, 6), ('(576*R* − 3600)/*EI* = −Δ', INK, None, 15), ('*R* = 6.25 − *EI*Δ/576', FOR, 'bold', 16)]:
        if s:
            o += T(bx + 124, yy, s, sz, c, 'middle', wgt)
        yy += sz + 10 if s else 8
    o += T(450, 372, '極限檢查：沉 3.6 m 正好等於懸臂梁自由下垂量（第 2 章），D 碰不到梁，*R* = 0 ✔', 15, INK, 'middle')
    return svg(W, H, o, '支承沉陷修正')


# ------------------------------------------------------------------ 圖 3-5 貫穿範例完成：彎矩圖＋變形
def fig3_5():
    W, H = 900, 500
    x0, Lpx = 140, 560
    o = ''
    yb = 90
    R_ = float(C3['R'])
    o += wall(x0, yb, 46, 'left') + L(x0, yb, x0 + Lpx, yb, STEEL, 1.3, '5 4')
    # 變形（s 自 A 量；M(s) = M_real(12 − s)）
    pts, vL, thL = deflect_pts(x0, yb, Lpx, lambda s: calcs.M_real(12 - s, R_), 12, 1000.0, 260)
    o += P(pts, AC, 3)
    o += roller(x0 + Lpx, yb + 4, s=8)
    o += A(x0 + Lpx / 2, yb - 56, x0 + Lpx / 2, yb - 4, LOAD, 2.4, 10) + T(x0 + Lpx / 2 + 8, yb - 34, '20 kN', 15, LOAD, 'start', 'bold')
    o += A(x0 + Lpx + 34, yb + 30, x0 + Lpx + 34, yb - 10, FOR, 2.4, 10) + T(x0 + Lpx + 42, yb + 30, '*R* = 6.25', 15, FOR, 'start', 'bold')
    o += T(x0 - 8, yb - 30, 'A', 16, INK, 'end', 'bold') + T(x0 + Lpx / 2 - 10, yb - 10, 'B', 15, INK, 'end', 'bold')
    o += T(x0 + Lpx + 4, yb - 18, 'C', 16, INK, 'start', 'bold')
    # θC 切線
    xe, ye = pts[-1]; xp, yp = pts[-14]
    ang = math.atan2(ye - yp, xe - xp)
    o += L(xe - 150 * math.cos(ang), ye - 150 * math.sin(ang), xe + 30 * math.cos(ang), ye + 30 * math.sin(ang), AC, 1.6, '6 4')
    o += T(xe - 10, yb + 112, 'θ_{C} = 90/*EI* = 0.09 rad（逆時針）', 15, AC, 'end', 'bold')
    # 彎矩圖（x 自 C 向左，畫成 A 在左）
    pl = Plot(x0, 230, Lpx, 210, -12, 0, -50, 42)
    o += bmd(pl, lambda u: calcs.M_real(-u, R_), -12, 0)
    o += T(x0 - 14, pl.Y(0) + 5, '*M*', 17, MOM, 'end', 'bold')
    o += T(pl.X(-12) + 6, pl.Y(-45) + 22, '−45（A，上緣受拉）', 15, MOM, 'start', 'bold')
    o += T(pl.X(-6), pl.Y(37.5) - 10, '+37.5（B）', 15, MOM, 'middle', 'bold')
    x0m = float(C3['x0'])
    o += pl.dot(-x0m, 0, MOM, 4) + T(pl.X(-x0m), pl.Y(0) + 26, f'反曲點 *x* = {x0m:.2f} m', 14, MOM, 'middle')
    o += T(pl.X(0) + 8, pl.Y(0) + 5, '0（C）', 15, MOM, 'start')
    o += R(150, 460, 600, 32, KEY2, PUR, 1.2, 8)
    o += T(450, 482, '*M* = 6.25*x* − 20⟨*x* − 6⟩（*x* 自 C 量）', 16, PUR, 'middle', 'bold')
    return svg(W, H, o, 'SA-2014-4 完成')


# ------------------------------------------------------------------ 圖 3-6 2013-2 兩個多餘力
def fig3_6():
    W, H = 900, 380
    o = ''
    titles = ['(a) 載重＋兩個多餘力', '(b) ∂*M*/∂*C*_{x}（*C*_{x} = 1）', '(c) ∂*M*/∂*C*_{y}（*C*_{y} = 1）']
    sc = 13.0
    for k in range(3):
        x0 = 40 + k * 300
        A_ = (x0 + 70, 290); B_ = (x0 + 70, 290 - 10 * sc); C_ = (x0 + 70 + 10 * sc, 290 - 10 * sc)
        o += T(x0 + 135, 36, titles[k], 16, INK, 'middle', 'bold')
        o += L(*A_, *B_, INK, 4) + L(*B_, *C_, INK, 4) + fixed_wall(A_[0], A_[1], 40)
        o += T(A_[0] + 12, A_[1] - 8, 'A', 15, INK, 'start', 'bold') + T(B_[0] - 10, B_[1] - 6, 'B', 15, INK, 'end', 'bold')
        o += T(C_[0] + 4, C_[1] - 14, 'C', 15, INK, 'start', 'bold')
        if k == 0:
            mx = (B_[0] + C_[0]) / 2
            o += A(mx, B_[1] - 50, mx, B_[1] - 4, LOAD, 2.4, 10) + T(mx + 8, B_[1] - 30, '20 kN', 15, LOAD, 'start', 'bold')
            o += A(C_[0] + 50, C_[1], C_[0] + 6, C_[1], FOR, 2.4, 10) + T(C_[0] + 30, C_[1] + 22, '*C*_{x}', 15, FOR, 'middle', 'bold')
            o += A(C_[0], C_[1] + 50, C_[0], C_[1] + 6, FOR, 2.4, 10) + T(C_[0] + 8, C_[1] + 52, '*C*_{y}', 15, FOR, 'start', 'bold')
            o += T(x0 + 135, 350, '每邊 10 m，*EI* 相同', 14, MUT, 'middle')
        elif k == 1:
            s, _ = member_bmd(B_, A_, lambda t: 10 * t, 4.0, side=-1, c=FOR, fill=TENM)
            o += s + T(A_[0] - 48, A_[1] - 10, '10', 15, FOR, 'end', 'bold')
            o += T((B_[0] + C_[0]) / 2, C_[1] - 14, 'BC：0', 15, FOR, 'middle', 'bold')
            o += T(x0 + 135, 350, '只有柱子有，*m* = *y*', 15, FOR, 'middle', 'bold')
        else:
            s, _ = member_bmd(C_, B_, lambda t: 10 * t, 4.0, side=-1, c=FOR, fill=TENM)
            o += s + T(B_[0] + 4, B_[1] - 48, '10', 15, FOR, 'start', 'bold')
            s2, _ = member_bmd(B_, A_, lambda t: 10, 4.0, side=-1, c=FOR, fill=TENM)
            o += s2 + T(B_[0] - 48, (A_[1] + B_[1]) / 2, '10', 15, FOR, 'end', 'bold')
            o += T(x0 + 135, 350, '梁 *m* = *x*、柱 *m* = 10', 15, FOR, 'middle', 'bold')
    return svg(W, H, o, 'SA-2013-2 兩個多餘力')


# ------------------------------------------------------------------ 圖 3-7 斜桿：ds 與 dx
def fig3_7():
    W, H = 900, 420
    o = ''
    sc = 36
    Ax, Ay = 60, 310
    Bx, By = Ax + 6 * sc, Ay
    Cx, Cy = Bx + 4.5 * sc, Ay - 6 * sc
    o += L(Ax, Ay, Bx, By, INK, 4) + L(Bx, By, Cx, Cy, INK, 4)
    o += roller(Ax, Ay + 2, s=9)
    o += wall(Cx, Cy, 44, 'right')
    o += udl(Ax + 2, Bx - 2, Ay - 4, 22, 9, LOAD, '2 kN/m')
    o += T(Ax - 12, Ay - 6, 'A', 15, INK, 'end', 'bold') + T(Bx + 4, By + 24, 'B', 15, INK, 'start', 'bold')
    o += T(Cx - 12, Cy - 18, 'C', 15, INK, 'end', 'bold')
    o += dim(Ax, Ay + 46, Bx, Ay + 46, '6 m', MUT, size=14) + dim(Bx, Ay + 46, Cx, Ay + 46, '4.5 m', MUT, size=14)
    o += dim(Cx + 36, Cy, Cx + 36, Ay, '', MUT) + T(Cx + 44, (Cy + Ay) / 2 + 5, '6 m', 14, MUT, 'start')
    # 小三角 ds、dx、dy
    t0, t1 = 0.42, 0.62
    p0 = (Bx + (Cx - Bx) * t0, By + (Cy - By) * t0); p1 = (Bx + (Cx - Bx) * t1, By + (Cy - By) * t1)
    o += L(p0[0], p0[1], p1[0], p0[1], AC, 2) + L(p1[0], p0[1], p1[0], p1[1], AC, 2) + L(p0[0], p0[1], p1[0], p1[1], PUR, 4)
    o += T((p0[0] + p1[0]) / 2, p0[1] + 22, '*dx*', 15, AC, 'middle', 'bold')
    o += T(p1[0] + 8, (p0[1] + p1[1]) / 2 + 5, '*dy*', 15, AC, 'start', 'bold')
    o += T((p0[0] + p1[0]) / 2 - 14, (p0[1] + p1[1]) / 2 - 6, '*ds*', 15, PUR, 'end', 'bold')
    bx = 520
    o += R(bx, 46, 368, 330, KEY2, PUR, 1.4, 10)
    yy = 78
    for s, c, wgt, sz in [('兩件事分開想', PUR, 'bold', 17), ('', INK, None, 6),
                          ('① 彎矩看「水平」力臂', INK, 'bold', 15), ('垂直力對切口的力臂＝水平距離', INK, None, 15),
                          ('⇒ *M* 可以直接用 *x* 寫', INK, None, 15), ('BC：*M* = *Rx* − 12(*x* − 3)', MOM, 'bold', 15), ('', INK, None, 6),
                          ('② 能量沿「桿長」累積', INK, 'bold', 15), ('*ds* = √(1 + (6/4.5)^{2}) *dx* = (5/3)*dx*', PUR, 'bold', 15),
                          ('多餘力 *R*：A 的垂直反力', FOR, 'bold', 15), ('漏了 5/3：*R* = 7.137（錯）', MOM, None, 15), ('乘上 5/3：*R* = 7.350 kN ✔', FOR, 'bold', 15)]:
        if s:
            o += T(bx + 184, yy, s, sz, c, 'middle', wgt)
        yy += sz + 10 if s else 8
    o += T(450, 408, 'SA-2008-3：A 滾支承、C 固接，以 A 的反力為多餘力；*EI* 相同可消去', 15, MUT, 'middle')
    return svg(W, H, o, '斜桿 ds 與 dx')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3, 'fig3_4': fig3_4, 'fig3_5': fig3_5,
       'fig3_6': fig3_6, 'fig3_7': fig3_7}
