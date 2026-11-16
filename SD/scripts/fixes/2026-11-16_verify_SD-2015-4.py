#!/usr/bin/env python3
"""SD-2015-4 勘誤驗算（2026-11-16）：簡易懸臂梁法。柱 x=0、7、17 m，h=4 m，P=20 tf 向右作用於節點 1，柱面積皆 1 m²。
軸力 N 以壓力為正；路徑 1：懸臂梁法逐步；路徑 2：整體傾覆力矩（對柱 1 底）閉合與拉壓方向判定。最後印 MISMATCHES。"""
import sys
from fractions import Fraction as F
from pathlib import Path
SD = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
md = (SD/"raw/solutions/SD-2015-4/SD-2015-4.md").read_text(encoding="utf-8")
x=[F(0),F(7),F(17)]; h=F(4); P=F(20)
xb=sum(x)/3; d=[xi-xb for xi in x]; I=sum(di**2 for di in d)
k=P*h/2/I; N=[k*di for di in d]          # 上方自由體：柱軸力逆時針力矩抵抗 P·h/2 順時針 → 右側受壓為正
Vb12=-N[0]; Vb23=Vb12-N[1]               # 節點垂直平衡（大小）
Mb12=abs(Vb12)*F(7,2); Mb23=abs(Vb23)*5
Mc=[Mb12, Mb12+Mb23, Mb23]; Vc=[2*m/h for m in Mc]
mm=0
def chk(n,a,b):
    global mm; ok=(a==b); mm+=(not ok); print(("OK " if ok else "BAD"),n,float(a),"vs",float(b))
chk("x̄=8",xb,8); chk("ΣAd²=146",I,146); chk("N1=-160/73（拉）",N[0],F(-160,73)); chk("N2=-20/73（拉）",N[1],F(-20,73)); chk("N3=+180/73（壓）",N[2],F(180,73))
chk("Mb12=560/73",Mb12,F(560,73)); chk("Mb23=900/73",Mb23,F(900,73)); chk("Mc2=20",Mc[1],20); chk("ΣVc=P",sum(Vc),P)
ot=sum(Mc)+sum(Ni*xi for Ni,xi in zip(N,x)); chk("對柱1底 ΣM_base+ΣN·x = P·H（壓為正）",ot,P*h)
chk("拉壓寫反時不閉合（應為 0 差值檢查）", sum(Mc)-sum(Ni*xi for Ni,xi in zip(N,x)) != P*h, True)
for s in ["| 拉力 |","| 壓力 |","左柱受拉、右柱受壓","7.67","12.33","boxed{20}"]:
    if s not in md: mm+=1; print("BAD 正本缺",s)
for s in ["右柱受拉、左柱受壓","右柱（張力）","中柱（壓力）","| 張力 |","→右柱受拉"]:
    if s in md: mm+=1; print("BAD 殘留舊觀念",s)
print("MISMATCHES:",mm)
