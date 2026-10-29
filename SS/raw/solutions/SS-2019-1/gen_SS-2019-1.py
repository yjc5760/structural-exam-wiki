#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2019-1 圖解產生腳本（鋼結構三種防蝕方法）

數字全部取自解題檔 §4（Sa 2½／Sa 3、粗糙度 25–75 μm、上緣 ≥60 μm、
鋅噴塗 100–150 μm、鋁噴塗 80–120 μm、封孔 4 h、鍍鋅槽 450 °C、
§7.4.4 之四項環境限制、§7.4.5 之現場銲接兩側各 100 mm）。
圖 3 之露點界線由 Magnus 式現算，改溫度範圍會跟著變。
執行：python3 gen_SS-2019-1.py   →   figs/*.svg
"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.environ.get("SD_SKILL",
                       os.path.normpath(os.path.join(_HERE, "..", "..", "..",
                                                     "skills", "struct-diagram")))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from structdraw import Canvas, C, compose

OUT = os.path.join(_HERE, "figs")

# ══════════════════════════════════════════════════════════════
# 由 SS-2019-1 §4 取得
# ══════════════════════════════════════════════════════════════
RG_LO, RG_HI = 25.0, 75.0      # μm  §7.2.3 表面粗糙度一般範圍
RG_SPRAY_MIN = 60.0            # μm  金屬噴塗取上緣，一般 ≧ 60
ZN_LO, ZN_HI = 100.0, 150.0    # μm  鋅噴塗常用厚度
AL_LO, AL_HI = 80.0, 120.0     # μm  鋁噴塗常用厚度
SEAL_HR = 4.0                  # h   噴塗後封孔時限
GALV_T  = 450.0                # °C  熔融鋅液溫度
NOPAINT_MM = 100.0             # mm  §7.4.5 工地銲接部位相鄰兩側各 100 mm

# §7.4.4 環境限制（任一成立即不得塗裝）
T_LO   = 5.0      # °C  溫度 ≦ 5
T_HI   = 50.0     # °C  鋼材表面溫度 ≧ 50
RH_HI  = 85.0     # %   相對濕度 ≧ 85
DEW_DT = 3.0      # °C  鋼材表面溫度須高於露點 3 °C 以上


def dew_point(T, RH):
    """Magnus 式露點（°C）"""
    g = math.log(RH/100.0) + 17.625*T/(243.04 + T)
    return 243.04*g/(17.625 - g)


def rh_at_dew_limit(T):
    """在溫度 T 下，使『表面溫度恰高於露點 DEW_DT』之相對濕度上限（%）"""
    Td = T - DEW_DT
    if Td <= -60:
        return 100.0
    g = 17.625*Td/(243.04 + Td)
    return min(100.0, 100.0*math.exp(g - 17.625*T/(243.04 + T)))


# ══════════════════════════════════════════════════════════════
def fig1_mechanism():
    """圖 1：三種方法在塗層破損處的差別——屏障 vs 屏障＋犧牲陽極"""
    PWD, PH = 380, 440
    XL, XR, YL, YH = 0.0, 100.0, -34.0, 46.0
    Lm, Tm, Bm = 26, 108, 122
    sx = min((PWD-2*Lm)/(XR-XL), (PH-Tm-Bm)/(YH-YL))
    OX, OY = Lm - XL*sx, Bm - YL*sx
    XB = 50.0                       # 破損位置

    def steel(cv):
        cv.polygon([(0, -30), (100, -30), (100, 0), (0, 0)],
                   "#DCE3EC", C["member"], 2.0)
        cv.text_px(cv.X(6), cv.Y(-15), "鋼材", 12, C["member"], "start", weight="700")

    def breach(cv, col, htop):
        """破損（刮傷）：在塗層上切出一道缺口，缺口底部見鋼材"""
        cv.polygon([(XB-4.5, htop), (XB+4.5, htop), (XB, 0)], "#FFFFFF", col, 2.4)
        cv.text_px(cv.X(XB), cv.Y(htop + 10), "塗層破損", 11.5, col, weight="700")

    # ── 格 1：塗裝（純屏障）──
    p1 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p1.panel("塗裝（油漆系統）", "有機塗膜：只有屏障保護")
    steel(p1)
    for i, (h0, h1, cc, nm) in enumerate(((0, 6, "#7A8CA0", "底漆"),
                                          (6, 13, "#A8B6C6", "中間漆"),
                                          (13, 20, "#CBD5E0", "面漆"))):
        p1.polygon([(0, h0), (100, h0), (100, h1), (0, h1)], cc, C["member"], 1.4)
        p1.text_px(p1.X(97), p1.Y((h0+h1)/2), nm, 10.5, "#FFFFFF" if i == 0 else C["text"],
                   "end")
    breach(p1, C["load"], 20)
    # 露鋼直接鏽蝕、並沿膜下擴展
    p1.polygon([(XB-13, 0), (XB+13, 0), (XB+9, -6), (XB-9, -6)], C["load"], C["load"], 1.2)
    for dx in (-13, 13):
        p1.arrow((XB + dx, -2.5), (XB + dx*1.7, -2.5), C["load"], 2.0, 7)
    p1.text_px(PWD/2, PH - 84, "露鋼處立即鏽蝕", 12.5, C["load"], weight="700")
    p1.text_px(PWD/2, PH - 62, "且鏽蝕沿膜下擴展（膜下腐蝕）", 11.5, C["load"])
    p1.text_px(PWD/2, PH - 36, "塗膜無法保護沒被蓋住的地方", 12, C["muted"])
    p1.text_px(PWD/2, PH - 14, "⇒ 表面處理是成敗關鍵", 12, C["muted"])

    # ── 格 2：熱浸鍍鋅 ──
    p2 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p2.panel("熱浸鍍鋅", f"浸入約 {GALV_T:.0f} °C 熔融鋅液")
    steel(p2)
    p2.polygon([(0, 0), (100, 0), (100, 7), (0, 7)], "#9AA7B4", C["member"], 1.4)
    p2.text_px(p2.X(97), p2.Y(3.5), "鋅鐵合金層", 10.5, "#FFFFFF", "end")
    p2.polygon([(0, 7), (100, 7), (100, 20), (0, 20)], "#C3D2DC", C["member"], 1.4)
    p2.text_px(p2.X(97), p2.Y(13.5), "純鋅層", 10.5, C["text"], "end")
    breach(p2, C["bmd"], 20)
    for dx in (-16, 16):
        p2.arrow((XB + dx, 10), (XB + dx*0.25, 1.5), C["bmd"], 2.2, 7)
    p2.text_px(p2.X(XB), p2.Y(-8), "露鋼受保護", 11.5, C["bmd"], weight="700")
    p2.text_px(PWD/2, PH - 84, "鄰近的鋅優先溶出", 12.5, C["bmd"], weight="700")
    p2.text_px(PWD/2, PH - 62, "＝屏障 ＋ 犧牲陽極（雙重保護）", 11.5, C["bmd"])
    p2.text_px(PWD/2, PH - 36, "密閉斷面須留排氣孔；高強度鋼件", 12, C["load"])
    p2.text_px(PWD/2, PH - 14, "酸洗有氫脆之虞，F10T／A490 不建議", 12, C["load"])

    # ── 格 3：金屬噴塗 ──
    p3 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p3.panel("金屬噴塗（鋅／鋁）", "多孔性金屬層，靠機械咬合附著")
    steel(p3)
    p3.polygon([(0, 0), (100, 0), (100, 17), (0, 17)], "#C3D2DC", C["member"], 1.4)
    for i in range(30):                       # 孔隙
        cx = 3 + (i*13) % 95
        cy = 3 + ((i*7) % 5)*2.8
        p3.parts.append(f'<circle cx="{p3.X(cx):.1f}" cy="{p3.Y(cy):.1f}" r="2.2" '
                        f'fill="#FFFFFF" opacity="0.85"/>')
    p3.polygon([(0, 17), (100, 17), (100, 25), (0, 25)], C["fill_t"], C["load"], 1.4)
    p3.text_px(p3.X(97), p3.Y(21), "封孔漆", 10.5, C["load"], "end", weight="700")
    breach(p3, C["bmd"], 25)
    for dx in (-16, 16):
        p3.arrow((XB + dx, 9), (XB + dx*0.25, 1.5), C["bmd"], 2.2, 7)
    p3.text_px(p3.X(XB), p3.Y(-8), "同樣有犧牲陽極", 11.5, C["bmd"], weight="700")
    p3.text_px(PWD/2, PH - 84, f"塗層天生多孔，須於 {SEAL_HR:.0f} 小時內封孔",
               12.5, C["load"], weight="700")
    p3.text_px(PWD/2, PH - 62, "未封孔＝把腐蝕介質的通道留著", 11.5, C["load"])
    p3.text_px(PWD/2, PH - 36, "可現場施工、構件尺寸不受限", 12, C["muted"])
    p3.text_px(PWD/2, PH - 14, "採十字交叉噴塗確保均勻", 12, C["muted"])

    compose([p1, p2, p3], cols=3,
            title="圖 1　三種防蝕法的差別，在塗層「破損之後」才看得出來",
            sub="塗裝只有屏障保護；熱浸鍍鋅與金屬噴塗另有犧牲陽極效果，"
                "局部破損時鄰近的鋅／鋁仍能保護露鋼",
            note="把三種方法都寫成「隔絕水氧」就漏掉了犧牲陽極這個關鍵區別——"
                 "它正是耐久性差異的來源",
            path=os.path.join(OUT, "SS-2019-1-fig-1-mechanism.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_surface_prep():
    """圖 2：表面處理等級與粗糙度／膜厚的數量級"""
    W, H = 1000, 560
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")

    # ── 上：共用 μm 尺 ──
    Lm, Rm = 210, 90
    UMAX = 170.0
    X = lambda u: Lm + (W-Lm-Rm)*u/UMAX
    yax = 300
    cv.parts.append(f'<line x1="{Lm}" y1="{yax}" x2="{X(UMAX)}" y2="{yax}" '
                    f'stroke="{C["muted"]}" stroke-width="1.8"/>')
    for u in range(0, int(UMAX)+1, 25):
        cv.parts.append(f'<line x1="{X(u):.1f}" y1="{yax}" x2="{X(u):.1f}" y2="{yax+7}" '
                        f'stroke="{C["muted"]}" stroke-width="1.4"/>')
        cv.text_px(X(u), yax + 22, f"{u}", 11, C["muted"])
    cv.text_px(X(UMAX) + 8, yax + 22, "μm", 11.5, C["muted"], "start")

    bars = ((f"表面粗糙度（§7.2.3）", "塗裝：一般落在此範圍內",
             RG_LO, RG_HI, C["bmd"], 132),
            (f"金屬噴塗取上緣", f"一般 ≧ {RG_SPRAY_MIN:.0f} μm",
             RG_SPRAY_MIN, RG_HI, C["load"], 190),
            ("鋅噴塗膜厚", f"{ZN_LO:.0f}～{ZN_HI:.0f} μm",
             ZN_LO, ZN_HI, C["accent"], 248),
            ("鋁噴塗膜厚", f"{AL_LO:.0f}～{AL_HI:.0f} μm",
             AL_LO, AL_HI, C["compr"], 248))
    for nm, note, lo, hi, col, y in bars[:3]:
        cv.rect_px(X(lo), y-15, X(hi)-X(lo), 30, col, 6)
        cv.text_px(Lm - 16, y - 8, nm, 12.5, C["text"], "end", weight="700")
        cv.text_px(Lm - 16, y + 13, note, 11, C["muted"], "end")
        cv.text_px((X(lo)+X(hi))/2, y, f"{lo:.0f}～{hi:.0f}", 12, "#FFFFFF", weight="700")
    # 鋁噴塗與鋅噴塗同列，錯開高度
    nm, note, lo, hi, col, y = bars[3]
    cv.rect_px(X(lo), y+22, X(hi)-X(lo), 30, col, 6)
    cv.text_px(Lm - 16, y + 29, nm, 12.5, C["text"], "end", weight="700")
    cv.text_px(Lm - 16, y + 50, note, 11, C["muted"], "end")
    cv.text_px((X(lo)+X(hi))/2, y + 37, f"{lo:.0f}～{hi:.0f}", 12, "#FFFFFF", weight="700")

    for u, col in ((RG_LO, C["bmd"]), (RG_HI, C["bmd"]), (RG_SPRAY_MIN, C["load"])):
        cv.parts.append(f'<line x1="{X(u):.1f}" y1="112" x2="{X(u):.1f}" y2="{yax}" '
                        f'stroke="{col}" stroke-width="1.3" stroke-dasharray="5 4" '
                        f'opacity="0.6"/>')

    cv.text_px(X((RG_LO+RG_HI)/2), 104, "粗糙度是「基材的凹凸」，不是膜厚——兩者不可混為一談",
               12, C["muted"])

    # ── 下：清潔度等級 ──
    yb = 380
    cv.text_px(Lm - 16, yb, "噴砂清潔度", 12.5, C["text"], "end", weight="700")
    cards = (("塗裝", "Sa 2½", "徹底噴砂處理\n95% 氧化層、鏽及異物去除", C["bmd"]),
             ("熱浸鍍鋅", "脫脂＋酸洗＋助鍍", "以化學前處理取代噴砂\n酸洗廢液須妥善處理",
              C["accent"]),
             ("金屬噴塗", "Sa 3", "絕對徹底噴砂處理\n所有氧化層、鏽及異物徹底除去", C["load"]))
    cw, gap = 246, 18
    for i, (who, lvl, desc, col) in enumerate(cards):
        x = Lm + i*(cw + gap)
        cv.rect_px(x, yb - 22, cw, 118, "#F5F7FA", 10, col, 1.8)
        cv.text_px(x + 14, yb - 2, who, 12, C["muted"], "start")
        cv.text_px(x + 14, yb + 22, lvl, 16, col, "start", weight="700")
        for j, ln in enumerate(desc.split("\n")):
            cv.text_px(x + 14, yb + 50 + j*20, ln, 11, C["text"], "start")

    cv.text_px(W/2, 34, "圖 2　表面處理：金屬噴塗的要求比塗裝嚴一級", 17.5, C["text"],
               weight="700")
    cv.text_px(W/2, 58, "清潔度 Sa 2½ → Sa 3；粗糙度不是另訂一組數字，而是取同一範圍的上緣",
               13, C["muted"])
    cv.text_px(W/2, 82,
               f"§7.2.3 只給一個範圍 {RG_LO:.0f}～{RG_HI:.0f} μm；"
               f"金屬噴塗取上緣（一般 ≧ {RG_SPRAY_MIN:.0f} μm），"
               f"不要自行寫成「R_z 40～70」之類的數字",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               "金屬噴塗層靠機械咬合附著（非化學鍵結），故對粗糙度特別敏感；"
               "熱浸鍍鋅走化學前處理路線，把它也寫成 Sa 2½ 就把三法混成一法了",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2019-1-fig-2-surface-prep.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_env_window():
    """圖 3：§7.4.4 四項環境限制圍出的可施工窗口"""
    W, H = 1020, 600
    Lm, Rm, Tm, Bm = 96, 320, 132, 104
    TA, TB_ = -2.0, 60.0          # 溫度軸
    RA, RB = 40.0, 100.0          # 濕度軸
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    X = lambda t: Lm + (W-Lm-Rm)*(t-TA)/(TB_-TA)
    Y = lambda r: (H-Bm) - (H-Tm-Bm)*(r-RA)/(RB-RA)

    # 可施工窗口（先鋪底）
    cv.rect_px(X(TA), Y(RB), X(TB_)-X(TA), Y(RA)-Y(RB), "#F0F5F0", 0)
    # ① 溫度 ≦ 5、④ 表面溫度 ≧ 50
    for t0, t1 in ((TA, T_LO), (T_HI, TB_)):
        cv.rect_px(X(t0), Y(RB), X(t1)-X(t0), Y(RA)-Y(RB), "rgba(192,57,43,0.13)", 0)
    # ② 相對濕度 ≧ 85
    cv.rect_px(X(TA), Y(RB), X(TB_)-X(TA), Y(RH_HI)-Y(RB), "rgba(192,57,43,0.13)", 0)
    # ③ 表面溫度未高於露點 3 °C 以上（Magnus 式現算）
    TS = [T_LO + (T_HI-T_LO)*i/160 for i in range(161)]
    dew = [(t, rh_at_dew_limit(t)) for t in TS]
    poly = " ".join(f"{X(t):.2f},{Y(min(r, RH_HI)):.2f}" for t, r in dew)
    poly += f" {X(T_HI):.2f},{Y(RH_HI):.2f} {X(T_LO):.2f},{Y(RH_HI):.2f}"
    cv.parts.append(f'<polygon points="{poly}" fill="rgba(180,83,9,0.22)" '
                    f'stroke="{C["accent"]}" stroke-width="2.2"/>')

    # 座標軸
    cv.parts.append(f'<rect x="{X(TA)}" y="{Y(RB)}" width="{X(TB_)-X(TA)}" '
                    f'height="{Y(RA)-Y(RB)}" fill="none" stroke="{C["muted"]}" '
                    f'stroke-width="1.6"/>')
    for t in range(0, int(TB_)+1, 10):
        cv.parts.append(f'<line x1="{X(t):.1f}" y1="{Y(RA)}" x2="{X(t):.1f}" '
                        f'y2="{Y(RA)+7}" stroke="{C["muted"]}" stroke-width="1.3"/>')
        cv.text_px(X(t), Y(RA) + 22, f"{t}", 11, C["muted"])
    for r in range(40, 101, 10):
        cv.parts.append(f'<line x1="{X(TA)-7}" y1="{Y(r):.1f}" x2="{X(TA)}" '
                        f'y2="{Y(r):.1f}" stroke="{C["muted"]}" stroke-width="1.3"/>')
        cv.text_px(X(TA) - 14, Y(r), f"{r}", 11, C["muted"], "end")
    cv.text_px((X(TA)+X(TB_))/2, Y(RA) + 44, "鋼材表面溫度（°C）", 12.5, C["muted"])
    cv.text_px(X(TA) - 6, Tm - 16, "相對濕度（%）", 12.5, C["muted"], "start")

    # 四項標註
    cv.text_px((X(TA)+X(T_LO))/2, Y(62), "①", 17, C["load"], weight="700")
    cv.text_px((X(TA)+X(T_LO))/2, Y(56), f"≦{T_LO:.0f}°C", 11, C["load"], weight="700")
    cv.text_px((X(T_HI)+X(TB_))/2, Y(62), "④", 17, C["load"], weight="700")
    cv.text_px((X(T_HI)+X(TB_))/2, Y(56), f"≧{T_HI:.0f}°C", 11, C["load"], weight="700")
    cv.text_px((X(T_LO)+X(TB_))/2, Y(94), f"②　相對濕度 ≧ {RH_HI:.0f}%", 13, C["load"],
               weight="700")
    cv.text_px(X(30), Y(80.5), f"③　表面溫度未高於露點 {DEW_DT:.0f}°C 以上", 12.5,
               C["accent"], weight="700")
    cv.text_px(X(26), Y(56), "可施工窗口", 15, C["bmd"], weight="700")

    # 露點界線隨溫度變動：標出兩個算例
    for t in (10.0, 40.0):
        r = rh_at_dew_limit(t)
        cv.parts.append(f'<circle cx="{X(t):.2f}" cy="{Y(r):.2f}" r="4.6" '
                        f'fill="{C["accent"]}" stroke="#FFFFFF" stroke-width="1.8"/>')
        cv.text_px(X(t), Y(r) - 14, f"{t:.0f}°C → {r:.1f}%", 11, C["accent"], weight="700")

    # ── 右側：§7.4.5 不予塗裝部位 ──
    bx = W - Rm + 24
    cv.text_px(bx, 150, "§7.4.5　不予塗裝部位", 13, C["text"], "start", weight="700")
    items = (f"① 工地銲接部位及相鄰兩側各 {NOPAINT_MM:.0f} mm",
             "② 摩阻式高強度螺栓接合面",
             f"③ 埋件（距混凝土面 {NOPAINT_MM:.0f} mm 深仍須塗裝）",
             "④ 軸件、滾輪等密著接觸面或迴轉面",
             "⑤ 密閉空間之內露面")
    for i, t in enumerate(items):
        cv.text_px(bx, 178 + i*26, t, 11.5, C["muted"], "start")

    # 銲接兩側各 100 mm 之小示意
    gx, gy = bx, 340
    cv.rect_px(gx, gy, 250, 34, "#DCE3EC", 4, C["member"], 1.8)
    cv.parts.append(f'<line x1="{gx+125}" y1="{gy-6}" x2="{gx+125}" y2="{gy+40}" '
                    f'stroke="{C["load"]}" stroke-width="3"/>')
    cv.text_px(gx + 125, gy - 14, "工地銲接", 11, C["load"], weight="700")
    cv.rect_px(gx + 55, gy, 140, 34, "rgba(192,57,43,0.16)", 0)
    for x0, x1 in ((gx+55, gx+125), (gx+125, gx+195)):
        cv.parts.append(f'<line x1="{x0}" y1="{gy+50}" x2="{x1}" y2="{gy+50}" '
                        f'stroke="{C["load"]}" stroke-width="1.8"/>')
        for xx in (x0, x1):
            cv.parts.append(f'<line x1="{xx}" y1="{gy+45}" x2="{xx}" y2="{gy+55}" '
                            f'stroke="{C["load"]}" stroke-width="1.8"/>')
        cv.text_px((x0+x1)/2, gy + 66, f"{NOPAINT_MM:.0f} mm", 11, C["load"],
                   weight="700")
    cv.text_px(gx, gy + 92, f"不是 50 mm——兩側各 {NOPAINT_MM:.0f} mm，", 11.5,
               C["load"], "start", weight="700")
    cv.text_px(gx, gy + 112, f"合計 {2*NOPAINT_MM:.0f} mm 範圍內不予塗裝", 11.5,
               C["load"], "start", weight="700")

    cv.text_px(W/2, 34, "圖 3　§7.4.4 的四項限制是「任一成立即不得塗裝」", 17.5,
               C["text"], weight="700")
    cv.text_px(W/2, 58, "四項各切掉圖上一塊區域，剩下的綠色才是可施工窗口", 13, C["muted"])
    cv.text_px(W/2, 84,
               "③ 露點條件不是 ② 的重述：溫度愈低，露點界線愈早咬住（10 °C 時約 "
               f"{rh_at_dew_limit(10.0):.1f}%，已低於 {RH_HI:.0f}%）",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               "只寫「濕度與露點」而漏掉 ① 5 °C 與 ④ 50 °C，等於漏掉一半的環境限制",
               13, C["load"])
    cv.save(os.path.join(OUT, "SS-2019-1-fig-3-env-window.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1_mechanism(); fig2_surface_prep(); fig3_env_window()
    print(f"粗糙度 {RG_LO:.0f}～{RG_HI:.0f} μm；金屬噴塗取上緣 ≧ {RG_SPRAY_MIN:.0f} μm")
    print(f"鋅噴塗 {ZN_LO:.0f}～{ZN_HI:.0f}、鋁噴塗 {AL_LO:.0f}～{AL_HI:.0f} μm；"
          f"封孔 {SEAL_HR:.0f} h")
    for t in (5, 10, 20, 30, 40, 50):
        print(f"  露點界線 @ {t:>2} °C：RH ≦ {rh_at_dew_limit(float(t)):.1f}%"
              f"（露點 {dew_point(float(t), rh_at_dew_limit(float(t))):.1f} °C）")
    print("done ->", OUT)
