#!/usr/bin/env python3
"""SD-2024-3 解題圖解（struct-diagram；2026-11-16 圖解補繪，非勘誤）
圖 1：V*/V 隨 Fu 變化，一般工址（4.2αy）與臺北盆地（3.5αy）兩條線——兩式依工址分列，不是依週期二選一。
圖 2：設計地震力的折減鏈 ISaD·W ÷Fu ÷1.4 ÷αy，與 V* 的位置（例：R = 4.8 長週期、RC 強度設計 αy = 1.5）。
數值全由下列常數與規範關係式算出（建築物耐震設計規範 111 年版 2.9、2.10 節）。
用法：python3 gen_SD-2024-3.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
SKILL = os.environ.get("STRUCTDRAW",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts"))
sys.path.insert(0, SKILL)
from structdraw import Canvas, C
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")

K_GEN, K_TPE = 4.2, 3.5           # 中小度地震分母係數
R_MAX = 4.8
RA_GEN = 1 + (R_MAX - 1) / 1.5    # 一般工址 Ra（長週期 Fu 上限）
RA_TPE = 1 + (R_MAX - 1) / 2.0    # 臺北盆地 Ra
FU_EX, AY_EX = RA_GEN, 1.5        # 圖 2 例：R = 4.8 長週期、RC 強度設計


def ratio(fu, k):                 # V*/V = Fu·1.4/k
    return fu * 1.4 / k


def fig1():
    W, HH = 940, 580
    F0, F1, ymax = 1.0, 3.8, 1.35
    L, R_, T_, B = 96, 200, 100, 120
    sx = (HH - T_ - B) / ymax
    XSC = (W - L - R_) / (sx * (F1 - F0))
    cv = Canvas(W, HH, sx=sx, ox=L, oy=B)
    XM = lambda f: (f - F0) * XSC
    cv.text_px(W / 2, 34, "圖 1　中小度地震 V* 與設計地震 V 的比值：依工址分兩式", 17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, "一般工址（含近斷層）V*/V = Fu/3；臺北盆地 V*/V = 0.4 Fu（與週期無關）", 13, C["muted"])
    cv.axes((0, 0), XM(F1) * 0.99, ymax * 0.99, ("F_{u}", "V^{*}/V"), C["muted"], 1.8)
    cv.line((0, 1.0), (XM(F1) * 0.97, 1.0), C["bmd"], 2.6)
    cv.text_px(cv.X(XM(F1) * 0.97) + 10, cv.Y(1.0), "V*＝V", 13, C["bmd"], "start", weight="700")
    for k, fmax, col, lab in ((K_GEN, RA_GEN, C["sfd"], "一般工址 4.2αy"), (K_TPE, RA_TPE, C["load"], "臺北盆地 3.5αy")):
        pts = [(XM(F0 + i * (fmax - F0) / 200), ratio(F0 + i * (fmax - F0) / 200, k)) for i in range(201)]
        cv.poly(pts, col, 4.0)
        fx = k / 1.4                                   # V* = V 的 Fu
        cv.line((XM(fx), 0), (XM(fx), 1.0), col, 1.6, dash="6 5")
        cv.dot((XM(fx), 1.0), 5.4, col)
        cv.text_px(cv.X(XM(fx)), cv.Y(0) + 40, f"Fu = {fx:.1f}", 12.5, col, weight="700")
        cv.dot((XM(fmax), ratio(fmax, k)), 5.0, col)
        if k == K_TPE:   # 盆地標在端點左上，一般工址標在端點右下，避免重疊
            cv.text_px(cv.X(XM(fmax)) + 6, cv.Y(ratio(fmax, k) + 0.08),
                       f"{lab}：Fu 上限 {fmax:.2f} → {ratio(fmax, k):.3f}", 12.5, col, "end", weight="700")
        else:
            cv.text_px(cv.X(XM(fmax)) - 40, cv.Y(ratio(fmax, k) + 0.08),
                       f"{lab}：Fu 上限 {fmax:.2f} → {ratio(fmax, k):.3f}", 12.5, col, "start", weight="700")
    for f in (1, 2, 3):
        cv.line((XM(f), -0.015), (XM(f), 0.015), C["muted"], 1.2)
        cv.text_px(cv.X(XM(f)), cv.Y(0) + 20, str(f), 11.5, C["muted"])
    for yv in (0.5, 1.0):
        cv.text_px(cv.X(0) - 12, cv.Y(yv), f"{yv:.1f}", 11.5, C["muted"], "end")
    cv.text_px(cv.X(XM(1.6)), cv.Y(1.08), "V* ＞ V：中小度地震控制", 13, C["text"], weight="700")
    cv.text_px(cv.X(XM(1.6)), cv.Y(0.22), "V* ＜ V：設計地震控制", 13, C["text"], weight="700")
    cv.text_px(W / 2, HH - 44, f"Fu 上限取 R = {R_MAX} 長週期：一般工址 Ra = 1+(R−1)/1.5，臺北盆地 Ra = 1+(R−1)/2.0",
               12.5, C["muted"])
    cv.text_px(W / 2, HH - 20, "攔錯：把 4.2／3.5 解為短週期／長週期、兩式取較小；設計力是 V、V*、VM 取最大",
               13.5, C["muted"])
    cv.save(f"{OUT}/SD-2024-3-fig-1-vstar-site.svg")


def fig2():
    W, HH = 960, 520
    cv = Canvas(W, HH, sx=1, bg="#FFFFFF")
    cv.text_px(W / 2, 34, "圖 2　設計地震力的折減鏈：÷Fu → ÷1.4 → ÷αy", 17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, f"例：R = {R_MAX}、長週期（Fu = Ra = {FU_EX:.3f}）、RC 強度設計 αy = {AY_EX}；"
               "設 SaD/Fu ≤ 0.3（修正係數不改值）；以 I·SaD·W = 1 為基準", 12.5, C["muted"])
    v_el = 1.0
    v_u = v_el / FU_EX
    v_y = v_u / 1.4
    v_d = v_y / AY_EX
    v_s = v_el / (K_GEN * AY_EX)
    rows = [("彈性需求 I·SaD·W", v_el, C["member2"], ""),
            ("÷ Fu：形成崩塌機構所需強度", v_u, C["sfd"], f"÷ {FU_EX:.3f}（韌性，等位移法則）"),
            ("÷ 1.4：第一個構材降伏", v_y, C["accent"], "÷ 1.4（系統超強，橋梁 1.2）"),
            ("÷ αy：設計地震力 V", v_d, C["bmd"], f"÷ {AY_EX}（起始降伏地震力放大倍數）"),
            ("中小度地震 V* ＝ I·SaD·W ÷ 4.2αy", v_s, C["load"], "不除 Fu（要求彈性）")]
    x0, bw = 330, 420
    for i, (name, v, col, note) in enumerate(rows):
        y = 112 + i * 64
        cv.text_px(x0 - 14, y, name, 13.5, C["text"], "end", weight="700")
        cv.rect_px(x0, y - 15, bw, 30, "#EDF1F6", 7)
        cv.rect_px(x0, y - 15, max(bw * v, 4), 30, col, 7)
        cv.text_px(x0 + bw * v + 10, y, f"{v:.3f}", 13.5, col, "start", weight="700")
        if note:
            cv.text_px(x0 + bw + 12, y, note, 11.8, C["muted"], "start")
    cv.text_px(W / 2, 112 + 5 * 64 + 6,
               f"V*/V = {v_s/v_d:.3f} = Fu/3 ＞ 1：本例中小度地震控制（臺北盆地 3.5αy 時 V* 更大）",
               14, C["text"], weight="700")
    cv.text_px(W / 2, HH - 22, "攔錯：把 αy 當成代表贅餘度的超強係數、把 ÷αy 與 ÷1.4 的意義對調",
               13.5, C["muted"])
    cv.save(f"{OUT}/SD-2024-3-fig-2-reduction-chain.svg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1(); fig2()
    print(f"RA_GEN={RA_GEN:.4f} RA_TPE={RA_TPE:.4f} V*/V gen max={ratio(RA_GEN,K_GEN):.4f} tpe max={ratio(RA_TPE,K_TPE):.4f}")
    print(f"chain: Vu={1/FU_EX:.4f} Vy={1/FU_EX/1.4:.4f} V={1/FU_EX/1.4/AY_EX:.4f} V*={1/(K_GEN*AY_EX):.4f}")
