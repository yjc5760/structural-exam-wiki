# -*- coding: utf-8 -*-
"""SM 題組共用的繪圖輔助：深度剖面、XY 座標框。全部只用 structdraw 的 primitives。"""
import sys, math
sys.path.insert(0, "/root/.claude/skills/synced/6983ec08-a01a-44e4-a131-56c9e592c524_ab4f317b-1625-4c71-b32d-871e33fbc9cc/struct-diagram/scripts")
from structdraw import Canvas, C, compose, esc


def frame(cv, x0, x1, y0, y1, xt, yt, xlab, ylab, xfmt="{:g}", yfmt="{:g}",
          grid=True, ylab_dx=-52, xlab_dy=44):
    """畫一個 XY 座標框（模型座標＝資料座標）。xt/yt 為刻度值串列。"""
    if grid:
        for t in xt:
            cv.line((t, y0), (t, y1), C["border"], 1.1)
        for t in yt:
            cv.line((x0, t), (x1, t), C["border"], 1.1)
    cv.line((x0, y0), (x1, y0), C["muted"], 1.9)
    cv.line((x0, y0), (x0, y1), C["muted"], 1.9)
    for t in xt:
        cv.line((t, y0), (t, y0), C["muted"], 1.6)
        cv.text_px(cv.X(t), cv.Y(y0) + 17, xfmt.format(t), 12.5, C["muted"])
    for t in yt:
        cv.text_px(cv.X(x0) - 9, cv.Y(t), yfmt.format(t), 12.5, C["muted"], anchor="end")
    cv.text_px((cv.X(x0) + cv.X(x1)) / 2, cv.Y(y0) + xlab_dy, xlab, 13.5, C["text"])
    cv.text_px(cv.X(x0) + ylab_dx, (cv.Y(y0) + cv.Y(y1)) / 2, ylab, 13.5, C["text"])


def fit(W, H, xr, yr, L, R, T, B):
    """由四邊留白反推 sx 與 ox/oy（等向）。xr/yr 為 (min,max)。"""
    sx = min((W - L - R) / (xr[1] - xr[0]), (H - T - B) / (yr[1] - yr[0]))
    return dict(sx=sx, ox=L - xr[0] * sx, oy=B - yr[0] * sx)


def hatch_band(cv, x0, x1, y0, y1, color, n=16, w=1.2, op=0.75):
    """斜線填充（表示不透水層／夯實面）。"""
    span = (x1 - x0) + (y1 - y0)
    for i in range(n + 1):
        t = x0 + (x1 - x0) * i / n
        cv.line((t, y0), (max(x0, t - (y1 - y0)), y1), color, w, op=op)


def soil_fill(cv, x0, x1, y0, y1, fill):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill)


def wt_symbol(cv, x, y, color=C["deform"], s=0.02):
    """地下水位符號 ▽ 加雙橫線。"""
    cv.polygon([(x - s * 1.6, y), (x + s * 1.6, y), (x, y - s * 2.4)], "none", color, 2.0)
    cv.line((x - s * 1.1, y - s * 3.2), (x + s * 1.1, y - s * 3.2), color, 1.8)
    cv.line((x - s * 0.6, y - s * 4.2), (x + s * 0.6, y - s * 4.2), color, 1.8)


# ── Terzaghi 一維壓密（供繪圖用；數值另在各題 §4 手算對照）──
def U_avg(Tv, terms=200):
    s = 0.0
    for m in range(terms):
        M = (2 * m + 1) * math.pi / 2
        s += 2 / M ** 2 * math.exp(-M ** 2 * Tv)
    return 1 - s


def U_local(Tv, Z=1.0, terms=200):
    s = 0.0
    for m in range(terms):
        M = (2 * m + 1) * math.pi / 2
        s += 2 / M * math.sin(M * Z) * math.exp(-M ** 2 * Tv)
    return 1 - s


