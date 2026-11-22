# -*- coding: utf-8 -*-
"""第 9 章：最優設計。"""
from figs_ps import *  # noqa
from calcs import rc2015_4

Q = rc2015_4()


def fig9_1():
    W, H = 900, 360
    o = T(450, 26, 'RC-2015-4：四條同時達限（*f*_{ca} = 140、*f*_{ta} = 0），跨中兩個時刻的應力圖', 16, INK, 'middle', 'bold')
    F, Ar, S, e, MD, ML = Q['F'], Q['A'], Q['S'], Q['e'], Q['MD'], Q['ML']
    t1 = F / Ar - F * e / S + MD / S; b1 = F / Ar + F * e / S - MD / S
    t2 = t1 + ML / S; b2 = b1 - ML / S
    hp, y0, k = 160, 80, 0.75
    for xa, t, b, lab in ((250, t1, b1, '傳遞（*F*＋*M*_{D}）'), (650, t2, b2, '使用（*F*＋*M*_{D}＋*M*_{L}）')):
        o += sblock(xa, y0, hp, round(t, 6), round(b, 6), k)
        o += T(xa, y0 + hp + 48, lab, 15, INK, 'middle', 'bold')
    o += A(400, y0 + hp / 2, 500, y0 + hp / 2, KEY, 2.4, 12)
    o += T(450, y0 + hp / 2 - 12, '加 *M*_{L}', 15, KEY, 'middle', 'bold')
    o += T(450, 330, f"上緣 0 → 140、下緣 140 → 0：活載把應力整個「翻」過來，*M*_{{L}}/*S* = 140 + 0 = 140", 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '最優設計')


ALL = {'fig9_1': fig9_1}
