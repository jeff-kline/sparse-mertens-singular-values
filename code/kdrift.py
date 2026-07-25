import math, numpy as np, sys
sys.path.insert(0,".")
from checkA import rho
D=[(1e5,2289.3),(3e5,5211.8),(1e6,12850.5),(3e6,29519.5),(1e7,73972.3),(3e7,172026.3)]
print("TRUE data: effective k in ||w|| = C n^{5/6} (log n)^{-k}, and local exponent")
for i in range(1,len(D)):
    n0,W0=D[i-1]; n1,W1=D[i]; L0,L1=math.log(n0),math.log(n1)
    k=-(math.log(W1/W0)-(5/6)*math.log(n1/n0))/math.log(L1/L0)
    e=math.log(W1/W0)/math.log(n1/n0)
    print(f"  n {n0:.0e} -> {n1:.0e}:  k = {k:7.4f}   local exp = {e:.4f}")
# model: J(L) and its B-share
a=np.linspace(1e-7,0.5,400001)
g=rho((1-2*a)/a)**2/(a*(1-a)**2)
print("\nMODEL (j = p prime, |M| ~ rho(u-1) x/log x):  k, local exp, B-share")
Ls=[math.log(n) for n,_ in D]
V=[]
for L in Ls:
    wt=g*np.exp(-a*L); J=np.trapezoid(wt,a)
    Bs=np.trapezoid(np.where(a>=1/3,wt,0.0),a)/J
    V.append((L,math.exp(L)*math.sqrt(J)/L,Bs))
for i in range(1,len(V)):
    L0,W0,_=V[i-1]; L1,W1,B1=V[i]
    k=-(math.log(W1/W0)-(5/6)*(L1-L0))/math.log(L1/L0)
    e=math.log(W1/W0)/(L1-L0)
    print(f"  L {L0:6.3f} -> {L1:6.3f}:  k = {k:7.4f}   local exp = {e:.4f}   Bshare(top)={B1:.4f}")
print("\nMODEL far out: local exponent and k")
for L in [20,30,50,100,300,1000,3000,1e4,1e5,1e6]:
    h=1e-3*L
    J0=np.trapezoid(g*np.exp(-a*(L-h)),a); J1=np.trapezoid(g*np.exp(-a*(L+h)),a)
    W0=math.exp(L-h)*math.sqrt(J0)/(L-h); W1=math.exp(L+h)*math.sqrt(J1)/(L+h)
    e=math.log(W1/W0)/(2*h)
    J=np.trapezoid(g*np.exp(-a*L),a)
    logW=L+0.5*math.log(J)-math.log(L)
    pred=math.sqrt(L*math.log(L))
    print(f"  L={L:8.0f}  local exp={e:.5f}   (log n - log||w||)/sqrt(L logL) = {(L-logW)/pred:.4f}")
