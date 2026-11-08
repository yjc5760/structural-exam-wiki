# -*- coding: utf-8 -*-
"""教科書講義 SS-U2-3 設計規範對施工之要求 —— 所有數值（圖與內文共用，先算再寫）。

單位：長度 mm、溫度 °C、熱輸入 J/mm（內文寫 kJ/mm）、時間 s。

本單元全為說明題，calcs.py 的角色是：
  1. 用最簡單的物理模型（Rosenthal 點熱源）把「方向」算出來，讓圖上的曲線不是手描的；
     這些數字只代表趨勢（模型假設寫在每個函式的 docstring），不是規範值。
  2. 把規範表（施工規範 表 4.1-1、表 4.2-2）寫成資料，圖直接讀它。
  3. 貫穿全書的範例接頭（EX）的所有尺寸與判定。

執行 `python3 calcs.py` 印出全部數值，與內文逐一對照。
"""
import math

# ------------------------------------------------------------------
# 1. 熱傳模型（Rosenthal 移動點熱源，鋼材常數取 500～800°C 的代表值）
# ------------------------------------------------------------------
LAM = 0.025      # 熱傳導係數 λ，W/(mm·K)（= 25 W/m·K）
RHOC = 0.005     # 體積比熱 ρc，J/(mm³·K)
ALPHA = LAM / RHOC   # 熱擴散係數 a，mm²/s
T_MELT = 1500.0  # 熔融線（約）
ZONES = [        # 峰值溫度分區（°C）——銲接冶金的通用分界，趨勢用
    (1500, '熔融區（銲道）'),
    (1100, '粗晶區'),
    (900, '細晶區'),
    (700, '部分相變區'),
]

# 代表性「淨熱輸入」E（J/mm）——數值只代表量級
E_SAW = 3000.0    # 潛弧銲一道
E_ESW = 40000.0   # 電熱熔渣銲（箱型柱內橫隔板）一次成形，數十 kJ/mm 量級


def smaw_E(U=25.0, I=170.0, v=3.0, eta=0.8):
    """淨熱輸入 E = η·U·I / v（J/mm）。"""
    return eta * U * I / v


E_SMAW = smaw_E()        # 手銲一道：0.8 × 25 V × 170 A ÷ 3 mm/s ≈ 1.13 kJ/mm
E_SMALL = E_SMAW / 2     # 小銲腳一道（熱輸入約一半）


def t85_3d(E, T0=20.0):
    """厚板（三維散熱）的 800→500°C 冷卻時間 t8/5（s）。與板厚無關。"""
    return E / (2 * math.pi * LAM) * (1 / (500 - T0) - 1 / (800 - T0))


def t85_2d(E, d, T0=20.0):
    """薄板（二維散熱，熱只能沿板面走）的 t8/5（s）。與板厚平方成反比。"""
    return E ** 2 / (4 * math.pi * LAM * RHOC * d ** 2) * (1 / (500 - T0) ** 2 - 1 / (800 - T0) ** 2)


def t85(E, d, T0=20.0):
    """實際取兩者較大者：板薄時熱散不掉（2D 控制），板厚到某厚度之後再厚也一樣（3D 控制）。"""
    return max(t85_3d(E, T0), t85_2d(E, d, T0))


def d_trans(E, T0=20.0):
    """2D 與 3D 相等的轉換板厚（mm）。"""
    return math.sqrt(E / (2 * RHOC) * (1 / (500 - T0) + 1 / (800 - T0)))


def r_peak(E, Tp, T0=20.0):
    """厚板中，峰值溫度恰為 Tp 的位置離熱源中心的距離 r（mm）。
    Rosenthal 三維峰值溫度：Tp − T0 = (2/πe)·E/(ρc·r²)。"""
    return math.sqrt(2 / (math.pi * math.e) * E / (RHOC * (Tp - T0)))


def haz_width(E, T0=20.0):
    """熔融線（1500°C）到 700°C 線的距離 = 熱影響區寬度（mm），趨勢用。"""
    return r_peak(E, 700, T0) - r_peak(E, T_MELT, T0)


def T_at(E, r, t, T0=20.0):
    """厚板中距熱源 r 處、熱源通過後 t 秒的溫度（Rosenthal 三維）。"""
    return T0 + E / (2 * math.pi * LAM * t) * math.exp(-r ** 2 / (4 * ALPHA * t))


