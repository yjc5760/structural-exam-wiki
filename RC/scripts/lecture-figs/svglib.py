# -*- coding: utf-8 -*-
"""RC 講義共用 SVG 小工具（lecture-figs/*/gen_figs.py 共用）。

座標一律由呼叫端以數值換算後傳入；本檔只負責輸出 SVG 元素。
marker id 一律由呼叫端加圖號前綴（如 f3-arr），避免整頁 id 重複。
注入：inject(html, {id: svg}) 只替換 <!--FIG:id--> 之後緊接的 <svg>…</svg>，
找不到標記或標記重複即報錯；重跑結果逐位元相同。
"""
import re

INK, MUT, AX = "#263238", "#607d8b", "#455a64"
BLUE, BLUE2, BLUEL = "#1565c0", "#0d47a1", "#e3f2fd"
RED, RED2 = "#c62828", "#ffcdd2"
GRN, GRN2 = "#2e7d32", "#c8e6c9"
ORG, ORG2 = "#ef6c00", "#fff3e0"
PUR, PUR2 = "#6a1b9a", "#f3e5f5"
GREY, GREY2 = "#546e7a", "#eceff1"
BROWN, BROWN2 = "#6d4c41", "#efebe9"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, s, size=12, anchor="start", fill=INK, bold=False, italic=False, raw=False):
    w = ' font-weight="700"' if bold else ""
    it = ' font-style="italic"' if italic else ""
    body = s if raw else esc(s)
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{fill}"{w}{it}>{body}</text>')


def sub(base, s, size=None):
    """回傳含下標的 raw 文字片段：sub('f','ti') → f<tspan…>ti</tspan><tspan dy…>"""
    return (f'{esc(base)}<tspan dy="4" font-size="72%">{esc(s)}</tspan>'
            f'<tspan dy="-4"> </tspan>')


def L(x1, y1, x2, y2, stroke=AX, w=1.4, dash=None, marker=None, mstart=None, op=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{marker})"' if marker else ""
    ms = f' marker-start="url(#{mstart})"' if mstart else ""
    o = f' opacity="{op}"' if op else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{w}"{d}{m}{ms}{o}/>')


def P(pts, fill="none", stroke=AX, w=1.5, dash=None, op=None, close=True):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    tag = "polygon" if close else "polyline"
    da = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' fill-opacity="{op}"' if op is not None else ""
    return f'<{tag} points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"{da}{o}/>'


def R(x, y, w, h, fill=GREY2, stroke=GREY, sw=1.5, rx=0, dash=None, op=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' fill-opacity="{op}"' if op is not None else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da}{o}/>')


def C(x, y, r, fill=INK, stroke="none", sw=1.4):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def PATH(d, fill="none", stroke=AX, w=1.5, dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"{da}/>'


def defs(*markers):
    out = ["<defs>"]
    for name, col in markers:
        out.append(f'<marker id="{name}" markerWidth="9" markerHeight="9" refX="7" refY="4.5" '
                   f'orient="auto-start-reverse"><path d="M0,0 L9,4.5 L0,9 z" fill="{col}"/></marker>')
    out.append("</defs>")
    return "".join(out)


def svg(w, h, body, label):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="{esc(label)}">\n' + "\n".join(body) + "\n</svg>")


def box(x, y, w, h, lines, fill=GREY2, stroke=GREY, size=12.5, color=INK, bold_first=False, rx=6):
    out = [R(x, y, w, h, fill, stroke, 1.4, rx)]
    n = len(lines)
    lh = size * 1.45
    y0 = y + h / 2 - (n - 1) * lh / 2 + size * 0.35
    for i, s in enumerate(lines):
        out.append(T(x + w / 2, y0 + i * lh, s, size, "middle", color, bold_first and i == 0))
    return out


def diamond(cx, cy, w, h, lines, fill=ORG2, stroke=ORG, size=12.5):
    out = [P([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)], fill, stroke, 1.6)]
    n = len(lines)
    lh = size * 1.4
    y0 = cy - (n - 1) * lh / 2 + size * 0.35
    for i, s in enumerate(lines):
        out.append(T(cx, y0 + i * lh, s, size, "middle", INK))
    return out


def stress_diag(x0, yt, yb, ft, fb, k, comp_right=True, lim=None):
    """應力分布圖：x0 為零線，yt/yb 為頂底 y；ft/fb 為應力（壓為正，畫向右）；k=px per unit。"""
    out = [L(x0, yt - 6, x0, yb + 6, AX, 1.2)]
    xt, xb = x0 + ft * k, x0 + fb * k
    pts = [(x0, yt), (xt, yt), (xb, yb), (x0, yb)]
    # 分成壓/拉兩色：若同號一塊，否則以零點切開
    if ft * fb >= 0:
        col = (BLUEL, BLUE) if (ft + fb) >= 0 else (RED2, RED)
        out.append(P(pts, col[0], col[1], 1.6))
    else:
        yz = yt + (yb - yt) * ft / (ft - fb)
        ct = (BLUEL, BLUE) if ft > 0 else (RED2, RED)
        cb = (BLUEL, BLUE) if fb > 0 else (RED2, RED)
        out.append(P([(x0, yt), (xt, yt), (x0, yz)], ct[0], ct[1], 1.6))
        out.append(P([(x0, yz), (xb, yb), (x0, yb)], cb[0], cb[1], 1.6))
    return out, xt, xb


def inject(html, figs):
    for fid, s in figs.items():
        mark = f"<!--FIG:{fid}-->"
        n = html.count(mark)
        if n != 1:
            raise SystemExit(f"標記 {mark} 出現 {n} 次")
        i = html.index(mark) + len(mark)
        m = re.match(r"\s*<svg\b.*?</svg>", html[i:], flags=re.S)
        if m:
            html = html[:i] + "\n" + s + html[i + m.end():]
        else:
            html = html[:i] + "\n" + s + html[i:]
    return html
