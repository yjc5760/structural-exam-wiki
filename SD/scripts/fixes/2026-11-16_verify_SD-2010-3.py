#!/usr/bin/env python3
"""SD-2010-3 勘誤驗算（2026-11-16，X-G1 階段 C）
題意：題目正本判讀 #1（縱向）、#2（第 1、3 墩雙滾，第 2、4 墩雙鉸）、#7（柱高 L）、#10（橋梁延續）。
路徑 1：符號推導（規範式 β、γ）；路徑 2：FE 懸臂墩勁度＋集中質量特徵值；另算舊模型與橫向讀法作對照。"""
import numpy as np, sympy as sp
m, g, L, EI = sp.symbols("m g L EI", positive=True)
mis = []
def chk(name, got, ref, tol=1e-9):
    ok = abs(float(got) - float(ref)) <= tol * max(1.0, abs(float(ref)))
    print(f"{name:40s} {float(got):.6f}  ref {float(ref):.6f}  {'OK' if ok else 'MISMATCH'}")
    if not ok: mis.append(name)
# 路徑 1：振動單元＝1 支雙鉸墩＋其上兩跨（各一端鉸接在此墩），縱向剛體平移
k = 3*EI/L**3                      # 懸臂墩（底固定、頂經鉸支承、不受轉動束制）
W = m*g*2*L                        # 兩跨上構重量沿縱向施加
U0 = sp.simplify(W/k)              # = 2 m g L^4 / (3 EI)
beta = m*g*U0*2*L; gamma = m*g*U0**2*2*L
T = sp.simplify(2*sp.pi*sp.sqrt(gamma/(beta*g)))
coef = sp.simplify(T/(L**2*sp.sqrt(m/EI)))
print("U0 =", U0, "  T =", T)
chk("U0 / (m g L^4/EI)", sp.simplify(U0/(m*g*L**4/EI)), sp.Rational(2,3))
chk("T 係數 (×L²√(m/EI))", coef, 2*np.pi*np.sqrt(2/3))
chk("T 係數 = 5.130", round(float(coef),3), 5.130)
# 路徑 2：FE 懸臂墩（Euler–Bernoulli，20 元素）頂端勁度＋2mL 集中質量
def cant_k(n=20, EIv=1.0, Lv=1.0):
    le = Lv/n; K = np.zeros((2*n+2, 2*n+2))
    ke = EIv/le**3*np.array([[12,6*le,-12,6*le],[6*le,4*le**2,-6*le,2*le**2],[-12,-6*le,12,-6*le],[6*le,2*le**2,-6*le,4*le**2]])
    for e in range(n): K[2*e:2*e+4, 2*e:2*e+4] += ke
    Kf = K[2:, 2:]; F = np.zeros(len(Kf)); F[-2] = 1.0
    return 1.0/np.linalg.solve(Kf, F)[-2]
kfe = cant_k(); chk("FE 懸臂頂勁度 /(EI/L³)", kfe, 3.0, 1e-6)
chk("FE 特徵值週期係數", 2*np.pi*np.sqrt(2.0/kfe), 2*np.pi*np.sqrt(2/3), 1e-6)
# 對照：舊模型（全橋 3L、4 墩並聯）與橫向讀法（每墩分擔 mL）
old = 2*np.pi*np.sqrt(3/(4*3)); trans = 2*np.pi*np.sqrt(1/3)
chk("舊解係數 π", old, np.pi); chk("橫向讀法係數", trans, 3.6276, 1e-4)
chk("新/舊 比", float(coef)/old, 1.633, 1e-3)
chk("U0 / (U0 舊 = mgL⁴/4EI)", (2/3)/(1/4), 8/3)
print("MISMATCHES:", len(mis), mis if mis else "")
