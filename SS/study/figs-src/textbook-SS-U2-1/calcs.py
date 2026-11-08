# -*- coding: utf-8 -*-
"""SS-U2-1 塑性分析與設計｜教科書講義的所有數值（圖與內文共用）。

單位：tf、cm（F_y：tf/cm²；M：tf·cm；w：tf/cm，內文另換算 tf/m）。
考題數字取自 raw/solutions/SS-YYYY-N/SS-YYYY-N.md（勘誤後版本）。
執行 `python3 calcs.py` 印出所有數值，與內文逐一對照。
"""
import math

E = 2040.0          # tf/cm²
SQ2 = math.sqrt(2)


# ─────────────────────────── 斷面（由矩形塊組成，y 由底往上量） ───────────────────────────
class Section:
    """rects: [(名稱, b, y0, y1)]，y 由斷面底緣往上量 (cm)。"""

    def __init__(self, name, rects, Fy):
        self.name, self.rects, self.Fy = name, rects, Fy
        self.H = max(r[3] for r in rects)
        self.A = sum(b * (y1 - y0) for _, b, y0, y1 in rects)
        self.ybar = sum(b * (y1 - y0) * (y0 + y1) / 2 for _, b, y0, y1 in rects) / self.A   # ENA（距底）
        self.parts_I = []
        for nm, b, y0, y1 in rects:
            h = y1 - y0
            Ai = b * h
            d = (y0 + y1) / 2 - self.ybar
            self.parts_I.append(dict(nm=nm, A=Ai, yc=(y0 + y1) / 2, d=d, Iown=b * h ** 3 / 12, Ad2=Ai * d * d))
        self.I = sum(p['Iown'] + p['Ad2'] for p in self.parts_I)
        self.c_top, self.c_bot = self.H - self.ybar, self.ybar
        self.S_top, self.S_bot = self.I / self.c_top, self.I / self.c_bot
        self.S = min(self.S_top, self.S_bot)
        self.My = self.Fy * self.S
        self.ypna = self._pna()
        self.parts_Z = self._zparts()
        self.Z = sum(p['Q'] for p in self.parts_Z)
        self.Mp = self.Fy * self.Z
        self.f = self.Z / self.S
        # 上下半塊形心到 PNA 的距離（力偶法）
        Qt = sum(p['Q'] for p in self.parts_Z if p['side'] == 'top')
        Qb = sum(p['Q'] for p in self.parts_Z if p['side'] == 'bot')
        self.yt, self.yc_ = Qt / (self.A / 2), Qb / (self.A / 2)
        self.arm = self.yt + self.yc_

    def area_below(self, y):
        return sum(b * max(0.0, min(y, y1) - y0) for _, b, y0, y1 in self.rects)

    def _pna(self):
        lo, hi = 0.0, self.H
        for _ in range(200):
            m = (lo + hi) / 2
            if self.area_below(m) < self.A / 2:
                lo = m
            else:
                hi = m
        return (lo + hi) / 2

    def _zparts(self):
        out, yp = [], self.ypna
        for nm, b, y0, y1 in self.rects:
            for side, a, c in (('bot', y0, min(y1, yp)), ('top', max(y0, yp), y1)):
                if c - a > 1e-9:
                    Ai = b * (c - a)
                    dist = abs((a + c) / 2 - yp)
                    out.append(dict(nm=nm, side=side, A=Ai, dist=dist, Q=Ai * dist, y0=a, y1=c))
        return out

    def Z_about(self, yp):
        """（錯解對照用）對任意軸 yp 取 Σ|y−yp|dA。"""
        tot = 0.0
        for _, b, y0, y1 in self.rects:
            for a, c in ((y0, min(y1, yp)), (max(y0, yp), y1)):
                if c - a > 1e-9:
                    tot += b * (c - a) * abs((a + c) / 2 - yp)
        return tot

    def which_block_pna(self):
        for nm, b, y0, y1 in self.rects:
            if y0 - 1e-9 <= self.ypna <= y1 + 1e-9:
                return nm

    def moment_at_curvature(self, phi, n=4000):
        """彈—完全塑性材料、平面保持平面。phi 以 1/cm 計；回傳 (M, 中性軸 y)。
        非對稱斷面中性軸隨曲率移動：以 ΣF=0 二分求解。"""
        Fy = self.Fy

        def stress(y, yn):
            eps = phi * (y - yn)
            s = E * eps
            return max(-Fy, min(Fy, s))

        def integ(yn, mom=False):
            tot = 0.0
            for _, b, y0, y1 in self.rects:
                k = max(20, int(n * (y1 - y0) / self.H))
                h = (y1 - y0) / k
                for i in range(k):
                    y = y0 + (i + 0.5) * h
                    s = stress(y, yn)
                    tot += s * b * h * ((y - yn) if mom else 1.0)
            return tot

        lo, hi = 0.0, self.H
        for _ in range(60):
            m = (lo + hi) / 2
            if integ(m) > 0:     # 拉 > 壓 → 中性軸要往上
                lo = m
            else:
                hi = m
        yn = (lo + hi) / 2
        return integ(yn, True), yn

    def phi_y(self):
        """第一次降伏時的曲率：較遠的外緣達 εy。"""
        return (self.Fy / E) / max(self.c_top, self.c_bot)


