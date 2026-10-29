#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2022-3 圖解產生腳本（韌性抗彎構架之重要銲接部位與 NDT）

部位編號、必要／補充 NDT 與選擇理由全部照 §4 之「NDT 方法選擇總表」與
「§4 四、NDT 方法選擇邏輯提醒」，未自行增刪。
執行：python3 gen_SS-2022-3.py   →   figs/*.svg
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
# §4「NDT 方法選擇總表」原文（編號、必要 NDT、補充 NDT）
# ══════════════════════════════════════════════════════════════
SPOTS = (
    ("①",  "梁翼板對柱 CJP",        "UT 100%",   "VT",            "★★★★★"),
    ("①′", "箱型柱內橫隔板↔柱壁 ESW", "UT 全長",   "MT、VT",        "★★★★★"),
    ("②",  "連續板銲道（H 型柱）",    "MT",        "UT（若 CJP）",  "★★★★"),
    ("③",  "面板區加厚板銲道",       "UT 或 MT",  "VT",            "★★★"),
    ("④",  "梁腹板剪力板銲道",       "MT 或 VT",  "—",             "★★"),
    ("⑤",  "柱接合 CJP",            "UT 100%",   "VT",            "★★★"),
    ("⑥",  "柱底板銲道",            "UT 或 MT",  "VT",            "★★★"),
)
BASELINE = ("所有銲道（基線）", "VT 全數", "最基本要求")

# §4 四、NDT 選擇邏輯（缺陷型態 → 方法）
LOGIC = (
    ("面積型內部缺陷", "裂縫、未熔合 LF、未滲透 LP", "UT", "超音波", C["load"]),
    ("體積型內部缺陷", "氣孔、夾渣",                 "RT", "放射線", C["accent"]),
    ("表面／近表面裂縫（磁性材料）", "銲趾裂縫、表面裂縫", "MT", "磁粒", C["bmd"]),
    ("表面／近表面裂縫（非磁性材料）", "沃斯田鐵系不鏽鋼等", "PT", "液滲", C["compr"]),
    ("表面可見缺陷（銲道幾何）", "咬邊、重疊、尺寸不足", "VT", "目視", C["muted"]),
)


def poly_px(cv, pts, fill, stroke, sw, dash=None):
    p = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    d = f' stroke-dasharray="{dash}"' if dash else ''
    cv.parts.append(f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" '
                    f'stroke-width="{sw}"{d}/>')


def line_px(cv, x1, y1, x2, y2, col, sw, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    cv.parts.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                    f'stroke="{col}" stroke-width="{sw}"{d}/>')


def marker(cv, x, y, num, col):
    cv.parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="12" fill="{col}" '
                    f'stroke="#FFFFFF" stroke-width="2.2"/>')
    cv.text_px(x, y, num, 12.5, "#FFFFFF", weight="700")


# ══════════════════════════════════════════════════════════════
def fig1_joint_map():
    """圖 1：重要銲接部位在接頭上的位置"""
    W, H = 1140, 840
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    S = 2.35

    def draw_joint(ox, oy, boxcol):
        """boxcol=True 畫箱型柱（內橫隔板 ESW）；False 畫 H 型柱（連續板）"""
        X = lambda x: ox + x*S
        Y = lambda y: oy - y*S
        CW, CT, CB = 14.0, 84.0, -56.0          # 柱半寬、柱頂、柱底
        BF1, BF2, BF3, BF4 = 10.0, 14.0, 46.0, 50.0   # 梁下翼板／上翼板高程
        BX = 92.0                                # 梁伸出長度
        STEEL, EDGE = "#DCE3EC", C["member"]

        # 柱
        poly_px(cv, [(X(-CW), Y(CB)), (X(CW), Y(CB)), (X(CW), Y(CT)), (X(-CW), Y(CT))],
                STEEL, EDGE, 2.2)
        if boxcol:
            # 內橫隔板（封在柱內，畫虛線表示不可見）
            for y0, y1 in ((BF1, BF2), (BF3, BF4)):
                poly_px(cv, [(X(-CW), Y(y0)), (X(CW), Y(y0)), (X(CW), Y(y1)),
                             (X(-CW), Y(y1))], "#C3D2DC", C["load"], 2.0, dash="6 4")
            cv.text_px(X(0), Y((BF2+BF3)/2), "內橫隔板", 11, C["load"], weight="700")
            cv.text_px(X(0), Y((BF2+BF3)/2) + 17, "（封在柱內）", 10.5, C["load"])
        else:
            # H 型柱：腹板 + 連續板 + 面板區加厚板
            line_px(cv, X(0), Y(CB), X(0), Y(CT), EDGE, 1.6, dash="5 4")
            for y0, y1 in ((BF1, BF2), (BF3, BF4)):
                poly_px(cv, [(X(-CW), Y(y0)), (X(CW), Y(y0)), (X(CW), Y(y1)),
                             (X(-CW), Y(y1))], "#C3D2DC", C["bmd"], 2.0)
            poly_px(cv, [(X(-11), Y(BF2)), (X(11), Y(BF2)), (X(11), Y(BF3)),
                         (X(-11), Y(BF3))], "rgba(180,83,9,0.20)", C["accent"], 1.8)
            cv.text_px(X(0), Y((BF2+BF3)/2), "加厚板", 11, C["accent"], weight="700")
            cv.text_px(X(0), Y((BF2+BF3)/2) + 17, "Panel Zone", 10, C["accent"])

        # 梁
        for y0, y1 in ((BF1, BF2), (BF3, BF4)):
            poly_px(cv, [(X(CW), Y(y0)), (X(BX), Y(y0)), (X(BX), Y(y1)), (X(CW), Y(y1))],
                    STEEL, EDGE, 2.2)
        poly_px(cv, [(X(CW), Y(BF2)), (X(BX), Y(BF2)), (X(BX), Y(BF3)), (X(CW), Y(BF3))],
                "#EDF1F6", EDGE, 1.6)
        cv.text_px(X(BX) - 8, Y((BF2+BF3)/2), "梁", 12, C["member"], "end", weight="700")

        # 剪力板
        poly_px(cv, [(X(CW), Y(18)), (X(CW+20), Y(18)), (X(CW+20), Y(42)), (X(CW), Y(42))],
                "#B9C6D4", C["member"], 1.8)

        # 柱接合（CJP）
        line_px(cv, X(-CW), Y(68), X(CW), Y(68), C["load"], 3.0)
        # 柱底板
        poly_px(cv, [(X(-26), Y(CB-7)), (X(26), Y(CB-7)), (X(26), Y(CB)), (X(-26), Y(CB))],
                "#B9C6D4", C["member"], 2.2)
        return X, Y, CW, BF1, BF2, BF3, BF4

    # ── 左：箱型柱 ──
    XA, YA, CW, BF1, BF2, BF3, BF4 = draw_joint(250, 400, True)
    cv.text_px(250, 128, "國內常見：箱型柱＋內橫隔板", 14, C["text"], weight="700")
    cv.text_px(250, 150, "隔板端部以 ESW 自柱外一道成形", 11.5, C["muted"])
    marker(cv, XA(CW), YA(BF4), "①", C["load"])
    marker(cv, XA(-CW), YA(BF3), "①′", C["load"])
    marker(cv, XA(CW+20), YA(30), "④", C["bmd"])
    marker(cv, XA(0), YA(68), "⑤", C["accent"])
    marker(cv, XA(0), YA(-56), "⑥", C["accent"])

    # ── 右：H 型柱 ──
    XB, YB, *_ = draw_joint(700, 400, False)
    cv.text_px(700, 128, "H 型柱：以連續板取代內橫隔板", 14, C["text"], weight="700")
    cv.text_px(700, 150, "功能相同，但銲道看得見、修得到", 11.5, C["muted"])
    marker(cv, XB(CW), YB(BF4), "①", C["load"])
    marker(cv, XB(-CW), YB(BF3), "②", C["bmd"])
    marker(cv, XB(-CW), YB(30), "③", C["accent"])
    marker(cv, XB(CW+20), YB(30), "④", C["bmd"])

    # ── 下：對照表 ──
    ty = 592
    cols = (0, 300, 470, 620)
    heads = ("銲接部位", "必要 NDT", "補充", "重要性")
    tx = 88
    for cx, hd in zip(cols, heads):
        cv.text_px(tx + cx, ty, hd, 12, C["muted"], "start", weight="700")
    line_px(cv, tx - 8, ty + 10, tx + 760, ty + 10, C["muted"], 1.4)
    for i, (num, nm, need, extra, imp) in enumerate(SPOTS):
        y = ty + 30 + i*22
        col = C["load"] if num in ("①", "①′") else (
            C["bmd"] if num in ("②", "④") else C["accent"])
        cv.text_px(tx, y, num, 12, col, "start", weight="700")
        cv.text_px(tx + 34, y, nm, 12, C["text"], "start")
        cv.text_px(tx + cols[1], y, need, 12, col, "start", weight="700")
        cv.text_px(tx + cols[2], y, extra, 11.5, C["muted"], "start")
        cv.text_px(tx + cols[3], y, imp, 11.5, col, "start")
    y = ty + 30 + len(SPOTS)*22 + 6
    cv.text_px(tx + 34, y, BASELINE[0], 12, C["muted"], "start")
    cv.text_px(tx + cols[1], y, BASELINE[1], 12, C["muted"], "start", weight="700")
    cv.text_px(tx + cols[2], y, BASELINE[2], 11.5, C["muted"], "start")

    cv.text_px(W/2, 34, "圖 1　韌性抗彎構架的重要銲接部位在哪裡", 17.5, C["text"],
               weight="700")
    cv.text_px(W/2, 58,
               "容量設計要求塑鉸出現在梁端，柱端與 Panel Zone 保持彈性——"
               "所以梁端這幾道銲道的品質就是整個構架的韌性",
               13, C["muted"])
    cv.text_px(W/2, 84,
               "①′ 的 ESW 用在「內橫隔板與柱壁」，不是剪力板；"
               "剪力板（④）與柱面是填角銲／CJP",
               12.5, C["load"])
    cv.save(os.path.join(OUT, "SS-2022-3-fig-1-joint-map.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_ndt_logic():
    """圖 2：缺陷型態決定 NDT 方法"""
    W, H = 1080, 572
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")

    x0, xm, xr = 70, 545, 660
    cv.text_px(x0, 132, "缺陷型態", 12, C["muted"], "start", weight="700")
    cv.text_px(x0 + 240, 132, "典型缺陷", 12, C["muted"], "start", weight="700")
    cv.text_px(xm + 24, 132, "方法", 12, C["muted"], "start", weight="700")
    cv.text_px(xr + 20, 132, "本題用在哪", 12, C["muted"], "start", weight="700")
    cv.parts.append(f'<line x1="{x0-8}" y1="142" x2="{W-56}" y2="142" '
                    f'stroke="{C["muted"]}" stroke-width="1.4"/>')

    where = ("①梁翼板 CJP、①′ESW、⑤柱接合、③加厚板",
             "（本題各部位皆非首選）",
             "②連續板、④剪力板、③加厚板表面",
             "（鋼結構為磁性材料，通常用 MT）",
             "所有銲道之基線要求")
    for i, ((kind, ex, abbr, zh, col), wh) in enumerate(zip(LOGIC, where)):
        y = 180 + i*76
        cv.rect_px(x0 - 8, y - 24, W - 118, 56,
                   "#F5F7FA" if i % 2 == 0 else "#FFFFFF", 8)
        cv.text_px(x0, y - 6, kind, 12.5, C["text"], "start", weight="700")
        cv.text_px(x0 + 240, y - 6, ex, 11.5, C["muted"], "start")
        cv.parts.append(f'<polygon points="{xm},{y-8} {xm+18},{y} {xm},{y+8}" '
                        f'fill="{col}"/>')
        cv.rect_px(xm + 24, y - 17, 96, 34, col, 7)
        cv.text_px(xm + 44, y, abbr, 15, "#FFFFFF", "start", weight="700")
        cv.text_px(xm + 112, y, zh, 11, "#FFFFFF", "end")
        cv.text_px(xr + 20, y - 6, wh, 11.5, col if i != 1 else C["muted"], "start")
        if i == 0:
            cv.text_px(xr + 20, y + 14, "全滲透銲道最怕 LF／LP，正是 UT 最靈敏者",
                       11, C["load"], "start", weight="700")
        if i == 1:
            cv.text_px(xr + 20, y + 14, "RT 對面積型缺陷靈敏度差，且射線防護困難",
                       11, C["load"], "start")

    cv.text_px(W/2, 34, "圖 2　NDT 不是憑重要性挑，是憑「怕什麼缺陷」挑", 17.5,
               C["text"], weight="700")
    cv.text_px(W/2, 58, "先問這道銲道最可能出什麼缺陷、缺陷在表面還是內部，方法就定了",
               13, C["muted"])
    cv.text_px(W/2, 84,
               "把梁翼板 CJP 寫成「RT 100%」是最常見的錯：CJP 怕的是面積型的未熔合／未滲透，"
               "不是氣孔夾渣",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               "反過來也一樣——填角銲（④剪力板）幾何不規則，UT 困難，"
               "表面檢測的 MT／VT 才是對的答案",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2022-3-fig-2-ndt-logic.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_esw_diaphragm():
    """圖 3：內橫隔板為何只能 ESW、又為何只能 UT"""
    PWD, PH = 380, 470
    XL, XR, YL, YH = -72.0, 62.0, -52.0, 62.0
    Lm, Tm, Bm = 24, 106, 130
    sx = min((PWD-2*Lm)/(XR-XL), (PH-Tm-Bm)/(YH-YL))
    OX, OY = Lm - XL*sx, Bm - YL*sx
    TW = 8.0                       # 柱壁厚
    HW = 34.0                      # 柱半寬（內側）

    # ── 格 1：組立順序決定了施銲方向 ──
    p1 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p1.panel("① 為什麼只能用 ESW", "柱之水平斷面（俯視）")
    # 先組立的三面柱壁
    for (x0, x1), (y0, y1) in (((-HW-TW, -HW), (-HW-TW, HW+TW)),
                               ((-HW, HW), (HW, HW+TW)),
                               ((-HW, HW), (-HW-TW, -HW))):
        p1.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                   "#C3D2DC", C["member"], 2.0)
    # 置入之內橫隔板
    p1.polygon([(-HW, -HW), (HW, -HW), (HW, HW), (-HW, HW)],
               "rgba(192,57,43,0.10)", C["load"], 2.0)
    p1.text_px(p1.X(0), p1.Y(4), "內橫隔板", 12, C["load"], weight="700")
    p1.text_px(p1.X(0), p1.Y(-6), "（置入後）", 10.5, C["load"])
    # 三面：柱內可施銲
    for pts in (((-HW, -HW), (-HW, HW)), ((-HW, HW), (HW, HW)),
                ((-HW, -HW), (HW, -HW))):
        p1.poly(list(pts), C["bmd"], 4.0)
    p1.text_px(p1.X(-HW-TW) - 8, p1.Y(0), "三面", 10.5, C["bmd"], "end", weight="700")
    p1.text_px(p1.X(-HW-TW) - 8, p1.Y(-10), "柱內", 10.5, C["bmd"], "end", weight="700")
    p1.text_px(p1.X(-HW-TW) - 8, p1.Y(-20), "可施銲", 10.5, C["bmd"], "end", weight="700")
    # 第四片柱壁合攏後，只能自柱外施銲
    p1.polygon([(HW, -HW-TW), (HW+TW, -HW-TW), (HW+TW, HW+TW), (HW, HW+TW)],
               "#EDF1F6", C["accent"], 2.2)
    p1.poly([(HW, -HW), (HW, HW)], C["load"], 4.0)
    p1.arrow((HW+TW+16, 0), (HW+TW+1, 0), C["load"], 2.8, 9)
    p1.text_px(p1.X(HW+TW+20), p1.Y(6), "ESW", 12, C["load"], "start", weight="700")
    p1.text_px(p1.X(HW+TW+20), p1.Y(-6), "自柱外", 11, C["load"], "start", weight="700")
    p1.text_px(p1.X(HW+TW/2), p1.Y(HW+TW+7), "第四片", 10.5, C["accent"], weight="700")
    p1.text_px(PWD/2, PH - 96, "三面柱壁先組立、隔板置入，", 12, C["muted"])
    p1.text_px(PWD/2, PH - 74, "最後一片合攏後柱內再也進不去", 12, C["muted"])
    p1.text_px(PWD/2, PH - 48, "⇒ 只能自柱外一道成形", 12.5, C["load"], weight="700")
    p1.text_px(PWD/2, PH - 26, "＝電熱熔渣銲 ESW", 12.5, C["load"], weight="700")
    p1.text_px(PWD/2, PH - 6, "（不是為了效率才選它）", 11, C["muted"])

    # ── 格 2：ESW 帶來什麼問題 ──
    p2 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p2.panel("② ESW 換來的代價", "大熱輸入 ⇒ 冷卻極慢")
    # 柱壁（左）＋隔板（右），中間為銲道與 HAZ
    p2.polygon([(-58, -34), (-10, -34), (-10, 44), (-58, 44)], "#DCE3EC", C["member"], 2.0)
    p2.text_px(p2.X(-34), p2.Y(38), "柱壁", 11.5, C["member"], weight="700")
    p2.polygon([(14, -34), (58, -34), (58, 44), (14, 44)],
               "rgba(192,57,43,0.10)", C["load"], 2.0)
    p2.text_px(p2.X(44), p2.Y(38), "內橫隔板", 11.5, C["load"], weight="700")
    p2.polygon([(-10, -34), (14, -34), (14, 44), (-10, 44)], C["fill_t"], C["load"], 2.0)
    p2.text_px(p2.X(2), p2.Y(28), "ESW", 12, C["load"], weight="700")
    p2.text_px(p2.X(2), p2.Y(18), "銲道", 11, C["load"])
    for x0, x1 in ((-26, -10), (14, 30)):
        p2.polygon([(x0, -34), (x1, -34), (x1, 44), (x0, 44)],
                   "rgba(180,83,9,0.26)", C["accent"], 1.6)
    p2.text_px(p2.X(-18), p2.Y(-24), "HAZ", 11, C["accent"], weight="700")
    p2.text_px(p2.X(22), p2.Y(-24), "HAZ", 11, C["accent"], weight="700")
    p2.arrow((-26, -44), (-10, -44), C["accent"], 2.0, 7)
    p2.arrow((-10, -44), (-26, -44), C["accent"], 2.0, 7)
    p2.text_px(p2.X(-18), p2.Y(-50), "HAZ 特別寬", 10.5, C["accent"], weight="700")
    p2.text_px(PWD/2, PH - 96, "冷卻慢 ⇒ HAZ 晶粒粗大 ⇒ CVN 韌性大幅下降", 12,
               C["accent"], weight="700")
    p2.text_px(PWD/2, PH - 74, "是耐震接頭最典型的脆化來源", 11.5, C["muted"])
    p2.text_px(PWD/2, PH - 48, "典型缺陷：未熔合 LOF ＋ 夾渣", 12.5, C["load"],
               weight="700")
    p2.text_px(PWD/2, PH - 26, "——LOF 是面狀缺陷，RT 不敏感", 12, C["load"])
    p2.text_px(PWD/2, PH - 6, "完工後封在柱內，無法目視、難以修補", 11, C["muted"])

    # ── 格 3：只能 UT，不能 RT ──
    p3 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p3.panel("③ 為什麼是 UT 不是 RT", "檢測要能從柱外進行")
    p3.polygon([(-58, -34), (-10, -34), (-10, 44), (-58, 44)], "#DCE3EC", C["member"], 2.0)
    p3.polygon([(-10, -34), (14, -34), (14, 44), (-10, 44)], C["fill_t"], C["load"], 2.0)
    p3.polygon([(14, -34), (58, -34), (58, 44), (14, 44)],
               "rgba(192,57,43,0.10)", C["load"], 2.0)
    p3.text_px(p3.X(-34), p3.Y(38), "柱壁", 11.5, C["member"], weight="700")
    p3.text_px(p3.X(36), p3.Y(38), "隔板（柱內）", 11, C["load"], weight="700")
    # UT 探頭自柱壁外側入射
    p3.polygon([(-70, 4), (-58, 4), (-58, 18), (-70, 18)], C["bmd"], C["bmd"], 1.6)
    p3.text_px(p3.X(-64), p3.Y(26), "UT 探頭", 10.5, C["bmd"], weight="700")
    p3.arrow((-58, 12), (-2, 0), C["bmd"], 2.4, 8)
    p3.arrow((-2, 0), (-58, -12), C["bmd"], 2.4, 8)
    p3.text_px(p3.X(-34), p3.Y(-42), "入射／回波皆在柱外", 10.5, C["bmd"], weight="700")
    # RT 需要底片放柱內 —— 做不到
    p3.text_px(p3.X(38), p3.Y(8), "RT 底片", 10.5, C["load"], weight="700")
    p3.text_px(p3.X(38), p3.Y(-2), "須放這裡", 10.5, C["load"], weight="700")
    p3.text_px(p3.X(38), p3.Y(-14), "× 進不去", 12, C["load"], weight="700")
    p3.text_px(PWD/2, PH - 96, "UT：探頭與回波同側，自柱壁外表面即可全長掃描",
               11.5, C["bmd"], weight="700")
    p3.text_px(PWD/2, PH - 74, "柱壁外表面另補 MT 查表面／近表面裂縫，VT 為基本",
               11.5, C["bmd"])
    p3.text_px(PWD/2, PH - 48, "RT：射源與底片須分置兩側", 12.5, C["load"], weight="700")
    p3.text_px(PWD/2, PH - 26, "柱壁厚、幾何封閉 ⇒ 在此完全不可行", 12, C["load"])
    p3.text_px(PWD/2, PH - 6, "（不是「精度不夠」，是根本放不進去）", 11, C["muted"])

    compose([p1, p2, p3], cols=3,
            title="圖 3　①′ 箱型柱內橫隔板 ESW：本題最高階的得分點",
            sub="能寫出「ESW 是因為隔板無法自柱內施銲才不得不用，"
                "其大熱輸入正是 HAZ 脆化的根源」，就掌握了這一分",
            note="設計端若改採貫通式隔板或外隔板即不需 ESW，"
                 "銲道也回到可目視、可修補的位置——這是可以在答案裡加分的一句",
            path=os.path.join(OUT, "SS-2022-3-fig-3-esw-diaphragm.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1_joint_map(); fig2_ndt_logic(); fig3_esw_diaphragm()
    print(f"部位共 {len(SPOTS)} 處，另加基線 VT 全數")
    for num, nm, need, extra, imp in SPOTS:
        print(f"  {num:<3}{nm:<24}必要 {need:<10}補充 {extra}")
    print("done ->", OUT)
