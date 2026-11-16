#!/usr/bin/env python3
"""SD-2018-2 勘誤驗算（2026-11-16，X-G1 階段 C）：三軸座標的斜率與軸向、規範譜各段在 log Spv–log T 上的斜率。
題意：題目正本判讀 #2（Spa 軸左上、Sd 軸右上）、#3（a→b 45°、b→c 較陡、c→d 45°、d→e 水平、e→f −45°）。"""
import numpy as np
mis = []
def chk(n, got, ref, tol=1e-9):
    ok = abs(got-ref) <= tol*max(1, abs(ref)); print(f"{n:46s} {got:+.6f} ref {ref:+.6f} {'OK' if ok else 'MISMATCH'}")
    if not ok: mis.append(n)
Spv_from_Spa = lambda T, Spa: T*Spa/(2*np.pi)
Spv_from_Sd = lambda T, Sd: 2*np.pi*Sd/T
T1, T2 = 0.5, 2.0
s = lambda f: (np.log10(f(T2)) - np.log10(f(T1)))/(np.log10(T2) - np.log10(T1))
chk("常數 Spa 線斜率", s(lambda T: Spv_from_Spa(T, 1.0)), +1)
chk("常數 Sd 線斜率", s(lambda T: Spv_from_Sd(T, 1.0)), -1)
# 軸向：在 (logT, logSpv) 平面，Spa = 2π Spv/T 的梯度方向；Sd = T Spv/2π 的梯度方向
gSpa = np.array([-1.0, 1.0])/np.sqrt(2); gSd = np.array([1.0, 1.0])/np.sqrt(2)   # d(logSpa)=dlogSpv−dlogT；d(logSd)=dlogSpv+dlogT
chk("Spa 增大方向 x 分量（負＝往左）", gSpa[0], -1/np.sqrt(2)); chk("Spa 增大方向 y 分量（正＝往上）", gSpa[1], 1/np.sqrt(2))
chk("Sd 增大方向 x 分量（正＝往右）", gSd[0], 1/np.sqrt(2));  chk("Sd 增大方向 y 分量", gSd[1], 1/np.sqrt(2))
# 數值確認：由 (T,Spv)=(1,1) 往左上走一步 Spa 變大、Sd 不變；往右上走 Sd 變大、Spa 不變
T, V, d = 1.0, 1.0, 0.1
Spa = lambda T, V: 2*np.pi*V/T; Sd = lambda T, V: T*V/(2*np.pi)
chk("左上一步 Spa 比", Spa(T*10**-d, V*10**d)/Spa(T, V), 10**(2*d)); chk("左上一步 Sd 比", Sd(T*10**-d, V*10**d)/Sd(T, V), 1.0)
chk("右上一步 Sd 比", Sd(T*10**d, V*10**d)/Sd(T, V), 10**(2*d)); chk("右上一步 Spa 比", Spa(T*10**d, V*10**d)/Spa(T, V), 1.0)
# 規範譜（SDS=1、SD1=0.6、T0=0.6，g=9.81）在 log Spv–log T 的斜率
SDS, SD1 = 1.0, 0.6; T0 = SD1/SDS; g = 9.81
Sa = lambda T: SDS*(0.4+3*T/T0) if T <= 0.2*T0 else (SDS if T <= T0 else SD1/T)
Spv = lambda T: Sa(T)*g*T/(2*np.pi)
sl = lambda a, b: (np.log10(Spv(b))-np.log10(Spv(a)))/(np.log10(b)-np.log10(a))
chk("短週期 SaD=SDS 段斜率（對應 c→d）", sl(0.3*T0, 0.9*T0), +1)
chk("中長週期 SD1/T 段斜率（對應 d→e，水平）", sl(1.5*T0, 4*T0), 0)
print("較短週期段斜率（>1，對應 b→c 較陡）:", round(sl(0.05*T0, 0.19*T0), 3)); 
if not sl(0.05*T0, 0.19*T0) > 1: mis.append("較短週期段斜率")
chk("T0 = SD1/SDS 處兩式相接", SDS, SD1/T0)
chk("0.2T0 處兩式相接", SDS*(0.4+3*0.2), SDS)
chk("SD1/T 段 Spv = SD1·g/2π", Spv(3*T0), SD1*g/(2*np.pi))
print("MISMATCHES:", len(mis), mis if mis else "")
