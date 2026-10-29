# -*- coding: utf-8 -*-
"""lecture-SS-U1-3 內嵌 SVG 小型繪圖庫。
- 像素座標（y 向下），與講義既有 SVG 相同。
- 文字標記：$...$ 內為數學（襯線斜體），_{..} 下標、^{..} 上標；其餘為一般中文。
- 顏色沿用講義 CSS 色票。
"""
import re, math
from html import escape

COL = dict(ac="#1565c0", ac_d="#0d47a1", ac2="#e3f2fd", ten="#2e7d32", ten_d="#1b5e20", ten2="#e8f5e9",
           comp="#c62828", comp_d="#b71c1c", comp2="#ffebee", warn="#ef6c00", warn_d="#e65100", warn2="#fff3e0",
           key="#6a1b9a", key2="#f3e5f5", ink="#263238", mut="#607d8b", grid="#eceff1", gray="#90a4ae",
           lgray="#b0bec5", dk="#455a64", sub="#546e7a", yel="#fff9c4")

MATH_FONT = "'Cambria Math','Cambria','Times New Roman',serif"


def _rich(s, size):
    """把標記字串轉成 tspan 序列。"""
    out = []
    parts = re.split(r"(\$[^$]*\$)", s)
    sub = round(size * 0.72, 1)
    for p in parts:
        if not p:
            continue
        if p.startswith("$"):
            body = p[1:-1]
            # 切出上下標
            toks = re.split(r"(_\{[^}]*\}|\^\{[^}]*\}|_[A-Za-z0-9]|\^[A-Za-z0-9])", body)
            for t in toks:
                if not t:
                    continue
                if t[0] in "_^":
                    inner = t[2:-1] if t[1] == "{" else t[1:]
                    dy = 0.32 * size if t[0] == "_" else -0.42 * size
                    out.append(f'<tspan font-family="{MATH_FONT}" font-style="italic" font-size="{sub}" dy="{dy:.1f}">{escape(inner)}</tspan>'
                               f'<tspan font-size="{size}" dy="{-dy:.1f}">​</tspan>')
                else:
                    out.append(f'<tspan font-family="{MATH_FONT}" font-style="italic">{escape(t)}</tspan>')
        else:
            out.append(f'<tspan>{escape(p)}</tspan>')
    return "".join(out)


