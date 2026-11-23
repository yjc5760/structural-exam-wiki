# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、全書地圖。"""
from plot import *  # noqa
from calcs import *  # noqa


def seed_tree(seeds, W=900, title=''):
    """seeds: [(代號, 種子短句, 顏色, [長出的公式...]), ...]；兩欄排列。"""
    n = len(seeds)
    cols = 2
    rows = (n + 1) // 2
    rowh = 150
    H = 70 + rows * rowh + 10
    o = T(W / 2, 32, title, 18, KEY, 'middle', 'bold') if title else ''
    for i, (code, txt, c, kids) in enumerate(seeds):
        cx = 30 + (i % cols) * 440
        cy = 60 + (i // cols) * rowh
        o += R(cx, cy, 160, 58, KEY2, KEY, 2, 12)
        o += T(cx + 80, cy + 24, code, 16, KEY, 'middle', 'bold')
        o += T(cx + 80, cy + 47, txt, 14, INK, 'middle')
        for j, k in enumerate(kids[:4]):
            ky = cy - 8 + j * 34
            o += L(cx + 160, cy + 29, cx + 200, ky + 14, c, 1.6)
            o += R(cx + 200, ky, 220, 28, '#fff', c, 1.3, 7)
            o += T(cx + 310, ky + 20, k, 14, c, 'middle')
    return svg(W, H, o, title or '種子家族樹')


def fig0_1():
    seeds = [
        ('S1 土粒不變', '變的只有孔隙', AC, ['*γ*_{d}=*γ*_{t}/(1+*w*)', '*Se*=*wG*_{s}', '*D*_{r}、土方守恆', 'Δ*H*=Δ*e H*/(1+*e*_{0})']),
        ('S3 兩條直線', '*e*–log*σ*′ 折點 *p*_{c}′', KEY, ['沉陷三式', 'OCR 選 *C*_{c} 或 *C*_{s}', 'Casagrande 求 *p*_{c}′', '*m*_{v}=*a*_{v}/(1+*e*_{0})']),
        ('S2 有效應力', '*σ*′=*σ*−*u*', TEN, ['*p*_{0}′（水位下用 *γ*′）', '水位升降 Δ*σ*′', '滲流時的 *u*', '代表點取層中點']),
        ('S4 力會擴散', '2:1 錐體', WARN, ['Δ*p*=*Q*/(*B*+*z*)(*L*+*z*)', '層平均 Δ*p*（積分）', '*z* 從基礎底面量', '頂、中、底差數倍']),
        ('S6 水先潤滑後佔位', '夯實曲線', COMP, ['*γ*_{zav}=*G*_{s}*γ*_{w}/(1+*wG*_{s})', 'OMC 與能量', '乾側／濕側特性', 'R.C.、CBR 反推']),
        ('S5 路徑平方', '*t*∝*H*_{dr}^{2}/*c*_{v}', WARN, ['*T*_{v}=*c*_{v}*t*/*H*_{dr}^{2}', '單面 *H*、雙面 *H*/2', '*U*=*S*_{t}/*S*_{∞}、比例法', '兩段式 0.933、0.085']),
    ]
    return seed_tree(seeds, title='六顆種子與它們長出的公式')


def fig0_2():
    W, H = 900, 470
    o = ''
    x0, x1 = 60, 560
    # 土層
    layers = [(70, 150, '#fff8e1', '砂（水位以上用 *γ*_{d}）'), (150, 230, '#e3f2fd', '砂（水位下用 *γ*′）'),
              (230, 390, '#ede7f6', '黏土 *H*（*C*_{c}、*C*_{s}、*e*_{0}、*c*_{v}）'), (390, 420, '#eceff1', '砂或不透水層？')]
    for ya, yb, fc, name in layers:
        o += R(x0, ya, x1 - x0, yb - ya, fc, MUT, 1)
        o += T(x0 + 12, ya + 22, name, 14, INK)
    o += L(x0, 150, x1, 150, AC, 2.2, '8 5') + T(x1 - 10, 144, '▽ 地下水位', 14, AC, 'end')
    # 基礎與 2:1
    o += R(260, 52, 100, 18, STEEL3, INK, 1.4) + A(310, 20, 310, 50, COMP, 2.6, 12) + T(320, 34, '*Q*', 16, COMP, 'start', 'bold')
    o += P([(260, 70), (210, 310), (410, 310), (360, 70)], WARN, 1.6, dash='6 4')
    o += L(x0, 310, x1, 310, KEY, 1.4, '3 3') + C(310, 310, 6, KEY, '#fff', 1.6) + T(322, 304, '中點', 14, KEY, 'start', 'bold')
    # 右側章節標籤
    tags = [(110, '第 1–2 章', '三相：*γ*_{d}、*γ*_{sat}、*γ*′ 怎麼來', AC),
            (190, '第 3 章', '*p*_{0}′＝骨架扛多少；2:1 求 Δ*p*', TEN),
            (270, '第 4 章', '*p*_{c}′、OCR：走 *C*_{s} 還是 *C*_{c}', KEY),
            (330, '第 5 章', '沉陷三式 → *S*_{c}', KEY),
            (405, '第 6 章', '上下透水？*H*_{dr} → *T*_{v} → *t*', WARN)]
    for y, ch, txt, c in tags:
        o += L(x1 + 4, y, x1 + 30, y, c, 1.4) + R(x1 + 30, y - 22, 300, 44, '#fff', c, 1.4, 8)
        o += T(x1 + 42, y - 3, ch, 14, c, 'start', 'bold') + T(x1 + 42, y + 16, txt, 14, INK)
    return svg(W, H, o, '全書地圖：剖面上每一步在哪一章')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2}
