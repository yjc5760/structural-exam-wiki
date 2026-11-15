import numpy as np
from scipy.signal import lsim
from scipy.integrate import solve_ivp
m,k,xi=100.,100.,0.30; w=np.sqrt(k/m); wd=w*np.sqrt(1-xi**2); c=2*xi*m*w
TA,TB,TC,TD,PM,PN=0.1,0.12,0.2,0.25,2000.,-500.
slope=PN/(TB-TA); TP=TA-PM/(-slope)
T=[0,TP,TA,TB,TC,TD]; P=[0,PM,0,PN,PN,0]
I=np.trapezoid(P,T)
segs=[0.5*TP*PM,0.5*(TA-TP)*PM,0.5*(TB-TA)*PN,(TC-TB)*PN,0.5*(TD-TC)*PN]
# exact state at TD via ODE (piecewise linear force, tight tol)
f=lambda t: np.interp(t,T,P)
sol=solve_ivp(lambda t,y:[y[1],(f(t)-c*y[1]-k*y[0])/m],[0,TD],[0,0],max_step=1e-4,rtol=1e-11,atol=1e-13)
x0,v0=sol.y[0,-1],sol.y[1,-1]
# kinematic approx
tt=np.linspace(0,TD,200001); xk=np.trapezoid((TD-tt)*f(tt),tt)/m; vk=I/m
def freemax(x0,v0):
    A=x0; B=(v0+xi*w*x0)/wd
    th=np.arctan2(B*wd-xi*w*A, xi*w*B+A*wd); tau=th/wd
    return tau, np.exp(-xi*w*tau)*(A*np.cos(wd*tau)+B*np.sin(wd*tau)), A, B
tau,xm,A,B=freemax(x0,v0); taur,xmr,Ar,Br=freemax(xk,vk)
# path 2: full lsim
t=np.linspace(0,30,300001); _,y,_=lsim(([1],[m,c,k]),f(t),t); i=np.argmax(np.abs(y))
# path 3: pure impulse
tau_i=np.arctan(wd/(xi*w))/wd; xi_imp=(I/(m*wd))*np.exp(-xi*w*tau_i)*np.sin(wd*tau_i)
R=dict(TP=TP,I=I,segs=segs,x0=x0,v0=v0,A=A,B=B,tau=tau,tmax=TD+tau,xmax=xm,xk=xk,vk=vk,xmax_kin=xmr,lsim=(y[i],t[i]),imp=xi_imp,wd=wd)
for kk,vv in R.items(): print(kk,vv)
print('MISMATCHES:', int(abs(xm-y[i])>1e-3*abs(xm)))
