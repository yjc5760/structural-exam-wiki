#!/usr/bin/env python3
"""SD-2003-4 勘誤驗算（2026-11-16，FIX-SD-U1-2-G1）
題意依題目正本 SD-2003-4-problem.md（已確認）：u1＝C 點沿 DC 平移、u2＝B 點沿 CB 平移、u3＝A 點沿 DA 平移；
柱兩端固接 k_i＝12EI_i/h^3；剛性方板質量 m 均勻；地震沿 D→B。
三條路徑：(1) 應變能／動能對自由度二次微分；(2) 質心 x、y、θ 矩陣以座標轉換 T^T K_c T；(3) 單位位移＝繞 D 剛體轉動的力平衡。
最後與解析正本寫入的值比對，印出 MISMATCHES。"""
import sympy as sp
a, m, EI, h = sp.symbols("a m EI h", positive=True)
k = 12*EI/h**3
u1, u2, u3 = sp.symbols("u1 u2 u3")
U = [u1, u2, u3]
# 平面座標：原點樓版中心，x 沿 DC，y 沿 DA；θ 逆時針
th = (u2 - u3)/a; uy = (u2 + u3)/2; ux = u1 - th*a/2
cols = {"D": (-a/2, -a/2, 2*k), "A": (-a/2, a/2, 2*k), "B": (a/2, a/2, k), "C": (a/2, -a/2, k)}
# 自由度定義自我檢查：C 的 x 位移＝u1、B 的 y 位移＝u2、A 的 y 位移＝u3
disp = lambda x, y: (ux - th*y, uy + th*x)
assert sp.simplify(disp(*cols["C"][:2])[0] - u1) == 0
assert sp.simplify(disp(*cols["B"][:2])[1] - u2) == 0
assert sp.simplify(disp(*cols["A"][:2])[1] - u3) == 0
Ue = sum(kk*(disp(x, y)[0]**2 + disp(x, y)[1]**2) for x, y, kk in cols.values())/2
Jc = m*a**2/6
Te = (m*(ux**2 + uy**2) + Jc*th**2)/2
K1 = sp.Matrix(3, 3, lambda i, j: sp.diff(Ue, U[i], U[j]))
M1 = sp.Matrix(3, 3, lambda i, j: sp.diff(Te, U[i], U[j]))
# 路徑 2：質心座標矩陣（本庫舊解 §4 的 K_c、M_c）＋轉換
Kc = k*sp.Matrix([[6, 0, 0], [0, 6, -a], [0, -a, 3*a**2]])
Mc = sp.Matrix([[m, 0, 0], [0, m, 0], [0, 0, Jc]])
T = sp.Matrix([[1, -sp.Rational(1, 2), sp.Rational(1, 2)], [0, sp.Rational(1, 2), sp.Rational(1, 2)], [0, 1/a, -1/a]])
K2 = sp.simplify(T.T*Kc*T); M2 = sp.simplify(T.T*Mc*T)
# 路徑 3：u2＝1（u1＝u3＝0）＝繞 D 轉 1/a；各柱位移、力，再由 P1(C,x)、P2(B,y)、P3(A,y) 平衡
th0 = 1/a; D = sp.Matrix([-a/2, -a/2])
F = sp.Matrix([0, 0]); MD = 0
for x, y, kk in cols.values():
    r = sp.Matrix([x, y]) - D; d = sp.Matrix([-th0*r[1], th0*r[0]]); f = kk*d
    F += f; MD += r[0]*f[1] - r[1]*f[0]
P1 = F[0]; P2 = sp.simplify(MD/a); P3 = sp.simplify(F[1] - P2)          # C 對 D 力臂 0；B 力臂 a；A 力臂 0
G = sp.Matrix([0, 0]) - D; aG = sp.Matrix([-th0*G[1], th0*G[0]])
Fi = m*aG; Mi = G[0]*Fi[1] - G[1]*Fi[0] + Jc*th0
Q1 = Fi[0]; Q2 = sp.simplify(Mi/a); Q3 = sp.simplify(Fi[1] - Q2)
# e：地表沿 D→B 單位位移 (1/√2, 1/√2) 對各自由度的剛體位移
e = sp.Matrix([1, 1, 1])/sp.sqrt(2)
assert sp.simplify(T*e - sp.Matrix([1/sp.sqrt(2), 1/sp.sqrt(2), 0])) == sp.zeros(3, 1)
print("K/k =", sp.simplify(K1/k)); print("M/m =", sp.simplify(M1/m))
# 正本寫入值
book = {"k12": -36*EI/h**3, "k22": 60*EI/h**3, "k32": -36*EI/h**3,
        "m12": -m/2, "m22": 2*m/3, "m32": -m/6}
mis = 0
for name, (K, M) in {"能量法": (K1, M1), "座標轉換": (K2, M2)}.items():
    for i, nm in enumerate(("12", "22", "32")):
        for key, val in (("k"+nm, K[i, 1]), ("m"+nm, M[i, 1])):
            ok = sp.simplify(val - book[key]) == 0; mis += (not ok)
            print(f"{name} {key} = {sp.simplify(val)}  {'OK' if ok else 'MISMATCH'}")
    ok = sp.simplify(K - K.T) == sp.zeros(3, 3) and sp.simplify(M - M.T) == sp.zeros(3, 3); mis += (not ok)
for key, val in (("k12", P1), ("k22", P2), ("k32", P3), ("m12", Q1), ("m22", Q2), ("m32", Q3)):
    ok = sp.simplify(val - book[key]) == 0; mis += (not ok); print(f"平衡法 {key} = {sp.simplify(val)}  {'OK' if ok else 'MISMATCH'}")
# 完整矩陣（§5 引用）
ok = sp.simplify(K1 - k*sp.Matrix([[6, -3, 3], [-3, 5, -3], [3, -3, 7]])) == sp.zeros(3, 3); mis += (not ok)
ok = sp.simplify(M1 - m*sp.Matrix([[1, -sp.Rational(1,2), sp.Rational(1,2)], [-sp.Rational(1,2), sp.Rational(2,3), -sp.Rational(1,6)], [sp.Rational(1,2), -sp.Rational(1,6), sp.Rational(2,3)]])) == sp.zeros(3, 3); mis += (not ok)
# Me 第二列（§4 運動方程式驗核）：(M e)_2 = (−1/2+2/3−1/6) m/√2 = 0
ok = sp.simplify((M1*e)[1]) == 0; mis += (not ok); print("(Me)_2 =", sp.simplify((M1*e)[1]))
print("MISMATCHES:", mis)
