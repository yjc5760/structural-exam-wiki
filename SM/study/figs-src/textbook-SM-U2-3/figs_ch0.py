# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、先數橫桿。"""
from plot import *  # noqa
from figkit import seed_tree
from calcs import *  # noqa


def fig0_1():
    seeds = [
        ('S1 Rankine 相切', '主動／被動', TEN, ['*K*_{a}=tan²(45°−*φ*/2)', '*K*_{p}=1/*K*_{a}', '黏土 *σ*_{v}∓2*c*_{u}', '淨被動 4*c*_{u}−*γH*']),
        ('S2 水的 *K*=1', '水土分開', AC, ['*K*_{a}*γ*′*z*+*γ*_{w}*z*_{w}', '淨水壓', '滲流 *γ*′±*iγ*_{w}', '黏土用總應力']),
        ('S3 牆是剛體', 'Σ*M*=Σ*F*=0', WARN, ['懸臂：零淨壓力點', '自由端：對地錨取矩', 'Blum 反曲點', '鉸接法、*S*=*M*/*σ*']),
        ('S4 倒過來的基礎', '*N*_{c}=*π*+2', COMP, ['*FS*=*N*_{c}*S*_{u}/(*γH*+*q*)', 'Bjerrum–Eide 3D', '圓弧力矩法', '*N*_{s}=*γH*/*c*_{u}']),
        ('S5 水的三種攻擊', '頂、沖、推', AC, ['上舉 *γ*_{t}*t*/*γ*_{w}*h*_{w}', '*i*_{cr}=*γ*′/*γ*_{w}', '最短流徑 *L*', 'Peck 砂 0.65']),
        ('S6 天平', '抵抗÷驅動', KEY, ['反算降水位', '反算開挖深度', '反算改良強度', '先降驅動再升抵抗']),
    ]
    return seed_tree(seeds, title='六顆種子與它們長出的公式')


def _wall_icon(x, y, n, title, ch, c):
    o = R(x, y, 250, 210, '#fff', c, 1.8, 12)
    o += T(x + 125, y + 26, title, 16, c, 'middle', 'bold')
    gx = x + 30
    o += R(gx, y + 70, 100, 110, '#efe6d8', None, 0) + R(gx + 100, y + 140, 90, 40, '#efe6d8', None, 0)
    o += L(gx, y + 70, gx + 100, y + 70, INK, 1.6) + L(gx + 100, y + 140, gx + 190, y + 140, INK, 1.6)
    o += L(gx + 100, y + 55, gx + 100, y + 180, INK, 4)
    for k in range(n):
        yy = y + 85 + k * 20
        o += L(gx + 100, yy, gx + 190, yy, WARN, 3)
    o += T(x + 125, y + 200, ch, 15, INK, 'middle', 'bold')
    return o


def fig0_2():
    W, H = 900, 300
    o = _wall_icon(20, 30, 0, '0 根：懸臂', '第 2 章', TEN)
    o += _wall_icon(320, 30, 1, '1 根：錨定', '第 3 章', WARN)
    o += _wall_icon(620, 30, 3, '多根：支撐', '第 4 章 Peck', COMP)
    o += T(450, 280, '坑底：黏土 → 第 5 章隆起；水位／受壓層 → 第 6 章砂湧、上舉', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '先數橫桿')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2}
