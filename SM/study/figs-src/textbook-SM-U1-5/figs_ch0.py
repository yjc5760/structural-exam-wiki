# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、莫爾圖地圖。"""
from plot import *  # noqa
from figkit import seed_tree
from calcs import *  # noqa


def fig0_1():
    seeds = [
        ('S1 有效應力', '*σ*′=*σ*−*u*', TEN, ['UU／CU／CD 選型', '總應力圓 vs 有效圓', '*i*_{cr}=*γ*′/*γ*_{w}', '取樣擾動']),
        ('S4 相切＝破壞', '直角三角形', KEY, ['主應力式', 'sin*φ*′ 捷徑', '*θ*_{f}=45°+*φ*/2', '破壞面 *σ*_{ff}、*τ*_{ff}']),
        ('S2 莫爾圓', '圓心、半徑、2*θ*', COMP, ['任意面 *σ*_{n}、*τ*', '極點法', '*S*_{u}=(*σ*_{1}−*σ*_{3})_{f}/2', '最大剪應力面 45°']),
        ('S5 水擠不出去', '彈簧＋水', AC, ['Δ*u*=*B*[Δ*σ*_{3}+*A*Δ*q*]', '*B*=1 ⇒ *φ*_{u}=0', '*A*_{f}=Δ*u*_{f}/Δ*q*_{f}', '由 *φ*′ 推 *S*_{u}']),
        ('S3 摩擦塊', '*τ*=*c*+*σ*tan*φ*', WARN, ['莫爾–庫倫', '*φ*_{u}=0：*τ*=*c*_{u}', '*c*′=0（NC 黏土）', '名詞解釋']),
        ('S6 應力路徑', '圓頂的軌跡', TEN, ['*p*=(*σ*_{1}+*σ*_{3})/2', '*K*_{f}：tan*α*=sin*φ*', '*K*_{0} 起點', 'AC／LE']),
    ]
    return seed_tree(seeds, title='六顆種子與它們長出的公式')


def fig0_2():
    W, H = 900, 430
    pl = Plot(80, 50, 560, 300, 0, 240, 0, 120)
    X, Y = pl.X, pl.Y
    o = A(X(0), Y(0), X(240) + 16, Y(0), INK, 1.5) + A(X(0), Y(0), X(0), Y(120) - 14, INK, 1.5)
    o += T(X(240) + 20, Y(0) + 5, '*σ*', 16, INK) + T(X(0), Y(120) - 22, '*τ*', 16, INK, 'middle')
    phi, c = 28.0, 10.0
    o += L(X(0), Y(c), X(240), Y(c + 240 * tan(phi)), WARN, 2.4)
    # 有效圓相切
    s3e = 40.0
    s1e = s1_fail(s3e, phi, c)
    Ce, Re = (s1e + s3e) / 2, (s1e - s3e) / 2
    uf = 60.0

    def circ(Cc, R, col, w=2.6, dash=None):
        pts = [(X(Cc + R * math.cos(t)), Y(R * math.sin(t))) for t in [i * math.pi / 120 for i in range(121)]]
        return P(pts, col, w, dash=dash)
    o += circ(Ce, Re, TEN, 3) + circ(Ce + uf, Re, COMP, 2.6, '7 4')
    tx = Ce - Re * sin(phi)
    ty = Re * cos(phi)
    o += L(X(Ce), Y(0), X(tx), Y(ty), KEY, 2) + C(X(tx), Y(ty), 6, KEY, '#fff', 1.8)
    o += A(X(Ce), Y(-6) + 0, X(Ce + uf), Y(-6) + 0, AC, 1.8, 9, both=True)
    o += T(X(Ce + uf / 2), Y(0) + 34, '*u*_{f}（第 1、4 章）', 14, AC, 'middle', 'bold')
    o += T(X(Ce), Y(Re * 0.35), '有效應力圓（第 2 章）', 14, TEN, 'middle', 'bold')
    o += T(X(Ce + uf + Re * 0.75), Y(Re * 0.75) + 10, '總應力圓', 14, COMP, 'start', 'bold')
    o += T(X(200), Y(c + 200 * tan(phi)) - 12, '包絡線（第 3 章）', 14, WARN, 'end', 'bold')
    o += T(X(tx) - 10, Y(ty) - 12, '切點＝破壞面（第 3 章）', 14, KEY, 'end', 'bold')
    o += C(X(Ce), Y(Re), 5, TEN, '#fff', 1.6)
    o += A(X(Ce) + 4, Y(Re) - 4, X(Ce) + 40, Y(Re) - 40, TEN, 1.6, 8)
    o += T(X(Ce) + 44, Y(Re) - 44, '圓頂 (*p*, *q*)：第 5 章', 14, TEN, 'start', 'bold')
    o += box(670, 70, 215, 140, '一張圖讀全單元', ['圓：一點的應力', '線：材料的強度', '相切：破壞', '平移 *u*：總↔有效'], KEY2, KEY)
    return svg(W, H, o, '莫爾圖全書地圖')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2}