# 貫穿全冊範例：SS-2020-2 非對稱 H 型（上翼 30×2.5、腹板 1.5×55、下翼 20×2.5，全深 60 cm）
S20 = Section('SS-2020-2', [('下翼板', 20.0, 0.0, 2.5), ('腹板', 1.5, 2.5, 57.5), ('上翼板', 30.0, 57.5, 60.0)], 2.5)
# SS-2023-3 非對稱 I 型（底翼 30×5、腹板 2×100、頂翼 50×5，全高 110 cm）
S23 = Section('SS-2023-3', [('底翼板', 30.0, 0.0, 5.0), ('腹板', 2.0, 5.0, 105.0), ('頂翼板', 50.0, 105.0, 110.0)], 2.5)
# SS-2010-1 階梯斷面（由下而上：6×2、2×2、6×2、2×2），SS540 F_y = 4.0
S10 = Section('SS-2010-1', [('①底 6×2', 6.0, 0.0, 2.0), ('②中 2×2', 2.0, 2.0, 4.0), ('③中上 6×2', 6.0, 4.0, 6.0), ('④頂 2×2', 2.0, 6.0, 8.0)], 4.0)
# SS-2005-4 T 型（翼板 40×2.6 在上、腹板 2.4×21.4，全深 24 cm）
S05 = Section('SS-2005-4', [('腹板', 2.4, 0.0, 21.4), ('翼板', 40.0, 21.4, 24.0)], 2.5)
# SS-2006-3 H600×300×12×20（cm：d=60, bf=30, tw=1.2, tf=2.0），F_y = 3.5
S06 = Section('SS-2006-3', [('下翼板', 30.0, 0.0, 2.0), ('腹板', 1.2, 2.0, 58.0), ('上翼板', 30.0, 58.0, 60.0)], 3.5)
# SS-2009-3 H500×304×15×24（cm：d=50, bf=30.4, tw=1.5, tf=2.4），F_y = 3.5
S09 = Section('SS-2009-3', [('下翼板', 30.4, 0.0, 2.4), ('腹板', 1.5, 2.4, 47.6), ('上翼板', 30.4, 47.6, 50.0)], 3.5)
# 矩形 b×h（形狀因子 1.5 的代表）
RECT = Section('矩形 10×20', [('矩形', 10.0, 0.0, 20.0)], 2.5)


def h_closed_Z(bf, tf, d, tw):
    hw = d - 2 * tf
    return bf * tf * (d - tf) + tw * hw ** 2 / 4


def h_closed_I(bf, tf, d, tw):
    hw = d - 2 * tf
    return (bf * d ** 3 - (bf - tw) * hw ** 3) / 12


# 圓與圓管（以 D 表示的係數）
def tube(ratio):
    """d = ratio·D。回傳 (I/D^4, S/D^3, Z/D^3, f)"""
    I = math.pi / 64 * (1 - ratio ** 4)
    S = I / 0.5
    Z = (1 - ratio ** 3) / 6
    return I, S, Z, Z / S


CIRCLE = tube(0.0)
TUBE06 = tube(0.6)          # SS-2013-1
F_CIRCLE = 16 / (3 * math.pi)


