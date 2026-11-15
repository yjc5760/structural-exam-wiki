# -*- coding: utf-8 -*-
"""SM-2016-1 圖解。
fig-1-problem：題目圖一（覆土施工剖面圖）重繪，幾何只取自題目正本 SM-2016-1-problem.md §4 判讀清單（#3–#7、#9），不含任何解題結果。
圖二（e–log σ′ 曲線）、圖三（等時線圖）為曲線圖、表一為表格，不重繪。
用法：python gen_SM-2016-1.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
H_F  = 6.0     # #3/#9 砂質覆土 6.0 m（原地表面以上）
H_S  = 2.0     # #3 砂土 2.0 m
WT   = H_S     # #4 地下水位在砂土底＝粘土頂
H_C  = 4.0     # #3 粘土 4.0 m，下為不透水岩盤（#7）
PTS  = [("A", 1.0), ("B", 2.0), ("C", 3.0)]   # #5 粘土頂下 1、2、3 m
Z_C, Z_R = H_S, H_S + H_C   # 以原地表面為深度 0

def fig_problem():
    W, H = 900, 640
    XL, XR = 0.0, 10.0
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL - 2.2, XR + 1.9), (-(Z_R + 1.3), H_F + 0.5), 40, 40, 60, 50))
    Y = lambda d: -d            # d：原地表面以下深度；覆土在 d < 0
    for d0, d1, col in [(-H_F, 0, "rgba(180,83,9,0.10)"), (0, Z_C, "rgba(180,83,9,0.22)"),
                        (Z_C, Z_R, "rgba(63,74,90,0.22)")]:
        soil_fill(cv, XL, XR, Y(d1), Y(d0), col)
    cv.line((XL, Y(-H_F)), (XR, Y(-H_F)), C["member"], 2.6)
    cv.line((XL, Y(0)), (XR, Y(0)), C["member2"], 1.8)
    cv.line((XL, Y(Z_C)), (XR, Y(Z_C)), C["member2"], 1.8)
    cv.line((XL, Y(Z_R)), (XR, Y(Z_R)), C["member"], 2.6)
    for x in (1.0, 4.4, 7.8):        # 不透水岩盤剖線
        for k in range(4):
            cv.line((x + k * 0.35, Y(Z_R)), (x + k * 0.35 - 0.3, Y(Z_R + 0.5)), C["member"], 1.4)
    # 地下水位（粘土頂）
    wt_symbol(cv, 1.2, Y(WT), C["deform"], 0.16)
    cv.text_px(cv.X(XR) + 8, cv.Y(Y(WT)), "地下水位", 12.5, C["deform"], anchor="start", weight="700")
    # 層名與參數
    cv.text_px(cv.X(2.6), cv.Y(Y(-H_F / 2)), "砂質覆土", 13, C["text"], weight="700")
    cv.math_px(cv.X(6.2), cv.Y(Y(-H_F / 2)), "γ_{m} = 16 kN/m^{3}", 13, C["text"], anchor="start")
    cv.text_px(cv.X(XR) - 4, cv.Y(Y(0)) - 12, "原地表面", 12.5, C["muted"], anchor="end")
    cv.text_px(cv.X(2.6), cv.Y(Y(H_S / 2)), "砂土", 13, C["text"], weight="700")
    cv.math_px(cv.X(6.2), cv.Y(Y(H_S / 2)), "γ_{m} = 16 kN/m^{3}", 13, C["text"], anchor="start")
    cv.text_px(cv.X(1.6), cv.Y(Y(Z_C + 2.0)), "粘土", 13, C["text"], weight="700")
    cv.math_px(cv.X(6.2), cv.Y(Y(Z_C + 1.4)), "γ_{sat} = 17.81 kN/m^{3}", 13, C["text"], anchor="start")
    cv.math_px(cv.X(6.2), cv.Y(Y(Z_C + 2.4)), "c_{v} = 1.5 m^{2}/yr", 13, C["text"], anchor="start")
    cv.text_px(cv.X(5.0), cv.Y(Y(Z_R + 0.9)), "不透水岩盤", 13, C["text"], weight="700")
    # A、B、C 與 1.0 m 尺寸線（#5）
    xp, xd2 = 3.6, 4.6
    for name, dz in PTS:
        dot(cv, cv.X(xp), cv.Y(Y(Z_C + dz)), 5, C["text"])
        cv.text_px(cv.X(xp) - 12, cv.Y(Y(Z_C + dz)), name, 13, C["text"], anchor="end", weight="700")
        cv.line((xp + 0.15, Y(Z_C + dz)), (xd2 + 0.25, Y(Z_C + dz)), C["dim"], 0.9, dash="2 3")
    prev = 0.0
    for name, dz in PTS:
        cv.dim((xd2, Y(Z_C + dz)), (xd2, Y(Z_C + prev)), "1.0 m", 0, C["dim"], 11.5, label_off=26)
        prev = dz
    # 左側尺寸線（#3）
    xd = XL - 1.0
    cv.dim((xd, Y(0)), (xd, Y(-H_F)), "6.0 m", 0, C["dim"], 12.5, label_off=-30)
    cv.dim((xd, Y(Z_C)), (xd, Y(0)), "2.0 m", 0, C["dim"], 12.5, label_off=-30)
    cv.dim((xd, Y(Z_R)), (xd, Y(Z_C)), "4.0 m", 0, C["dim"], 12.5, label_off=-30)
    for d in (-H_F, 0, Z_C, Z_R):
        cv.line((xd - 0.25, Y(d)), (XL, Y(d)), C["dim"], 0.9, dash="2 3")
    return cv

compose([fig_problem()],
        title="SM-2016-1 題目圖一（覆土施工剖面圖）重繪",
        sub="依題目正本判讀清單；地下水位在粘土頂，粘土下為不透水岩盤（單向排水）",
        note="攔錯用：6.0 m 覆土在原地表面之上；A、B、C 由粘土頂往下各 1.0 m；岩盤不透水，粘土只能向上排水。",
        path=os.path.join(OUT, "SM-2016-1-fig-1-problem.svg"))


# ══════ fig-2：應力路徑（理想化 e–log σ'）＋ 3 年超額孔隙水壓等時線（解題圖解）══════
# ── 由 SM-2016-1 §4（一）（二）（三）解得 ──
import math
S0, E0 = 48.0, 0.900          # 表一 σ'0、e0（§4 一 Step 1 驗算 B 點 = 48 kPa）
SC = 150.0                    # 表一 σ'c
S1, E1, S2, E2 = 1536.0, 0.650, 96.0, 0.710   # 表一解壓段
CS = (E2 - E1) / math.log10(S1 / S2)          # 0.04983（§4 一 Step 3）
EC = E0 - CS * math.log10(SC / S0)            # 0.8753
DSIG = H_F * 16.0                             # 96 kPa（§4 二 Step 1）
SF = S0 + DSIG                                # 144 kPa
EF = E0 - CS * math.log10(SF / S0)
SC_M = H_C / (1 + E0) * CS * math.log10(SF / S0)   # 0.050 m
CV, T_YR = 1.5, 3.0
HDR = H_C                                     # 單向排水
TV = CV * T_YR / HDR ** 2                     # 0.28125
def u_one(z):                                 # §4（三）Step 2 級數第一項
    return 4 / math.pi * DSIG * math.sin(math.pi * z / (2 * HDR)) * math.exp(-math.pi ** 2 / 4 * TV)
U_PT = {n: u_one(dz) for n, dz in PTS}        # 23.37／43.18／56.42 kPa

def fig_elog():
    W, H = 560, 520
    cv = Canvas(W, H, bg="#FFFFFF")
    L, R, T, B = 80, 30, 40, 440
    LA, LB, EA, EB = math.log10(30), math.log10(3000), 0.60, 0.95
    X = lambda s: L + (math.log10(s) - LA) / (LB - LA) * (W - L - R)
    Y = lambda e: B - (e - EA) / (EB - EA) * (B - T)
    for s in (30, 100, 300, 1000, 3000):
        seg(cv, (X(s), T), (X(s), B), C["border"], 1.0)
        cv.text_px(X(s), B + 18, "%d" % s, 12.5, C["muted"])
    for e in (0.60, 0.70, 0.80, 0.90):
        seg(cv, (L, Y(e)), (W - R, Y(e)), C["border"], 1.0)
        cv.text_px(L - 9, Y(e), "%.2f" % e, 12.5, C["muted"], anchor="end")
    seg(cv, (L, B), (W - R, B), C["muted"], 1.9); seg(cv, (L, B), (L, T), C["muted"], 1.9)
    cv.text_px((L + W - R) / 2, B + 42, "有效應力 σ'（kPa，對數）", 13, C["text"])
    cv.text_px(L - 30, T - 18, "孔隙比 e", 13, C["text"])
    # 理想化折線（表一四點）
    curve(cv, [(X(S0), Y(E0)), (X(SC), Y(EC))], C["member2"], 2.0)
    curve(cv, [(X(SC), Y(EC)), (X(S1), Y(E1))], C["member2"], 2.0)
    curve(cv, [(X(S1), Y(E1)), (X(S2), Y(E2))], C["member2"], 2.0, dash="6 4")
    curve(cv, [(X(S0), Y(E0)), (X(SF), Y(EF))], C["deform"], 4.0)
    seg(cv, (X(SC), Y(EC)), (X(SC), B), C["accent"], 1.2, dash="4 4")
    for s, e, lab, dx, dy, anc in ((S0, E0, "σ'0 = 48，e0 = 0.900", -6, -20, "start"),
                                   (SC, EC, "σ'c = 150，ec = %.3f" % EC, 8, -18, "start"),
                                   (S1, E1, "1536，0.650", -8, 18, "end"),
                                   (S2, E2, "96，0.710（解壓）", -10, 0, "end")):
        dot(cv, X(s), Y(e), 5.5, C["text"])
        cv.text_px(X(s) + dx, Y(e) + dy, lab, 11.5, C["text"], anchor=anc, weight="700")
    dot(cv, X(SF), Y(EF), 6, C["deform"])
    tag_px(cv, X(SF) - 10, Y(EF) + 30, "σ'f = %.0f，小於 σ'c → 全在再壓段" % SF, 11.5, C["deform"], anchor="middle")
    cv.text_px(X(34), Y(0.645), "Cs = %.5f" % CS, 12, C["muted"], anchor="start", weight="700")
    cv.text_px(X(34), Y(0.625), "（解壓段斜率，再壓段同）", 11, C["muted"], anchor="start")
    cv.text_px(W / 2, 18, "(a) 表一四點連成的理想化折線", 13, C["text"], weight="700")
    return cv

def fig_iso():
    W, H = 560, 520
    cv = Canvas(W, H, bg="#FFFFFF")
    L, R, T, B = 80, 40, 60, 440
    UA, UB = 0, 110
    X = lambda u: L + (u - UA) / (UB - UA) * (W - L - R)
    Y = lambda z: T + z / H_C * (B - T)          # z：粘土頂往下
    for u in range(0, 101, 20):
        seg(cv, (X(u), T), (X(u), B), C["border"], 1.0)
        cv.text_px(X(u), B + 18, "%d" % u, 12.5, C["muted"])
    for z in range(0, 5):
        seg(cv, (L, Y(z)), (W - R, Y(z)), C["border"], 1.0)
        cv.text_px(L - 9, Y(z), "%d" % z, 12.5, C["muted"], anchor="end")
    seg(cv, (L, T), (W - R, T), C["muted"], 1.9); seg(cv, (L, T), (L, B), C["muted"], 1.9)
    cv.text_px((L + W - R) / 2, B + 42, "超額孔隙水壓 Δu（kPa）", 13, C["text"])
    cv.text_px(L - 40, T - 22, "粘土頂下 z（m）", 13, C["text"], anchor="start")
    cv.text_px(W - R, T - 10, "頂：砂（排水，Δu = 0）", 11.5, C["deform"], anchor="end", weight="700")
    seg(cv, (L, B), (W - R, B), C["member"], 2.4)
    for k in range(1, 22):                       # 不透水底剖線
        x0 = L + k * (W - L - R) / 22
        seg(cv, (x0, B), (x0 - 9, B + 9), C["member"], 1.2)
    cv.text_px(W - R, B - 12, "底：不透水岩盤（∂u/∂z = 0）", 11.5, C["member"], anchor="end", weight="700")
    seg(cv, (X(DSIG), T), (X(DSIG), B), C["muted"], 1.5, dash="7 4")
    cv.text_px(X(DSIG) - 4, T + 14, "t = 0：Δu0 = 96", 11.5, C["muted"], anchor="end", weight="700")
    zs = [H_C * j / 120 for j in range(121)]
    tv_wrong = CV * T_YR / (H_C / 2) ** 2
    curve(cv, [(X(DSIG * (1 - U_local(tv_wrong, z / (H_C / 2) if z <= H_C / 2 else (H_C - z) / (H_C / 2)))), Y(z)) for z in zs],
          C["load"], 1.8, dash="6 4")
    curve(cv, [(X(u_one(z)), Y(z)) for z in zs], C["deform"], 3.0)
    for n, dz in PTS:
        u = U_PT[n]
        dot(cv, X(u), Y(dz), 6, C["deform"])
        tag_px(cv, X(u) + 12, Y(dz), "%s：%.2f kPa" % (n, u), 12, C["deform"], anchor="start")
    cv.legend(L + 14, B - 70, [(C["deform"], "單向排水 Tv = %.5f" % TV), (C["load"], "錯：雙向排水")], size=11.5)
    cv.text_px(W / 2, 18, "(b) 加載 3 年後的等時線", 13, C["text"], weight="700")
    return cv

compose([fig_elog(), fig_iso()],
        title="圖 2　應力路徑只走再壓段；3 年後孔隙水壓由頂往下遞增",
        sub="σ'f = 48 + 96 = 144 kPa 未達 σ'c = 150 kPa；Δu = Δu0 [1 − Uz(Tv, z/Hdr)]，Hdr = 4 m",
        note="攔錯用：誤用 Cc 段會高估沉陷；誤當雙向排水（紅虛線）會把底部 C 點的水壓算成接近 0。",
        path=os.path.join(OUT, "SM-2016-1-fig-2-path-isochrone.svg"))
print("CS %.5f EC %.4f EF %.4f SC %.4f TV %.5f" % (CS, EC, EF, SC_M, TV), {k: round(v, 2) for k, v in U_PT.items()})
