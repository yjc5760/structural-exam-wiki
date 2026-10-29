"""Tiny SVG helper for lecture figures (inline SVG, fonts inherited from page)."""
import math

INK = "#263238"; MUT = "#607d8b"; BLUE = "#1565c0"; RED = "#c62828"
GREEN = "#2e7d32"; ORANGE = "#ef6c00"; PURPLE = "#6a1b9a"
STEEL = "#cfd8dc"; STEEL_D = "#455a64"; WELD = "#ff8a65"; GRID = "#eceff1"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Fig:
    def __init__(self, w, h, pid):
        self.w, self.h, self.pid = w, h, pid
        self.el = []
        self.defs = []
        self._markers = set()

    # ---------- primitives ----------
    def raw(self, s):
        self.el.append(s)

    def text(self, x, y, s, size=13, fill=INK, anchor="start", weight=None, italic=False, rot=None):
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        wgt = f' font-weight="{weight}"' if weight else ""
        it = ' font-style="italic"' if italic else ""
        tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
        self.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}"{a}{wgt}{it}{tr}>{esc(s)}</text>')

    def lines(self, x, y, rows, size=13, fill=INK, anchor="start", lh=None, weight=None):
        lh = lh or size * 1.5
        for i, r in enumerate(rows):
            if isinstance(r, tuple):
                s, f2, w2 = (r + (None,))[:3] if len(r) == 2 else r
                self.text(x, y + i * lh, s, size, f2, anchor, w2)
            else:
                self.text(x, y + i * lh, r, size, fill, anchor, weight)

    def rect(self, x, y, w, h, fill="none", stroke=INK, sw=1.2, rx=0, dash=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{op}"' if op is not None else ""
        self.el.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1.2, dash=None, arrow=None, arrow_start=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{self.marker(arrow)})"' if arrow else ""
        ms = f' marker-start="url(#{self.marker(arrow_start, start=True)})"' if arrow_start else ""
        o = f' opacity="{op}"' if op is not None else ""
        self.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}{m}{ms}{o}/>')

    def path(self, d, fill="none", stroke=INK, sw=1.2, dash=None, arrow=None, op=None, join="round"):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{self.marker(arrow)})"' if arrow else ""
        o = f' opacity="{op}"' if op is not None else ""
        self.el.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="{join}"{ds}{m}{o}/>')

    def poly(self, pts, fill="none", stroke=INK, sw=1.2, close=True, dash=None, op=None, arrow=None):
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + (" Z" if close else "")
        self.path(d, fill, stroke, sw, dash, arrow=arrow, op=op)

    def circle(self, cx, cy, r, fill="none", stroke=INK, sw=1.2, op=None):
        o = f' opacity="{op}"' if op is not None else ""
        self.el.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{o}/>')

    def marker(self, color, start=False):
        mid = f"{self.pid}-ar-{color.strip('#')}{'-s' if start else ''}"
        if mid not in self._markers:
            self._markers.add(mid)
            if start:
                self.defs.append(f'<marker id="{mid}" markerWidth="10" markerHeight="10" refX="1" refY="4" orient="auto"><path d="M9,0 L9,8 L0,4 z" fill="{color}"/></marker>')
            else:
                self.defs.append(f'<marker id="{mid}" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4 z" fill="{color}"/></marker>')
        return mid

    def hatch(self, color="#90a4ae", gap=7, name="h"):
        hid = f"{self.pid}-{name}"
        self.defs.append(f'<pattern id="{hid}" width="{gap}" height="{gap}" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="{gap}" stroke="{color}" stroke-width="1.2"/></pattern>')
        return f"url(#{hid})"

    def dim(self, x1, y1, x2, y2, label, color=MUT, off=0, size=12, lpos=None, anchor="middle"):
        """dimension line with ticks; label at midpoint offset."""
        self.line(x1, y1, x2, y2, color, 1.1, arrow=color, arrow_start=color)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        lx, ly = lpos if lpos else (mx, my - 6)
        self.text(lx, ly, label, size, color, anchor, "600")

    def svg(self):
        d = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        return (f'<svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg">\n'
                + d + "\n" + "\n".join(self.el) + "\n</svg>")


def axes(f, x0, y0, x1, y1, xmin, xmax, ymin, ymax):
    """return mapping functions for a plot box (x0,y0)-(x1,y1) in px; y0 top."""
    X = lambda v: x0 + (v - xmin) / (xmax - xmin) * (x1 - x0)
    Y = lambda v: y1 - (v - ymin) / (ymax - ymin) * (y1 - y0)
    return X, Y
