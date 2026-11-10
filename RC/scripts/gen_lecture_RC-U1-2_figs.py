#!/usr/bin/env python3
"""lecture-RC-U1-2 講義的資料驅動 SVG 圖解產生器。

所有幾何都由 engine.py 的斷面引擎（與講義 §1 同一套式子）或題目給定數值算出，
改任何一個輸入重跑，圖就跟著變。用法：
    python3 scripts/gen_lecture_RC-U1-2_figs.py <輸出 json>
輸出 {圖名: '<svg ...>...</svg>'}，由 apply 步驟換進講義對應的 <div class="fig">。
"""
import json, math, sys, os


# ════ 斷面引擎（講義 §1 的同一套式子） ════
ES = 2.04e6
ECU = 0.003


def beta1(fc):
    return max(0.65, min(0.85, 0.85 - 0.05 * (fc - 280) / 70))


def phi_of(eps_t, fy, spiral=False):
    ety = fy / ES
    lim = 0.005 if fy <= 4200 else ety + 0.003   # 本庫約定：SD420 取 0.005；高強度鋼筋 εty+0.003
    lo = 0.75 if spiral else 0.65
    if eps_t <= ety:
        return lo
    if eps_t >= lim:
        return 0.90
    return lo + (0.90 - lo) * (eps_t - ety) / (lim - ety)


class Section:
    def __init__(self, b, h, fc, fy, layers):
        self.b, self.h, self.fc, self.fy = b, h, fc, fy
        self.layers = layers                       # [(d, As)]
        self.b1 = beta1(fc)
        self.dt = max(d for d, _ in layers)
        self.Ast = sum(A for _, A in layers)
        self.Po = 0.85 * fc * (b * h - self.Ast) + fy * self.Ast

    def at(self, c):
        a = min(self.b1 * c, self.h)
        Cc = 0.85 * self.fc * a * self.b
        P = Cc
        M = Cc * (self.h / 2 - a / 2)
        bars = []
        for d, A in self.layers:
            eps = ECU * (c - d) / c
            fs = max(-self.fy, min(self.fy, ES * eps))
            fn = fs - 0.85 * self.fc if d < a else fs
            F = A * fn
            P += F
            M += F * (self.h / 2 - d)
            bars.append(dict(d=d, A=A, eps=eps, fs=fs, F=F))
        et = ECU * (self.dt - c) / c
        ph = phi_of(et, self.fy)
        return dict(c=c, a=a, Cc=Cc, P=P, M=M, et=et, phi=ph, bars=bars,
                    Pt=P / 1e3, Mt=M / 1e5, fPt=ph * P / 1e3, fMt=ph * M / 1e5)

    def c_pure_bending(self):
        lo, hi = 0.5, self.dt
        for _ in range(200):
            m = (lo + hi) / 2
            if self.at(m)['P'] > 0:
                hi = m
            else:
                lo = m
        return (lo + hi) / 2


# RC-2015-1：60×60，頂底各 4-#10
S15 = Section(60, 60, 350, 4200, [(8, 4 * 8.143), (52, 4 * 8.143)])
# RC-2008-2：40×56，4+2+2 #8
S08 = Section(40, 56, 350, 4200, [(8, 4 * 5.07), (28, 2 * 5.07), (48, 2 * 5.07)])


FONT = "'Microsoft JhengHei','Noto Sans TC','Noto Sans CJK TC',sans-serif"
INK, MUT, GRID = '#263238', '#607d8b', '#eceff1'
BLUE, RED, GRN, ORG, PUR = '#1565c0', '#c62828', '#2e7d32', '#ef6c00', '#6a1b9a'


def f(x):
    return f'{x:.1f}'.rstrip('0').rstrip('.')


