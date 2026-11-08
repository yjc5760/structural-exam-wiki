"""SS-U2-1 講義所有數值的唯一來源（圖與內文都從這裡取）。

斷面以「由下往上堆疊的矩形」描述：(b, h, y_bottom)，單位 cm。
材料：理想彈塑性（無應變硬化、無殘留應力），E = 2040 tf/cm²。
執行 `python3 calcs.py` 會跑全部 assert 並印出內文用到的數字。
"""
import math

E = 2040.0
SQ2 = math.sqrt(2)


# ---------------------------------------------------------------- 斷面性質
class Sec:
    def __init__(self, blocks, Fy, name=""):
        self.b = blocks
        self.Fy = Fy
        self.name = name
        self.H = max(y + h for _, h, y in blocks)

    @property
    def A(self):
        return math.fsum(b * h for b, h, _ in self.b)

    @property
    def ena(self):  # 距底
        return math.fsum(b * h * (y + h / 2) for b, h, y in self.b) / self.A

    @property
    def I(self):
        c = self.ena
        return math.fsum(b * h ** 3 / 12 + b * h * (y + h / 2 - c) ** 2 for b, h, y in self.b)

    @property
    def S_top(self):
        return self.I / (self.H - self.ena)

    @property
    def S_bot(self):
        return self.I / self.ena

    @property
    def S_min(self):
        return min(self.S_top, self.S_bot)

    def area_below(self, yy):
        return math.fsum(b * min(max(yy - y, 0), h) for b, h, y in self.b)

    @property
    def pna(self):  # 距底，半面積法（二分）
        lo, hi = 0.0, self.H
        for _ in range(200):
            m = (lo + hi) / 2
            if self.area_below(m) < self.A / 2:
                lo = m
            else:
                hi = m
        return (lo + hi) / 2

    @property
    def Z(self):
        p = self.pna
        z = 0.0
        for b, h, y in self.b:
            lo, hi = y, y + h
            if hi <= p:
                z += b * h * (p - (y + h / 2))
            elif lo >= p:
                z += b * h * ((y + h / 2) - p)
            else:
                z += b * (p - lo) ** 2 / 2 + b * (hi - p) ** 2 / 2
        return z

    @property
    def My(self):
        return self.Fy * self.S_min

    @property
    def Mp(self):
        return self.Fy * self.Z

    @property
    def f(self):
        return self.Z / self.S_min

    # ---- 纖維法：給曲率 φ，求中性軸與彎矩（理想彈塑性）
    def _fibers(self, n=400):
        out = []
        for b, h, y in self.b:
            k = max(4, int(n * h / self.H))
            dy = h / k
            for i in range(k):
                out.append((y + (i + 0.5) * dy, b * dy))
        return out

    def moment_at(self, phi, fibers=None):
        fb = fibers or self._fibers()
        Fy = self.Fy

        lo, hi = -self.H, 2 * self.H
        # 正曲率＝頂部受壓；以壓應力為正：σ = clip(E·φ·(y − y_na), ±Fy)，二分找合力為 0 的中性軸
        def N(yna):
            return math.fsum(max(-Fy, min(Fy, E * phi * (yy - yna))) * a for yy, a in fb)
        for _ in range(80):
            m = (lo + hi) / 2
            if N(m) > 0:
                lo = m
            else:
                hi = m
        yna = (lo + hi) / 2
        M = math.fsum(max(-Fy, min(Fy, E * phi * (yy - yna))) * a * (yy - yna) for yy, a in fb)
        return yna, M

    def phi_y(self):
        """最先降伏的那一側在 M = My 時的曲率。"""
        c = max(self.ena, self.H - self.ena)
        return self.Fy / (E * c)


def rect_blocks(b, h):
    return [(b, h, 0.0)]


def H_blocks(d, bf, tw, tf):  # 雙對稱 H，cm
    return [(bf, tf, 0.0), (tw, d - 2 * tf, tf), (bf, tf, d - tf)]


