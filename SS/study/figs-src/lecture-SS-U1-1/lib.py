"""Tiny SVG helper library for lecture figures (all geometry computed, no hand-drawn curves)."""
import math, re
from xml.sax.saxutils import escape

INK = '#263238'; MUT = '#607d8b'; GRID = '#e3e8eb'
TEN = '#2e7d32'; TEN2 = '#e8f5e9'; TENM = '#a5d6a7'
COMP = '#c62828'; COMP2 = '#ffebee'; COMPM = '#ef9a9a'
AC = '#1565c0'; AC2 = '#e3f2fd'; ACM = '#90caf9'
WARN = '#ef6c00'; WARN2 = '#fff3e0'; WARNM = '#ffcc80'
KEY = '#6a1b9a'; KEY2 = '#f3e5f5'
STEEL = '#90a4ae'; STEEL2 = '#eceff1'; STEEL3 = '#cfd8dc'
SERIF = "'Times New Roman',Times,serif"


def f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def _math(s, size):
    """Mini markup -> tspans.  _{..} subscript, ^{..} superscript, *x* italic (serif)."""
    out = []
    i = 0
    dy = 0  # current offset
    sub = round(size * 0.28, 1); sup = round(size * 0.38, 1)
    pat = re.compile(r'(_\{[^}]*\}|\^\{[^}]*\}|\*[^*]+\*)')
    for tok in pat.split(s):
        if not tok:
            continue
        if tok.startswith('_{'):
            out.append(f'<tspan dy="{sub}" font-size="{f(size*0.72)}">{_inner(tok[2:-1])}</tspan><tspan dy="{-sub}">​</tspan>')
        elif tok.startswith('^{'):
            out.append(f'<tspan dy="{-sup}" font-size="{f(size*0.72)}">{_inner(tok[2:-1])}</tspan><tspan dy="{sup}">​</tspan>')
        elif tok.startswith('*'):
            out.append(f'<tspan font-style="italic" font-family="{SERIF}">{escape(tok[1:-1])}</tspan>')
        else:
            out.append(escape(tok))
    return ''.join(out)


def _inner(s):
    # allow italics inside sub/sup
    return re.sub(r'\*([^*]+)\*', lambda m: f'<tspan font-style="italic" font-family="{SERIF}">{escape(m.group(1))}</tspan>', escape(s).replace('&lt;', '\x00')).replace('\x00', '&lt;')


def T(x, y, s, size=13, fill=INK, anchor='start', weight=None, italic=False, extra=''):
    w = f' font-weight="{weight}"' if weight else ''
    it = f' font-style="italic" font-family="{SERIF}"' if italic else ''
    return f'<text x="{f(x)}" y="{f(y)}" font-size="{f(size)}" fill="{fill}" text-anchor="{anchor}"{w}{it}{extra}>{_math(s, size)}</text>'


def L(x1, y1, x2, y2, c=INK, w=1.5, dash=None, cap='round', op=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    o = f' opacity="{op}"' if op else ''
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{c}" stroke-width="{f(w)}" stroke-linecap="{cap}"{d}{o}/>'


def P(pts, c=INK, w=2, fill='none', dash=None, close=False, op=None, join='round'):
    d = 'M' + ' L'.join(f'{f(x)},{f(y)}' for x, y in pts) + (' Z' if close else '')
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    o = f' opacity="{op}"' if op else ''
    st = f' stroke="{c}" stroke-width="{f(w)}"' if c else ' stroke="none"'
    return f'<path d="{d}" fill="{fill}"{st}{ds}{o} stroke-linejoin="{join}" stroke-linecap="round"/>'


def R(x, y, w, h, fill='none', c=INK, sw=1.2, rx=0, dash=None, op=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    o = f' opacity="{op}"' if op else ''
    st = f' stroke="{c}" stroke-width="{f(sw)}"' if c else ''
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}" fill="{fill}"{st}{ds}{o}/>'


def C(x, y, r, fill='#fff', c=INK, sw=1.5):
    st = f' stroke="{c}" stroke-width="{f(sw)}"' if c else ''
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}"{st}/>'


