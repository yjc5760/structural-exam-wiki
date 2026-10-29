#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2021-1 圖解產生腳本（填角銲四種瑕疵之辨識與 NDT 配對）

瑕疵幾何由「缺料／多料、在銲材／在母材」兩個判準決定；RT 路徑長度由斷面幾何算出。
執行：python3 gen_SS-2021-1.py   →   figs/*.svg
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
# 由 SS-2021-1 §4 之判讀結果取得（幾何為繪圖單位，比例依斷面示意）
# ══════════════════════════════════════════════════════════════
TB   = 10.0      # 底板厚
TV   = 8.0       # 直立板厚
WLEG = 16.0      # 填角銲腳（左右各一道）
MT_DEPTH = 3.0   # mm  MT 之有效深度（近表面約 3 mm）        §4 ③

# 四處瑕疵：標號 → (名稱, 在哪裡, 缺料/多料, 主選 NDT, 次選)
DEFECTS = (
    ("a", "咬邊 Undercut",        "母材（直立板）", "缺料", "VT", "MT"),
    ("b", "銲道裂縫 Weld Crack",  "銲材內",         "裂縫", "MT", "PT"),
    ("c", "重疊 Overlap",         "銲材翻捲於母材上", "多料", "VT", "PT"),
    ("d", "母材／HAZ 裂縫（層狀撕裂）", "母材（底板）內", "裂縫", "UT", "MT"),
)
NDT_USED = [d[4] for d in DEFECTS]          # VT, MT, VT, UT —— RT 一次都沒用到

# 五種 NDT：名稱 → (可測最大深度[mm]，可測缺陷型態)
NDT = (
    ("VT", "目視",   0.0,  "表面幾何"),
    ("PT", "液滲",   0.0,  "表面開口"),
    ("MT", "磁粒",   MT_DEPTH, "表面／近表面裂縫"),
    ("RT", "放射線", 999.0, "內部體積型"),
    ("UT", "超音波", 999.0, "內部面積型"),
)


# ══════════════════════════════════════════════════════════════
def fig1_defects():
    """圖 1：T 型填角銲斷面與四處瑕疵的幾何"""
    W, H = 960, 560
    XL, XR = -44.0, 44.0
    YL, YH = -16.0, 42.0
    Lm, Rm, Tm, Bm = 56, 56, 118, 100
    sx = min((W-Lm-Rm)/(XR-XL), (H-Tm-Bm)/(YH-YL))
    ox = (W - (XR-XL)*sx)/2 - XL*sx
    cv = Canvas(W, H, sx=sx, ox=ox, oy=Bm - YL*sx, bg="#FFFFFF")

    # 底板（翼板）與直立板（腹板）
    cv.polygon([(-40, 0), (40, 0), (40, TB), (-40, TB)], "#DCE3EC", C["member"], 2.4)
    cv.polygon([(-TV/2, TB), (TV/2, TB), (TV/2, 38), (-TV/2, 38)], "#DCE3EC", C["member"], 2.4)
    cv.text_px(cv.X(-30), cv.Y(TB/2), "底板", 12, C["muted"])
    cv.text_px(cv.X(0), cv.Y(38) - 16, "直立板", 12, C["muted"])
    # 折斷符號
    for xx in (-40, 40):
        cv.poly([(xx, -1.4), (xx + (1.6 if xx < 0 else -1.6), 1.0),
                 (xx + (-1.6 if xx < 0 else 1.6), TB-1.0), (xx, TB+1.4)], C["member"], 1.8)

    # 左右兩道填角銲（三角形；左側含 a、b、c，右側含 d）
    cv.polygon([(-TV/2, TB), (-TV/2, TB+WLEG), (-TV/2 - WLEG, TB)], C["fill_t"], C["member2"], 2.2)
    cv.polygon([(TV/2, TB), (TV/2, TB+WLEG), (TV/2 + WLEG, TB)], C["fill_t"], C["member2"], 2.2)
    cv.text_px(cv.X(TV/2 + WLEG*0.45), cv.Y(TB + WLEG*0.30), "填角銲", 11.5, C["muted"])

    # ── a：上銲趾處母材被熔蝕出凹口（缺料）──
    ax, ay = -TV/2, TB + WLEG
    cv.polygon([(ax, ay-2.6), (ax+2.8, ay+0.4), (ax, ay+3.4)], "#FFFFFF", C["bmd"], 2.2)
    cv.dot((ax + 1.2, ay + 0.4), 4.6, fill=C["bmd"])
    cv.line((ax + 1.2, ay + 0.4), (-24, 34), C["bmd"], 1.3, dash="4 3")
    cv.text_px(cv.X(-24) - 6, cv.Y(34), "a　咬邊：母材被挖出凹口（缺料）", 12.5, C["bmd"],
               "end", weight="700")

    # ── b：銲材內、自銲面開口並分岔的鋸齒線 ──
    bx0, by0 = -TV/2 - WLEG*0.52, TB + WLEG*0.46
    zig = [(bx0, by0), (bx0+1.5, by0-1.8), (bx0+0.4, by0-3.4), (bx0+2.0, by0-5.0),
           (bx0+1.1, by0-6.4)]
    cv.poly(zig, C["load"], 2.6)
    cv.poly([(bx0+0.4, by0-3.4), (bx0-1.4, by0-4.8)], C["load"], 2.2)
    cv.dot((bx0, by0), 4.6, fill=C["load"])
    cv.line((bx0, by0), (-30, 26), C["load"], 1.3, dash="4 3")
    cv.text_px(cv.X(-30) - 6, cv.Y(26), "b　銲道裂縫：銲材內、自表面開口分岔", 12.5,
               C["load"], "end", weight="700")

    # ── c：下銲趾銲材翻捲、平舖於底板上（多料、未熔合）──
    cx0 = -TV/2 - WLEG
    cv.polygon([(cx0, TB), (cx0 - 6.2, TB + 1.9), (cx0 - 7.6, TB + 0.2), (cx0 - 1.0, TB)],
               C["fill_s"], C["sfd"], 2.2)
    cv.line((cx0 - 7.0, TB), (cx0 - 0.6, TB), C["sfd"], 2.0, dash="3 2")
    cv.dot((cx0 - 4.0, TB + 1.0), 4.6, fill=C["sfd"])
    cv.line((cx0 - 4.0, TB + 1.0), (-30, 16), C["sfd"], 1.3, dash="4 3")
    cv.text_px(cv.X(-30) - 6, cv.Y(16), "c　重疊：銲材翻捲外舖、未與母材熔合（多料）",
               12.5, C["sfd"], "end", weight="700")

    # ── d：右側下銲趾正下方，往底板厚度方向的鋸齒線（母材內）──
    dx0, dy0 = TV/2 + WLEG*0.94, TB
    dz = [(dx0, dy0), (dx0-1.4, dy0-2.2), (dx0+0.6, dy0-3.8), (dx0-0.9, dy0-6.2),
          (dx0+0.4, dy0-8.4)]
    cv.poly(dz, C["accent"], 2.8)
    cv.dot((dx0, dy0), 4.6, fill=C["accent"])
    cv.line((dx0, dy0 - 5.0), (30, -8), C["accent"], 1.3, dash="4 3")
    cv.text_px(cv.X(30) + 6, cv.Y(-8), "d　母材／HAZ 裂縫：往板厚方向", 12.5, C["accent"],
               "start", weight="700")
    cv.text_px(cv.X(30) + 6, cv.Y(-8) + 18, "（受拘束時即層狀撕裂）", 11.5, C["accent"],
               "start")

    cv.text_px(W/2, 34, "圖 1　四處瑕疵的斷面幾何——先讀幾何再定名", 17.5,
               C["text"], weight="700")
    cv.text_px(W/2, 58,
               "兩個問題答完，名稱就唯一：① 缺料還是多料　② 在銲材裡還是在母材裡",
               13, C["muted"])
    cv.text_px(W/2, 84,
               "咬邊與重疊都在銲趾、方向卻相反：咬邊少肉是缺口，重疊多肉是假接",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               "圖中沒有任何圓形空洞或不規則夾雜——四處全是表面或自表面起始的缺陷",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2021-1-fig-1-defects.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_ndt_map():
    """圖 2：五種 NDT 的適用範圍，以及 a～d 落在哪一格"""
    W, H = 980, 560
    Lm, Rm, Tm, Bm = 150, 60, 118, 108
    COLS = ("表面幾何", "表面／近表面裂縫", "內部面積型", "內部體積型")
    ROWS = ("表面", "近表面（約 3 mm）", "內部")
    cw = (W - Lm - Rm)/len(COLS)
    ch = (H - Tm - Bm)/len(ROWS)
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    X = lambda j: Lm + j*cw
    Y = lambda i: Tm + i*ch

    for i in range(len(ROWS)):
        for j in range(len(COLS)):
            cv.rect_px(X(j)+3, Y(i)+3, cw-6, ch-6, "#F5F7FA", 8, C["border"], 1.2)
    for j, c in enumerate(COLS):
        cv.text_px(X(j)+cw/2, Tm - 16, c, 12.5, C["text"], weight="700")
    for i, r in enumerate(ROWS):
        cv.text_px(Lm - 14, Y(i)+ch/2, r, 12.5, C["text"], "end", weight="700")

    # 五種方法覆蓋哪些格（依 §4 之適用缺陷與限制）
    COVER = {"VT": [(0, 0)],
             "PT": [(0, 0), (0, 1)],
             "MT": [(0, 1), (1, 1)],
             "UT": [(2, 1), (2, 2)],
             "RT": [(2, 3)]}
    COL_OF = {"VT": C["bmd"], "PT": C["compr"], "MT": C["load"],
              "UT": C["accent"], "RT": C["muted"]}
    SLOT = {}                                  # 同一格內多個標籤的堆疊位置
    for nm in ("VT", "PT", "MT", "UT", "RT"):
        for (i, j) in COVER[nm]:
            k = SLOT.get((i, j), 0); SLOT[(i, j)] = k + 1
            cv.rect_px(X(j)+14, Y(i)+16+k*30, cw-28, 24, COL_OF[nm], 6)
            zh = {"VT": "目視", "PT": "液滲", "MT": "磁粒",
                  "UT": "超音波", "RT": "放射線"}[nm]
            cv.text_px(X(j)+cw/2, Y(i)+28+k*30, f"{nm}　{zh}", 12.5, "#FFFFFF", weight="700")

    # a～d 的落點
    PLACE = {"a": (0, 0), "b": (0, 1), "c": (0, 0), "d": (2, 1)}
    OFF = {}
    for tag, name, where, kind, main, alt in DEFECTS:
        i, j = PLACE[tag]
        k = OFF.get((i, j), 0); OFF[(i, j)] = k + 1
        px = X(j) + 30 + k*84
        py = Y(i) + ch - 22
        cv.parts.append(f'<circle cx="{px}" cy="{py}" r="12" fill="#FFFFFF" '
                        f'stroke="{C["text"]}" stroke-width="2"/>')
        cv.text_px(px, py, tag, 13, C["text"], weight="700")
        cv.text_px(px + 16, py, f"→ {main}", 11.5, C["muted"], "start")

    # RT 未被用到
    xr, yr = X(3), Y(2)
    cv.parts.append(f'<line x1="{xr+14}" y1="{yr+14}" x2="{xr+cw-14}" y2="{yr+ch-14}" '
                    f'stroke="{C["load"]}" stroke-width="2.6"/>')
    cv.parts.append(f'<line x1="{xr+cw-14}" y1="{yr+14}" x2="{xr+14}" y2="{yr+ch-14}" '
                    f'stroke="{C["load"]}" stroke-width="2.6"/>')
    cv.text_px(xr+cw/2, yr+ch-18, "本題無此類缺陷", 12, C["load"], weight="700")

    cv.text_px(W/2, 34, "圖 2　NDT 的適用範圍：深度 × 缺陷型態", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58, "「適合」二字考的是限制條件：測得到多深、測得到哪一種缺陷",
               13, C["muted"])
    cv.text_px(W/2, 84,
               f"四小題用掉 {NDT_USED.count('VT')} 次 VT、{NDT_USED.count('MT')} 次 MT、"
               f"{NDT_USED.count('UT')} 次 UT——RT 一次都沒用到",
               12.5, C["accent"])
    cv.text_px(W/2, H - 50,
               "MT 限鐵磁性材料、有效深度約 3 mm、檢後須消磁；PT 材質不限但只測表面開口",
               13, C["muted"])
    cv.text_px(W/2, H - 26,
               "d 在母材內往板厚方向延伸，表面只看得到起始一小段 ⇒ 只有 UT 能定量深度",
               12.5, C["accent"])
    cv.save(os.path.join(OUT, "SS-2021-1-fig-2-ndt-map.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_rt_fillet():
    """圖 3：填角銲為何不用 RT——射線路徑長度沿位置變化"""
    PWD, PH = 500, 470

    def path_len_butt(x):
        """對接銲：厚度處處相同"""
        return TB

    def path_len_fillet(x):
        """填角銲：射線鉛垂穿過『底板 + 三角形銲道』之總厚度
        銲道斷面為直角三角形，斜邊自 (0, TB+WLEG) 到 (WLEG, TB)"""
        if x < 0:
            return TB
        if x > WLEG:
            return TB
        return TB + (WLEG - x)

    XS = [(-6.0 + 30.0*i/240) for i in range(241)]

    # ── 格 1：兩種接頭的斷面與射線 ──
    XL, XR, YL, YH = -14.0, 26.0, -8.0, 36.0
    Lm, Tm, Bm = 40, 112, 116
    sx = min((PWD-2*Lm)/(XR-XL), (PH-Tm-Bm)/(YH-YL))
    p1 = Canvas(PWD, PH, sx=sx, ox=Lm - XL*sx, oy=Bm - YL*sx)
    p1.panel("斷面與射線路徑", "射線鉛垂入射，底片在下")
    # 對接銲（左）以灰色示意
    p1.polygon([(-12, 0), (-5, 0), (-5, TB), (-12, TB)], "#EDF1F6", C["muted"], 1.8)
    p1.line((-8.5, 0), (-8.5, TB), C["muted"], 2.0, dash="3 2")
    p1.text_px(p1.X(-8.5), p1.Y(TB) - 14, "對接銲", 11.5, C["muted"], weight="700")
    # 填角銲（右）：T 型接頭之底板 + 直立板 + 三角形銲道
    p1.polygon([(-2, 0), (24, 0), (24, TB), (-2, TB)], "#DCE3EC", C["member"], 2.2)
    p1.polygon([(-2, TB), (0, TB), (0, TB+22), (-2, TB+22)], "#DCE3EC", C["member"], 2.2)
    p1.polygon([(0, TB), (0, TB+WLEG), (WLEG, TB)], C["fill_t"], C["load"], 2.2)
    p1.text_px(p1.X(12), p1.Y(TB) - 14, "填角銲", 11.5, C["load"], weight="700")
    for x in (0.0, WLEG*0.35, WLEG*0.7, WLEG):
        p1.arrow((x, 30), (x, path_len_fillet(x) + 1.0), C["accent"], 1.8, 7)
    p1.text_px(p1.X(WLEG/2), p1.Y(31) - 12, "射線", 11.5, C["accent"], weight="700")
    p1.line((-3.0, -3.0), (25.0, -3.0), C["member2"], 3.0)
    p1.text_px(p1.X(11), p1.Y(-3) + 18, "底片", 11.5, C["muted"])
    p1.text_px(PWD/2, PH - 40, "填角銲的穿透厚度沿位置連續變化", 12.5, C["load"],
               weight="700")
    p1.text_px(PWD/2, PH - 18, "底片密度沒有可比的基準", 12, C["muted"])

    # ── 格 2：路徑長度曲線 ──
    p2 = Canvas(PWD, PH, sx=1)
    p2.panel("穿透厚度沿位置的變化", "縱軸為射線經過的鋼材總厚度")
    L2, R2, T2, B2 = 76, 44, 118, 116
    sxx = (PWD - L2 - R2)/30.0
    ymax = (TB + WLEG)*1.18
    syy = (PH - T2 - B2)/ymax
    X2 = lambda x: L2 + (x + 6.0)*sxx
    Y2 = lambda v: PH - B2 - v*syy
    p2.parts.append(f'<line x1="{L2}" y1="{Y2(0)}" x2="{X2(24)}" y2="{Y2(0)}" '
                    f'stroke="{C["muted"]}" stroke-width="1.8"/>')
    p2.parts.append(f'<line x1="{L2}" y1="{Y2(0)}" x2="{L2}" y2="{Y2(ymax)}" '
                    f'stroke="{C["muted"]}" stroke-width="1.8"/>')
    for v in (10, 20):
        p2.text_px(L2 - 10, Y2(v), f"{v}", 11.5, C["muted"], "end")
    for nm, fn, col in (("對接銲", path_len_butt, C["muted"]),
                        ("填角銲", path_len_fillet, C["load"])):
        pts = " ".join(f"{X2(x):.2f},{Y2(fn(x)):.2f}" for x in XS)
        p2.parts.append(f'<polyline points="{pts}" fill="none" stroke="{col}" '
                        f'stroke-width="3.2" stroke-linejoin="round"/>')
        xl_ = 5.0
        p2.text_px(X2(xl_) + (26 if nm == "填角銲" else 26), Y2(fn(xl_)) - 14, nm, 12, col,
                   "start", weight="700")
    p2.text_px(X2(9), Y2(ymax) - 6, f"厚度自 {TB+WLEG:g} 變到 {TB:g}", 12, C["load"],
               weight="700")
    p2.text_px(PWD/2, PH - 62,
               f"變化幅度 {100*(WLEG)/(TB):.0f}%（{TB:g} → {TB+WLEG:g}）", 13, C["load"],
               weight="700")
    p2.text_px(PWD/2, PH - 38, "對接銲厚度均勻，可設定單一曝光參數", 12, C["muted"])
    p2.text_px(PWD/2, PH - 16, "填角銲的密度差被幾何效應淹沒", 12, C["muted"])

    compose([p1, p2], cols=2,
            title="圖 3　填角銲為何實務上不做 RT",
            sub="RT 量的是「衰減差」，前提是斷面厚度均勻、底片密度有基準可比",
            note="且直立板阻擋，射源與底片難以分置兩側；填角銲實務以 VT + MT／PT 為主，"
                 "需深度資訊時用 UT",
            path=os.path.join(OUT, "SS-2021-1-fig-3-rt-fillet.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1_defects(); fig2_ndt_map(); fig3_rt_fillet()
    for tag, name, where, kind, main, alt in DEFECTS:
        print(f"  {tag}: {name:<22} 位置={where:<14} {kind:<4} 主選={main} 次選={alt}")
    print(f"用到的 NDT：{NDT_USED}　RT 次數 = {NDT_USED.count('RT')}")
    print(f"填角銲穿透厚度：{TB:g} → {TB+WLEG:g}（變化 {100*WLEG/TB:.0f}%）")
    print("done ->", OUT)