# ---------------------------------------------------------------- 各題斷面
S2010 = Sec([(6, 2, 0), (2, 2, 2), (6, 2, 4), (2, 2, 6)], 4.0, "SS-2010-1")
S2023 = Sec([(30, 5, 0), (2, 100, 5), (50, 5, 105)], 2.5, "SS-2023-3")
S2005 = Sec([(2.4, 21.4, 0), (40, 2.6, 21.4)], 2.5, "SS-2005-4 T")          # 翼板在上
S2020 = Sec([(20, 2.5, 0), (1.5, 55, 2.5), (30, 2.5, 57.5)], 2.5, "SS-2020-2")
S2009 = Sec(H_blocks(50.0, 30.4, 1.5, 2.4), 3.5, "H500×304×15×24")
S2006 = Sec(H_blocks(60.0, 30.0, 1.2, 2.0), 3.5, "H600×300×12×20")
RECT = Sec(rect_blocks(10, 20), 2.5, "矩形")
S2021 = Sec(H_blocks(70.0, 30.0, 1.2, 2.5), 3.5, "BH700×300×12×25")   # 副考點 SS-2021-3
S2025 = Sec(H_blocks(70.0, 30.0, 1.3, 2.4), 3.5, "RH700×300×13×24")   # 副考點 SS-2025-3

# 圓與空心圓（解析式，以 D 為單位）
def tube(D, ratio):
    d = ratio * D
    S = math.pi * (D ** 4 - d ** 4) / (32 * D)
    Z = (D ** 3 - d ** 3) / 6
    return S, Z, Z / S

S_tube, Z_tube, f_tube = tube(1.0, 0.6)
S_circ, Z_circ, f_circ = tube(1.0, 0.0)


# ---------------------------------------------------------------- 機構法
def w_propped(x, L, Mp):
    """一端固定（x=0）一端簡支，全跨均布；跨間鉸距固定端 x。回傳 w。"""
    return 2 * Mp * (2 * L - x) / (L * x * (L - x))


X_OPT = 2 - SQ2           # x/L（距固定端）
K_PROP = 6 + 4 * SQ2      # w_u = K·Mp/L²


def propped_M(xs, w, L, MA):
    """固定端彎矩 −MA 時沿跨彎矩（x 自固定端）。"""
    RA = w * L / 2 + MA / L
    return [RA * x - w * x * x / 2 - MA for x in xs]


def propped_elastic_defl(x, w, L, EI):
    """彈性 propped cantilever（固定在 x=0）均布撓度。"""
    return w * x * x * (L - x) * (3 * L - 2 * x) / (48 * EI)


def ss_defl(x, w, L, EI):
    return w * x * (L ** 3 - 2 * L * x * x + x ** 3) / (24 * EI)


# 2005-4 數值
L05 = 600.0
wu05 = K_PROP * S2005.Mp / L05 ** 2
w1_05 = 8 * S2005.Mp / L05 ** 2          # 固定端先達 Mp（彈性 wL²/8）
we_05 = 8 * S2005.My / L05 ** 2          # 固定端最外纖維先達 Fy
xc05 = X_OPT * L05

# 2020-2 數值
L20 = 800.0
wu20 = K_PROP * S2020.Mp / L20 ** 2
xA20 = (SQ2 - 1) * L20                   # 距滾支端

# 重分配比（各結構）
REDIST = [
    # 名稱, 第一鉸 (係數), 崩塌 (係數), 單位
    ("簡支梁 均布", 8.0, 8.0, "M_p/L²"),
    ("一端固定一端簡支 均布", 8.0, K_PROP, "M_p/L²"),
    ("一端固定一端簡支 跨中集中", 16 / 3, 6.0, "M_p/L"),
    ("兩端固定 均布", 12.0, 16.0, "M_p/L²"),
]


# 空心圓管：t → 0 的極限 f → 4/π
F_THIN = 4 / math.pi

# 寬厚比（國內極限設計法：塑性設計斷面 λpd，Fy 以 tf/cm² 計；見 SS-2021-3 考卷所附、SS-2014-3 題解）
def lam_pd_flange(Fy):
    return 14 / math.sqrt(Fy)


