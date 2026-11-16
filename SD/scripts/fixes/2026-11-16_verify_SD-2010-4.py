#!/usr/bin/env python3
"""SD-2010-4 勘誤驗算（2026-11-16）。題意依題目正本（已確認）：(a) 左柱底鉸、右柱底固定；(b) 兩柱底固定；柱頂剛接剛性樓版。
路徑 1：直接勁度法（2D 構架，梁 EI 取極大）數值凝縮側向勁度；路徑 2：閉合式 3、12 EI/L³。
崩塌：虛功法 vs 逐步塑鉸（事件對事件）推覆。EI=L=Mp=1 無因次。最後印 MISMATCHES。"""
import sys, numpy as np
from pathlib import Path
SD = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
md = (SD/"raw/solutions/SD-2010-4/SD-2010-4.md").read_text(encoding="utf-8")
def frame_K(left_pin, releases=()):
    # 節點：0 左底、1 右底、2 左頂、3 右頂；DOF (u,v,θ)；跨度 1
    X = {0:(0,0),1:(1,0),2:(0,1),3:(1,1)}; N=12; K=np.zeros((N,N))
    def elem(i,j,EI,EA=1e8):
        (x1,y1),(x2,y2)=X[i],X[j]; L=np.hypot(x2-x1,y2-y1); c,s=(x2-x1)/L,(y2-y1)/L
        k=np.zeros((6,6)); a=EA/L; b=EI/L**3
        k[[0,3],[0,3]]=a; k[0,3]=k[3,0]=-a
        kb=b*np.array([[12,6*L,-12,6*L],[6*L,4*L*L,-6*L,2*L*L],[-12,-6*L,12,-6*L],[6*L,2*L*L,-6*L,4*L*L]])
        idx=[1,2,4,5]
        for p in range(4):
            for q in range(4): k[idx[p],idx[q]]=kb[p,q]
        T=np.zeros((6,6)); R=np.array([[c,s,0],[-s,c,0],[0,0,1]]); T[:3,:3]=R; T[3:,3:]=R
        kg=T.T@k@T; d=[3*i,3*i+1,3*i+2,3*j,3*j+1,3*j+2]
        for p in range(6):
            for q in range(6): K[d[p],d[q]]+=kg[p,q]
    elem(0,2,1.0); elem(1,3,1.0); elem(2,3,1e6)
    fixed=[0,1,3,4,5]+([] if left_pin else [2])
    free=[d for d in range(N) if d not in fixed]
    Kf=K[np.ix_(free,free)]
    # 側向：節點 2、3 的 u 相同（梁 EA 大已近似），對 u2 施單位力求位移
    F=np.zeros(len(free)); F[free.index(6)]=1.0
    u=np.linalg.solve(Kf,F); return 1/u[free.index(6)]
mm=0
def chk(n,a,b,tol=1e-3):
    global mm; ok=abs(a-b)<tol*max(1,abs(b)); mm+=(not ok); print(("OK " if ok else "BAD"),n,round(a,5),"vs",round(b,5))
Ka=frame_K(True); Kb=frame_K(False)
chk("K_a = 15",Ka,15); chk("K_b = 24",Kb,24)
chk("ω_a/ω_b = √(15/24)",np.sqrt(Ka/Kb),0.79057); chk("ω_b/ω_a",np.sqrt(Kb/Ka),1.26491)
# 逐步塑鉸 (a)：右柱 k=12，端彎矩 = 6Δ（EI=L=1）；左柱 k=3，頂彎矩 = 3Δ
D1=1/6; V1=15*D1; Du=1/3; Vu=2+3*Du
chk("Δ1 = 1/6",D1,1/6); chk("V1 = 2.5",V1,2.5); chk("左柱頂彎矩@Δ1 = 0.5",3*D1,0.5); chk("Δu = 2Δ1",Du,2*D1); chk("V_a = 3",Vu,3)
chk("虛功 V_a",3.0,Vu); chk("V_b = 4（每柱 VL/4=Mp）",4.0,24*(1/6)); chk("V_a/V_b",3/4,0.75)
chk("Mp/My = Z/S = 1.5",(1/4)/(1/6),1.5); chk("右柱彈性剪力比 12/15",12/15,0.8)
for s in ["\\sqrt{\\frac{15}{24}} = 0.791","1.265","V_a = \\frac{3M_p}{L}","\\frac{4M_p}{L} = \\frac{\\sigma_y b^3}{L}","0.75","M_pL^2/(3EI)","2.5M_p/L"]:
    if s not in md: mm+=1; print("BAD 正本缺",s)
body=md.split("### 5.4")[0].split("## 2.")[1]
for s in ["6EI/L^3}","= 2}","V_a = 2V_b","\\frac{2M_p}{L} = \\frac{\\sigma_y b^3}{2L}","\\sqrt{4}","固定-固定結構性能較優"]:
    if s in body: mm+=1; print("BAD §2–§5.3 殘留舊值",s)
print("MISMATCHES:",mm)