# ─────────────────────────── 崩塌載重 ───────────────────────────
COEF_SS_U = 8.0              # 簡支均佈 w_u = 8Mp/L²
COEF_FF_U = 16.0             # 兩端固定均佈
COEF_PC_P = 6.0              # 固端-簡支 跨中集中 P_u = 6Mp/L
COEF_FF_P = 8.0              # 兩端固定 跨中集中
COEF_SS_P = 4.0              # 簡支 跨中集中
X_PROP = SQ2 - 1             # 固端-簡支均佈：跨間鉸距簡支端 x/L
COEF_PC_U = 6 + 4 * SQ2      # = 2(1+√2)² = 11.657


def wu_prop(xi):
    """固端-簡支均佈：跨間鉸距『簡支端』 xi·L，回傳 w_u·L²/M_p。
    虛功：w·L·δ/2 = M_p(θ1 + 2θ2)，θ1 = δ/x、θ2 = δ/(L−x)。"""
    return 2 * (1 / xi + 2 / (1 - xi))


def wu_ss(xi):
    """簡支均佈：鉸在 xi·L，w_u·L²/M_p = 2(1/ξ + 1/(1−ξ))"""
    return 2 * (1 / xi + 1 / (1 - xi))


def wu_ff(xi):
    return 2 * (2 / xi + 2 / (1 - xi))


# 貫穿範例：SS-2020-2（L = 800 cm，A 滾支、B 固定）
L20 = 800.0
X20 = X_PROP * L20                       # 距 A（簡支）
WU20 = COEF_PC_U * S20.Mp / L20 ** 2     # tf/cm
# SS-2005-4（L = 600 cm，左固接、右鉸支）
L05 = 600.0
X05_fix = (2 - SQ2) * L05                # 距固端
WU05 = COEF_PC_U * S05.Mp / L05 ** 2


def prop_check_moment(Mp, L, w):
    """固端-簡支均佈崩塌狀態的彎矩分布（距簡支端 x）。固端 −Mp。"""
    RA = w * L / 2 - Mp / L
    return lambda x: RA * x - w * x * x / 2, RA


# 彈性：固端-簡支均佈
EL_FIX = 1 / 8          # 固端 wL²/8
EL_POS = 9 / 128        # 正彎矩最大 9wL²/128 在距簡支端 3L/8
W_FIRST_HINGE = 8.0     # 第一個鉸（固端）出現時 w = 8Mp/L²
RESERVE = COEF_PC_U / W_FIRST_HINGE     # 第一鉸 → 崩塌的儲備比


# 門型剛架（換構型示範，自訂數字：柱腳固定、等斷面 Mp、跨 L、高 h、梁中點 P、梁頂水平 H）
PF = dict(L=600.0, h=400.0)
def portal(P, H, Mp, L=PF['L'], h=PF['h']):
    beam = 4 * Mp / (P * L / 2)            # 梁機構：P·(L/2)θ = 4Mpθ → 載重倍數
    sway = 4 * Mp / (H * h)                # 側移機構：H·hθ = 4Mpθ
    comb = 6 * Mp / (H * h + P * L / 2)    # 組合：H·hθ + P(L/2)θ = 6Mpθ
    return dict(beam=beam, sway=sway, comb=comb)


PF_EX = dict(P=20.0, H=8.0, Mp=1500.0)     # tf、tf、tf·cm（自訂）


# SS-2021-3 BH700×300×12×25（cm：d=70, bf=30, tw=1.2, tf=2.5），F_y = 3.5（考卷表 S_x = 5,670）
S21 = Section('SS-2021-3', [('下翼板', 30.0, 0.0, 2.5), ('腹板', 1.2, 2.5, 67.5), ('上翼板', 30.0, 67.5, 70.0)], 3.5)
S21_TABLE_S = 5670.0
L21 = 1200.0
WU21 = COEF_PC_U * S21.Mp / L21 ** 2

# 塑性區長度（簡支梁）：|M| > M_y 的範圍
def plastic_zone_point(f):     # 跨中集中：L(1 − 1/f)
    return 1 - 1 / f
