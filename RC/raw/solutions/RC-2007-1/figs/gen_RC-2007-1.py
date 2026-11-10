#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2007-1 單筋 T 形梁設計・D29 排列與有效深度回饋 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2007-1.md §1 給定的原始資料；b、a、As、根數、s、d_actual、
     φMn 一律由下方函式現算，檔尾對 §4／§5 公佈值 assert。
  2. 改 §1 任一數字（L、b_w、h、M_D、M_L）重跑，三張圖全部跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

FIGURES
  fig-1-flange-width  有效翼板寬三條件   攔：三條件取錯（取大或漏一條）
  fig-2-bar-layout    單排✗ / 兩排✓      攔：拿題給 d = 53.5 直接交卷
  fig-3-sensitivity   層間淨距敏感度     攔：只算一個假設就宣告「夠了」
"""
import sys, os, math

sys.path.insert(0, os.environ.get(
    "STRUCTDRAW_DIR", "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose                       # noqa: E402
from recipes import bar_compare                                  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2007-1"

# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
HF     = 12.0      # 版厚（翼板）cm
BW     = 30.0      # 梁腹寬 cm
HH     = 60.0      # 梁全深 cm
D_GIV  = 53.5      # 題目假定有效深度 cm
L      = 600.0     # 跨距 = 梁間距 cm
MD     = 12.0      # tf·m
ML     = 35.0      # tf·m
FC     = 280.0
FY     = 4200.0
AB     = 6.469     # D29 單根面積 cm^2
COVER  = 4.0       # 側保護層
D_STIR = 1.0       # D10 箍筋
EPS_CU = 0.003
PHI    = 0.90      # 題目給定：拉力控制時 φ = 0.9

B1    = 0.85 if FC <= 280 else max(0.65, 0.85 - 0.05 * (FC - 280) / 70)
DB    = math.sqrt(4 * AB / math.pi)              # D29 直徑
S_REQ = max(DB, 2.5)                             # 最小淨間距
INNER = BW - 2 * (COVER + D_STIR)                # 可用橫向淨寬

# ── Step 1～3：Mu → 有效翼板寬 → a、As ────────────────────
MU    = 1.2 * MD + 1.6 * ML                      # tf·m
CANDS = [("L/4", L / 4), ("b_w + 16h_f", BW + 16 * HF), ("梁間距", L)]
BEFF  = min(v for _, v in CANDS)
MN_REQ = MU * 1e5 / PHI
# 0.85f'c·b·a(d − a/2) = Mn_req → 解 a（取小根）
qa, qb, qc = -0.5 * 0.85 * FC * BEFF, 0.85 * FC * BEFF * D_GIV, -MN_REQ
A_REQ = (-qb + math.sqrt(qb * qb - 4 * qa * qc)) / (2 * qa)
AS_REQ = 0.85 * FC * A_REQ * BEFF / FY
C_REQ  = A_REQ / B1
ET_REQ = EPS_CU * (D_GIV - C_REQ) / C_REQ

N_BAR  = math.ceil(AS_REQ / AB)
AS_PRO = N_BAR * AB


def s_clear(n):
    return (INNER - n * DB) / (n - 1)


def d_actual(rows, gap):
    """rows = 各排根數（由底排起算）；gap = 層間淨距 (cm)。"""
    y0 = COVER + D_STIR + DB / 2
    ys = [y0 + k * (DB + gap) for k in range(len(rows))]
    ybar = sum(n * y for n, y in zip(rows, ys)) / sum(rows)
    return HH - ybar, ys, ybar


def phiMn(As, d):
    a = As * FY / (0.85 * FC * BEFF)
    return PHI * As * FY * (d - a / 2) / 1e5, a


GAP_MAIN = DB                                     # 本解取層間淨距 = d_b
ROWS     = [3, 3]
D_ACT, YS, YBAR = d_actual(ROWS, GAP_MAIN)
PMN, A_ACT = phiMn(AS_PRO, D_ACT)
C_ACT  = A_ACT / B1
ET_ACT = EPS_CU * (D_ACT - C_ACT) / C_ACT

# ══════════════════════════════════════════════════════════
# 圖 1　有效翼板寬三條件
# ══════════════════════════════════════════════════════════
cases = []
for name, v in CANDS:
    col = C["bmd"] if abs(v - BEFF) < 1e-9 else C["muted"]
    tag = "　← 三者取最小，本項控制" if abs(v - BEFF) < 1e-9 else ""
    cases.append((name, {"L/4": f"L = {L:.0f} cm",
                         "b_w + 16h_f": f"b_w = {BW:.0f}，h_f = {HF:.0f} cm",
                         "梁間距": "與跨距同為 6 m"}[name] + tag,
                  v, f"{v:.0f} cm", col))
bar_compare(cases,
            title=f"{TAG}　T 形梁有效翼板寬：三條件取「最小」，不是取最大",
            sub=f"b_e = min(L/4, b_w+16h_f, 梁間距) = {BEFF:.0f} cm",
            note=(f"取錯成 {max(v for _,v in CANDS):.0f} cm 會讓 a 從 {A_REQ:.2f} cm "
                  f"掉到 {0.85*FC*A_REQ*BEFF/(0.85*FC*L):.2f} cm，整題的翼板判斷全部失真"),
            path=f"{OUT}/{TAG}-fig-1-flange-width.svg")

# ══════════════════════════════════════════════════════════
# 圖 2　單排放不下 → 兩排 → d 下降
# ══════════════════════════════════════════════════════════
PW, PH = 520, 560
sc = min((PW - 215) / (BW + 44), (PH - 250) / HH)   # +44 = 兩側翼板示意寬


def sect_panel(rows, gap, title, ok):
    d, ys, ybar = d_actual(rows, gap)
    cv = Canvas(PW, PH, sx=sc, ox=PW / 2, oy=PH - 128 - HH * sc)
    cv.panel(title, f"每排淨間距 s = {s_clear(rows[0]):.2f} cm")
    # 腹板 + 翼板（只畫腹板寬度範圍與版厚示意）
    cv.polygon([(-BW / 2, 0), (BW / 2, 0), (BW / 2, HH - HF), (BW / 2 + 22, HH - HF),
                (BW / 2 + 22, HH), (-BW / 2 - 22, HH), (-BW / 2 - 22, HH - HF),
                (-BW / 2, HH - HF), (-BW / 2, 0)], "#EDF1F6", C["member"], 2.6)
    cv.poly([(-BW / 2 + COVER, COVER), (BW / 2 - COVER, COVER),
             (BW / 2 - COVER, HH - COVER), (-BW / 2 + COVER, HH - COVER),
             (-BW / 2 + COVER, COVER)], C["member2"], 1.6, dash="5 4")
    col = C["bmd"] if ok else C["load"]
    for k, n in enumerate(rows):
        xs = ([0.0] if n == 1 else
              [-INNER / 2 + DB / 2 + i * (INNER - DB) / (n - 1) for i in range(n)])
        for x in xs:
            cv.circle((x, ys[k]), DB / 2, fill="rgba(192,57,43,0.18)",
                      stroke=C["tension"], w=2.2)
    cv.dim((-BW / 2, 0), (BW / 2, 0), f"b_{{w}}={BW:.0f}", off=34, label_off=14)
    cv.dim((-BW / 2 - 22, HH), (-BW / 2 - 22, 0), f"h={HH:.0f}", off=40, label_off=13)
    cv.line((-BW / 2 - 22, ybar), (BW / 2 + 22, ybar), C["tension"], 1.6, dash="6 4")
    cv.dim((BW / 2 + 22, HH), (BW / 2 + 22, HH - d), f"d={d:.2f}", off=-40, label_off=-13)
    cv.text_px(PW / 2, PH - 96,
               f"s = {s_clear(rows[0]):.2f} cm  "
               + ("大於" if ok else "小於")
               + f"  max(d_b, 2.5) = {S_REQ:.2f} cm  " + ("✓" if ok else "×"),
               13.5, col, weight="700")
    if ok:
        cv.text_px(PW / 2, PH - 72, f"層間淨距取 d_{{b}} = {gap:.2f} cm，"
                                    f"鋼筋形心 {ybar:.2f} cm", 12, C["muted"])
        pm, _ = phiMn(AS_PRO, d)
        cv.text_px(PW / 2, PH - 46, f"φM_{{n}} = {pm:.2f} tf·m  大於  M_{{u}} = {MU:.1f} tf·m ✓",
                   14, col, weight="700")
    else:
        cv.text_px(PW / 2, PH - 72, "單排排不下，必須改兩排", 12.5, col, weight="700")
        cv.text_px(PW / 2, PH - 46, f"（若勉強單排，d 會是 {HH - ys[0]:.2f} cm）",
                   12, C["muted"])
    return cv


compose([sect_panel([N_BAR], GAP_MAIN, f"單排 {N_BAR} 根 D29", False),
         sect_panel(ROWS, GAP_MAIN, f"兩排 {ROWS[0]}+{ROWS[1]} 根 D29", True)],
        title=f"{TAG}　放兩排之後，有效深度不再是題目給的 53.5 cm",
        sub=(f"需求 A_s = {AS_REQ:.1f} cm² → {N_BAR}-D29（A_s,prov = {AS_PRO:.2f} cm²）；"
             f"箍筋內淨寬 {INNER:.0f} cm"),
        note=(f"題給 d = {D_GIV:.1f} cm 是「假設單排」的估算起點；"
              f"實際兩排後 d = {D_ACT:.2f} cm，必須拿它重驗一次 φMn"),
        path=f"{OUT}/{TAG}-fig-2-bar-layout.svg")

# ══════════════════════════════════════════════════════════
# 圖 3　層間淨距假設的敏感度
# ══════════════════════════════════════════════════════════
W3, H3 = 840, 530
L_, R_, T_, B_ = 100, 178, 96, 128
pw, ph = W3 - L_ - R_, H3 - T_ - B_
asp = ph / pw
G0, G1 = 2.2, 5.0                                 # 層間淨距範圍 (cm)
Y0, Y1 = 69.2, 71.8                               # φMn 範圍 (tf·m)
cv = Canvas(W3, H3, sx=pw, ox=L_, oy=B_)


def P(g, y): return ((g - G0) / (G1 - G0), (y - Y0) / (Y1 - Y0) * asp)


cv.panel("φM_n 對「層間淨距」假設有多敏感？", "本題餘裕只有 0.9%")

# 不足區底色
cv.polygon([P(G0, Y0), P(G1, Y0), P(G1, MU), P(G0, MU)], "rgba(192,57,43,0.10)")
for y in (69.5, 70.0, 70.5, 71.0, 71.5):
    cv.line(P(G0, y), P(G1, y), C["border"], 1.0)
    cv.math_px(cv.X(P(G0, y)[0]) - 10, cv.Y(P(G0, y)[1]), f"{y:.1f}", 12.5, C["muted"], "end")
for g in (2.5, 3.0, 3.5, 4.0, 4.5, 5.0):
    cv.line(P(g, Y0), (P(g, Y0)[0], P(g, Y0)[1] - 7 / pw), C["muted"], 1.4)
    cv.math_px(cv.X(P(g, Y0)[0]), cv.Y(P(g, Y0)[1]) + 22, f"{g:.1f}", 12, C["muted"])
cv.line(P(G0, Y0), P(G1, Y0), C["muted"], 1.8)
cv.line(P(G0, Y0), P(G0, Y1), C["muted"], 1.8)
cv.text_px(cv.X(P(G1, Y0)[0]) + 12, cv.Y(P(G1, Y0)[1]), "層間淨距 (cm)", 12.5, C["muted"], "start")
cv.text_px(cv.X(P(G0, Y1)[0]) - 10, cv.Y(P(G0, Y1)[1]) - 22, "φM_{n} (tf·m)", 13,
           C["muted"], "end")

n = 200
cv.poly([P(G0 + (G1 - G0) * i / n, phiMn(AS_PRO, d_actual(ROWS, G0 + (G1 - G0) * i / n)[0])[0])
         for i in range(n + 1)], C["bmd"], 3.4)
cv.line(P(G0, MU), P(G1, MU), C["load"], 2.4, dash="8 5")
cv.math_px(cv.X(P(G0, 0)[0]) + 8, cv.Y(P(0, MU)[1]) - 13, f"M_{{u}} = {MU:.1f} tf·m",
           13.5, C["load"], "start", weight="700")

for g, lab in ((2.5, "規範下限"), (DB, "本解 = d_b"), (3.5, ""), (4.0, "")):
    pm = phiMn(AS_PRO, d_actual(ROWS, g)[0])[0]
    is_main = abs(g - DB) < 1e-9
    col = C["accent"] if is_main else C["muted"]
    cv.dot(P(g, pm), 6.2 if is_main else 5.0, fill=col, stroke="#FFFFFF", w=2.0)
    cv.math_px(cv.X(P(g, 0)[0]), cv.Y(P(0, pm)[1]) - 16, f"{pm:.2f}", 12.5, col, weight="700")
    if lab:
        cv.text_px(cv.X(P(g, 0)[0]), cv.Y(P(0, Y0)[1]) + 42, lab, 11.5, col)

# 交點（φMn = Mu）
lo, hi = G0, G1
for _ in range(80):
    m = (lo + hi) / 2
    if phiMn(AS_PRO, d_actual(ROWS, m)[0])[0] > MU: lo = m
    else: hi = m
G_CRIT = (lo + hi) / 2
cv.line(P(G_CRIT, Y0), P(G_CRIT, Y1 - 0.12), C["load"], 1.8, dash="4 5")
cv.text_px(cv.X(P(G_CRIT, 0)[0]) + 8, T_ + 40, f"{G_CRIT:.2f} cm 以上就不足",
           12.5, C["load"], "start", weight="700")

cv.text_px(W3 / 2, H3 - 52,
           f"層間淨距只要從 {DB:.2f} 放寬到 {G_CRIT:.2f} cm，{N_BAR}-D29 就不夠了",
           13.5, C["load"], weight="700")
cv.text_px(W3 / 2, H3 - 28,
           "卷面務必明寫層間距假設值，並附上 φMn 與 Mu 的比較", 12.5, C["muted"])
cv.save(f"{OUT}/{TAG}-fig-3-sensitivity.svg")

# ══════════════════════════════════════════════════════════
# 對 .md §4／§5 公佈值 assert
# ══════════════════════════════════════════════════════════
assert abs(MU - 70.4) < 1e-9,               MU
assert abs(BEFF - 150.0) < 1e-9,            BEFF
assert abs(A_REQ - 4.27) < 0.01,            A_REQ
assert abs(AS_REQ - 36.3) < 0.05,           AS_REQ
assert abs(ET_REQ - 0.0290) < 5e-4,         ET_REQ
assert N_BAR == 6,                          N_BAR
assert abs(AS_PRO - 38.81) < 0.01,          AS_PRO
assert abs(DB - 2.87) < 0.005,              DB
assert abs(s_clear(6) - 0.56) < 0.01,       s_clear(6)
assert abs(s_clear(3) - 5.70) < 0.01,       s_clear(3)
assert abs(YS[0] - 6.44) < 0.01,            YS[0]
assert abs(YS[1] - 12.18) < 0.01,           YS[1]
assert abs(YBAR - 9.31) < 0.01,             YBAR
assert abs(D_ACT - 50.69) < 0.02,           D_ACT
assert abs(A_ACT - 4.566) < 0.005,          A_ACT
assert abs(PMN - 71.03) < 0.03,             PMN
assert abs(ET_ACT - 0.0253) < 5e-4,         ET_ACT
for g, want in ((2.5, 71.30), (DB, 71.03), (3.5, 70.57), (4.0, 70.20)):
    got = phiMn(AS_PRO, d_actual(ROWS, g)[0])[0]
    assert abs(got - want) < 0.03, (g, got, want)
print(f"{TAG}: 3 圖 OK　Mu={MU} b_e={BEFF:.0f} a={A_REQ:.2f} As={AS_REQ:.1f} n={N_BAR} "
      f"s(6)={s_clear(6):.2f} s(3)={s_clear(3):.2f} d={D_ACT:.2f} φMn={PMN:.2f} "
      f"臨界層間距={G_CRIT:.2f} cm")