def t_to(E, Tx, T0=20.0, r=6.0):
    """距熱源 r 處冷到 Tx 所需時間（s）；T0 ≥ Tx 時永遠不會冷到，回傳 inf。"""
    if T0 >= Tx:
        return math.inf
    lo, hi = 0.5, 1e6
    # 先找到峰值之後
    tp = r ** 2 / (4 * ALPHA)
    lo = tp
    for _ in range(200):
        mid = (lo + hi) / 2
        if T_at(E, r, mid, T0) > Tx:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ------------------------------------------------------------------
# 2. 規範表（鋼構造建築物鋼結構施工規範，營建署版）
# ------------------------------------------------------------------
# 表 4.1-1 填角銲最小尺寸（依較厚板厚 t）
FILLET_MIN = [(6, 3), (12, 5), (19, 6), (None, 8)]   # (t 上限, w_min)；None = 19 以上


def fillet_min(t):
    for tu, w in FILLET_MIN:
        if tu is None or t <= tu:
            return w


# 表 4.2-2 最低預熱與層間溫度（°C）；None = 不需預熱（母材 < 0°C 時須先熱到 21°C）
PREHEAT_BANDS = [(3, 19), (19, 38), (38, 64), (64, 120)]
PREHEAT = {
    '甲': dict(desc='SM400、SN400 等；非低氫系手銲', T=[None, 66, 110, 150]),
    '乙': dict(desc='SM490、SN490 等；低氫系手銲、SAW、GMAW、FCAW', T=[None, 10, 66, 110]),
    '丙': dict(desc='SM570 等（高強度）；低氫系', T=[10, 66, 110, 150]),
}


def preheat(cat, t):
    for (a, b), T in zip(PREHEAT_BANDS, PREHEAT[cat]['T']):
        if t <= b:
            return T
    return PREHEAT[cat]['T'][-1]


def fillet_trend_k():
    """最小銲腳的「長相有道理」檢查：
    2D 冷卻 t8/5 ∝ E²/d²，若要求 t8/5 不低於某值 → E ∝ d；
    一道銲的熱輸入約 ∝ 銲道面積 ∝ w² → w ∝ √d。
    用表 4.1-1 前三列（各區間上緣）以最小平方擬合 w = k√t。"""
    pts = [(6, 3), (12, 5), (19, 6)]
    return sum(w * math.sqrt(t) for t, w in pts) / sum(t for t, _ in pts)


# ------------------------------------------------------------------
# 3. 碳當量（IIW 式）
# ------------------------------------------------------------------
def ceq(C, Mn, Cr=0.0, Mo=0.0, V=0.0, Ni=0.0, Cu=0.0):
    return C + Mn / 6 + (Cr + Mo + V) / 5 + (Ni + Cu) / 15


CHEM_EX = dict(C=0.16, Mn=1.45, Cr=0.03, Mo=0.01, V=0.0, Ni=0.02, Cu=0.02)   # 假設成分（示範用）

# ------------------------------------------------------------------
# 4. 貫穿全書的範例接頭
# ------------------------------------------------------------------
EX = dict(
    col='箱型柱 □550×550×50', col_t=50, col_steel='SN490C',
    beam='H600×200×11×17', bf_t=17, bw_t=11, beam_steel='SN490B',
    tab_t=12, bolt='M22（F10T）', d_b=22,
)


def example():
    d = dict(EX)
    # 第 1 章：熱循環
    d['E_smaw'] = smaw_E()
    d['t85_col'] = t85(E_SMAW, d['col_t'])          # 50 mm 柱板
    d['t85_thin'] = t85(E_SMAW, 10)                 # 10 mm 薄板對照
    d['t85_small_col'] = t85(E_SMALL, d['col_t'])   # 小銲腳銲在厚板
    d['dtr'] = d_trans(E_SMAW)
    d['haz_smaw'] = haz_width(E_SMAW)
    d['haz_esw'] = haz_width(E_ESW)
    d['haz_ratio'] = d['haz_esw'] / d['haz_smaw']
    d['r_melt'] = r_peak(E_SMAW, T_MELT)
    d['r700'] = r_peak(E_SMAW, 700)
    d['pre_col'] = preheat('乙', d['col_t'])         # 柱板 50 mm → 表 4.2-2 乙類
    d['pre_bf'] = preheat('乙', d['bf_t'])           # 梁翼 17 mm
    d['pre_col_nonlowH'] = preheat('甲', d['col_t']) # 若用非低氫系（甲類欄）
    d['wmin_tab'] = fillet_min(max(d['tab_t'], d['bw_t']))  # 剪力板 12 vs 梁腹 11 → 依較厚 12
    d['t85_col_pre'] = t85(E_SMAW, d['col_t'], d['pre_col'])
    # 第 2 章：氫有多少時間逃
    d['t100_T20'] = t_to(E_SMAW, 100, 20)
    d['t100_T66'] = t_to(E_SMAW, 100, 66)
    d['t100_ratio'] = d['t100_T66'] / d['t100_T20']
    d['ceq_ex'] = ceq(**CHEM_EX)
    return d