def plastic_zone_udl(f):       # 均佈：L·sqrt(1 − 1/f)
    return math.sqrt(1 - 1 / f)

# 綜合重建練習：SS-2023-3 斷面，L = 10 m
LX = 1000.0
EX_WU_PROP = COEF_PC_U * S23.Mp / LX ** 2       # 固端-簡支均佈 tf/cm
EX_P_FF = COEF_FF_P * S23.Mp / LX               # 兩端固定跨中集中 tf
EX_P_PC = COEF_PC_P * S23.Mp / LX               # 固端-簡支跨中集中 tf

# 下限示範：固端彎矩取 −Mp、均佈 w（以 Mp/L² 為單位）時跨內最大正彎矩 / Mp
def prop_span_max(wc):
    RA = wc / 2 - 1
    return RA * RA / (2 * wc), RA / wc
LB_DEMO = 11.0
UB_DEMO = [(0.3, wu_prop(0.3)), (0.5, wu_prop(0.5)), (X_PROP, COEF_PC_U)]
WRONG_MAX = prop_span_max(wu_prop(0.5))      # 鉸放跨中（w = 12）時的最大正彎矩

# 2020-2 三個載重等級（tf/m）
W20_YIELD = 8 * S20.My / L20 ** 2 * 100
W20_HINGE1 = 8 * S20.Mp / L20 ** 2 * 100
W20_COLL = WU20 * 100

# 規範
PHI_B = 0.9
ASD_LF = 1.7        # 舊 ASD 塑性設計：重力載重係數
ASD_LF_W = 1.3      # 含風力／地震


