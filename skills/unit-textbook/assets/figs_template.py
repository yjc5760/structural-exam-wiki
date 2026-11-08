# -*- coding: utf-8 -*-
"""第 N 章的向量圖。規則：所有座標、曲線、標註數字都由程式或 calcs.py 算出，不手描。"""
from plot import *  # noqa  （lib.py 的 T/L/A/P/R/C/dim/pin/fixed_wall/svg、plot.py 的 Plot/box/badge 與色票）
from calcs import *  # noqa
import math


def figN_1():
    W, H = 900, 400                          # 寬固定 900；高依內容
    pl = Plot(90, 50, 600, 290, 0, 10, 0, 1.2)  # x0, y0, w, h, xmin, xmax, ymin, ymax
    o = pl.axes([0, 2, 4, 6, 8, 10], [0, 0.5, 1.0], '*x*（單位）', '*y*（單位）')
    o += pl.curve(lambda x: 1 - math.exp(-x / 3), 0, 10, COMP, 3.2)       # 曲線逐點計算
    o += pl.dot(3, 1 - math.exp(-1), KEY, 6)
    o += T(pl.X(3) + 10, pl.Y(0.63) - 10, '標註：*x* = 3 時 0.63', 15, KEY, 'start', 'bold')
    # 右側說明框（字 ≥ 14px；中文字寬約 = 字級，先估寬度再放）
    o += R(710, 80, 180, 120, KEY2, KEY, 1.4, 8)
    o += T(800, 106, '一句結論', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '圖的替代文字')


ALL = {'figN_1': figN_1}
