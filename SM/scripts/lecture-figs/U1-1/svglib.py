"""Tiny SVG helper: every coordinate is computed by the caller from physical values."""
import re, html

FONT = "Noto Sans TC, Microsoft JhengHei, sans-serif"
AIR, AIR_S = "#f5f5f5", "#9e9e9e"
WAT, WAT_S = "#4fc3f7", "#0288d1"
SOL, SOL_S = "#a1887f", "#6d4c41"
INK, MUT = "#263238", "#607d8b"


def esc(s):
    return html.escape(s, quote=False)


def rich(s, size):
    """'V_{s} = 1' -> tspans; _{..} subscript, ^{..} superscript, *..* bold."""
    out, shift = [], 0.0
    pos = 0
    for m in re.finditer(r"(_\{[^}]*\}|\^\{[^}]*\})", s):
        if m.start() > pos:
            seg = s[pos:m.start()]
            if shift:
                out.append(f'<tspan dy="{-shift:.1f}">{esc(seg)}</tspan>'); shift = 0.0
            else:
                out.append(esc(seg))
        tok = m.group(0)
        body = tok[2:-1]
        d = 0.28 * size if tok[0] == "_" else -0.38 * size
        out.append(f'<tspan dy="{d - shift:.1f}" font-size="{0.74*size:.1f}">{esc(body)}</tspan>')
        shift = d
        pos = m.end()
    if pos < len(s):
        seg = s[pos:]
        if shift:
            out.append(f'<tspan dy="{-shift:.1f}">{esc(seg)}</tspan>')
        else:
            out.append(esc(seg))
    return "".join(out)


def T(x, y, s, size=13, fill=INK, anchor="middle", weight=None, extra=""):
    w = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}"{w}{extra}>{rich(s, size)}</text>')


def R(x, y, w, h, fill, stroke="none", sw=1.5, extra=""):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>')


def L(x1, y1, x2, y2, stroke=INK, sw=1.4, dash=None, extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}{extra}/>')


def PL(pts, stroke, sw=2.2, dash=None, fill="none", extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{extra}/>'


def PG(pts, fill, stroke="none", sw=1, extra=""):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'


def C(x, y, r, fill, stroke="none", sw=1):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def vdim(x, y1, y2, color=INK, tick=6, sw=1.3):
    """vertical dimension line with end ticks"""
    return (L(x, y1, x, y2, color, sw) + L(x - tick, y1, x + tick, y1, color, sw)
            + L(x - tick, y2, x + tick, y2, color, sw))


def hdim(y, x1, x2, color=INK, tick=6, sw=1.3):
    return (L(x1, y, x2, y, color, sw) + L(x1, y - tick, x1, y + tick, color, sw)
            + L(x2, y - tick, x2, y + tick, color, sw))


def arrow_defs(ids=(("ar", "#455a64"),)):
    s = "<defs>"
    for i, c in ids:
        s += (f'<marker id="{i}" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto">'
              f'<path d="M0,0 L0,6 L8,3 z" fill="{c}"/></marker>')
    return s + "</defs>"


def svg(w, h, body, idp=""):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="{FONT}">\n' + "\n".join(body) + "\n</svg>")