# ------------------------------------------------------------------
# 5. 第 3 章：銲道幾何與力流（單位 mm、MPa、kN）
# ------------------------------------------------------------------
F_EXX = 490.0     # E70 銲材
W_TAB = 6.0       # 範例剪力板填角銲腳


def throat(w):
    """等腳填角銲：最短的一刀在 45° 斜線上 = w·cos45°。"""
    return w * math.cos(math.radians(45))


def fillet_Rn(w, L, theta_deg=0.0):
    """標稱強度 0.60 F_EXX × t_e × L × (1 + 0.5 sin^1.5θ)（θ＝力與銲道軸夾角；AISC J2-5）。"""
    th = math.radians(theta_deg)
    return 0.60 * F_EXX * throat(w) * L * (1 + 0.5 * math.sin(th) ** 1.5) / 1000.0


def fillet_max(t_edge):
    return t_edge if t_edge < 6 else t_edge - 2


def end_return(w):
    return 2 * w, 4 * w


def min_len(w, intermittent=False):
    return max(4 * w, 40.0) if intermittent else 4 * w


def tearout_spacing():
    """承壓上限 2.4dtFu ＝ 撕出 1.2·Lc·t·Fu → Lc = 2d；孔間淨距 Lc = s − d_h ≈ s − d → s = 3d。"""
    return 2.4 / 1.2 + 1.0     # 以 d 為單位


# ------------------------------------------------------------------
# 6. 第 5 章：高強度螺栓（M22 F10T）
# ------------------------------------------------------------------
BOLT = dict(d=22.0, Ab=math.pi * 22 ** 2 / 4, At=303.0, Fu=1000.0, Fy=900.0, hole=23.5)
MU_A, MU_PAINT = 0.33, 0.15


def bolt_calc():
    b = dict(BOLT)
    b['T0'] = 0.70 * b['Fu'] * b['At'] / 1000           # kN
    b['T0_Ab'] = 0.70 * b['Fu'] * b['Ab'] / 1000
    b['over'] = b['T0_Ab'] / b['T0'] - 1
    b['sig_T0'] = 0.70 * b['Fu']                         # MPa
    b['ratio_y'] = b['sig_T0'] / b['Fy']
    b['slip'] = MU_A * b['T0']                           # kN／栓／剪力面
    b['slip_paint'] = MU_PAINT * b['T0']
    b['ream_max'] = b['hole'] + 2.0
    b['s_min'] = 3 * b['d']; b['s_abs'] = 8 / 3 * b['d']; b['Le'] = 1.5 * b['d']
    return b


# ------------------------------------------------------------------
# 7. 第 6 章：防蝕
# ------------------------------------------------------------------
E_ZN, E_FE = -0.76, -0.44
ZINC_RATE = [('C2 鄉間', 0.7), ('C3 都市', 2.1), ('C4 工業／沿海', 4.2), ('C5 嚴重海洋', 8.4)]  # ISO 9223 鋅腐蝕速率上限 μm/年
GALV_T = 85.0


def dew_point(T, RH):
    """Magnus 式露點（°C）。"""
    a, b = 17.62, 243.12
    g = math.log(RH / 100) + a * T / (b + T)
    return b * g / (a - g)


def rh_limit_dew3(T):
    """鋼面＝氣溫時，「鋼面需高於露點 3°C」開始不滿足的相對溼度（%）。"""
    lo, hi = 30.0, 100.0
    for _ in range(60):
        m = (lo + hi) / 2
        if dew_point(T, m) + 3 > T:
            hi = m
        else:
            lo = m
    return (lo + hi) / 2


