import numpy as np
E=2.3e6; g=980.0
a1,a2,h1,h2=50.,40.,420.,320.
I1,I2=a1**4/12,a2**4/12
kf1=12*E*I1/h1**3; kp1=3*E*I1/h1**3; kf2=12*E*I2/h2**3
k1=2*kf1+kp1; k2=2*kf2
m1,m2=75000/g,20000/g
A=m1*m2; B=(k1+k2)*m2+k2*m1; C=k1*k2
lam=np.sort(np.roots([A,-B,C]).real); w=np.sqrt(lam); T=2*np.pi/w; f=w/2/np.pi
r=[(k1+k2-l*m1)/k2 for l in lam]; r2=[k2/(k2-l*m2) for l in lam]
# path2 numpy eig + SI units
gS=9.80665; ES=E*gS*1e4; K=np.array([[k1+k2,-k2],[-k2,k2]]); M=np.diag([m1,m2])
w2=np.sqrt(np.sort(np.linalg.eigvals(np.linalg.solve(M,K)).real))
kS1=(24+3)*ES*(0.5**4/12)/4.2**3; kS2=24*ES*(0.4**4/12)/3.2**3
wS=np.sqrt(np.sort(np.linalg.eigvals(np.linalg.solve(np.diag([75000,20000]),[[kS1+kS2,-kS2],[-kS2,kS2]])).real))
print(dict(I1=I1,I2=I2,kf1=kf1,kp1=kp1,kf2=kf2,k1=k1,k2=k2,m1=m1,m2=m2,A=A,B=B,C=C,BA=B/A,CA=C/A,disc=(B/A)**2-4*C/A,lam=lam,w=w,T=T,f=f,r=r,r2=r2,w_eig=w2,w_SI=wS))
orth=m1*1*1+m2*r[0]*r[1]; print('orth',orth)
print('mode norm top=1:',[1/x for x in r])
print('MISMATCHES:', int(np.max(np.abs(w-w2))>1e-6) + int(np.max(np.abs(w-wS)/w)>2e-3) + int(max(abs(r[i]-r2[i]) for i in range(2))>1e-6))
