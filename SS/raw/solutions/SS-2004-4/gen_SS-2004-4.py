#!/usr/bin/env python3
"""
SS-2004-4 斜置懸臂梁柱構材（ASD，弱軸彎曲＋軸壓）— 題目附圖重繪腳本

用法：
    python3 gen_SS-2004-4.py [輸出目錄]

重繪依據：題目正本 SS-2004-4-problem.md §4 判讀清單（待確認）。
圖上每個支承、角度、載重都對應清單一項；只畫考卷給的東西，不含任何解題結果
（P 的分量、f_a、f_b、KL 都不畫）。
構材長度為示意比例（L = 350 cm 只標符號 L，照考卷）；斷面小圖為示意（題未給板件尺寸）。
自由端兩個弧形箭頭依清單 #5 判為 45° 角度標註，重繪成角度弧，不畫成外加彎矩。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2004-4"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2004-4-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
ANG_P = 45.0         # #1 構材軸線與鉛直 P 夾 45°（構材與水平亦 45°）
ANG_WALL = 90.0      # #3 構材與固定端牆面夾 90°
LEN = 1.0            # #6 L 沿構材軸量（L = 350 cm；圖上只標 L，長度示意）
#                      #2 P 鉛直向下作用於右上自由端；固定端在左下
#                      #4 斷面：翼板垂直、腹板水平，P 平行翼板
#                      #5 自由端弧箭頭＝45° 角度標註，非外加彎矩

PW, PH = 500, 520
TH = math.radians(90.0 - ANG_P)          # 構材與水平夾角（由 #1 推得）
UX, UY = math.cos(TH), math.sin(TH)      # 構材方向（固定端 → 自由端）


def _arc(cv, p, r_px, a0, a1, color, w=1.6):
    """角度弧（數學角，度；r 為像素）"""
    cx, cy = cv.P(p)
    pts = []
    for k in range(25):
        a = math.radians(a0 + (a1 - a0) * k / 24)
        pts.append(f"{cx + r_px*math.cos(a):.2f},{cy - r_px*math.sin(a):.2f}")
    cv.parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" '
                    f'stroke-width="{w}" stroke-linecap="round"/>')


def elevation_panel():
    sx = 300
    cv = Canvas(PW, PH, sx=sx, ox=130, oy=125)
    cv.panel("構材立面", "左下固定端、右上自由端（長度示意）")
    a, b = (0, 0), (LEN * UX, LEN * UY)
    cv.line(a, b, C["member"], 5, cap="butt")
    # 固定端：牆面垂直於構材（#3），剖線朝構材外側
    cv.support(a, "fixed", math.degrees(TH) - 90, size=30)
    # 90° 標註（構材 ↔ 牆面）
    _arc(cv, a, 44, math.degrees(TH) - 90, math.degrees(TH), C["dim"])
    cv.text(a, f"{ANG_WALL:.0f}°", 13.5, C["muted"], "start", dx=40, dy=30)
    # P 鉛直向下（#2）
    cv.arrow(b, (b[0], b[1] - 0.42), C["load"], 3.0, 11)
    cv.math((b[0], b[1] - 0.42), "P", 17, C["load"], "start", dx=10, dy=-4, weight="700")
    # 45° 標註（構材軸線 ↔ P 作用線），#5
    _arc(cv, b, 52, 180 + math.degrees(TH), 270, C["dim"])
    cv.text(b, f"{ANG_P:.0f}°", 13.5, C["muted"], "end", dx=-14, dy=66)
    # L 沿構材（#6）
    cv.dim(a, b, "L", off=-46, label_off=-18, size=17)
    return cv


def section_panel():
    cv = Canvas(PW, PH, sx=5.2, ox=PW / 2, oy=PH / 2 + 10)
    cv.panel("斷面小圖", "翼板垂直、腹板水平（示意）")
    d, bf, tf, tw = 28.0, 28.0, 2.0, 1.4      # 示意比例，題未給板件尺寸
    m = C["member"]
    for x0, x1, y0, y1 in ((-d / 2, -d / 2 + tf, -bf / 2, bf / 2),
                           (d / 2 - tf, d / 2, -bf / 2, bf / 2),
                           (-d / 2 + tf, d / 2 - tf, -tw / 2, tw / 2)):
        cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], C["fill_c"], m, 1.6)
    # P 自腹板中點鉛直向下、平行翼板（#4）
    cv.arrow((0, 0), (0, -bf / 2 - 12), C["load"], 2.8, 10)
    cv.math((0, -bf / 2 - 12), "P", 17, C["load"], "start", dx=10, dy=-2, weight="700")
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([elevation_panel(), section_panel()], cols=2,
            title="SS-2004-4 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#6；構材長度與斷面為示意",
            note="自由端的 45° 是構材軸線與鉛直 P 的夾角（角度標註），不是外加端彎矩",
            path=path)
    return path


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


def rsum(terms, nd=3):
    """精確加總後再四捨五入（2026-11-03 勘誤後解析即採此值：簡化式 1.782）"""
    return round(sum(terms), nd)


def _stack_row(cv, x0, y, scale, terms, colors, name, total_color, h=34, fmt="{:.3f}"):
    """水平堆疊長條：互制比 1.0 對應 scale 像素"""
    cv.text_px(x0 - 14, y, name, 14, C["text"], "end", weight="700")
    xx = x0
    for t, col in zip(terms, colors):
        w = scale * t
        cv.rect_px(xx, y - h/2, w, h, col, 0)
        if w > 44:
            cv.text_px(xx + w/2, y, fmt.format(t), 12.5, "#FFFFFF", weight="700")
        xx += w
    tot = rsum(terms)
    cv.text_px(xx + 12, y, "= " + fmt.format(tot), 15, total_color, "start", weight="700")
    return tot


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2004-4.md §1／§4（三），由下式即時算出
# ══════════════════════════════════════════════════════════════
P_TF   = 2.0                 # tf，P = 2000 kg                     §1
L_CM   = 350.0               # cm，沿構材軸量                     §1
A_G    = 59.0                # cm^2                                §1
S_Y    = 152.0               # cm^3（弱軸彎曲，S_y 控制）          §1
R_Y    = 5.13                # cm                                  §1
K_EFF  = 2.1                 # 題給                                §1
C_C    = 127.0               # 題給                                §1
E_TF   = 2.1e3               # tf/cm^2                             §1
F_Y    = 2.5                 # tf/cm^2                             §1

N_AX   = P_TF * math.cos(math.radians(ANG_P))    # 沿桿軸壓力          §4.1
V_TR   = P_TF * math.sin(math.radians(ANG_P))    # 垂直桿軸橫力        §4.1
M_FIX  = V_TR * L_CM                             # 固端彎矩 = P × 水平投影 §4.2
ARM    = L_CM * math.sin(math.radians(ANG_P))    # P 對固定端之力臂
M_WRONG = P_TF * L_CM                            # 誤：把整個 P 當橫力
fa     = N_AX / A_G                              # §4.3
fby    = M_FIX / S_Y                             # §4.3
KLR    = K_EFF * L_CM / R_Y                      # §4.4
FA     = 12 * math.pi**2 * E_TF / (23 * KLR**2)  # KL/r > Cc → 彈性式   §4.4
FBY    = 0.75 * F_Y                              # §4.4
R_AX, R_BY = fa / FA, fby / FBY                  # §4.5
R_STR  = fa / (0.6 * F_Y)                        # 強度式之軸力項        §4.5


def fig1_decompose():
    """圖 1：P 分解為 N、V；固端彎矩 = P × 水平力臂 = V × L"""
    W1, H1 = 520, 540
    # ── 格 1：受力分解 ──
    cv = Canvas(W1, H1, sx=300, ox=120, oy=165)
    cv.panel("① 鉛直 P 分解到構材座標", "固定端在左下、自由端在右上（長度示意）")
    a, b = (0, 0), (LEN * UX, LEN * UY)
    cv.line(a, b, C["member"], 5, cap="butt")
    cv.support(a, "fixed", math.degrees(TH) - 90, size=30)
    # P 作用線與力臂（水平投影）
    cv.line(b, (b[0], 0), C["ghost"], 1.6, dash="6 5")
    cv.line((-0.08, 0), (b[0] + 0.06, 0), C["ghost"], 1.6, dash="6 5")
    cv.dim((0, 0), (b[0], 0), f"L sin45° = {ARM:.1f} cm", off=56, label_off=16, size=13)
    cv.text_px(cv.X(b[0] / 2), cv.Y(0) + 96, "＝ P 對固定端的力臂", 12.5, C["muted"])
    # P
    cv.arrow(b, (b[0], b[1] - 0.40), C["load"], 3.2, 11)
    cv.text_px(cv.X(b[0]) - 10, cv.Y(b[1] - 0.36), f"P = {P_TF:g} tf", 14, C["load"], "end", weight="700")
    # 分量：N 沿 −u（壓向固定端），V 沿 (UY, −UX)
    s = 0.30
    off = (-UY * 0.045, UX * 0.045)                 # N 畫在構材上方側邊，避免與構材重疊
    n0 = (b[0] + off[0], b[1] + off[1])
    cv.arrow(n0, (n0[0] - s * UX, n0[1] - s * UY), C["compr"], 3.0, 10)
    cv.text_px(cv.X(n0[0] - s * UX) - 8, cv.Y(n0[1] - s * UY) - 14,
               f"N = P cos45° = {N_AX:.3f} tf（壓）", 13, C["compr"], "end", weight="700")
    cv.arrow(b, (b[0] + s * UY, b[1] - s * UX), C["sfd"], 3.0, 10)
    vx, vy = cv.X(b[0] + s * UY) - 6, cv.Y(b[1] - s * UX)
    cv.text_px(vx, vy + 24, "V = P sin45°", 13, C["sfd"], "start", weight="700")
    cv.text_px(vx, vy + 44, f"= {V_TR:.3f} tf", 13, C["sfd"], "start", weight="700")
    # 固端彎矩
    cv.moment_arrow(a, r=40, ccw=False, color=C["bmd"], w=2.6, span=230, start=150)
    cv.text_px(cv.X(0) + 50, cv.Y(0) + 26, f"M = {M_FIX:.0f} tf·cm", 14, C["bmd"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 30, "P × 力臂 與 V × L 是同一個量：兩種算法必須相等", 12.5, C["muted"])
    p1 = cv

    # ── 格 2：沿構材的彎矩分佈 ──
    cv = Canvas(W1, H1, sx=1)
    cv.panel("② 沿構材的彎矩 M(s)（s 由自由端量起）", "M 隨 s 線性增加，固端最大")
    X0, X1 = 80, 440
    YB, YT = 400, 130                  # 像素（y 向下）
    def px(s_cm, m):
        return X0 + (X1 - X0) * s_cm / L_CM, YB - (YB - YT) * m / M_WRONG
    _hl(cv, H1, X0, YB, X1 + 10, YB, C["muted"], 1.6)
    _hl(cv, H1, X0, YB, X0, YT - 20, C["muted"], 1.6)
    xe, ye = px(L_CM, M_FIX)
    cv.polygon([(X0, H1 - YB), (xe, H1 - ye), (xe, H1 - YB)], C["fill_m"], C["bmd"], 2.4)
    xw, yw = px(L_CM, M_WRONG)
    _hl(cv, H1, X0, YB, xw, yw, C["load"], 2.2, dash="7 5")
    cv.dot((xe, H1 - ye), 5, fill=C["bmd"])
    cv.dot((xw, H1 - yw), 5, fill=C["load"])
    cv.text_px(xe - 12, ye + 125, f"V·L = {M_FIX:.0f} tf·cm", 14, C["bmd"], "end", weight="700")
    cv.text_px(xw - 8, yw - 14, f"誤：P·L = {M_WRONG:.0f}", 13, C["load"], "end", weight="700")
    cv.text_px(X0, YB + 22, "自由端 s = 0", 12, C["muted"], "start")
    cv.text_px(X1, YB + 22, f"固定端 s = L = {L_CM:.0f} cm", 12, C["muted"], "end")
    cv.text_px(W1 / 2, YB + 60, f"fby = {M_FIX:.0f} / {S_Y:.0f} = {fby:.3f} tf/cm²", 14, C["text"], weight="700")
    cv.text_px(W1 / 2, YB + 86, f"誤用 P·L 會得 {M_WRONG / S_Y:.3f}，高估 {M_WRONG / M_FIX - 1:.0%}",
               12.5, C["load"])
    p2 = cv

    path = os.path.join(OUT, f"{TAG}-fig-1-decompose.svg")
    compose([p1, p2], cols=2,
            title="圖 1　45° 懸臂：P 拆成軸壓 N 與橫力 V，固端彎矩取水平力臂",
            sub=f"N = V = {N_AX:.3f} tf；M = P × L sin45° = V × L = {M_FIX:.0f} tf·cm（弱軸，S_y 控制）",
            note="斜置構材的彎矩只由垂直桿軸的分量產生；沿桿軸的分量 N 是軸壓，不貢獻一階彎矩",
            path=path)
    return path


def fig2_ratio():
    """圖 2：各項比值的量級——NG 幾乎全來自弱軸彎曲"""
    W1, H1 = 560, 420
    COLS = [C["compr"], C["load"]]
    SC = 182.0                                   # 比值 1.0 = 182 px
    # ── 格 1：兩式堆疊 ──
    cv = Canvas(W1, H1, sx=1)
    cv.panel("① 互制比的組成", f"fa/Fa = {R_AX:.3f} &lt; 0.15 ⇒ 簡化式")
    x0 = 120
    _hl(cv, H1, x0 + SC, 96, x0 + SC, 300, C["load"], 2.0, dash="6 4")
    cv.text_px(x0 + SC, 86, "上限 1.0", 12.5, C["load"], weight="700")
    _stack_row(cv, x0, 160, SC, [R_AX, R_BY], COLS, "簡化互制式", C["load"])
    _stack_row(cv, x0, 240, SC, [R_STR, R_BY], COLS, "強度式", C["load"])
    cv.legend(x0 - 96, 320, [(COLS[0], "軸壓項（左端細條）"), (COLS[1], "弱軸彎曲項 fby/Fby")],
              size=12, gap=20)
    cv.text_px(W1 / 2, H1 - 28, "軸壓項只佔 2.6%；拿掉它照樣 N.G.", 12.5, C["muted"])
    p1 = cv

    # ── 格 2：實際應力 vs 容許應力 ──
    cv = Canvas(W1, H1, sx=1)
    cv.panel("② 實際應力與容許應力（tf/cm²）", f"KL/ry = {KLR:.1f} > Cc = {C_C:g} ⇒ Fa 用彈性式")
    x0, sc = 130, 100.0                          # 1 tf/cm² = 100 px
    rows = ((f"軸壓", fa, FA, C["compr"]), ("弱軸彎曲", fby, FBY, C["load"]))
    y = 130
    for nm, act, alw, col in rows:
        cv.text_px(x0 - 14, y + 14, nm, 14, C["text"], "end", weight="700")
        cv.rect_px(x0, y, sc * alw, 22, C["ghost"], 4)
        cv.text_px(x0 + sc * alw + 10, y + 11, f"容許 {alw:.3f}", 12.5, C["muted"], "start", weight="700")
        cv.rect_px(x0, y + 28, max(sc * act, 3), 22, col, 4)
        cv.text_px(x0 + max(sc * act, 3) + 10, y + 39, f"實際 {act:.3f}", 12.5, col, "start", weight="700")
        y += 110
    cv.text_px(W1 / 2, H1 - 52, f"Fa 雖已因細長降到 {FA:.3f}，fa 仍只有它的 {R_AX:.1%}", 12.5, C["muted"])
    cv.text_px(W1 / 2, H1 - 28, f"fby 超過 Fby {R_BY - 1:.0%}——瓶頸在弱軸斷面模數", 12.5, C["load"], weight="700")
    p2 = cv

    path = os.path.join(OUT, f"{TAG}-fig-2-ratio.svg")
    compose([p1, p2], cols=2,
            title=f"圖 2　ASD 檢核量級：簡化式 {rsum([R_AX, R_BY]):.3f}、強度式 {rsum([R_STR, R_BY]):.3f}，皆 N.G.",
            sub=f"fa/Fa = {R_AX:.3f}　fby/Fby = {R_BY:.3f}",
            note="這是彎曲控制的構材：加大 S_y（或改繞強軸彎曲）才有用，加大 r_y 幾乎無效",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把自由端 45° 角度弧當成外加彎矩；P 當成沿構材軸向或垂直構材；P 平行翼板卻判成繞強軸彎曲"),
    (fig1_decompose, "§4（三）4.1–4.2",
     "把整個 P 當橫力而得 M = P·L = 700；用沿桿全長而非水平力臂；把 N 也算進彎矩"),
    (fig2_ratio, "§4（三）4.3–4.6",
     "以為細長（KL/r > Cc）就是軸壓控制；NG 實際上 97% 來自弱軸彎曲項"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
