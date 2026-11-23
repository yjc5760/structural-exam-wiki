# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、自由體圖地圖。"""
from plot import *  # noqa
from figkit import seed_tree
from calcs import *  # noqa


def fig0_1():
    seeds = [
        ('S1 Rankine 相切', '主動圓', TEN, ['*K*_{a}=tan²(45°−*φ*/2)', '傾斜填土：平行地表', '*K*_{a}*σ*_{v}−2*c*√*K*_{a}', '*z*_{c}、超載 *K*_{a}*q*']),
        ('S2 Coulomb 楔體', '三力閉合', WARN, ['*K*_{a} 的來源', 'β、α、δ 量自哪', 'M-O：重力轉 *θ*′', 'Δ*P*_{ae} 在 0.6*H*']),
        ('S3 牆是剛體', 'Σ*F*、Σ*M*', AC, ['分塊 *W*_{i}、*x*_{i}', '*P*_{av} 進 Σ*M*_{R}', '虛擬牆背', 'Σ*V*、Σ*M*_{O}']),
        ('S4 摩擦塊', '底面抗滑', COMP, ['Σ*V*tan*δ*+*c*_{a}*B*+*P*_{p}', '*δ*=(2/3～1)*φ*', '*φ*=0：*S*_{u}*B*', '剪力榫']),
        ('S5 梯形底壓', '中間三分之一', WARN, ['*e*=*B*/2−*x̄*', '*q*=Σ*V*/*B*(1±6*e*/*B*)', '*B*′=*B*−2*e*', '傾斜因數']),
        ('S6 加勁', '摩擦綁成牆', KEY, ['拉斷 *T*_{ult}', '拔出 2*L*_{e}*σ*′tan*φ*', '外穩定＝重力牆', '整體滑動']),
    ]
    return seed_tree(seeds, title='六顆種子與它們長出的公式')


def fig0_2():
    W, H = 900, 430
    o = ''
    x0, yb = 200, 340
    s = 30
    poly = [(x0, yb), (x0 + 5 * s, yb), (x0 + 3 * s, yb - 8 * s * 0.95), (x0, yb - 8 * s * 0.95)]
    o += P(poly, INK, 2, fill=STEEL2, close=True)
    o += hatch_ground(x0 - 60, yb, 5 * s + 140)
    # 土壓
    o += A(x0 + 5 * s + 140, yb - 90, x0 + 4.3 * s + 4, yb - 80 + 18, TEN, 3, 13)
    o += T(x0 + 5 * s + 145, yb - 92, '*P*_{a}（第 1、2 章）', 15, TEN, 'start', 'bold')
    # 牆重
    o += A(x0 + 2 * s, yb - 140, x0 + 2 * s, yb - 60, AC, 3, 12) + T(x0 + 2 * s + 8, yb - 120, '*W*（第 3 章）', 15, AC, 'start', 'bold')
    # 底面
    o += A(x0 + 5 * s, yb + 22, x0 - 10, yb + 22, COMP, 2.6, 11) + T(x0 - 14, yb + 28, '滑動（第 4 章）', 15, COMP, 'end', 'bold')
    o += C(x0, yb, 7, KEY, '#fff', 2) + T(x0 - 12, yb - 10, '牆趾：傾覆（第 4 章）', 15, KEY, 'end', 'bold')
    qx = [x0 + i * 5 * s / 10 for i in range(11)]
    o += P([(x0, yb + 50 + 60)] + [(x, yb + 50 + 60 - 50 * (1 - i / 10) - 6) for i, x in enumerate(qx)] + [(x0 + 5 * s, yb + 50 + 60)], WARN, 2, fill=WARN2, close=True)
    o += T(x0 + 5 * s + 10, yb + 100, '底壓、偏心、承載（第 5 章）', 15, WARN, 'start', 'bold')
    o += box(620, 40, 265, 140, '一張自由體圖、三種讀法', ['水平：滑動', '力矩：傾覆', '垂直分布：承載'], KEY2, KEY)
    return svg(W, H + 30, o, '自由體圖地圖')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2}
