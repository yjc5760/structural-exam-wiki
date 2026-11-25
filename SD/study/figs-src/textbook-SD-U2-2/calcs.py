# -*- coding: utf-8 -*-
"""SD-U2-2 建築耐震設計規範：教科書講義的所有數值。
規範依據：建築物耐震設計規範及解說（內政部 111 年版）。單位依考題（kN、tf、m、s）。
"""
import math
import numpy as np

PI = math.pi

# ---------- 第 1 章：回歸期與超越機率 ----------
def TR_from(P50, n=50):
    Pa = 1 - (1 - P50) ** (1 / n)
    return 1 / Pa


def P_from(TR, n=50):
    return 1 - (1 - 1 / TR) ** n


LEVELS = {'中小度地震': 0.80, '設計地震': 0.10, '最大考量地震': 0.02}
TRS = {k: TR_from(v) for k, v in LEVELS.items()}
TR_APPROX = {k: 50 / v for k, v in LEVELS.items()}          # 小機率近似 50/P
TR_POISSON = {k: -50 / math.log(1 - v) for k, v in LEVELS.items()}


# ---------- 第 2 章：工址設計譜（示範值） ----------
SITE = dict(SDS=0.8, SD1=0.45)
SITE['T0'] = SITE['SD1'] / SITE['SDS']


def SaD(T, SDS=SITE['SDS'], SD1=SITE['SD1']):
    T0 = SD1 / SDS
    if T <= 0.2 * T0:
        return SDS * (0.4 + 3 * T / T0)
    if T <= T0:
        return SDS
    if T <= 2.5 * T0:
        return SD1 / T
    return 0.4 * SDS


# ---------- 第 3 章：Ra、Fu、(·)m ----------
def Ra(R, basin=False):
    return 1 + (R - 1) / (2.0 if basin else 1.5)


def Fu(T, T0, ra):
    s = math.sqrt(2 * ra - 1)
    if T >= T0:
        return ra
    if T >= 0.6 * T0:
        return s + (ra - s) * (T - 0.6 * T0) / (0.4 * T0)
    if T >= 0.2 * T0:
        return s
    return s + (s - 1) * (T - 0.2 * T0) / (0.2 * T0)


def mod(x):
    if x <= 0.3:
        return x
    if x < 0.8:
        return 0.52 * x + 0.144
    return 0.70 * x


RA_TAB = {R: dict(Ra=Ra(R), sq=math.sqrt(2 * Ra(R) - 1), VstarV=Ra(R) / 3) for R in (1.0, 2.0, 3.2, 4.0, 4.8)}

# ---------- 第 4 章：V、V*、VM ----------
# V*/V = Fu/3（一般工址）、Fu/2.5（臺北盆地）
VSTAR = {R: dict(general=Ra(R) / 3, basin=Ra(R, True) / 2.5) for R in (2.0, 3.2, 4.0, 4.8)}

# ---------- 第 5 章：豎向分配 ----------
def Ft(T, V):
    if T <= 0.7:
        return 0.0
    return min(0.07 * T * V, 0.25 * V)


def distribute(w, h, V, T):
    ft = Ft(T, V)
    wh = [a * b for a, b in zip(w, h)]
    s = sum(wh)
    F = [(V - ft) * x / s for x in wh]
    F[-1] += ft
    Vs = [sum(F[i:]) for i in range(len(F))]
    M0 = sum(f_ * hh for f_, hh in zip(F, h))
    return dict(Ft=ft, F=F, Vs=Vs, M0=M0, sum_wh=s)


# SD-2025-1：8 層、每層 20 kN、層高 3.5 m、T = 0.8 s、I = 1.25、SaD = 0.6、Fu = 2、αy = 1.4
Q2025 = dict(I=1.25, SaD=0.6, Fu=2.0, ay=1.4, W=160.0, T=0.8)
Q2025['ratio'] = Q2025['SaD'] / Q2025['Fu']                         # 0.30 → (·)m 不修正
Q2025['V'] = Q2025['I'] / (1.4 * Q2025['ay']) * mod(Q2025['ratio']) * Q2025['W']
Q2025.update(distribute([20.0] * 8, [3.5 * (i + 1) for i in range(8)], Q2025['V'], Q2025['T']))
Q2025['h_eq'] = Q2025['M0'] / Q2025['V']

# SD-2005-3：12 層 RC，V = 450 t；一樓 4 m、其餘 3.2 m；2F 400 t、3F~12F 300 t、屋頂 200 t
H05 = [4.0 + 3.2 * i for i in range(12)]                 # 2F … 屋頂（R）
W05 = [400.0] + [300.0] * 10 + [200.0]
Q2005 = dict(hn=H05[-1])
Q2005['T'] = 0.070 * Q2005['hn'] ** 0.75
Q2005.update(distribute(W05, H05, 450.0, Q2005['T']))

# 經驗週期
CT = {'鋼構架': 0.085, 'RC 構架、偏心斜撐': 0.070, '其他': 0.050}

# ---------- 第 6 章：扭轉放大 ----------
def Ax(dmax, davg):
    return min(max((dmax / (1.2 * davg)) ** 2, 1.0), 3.0)


AX_EX = dict(d1=1.0, d2=1.8)
AX_EX['avg'] = (AX_EX['d1'] + AX_EX['d2']) / 2
AX_EX['ratio'] = AX_EX['d2'] / AX_EX['avg']
AX_EX['Ax'] = Ax(AX_EX['d2'], AX_EX['avg'])


if __name__ == '__main__':
    print('TR', TRS, TR_APPROX, TR_POISSON)
    print('SITE', SITE, [round(SaD(t), 3) for t in (0, 0.1, 0.5, 1, 1.5, 2)])
    print('RA_TAB', RA_TAB); print('VSTAR', VSTAR)
    print('2025', {k: (round(v, 4) if isinstance(v, float) else [round(x, 3) for x in v] if isinstance(v, list) else v) for k, v in Q2025.items()})
    print('2005', {k: (round(v, 4) if isinstance(v, float) else [round(x, 2) for x in v] if isinstance(v, list) else v) for k, v in Q2005.items()})
    print('AX', AX_EX)
