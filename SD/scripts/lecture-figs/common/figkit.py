"""figkit.py — SD 講義圖的共用小工具（建立在 scripts/structdraw.py 之上）。
- Plot：資料座標 → 像素（線性或對數軸），曲線一律取點畫折線
- flow：決策流程圖（方框／菱形／帶標籤箭頭），節點座標用格線
- embed：把 HTML 中 <!--FIG:id--> 後的 <svg>…</svg> 換成新圖；找不到或重複就報錯
"""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
from structdraw import Canvas, C, FONT, FONT_M, est_width, mtext  # noqa

def new(w, h):
    return Canvas(w, h, sx=1.0, ox=0.0, oy=0.0)

def px_line(cv, x0, y0, x1, y1, color=C['member'], w=2, dash=None, op=1.0):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    cv.parts.append(f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}" stroke="{color}" '
                    f'stroke-width="{w}" stroke-linecap="round"{d} opacity="{op}"/>')

def px_poly(cv, pts, color=C['member'], w=2, dash=None, fill='none', op=1.0):
    s = ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)
    d = f' stroke-dasharray="{dash}"' if dash else ''
    cv.parts.append(f'<polyline points="{s}" fill="{fill}" stroke="{color}" stroke-width="{w}" '
                    f'stroke-linejoin="round" stroke-linecap="round"{d} opacity="{op}"/>')

def px_polygon(cv, pts, fill, stroke='none', w=1, op=1.0):
    s = ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)
    cv.parts.append(f'<polygon points="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" opacity="{op}"/>')

def px_arrow(cv, x0, y0, x1, y1, color=C['load'], w=2.2, head=9, dash=None):
    ang = math.atan2(y1 - y0, x1 - x0)
    bx, by = x1 - head * math.cos(ang), y1 - head * math.sin(ang)
    px_line(cv, x0, y0, bx, by, color, w, dash)
    hw = head * 0.46
    px_polygon(cv, [(x1, y1), (bx - hw * math.sin(ang), by + hw * math.cos(ang)),
                    (bx + hw * math.sin(ang), by - hw * math.cos(ang))], color)

def px_rect(cv, x, y, w, h, fill='none', stroke=C['member'], sw=1.4, rx=6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    cv.parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="{fill}" '
                    f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

def T(cv, x, y, s, size=13, color=C['text'], anchor='middle', weight='400', math_=False):
    if math_:
        cv.math_px(x, y, s, size, color, anchor, weight)
    else:
        cv.text_px(x, y, s, size, color, anchor, weight)

class Plot:
    """矩形繪圖區：x0,y0 為左上角像素；xr,yr 為資料範圍；log 軸以 10 為底"""
    def __init__(self, cv, x0, y0, w, h, xr, yr, xlog=False, ylog=False):
        self.cv, self.x0, self.y0, self.w, self.h = cv, x0, y0, w, h
        self.xr, self.yr, self.xlog, self.ylog = xr, yr, xlog, ylog
    def _n(self, v, r, lg):
        if lg: return (math.log10(v) - math.log10(r[0])) / (math.log10(r[1]) - math.log10(r[0]))
        return (v - r[0]) / (r[1] - r[0])
    def X(self, x): return self.x0 + self._n(x, self.xr, self.xlog) * self.w
    def Y(self, y): return self.y0 + self.h - self._n(y, self.yr, self.ylog) * self.h
    def P(self, x, y): return (self.X(x), self.Y(y))
    def frame(self, xt, yt, xl='', yl='', xfmt='{:g}', yfmt='{:g}', grid=True, size=11.5):
        cv = self.cv
        for v in xt:
            X = self.X(v)
            if grid: px_line(cv, X, self.y0, X, self.y0 + self.h, '#E6EBF1', 1)
            T(cv, X, self.y0 + self.h + 16, xfmt.format(v), size, C['muted'])
        for v in yt:
            Y = self.Y(v)
            if grid: px_line(cv, self.x0, Y, self.x0 + self.w, Y, '#E6EBF1', 1)
            T(cv, self.x0 - 7, Y, yfmt.format(v), size, C['muted'], 'end')
        px_line(cv, self.x0, self.y0 + self.h, self.x0 + self.w, self.y0 + self.h, C['member'], 1.4)
        px_line(cv, self.x0, self.y0, self.x0, self.y0 + self.h, C['member'], 1.4)
        if xl: T(cv, self.x0 + self.w / 2, self.y0 + self.h + 36, xl, 12.5, C['text'])
        if yl: T(cv, self.x0 + 6, self.y0 - 14, yl, 12.5, C['text'], 'start')
    def curve(self, xs, ys, color=C['deform'], w=2.4, dash=None):
        px_poly(self.cv, [self.P(x, y) for x, y in zip(xs, ys)], color, w, dash)
    def dot(self, x, y, r=4.5, fill=C['load']):
        X, Y = self.P(x, y)
        self.cv.parts.append(f'<circle cx="{X:.2f}" cy="{Y:.2f}" r="{r}" fill="{fill}" stroke="#fff" stroke-width="1.5"/>')

# ---------- 流程圖 ----------
def box(cv, cx, cy, w, h, lines, fill='#E3F2FD', stroke='#1565C0', size=12.5, color=C['text'], bold_first=False):
    px_rect(cv, cx - w / 2, cy - h / 2, w, h, fill, stroke, 1.5, 8)
    n = len(lines); lh = size * 1.55
    for i, s in enumerate(lines):
        T(cv, cx, cy + (i - (n - 1) / 2) * lh, s, size, color, 'middle', '700' if (bold_first and i == 0) else '400')

def diamond(cv, cx, cy, w, h, lines, fill='#FFF3E0', stroke='#EF6C00', size=12.5):
    px_polygon(cv, [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)], fill, stroke, 1.6)
    n = len(lines); lh = size * 1.5
    for i, s in enumerate(lines):
        T(cv, cx, cy + (i - (n - 1) / 2) * lh, s, size, C['text'])

def edge(cv, pts, label=None, lpos=None, color=C['member'], lcolor=None, anchor='start'):
    for (a, b), (c, d) in zip(pts[:-2], pts[1:-1]):
        px_line(cv, a, b, c, d, color, 1.6)
    (a, b), (c, d) = pts[-2], pts[-1]
    px_arrow(cv, a, b, c, d, color, 1.6, 8)
    if label:
        x, y = lpos
        T(cv, x, y, label, 12, lcolor or ('#2E7D32' if label == '是' else '#C62828'), anchor, '700')

# ---------- 嵌入 ----------
def finish(svg, fid):
    """id 加圖號前綴，避免同頁不同圖互相污染"""
    return svg.replace('sdclip', f'{fid}-clip')

def embed(html_path, figs):
    s = open(html_path, encoding='utf-8').read()
    for fid, svg in figs.items():
        pat = re.compile(r'(<!--FIG:%s-->\s*)<svg.*?</svg>' % re.escape(fid), re.S)
        n = len(pat.findall(s))
        if n != 1: raise SystemExit(f'FIG:{fid} 出現 {n} 次（應為 1）')
        s = pat.sub(lambda m: m.group(1) + finish(svg, fid), s)
    open(html_path, 'w', encoding='utf-8').write(s)
    print(f'embedded {len(figs)} figs -> {html_path}')