def lam_pd_web(Fy):
    return 138 / math.sqrt(Fy)


def lam_p_flange(Fy):
    return 17 / math.sqrt(Fy)


# 固定端與跨間 Mp 不同時（AISC 360-16 F9：T 型肢受壓 Mn ≤ My）
def w_propped2(x, L, MA, MC):
    return 2 * (MA * (L - x) + MC * L) / (L * x * (L - x))


def wu_propped2(L, MA, MC, n=20000):
    return min(w_propped2(L * i / n, L, MA, MC) for i in range(1, n))


# F9：肢受拉 Mp ≤ 1.6My、肢受壓 Mn ≤ My；My = Fy·Sx，Sx 取至肢端（先降伏、較小者）
MC05_F9 = min(S2005.Mp, 1.6 * S2005.My)   # 跨間正彎矩（肢受拉）→ 1.6My 控制
MA05_F9 = S2005.My                         # 固端負彎矩（肢受壓）
X05_F9 = L05 * ((MA05_F9 + MC05_F9) - math.sqrt((MA05_F9 + MC05_F9) * MC05_F9)) / MA05_F9  # 閉合解
WU05_F9 = w_propped2(X05_F9, L05, MA05_F9, MC05_F9)


def check():
    r = lambda v, n=1: round(v, n)
    # 2010-1
    assert r(S2010.ena, 3) == 3.5 and r(S2010.I, 2) == 162.67
    assert r(S2010.My, 1) == 144.6 and r(S2010.pna, 3) == 4.0
    assert r(S2010.Z, 2) == 64.0 and r(S2010.Mp, 1) == 256.0 and r(S2010.f, 2) == 1.77
    # 2023-3
    assert r(S2023.ena, 2) == 63.75 and abs(S2023.I - 1224062.5) < 1
    assert r(S2023.S_bot, 0) == 19201 and abs(S2023.My - 48003) < 1  # 題解先把 S 四捨五入再乘
    assert r(S2023.pna, 2) == 80.0 and r(S2023.Z, 1) == 24750.0 and r(S2023.Mp, 0) == 61875
    assert r(S2023.f, 3) == 1.289
    # 2005-4
    assert r(S2005.A, 2) == 155.36
    assert r(S2005.H - S2005.pna, 3) == 1.942
    assert r(S2005.Z, 1) == 667.4 and r(S2005.Mp, 1) == 1668.6
    assert r(S2005.H - S2005.ena, 2) == 5.27 and r(S2005.I, 0) == 6970  # 題解 6969.5
    assert r(S2005.S_bot, 1) == 372.0 and r(S2005.My, 0) == 930
    assert r(wu05 * 100, 2) == 5.40 and r(xc05, 1) == 351.5
    assert r(wu05 / we_05, 2) == 2.61 and r(S2005.f, 2) == 1.79
    # 2020-2
    assert r(S2020.H - S2020.pna, 2) == 21.67 and r(S2020.H - S2020.ena, 2) == 26.54
    assert r(S2020.Z, 0) == 4624 and r(S2020.Mp, 0) == 11560
    assert r(xA20, 1) == 331.4 and r(wu20 * 100, 2) == 21.06
    # 2009-3 / 2006-3
    assert r(S2009.S_min, 0) == 3771 and r(S2009.Z, 0) == 4239 and r(S2009.f, 3) == 1.124
    assert r(S2006.Z, 1) == 4420.8 and r(S2006.Mp, 1) == 15472.8
    # tube / circle / rect
    assert r(S_tube, 4) == 0.0855 and r(Z_tube, 4) == 0.1307 and r(f_tube, 3) == 1.529
    assert r(f_circ, 3) == 1.698 and r(RECT.f, 3) == 1.5
    # 機構：最小值在 X_OPT，且數值掃描吻合
    xs = [L05 * i / 2000 for i in range(1, 2000)]
    wmin = min(w_propped(x, L05, 1.0) for x in xs)
    assert abs(wmin * L05 ** 2 - K_PROP) < 1e-3
    assert r(w_propped(L05 / 2, L05, 1.0) * L05 ** 2, 3) == 12.0
    # 下限檢核：w_u 時全跨 |M| ≤ Mp，最大正彎矩恰在 x_c
    Ms = propped_M(xs, wu05, L05, S2005.Mp)
    assert max(Ms) <= S2005.Mp * (1 + 1e-6)
    assert abs(xs[Ms.index(max(Ms))] - xc05) < 1.0
    # 彈性階段：固定端 wL²/8 為全跨最大，跨間最大 9wL²/128
    assert r(9 / 128 * 8, 4) == 0.5625
    # 管：薄管極限
    St, Zt, ft = tube(1.0, 0.999)
    assert abs(ft - F_THIN) < 2e-3
    # 寬厚比
    assert r(20 / 2.6, 2) == 7.69 and r(lam_pd_flange(2.5), 2) == 8.85 and r(lam_p_flange(2.5), 2) == 10.75
    assert r(lam_pd_web(2.5), 1) == 87.3
    # 360-16 F9 估算：M_A = My = 930.1（肢受壓）、M_C = 1.6My = 1488.2 < Mp（肢受拉）
    # 題解 2026-11-01 第二次勘誤後為 4.28 tf/m（原以翼板側 S 計 1.6My = 5293，誤）
    assert r(MC05_F9, 1) == 1488.2 and MC05_F9 < S2005.Mp
    assert r(WU05_F9 * 100, 2) == 4.28 and r(X05_F9 / L05, 4) == 0.5604
    assert abs(wu_propped2(L05, MA05_F9, MC05_F9) - WU05_F9) < 1e-7   # 數值掃描＝閉合解
    xs = [L05 * i / 4000 for i in range(1, 4000)]
    Mf9 = propped_M(xs, WU05_F9, L05, MA05_F9)
    assert abs(max(Mf9) - MC05_F9) < 1e-3 * MC05_F9                    # 下限：最大正彎矩＝M_C
    # 副考點 SS-2021-3（Sx 取考卷表一 5670）、SS-2025-3
    assert r(S2021.Z, 1) == 6330.0 and r(S2021.Mp / 100, 1) == 221.6
    assert r(S2021.Z / 5670, 3) == 1.116
    assert r(K_PROP * S2021.Mp / 1200.0 ** 2 * 100, 1) == 17.9
    assert r(S2025.Z, 1) == 6248.8 and r(S2025.Mp, 0) == 21871
    # §1.2 內文：H500×304 在 φ = 2φy 時已達約 0.98 Mp
    _, M2 = S2009.moment_at(2 * S2009.phi_y(), S2009._fibers(500))
    assert r(M2 / S2009.Mp, 2) == 0.98
    return True


if __name__ == "__main__":
    check()
    for s in (S2010, S2023, S2005, S2020, S2009, S2006):
        print(f"{s.name:16s} A={s.A:9.2f} ENA={s.ena:7.3f} PNA={s.pna:7.3f} I={s.I:11.1f} "
              f"Stop={s.S_top:9.1f} Sbot={s.S_bot:9.1f} Z={s.Z:9.1f} My={s.My:9.1f} Mp={s.Mp:9.1f} f={s.f:.3f}")
    print("tube S,Z,f", S_tube, Z_tube, f_tube, "circle f", f_circ)
    print("2005-4 we, w1, wu (tf/m):", we_05 * 100, w1_05 * 100, wu05 * 100, "ratios",
          w1_05 / we_05, wu05 / w1_05, wu05 / we_05, "xc", xc05)
    print("2020-2 wu tf/m", wu20 * 100, "xA", xA20)
    print("K", K_PROP, "wrong midspan", w_propped(300, 600, 1) * 600 ** 2)
    print("F9 wu tf/m", WU05_F9 * 100, "thin f", F_THIN)
    print("OK")