class Svg:
    def __init__(self, w, h):
        self.w, self.h, self.el, self.defs = w, h, [], set()

    def add(self, s):
        self.el.append(s)

    def line(self, x1, y1, x2, y2, c=INK, w=1.5, dash=None, arrow=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        m = ''
        if arrow:
            mid = 'ar' + c.strip('#')
            self.defs.add(mid + '|' + c)
            m = f' marker-end="url(#{mid})"'
        self.add(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{c}" stroke-width="{w}"{d}{o}{m}/>')

    def poly(self, pts, c=INK, w=2, fill='none', dash=None, close=False, op=None):
        p = ' '.join(f'{f(x)},{f(y)}' for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' fill-opacity="{op}"' if op else ''
        tag = 'polygon' if close else 'polyline'
        self.add(f'<{tag} points="{p}" fill="{fill}"{o} stroke="{c}" stroke-width="{w}" stroke-linejoin="round"{d}/>')

    def rect(self, x, y, w, h, fill='none', c=INK, sw=1.5, rx=0, op=None, dash=None):
        o = f' fill-opacity="{op}"' if op else ''
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" fill="{fill}"{o} stroke="{c}" stroke-width="{sw}"{d}/>')

    def circ(self, x, y, r, fill=INK, c='none', sw=1.5):
        self.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size=12, c=INK, anchor='start', bold=False, italic=False):
        b = ' font-weight="700"' if bold else ''
        i = ' font-style="italic"' if italic else ''
        s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        self.add(f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" fill="{c}" text-anchor="{anchor}"{b}{i}>{s}</text>')

    def path(self, d, c=INK, w=2, fill='none', dash=None, op=None):
        da = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' fill-opacity="{op}"' if op else ''
        self.add(f'<path d="{d}" fill="{fill}"{o} stroke="{c}" stroke-width="{w}"{da}/>')

    def render(self):
        defs = ''.join(
            f'<marker id="{m.split("|")[0]}" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" '
            f'refX="10" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{m.split("|")[1]}"/></marker>'
            for m in sorted(self.defs))
        return (f'<svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">'
                f'<defs>{defs}</defs>' + ''.join(self.el) + '</svg>')


class Axes:
    """資料座標 → 畫布座標"""
    def __init__(self, svg, x0, y0, w, h, xr, yr):
        self.s, self.x0, self.y0, self.w, self.h, self.xr, self.yr = svg, x0, y0, w, h, xr, yr

    def X(self, v):
        return self.x0 + (v - self.xr[0]) / (self.xr[1] - self.xr[0]) * self.w

    def Y(self, v):
        return self.y0 + self.h - (v - self.yr[0]) / (self.yr[1] - self.yr[0]) * self.h

    def P(self, x, y):
        return (self.X(x), self.Y(y))

    def frame(self, xt, yt, xl, yl, xfmt='{:g}', yfmt='{:g}', grid=True):
        s = self
        for v in xt:
            if grid:
                s.s.line(s.X(v), s.y0, s.X(v), s.y0 + s.h, GRID, 1)
            s.s.line(s.X(v), s.y0 + s.h, s.X(v), s.y0 + s.h + 5, INK, 1.2)
            s.s.text(s.X(v), s.y0 + s.h + 19, xfmt.format(v), 11.5, MUT, 'middle')
        for v in yt:
            if grid:
                s.s.line(s.x0, s.Y(v), s.x0 + s.w, s.Y(v), GRID, 1)
            s.s.line(s.x0 - 5, s.Y(v), s.x0, s.Y(v), INK, 1.2)
            s.s.text(s.x0 - 9, s.Y(v) + 4, yfmt.format(v), 11.5, MUT, 'end')
        s.s.line(s.x0, s.y0 + s.h, s.x0 + s.w + 10, s.y0 + s.h, INK, 1.8, arrow=True)
        s.s.line(s.x0, s.y0 + s.h, s.x0, s.y0 - 10, INK, 1.8, arrow=True)
        s.s.text(s.x0 + s.w + 14, s.y0 + s.h + 4, xl, 13, INK, 'start', True)
        s.s.text(s.x0 - 6, s.y0 - 16, yl, 13, INK, 'start', True)


def label_box(s, x, y, lines, c, w=None, anchor='start', size=12):
    """帶白底的標註，lines=[(text, bold)]"""
    w = w or max(len(t) for t, _ in lines) * size * 0.62 + 12
    h = len(lines) * (size + 5) + 6
    bx = x if anchor == 'start' else x - w if anchor == 'end' else x - w / 2
    s.rect(bx, y, w, h, '#fff', c, 1, 5, op=0.92)
    for i, (t, b) in enumerate(lines):
        s.text(bx + 6, y + 4 + (i + 1) * (size + 4) - 2, t, size if b else size - 0.8, c, 'start', b)


# ════════════════════════════════════════════════════════════
# 圖 0-2  RC-2015-1 的 P-M 互制圖（標稱 vs 設計，實算）
# ════════════════════════════════════════════════════════════
def fig_pm():
    sec = S15
    s = Svg(760, 500)
    ax = Axes(s, 78, 40, 560, 400, (0, 150), (0, 1400))
    ax.frame(range(0, 151, 25), range(0, 1401, 200), 'Mn (tf·m)', 'Pn (tf)')
    cs = [sec.c_pure_bending()] + [x / 10 for x in range(90, 3000)] + [300 + x * 5 for x in range(1, 400)]
    rs = [sec.at(c) for c in cs]
    nom = [(0, 0)] if False else []
    nom = [ax.P(r['Mt'], r['Pt']) for r in rs] + [ax.P(0, sec.Po / 1e3)]
    s.poly(nom, BLUE, 3.2)
    cap = 0.80 * 0.65 * sec.Po / 1e3
    cb = 6120 / (6120 + 4200) * sec.dt
    ctc = 0.375 * sec.dt
    # 設計曲線：依 φ 分區著色
    zones = [(lambda r: r['c'] <= ctc, GRN), (lambda r: ctc <= r['c'] <= cb, ORG), (lambda r: r['c'] >= cb, RED)]
    capped = []
    for r in rs:
        capped.append((r, min(r['fPt'], cap)))
    for cond, col in zones:
        pts = [ax.P(r['fMt'], p) for r, p in capped if cond(r) and r['fPt'] <= cap]
        s.poly(pts, col, 3.4, dash='9 5')
    # 截頂段
    rc = min((r for r in rs if r['fPt'] >= cap), key=lambda r: r['c'])
    s.poly([ax.P(0, cap), ax.P(rc['fMt'] * cap / rc['fPt'] if False else rc['fMt'], cap)], RED, 3.4)
    s.line(ax.X(0), ax.Y(0.65 * sec.Po / 1e3), ax.X(rc['fMt'] * 0.6), ax.Y(0.65 * sec.Po / 1e3), RED, 1, '3 3')
    s.text(ax.X(2), ax.Y(0.65 * sec.Po / 1e3) - 5, 'φPo = 861（截頂前）', 10.5, RED)

    def dot(m, p, col, r=6):
        s.circ(ax.X(m), ax.Y(p), r, col, '#fff', 1.6)

    # 控制點
    P0 = sec.Po / 1e3
    e0 = sec.at(sec.dt)
    eb = sec.at(cb)
    et = sec.at(ctc)
    ep = sec.at(sec.c_pure_bending())
    dot(0, P0, '#0d47a1')
    label_box(s, ax.X(4), ax.Y(P0) - 12, [(f'① 純軸壓 Po = {P0:.0f} tf', True)], '#0d47a1')
    dot(e0['Mt'], e0['Pt'], PUR)
    label_box(s, ax.X(e0['Mt']) + 10, ax.Y(e0['Pt']) - 30, [(f'② εt = 0（c = dt = {sec.dt:g}）', True), (f'({e0["Mt"]:.1f}, {e0["Pt"]:.0f})', False)], PUR)
    dot(eb['Mt'], eb['Pt'], RED, 7)
    label_box(s, ax.X(eb['Mt']) - 6, ax.Y(eb['Pt']) - 64, [(f'③ 平衡點 c = {cb:.2f}', True), (f'Mn 峰值 ({eb["Mt"]:.1f}, {eb["Pt"]:.0f})', False)], RED, anchor='end')
    dot(ep['Mt'], 0, GRN)
    s.line(ax.X(ep['Mt']) - 3, ax.Y(0) - 5, ax.X(30), ax.Y(150), GRN, 1)
    label_box(s, ax.X(8), ax.Y(150) - 34, [(f'④ 純彎 Mn = {ep["Mt"]:.1f}', True), (f'φMn = {ep["fMt"]:.1f}（φ = 0.90）', False)], GRN)
    # 設計曲線上的點
    dot(eb['fMt'], eb['fPt'], RED, 5)
    s.text(ax.X(eb['fMt']) - 4, ax.Y(eb['fPt']) + 20, f'③ ×φ=0.65 → ({eb["fMt"]:.1f}, {eb["fPt"]:.0f})', 11, RED, 'end', True)
    s.add(f'<path d="M{f(ax.X(et["fMt"]))},{f(ax.Y(et["fPt"]) - 10)} l3,7 7,0 -5.5,4.5 2,7.5 -6.5,-4.3 -6.5,4.3 2,-7.5 -5.5,-4.5 7,0 z" fill="#ffb300" stroke="#e65100" stroke-width="1.2"/>')
    label_box(s, ax.X(et['fMt']) + 12, ax.Y(et['fPt']) + 6,
              [(f'★ φMn 峰值 = {et["fMt"]:.1f}', True), (f'εt = 0.005，c = {ctc:.2f}，φPn = {et["fPt"]:.0f}', False)], '#e65100')
    dot(ep['fMt'], 0, GRN, 4.5)
    s.text(ax.X(2), ax.Y(cap) - 8, f'0.80φPo = {cap:.0f}（水平截頂）', 11.5, RED, bold=True)
    # 圖例
    lx, ly = 470, 52
    s.rect(lx, ly, 260, 112, '#fafafa', '#cfd8dc', 1, 7)
    s.line(lx + 12, ly + 20, lx + 44, ly + 20, BLUE, 3.2)
    s.text(lx + 52, ly + 24, '標稱 (Mn, Pn)', 12)
    s.line(lx + 12, ly + 44, lx + 44, ly + 44, RED, 3.4, '9 5')
    s.text(lx + 52, ly + 48, '設計：壓力控制 φ = 0.65', 12)
    s.line(lx + 12, ly + 68, lx + 44, ly + 68, ORG, 3.4, '9 5')
    s.text(lx + 52, ly + 72, '設計：過渡區 φ 0.65→0.90', 12)
    s.line(lx + 12, ly + 92, lx + 44, ly + 92, GRN, 3.4, '9 5')
    s.text(lx + 52, ly + 96, '設計：拉力控制 φ = 0.90', 12)
    s.text(78, 492, 'RC-2015-1 斷面：60×60 cm、頂底各 4-#10、d′ = 8、d = 52、f′c = 350、fy = 4200（kgf/cm²）', 11.5, MUT)
    return s.render()


# ════════════════════════════════════════════════════════════
# 圖 2-1  應變扇形：控制點都是繞 εcu = 0.003 旋轉的直線
# ════════════════════════════════════════════════════════════
def fig_fan():
    sec = S15
    s = Svg(860, 430)
    top, H = 60, 300          # 斷面 60 cm → 300 px
    k = H / sec.h
    # 斷面
    sx = 80
    s.text(sx + 75, 34, '斷面 60×60', 13, INK, 'middle', True)
    s.rect(sx, top, 150, H, '#eceff1', '#37474f', 2)
    for d in (8, 52):
        for i in range(4):
            s.circ(sx + 22 + i * 35.3, top + d * k, 7, BLUE)
    s.line(sx - 6, top, sx + 156, top, RED, 4)
    s.text(sx + 75, top - 8, '壓力面', 11, RED, 'middle')
    for d, lab in ((8, "d′ = 8"), (52, 'dt = 52')):
        s.text(sx - 8, top + d * k + 4, lab, 11, MUT, 'end')
    s.line(sx + 150, top + H / 2, sx + 170, top + H / 2, MUT, 1, '3 3')
    s.text(sx + 174, top + H / 2 + 4, 'h/2', 10.5, MUT)
    # 應變軸
    ax0 = 540                   # 應變 0 的 x
    kx = 16000                  # px / 單位應變
    X = lambda e: ax0 + e * kx  # 壓為正 → 右
    s.text(420, 34, '應變分布（同一比例尺）', 13, INK, 'middle', True)
    s.line(X(0), top - 6, X(0), top + H + 6, '#90a4ae', 1.5)
    s.text(X(0), top + H + 22, '0', 11, MUT, 'middle')
    s.line(X(ECU), top - 4, X(ECU), top + H + 6, '#cfd8dc', 1, '4 3')
    s.text(X(ECU), top + H + 22, '+0.003', 11, MUT, 'middle')
    ety = 4200 / ES
    s.line(X(-ety), top + 30, X(-ety), top + H + 6, '#a5d6a7', 1, '4 3')
    s.text(X(-ety), top + H + 22, '−εy', 11, GRN, 'middle')
    s.line(X(-0.005), top + 30, X(-0.005), top + H + 6, '#c8e6c9', 1, '4 3')
    s.text(X(-0.005), top + H + 22, '−0.005', 11, GRN, 'middle')
    s.line(sx + 150, top + 52 * k, X(ECU) + 30, top + 52 * k, '#b0bec5', 0.8, '2 4')
    cb = 6120 / 10320 * 52
    cases = [
        (None, '①', '#0d47a1', 'c → ∞（均勻 0.003）'),
        (52, '②', PUR, 'c = 52，εt = 0'),
        (cb, '③', RED, f'c = {cb:.2f}，εt = εy'),
        (19.5, '★', '#e65100', 'c = 19.50，εt = 0.005'),
        (sec.c_pure_bending(), '④', GRN, f'c = {sec.c_pure_bending():.2f}，P = 0'),
    ]
    for c, tag, col, txt in cases:
        if c is None:
            s.line(X(ECU), top, X(ECU), top + H, col, 2.6)
            s.text(X(ECU) + 6, top + H - 6, tag, 13, col, bold=True)
            continue
        eb = ECU * (c - sec.h) / c
        s.line(X(ECU), top, X(eb), top + H, col, 2.4)
        # dt 處的點
        e52 = ECU * (c - 52) / c
        s.circ(X(e52), top + 52 * k, 4, col)
        # 中性軸
        s.line(X(0) - 6, top + c * k, X(0) + 6, top + c * k, col, 2)
        s.text(X(eb) - 4, top + H + 40 if tag in '④★' else top + H - 8, tag, 13, col, 'end' if tag in '④★' else 'start', True) if False else None
    # 標籤欄
    lx = 640
    s.circ(X(ECU), top, 6, '#fff', INK, 2.2)
    s.text(X(ECU) + 10, top - 6, 'εcu = 0.003 固定不動（樞紐）', 11.5, INK, bold=True)
    for i, (c, tag, col, txt) in enumerate(cases):
        y = top + 70 + i * 34
        s.rect(lx, y - 15, 205, 26, '#fff', col, 1.2, 6)
        s.text(lx + 8, y + 3, f'{tag} {txt}', 12, col, bold=True)
    # 線端標號
    for c, tag, col, txt in cases[1:]:
        eb = ECU * (c - sec.h) / c
        s.text(X(eb), top + H + 40, tag, 13, col, 'middle', True)
    s.text(X(0), top + H + 62, '← 拉　｜　壓 →', 11.5, MUT, 'middle')
    return s.render()


# ════════════════════════════════════════════════════════════
# 圖 1-2  RC-2008-2（範例 A）三張圖：幾何／應變／應力與合力，按比例
# ════════════════════════════════════════════════════════════
def fig_ex_a():
    sec = S08
    r = sec.at(48)
    s = Svg(800, 400)
    top, H = 50, 280
    k = H / sec.h               # 5 px/cm
    # ── 斷面 40×56
    sx, sw = 70, 40 * k * 0.8   # 寬度 0.8 倍比例以省空間
    kb = sw / 40
    s.text(sx + sw / 2, 26, '① 斷面 40×56', 13, INK, 'middle', True)
    s.rect(sx, top, sw, H, '#eceff1', '#37474f', 2)
    rows = [(8, 4), (28, 2), (48, 2)]
    for d, n in rows:
        xs = [sx + 6 * kb + i * (28 * kb) / (n - 1) for i in range(n)]
        for x in xs:
            s.circ(x, top + d * k, 6, BLUE)
    s.rect(sx, top, sw, r['a'] * k, RED, 'none', 0, op=0.13)
    s.line(sx - 4, top, sx + sw + 4, top, RED, 4)
    for d, lab in ((8, 'd₁ = 8（4-#8）'), (28, 'd₂ = 28（2-#8）＝ h/2'), (48, 'd₃ = 48（2-#8）')):
        s.text(sx + sw + 8, top + d * k + 4, lab, 11, INK)
    s.line(sx - 14, top, sx - 14, top + r['a'] * k, RED, 1.2)
    s.text(sx - 18, top + r['a'] * k / 2, f"a={r['a']:.1f}", 11, RED, 'end')
    # ── 應變
    ax0, kx = 380, 40000
    X = lambda e: ax0 + e * kx
    s.text(ax0 + 40, 26, '② 應變（c = dt = 48）', 13, INK, 'middle', True)
    s.line(X(0), top - 4, X(0), top + H + 4, '#90a4ae', 1.5)
    eb = ECU * (48 - 56) / 48
    s.poly([(X(0), top), (X(ECU), top), (X(0), top + 48 * k)], RED, 2, '#ffcdd2', close=True)
    s.poly([(X(0), top + 48 * k), (X(eb), top + H), (X(0), top + H)], GRN, 2, '#c8e6c9', close=True)
    ey = 4200 / ES
    s.line(X(ey), top - 4, X(ey), top + H, ORG, 1.4, '5 4')
    s.text(X(ey) - 2, top + H + 18, f'εy = {ey:.5f}', 11, ORG, 'middle', True)
    s.text(X(ECU) + 4, top - 6, '0.003', 11, RED, bold=True)
    for b in r['bars']:
        y = top + b['d'] * k
        s.line(X(0), y, X(b['eps']), y, INK, 2)
        s.circ(X(b['eps']), y, 3.5, INK)
        yl = '✔ 降伏' if abs(b['eps']) >= ey else '✘ 未降伏' if b['eps'] > 0 else ''
        col = RED if yl.startswith('✔') else ORG
        if not yl:
            continue
        s.text(max(X(b['eps']), X(ey)) + 8, y + 4, f"{b['eps']:.5f} {yl}", 11, col if yl else MUT, bold=bool(yl))
    s.line(X(0) - 30, top + 48 * k, X(0) + 145, top + 48 * k, INK, 1.2, '5 4')
    s.text(X(0) + 150, top + 48 * k + 4, '中性軸', 11, INK, 'start', True)
    # ── 應力與合力
    fx = 610
    s.text(fx + 70, 26, '③ 應力與合力', 13, INK, 'middle', True)
    s.rect(fx, top, 46, r['a'] * k, '#ef9a9a', RED, 1.6)
    s.text(fx + 23, top + r['a'] * k / 2 - 4, "0.85f′c", 10.5, INK, 'middle', True)
    s.line(fx, top - 4, fx, top + H + 4, '#90a4ae', 1.5)
    kf = 100 / r['Cc']           # 力的長度比例（全部同一比例）
    yc = top + r['a'] * k / 2
    s.line(fx + 50, yc, fx + 50 + r['Cc'] * kf, yc, RED, 3.2, arrow=True)
    s.text(fx + 54, yc + 17, f"Cc = {r['Cc']/1e3:.1f} tf", 11.5, RED, bold=True)
    names = ['Cs1', 'Cs2', 'T3']
    for b, nm in zip(r['bars'], names):
        y = top + b['d'] * k
        L = abs(b['F']) * kf
        if L > 1:
            s.line(fx + 50, y, fx + 50 + L, y, RED, 2.6, arrow=True)
        s.text(fx + 58 + L, y - 6 if nm == 'Cs2' else y + 4, f"{nm} = {b['F']/1e3:.1f} tf" if L > 1 else f'{nm} = 0（εt = 0）', 11, RED if L > 1 else MUT, bold=True)
    # 形心與力臂
    s.line(fx - 8, top + 28 * k, fx + 175, top + 28 * k, PUR, 1, '2 3')
    s.text(fx - 10, top + 28 * k + 4, 'h/2', 11, PUR, 'end', True)
    s.text(fx + 50, top + 28 * k + 20, '力臂 = 0 → 只貢獻 Pn', 10.5, PUR, 'start', True)
    s.text(X(0) + 8, top + 48 * k - 6, 'εt = 0', 11, GRN, 'start', True)
    s.text(40, top + H + 50, f"Pn = {r['Pt']:.1f} tf　Mn = {r['Mt']:.2f} tf·m　（力箭頭與應變均按比例；斷面寬向縮為 0.8 倍）", 12, INK, bold=True)
    return s.render()


# ════════════════════════════════════════════════════════════
# 圖 3-1  Mn(c) 與 φMn(c)：兩個峰值不在同一點
# ════════════════════════════════════════════════════════════
def fig_mc():
    sec = S15
    s = Svg(760, 430)
    ax = Axes(s, 70, 40, 600, 300, (0, 60), (0, 150))
    cb = 6120 / 10320 * 52
    ctc = 19.5
    for x0, x1, col in ((0, ctc, '#e8f5e9'), (ctc, cb, '#fff3e0'), (cb, 60, '#ffebee')):
        s.rect(ax.X(x0), ax.y0, ax.X(x1) - ax.X(x0), ax.h, col, 'none', 0, op=0.7)
    ax.frame(range(0, 61, 10), range(0, 151, 25), 'c (cm)', 'tf·m')
    cp = sec.c_pure_bending()
    cs = [cp + i * (60 - cp) / 600 for i in range(601)]
    rs = [sec.at(c) for c in cs]
    s.poly([ax.P(r['c'], r['Mt']) for r in rs], BLUE, 3.2)
    s.poly([ax.P(r['c'], r['fMt']) for r in rs], RED, 3.2, dash='9 5')
    b, t, p = sec.at(cb), sec.at(ctc), sec.at(cp)
    for rr, col in ((b, BLUE), (b, RED), (t, RED), (t, BLUE)):
        val = rr['Mt'] if col == BLUE else rr['fMt']
        s.line(ax.X(rr['c']), ax.Y(val), ax.X(rr['c']), ax.Y(0), col, 1, '3 3')
    s.circ(ax.X(cb), ax.Y(b['Mt']), 7, BLUE, '#fff', 1.6)
    label_box(s, ax.X(cb) + 10, ax.Y(b['Mt']) - 14, [(f'Mn 峰值 {b["Mt"]:.2f}', True), (f'c = cb = {cb:.2f}（平衡點）', False)], BLUE)
    s.circ(ax.X(cb), ax.Y(b['fMt']), 5, RED, '#fff', 1.4)
    s.text(ax.X(cb) + 9, ax.Y(b['fMt']) - 10, f'×0.65 → {b["fMt"]:.1f}', 11.5, RED, bold=True)
    s.add(f'<path d="M{f(ax.X(ctc))},{f(ax.Y(t["fMt"]) - 10)} l3,7 7,0 -5.5,4.5 2,7.5 -6.5,-4.3 -6.5,4.3 2,-7.5 -5.5,-4.5 7,0 z" fill="#ffb300" stroke="#e65100" stroke-width="1.2"/>')
    label_box(s, ax.X(ctc) - 12, ax.Y(t['fMt']) - 52, [(f'★ φMn 峰值 {t["fMt"]:.1f}', True), ('c = 0.375d = 19.50（εt = 0.005）', False)], '#e65100', anchor='end')
    s.circ(ax.X(ctc), ax.Y(t['Mt']), 4.5, BLUE)
    s.text(ax.X(ctc) - 8, ax.Y(t['Mt']) - 6, f'{t["Mt"]:.2f}', 11, BLUE, 'end')
    s.circ(ax.X(cp), ax.Y(p['Mt']), 4.5, GRN)
    s.text(ax.X(0.8), ax.Y(50), f'純彎 c = {cp:.2f}', 11, GRN, bold=True)
    s.text(ax.X(0.8), ax.Y(50) + 15, f'Mn {p["Mt"]:.1f}／φMn {p["fMt"]:.1f}', 11, GRN)
    # 區帶標題
    yb = ax.y0 + ax.h
    s.text(ax.X(ctc / 2), yb - 30, '拉力控制 φ = 0.90', 12, GRN, 'middle', True)
    s.text(ax.X((ctc + cb) / 2), yb - 30, '過渡區', 12, ORG, 'middle', True)
    s.text(ax.X((cb + 60) / 2), yb - 30, '壓力控制 φ = 0.65', 12, RED, 'middle', True)
    s.text(ax.X((ctc + cb) / 2), yb - 14, 'φ +38%、Mn −15%', 11, ORG, 'middle')
    label_box(s, ax.X(21), ax.Y(52), [('小跳階：a 越過 d′ = 8', True), ('壓力筋開始扣 0.85f′c', False)], MUT, size=11)
    s.line(ax.X(21), ax.Y(52) + 10, ax.X(10.2), ax.Y(sec.at(10.05)['Mt']) + 4, MUT, 1)
    # 圖例
    s.line(80, 400, 112, 400, BLUE, 3.2)
    s.text(118, 404, '標稱 Mn(c)', 12)
    s.line(230, 400, 262, 400, RED, 3.2, '9 5')
    s.text(268, 404, '設計 φMn(c)', 12)
    s.text(380, 404, 'RC-2015-1 實算（左端起於純彎 P = 0；c 越大軸力越大）', 11.5, MUT)
    return s.render()


# ════════════════════════════════════════════════════════════
# 圖 4-1  φ–εt 分段圖（按比例）
# ════════════════════════════════════════════════════════════
def fig_phi():
    s = Svg(760, 380)
    ax = Axes(s, 70, 40, 600, 260, (0, 0.007), (0.6, 0.95))
    ax.frame([0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007], [0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95],
             'εt', 'φ', xfmt='{:.3f}', yfmt='{:.2f}')
    ety = 4200 / ES
    xs = [i * 0.007 / 700 for i in range(701)]
    s.poly([ax.P(x, phi_of(x, 4200)) for x in xs], RED, 3.4)
    s.poly([ax.P(x, phi_of(x, 4200, True)) for x in xs], BLUE, 3, dash='9 5')
    for x, lab in ((ety, f'εty = fy/Es = {ety:.5f}'), (0.005, '0.005')):
        s.line(ax.X(x), ax.Y(0.6), ax.X(x), ax.Y(0.93), '#90a4ae', 1.2, '4 4')
    s.text(ax.X(ety), ax.Y(0.6) + 36, f'εty = {ety:.5f}', 11.5, INK, 'middle', True)
    s.text(ax.X(0.005), ax.Y(0.6) + 36, '0.005', 11.5, INK, 'middle', True)
    s.text(ax.X(ety / 2), ax.Y(0.70), '壓力控制', 12.5, RED, 'middle', True)
    s.text(ax.X(0.0042), ax.Y(0.607), '過渡區（線性內插）', 12.5, ORG, 'middle', True)
    s.text(ax.X(0.006), ax.Y(0.607), '拉力控制', 12.5, GRN, 'middle', True)
    pts = [(ety, 0.65, PUR, '③ 平衡點：恰在轉角上，φ = 0.650', 'below'),
           (0.002473, phi_of(0.002473, 4200), ORG, 'RC-2011-3：εt = 0.002473 → 0.685', 'above'),
           (0.005, 0.90, '#e65100', 'RC-2015-1 ★：εt = 0.005 → 0.90', 'above')]
    for x, y, col, t, pos in pts:
        s.circ(ax.X(x), ax.Y(y), 6, col, '#fff', 1.5)
    label_box(s, ax.X(ety) - 4, ax.Y(0.65) + 6, [(pts[0][3], True)], PUR, anchor='end', size=11.5)
    label_box(s, ax.X(0.002473) + 10, ax.Y(0.685) - 6, [(pts[1][3], True)], ORG, size=11.5)
    label_box(s, ax.X(0.005) - 8, ax.Y(0.90) - 34, [(pts[2][3], True)], '#e65100', anchor='end', size=11.5)
    s.line(ax.X(0), ax.Y(0.655), ax.X(ety), ax.Y(0.655), '#9e9e9e', 1, '2 2')
    s.text(ax.X(0.0001), ax.Y(0.655) - 4, '舊式在此給 0.655（本庫不用）', 10.5, '#757575')
    s.line(90, 355, 122, 355, RED, 3.4)
    s.text(128, 359, '矩形箍筋柱 0.65 → 0.90', 12)
    s.line(330, 355, 362, 355, BLUE, 3, '9 5')
    s.text(368, 359, '螺旋柱 0.75 → 0.90', 12)
    s.text(530, 359, 'SD420；現行式', 11.5, MUT)
    return s.render()


# ════════════════════════════════════════════════════════════
# 圖 5-2  螺旋筋半環自由體：f_L = ρs·fyt / 2 的 2
# ════════════════════════════════════════════════════════════
def fig_fbd():
    s = Svg(760, 360)
    cx, cy, R = 200, 220, 150            # Dc = 68 cm → 300 px
    s.text(cx, 26, '平面：沿直徑切開的半圈螺旋筋', 13, INK, 'middle', True)
    s.path(f'M{cx-R},{cy} A{R},{R} 0 0 1 {cx+R},{cy}', BLUE, 6)
    s.path(f'M{cx-R+12},{cy} A{R-12},{R-12} 0 0 1 {cx+R-12},{cy} Z', 'none', 0, '#e8f5e9')
    s.line(cx - R - 20, cy, cx + R + 20, cy, '#90a4ae', 1.5, '6 4')
    s.text(cx + R + 24, cy + 4, '切面', 11, MUT)
    for i in range(1, 12):
        th = math.pi * i / 12
        x1, y1 = cx + (R - 46) * math.cos(th), cy - (R - 46) * math.sin(th)
        x2, y2 = cx + (R - 8) * math.cos(th), cy - (R - 8) * math.sin(th)
        s.line(x1, y1, x2, y2, GRN, 2.2, arrow=True)
    s.text(cx, cy - 64, 'fL（混凝土膨脹推螺筋）', 12, GRN, 'middle', True)
    for sx_ in (cx - R, cx + R):
        s.line(sx_, cy + 2, sx_, cy + 62, RED, 3.4, arrow=True)
        s.text(sx_, cy + 80, 'Asp·fyt', 12, RED, 'middle', True)
    s.line(cx - R, cy + 92, cx + R, cy + 92, INK, 1.2)
    for x_ in (cx - R, cx + R):
        s.line(x_, cy + 86, x_, cy + 98, INK, 1.2)
    s.text(cx, cy + 114, 'Dc = 68 cm（量到螺筋外緣，與 Ach 同一基準）', 11.5, INK, 'middle', True)
    # 立面
    ex = 470
    s.text(ex + 100, 26, '立面：一個螺距 s 內', 13, INK, 'middle', True)
    s.rect(ex, 60, 200, 200, '#e8f5e9', GRN, 1.5)
    for y in (60, 160, 260):
        s.line(ex - 6, y, ex + 206, y - 6, BLUE, 5)
    s.line(ex + 222, 60, ex + 222, 160, INK, 1.2)
    s.text(ex + 228, 114, 's', 13, INK, bold=True, italic=True)
    s.text(ex + 100, 290, '受側壓的投影面積 = Dc × s', 12, INK, 'middle', True)
    # 平衡式
    label_box(s, 440, 306, [('↑ 垂直平衡：fL·Dc·s = 2·Asp·fyt', True)], PUR, w=300, size=12.5)
    return s.render()


# ════════════════════════════════════════════════════════════
# 圖 5-3  應力–應變：無圍束 vs 圍束（RC-2010-1 參數）
# ════════════════════════════════════════════════════════════
def mander(eps, fcc, ecc, Ec):
    x = eps / ecc
    Esec = fcc / ecc
    r = Ec / (Ec - Esec)
    return fcc * x * r / (r - 1 + x ** r)


def fig_ss():
    fc, fyt, rho = 350, 4200, 0.00747
    fL = rho * fyt / 2
    fcc = fc + 4.1 * fL
    eco = 0.002
    ecc = eco * (1 + 5 * (fcc / fc - 1))
    Ec = 15000 * math.sqrt(fc)
    ecu_c = 0.004 + 1.4 * rho * fyt * 0.09 / fcc
    s = Svg(760, 390)
    ax = Axes(s, 70, 40, 600, 270, (0, 0.016), (0, 450))
    ax.frame([0, 0.002, 0.004, 0.006, 0.008, 0.010, 0.012, 0.014, 0.016], range(0, 451, 50), 'ε', "f (kgf/cm²)", xfmt='{:.3f}')
    # 無圍束：Mander 至 2εco，之後直線降至 εsp = 0.005（保護層剝落）
    xs = [i * 2 * eco / 200 for i in range(201)]
    u = [ax.P(x, mander(x, fc, eco, Ec)) for x in xs]
    f2 = mander(2 * eco, fc, eco, Ec)
    u.append(ax.P(0.005, 0))
    s.poly(u, RED, 3)
    xs = [i * ecu_c / 400 for i in range(401)]
    cpts = [ax.P(x, mander(x, fcc, ecc, Ec)) for x in xs]
    s.poly([ax.P(0, 0)] + cpts + [ax.P(ecu_c, 0)], GRN, 0, '#c8e6c9', close=True, op=0.55)
    s.poly([ax.P(0, 0)] + [ax.P(x, mander(x, fc, eco, Ec)) for x in [i * 2 * eco / 200 for i in range(201)]] + [ax.P(0.005, 0)], RED, 0, '#ffcdd2', close=True, op=0.8)
    s.poly(u, RED, 3)
    s.poly(cpts, GRN, 3.2)
    fend = mander(ecu_c, fcc, ecc, Ec)
    s.add(f'<path d="M{f(ax.X(ecu_c)-7)},{f(ax.Y(fend)-7)} l14,14 M{f(ax.X(ecu_c)+7)},{f(ax.Y(fend)-7)} l-14,14" stroke="{GRN}" stroke-width="2.5"/>')
    s.line(ax.X(0.003), ax.Y(0), ax.X(0.003), ax.Y(440), INK, 1.2, '5 4')
    s.text(ax.X(0.003) + 4, ax.Y(30), 'ACI εcu = 0.003', 11.5, INK, bold=True)
    s.circ(ax.X(ecc), ax.Y(fcc), 5, GRN, '#fff')
    label_box(s, ax.X(ecc) + 10, ax.Y(fcc) - 44, [(f"f′cc = f′c + 4.1fL = {fcc:.1f}", True), (f'fL = ρs·fyt/2 = {fL:.2f}', False)], GRN)
    s.circ(ax.X(eco), ax.Y(fc), 5, RED, '#fff')
    s.text(ax.X(eco) - 6, ax.Y(fc) - 10, "f′c = 350", 11.5, RED, 'end', True)
    s.text(ax.X(0.005) + 4, ax.Y(0) - 8, '蓋層剝落 ≈ 0.005', 11, RED)
    label_box(s, ax.X(ecu_c) - 4, ax.Y(fend) - 50, [(f'圍束 εcu ≈ {ecu_c:.4f}', True), ('0.004 + 1.4ρs·fyt·εsu / f′cc', False)], GRN, anchor='end')
    s.text(ax.X(0.0105), ax.Y(130), '曲線下面積 ＝ 消能能力', 12, GRN, 'middle', True)
    s.text(ax.X(0.0105), ax.Y(110), f'強度只 +{(fcc/fc-1)*100:.0f}%，可用應變 ×{ecu_c/0.003:.1f}', 11.5, GRN, 'middle')
    s.line(90, 368, 122, 368, RED, 3)
    s.text(128, 372, '無圍束 f′c = 350', 12)
    s.line(270, 368, 302, 368, GRN, 3.2)
    s.text(308, 372, f'圍束（RC-2010-1：#4@10，ρs = {rho}）', 12)
    s.text(575, 372, '曲線形狀：Mander (1988)', 11, MUT)
    return s.render()


# ════════════════════════════════════════════════════════════
# 圖 5-4  耐震箍筋：bc、Ach 都量到箍筋外緣（RC-2004-3）
# ════════════════════════════════════════════════════════════
def fig_ash():
    s = Svg(760, 440)
    k = 6.0                          # px/cm
    ox, oy = 60, 50
    B, cov, db_h, db_l = 50, 4.0, 1.27, 2.54
    s.text(ox + B * k / 2, 30, 'RC-2004-3：50×50，保護層 4 cm 量到箍筋外緣', 13, INK, 'middle', True)
    s.rect(ox, oy, B * k, B * k, '#eceff1', '#37474f', 2)
    s.rect(ox + cov * k, oy + cov * k, (B - 2 * cov) * k, (B - 2 * cov) * k, '#e3f2fd', 'none', 0, op=0.8)
    # 箍筋（外緣、中心線）
    o = cov * k
    s.rect(ox + o + db_h * k / 2, oy + o + db_h * k / 2, (B - 2 * cov - db_h) * k, (B - 2 * cov - db_h) * k, 'none', BLUE, db_h * k, 6)
    # 繫筋
    mid = ox + B * k / 2
    s.line(mid, oy + o + db_h * k, mid, oy + B * k - o - db_h * k, ORG, db_h * k)
    s.line(ox + o + db_h * k, oy + B * k / 2, ox + B * k - o - db_h * k, oy + B * k / 2, ORG, db_h * k)
    # 主筋
    inner = cov + db_h + db_l / 2
    pos = [inner, B / 2, B - inner]
    for x in pos:
        for y in pos:
            if (x, y) != (B / 2, B / 2):
                s.circ(ox + x * k, oy + y * k, db_l * k / 2, '#37474f')
    # 尺寸：bc 外緣
    y1 = oy + B * k + 26
    s.line(ox + o, y1, ox + B * k - o, y1, GRN, 1.6)
    for x in (ox + o, ox + B * k - o):
        s.line(x, oy + B * k - o, x, y1 + 6, GRN, 1, '3 2')
    s.text(ox + B * k / 2, y1 - 6, 'bc = 50 − 2×4 = 42 cm（外緣到外緣）✔', 12, GRN, 'middle', True)
    y2 = y1 + 34
    cl = (B - 2 * cov - db_h)
    s.line(ox + o + db_h * k / 2, y2, ox + B * k - o - db_h * k / 2, y2, '#9e9e9e', 1.4, '4 3')
    s.text(ox + B * k / 2, y2 - 6, f'中心距 {cl:.2f} cm —— 舊版 ACI 318-99 的 hc，不可混用 ✘', 11, '#757575', 'middle')
    # 右側說明
    rx = 400
    label_box(s, rx, 60, [('Ach = bc² = 42² = 1764 cm²', True), ('Ag / Ach = 2500 / 1764 = 1.417', False)], BLUE, w=330, size=12.5)
    label_box(s, rx, 130, [('每方向肢數 = 外箍 2 肢 + 繫筋 1 肢 = 3', True), ('Ash = 3 × 1.29 = 3.87 cm²（D13）', False)], ORG, w=330, size=12.5)
    label_box(s, rx, 200, [('式一：s ≤ Ash·fyt / [0.3·bc·f′c(Ag/Ach − 1)] = 7.36', True),
                           ('式二：s ≤ Ash·fyt / (0.09·bc·f′c) = 10.24', False),
                           ('取小 → 7.36 → 無條件捨去 s = 7 cm', True)], PUR, w=340, size=12)
    label_box(s, rx, 290, [('式一較嚴的門檻：Ag/Ach > 1.3', True), ('（保護層 4 cm 時方柱邊長 < 約 65 cm）', False)], MUT, w=330, size=12)
    # 標示被切的肢
    s.line(ox - 20, oy + B * k * 0.3, ox + B * k + 20, oy + B * k * 0.3, RED, 1.4, '6 4')
    s.text(ox - 24, oy + B * k * 0.3 + 4, '切面', 11, RED, 'end', True)
    for x in (ox + o + db_h * k / 2, mid, ox + B * k - o - db_h * k / 2):
        s.circ(x, oy + B * k * 0.3, 5, '#fff', RED, 2)
    return s.render()


# ════════════════════════════════════════════════════════════
# 圖 6-2  δns 對 Pu/(0.75Pc)：正回饋的發散
# ════════════════════════════════════════════════════════════
def fig_delta():
    s = Svg(760, 390)
    ax = Axes(s, 70, 40, 560, 270, (0, 1.0), (0, 5))
    s.rect(ax.X(0.2), ax.Y(5), ax.X(0.6) - ax.X(0.2), ax.h, '#e8f5e9', 'none', 0, op=0.6)
    ax.frame([0, 0.2, 0.4, 0.6, 0.8, 1.0], range(0, 6), 'Pu / (0.75 Pc)', 'δns', xfmt='{:.1f}')
    for cm, col, dash, lab in ((1.0, BLUE, None, 'Cm = 1.0（均勻彎矩／橫向載重）'), (0.822, RED, '9 5', 'Cm = 0.822（RC-2006-2）')):
        xs = [i / 1000 for i in range(0, 900)]
        pts = [ax.P(x, max(1.0, cm / (1 - x))) for x in xs if cm / (1 - x) <= 5]
        s.poly(pts, col, 3, dash=dash)
        raw = [ax.P(x, cm / (1 - x)) for x in xs if x < 1 - cm]
        if raw:
            s.poly(raw, col, 1.2, dash='2 3')
    s.line(ax.X(1), ax.Y(0), ax.X(1), ax.Y(5), INK, 1.4, '6 4')
    s.text(ax.X(1) - 6, ax.Y(4.7), 'Pu = 0.75Pc：挫屈（δ → ∞）', 12, INK, 'end', True)
    s.line(ax.X(0), ax.Y(1), ax.X(1), ax.Y(1), '#9e9e9e', 1, '3 3')
    s.text(ax.X(0.62), ax.Y(1) + 18, 'δns ≥ 1.0 下限（細點線＝未截平的 Cm/(1−x)）', 11, '#616161')
    x0, d0 = 400 / (0.75 * 1362), 0.822 / (1 - 400 / (0.75 * 1362))
    s.circ(ax.X(x0), ax.Y(d0), 6.5, '#e65100', '#fff', 1.6)
    s.line(ax.X(x0), ax.Y(d0), ax.X(x0), ax.Y(0), '#e65100', 1, '3 3')
    s.line(ax.X(x0), ax.Y(d0), ax.X(x0) - 30, ax.Y(d0) - 38, '#e65100', 1)
    label_box(s, ax.X(x0) - 12, ax.Y(d0) - 70, [(f'RC-2006-2：{x0:.3f} → δns = {d0:.3f}', True), ('Mc = 1.351 × 27 = 36.5 tf·m', False)], '#e65100', anchor='end')
    s.text(ax.X(0.4), ax.Y(4.75), '常見健康範圍 0.2–0.6', 11.5, GRN, 'middle', True)
    s.line(90, 368, 122, 368, BLUE, 3)
    s.text(128, 372, 'Cm = 1.0', 12)
    s.line(230, 368, 262, 368, RED, 3, '9 5')
    s.text(268, 372, 'Cm = 0.822（RC-2006-2）', 12)
    s.text(470, 372, '超過 0.8 曲線急升：斷面明顯不足', 11.5, MUT)
    return s.render()


FIGS = dict(pm=fig_pm, fan=fig_fan, exa=fig_ex_a, mc=fig_mc, phi=fig_phi,
            fbd=fig_fbd, ss=fig_ss, ash=fig_ash, delta=fig_delta)

if __name__ == '__main__':
    out = {k: v() for k, v in FIGS.items()}
    json.dump(out, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False)
    # 每張另存一份獨立 svg 方便預覽
    d = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'svg')
    os.makedirs(d, exist_ok=True)
    for k, v in out.items():
        open(os.path.join(d, k + '.svg'), 'w', encoding='utf-8').write(v)
    print('ok', list(out))