def tag_px(cv, x, y, s, size=13, color=None, anchor="middle", weight="700",
           pad=6, bg="#FFFFFFEE", border=None, math=False):
    """帶白底圓角框的標註，避免與線條交疊時看不清。"""
    from structdraw import est_width
    color = color or C["text"]
    w = est_width(s, size) if ("_" in s or "^" in s) else len(s) * size * 0.62
    # 中日文字寬約等於 size，英數約 0.55 size
    w = sum((size * 1.02) if ord(ch) > 0x2E80 else (size * 0.56) for ch in s)
    h = size + pad * 2
    x0 = {"middle": x - w / 2 - pad, "start": x - pad, "end": x - w - pad}[anchor]
    cv.rect_px(x0, y - h / 2, w + pad * 2, h, bg, 6,
               border or "rgba(0,0,0,0.10)", 1)
    if math:
        cv.math_px(x, y, s, size, color, anchor=anchor, weight=weight)
    else:
        cv.text_px(x, y, s, size, color, anchor=anchor, weight=weight)


def seg(cv, p0, p1, col, w, dash=None):
    """像素座標直線（給自訂投影的圖用）。"""
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%s" '
                    'stroke-linecap="round"%s/>' % (p0[0], p0[1], p1[0], p1[1], col, w, d))


def curve(cv, pts, col, w, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    cv.parts.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" '
                    'stroke-linecap="round" stroke-linejoin="round"%s/>'
                    % (" ".join("%.2f,%.2f" % p for p in pts), col, w, d))


def dot(cv, x, y, r, fill, stroke="#FFFFFF", w=2.4):
    cv.parts.append('<circle cx="%.2f" cy="%.2f" r="%.1f" fill="%s" stroke="%s" '
                    'stroke-width="%s"/>' % (x, y, r, fill, stroke, w))


def vbar(cv, cx, base_y, bw, parts_, scale, title=None, sub=None, title_col=None):
    """三相體積柱：parts_ = [(高度值, 填色, 邊色, 標籤), ...]，由下往上堆。
    回傳柱頂的像素 y。"""
    y = base_y
    for h, fill, stroke, lab in parts_:
        hp = h * scale
        if hp <= 0:
            continue
        cv.rect_px(cx - bw / 2, y - hp, bw, hp, fill, 0, stroke, 1.8)
        if lab and hp > 20:
            cv.text_px(cx, y - hp / 2, lab, 12.5, stroke)
        y -= hp
    if title:
        cv.text_px(cx, base_y + 26, title, 13.5, title_col or C["text"], weight="700")
    if sub:
        cv.text_px(cx, base_y + 48, sub, 12, C["muted"])
    return y


def hmonotone(pts, n=240):
    """單調三次 Hermite（Fritsch–Carlson）取樣；pts 為已排序的 (x, y)。"""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    k = len(xs)
    d = [(ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]) for i in range(k - 1)]
    m = [d[0]] + [(d[i - 1] + d[i]) / 2 for i in range(1, k - 1)] + [d[-1]]
    for i in range(k - 1):
        if d[i] == 0:
            m[i] = m[i + 1] = 0
        else:
            a, b = m[i] / d[i], m[i + 1] / d[i]
            s = a * a + b * b
            if s > 9:
                t = 3.0 / (s ** 0.5)
                m[i] = t * a * d[i]; m[i + 1] = t * b * d[i]
    out = []
    for i in range(k - 1):
        h = xs[i + 1] - xs[i]
        for j in range(n // (k - 1) + 1):
            t = j / (n // (k - 1))
            h00 = 2*t**3 - 3*t**2 + 1; h10 = t**3 - 2*t**2 + t
            h01 = -2*t**3 + 3*t**2;    h11 = t**3 - t**2
            out.append((xs[i] + h*t, h00*ys[i] + h10*h*m[i] + h01*ys[i+1] + h11*h*m[i+1]))
    return out
