#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2013-2 方形柱耐震圍束箍筋配置 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2013-2.md §1／§3.5 L1 的原始給定（含 §5① 的 D10 比較值、
     §4 Step 5 的 l_o 三條件常數）。h_c、A_g、A_ch、A_g/A_ch、A_sh/s、主筋心距、
     h_x、s_o、6d_b、b/4、s、A_sh,req、腳數、A_sh,prov、密箍區外間距、rho_g、
     以及「只配 2 支繫筋」的對照值全部現算，檔尾對 §4／§5 公佈值 assert。
  2. 改 §1 任一數字重跑，四張圖的幾何與標註跟著變（主筋位置、繫筋位置、
     箍筋間距的實際落點都由算式決定，無寫死座標）。
  3. FIGURES 表寫明每張圖攔什麼錯。

用法：
    STRUCTDRAW_DIR=<skill>/scripts python3 gen_RC-2013-2.py figs
"""
import sys, os, math

sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C
from recipes import bar_compare

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2013-2"

# ══════════════════════════════════════════════════════════
# §1 原始給定（方形柱・特殊抗彎構架柱・耐震圍束箍筋）
# ══════════════════════════════════════════════════════════
B = 50.0            # cm  方形柱邊長（§1）
CC = 4.0            # cm  保護層，量至箍筋外緣（§1）
D_LONG = 3.22       # cm  D32 主筋直徑（§1 圖說）
AB_LONG = 8.14      # cm^2 一支 D32 斷面積（§1 圖說）
N_LONG = 16         # 支  主筋總數（§1）
N_FACE = 5          # 支  每面主筋數（含角筋）（§1 圖說）
FC = 280.0          # kgf/cm^2（§1）
FYH = 2800.0        # kgf/cm^2 橫向鋼筋降伏強度（§1）

D_TIE = 1.27        # cm  D13 箍筋直徑（§3.5 L1／§4 Step 3）
AB_TIE = 1.27       # cm^2 一支 D13 斷面積（§3.5 L1）
AB_D10 = 0.71       # cm^2 一支 D10 斷面積（§5① 的對照規格）

# 規範常數（土木 401-100／401-112 §15.4／ACI 318-19 §18.7.5）
SO_LO, SO_HI = 10.0, 15.0     # s_o 的下、上限（cm）
HX_LIMIT = 35.0               # h_x 上限（cm）
S_OUT_CAP = 15.0              # l_o 以外之絕對間距上限（cm，＝150 mm）
LO_ABS = 45.0                 # l_o 第三條件（cm，＝450 mm）
HOOK_MIN = 7.5                # 耐震彎鉤延伸下限（cm，＝75 mm）
RHO_LO, RHO_HI = 0.01, 0.06   # 縱向鋼筋比範圍（§5④）

LU_DEMO = 300.0     # cm  ★示意柱淨高：原卷未給 l_u，僅為圖 4 畫得下用（§4 Step 5）

# ══════════════════════════════════════════════════════════
# 現算（以下沒有一個數字是手打的結果）
# ══════════════════════════════════════════════════════════
HC = B - 2 * CC                       # 核心邊長（量至箍筋外緣）
AG = B * B
ACH = HC * HC
RATIO = AG / ACH

ASH1_PER_S = 0.3 * HC * (RATIO - 1.0) * FC / FYH      # 公式一 A_sh/s
ASH2_PER_S = 0.09 * HC * FC / FYH                     # 公式二 A_sh/s
ASH_PER_S = max(ASH1_PER_S, ASH2_PER_S)               # 兩式取大

# 主筋幾何：h_c 量到箍筋外緣，故主筋中心距總長要扣「兩側各一個箍筋直徑」＋一個主筋直徑
PITCH = (HC - 2 * D_TIE - D_LONG) / (N_FACE - 1)
X_BAR0 = CC + D_TIE + D_LONG / 2.0                    # 角筋中心到柱外緣
X_BARS = [X_BAR0 + i * PITCH for i in range(N_FACE)]
T0 = CC + D_TIE / 2.0                                 # 外箍中心線到柱外緣
T1 = B - T0

HX = PITCH                                            # 全部中間筋皆配繫筋
SO_RAW = 10.0 + (HX_LIMIT - HX) / 3.0
SO = min(max(SO_RAW, SO_LO), SO_HI)                   # 受 10～15 cm 夾制

S_6DB = 6.0 * D_LONG
S_B4 = B / 4.0
S_MAX = min(S_B4, S_6DB, SO)
S = float(math.floor(S_MAX))                          # 取整至 cm

ASH_REQ = ASH_PER_S * S
ASH2_AT_S = ASH2_PER_S * S
LEGS_MIN = int(math.ceil(ASH_REQ / AB_TIE - 1e-9))
N_CT = LEGS_MIN - 2                                   # 外箍已提供 2 腳
ASH_PROV = LEGS_MIN * AB_TIE
D13_4LEGS = (LEGS_MIN - 1) * AB_TIE                   # 少一支繫筋（只配 2 支）
D10_5LEGS = LEGS_MIN * AB_D10

S_OUTSIDE = min(S_6DB, S_OUT_CAP)
RHO_G = N_LONG * AB_LONG / AG

ALT_HX = 2.0 * PITCH                                  # 只在位置 2、4 配繫筋
ALT_SO_RAW = 10.0 + (HX_LIMIT - ALT_HX) / 3.0
ALT_SO = min(max(ALT_SO_RAW, SO_LO), SO_HI)

# 只扣「一個」箍筋直徑的舊版誤算（§4 Step 3 勘誤註）
PITCH_WRONG = (HC - D_TIE - D_LONG) / (N_FACE - 1)

LO = max(B, LU_DEMO / 6.0, LO_ABS)
HOOK_EXT = max(6.0 * D_TIE, HOOK_MIN)                 # 耐震彎鉤延伸長度

# 繫筋位置＝所有「中間」主筋的座標（角筋由外箍轉角直接支撐）
CT_POS = X_BARS[1:-1]
# 每一方向的箍筋腳位置：外箍兩腳（箍筋中心線）＋各繫筋
LEG_POS = [T0] + list(CT_POS) + [T1]


def M(s):
    """math()/math_px() 用 FONT_M 襯線字型，缺中日韓字元會被靜默丟掉。"""
    assert not any(ord(ch) > 0x2E80 for ch in s), f"math 字串不得含中日韓字元：{s}"
    return s


def ticks(y0, y1, step):
    """由 y0 起以 step 遞增（step 可為負）直到超出 y1，回傳落點串列。"""
    out, y = [], y0
    while (y <= y1 + 1e-9) if step > 0 else (y >= y1 - 1e-9):
        out.append(y)
        y += step
    return out


# ══════════════════════════════════════════════════════════
# 圖 1　斷面與橫向鋼筋配置（取代 .md 中的 ASCII 圖）
# ══════════════════════════════════════════════════════════
def fig1():
    W, H = 1080, 740
    SX = 8.0
    cv = Canvas(W, H, sx=SX, ox=140, oy=160, bg="#FFFFFF")

    cv.text_px(W / 2, 34,
               f"圖 1　{TAG}　方形柱 {B:g}×{B:g} cm 耐震圍束橫向鋼筋配置",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"{N_LONG}-D32（每面 {N_FACE} 根含角筋）　c_{{c}} = {CC:g} cm（量至箍筋外緣）　"
               f"f'_{{c}} = {FC:g}、f_{{yh}} = {FYH:g} kgf/cm^{{2}}　橫向鋼筋 D13",
               13, C["muted"])

    # ── 混凝土斷面與核心 ──
    cv.polygon([(0, 0), (B, 0), (B, B), (0, B)], "#EDF1F6", C["member"], 2.6)
    cv.polygon([(CC, CC), (B - CC, CC), (B - CC, B - CC), (CC, B - CC)],
               "rgba(29,78,216,0.06)", C["member2"], 1.4)
    cv.parts[-1] = cv.parts[-1].replace('stroke-width="1.4"',
                                        'stroke-width="1.4" stroke-dasharray="6 4"')

    # ── 外圍 D13 閉合箍筋（畫在箍筋中心線上）──
    cv.polygon([(T0, T0), (T1, T0), (T1, T1), (T0, T1)], "none", C["load"], 2.6)
    # 135° 耐震彎鉤：對角兩個轉角，延伸 HOOK_EXT，鉤住角筋後斜向伸入核心
    dhk = HOOK_EXT / math.sqrt(2.0)
    cv.line((T0, T0), (T0 + dhk, T0 + dhk), C["load"], 2.6)
    cv.line((T1, T1), (T1 - dhk, T1 - dhk), C["load"], 2.6)

    # ── 垂直繫筋（提供 x 方向腳）：鉤住上、下面的中間主筋 ──
    yb, yt = X_BARS[0], X_BARS[-1]
    for x in CT_POS:
        cv.line((x, yb), (x, yt), C["deform"], 2.4)
        cv.line((x, yb), (x - dhk, yb + dhk), C["deform"], 2.4)          # 135°
        cv.poly([(x, yt), (x, yt - 1.9), (x - 6.0 * D_TIE, yt - 1.9)],
                C["deform"], 2.4)                                        # 90°
    # ── 水平繫筋（提供 y 方向腳）：鉤住左、右面的中間主筋 ──
    xl, xr = X_BARS[0], X_BARS[-1]
    for y in CT_POS:
        cv.line((xl, y), (xr, y), C["bmd"], 2.4)
        cv.line((xl, y), (xl + dhk, y + dhk), C["bmd"], 2.4)             # 135°
        cv.poly([(xr, y), (xr - 1.9, y), (xr - 1.9, y - 6.0 * D_TIE)],
                C["bmd"], 2.4)                                           # 90°

    # ── 16-D32 主筋（真實直徑）──
    bars = [(x, y) for x in X_BARS for y in (X_BARS[0], X_BARS[-1])] + \
           [(x, y) for x in (X_BARS[0], X_BARS[-1]) for y in X_BARS[1:-1]]
    assert len(bars) == N_LONG
    for p in bars:
        cv.circle(p, D_LONG / 2.0, C["member"], "#FFFFFF", 1.4)

    # ── 尺寸線 ──
    cv.dim((0, B), (B, B), M(f"{B:g} cm"), off=-40, label_off=-15)
    cv.dim((CC, CC), (CC, B - CC), M(f"h_{{c}} = {HC:g} cm"), off=-70, label_off=-22)
    cv.dim((X_BARS[0], X_BARS[0]), (X_BARS[1], X_BARS[0]),
           M(f"h_{{x}} = {HX:.2f}"), off=76, label_off=16)
    cv.dim((B, B - CC), (B, B), M(f"{CC:g}"), off=30, label_off=14)

    # ── 右欄① 斷面幾何 ──
    RX = 628
    cv.rect_px(608, 126, 452, 224, C["panel"], 12, C["border"], 1.2)
    rows = [
        f"A_{{g}} = {B:g} × {B:g} = {AG:g} cm^{{2}}",
        f"h_{{c}} = {B:g} - 2({CC:g}) = {HC:g} cm　（量至箍筋外緣）",
        f"A_{{ch}} = {HC:g} × {HC:g} = {ACH:g} cm^{{2}}",
        f"A_{{g}}/A_{{ch}} = {AG:g}/{ACH:g} = {RATIO:.3f}",
        f"相鄰主筋心距 = ({HC:g} - 2({D_TIE:g}) - {D_LONG:g})/{N_FACE-1:d} = {PITCH:.2f} cm",
        f"h_{{x}} = {HX:.2f} cm ≤ {HX_LIMIT:g} cm ✓",
        f"圖中虛線方框 ＝ 核心邊界（量至箍筋外緣）",
    ]
    for i, t in enumerate(rows):
        cv.text_px(RX, 152 + i * 29, t, 13,
                   C["muted"] if i == 6 else C["text"], "start")

    # ── 右欄② 每方向腳數（小示意圖）──
    cv.rect_px(608, 366, 452, 174, C["panel"], 12, C["border"], 1.2)
    cv.text_px(RX, 392,
               f"每方向箍筋腳數 = 外箍 2 腳 + 繫筋 {N_CT} 腳 = {LEGS_MIN} 腳",
               13.5, C["text"], "start", weight="700")
    mx0, mw = 660, 240
    cv.rect_px(mx0, 418, mw, 22, "#EDF1F6", 5)
    for i, xl_ in enumerate(LEG_POS):
        px = mx0 + mw * xl_ / B
        col = C["load"] if xl_ in (T0, T1) else C["deform"]
        cv.parts.append(f'<line x1="{px:.2f}" y1="412" x2="{px:.2f}" y2="446" '
                        f'stroke="{col}" stroke-width="3.2" stroke-linecap="round"/>')
        cv.text_px(px, 460, f"{i+1}", 11.5, C["muted"])
    cv.text_px(mx0 + mw + 14, 429, "（x 方向；y 方向同）", 12, C["muted"], "start")
    cv.text_px(RX, 486,
               f"A_{{sh,x}} = A_{{sh,y}} = {LEGS_MIN} × {AB_TIE:g} = {ASH_PROV:.2f} cm^{{2}}"
               f" ≥ {ASH_REQ:.2f} cm^{{2}} ✓",
               13.5, C["bmd"], "start", weight="700")
    cv.text_px(RX, 512,
               f"A_{{sh}} 是「單一方向」的量：同方向所有箍筋腳一起算",
               12.5, C["muted"], "start")

    # ── 右欄③ 圖例 ──
    cv.rect_px(608, 556, 452, 144, C["panel"], 12, C["border"], 1.2)
    cv.legend(RX, 586, [
        (C["load"], "外圍 D13 閉合箍筋（135° 耐震彎鉤，對角兩處）"),
        (C["deform"], f"D13 垂直繫筋 ×{N_CT}（鉤住上、下面中間筋）＝ x 方向腳"),
        (C["bmd"], f"D13 水平繫筋 ×{N_CT}（鉤住左、右面中間筋）＝ y 方向腳"),
        (C["member"], f"{N_LONG}-D32 主筋（每面 {N_FACE} 根，含角筋）"),
    ], size=12.5, gap=24, swatch=22)
    cv.text_px(RX, 682,
               f"彎鉤延伸 = max(6d_{{b}}, {HOOK_MIN:g}) = {HOOK_EXT:.2f} cm；"
               f"繫筋 90° 彎鉤沿柱高逐層交錯",
               12, C["muted"], "start")

    cv.text_px(W / 2, 722,
               f"三根中間主筋每一根都被繫筋直接鉤住 → h_{{x}} = {HX:.2f} cm；"
               f"h_{{x}} 要扣兩側各一個箍筋直徑（2 × {D_TIE:g}），"
               f"只扣一個會誤得 {PITCH_WRONG:.2f} cm",
               12.5, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 2　A_sh 需求／提供比較（s = 12 cm）
# ══════════════════════════════════════════════════════════
def fig2():
    cases = [
        (f"A_{{sh,1}} 需求 ← 控制", "公式一（含 A_{g}/A_{ch} 項）", ASH_REQ,
         M(f"{ASH1_PER_S:.3f} \u00d7 {S:g} = {ASH_REQ:.2f} cm^{{2}}"), C["load"]),
        (f"A_{{sh,2}} 需求", "公式二（不含 A_{g}/A_{ch} 項）", ASH2_AT_S,
         M(f"{ASH2_PER_S:.3f} \u00d7 {S:g} = {ASH2_AT_S:.2f} cm^{{2}}"), C["muted"]),
        (f"D13 × {LEGS_MIN} 腳 ← 採用", f"外箍 2 腳 + 繫筋 {N_CT} 腳", ASH_PROV,
         M(f"{LEGS_MIN} \u00d7 {AB_TIE:g} = {ASH_PROV:.2f} cm^{{2}}  OK"), C["bmd"]),
        (f"D13 × {LEGS_MIN-1} 腳", "只配 2 支繫筋（跳過中央）", D13_4LEGS,
         M(f"{LEGS_MIN-1} \u00d7 {AB_TIE:g} = {D13_4LEGS:.2f} cm^{{2}}  NG"), C["ghost"]),
        (f"D10 × {LEGS_MIN} 腳", "箍筋規格太小", D10_5LEGS,
         M(f"{LEGS_MIN} \u00d7 {AB_D10:g} = {D10_5LEGS:.2f} cm^{{2}}  NG"), C["ghost"]),
    ]
    cv = bar_compare(
        cases, row_h=88,
        title=f"圖 2　A_{{sh}} 需求與提供（以 s = {S:g} cm 計，每一方向）",
        sub=f"兩個 A_{{sh}} 公式取「大」者控制：{ASH1_PER_S:.3f}s ＞ {ASH2_PER_S:.3f}s"
            f"　→　A_{{sh,req}} = {ASH_REQ:.2f} cm^{{2}}／方向",
        note=f"最少腳數 = {ASH_REQ:.2f} / {AB_TIE:g} = {ASH_REQ/AB_TIE:.2f} → 無條件進位取 "
             f"{LEGS_MIN} 腳；只配 2 支繫筋雖然 h_{{x}} = {ALT_HX:.2f} cm ≤ "
             f"{HX_LIMIT:g} cm 過關，A_{{sh}} 仍然不足")
    # 需求門檻線：讓不足的兩列一眼看出差多少
    peak = max(c[2] for c in cases)
    xr = 320 + 400 * ASH_REQ / peak
    cv.parts.append(f'<line x1="{xr:.1f}" y1="104" x2="{xr:.1f}" y2="{122+88*4+30:.0f}" '
                    f'stroke="{C["load"]}" stroke-width="1.8" stroke-dasharray="6 5"/>')
    cv.text_px(xr, 92, f"需求 {ASH_REQ:.2f} cm^{{2}}", 12.5, C["load"], weight="700")
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 3　密箍區間距三條件（＋密箍區外）
# ══════════════════════════════════════════════════════════
def fig3():
    cases = [
        (f"6 d_{{b}}", f"縱筋 D32：6 × {D_LONG:g}", S_6DB,
         M(f"{S_6DB:.2f} cm"), C["ghost"]),
        (f"s_{{o}} 公式", f"算得 {SO_RAW:.2f}，取上限 {SO_HI:g}", SO_RAW,
         M(f"{SO_RAW:.2f} \u2192 {SO:.1f} cm"), C["accent"]),
        (f"b/4 ← 控制", f"{B:g}/4", S_B4,
         M(f"{S_B4:.1f} cm"), C["load"]),
        (f"密箍區採用 s", "三條件取小後取整", S,
         M(f"s = {S:g} cm"), C["bmd"]),
        (f"密箍區「以外」", f"min(6d_{{b}}, {S_OUT_CAP:g})", S_OUTSIDE,
         M(f"{S_OUTSIDE:.1f} cm"), C["deform"]),
    ]
    cv = bar_compare(
        cases, row_h=88,
        title=f"圖 3　密箍區最大間距：三個條件同時攤開（長條越長 ＝ 間距越大 ＝ 越不安全）",
        sub=f"s ≤ min(b/4, 6d_{{b}}, s_{{o}}) = min({S_B4:.1f}, {S_6DB:.2f}, {SO:.1f}) "
            f"= {S_MAX:.1f} cm　→　採用 s = {S:g} cm",
        note=f"s_{{o}} = 10 + (35 - {HX:.2f})/3 = {SO_RAW:.2f} cm，"
             f"另限 {SO_LO:g} ≤ s_{{o}} ≤ {SO_HI:g} cm 故取 {SO:.1f}；"
             f"密箍區外 = min({S_6DB:.2f}, {S_OUT_CAP:g}) = {S_OUTSIDE:.1f} cm，"
             f"6d_{{b}} 不能單獨成立")
    # 把「18.65 被 15 截住」畫出來：條長仍畫到 18.65，並在 15 的位置立一條上限線
    peak = max(c[2] for c in cases)
    y_row = 122 + 1 * 88
    xc = 320 + 400 * SO / peak
    xe = 320 + 400 * SO_RAW / peak
    cv.parts.append(f'<line x1="{xc:.1f}" y1="{y_row-30:.0f}" x2="{xc:.1f}" '
                    f'y2="{y_row+30:.0f}" stroke="{C["load"]}" stroke-width="2.4"/>')
    cv.text_px(xc, y_row - 40, f"規範上限 {SO_HI:g} cm", 12.5, C["load"], weight="700")
    cv.text_px((xc + xe) / 2 + 30, y_row + 44, "超出上限的部分不可用", 12, C["load"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 4　柱立面：密箍區位置與內外間距
# ══════════════════════════════════════════════════════════
def fig4():
    W, H = 940, 720
    JD = 20.0                                  # 接頭（梁）示意帶厚度
    y_lo, y_hi = -JD, LU_DEMO + JD
    mT, mB = 122, 122
    SX = (H - mT - mB) / (y_hi - y_lo)
    OX = 180.0
    cv = Canvas(W, H, sx=SX, ox=OX, oy=mB - y_lo * SX, bg="#FFFFFF")

    cv.text_px(W / 2, 34,
               f"圖 4　柱立面：密箍區 l_{{o}} 的位置，以及密箍區內／外的箍筋間距",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"l_{{o}} = max(柱斷面最大邊長, l_{{u}}/6, {LO_ABS:g} cm)　"
               f"★本圖柱淨高 l_{{u}} = {LU_DEMO:g} cm 為示意值（原卷未給 l_{{u}}）",
               13, C["muted"])

    # 上下接頭（梁）示意帶
    for y0 in (-JD, LU_DEMO):
        cv.polygon([(0, y0), (B, y0), (B, y0 + JD), (0, y0 + JD)],
                   "#E1E6ED", C["member"], 1.6)
    # 柱身
    cv.polygon([(0, 0), (B, 0), (B, LU_DEMO), (0, LU_DEMO)],
               "#EDF1F6", C["member"], 2.4)
    # 密箍區底色
    for y0 in (0.0, LU_DEMO - LO):
        cv.polygon([(0, y0), (B, y0), (B, y0 + LO), (0, y0 + LO)],
                   C["fill_t"], "none", 0)
    # 縱向主筋（立面只見兩側外排）
    for x in (X_BARS[0], X_BARS[-1]):
        cv.line((x, -JD * 0.7), (x, LU_DEMO + JD * 0.7), C["member"], 2.0)

    # 箍筋落點：全部由 s 現算
    first = S / 2.0                              # 首支箍筋距接頭面：柱為 s_o/2（§18.7.5.3）
    bot = ticks(first, LO, S) + [LO]
    top = [LU_DEMO - LO] + ticks(LU_DEMO - first, LU_DEMO - LO, -S)
    mid = ticks(LO + S_OUTSIDE, LU_DEMO - LO, S_OUTSIDE)
    for y in sorted(set(bot + top)):
        cv.line((1.6, y), (B - 1.6, y), C["load"], 2.6)
    for y in sorted(set(mid)):
        cv.line((1.6, y), (B - 1.6, y), C["accent"], 2.2)

    # 左側：分區與全高尺寸
    cv.dim((0, 0), (0, LO), M(f"l_{{o}} = {LO:g}"), off=-42, label_off=-15)
    cv.dim((0, LO), (0, LU_DEMO - LO), M(f"{LU_DEMO-2*LO:g}"), off=-42, label_off=-15)
    cv.dim((0, LU_DEMO - LO), (0, LU_DEMO), M(f"l_{{o}} = {LO:g}"), off=-42, label_off=-15)
    cv.dim((0, 0), (0, LU_DEMO), M(f"l_{{u}} = {LU_DEMO:g}"), off=-116, label_off=-16)
    cv.dim((0, -JD), (B, -JD), M(f"{B:g}"), off=48, label_off=16)

    # 右側：實際間距量測
    cv.dim((B, bot[0]), (B, bot[1]), M(f"{S:g}"), off=24, label_off=13)
    cv.dim((B, mid[0]), (B, mid[1]), M(f"{S_OUTSIDE:g}"), off=24, label_off=13)
    cv.dim((B, top[-1]), (B, top[-2]), M(f"{S:g}"), off=24, label_off=13)

    TX = 306
    for ymid, txt, col in ((LO / 2, f"密箍區　D13 @ {S:g} cm", C["load"]),
                           (LU_DEMO / 2, f"密箍區以外　D13 @ {S_OUTSIDE:g} cm", C["accent"]),
                           (LU_DEMO - LO / 2, f"密箍區　D13 @ {S:g} cm", C["load"])):
        cv.parts.append(f'<line x1="{cv.X(B):.1f}" y1="{cv.Y(ymid):.1f}" '
                        f'x2="{TX-8:.1f}" y2="{cv.Y(ymid):.1f}" stroke="{col}" '
                        f'stroke-width="1" stroke-dasharray="3 4"/>')
        cv.text_px(TX, cv.Y(ymid), txt, 13.5, col, "start", weight="700")
    cv.text_px(TX, cv.Y(-JD / 2), "接頭面（梁／基礎）", 12, C["muted"], "start")
    cv.text_px(TX, cv.Y(LU_DEMO + JD / 2), "接頭面（梁）", 12, C["muted"], "start")
    cv.text_px(TX, cv.Y(first) + 4,
               f"首支箍筋距接頭面 \u2264 s/2 = {first:g} cm（柱 \u00a7 18.7.5.3）", 11.5,
               C["muted"], "start")

    # 右欄①：l_o 三條件
    cv.rect_px(560, 132, 356, 156, C["panel"], 12, C["border"], 1.2)
    for i, t in enumerate([
        f"l_{{o}} 三條件皆取「大」：",
        f"　① 柱斷面最大邊長 = {B:g} cm",
        f"　② l_{{u}}/6 = {LU_DEMO:g}/6 = {LU_DEMO/6:g} cm",
        f"　③ 絕對下限 = {LO_ABS:g} cm",
        f"→ l_{{o}} = {LO:g} cm（柱上、下端各一段）",
    ]):
        cv.text_px(580, 158 + i * 26, t, 12.5,
                   C["text"] if i in (0, 4) else C["muted"], "start",
                   weight="700" if i in (0, 4) else "400")

    # 右欄②：內外間距
    cv.rect_px(560, 308, 356, 132, C["panel"], 12, C["border"], 1.2)
    for i, (t, col, wt) in enumerate([
        (f"密箍區內　s = min(b/4, 6d_{{b}}, s_{{o}})", C["text"], "700"),
        (f"　= min({S_B4:.1f}, {S_6DB:.2f}, {SO:.1f}) → {S:g} cm", C["load"], "700"),
        (f"密箍區外　s = min(6d_{{b}}, {S_OUT_CAP:g}) ", C["text"], "700"),
        (f"　= min({S_6DB:.2f}, {S_OUT_CAP:g}) = {S_OUTSIDE:g} cm，不是 {S_6DB:.2f} cm",
         C["accent"], "700"),
    ]):
        cv.text_px(580, 332 + i * 26, t, 12.5, col, "start", weight=wt)

    # 右欄③：圖例
    cv.rect_px(560, 460, 356, 96, C["panel"], 12, C["border"], 1.2)
    cv.legend(580, 486, [
        (C["load"], f"密箍區內 D13 @ {S:g} cm（本圖 {len(set(bot+top))} 道）"),
        (C["accent"], f"密箍區外 D13 @ {S_OUTSIDE:g} cm（本圖 {len(set(mid))} 道）"),
        (C["member"], "縱向 D32 主筋（立面示意）"),
    ], size=12.5, gap=24, swatch=22)

    cv.text_px(W / 2, 700,
               f"若 l_{{u}} 超過 {6*B:g} cm，則 l_{{o}} 改由 l_{{u}}/6 控制；"
               f"作答寫成 l_{{o}} = max({B:g}, l_{{u}}/6) 最完整",
               12.5, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-section", fig1,
     "把 A_sh 當「整個斷面」的量；漏掉中央那支繫筋使中間筋失去直接支撐；"
     "h_x 只扣一個箍筋直徑（9.38）而非兩側各一個（9.06）"),
    ("3-ash", fig2,
     "兩個 A_sh 公式取 min；用 D10；只在位置 2、4 配繫筋（4 腳）"),
    ("2-spacing", fig3,
     "漏算第三條 s_o；忘記 s_o 還有 15 cm 上限；以為 6d_b 可以單獨成立"),
    ("4-elevation", fig4,
     "l_o 三條件沒取大；密箍區外誤用 6d_b = 19.3 cm"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    checks = [
        ("h_c cm",            HC,          42.0,    1e-9),
        ("A_g cm2",           AG,          2500.0,  1e-9),
        ("A_ch cm2",          ACH,         1764.0,  1e-9),
        ("A_g/A_ch",          RATIO,       1.417,   0.001),
        ("A_sh1/s cm2/cm",    ASH1_PER_S,  0.526,   0.001),
        ("A_sh2/s cm2/cm",    ASH2_PER_S,  0.378,   1e-9),
        ("b/4 cm",            S_B4,        12.5,    1e-9),
        ("6d_b cm",           S_6DB,       19.32,   1e-9),
        ("主筋心距 cm",        PITCH,       9.06,    0.001),
        ("s_o 原算 cm",        SO_RAW,      18.65,   0.005),
        ("s_o 取上限 cm",      SO,          15.0,    1e-9),
        ("s cm",              S,           12.0,    1e-9),
        ("A_sh,req cm2",      ASH_REQ,     6.31,    0.005),
        ("最少腳數",           LEGS_MIN,    5,       1e-9),
        ("A_sh,prov cm2",     ASH_PROV,    6.35,    1e-9),
        ("A_sh2@12 cm2",      ASH2_AT_S,   4.54,    0.005),
        ("D13 4 腳 cm2",       D13_4LEGS,   5.08,    1e-9),
        ("D10 5 腳 cm2",       D10_5LEGS,   3.55,    1e-9),
        ("密箍區外 s cm",       S_OUTSIDE,   15.0,    1e-9),
        ("rho_g",             RHO_G,       0.0521,  0.0001),
        ("替代配置 h_x cm",     ALT_HX,      18.12,   0.001),
        ("替代配置 s_o 原算",   ALT_SO_RAW,  15.63,   0.005),
        ("l_o cm（示意 l_u）",  LO,          50.0,    1e-9),
        ("彎鉤延伸 cm",         HOOK_EXT,    7.62,    1e-9),
    ]
    print(f"── 與 {TAG}.md §4／§5 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<18} 算得 {got:>12.6g}   .md {want:>9}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    assert N_CT == 3 and RHO_LO <= RHO_G <= RHO_HI and ALT_SO == SO

    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<32} 攔：{catches}")


if __name__ == "__main__":
    main()
