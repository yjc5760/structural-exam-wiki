# -*- coding: utf-8 -*-
"""SM-2025-3 圖解。所有數值由本檔依 SM-2025-3.md §3.5 的 L1 重算，非硬寫座標。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
D, Rad = math.degrees, math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")

# ── L1（§3.5，全部由考卷附圖的尺寸線判讀）────────────────────
H      = 7.0      # 牆總高（牆頂 → 底版底面）
B      = 6.0      # 底版全寬（左緣 → 牆背面）
T_BASE = 1.0      # 底版厚度
B_TOE  = 1.0      # 趾部突出
B_TOP  = 2.0      # 牆頂寬
GAM_S  = 17.0     # 背填砂土單位重
PHI    = 30.0     # 背填砂土內摩擦角
SU     = 30.0     # 基礎黏土不排水剪力強度
GAM_C  = 23.5     # 混凝土單位重

# ── L2（§4）──────────────────────────────────────────────
RUN    = B - B_TOE - B_TOP            # 牆身斜面水平投影 = 3.0（尺寸鏈閉合的關鍵）
H_STEM = H - T_BASE                   # 牆身高 = 6.0
KA     = math.tan(Rad(45 - PHI/2))**2 # 1/3
SIG_A  = KA*GAM_S*H                   # 牆底處主動土壓力 39.667
PA     = 0.5*KA*GAM_S*H**2            # 138.833
YA     = H/3.0                        # 2.333
R_SLIDE= SU*B                         # 180.0
FS     = R_SLIDE/PA                   # 1.2965
# 誤讀（H=8、B=7）作為對照
PA_BAD = 0.5*KA*GAM_S*(H+T_BASE)**2   # 181.333
R_BAD  = SU*(B+B_TOE)                 # 210.0
FS_BAD = R_BAD/PA_BAD                 # 1.1581
# 牆重（本小題不用，供 §5 對照）
A_BASE = B*T_BASE                     # 6
A_STEM = (B_TOP + (B - B_TOE))/2.0*H_STEM   # (2+5)/2*6 = 21
W_WALL = (A_BASE + A_STEM)*GAM_C            # 634.5

WALL = [(0,0), (B,0), (B,H), (B-B_TOP,H), (B_TOE,T_BASE), (0,T_BASE)]

PW, PH = 760, 700


def ground(cv, x_l, x_r):
    """基礎黏土（y<0）與背填砂土（x>B, 0<y<H）。"""
    cv.polygon([(x_l,-2.2), (x_r,-2.2), (x_r,0), (x_l,0)], "rgba(63,74,90,0.13)")
    cv.line((x_l,0), (0,0), C["muted"], 2.0)
    cv.line((B,0), (x_r,0), C["muted"], 2.0)
    cv.polygon([(B,0), (x_r,0), (x_r,H), (B,H)], "rgba(180,83,9,0.13)")
    cv.line((B,H), (x_r,H), C["muted"], 2.0)


# ══════════════════════════════════════════════════════════
# fig-1　尺寸鏈重繪：7 m 含底版、6 m 含趾部
# ══════════════════════════════════════════════════════════
def fig1():
    xmin, xmax, ymin, ymax = -3.6, 11.9, -3.9, 9.6
    L, R, T, Bm = 40, 40, 64, 122
    sx = min((PW-L-R)/(xmax-xmin), (PH-T-Bm)/(ymax-ymin))
    cv = Canvas(PW, PH, sx=sx, ox=L-xmin*sx, oy=Bm-ymin*sx, bg="#FFFFFF")
    cv.panel(title="考卷附圖的向量重繪：尺寸線到底量到哪裡",
             sub="四個標註量必須彼此閉合，這是判別讀法對錯的唯一依據")
    ground(cv, xmin+0.35, xmax-0.35)
    cv.polygon(WALL, "rgba(148,163,184,0.30)", C["member"], 2.6)
    cv.text_px(cv.X(9.9), cv.Y(H*0.80), "砂土", 14, C["accent"], weight="700")
    cv.text_px(cv.X(9.9), cv.Y(H*0.80)+21, "γ = %g kN/m³" % GAM_S, 12, C["muted"])
    cv.text_px(cv.X(9.9), cv.Y(H*0.80)+40, "φ' = %g°" % PHI, 12, C["muted"])
    cv.text_px(cv.X(9.9), cv.Y(-1.35), "黏土", 13.5, C["member"], weight="700")
    cv.text_px(cv.X(9.9), cv.Y(-1.35)+20, "S_u = %g kPa" % SU, 12.5, C["muted"])
    cv.text_px(cv.X(5.85), cv.Y(H*0.30), "混凝土", 13, C["muted"], weight="700", anchor="end")
    cv.text_px(cv.X(5.85), cv.Y(H*0.30)+19, "γ = %g kN/m³" % GAM_C, 11.5, C["muted"],
               anchor="end")

    # ── 考卷上實際標註的四個量（紅＝關鍵、灰＝次要）──
    cv.dim((-1.95, 0), (-1.95, H), "7 m", off=0, color=C["load"], size=14, label_off=-17)
    cv.text_px(cv.X(-1.95)-19, cv.Y(H/2.0)+21, "牆頂→底版底面", 11.5, C["load"])
    cv.dim((0, -2.45), (B, -2.45), "6 m", off=0, color=C["load"], size=14, label_off=16)
    cv.text_px(cv.X(B/2.0), cv.Y(-2.45)+34, "底版左緣→牆背面", 11.5, C["load"])
    cv.dim((-0.62, 0), (-0.62, T_BASE), "1 m", off=0, color=C["dim"], size=12, label_off=-13)
    cv.dim((0, T_BASE+0.50), (B_TOE, T_BASE+0.50), "1 m", off=0, color=C["dim"],
           size=12, label_off=-13)
    cv.dim((B-B_TOP, H+0.58), (B, H+0.58), "2 m", off=0, color=C["dim"], size=12, label_off=-13)

    # ── 圖上沒有標、由尺寸鏈導出的兩個量（accent 色）──
    cv.line((B_TOE, T_BASE), (B_TOE, -1.35), C["accent"], 1.3, dash="5 4")
    cv.line((B-B_TOP, H), (B-B_TOP, -1.35), C["accent"], 1.3, dash="5 4")
    cv.dim((B_TOE, -1.15), (B-B_TOP, -1.15), "3 m", off=0,
           color=C["accent"], size=12.5, label_off=-13)
    cv.text_px(cv.X(B-B_TOP)+12, cv.Y(-1.15)-1, "斜面投影（導出）",
               11.5, C["accent"], anchor="start")
    cv.line((B, T_BASE), (B+1.15, T_BASE), C["accent"], 1.3, dash="5 4")
    cv.dim((B+0.90, T_BASE), (B+0.90, H), "6 m", off=0, color=C["accent"],
           size=12.5, label_off=15)
    cv.text_px(cv.X(B+0.90)+17, cv.Y((T_BASE+H)/2.0)+20, "牆身（導出）", 11.5,
               C["accent"], anchor="start")

    rows = [("尺寸鏈閉合檢核（正確讀法）",
             "趾部 1 ＋ 斜面投影 3 ＋ 牆頂 2 ＝ 底寬 6 ✓　　牆身 6 ＋ 底版 1 ＝ 總高 7 ✓",
             C["member"]),
            ("若把 6 m 讀成「牆身底寬」（B = 7）",
             "斜面投影須為 7 − 1 − 2 ＝ 4 m，斜率變 4 : 6，與圖上 1 : 2 的斜面不符 ×",
             C["load"]),
            ("若把 7 m 讀成「牆身高」（H = 8）",
             "牆身須為 7 m，斜面變 3 : 7，同樣與圖形矛盾 ×", C["load"])]
    for i, (a, b, col) in enumerate(rows):
        y = PH - 100 + i*26
        cv.text_px(26, y, a, 12.5, col, anchor="start", weight="700")
        cv.text_px(296, y, b, 12.5, C["muted"], anchor="start")
    cv.save(os.path.join(OUT, "SM-2025-3-fig-1-geometry.svg"))


# ══════════════════════════════════════════════════════════
# fig-2　抗滑動自由體圖 ＋ 兩種讀法的 FS 對照
# ══════════════════════════════════════════════════════════
def panel_fbd():
    xmin, xmax, ymin, ymax = -2.4, 13.9, -2.4, 9.2
    L, R, T, Bm = 34, 34, 62, 96
    sx = min((PW-L-R)/(xmax-xmin), (PH-T-Bm)/(ymax-ymin))
    cv = Canvas(PW, PH, sx=sx, ox=L-xmin*sx, oy=Bm-ymin*sx, bg="#FFFFFF")
    cv.panel(title="抗滑動自由體圖（φ = 0 底面）",
             sub="牆重 W 垂直向下，但底面抗剪力與 W 無關")
    cv.polygon([(xmin+0.3,-2.0), (xmax-0.3,-2.0), (xmax-0.3,0), (xmin+0.3,0)],
               "rgba(63,74,90,0.13)")
    cv.line((xmin+0.3,0), (0,0), C["muted"], 2.0)
    cv.line((B,0), (xmax-0.3,0), C["muted"], 2.0)
    cv.polygon(WALL, "rgba(148,163,184,0.22)", C["member"], 2.4)

    # 主動土壓力三角形（比例：SIG_A 換算成 2.6 m 的繪圖寬度）
    ps = 2.1/SIG_A
    cv.polygon([(B,H), (B,0), (B+SIG_A*ps,0)], "rgba(220,38,38,0.20)", C["load"], 1.8)
    for k in range(1, 8):
        y = H*k/8.0
        cv.arrow((B + KA*GAM_S*(H-y)*ps, y), (B, y), C["load"], 1.7, 6)
    cv.text_px(cv.X(13.5), cv.Y(YA)+76, "σ_A = K_A·γ·H = %.2f kN/m²" % SIG_A,
               12.5, C["load"], anchor="end")
    cv.arrow((B+SIG_A*ps+1.3, YA), (B+0.15, YA), C["load"], 4.2, 13)
    cv.text_px(cv.X(13.5), cv.Y(YA)+34, "P_A = ½·K_A·γ·H² = %.2f kN/m" % PA,
               13.5, C["load"], anchor="end", weight="700")
    cv.text_px(cv.X(13.5), cv.Y(YA)+55, "作用點 H/3 = %.3f m" % YA,
               12, C["muted"], anchor="end")

    # 底面抗剪力
    for k in range(9):
        x = 0.3 + k*(B-0.6)/8.0
        cv.arrow((x-0.32, -0.45), (x+0.32, -0.45), C["deform"], 1.8, 6)
    cv.text_px(cv.X(B/2.0), cv.Y(-1.25),
               "τ_f = c_a = S_u = %g kPa（沿全寬 B = %g m 均勻分布）" % (SU, B),
               12.5, C["deform"], weight="700")
    cv.arrow((B+1.4, -0.80), (B+4.0, -0.80), C["deform"], 4.2, 13)
    cv.text_px(cv.X(B+2.7), cv.Y(-0.80)+20, "R = S_u·B = %.1f kN/m" % R_SLIDE,
               13.5, C["deform"], weight="700")

    # 牆重（灰色，標明不參與）
    cx = (A_BASE*(B/2.0) + (B_TOP*H_STEM)*(B-B_TOP/2.0)
          + (0.5*RUN*H_STEM)*(B_TOE+2*RUN/3.0)) / (A_BASE+A_STEM)
    cv.arrow((cx, H*0.50), (cx, H*0.50-2.0), C["muted"], 3.0, 10, dash="6 4")
    cv.text_px(cv.X(cx+0.45), cv.Y(H*0.50)-30, "W = %.1f kN/m" % W_WALL, 12.5,
               C["muted"], weight="700")
    cv.text_px(cv.X(cx+0.45), cv.Y(H*0.50)-11, "（W·tanδ = W·tan0° = 0）", 11.5, C["muted"])

    cv.text_px(PW/2, PH-58, "FS = R / P_A = %.1f / %.2f = %.3f" % (R_SLIDE, PA, FS),
               16, C["text"], weight="700")
    cv.text_px(PW/2, PH-33, "＜ 1.5，抗滑動不安全", 13, C["load"], weight="700")
    return cv


def panel_bars():
    cv = Canvas(PW, PH, sx=1, bg="#FFFFFF")
    cv.panel(title="兩種讀圖結果的差距", sub="數字都「看起來合理」，只有尺寸鏈能分辨")
    rows = [("正確讀法　H = 7 m、B = 6 m", PA, R_SLIDE, FS, True),
            ("誤讀　H = 8 m、B = 7 m", PA_BAD, R_BAD, FS_BAD, False)]
    peak = max(max(r[1], r[2]) for r in rows)
    x0, bw = 250, 330
    for i, (name, drv, res, fs, good) in enumerate(rows):
        y0 = 132 + i*250
        cv.text_px(38, y0, name, 15, C["text"] if good else C["load"],
                   anchor="start", weight="700")
        for j, (lab, val, col) in enumerate((("驅動 P_A", drv, C["load"]),
                                             ("抵抗 R", res, C["deform"]))):
            y = y0 + 46 + j*54
            cv.text_px(38, y, lab, 13, C["muted"], anchor="start")
            cv.rect_px(x0, y-17, bw, 34, "#EDF1F6", 8)
            cv.rect_px(x0, y-17, bw*val/peak, 34, col, 8)
            cv.text_px(x0 + bw*val/peak - 12, y, "%.1f" % val, 13.5, "#FFFFFF",
                       anchor="end", weight="700")
            cv.text_px(x0+bw+14, y, "kN/m", 12, C["muted"], anchor="start")
        cv.text_px(38, y0+156, "FS = %.3f" % fs, 20, C["deform"] if good else C["load"],
                   anchor="start", weight="700")
        cv.text_px(200, y0+158, "（本題正解）" if good else "（低估 %.1f%%）"
                   % (100*(1-fs/FS)), 13, C["muted"], anchor="start")
    cv.text_px(PW/2, PH-46, "誤讀使 FS 低估 %.1f%%——足以把邊界案例判成明顯不足的反向結論"
               % (100*(1-FS_BAD/FS)), 13, C["muted"])
    return cv


def fig2():
    compose([panel_fbd(), panel_bars()], cols=2,
            title="SM-2025-3　抗滑動檢核：自由體圖與讀圖敏感度",
            note="φ = 0 的黏土底面，抗滑力 R = Su × B 只跟底寬有關；"
                 "加重牆體完全無助於抗滑，只會惡化承載力。",
            path=os.path.join(OUT, "SM-2025-3-fig-2-sliding-fbd.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1(); fig2()
    print("KA=%.4f  σA=%.3f  PA=%.3f  R=%.1f  FS=%.4f" % (KA, SIG_A, PA, R_SLIDE, FS))
    print("誤讀 PA=%.3f R=%.1f FS=%.4f" % (PA_BAD, R_BAD, FS_BAD))
    print("A=%.1f m²  W=%.1f kN/m  x̄=%.3f m" % (A_BASE+A_STEM, W_WALL,
          (A_BASE*(B/2.)+(B_TOP*H_STEM)*(B-B_TOP/2.)+(0.5*RUN*H_STEM)*(B_TOE+2*RUN/3.))/(A_BASE+A_STEM)))