# ------------------------------------------------------------------
# 8. 第 7 章：耐震加嚴（範例接頭）
# ------------------------------------------------------------------
def panel_tau_ratio(ratio, Fy=325.0, E=200000.0, nu=0.3, k=9.34):
    """正方形節點域 (dz=wz=b) 之彈性剪力挫屈 τcr／τy；ratio = (dz+wz)/tz → b/t = ratio/2。"""
    bt = ratio / 2
    tcr = k * math.pi ** 2 * E / (12 * (1 - nu ** 2)) / bt ** 2
    return tcr / (0.6 * Fy)


def seismic():
    d = {}
    db, bf, tf, tw = 600.0, 200.0, 17.0, 11.0
    d['dz'] = db - 2 * tf
    d['wz'] = 550.0 - 2 * 50.0
    d['tz_min'] = (d['dz'] + d['wz']) / 90
    d['tz'] = 50.0
    d['Zx'] = bf * tf * (db - tf) + tw * (db - 2 * tf) ** 2 / 4        # mm³
    d['Fy_b'] = 325.0; d['Ry'] = 1.1                                   # Ry 為假設值（示範）
    d['Mp'] = d['Fy_b'] * d['Zx'] / 1e6                                 # kN·m
    d['Mpr'] = 1.1 * d['Ry'] * d['Mp']
    d['yr_hi'] = 445 / 490.0     # SN490B Fy 上限 / Fu 下限（YR 上限 0.80 的意義對照）
    d['tau90'] = panel_tau_ratio(90)
    return d


if __name__ == '__main__':
    print('E (SMAW 公式) =', round(smaw_E(), 1), 'J/mm')
    for T0 in (20, 66, 110):
        print(f'T0={T0}: t8/5 3D = {t85_3d(E_SMAW, T0):.2f} s')
    for d in (6, 10, 16, 20, 25, 30, 40, 50):
        print(f'd={d}: t8/5 = {t85(E_SMAW, d):.2f} s (2D {t85_2d(E_SMAW, d):.2f})')
    print('d_trans =', round(d_trans(E_SMAW), 1), 'mm')
    for Tp, n in ZONES:
        print(f'r({Tp}°C) = {r_peak(E_SMAW, Tp):.2f} mm   ESW: {r_peak(E_ESW, Tp):.1f} mm')
    print('HAZ SMAW =', round(haz_width(E_SMAW), 2), ' ESW =', round(haz_width(E_ESW), 1),
          ' ratio =', round(haz_width(E_ESW) / haz_width(E_SMAW), 2), ' sqrt(E ratio)=', round(math.sqrt(E_ESW / E_SMAW), 2))
    k = fillet_trend_k()
    print('fillet trend k =', round(k, 3), [(t, round(k * math.sqrt(t), 2)) for t in (6, 12, 19, 38)])
    for cat in PREHEAT:
        print(cat, [preheat(cat, t) for t in (12, 25, 50, 80)])
    for T0 in (20, 66, 110):
        print(f'T0={T0}: time to 100°C at r=6 mm = {t_to(E_SMAW, 100, T0):.1f} s; peak T = {T_at(E_SMAW, 6, 6**2/(4*ALPHA), T0):.0f}')
    for k_, v in example().items():
        print(k_, round(v, 3) if isinstance(v, float) else v)

    print('--- ch3')
    print('te(6)=', round(throat(6), 2), ' Rn(6,100,0)=', round(fillet_Rn(6, 100), 1), ' 90°:', round(fillet_Rn(6, 100, 90), 1))
    print('end return 6:', end_return(6), ' min len', min_len(6), min_len(6, True), ' max fillet 12:', fillet_max(12), ' s/d=', tearout_spacing())
    print('--- ch5'); [print(k_, round(v, 3) if isinstance(v, float) else v) for k_, v in bolt_calc().items()]
    print('--- ch6')
    for T in (10, 20, 30): print(T, 'RH limit', round(rh_limit_dew3(T), 1), ' Td@85%', round(dew_point(T, 85), 2))
    for n, r in ZINC_RATE: print(n, r, 'life', round(GALV_T / r, 1))
    print('--- ch7'); [print(k_, round(v, 3)) for k_, v in seismic().items()]