def head(x, y, ang, c=INK, size=9):
    """Arrow head with tip at (x,y) pointing along angle ang (radians)."""
    a1 = ang + math.radians(155); a2 = ang - math.radians(155)
    p = [(x, y), (x + size * math.cos(a1), y + size * math.sin(a1)),
         (x + size * 0.55 * math.cos(ang + math.pi), y + size * 0.55 * math.sin(ang + math.pi)),
         (x + size * math.cos(a2), y + size * math.sin(a2))]
    return P(p, c=None, fill=c, close=True)


def A(x1, y1, x2, y2, c=INK, w=1.8, size=9, both=False, dash=None):
    ang = math.atan2(y2 - y1, x2 - x1)
    s = size * 0.5
    xe, ye = x2 - s * math.cos(ang), y2 - s * math.sin(ang)
    xs, ys = (x1 + s * math.cos(ang), y1 + s * math.sin(ang)) if both else (x1, y1)
    out = L(xs, ys, xe, ye, c, w, dash) + head(x2, y2, ang, c, size)
    if both:
        out += head(x1, y1, ang + math.pi, c, size)
    return out


def curve_arrow(pts, c=INK, w=1.8, size=9, dash=None):
    x1, y1 = pts[-2]; x2, y2 = pts[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    return P(pts[:-1] + [(x2 - size * 0.5 * math.cos(ang), y2 - size * 0.5 * math.sin(ang))], c, w, dash=dash) + head(x2, y2, ang, c, size)


def dim(x1, y1, x2, y2, label='', c=INK, off=0, size=12, side=1, tick=5, lab_off=None, weight=None, anchor=None):
    """Dimension line with end ticks. off shifts the line perpendicular."""
    ang = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(ang), math.cos(ang)
    ax, ay = x1 + nx * off, y1 + ny * off
    bx, by = x2 + nx * off, y2 + ny * off
    o = L(ax, ay, bx, by, c, 1.1)
    for px, py in ((ax, ay), (bx, by)):
        o += L(px - nx * tick, py - ny * tick, px + nx * tick, py + ny * tick, c, 1.1)
    if label:
        lo = (lab_off if lab_off is not None else 8) * side
        mx, my = (ax + bx) / 2 + nx * lo, (ay + by) / 2 + ny * lo
        if anchor is None:
            anchor = 'middle'
        if abs(math.cos(ang)) > 0.5:  # horizontal-ish
            my += 4 if side > 0 else 0
            o += T(mx, my + (size * 0.35 if side > 0 else -2), label, size, c, anchor, weight)
        else:
            o += T(mx, my + size * 0.35, label, size, c, anchor if anchor != 'middle' else ('start' if side * nx > 0 else 'end'), weight)
    return o


def pin(x, y, c=INK, s=11):
    """Pin support, apex at (x,y)."""
    return (P([(x, y), (x - s, y + s * 1.5), (x + s, y + s * 1.5)], c, 1.5, fill='#fff', close=True)
            + hatch_ground(x - s * 1.6, y + s * 1.5, s * 3.2, c))


def hatch_ground(x, y, w, c=INK, down=True, n=None):
    o = L(x, y, x + w, y, c, 1.5)
    n = n or max(3, int(w / 7))
    for i in range(n + 1):
        xx = x + w * i / n
        o += L(xx, y, xx - 6, y + (7 if down else -7), c, 1)
    return o


def fixed_wall(x, y, w, c=INK, top=False):
    """Horizontal fixed support line centred at x, hatch above (top=True) or below."""
    o = L(x - w / 2, y, x + w / 2, y, c, 3)
    n = max(4, int(w / 7))
    for i in range(n + 1):
        xx = x - w / 2 + w * i / n
        o += L(xx, y, xx - 6, y + (-7 if top else 7), c, 1)
    return o


def svg(w, h, body, label=''):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="{escape(label)}" style="max-width:{w}px">\n{body}\n</svg>')


def poly_fn(fn, a, b, n=200):
    return [fn(a + (b - a) * i / n) for i in range(n + 1)]