class SVG:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.el = []
        self.defs = []

    # ── primitives ─────────────────────────────
    def line(self, x1, y1, x2, y2, c=COL["dk"], w=2, dash=None, cap="round", op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{op}"' if op else ""
        self.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="{cap}"{d}{o}/>')

    def poly(self, pts, c=COL["dk"], w=2, dash=None, fill="none", op=None, join="round", close=False):
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        tag = "polygon" if close else "polyline"
        da = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{op}"' if op else ""
        self.el.append(f'<{tag} points="{d}" fill="{fill}" stroke="{c}" stroke-width="{w}" stroke-linejoin="{join}" stroke-linecap="round"{da}{o}/>')

    def area(self, pts, fill, op=0.25):
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.el.append(f'<polygon points="{d}" fill="{fill}" opacity="{op}" stroke="none"/>')

    def rect(self, x, y, w, h, fill="#fff", stroke=COL["dk"], sw=1.6, rx=8, dash=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{op}"' if op else ""
        self.el.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')

    def circle(self, x, y, r, fill="#fff", stroke=COL["dk"], sw=2):
        self.el.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size=13, c=COL["ink"], anchor="middle", weight="400", rot=None):
        tr = f' transform="rotate({rot},{x:.1f},{y:.1f})"' if rot is not None else ""
        self.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{c}" text-anchor="{anchor}" font-weight="{weight}"{tr}>{_rich(s, size)}</text>')

    def arrow(self, x1, y1, x2, y2, c=COL["dk"], w=2.5, head=10, dash=None):
        ang = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
        self.line(x1, y1, bx, by, c, w, dash, cap="butt")
        hw = head * 0.5
        p1 = (bx + hw * math.sin(ang), by - hw * math.cos(ang))
        p2 = (bx - hw * math.sin(ang), by + hw * math.cos(ang))
        self.poly([(x2, y2), p1, p2], c, 1, fill=c, close=True)

    def darrow(self, x1, y1, x2, y2, c=COL["key"], w=1.6, head=7):
        self.arrow((x1 + x2) / 2, (y1 + y2) / 2, x2, y2, c, w, head)
        self.arrow((x1 + x2) / 2, (y1 + y2) / 2, x1, y1, c, w, head)

    def moment(self, x, y, r=18, ccw=True, c=COL["warn"], w=2.4, start=200, span=250):
        """力偶符號；角度為螢幕角（0° 向右，逆時針為正，y 向下故取負）。"""
        n = 30
        pts = []
        for i in range(n + 1):
            a = math.radians(start + (span if ccw else -span) * i / n)
            pts.append((x + r * math.cos(a), y - r * math.sin(a)))
        self.poly(pts[:-3], c, w)
        self.arrow(pts[-4][0], pts[-4][1], pts[-1][0], pts[-1][1], c, w, 8)

    def ground(self, x1, x2, y, n=None, c=COL["dk"]):
        self.line(x1, y, x2, y, c, 2)
        n = n or max(3, int((x2 - x1) / 14))
        for i in range(n + 1):
            xx = x1 + 4 + (x2 - x1 - 8) * i / n
            self.line(xx, y, xx - 7, y + 10, c, 1.3)

    def pin(self, x, y, c=COL["dk"], s=11):
        self.poly([(x, y), (x - s, y + s * 1.4), (x + s, y + s * 1.4)], c, 2, fill="#fff", close=True)
        self.ground(x - s * 1.5, x + s * 1.5, y + s * 1.4, 4, c)

    def roller(self, x, y, c=COL["dk"], s=10):
        self.poly([(x, y), (x - s, y + s * 1.3), (x + s, y + s * 1.3)], c, 2, fill="#fff", close=True)
        self.circle(x - s * 0.55, y + s * 1.3 + 4, 3.5, "#fff", c, 1.6)
        self.circle(x + s * 0.55, y + s * 1.3 + 4, 3.5, "#fff", c, 1.6)
        self.ground(x - s * 1.5, x + s * 1.5, y + s * 1.3 + 8, 4, c)

    def fixed(self, x, y, c=COL["dk"], half=18):
        self.line(x - half, y, x + half, y, c, 3)
        for i in range(5):
            xx = x - half + 2 + (2 * half - 4) * i / 4
            self.line(xx, y, xx - 7, y + 10, c, 1.3)

    def hinge(self, x, y, c=COL["comp"], r=5.5):
        self.circle(x, y, r, "#fff", c, 2.4)

    def raw(self, s):
        self.el.append(s)

    def svg(self, label=""):
        d = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        aria = f' role="img" aria-label="{escape(label)}"' if label else ""
        return (f'<svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg"{aria}>'
                + d + "\n  " + "\n  ".join(self.el) + "\n</svg>")


class Axes:
    """線性座標軸：資料 → 像素。"""
    def __init__(self, sv, x0, y0, w, h, xr, yr):
        self.sv, self.x0, self.y0, self.w, self.h = sv, x0, y0, w, h
        self.xr, self.yr = xr, yr

    def X(self, v):
        return self.x0 + (v - self.xr[0]) / (self.xr[1] - self.xr[0]) * self.w

    def Y(self, v):
        return self.y0 + self.h - (v - self.yr[0]) / (self.yr[1] - self.yr[0]) * self.h

    def P(self, x, y):
        return (self.X(x), self.Y(y))

    def frame(self, xt, yt, xfmt="{:g}", yfmt="{:g}", grid=True, xlabel="", ylabel="", ylabel_x=None):
        sv = self.sv
        for v in yt:
            if grid:
                sv.line(self.x0, self.Y(v), self.x0 + self.w, self.Y(v), COL["grid"], 1)
            sv.line(self.x0 - 5, self.Y(v), self.x0, self.Y(v), COL["mut"], 1.2)
            sv.text(self.x0 - 9, self.Y(v) + 4, yfmt.format(v), 11.5, COL["mut"], "end")
        for v in xt:
            if grid:
                sv.line(self.X(v), self.y0, self.X(v), self.y0 + self.h, COL["grid"], 1)
            sv.line(self.X(v), self.y0 + self.h, self.X(v), self.y0 + self.h + 5, COL["mut"], 1.2)
            sv.text(self.X(v), self.y0 + self.h + 19, xfmt.format(v), 11.5, COL["mut"])
        sv.line(self.x0, self.y0 + self.h, self.x0 + self.w, self.y0 + self.h, COL["dk"], 1.8)
        sv.line(self.x0, self.y0, self.x0, self.y0 + self.h, COL["dk"], 1.8)
        if xlabel:
            sv.text(self.x0 + self.w / 2, self.y0 + self.h + 40, xlabel, 13, COL["dk"])
        if ylabel:
            sv.text(ylabel_x if ylabel_x else self.x0, self.y0 - 12, ylabel, 13, COL["dk"], "middle")

    def curve(self, xs, ys, c, w=2.6, dash=None, clip=True):
        pts = []
        for x, y in zip(xs, ys):
            if clip and not (self.yr[0] - 1e-9 <= y <= self.yr[1] + 1e-9):
                if pts:
                    self.sv.poly(pts, c, w, dash)
                    pts = []
                continue
            pts.append(self.P(x, y))
        if pts:
            self.sv.poly(pts, c, w, dash)