def report():
    out = []
    for s in (S20, S23, S10, S05, S06, S09, RECT):
        out.append(f'\n== {s.name}  Fy={s.Fy}')
        out.append(f'  A={s.A:.3f}  ENA(距底)={s.ybar:.3f}  距頂={s.H - s.ybar:.3f}  I={s.I:.1f}')
        for p in s.parts_I:
            out.append(f'    {p["nm"]}: A={p["A"]:.2f} yc={p["yc"]:.3f} d={p["d"]:.3f} Iown={p["Iown"]:.1f} Ad2={p["Ad2"]:.1f}')
        out.append(f'  c_top={s.c_top:.3f} c_bot={s.c_bot:.3f} S_top={s.S_top:.1f} S_bot={s.S_bot:.1f} S={s.S:.1f}  My={s.My:.1f}')
        out.append(f'  PNA(距底)={s.ypna:.4f} 距頂={s.H - s.ypna:.4f} 在 {s.which_block_pna()}  A/2={s.A / 2:.3f}')
        for p in s.parts_Z:
            out.append(f'    {p["nm"]}[{p["side"]}]: A={p["A"]:.3f} dist={p["dist"]:.4f} Q={p["Q"]:.2f}')
        ze = s.Z_about(s.ybar)
        out.append(f'  [錯解] 對 ENA 取 Σ|y|dA = {ze:.2f}（{(ze / s.Z - 1) * 100:+.1f}%）；上下面積差 = {s.A - 2 * s.area_below(s.ybar):+.2f}')
        out.append(f'  Z={s.Z:.2f}  Mp={s.Mp:.1f}  f=Z/S={s.f:.4f}  ȳt={s.yt:.3f} ȳc={s.yc_:.3f} 力臂={s.arm:.3f}  C=T={s.Fy * s.A / 2:.2f}')
    out.append(f'\nH 封閉式 Z：2006-3 {h_closed_Z(30, 2, 60, 1.2):.1f}  2009-3 {h_closed_Z(30.4, 2.4, 50, 1.5):.1f}  2020-2 若當對稱(30 翼)→不適用')
    out.append(f'H 封閉式 I：2006-3 {h_closed_I(30, 2, 60, 1.2):.1f}  2009-3 {h_closed_I(30.4, 2.4, 50, 1.5):.1f}')
    out.append(f'圓：I/D4={CIRCLE[0]:.5f} S/D3={CIRCLE[1]:.5f} Z/D3={CIRCLE[2]:.5f} f={CIRCLE[3]:.4f} (16/3π={F_CIRCLE:.4f})')
    out.append(f'圓管 d=0.6D：I/D4={TUBE06[0]:.5f} S/D3={TUBE06[1]:.5f} (=0.8704π/32={0.8704 * math.pi / 32:.5f}) Z/D3={TUBE06[2]:.5f} f={TUBE06[3]:.4f}')
    for r in (0.8, 0.9, 0.95):
        out.append(f'  圓管 d={r}D f={tube(r)[3]:.4f}')
    out.append(f'\n固端-簡支均佈：x/L(距簡支)={X_PROP:.4f} 距固端={1 - X_PROP:.4f}  係數={COEF_PC_U:.4f}  wu(0.5)={wu_prop(0.5):.3f}')
    out.append(f'  檢查：wu_ss min={wu_ss(0.5):.3f} wu_ff min={wu_ff(0.5):.3f}')
    out.append(f'SS-2020-2：Mp={S20.Mp:.1f} x={X20:.1f} wu={WU20:.5f} tf/cm = {WU20 * 100:.2f} tf/m ; 若誤放跨中 {wu_prop(0.5) * S20.Mp / L20 ** 2 * 100:.2f} tf/m')
    m, RA = prop_check_moment(S20.Mp, L20, WU20)
    out.append(f'  RA={RA:.3f}  M(x)={m(X20):.1f} (應= Mp)  M(L)={m(L20):.1f} (應= -Mp)')
    out.append(f'SS-2005-4：Mp={S05.Mp:.1f} x(距固端)={X05_fix:.1f} wu={WU05:.5f} tf/cm = {WU05 * 100:.3f} tf/m')
    m, RA = prop_check_moment(S05.Mp, L05, WU05)
    out.append(f'  RA(簡支端)={RA:.3f} 固端反力={WU05 * L05 - RA:.3f}  M(x)={m(L05 - X05_fix):.1f}')
    out.append(f'彈性 固端-簡支：第一鉸 w={W_FIRST_HINGE}Mp/L²，崩塌 {COEF_PC_U:.3f} → 儲備 {RESERVE:.3f}')
    out.append(f'  2020-2 第一降伏 w_y=8My/L² = {8 * S20.My / L20 ** 2 * 100:.2f} tf/m；第一鉸 {8 * S20.Mp / L20 ** 2 * 100:.2f} tf/m')
    out.append(f'SS-2021-3: Z={S21.Z:.1f} I={S21.I:.0f} S={S21.S:.1f} Mp={S21.Mp:.0f} f(表S)={S21.Z / S21_TABLE_S:.3f} wu={WU21 * 100:.2f} tf/m')
    out.append(f'塑性區：矩形點載 {plastic_zone_point(1.5):.3f}L 均佈 {plastic_zone_udl(1.5):.3f}L；H(1.12) 點 {plastic_zone_point(1.12):.3f}L 均 {plastic_zone_udl(1.12):.3f}L；2020-2 點 {plastic_zone_point(S20.f):.3f}L')
    out.append(f'練習(2023-3,L=10m): wu={EX_WU_PROP * 100:.2f} tf/m  P_ff={EX_P_FF:.1f}  P_pc={EX_P_PC:.2f}')
    out.append(f'下限示範 w=11: span max={prop_span_max(11)[0]:.3f}Mp at {prop_span_max(11)[1]:.3f}L ; 上限 {UB_DEMO}; 跨中錯解 max={WRONG_MAX[0]:.4f} at {WRONG_MAX[1]:.4f}')
    out.append(f'2020-2 三等級 {W20_YIELD:.2f} {W20_HINGE1:.2f} {W20_COLL:.2f}  比 {W20_HINGE1/W20_YIELD:.3f} {W20_COLL/W20_HINGE1:.3f} {W20_COLL/W20_YIELD:.3f}')
    out.append(f'門型剛架 {PF} {PF_EX}: {portal(**PF_EX)}')
    # M–φ
    for s in (RECT, S20):
        py = s.phi_y()
        vals = [(k, s.moment_at_curvature(k * py)[0] / s.My) for k in (1, 2, 3, 5, 10, 20)]
        out.append(f'M–φ {s.name}: ' + '  '.join(f'φ={k}φy:{v:.3f}' for k, v in vals) + f'  f={s.f:.3f}')
    return '\n'.join(out)


if __name__ == '__main__':
    print(report())
