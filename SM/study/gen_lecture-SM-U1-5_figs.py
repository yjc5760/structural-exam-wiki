# -*- coding: utf-8 -*-
"""Data-driven SVG figures for lecture-SM-U1-5.html.
Every coordinate is computed from the numbers in raw/solutions/*.md."""
import math, re

D = math.radians
sind = lambda a: math.sin(D(a))
cosd = lambda a: math.cos(D(a))
tand = lambda a: math.tan(D(a))
asind = lambda x: math.degrees(math.asin(x))

INK, MUT, AX = "#37474f", "#607d8b", "#455a64"
RED, RED2, ORG, ORG2, GRN, GRN2, BLU, BLU2, PUR = (
    "#c62828", "#ffebee", "#e65100", "#fff3e0", "#2e7d32", "#e8f5e9", "#1565c0", "#e3f2fd", "#6a1b9a")
GRY = "#90a4ae"


def f(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


def rich(s, size):
    """'σ_{1f}′' -> tspans with real subscripts (dy shifts)."""
    out, off = [], 0.0
    parts = re.split(r"(_\{[^}]*\}|_[^\s{])", s)
    small = size * 0.74
    for p in parts:
        if not p:
            continue
        if p.startswith("_"):
            t = p[2:-1] if p.startswith("_{") else p[1:]
            dy = size * 0.30 - off
            out.append('<tspan dy="%s" font-size="%s">%s</tspan>' % (f(dy), f(small), t))
            off = size * 0.30
        else:
            dy = -off
            if off:
                out.append('<tspan dy="%s">%s</tspan>' % (f(dy), p))
            else:
                out.append(p)
            off = 0.0
    return "".join(out)


class SVG:
    def __init__(self, w, h):
        self.w, self.h, self.e, self.defs = w, h, [], {}

    def add(self, s):
        self.e.append(s)

    def line(self, x1, y1, x2, y2, c=AX, w=1.6, dash=None, arrow=None, op=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        m = ' marker-end="url(#%s)"' % self.marker(c) if arrow else ""
        o = ' opacity="%s"' % op if op else ""
        self.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s%s%s/>'
                 % (f(x1), f(y1), f(x2), f(y2), c, w, d, m, o))

    def marker(self, c):
        mid = "ar" + c.strip("#")
        self.defs[mid] = ('<marker id="%s" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto" '
                          'markerUnits="userSpaceOnUse"><path d="M0,0 L9,4.5 L0,9 z" fill="%s"/></marker>' % (mid, c))
        return mid

    def path(self, d, c=AX, w=1.6, fill="none", dash=None, arrow=None, op=None):
        ds = ' stroke-dasharray="%s"' % dash if dash else ""
        m = ' marker-end="url(#%s)"' % self.marker(c) if arrow else ""
        o = ' fill-opacity="%s"' % op if op else ""
        self.add('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s%s%s/>' % (d, fill, c, w, ds, m, o))

    def rect(self, x, y, w, h, fill="#fff", c="#dfe6ea", sw=1.4, rx=9, op=None):
        o = ' fill-opacity="%s"' % op if op else ""
        self.add('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>'
                 % (f(x), f(y), f(w), f(h), rx, fill, c, sw, o))

    def dot(self, x, y, c, r=4):
        self.add('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(x), f(y), r, c))

    def text(self, x, y, s, size=12, c=INK, bold=False, anchor=None, halo=False):
        a = ' text-anchor="%s"' % anchor if anchor else ""
        b = ' font-weight="bold"' if bold else ""
        h = ' stroke="#fff" stroke-width="3.5" paint-order="stroke" stroke-linejoin="round"' if halo else ""
        self.add('<text x="%s" y="%s" font-size="%s" fill="%s"%s%s%s>%s</text>'
                 % (f(x), f(y), size, c, b, a, h, rich(s, size)))

    def render(self):
        defs = "<defs>%s</defs>" % "".join(self.defs.values()) if self.defs else ""
        return ('<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" font-family="Microsoft JhengHei,Noto Sans TC,sans-serif">\n'
                % (self.w, self.h) + "\n".join("  " + x for x in self.e) + "\n  " + defs + "\n</svg>")


class Mohr:
    """σ–τ plot with equal scale on both axes (circles stay circles)."""

    def __init__(self, svg, ox, oy, s):
        self.g, self.ox, self.oy, self.s = svg, ox, oy, s

    def X(self, sig):
        return self.ox + self.s * sig

    def Y(self, tau):
        return self.oy - self.s * tau

    def axes(self, smax, tmax, xl="σ (kPa)", yl="τ (kPa)", smin=0):
        g = self.g
        g.line(self.X(smin), self.oy, self.X(smax), self.oy, AX, 1.8, arrow=True)
        g.line(self.X(smin), self.oy, self.X(smin), self.Y(tmax), AX, 1.8, arrow=True)
        g.text(self.X(smax) - 4, self.oy - 8, xl, 12.5, MUT, anchor="end")
        g.text(self.X(smin) + 8, self.Y(tmax) + 6, yl, 12.5, MUT)

    def circle(self, s3, s1, c, fill=None, w=2.2, dash=None, op=None):
        C, R = (s1 + s3) / 2, (s1 - s3) / 2
        d = "M%s %s A%s %s 0 0 1 %s %s" % (f(self.X(s3)), f(self.oy), f(R * self.s), f(R * self.s),
                                          f(self.X(s1)), f(self.oy))
        if fill:
            d += " Z"
        self.g.path(d, c, w, fill or "none", dash, op=op)
        return C, R

    def env(self, c0, phi, s_from, s_to, col, w=2.4, dash=None):
        t = tand(phi)
        self.g.line(self.X(s_from), self.Y(c0 + s_from * t), self.X(s_to), self.Y(c0 + s_to * t), col, w, dash)

    def tangent(self, C, R, phi):
        return C - R * sind(phi), R * cosd(phi)

    def arc(self, cx, cy, r, a0, a1, col, w=1.6):
        """angles in degrees, math convention (CCW from +σ), drawn in screen coords."""
        x0, y0 = cx + r * cosd(a0), cy - r * sind(a0)
        x1, y1 = cx + r * cosd(a1), cy - r * sind(a1)
        large = 1 if abs(a1 - a0) > 180 else 0
        sweep = 0 if a1 > a0 else 1
        self.g.path("M%s %s A%s %s 0 %d %d %s %s" % (f(x0), f(y0), f(r), f(r), large, sweep, f(x1), f(y1)), col, w)


# ---------------------------------------------------------------- 1.2 failure plane (SM-2018-2 effective)
def fig_plane():
    s3, s1 = 33.0, 118.0
    C, R = (s1 + s3) / 2, (s1 - s3) / 2
    phi = asind(R / C)                      # 34.26
    th = 45 + phi / 2                       # 62.13
    sff, tff = C - R * sind(phi), R * cosd(phi)
    g = SVG(880, 380)
    # --- specimen
    g.text(26, 26, "實體試體（SM-2018-2）", 14, BLU, True)
    x0, y0, W, H = 96, 78, 120, 200
    g.rect(x0, y0, W, H, "#eceff1", "#546e7a", 2, 6)
    for x in (x0 + 25, x0 + 60, x0 + 95):
        g.line(x, y0 - 36, x, y0 - 6, RED, 3.2, arrow=True)
    g.text(x0 + W + 8, y0 - 16, "σ_1′ = 118", 13, RED, True)
    g.line(x0 - 42, y0 + H / 2, x0 - 6, y0 + H / 2, GRN, 3, arrow=True)
    g.line(x0 + W + 42, y0 + H / 2, x0 + W + 6, y0 + H / 2, GRN, 3, arrow=True)
    g.text(x0 + W + 14, y0 + H / 2 + 22, "σ_3′ = 33", 13, GRN, True)
    # plane through centre at angle th
    cx, cy = x0 + W / 2, y0 + H / 2
    t = (H / 2) / sind(th)
    xa, ya = cx - t * cosd(th), cy + t * sind(th)
    xb, yb = cx + t * cosd(th), cy - t * sind(th)
    g.line(xa, ya, xb, yb, PUR, 2.6, "8 4")
    g.line(xa, ya, xa + 70, ya, GRY, 1.3)
    Mohr(g, 0, 0, 1).arc(xa, ya, 30, 0, th, PUR)
    g.text(xa + 34, ya - 10, "θ", 13, PUR, True)
    g.text(20, 312, "θ ＝ 破壞面與大主應力作用面（水平面）的夾角", 12.5, INK)
    g.text(20, 334, "θ = 45° + φ′/2 = 45° + %.2f°/2 = %.2f°" % (phi, th), 13, PUR, True)
    g.text(20, 356, "誤用 φ_{cu} = 17.35° → %.2f°（少了 %.1f°）" % (45 + 17.35 / 2, th - 45 - 17.35 / 2), 12.5, ORG, True)
    # --- Mohr
    m = Mohr(g, 410, 272, 3.2)
    g.text(410, 26, "有效應力莫爾圓上的對應", 14, BLU, True)
    m.axes(140, 72, "σ′ (kPa)", "τ (kPa)")
    m.circle(s3, s1, BLU, BLU2)
    m.env(0, phi, 0, 100, RED)
    g.text(m.X(100) - 4, m.Y(100 * tand(phi)) - 8, "τ = σ′ tanφ′，φ′ = %.2f°" % phi, 12.5, RED, True, "end")
    m.arc(m.X(0), m.Y(0), 42, 0, phi, RED)
    g.text(m.X(0) + 46, m.Y(0) - 8, "φ′", 12.5, RED, True)
    Fx, Fy, Cx = m.X(sff), m.Y(tff), m.X(C)
    g.line(Cx, m.oy, Fx, Fy, PUR, 2)
    # right-angle mark at F
    u = (cosd(phi), sind(phi))           # along envelope (screen: +x, -y)
    v = (Cx - Fx, m.oy - Fy)
    L = math.hypot(*v); v = (v[0] / L, v[1] / L)
    k = 9
    p1 = (Fx + k * u[0], Fy - k * u[1]); p2 = (p1[0] + k * v[0], p1[1] + k * v[1]); p3 = (Fx + k * v[0], Fy + k * v[1])
    g.path("M%s %s L%s %s L%s %s" % (f(p1[0]), f(p1[1]), f(p2[0]), f(p2[1]), f(p3[0]), f(p3[1])), PUR, 1.4)
    g.dot(Fx, Fy, PUR, 5)
    g.text(Fx - 12, Fy - 12, "F", 13, PUR, True, "end")
    g.line(Fx, Fy, Fx, m.oy, GRY, 1.1, "3 3")
    g.line(m.X(0), Fy, Fx, Fy, GRY, 1.1, "3 3")
    g.text(m.X(0) - 6, Fy + 4, f(tff), 11.5, PUR, anchor="end")
    g.text(Fx, m.oy + 16, f(sff), 11.5, PUR, anchor="middle")
    m.arc(Cx, m.oy, 34, 0, 90 + phi, ORG, 1.8)
    g.text(Cx + 30, m.oy - 34, "2θ = 90°+φ′", 12.5, ORG, True)
    g.text(Cx + 30, m.oy - 18, "= %.2f°" % (90 + phi), 12, ORG)
    for sv, col, lab in ((s3, GRN, "33"), (C, BLU, "C=75.5"), (s1, RED, "118")):
        g.dot(m.X(sv), m.oy, col, 4)
        g.text(m.X(sv), m.oy + 32, lab, 11.5, col, True, "middle")
    g.text(410, 344, "① 相切 ⟹ 半徑 CF ⊥ 包絡線 ⟹ 圓心角 ∠σ_1CF = 90° + φ′", 12.5, INK)
    g.text(410, 366, "② 圓上角度是實體夾角的兩倍 ⟹ 2θ = 90° + φ′ ⟹ θ = 45° + φ′/2", 12.5, INK)
    return g.render(), dict(phi=phi, th=th, sff=sff, tff=tff)


# ---------------------------------------------------------------- 2.1 SUU / UUU
def fig_uu():
    g = SVG(880, 262)
    g.text(26, 24, "SUU：飽和不壓密不排水", 14, RED, True)
    g.text(476, 24, "UUU：不飽和不壓密不排水", 14, ORG, True)
    g.add('<g transform="translate(0,-78)">')
    ox, oy, r = 56, 250, 38
    phi_e = 30.0
    ce = ox + r / sind(phi_e)            # effective circle tangent to φ′ line
    g.line(ox, oy, 440, oy, AX, 1.6, arrow=True)
    g.line(ox, oy, ox, 120, AX, 1.6, arrow=True)
    g.text(436, oy - 8, "σ", 12.5, MUT, anchor="end")
    g.text(ox + 8, 130, "τ", 12.5, MUT)
    g.path("M%s %s A%s %s 0 0 1 %s %s Z" % (f(ce - r), oy, r, r, f(ce + r), oy), GRN, 2.2, GRN2)
    for cx in (ce + 90, ce + 90 + 2 * r + 6, ce + 90 + 4 * r + 12):
        g.path("M%s %s A%s %s 0 0 1 %s %s" % (f(cx - r), oy, r, r, f(cx + r), oy), RED, 1.9, RED2)
    # φu = 0 line
    g.line(ox, oy - r, 434, oy - r, INK, 2.4)
    g.text(430, oy - r - 8, "φ_u = 0", 13, INK, True, "end")
    g.line(ox - 6, oy - r, ox + 6, oy - r, INK, 2)
    g.text(ox - 10, oy - r + 4, "S_u", 12, INK, True, "end")
    # φ′ envelope
    xe = ox + 175
    g.line(ox, oy, xe, oy - (xe - ox) * tand(phi_e), GRN, 1.8, "6 4")
    g.text(xe + 4, oy - (xe - ox) * tand(phi_e) + 4, "φ′ 線", 12, GRN, True)
    # arrows: total → effective (−u)
    g.line(ce + 90, oy + 14, ce + 6, oy + 14, PUR, 1.8, arrow=True)
    g.text(ce + 48, oy + 30, "−u", 12, PUR, True, "middle")
    g.text(ce, oy - 12, "有效圓", 11.5, GRN, True, "middle")
    g.text(26, 300, "三個總應力圓半徑相同（Δσ_3 全被水吃掉）", 12.5, INK)
    g.text(26, 322, "扣掉各自的 u 後全部疊在同一個有效圓上 → 強度不變", 12, MUT)

    # UUU (schematic, geometry verified tangent)
    bx, by = 500, 250
    g.line(bx, by, 864, by, AX, 1.6, arrow=True)
    g.line(bx, by, bx, 120, AX, 1.6, arrow=True)
    g.text(860, by - 8, "σ", 12.5, MUT, anchor="end")
    g.text(bx + 8, 130, "τ", 12.5, MUT)
    circles = [(562, 28), (650, 45), (762, 56), (820, 56)]
    for i, (cx, rr) in enumerate(circles[:3]):
        g.path("M%s %s A%s %s 0 0 1 %s %s Z" % (cx - rr, by, rr, rr, cx + rr, by), ORG, 1.8, ORG2)
    g.path("M%s %s L641.3 210.8 Q701.5 199 762 199 L 860 199" % (508, 237.1), INK, 2.4)
    g.text(530, 218, "φ_u > 0", 12.5, ORG, True)
    g.text(858, 191, "轉為 φ_u = 0", 12.5, INK, True, "end")
    g.line(700, 199, 700, by, GRY, 1, "3 3")
    g.text(700, by + 16, "≈ 飽和點", 11, MUT, anchor="middle")
    g.text(476, 300, "低圍壓：B < 1，部分 Δσ_3 變成有效應力 → 圓變大", 12.5, INK)
    g.text(476, 322, "空氣被壓縮溶解、B → 1 後 → 包絡線轉水平", 12, MUT)
    g.add('</g>')
    return g.render()


# ---------------------------------------------------------------- 2.2 CU two circles (SM-2018-2)
def fig_cu():
    s3, s1, uf = 100.0, 185.0, 67.0
    g = SVG(880, 350)
    m = Mohr(g, 70, 286, 1.6)
    m.axes(352, 150, "σ, σ′ (kPa)", "τ (kPa)")
    Ce, R = m.circle(s3 - uf, s1 - uf, GRN, GRN2)
    Ct, _ = m.circle(s3, s1, RED, None, 2.2, "7 4")
    phc = asind(R / Ct); phe = asind(R / Ce)
    m.env(0, phc, 0, 340, RED, 2.2, "7 4")
    m.env(0, phe, 0, 200, GRN, 2.4)
    g.text(m.X(340), m.Y(340 * tand(phc)) - 10, "總應力包絡線 φ_{cu} = %.2f°" % phc, 12.5, RED, True, "end")
    g.text(m.X(200) + 6, m.Y(200 * tand(phe)) + 12, "有效應力包絡線 φ′ = %.2f°" % phe, 12.5, GRN, True)
    for C, phi, col in ((Ct, phc, RED), (Ce, phe, GRN)):
        sx, ty = m.tangent(C, R, phi)
        g.line(m.X(C), m.oy, m.X(sx), m.Y(ty), col, 1.3, "3 3")
        g.dot(m.X(sx), m.Y(ty), col, 4.5)
    sx, ty = m.tangent(Ce, R, phe)
    g.text(m.X(sx) - 8, m.Y(ty) - 6, "(%s, %s)" % (f(sx), f(ty)), 11.5, GRN, True, "end", True)
    sx2, ty2 = m.tangent(Ct, R, phc)
    g.text(m.X(sx2) + 4, m.Y(ty2) - 10, "(%s, %s)" % (f(sx2), f(ty2)), 11.5, RED, True, None, True)
    # centres & shift arrow exactly uf long
    g.dot(m.X(Ct), m.oy, RED, 3.5); g.dot(m.X(Ce), m.oy, GRN, 3.5)
    yA = m.oy + 40
    g.line(m.X(Ct), m.oy + 4, m.X(Ct), yA + 4, GRY, 1)
    g.line(m.X(Ce), m.oy + 4, m.X(Ce), yA + 4, GRY, 1)
    g.line(m.X(Ct), yA, m.X(Ce) + 2, yA, PUR, 2.4, arrow=True)
    g.text((m.X(Ct) + m.X(Ce)) / 2, yA + 18, "整個圓左移 u_f = 67 kPa（R = 42.5 不變）", 12.5, PUR, True, "middle")
    for v, col, lab, dy in ((s3, RED, "σ_3=100", 18), (s1, RED, "σ_1=185", 18), (s3 - uf, GRN, "σ_3′=33", 18), (s1 - uf, GRN, "σ_1′=118", 18)):
        g.dot(m.X(v), m.oy, col, 3.5)
    g.text(m.X(s3 - uf), m.oy + 18, "33", 11.5, GRN, True, "middle")
    g.text(m.X(s1 - uf), m.oy + 18, "118", 11.5, GRN, True, "middle")
    g.text(m.X(s3), m.oy + 18, "100", 11.5, RED, True, "middle")
    g.text(m.X(s1), m.oy + 18, "185", 11.5, RED, True, "middle")
    g.rect(644, 30, 230, 150)
    g.text(656, 54, "NC 黏土 → 兩條線都過原點", 13, BLU, True)
    g.text(656, 78, "sinφ_{cu} = (185−100)/(185+100)", 12)
    g.text(656, 98, "　　　= 85/285 → %.2f°" % phc, 12)
    g.text(656, 122, "sinφ′ = (118−33)/(118+33)", 12)
    g.text(656, 142, "　　　= 85/151 → %.2f°" % phe, 12)
    g.text(656, 168, "分子相同、分母變小 → φ′ > φ_{cu}", 11.5, RED)
    return g.render(), dict(phc=phc, phe=phe)


# ---------------------------------------------------------------- 3.2 SM-2008-2 circles
def fig_2008():
    sv0, sh0 = 66.90, 33.45
    dq = sh0 / 0.8
    du = 1.7 / 3 * dq
    s1f, s3f = sv0 + 2 / 3 * dq - du, sh0 + 1 / 3 * dq - du
    w1, w3 = sv0 + 2 / 3 * dq, sh0 + 1 / 3 * dq        # forgot Δu
    g = SVG(880, 380)
    m = Mohr(g, 60, 300, 5.2)
    m.axes(106, 52, "σ′ (kPa)", "τ (kPa)")
    m.env(0, 30, 0, 82, RED, 2.4)
    g.text(m.X(82) + 4, m.Y(82 * tand(30)) + 4, "φ′ = 30°", 12.5, RED, True)
    m.env(0, asind(1 / 3), 0, 104, BLU, 1.6, "6 4")
    g.text(m.X(104), m.Y(104 * tand(asind(1 / 3))) - 8, "σ_1′/σ_3′ = 2 的切線（19.47°）", 12, BLU, True, "end")
    m.circle(sh0, sv0, GRY, "#eceff1", 1.8)
    m.circle(w3, w1, BLU, None, 2.0, "7 4")
    Cf, Rf = m.circle(s3f, s1f, RED, RED2, 2.4, op="0.55")
    sx, ty = m.tangent(Cf, Rf, 30)
    g.dot(m.X(sx), m.Y(ty), RED, 5)
    g.text(m.X(sx) - 8, m.Y(ty) - 8, "碰到包絡線", 12, RED, True, "end", True)
    # labels on axis
    for v, col, lab in ((s3f, RED, f(s3f)), (sh0, MUT, "33.45"), (w3, BLU, f(w3)),
                        (sv0, MUT, "66.90"), (s1f, RED, f(s1f)), (w1, BLU, f(w1))):
        g.dot(m.X(v), m.oy, col, 3.5)
    lab_y = m.oy + 18
    g.text(m.X(s3f), lab_y, f(s3f), 11, RED, True, "end")
    g.text(m.X(sh0) + 2, lab_y, "33.45", 11, MUT, True, "start")
    g.text(m.X(w3), lab_y + 14, f(w3), 11, BLU, True, "middle")
    g.text(m.X(sv0) - 2, lab_y, "66.90", 11, MUT, True, "end")
    g.text(m.X(s1f) + 2, lab_y, f(s1f), 11, RED, True, "start")
    g.text(m.X(w1), lab_y, f(w1), 11, BLU, True, "middle")
    # movement arrows
    ya = m.oy + 46
    g.line(m.X(sh0), ya, m.X(s3f) + 2, ya, RED, 2.2, arrow=True)
    g.text(m.X((sh0 + s3f) / 2), ya + 16, "σ_3′ −%.2f" % (sh0 - s3f), 11.5, RED, True, "middle")
    g.line(m.X(sv0), ya, m.X(s1f) - 2, ya, RED, 2.2, arrow=True)
    g.text(m.X((sv0 + s1f) / 2) + 14, ya + 16, "σ_1′ +%.2f" % (s1f - sv0), 11.5, RED, True, "middle")
    # legend / box
    bx = 640
    g.rect(bx, 40, 232, 252)
    g.text(bx + 14, 64, "Δq = %.2f kPa（H = %.2f m）" % (dq, dq / 9.81), 12.5, BLU, True)
    g.line(bx + 14, 86, bx + 40, 86, GRY, 3); g.text(bx + 48, 90, "加載前 (33.45, 66.90)", 12, INK)
    g.line(bx + 14, 110, bx + 40, 110, RED, 3); g.text(bx + 48, 114, "正確：扣 Δu = %.2f" % du, 12, RED, True)
    g.text(bx + 48, 132, "(%.2f, %.2f) 剛好相切" % (s3f, s1f), 11.5, RED)
    g.line(bx + 14, 156, bx + 40, 156, BLU, 2.4, "7 4"); g.text(bx + 48, 160, "忘了扣 Δu", 12, BLU, True)
    g.text(bx + 48, 178, "(%.2f, %.2f)" % (w3, w1), 11.5, BLU)
    g.text(bx + 14, 206, "初始比值 66.90/33.45 = 2", 12, INK)
    g.text(bx + 14, 226, "增量比值 Δσ_v/Δσ_h = 2", 12, INK)
    g.text(bx + 14, 250, "→ 不扣 Δu，σ_1′/σ_3′ 永遠 = 2", 12, BLU, True)
    g.text(bx + 14, 272, "＜ K_p = 3，永遠不會破壞", 12, BLU, True)
    return g.render(), dict(dq=dq, du=du, s1f=s1f, s3f=s3f, w1=w1, w3=w3)


# ---------------------------------------------------------------- 4.1 NC similarity (SM-2018-2 total)
def fig_similar():
    a = (100.0, 185.0); b = (250.0, 250 * 1.85)
    g = SVG(880, 262)
    m = Mohr(g, 50, 222, 1.04)
    m.axes(520, 170, "σ (kPa)", "τ (kPa)")
    phi = asind(85 / 285)
    m.env(0, phi, 0, 505, RED, 2.4)
    g.text(m.X(505) + 4, m.Y(505 * tand(phi)) + 4, "φ_{cu} = %.2f°" % phi, 12.5, RED, True)
    for (s3, s1), col, fill, nm in ((a, BLU, BLU2, "試體一"), (b, ORG, ORG2, "試體二")):
        C, R = m.circle(s3, s1, col, fill, 2.2)
        sx, ty = m.tangent(C, R, phi)
        g.line(m.X(C), m.oy, m.X(sx), m.Y(ty), col, 1.6, "4 3")
        g.dot(m.X(sx), m.Y(ty), col, 4.5)
        g.dot(m.X(C), m.oy, col, 3.5)
        g.text(m.X(s3), m.oy + 18, f(s3), 11.5, col, True, "middle")
        g.text(m.X(s1), m.oy + 18, f(s1), 11.5, col, True, "middle")
        g.text(m.X(C) + 8, m.oy - 12, "%s R = %g" % (nm, R), 12, col, True, None, True)
    g.rect(612, 100, 260, 134)
    g.text(626, 124, "同一條過原點直線切兩圓 → 相似", 12.5, BLU, True)
    g.text(626, 148, "R/C = 42.5/142.5 = 106.25/356.25", 12)
    g.text(626, 168, "　　= %.4f = sinφ_{cu}" % (85 / 285), 12)
    g.text(626, 192, "Δσ_d/σ_3 = 85/100 = 212.5/250", 12)
    g.text(626, 214, "放大倍率 250/100 = 2.5", 12, ORG, True)
    return g.render()


# ---------------------------------------------------------------- 4.2 SM-2010-1
def fig_su():
    sv0, phi = 111.9, 28.0
    Kp = tand(45 + phi / 2) ** 2
    s3e = sv0 / Kp
    C, R = (sv0 + s3e) / 2, (sv0 - s3e) / 2
    uf = 50 - s3e
    g = SVG(880, 360)
    m = Mohr(g, 60, 292, 2.6)
    m.axes(186, 92, "σ, σ′ (kPa)", "τ (kPa)")
    m.env(0, phi, 0, 150, RED, 2.4)
    g.text(m.X(150) - 4, m.Y(150 * tand(phi)) - 8, "c′ = 0，φ′ = 28°", 12.5, RED, True, "end")
    m.arc(m.X(0), m.oy, 44, 0, phi, RED)
    g.text(m.X(0) + 48, m.oy - 8, "φ′", 12.5, RED, True)
    m.circle(s3e, sv0, GRN, GRN2, 2.4)
    m.circle(50, 50 + 2 * R, ORG, None, 2.0, "7 4")
    g.line(m.X(0), m.Y(R), m.X(180), m.Y(R), ORG, 1.6, "4 4")
    g.text(m.X(180), m.Y(R) - 6, "總應力：φ_u = 0，S_u = %.2f" % R, 12, ORG, True, "end")
    sx, ty = m.tangent(C, R, phi)
    g.dot(m.X(sx), m.Y(ty), GRN, 4.5)
    g.line(m.X(C), m.oy, m.X(sv0), m.oy, GRN, 2.8)
    g.text(m.X(C) + 22, m.oy - 10, "R = S_u", 12.5, GRN, True)
    g.dot(m.X(C), m.oy, GRN, 3.5)
    for v, col, lab, dy, anc in ((s3e, GRN, "σ_{3f}′ = %.2f" % s3e, 20, "end"), (50, ORG, "σ_3 = 50", 20, "start"),
                                 (sv0, GRN, "σ_{1f}′ = σ_{v0}′ = 111.9", 38, "middle"),
                                 (50 + 2 * R, ORG, "σ_1 = %.2f" % (50 + 2 * R), 20, "start")):
        g.dot(m.X(v), m.oy, col, 4)
        g.line(m.X(v), m.oy + 4, m.X(v), m.oy + dy - 12, col, 1)
        g.text(m.X(v) + (4 if anc == "start" else (-4 if anc == "end" else 0)), m.oy + dy, lab, 12, col, True, anc)
    g.line(m.X(50), m.oy - 30, m.X(s3e) + 2, m.oy - 30, PUR, 2.2, arrow=True)
    g.text(m.X(50) + 6, m.oy - 26, "u_f = %.2f" % uf, 12, PUR, True, None, True)
    g.rect(586, 120, 286, 170)
    g.text(600, 144, "兩行推導", 13, BLU, True)
    g.text(600, 168, "sinφ′ = R/C，且 σ_1′ = C + R = σ_{v0}′", 12.5)
    g.text(600, 190, "⟹ sinφ′ = S_u / (σ_{v0}′ − S_u)", 12.5)
    g.text(600, 216, "S_u = σ_{v0}′·sinφ′/(1+sinφ′)", 13.5, GRN, True)
    g.text(600, 238, "= 111.9 × 0.4695/1.4695 = %.2f" % R, 12)
    g.text(600, 262, "S_u/σ_{v0}′ = %.3f（φ′=30° 時 = 1/3）" % (R / sv0), 12, MUT)
    g.text(600, 280, "總應力圓＝有效圓右移 u_f，半徑不變", 11.5, ORG)
    return g.render(), dict(Su=R, s3e=s3e, uf=uf)


# ---------------------------------------------------------------- 5 stress paths (SM-2013-3, ε≈0.9%)
def fig_paths():
    p0, q0 = 340.0, 60.0
    qf = 275 / 2
    uAC, uLE = 125.0, -30.0
    pAC, pLE = p0 + (qf - q0), p0 - (qf - q0)
    pe = pAC - uAC
    rows = [(0.25, 189, 52, -17), (0.50, 238, 100, -18), (0.75, 268, 120, -28)]
    g = SVG(880, 470)
    px0, sx, oy, sy = 200.0, 2.2, 404, 2.2
    X = lambda p: 100 + (p - px0) * sx
    Y = lambda q: oy - q * sy
    g.line(100, oy, 680, oy, AX, 1.8, arrow=True)
    g.line(100, oy, 100, 40, AX, 1.8, arrow=True)
    g.path("M94 %s l6 -5 M100 %s l6 -5" % (oy + 3, oy + 3), AX, 1.4)
    g.text(676, oy - 8, "p, p′ (kPa)", 12.5, MUT, anchor="end")
    g.text(108, 50, "q (kPa)", 12.5, MUT)
    for p in (220, 260, 300, 340, 380, 420):
        g.line(X(p), oy - 4, X(p), oy + 4, AX, 1.2)
        g.text(X(p), oy + 18, str(p), 11, MUT, anchor="middle")
    for q in (60, 100, 137.5):
        g.line(96, Y(q), 104, Y(q), AX, 1.2)
        g.text(92, Y(q) + 4, f(q), 11, MUT, anchor="end")
    for sphi, col, dash, lab in ((qf / pe, GRN, None, "K_f′"), (qf / pAC, RED, "7 4", "AC 總"), (qf / pLE, ORG, "7 4", "LE 總")):
        pend = min(150 / sphi, 470)
        g.line(X(220), Y(220 * sphi), X(pend), Y(pend * sphi), col, 2.2 if dash is None else 1.6, dash)
        g.text(X(222), Y(220 * sphi) - 7, lab, 11.5, col, True, None, True)
    g.line(X(p0), Y(q0), X(pAC), Y(qf), RED, 3)
    g.line(X(p0), Y(q0), X(pLE), Y(qf), ORG, 3)
    g.text(X(362) + 12, Y(82) + 4, "AC 的 TSP（+1）", 12.5, RED, True)
    g.text(X(318) - 12, Y(82) + 4, "LE 的 TSP（−1）", 12.5, ORG, True, "end")
    pts = [(p0, q0)] + [(p0 + (d - 120) / 2 - u, d / 2) for (_, d, u, _) in rows] + [(pe, qf)]
    P = [pts[0]] + pts + [pts[-1]]
    d = "M%s %s" % (f(X(pts[0][0])), f(Y(pts[0][1])))
    for i in range(1, len(P) - 2):
        a0, a1, a2, a3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (a1[0] + (a2[0] - a0[0]) / 6, a1[1] + (a2[1] - a0[1]) / 6)
        c2 = (a2[0] - (a3[0] - a1[0]) / 6, a2[1] - (a3[1] - a1[1]) / 6)
        d += " C%s %s, %s %s, %s %s" % (f(X(c1[0])), f(Y(c1[1])), f(X(c2[0])), f(Y(c2[1])), f(X(a2[0])), f(Y(a2[1])))
    g.path(d, PUR, 3.4)
    for (e, dd, ua, ul), (pp, qq) in zip(rows, pts[1:-1]):
        g.dot(X(pp), Y(qq), PUR, 3.4)
        g.text(X(pp) - 6, Y(qq) + 4, "%g%%" % e, 10.5, PUR, True, "end", True)
    g.line(X(330) + 4, Y(103), X(322) + 2, Y(100), PUR, 1)
    g.text(X(330) + 6, Y(103) + 4, "ESP（兩者共用）", 12.5, PUR, True)
    # u brackets above failure line
    y1, y2 = Y(qf) - 24, Y(qf) - 50
    for x in (pLE, pe, pAC):
        g.line(X(x), Y(qf) - 7, X(x), y2 - 4, GRY, 0.9, "2 3")
    g.line(X(pe), y1, X(pAC) - 2, y1, RED, 1.8, arrow=True)
    g.text((X(pe) + X(pAC)) / 2, y1 - 6, "u_{AC,f} = +125", 12, RED, True, "middle", True)
    g.line(X(pe), y2, X(pLE) + 2, y2, ORG, 1.8, arrow=True)
    g.text(X(pLE) - 6, y2 + 4, "u_{LE,f} = −30", 12, ORG, True, "end", True)
    g.line(X(pLE), Y(qf), X(pAC), Y(qf), GRY, 1, "3 3")
    g.dot(X(p0), Y(q0), BLU, 6)
    g.text(X(p0), Y(q0) + 22, "起點 (340, 60)", 12, BLU, True, "middle")
    g.dot(X(pAC), Y(qf), RED, 6)
    g.text(X(pAC) + 10, Y(qf) + 4, "(%s, %s)" % (f(pAC), f(qf)), 11.5, RED, True)
    g.dot(X(pLE), Y(qf), ORG, 6)
    g.text(X(pLE) - 10, Y(qf) + 4, "(%s, %s)" % (f(pLE), f(qf)), 11.5, ORG, True, "end")
    g.dot(X(pe), Y(qf), PUR, 6.5)
    g.text(X(pe) + 10, Y(qf) + 18, "(%s, %s)" % (f(pe), f(qf)), 11.5, PUR, True, None, True)
    phAC, phLE, phE = asind(qf / pAC), asind(qf / pLE), asind(qf / pe)
    g.rect(686, 150, 188, 210)
    g.text(698, 174, "三個破壞點（ε≈0.9%）", 12.5, BLU, True)
    g.text(698, 198, "AC 總 (%s, %s)" % (f(pAC), f(qf)), 11.5, RED)
    g.text(708, 216, "→ φ_{cu} = %.2f°" % phAC, 11.5, RED)
    g.text(698, 238, "LE 總 (%s, %s)" % (f(pLE), f(qf)), 11.5, ORG)
    g.text(708, 256, "→ φ_{cu} = %.2f°" % phLE, 11.5, ORG)
    g.text(698, 278, "有效 (%s, %s)" % (f(pe), f(qf)), 11.5, PUR)
    g.text(708, 296, "→ φ′ = %.2f°" % phE, 11.5, PUR)
    g.text(698, 320, "q 相同（S_u = 137.5）", 11.5, INK)
    g.text(698, 340, "sinφ = q/p，只差在 p", 11.5, INK, True)
    g.text(100, 452, "註：p 軸自 200 起畫（軸上折線）；K_f 線均過真原點，斜率 = sinφ。紫點旁為軸向應變 ε，取自解析逐點表。", 11.5, MUT)
    return g.render(), dict(phAC=phAC, phLE=phLE, phE=phE, pAC=pAC, pLE=pLE, pe=pe)


# ---------------------------------------------------------------- 6 false c′ (SM-2002-4)
def fig_falsec():
    sv0 = (19.8 - 9.81) * 20
    c, ph = 15.0, 25.0
    tnc = c / sv0 + tand(ph)
    phnc = math.degrees(math.atan(tnc))
    g = SVG(880, 370)
    m = Mohr(g, 80, 316, 1.1)
    m.axes(450, 250, "σ′ (kN/m²)", "τ (kN/m²)")
    g.rect(m.X(49), m.Y(236), (147 - 49) * m.s, 236 * m.s, "#ffcdd2", "none", 0, 0, "0.45")
    g.rect(m.X(sv0), m.Y(236), (400 - sv0) * m.s, 236 * m.s, "#c8e6c9", "none", 0, 0, "0.45")
    g.text(m.X(98), m.Y(236) + 16, "實驗室壓密 49～147", 11.5, RED, True, "middle")
    g.text(m.X(300), m.Y(236) + 16, "基礎加載後的設計範圍", 11.5, GRN, True, "middle")
    m.env(c, ph, 0, 420, ORG, 2.4)
    m.env(0, phnc, 0, 420, GRN, 2.4, "8 4")
    s = 280
    g.text(m.X(s), m.Y(s * tnc) - 12, "現地 NC（推估）：c′ = 0，φ′ ≈ %.1f°" % phnc, 12.5, GRN, True, "end", True)
    g.text(m.X(s) + 10, m.Y(c + s * tand(ph)) + 22, "量測：c′ = 15，φ′ = 25°", 12.5, ORG, True, None, True)
    tx = sv0 * tnc
    g.dot(m.X(sv0), m.Y(tx), PUR, 5)
    g.line(m.X(sv0), m.Y(tx), m.X(sv0), m.oy, PUR, 1.3, "3 3")
    g.text(m.X(sv0), m.oy + 18, "σ_{v0}′ = %.1f" % sv0, 12, PUR, True, "middle")
    g.text(m.X(sv0) + 10, m.Y(tx) + 20, "兩線交於 σ_p′ ≈ σ_{v0}′", 12, PUR, True, None, True)
    g.line(m.X(0) + 5, m.oy, m.X(0) + 5, m.Y(c), ORG, 3)
    g.text(m.X(0) - 6, m.Y(c / 2) + 4, "假 c′=15", 11.5, ORG, True, "end")
    s = 100
    g.line(m.X(s), m.Y(s * tnc), m.X(s), m.Y(c + s * tand(ph)), RED, 2.6)
    g.text(m.X(s) - 6, m.Y(c + s * tand(ph)) - 4, "高估 %.1f" % (c + s * tand(ph) - s * tnc), 11.5, RED, True, "end", True)
    s = 400
    g.line(m.X(s), m.Y(s * tnc), m.X(s), m.Y(c + s * tand(ph)), RED, 2.6)
    g.text(m.X(s) + 8, m.Y((s * tnc + c + s * tand(ph)) / 2) + 4, "低估 %.1f" % (s * tnc - c - s * tand(ph)), 11.5, RED, True)
    g.rect(600, 220, 274, 104)
    g.text(614, 242, "推估線怎麼來的（示意）", 12.5, BLU, True)
    g.text(614, 264, "OC 段包絡線在 σ_p′ 併入 NC 線；", 12)
    g.text(614, 284, "取 σ_p′ = σ_{v0}′ = 199.8 反推：", 12)
    g.text(614, 306, "tanφ′ = 15/199.8 + tan25° → %.1f°" % phnc, 12)
    return g.render(), dict(sv0=sv0, phnc=phnc)


if __name__ == "__main__":
    import json, sys
    out = {}
    for name, fn in [("plane", fig_plane), ("uu", fig_uu), ("cu", fig_cu), ("f2008", fig_2008),
                     ("similar", fig_similar), ("su", fig_su), ("paths", fig_paths), ("falsec", fig_falsec)]:
        r = fn()
        if isinstance(r, tuple):
            out[name] = r[0]; print(name, {k: round(v, 3) for k, v in r[1].items()})
        else:
            out[name] = r
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "figs.json", "w"), ensure_ascii=False)
