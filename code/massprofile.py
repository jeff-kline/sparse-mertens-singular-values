import numpy as np, math, sys
def sieve(n):
    isp=np.ones(n+1,dtype=bool); isp[:2]=False
    for i in range(2,int(n**0.5)+1):
        if isp[i]: isp[i*i::i]=False
    primes=np.nonzero(isp)[0]
    mu=np.ones(n+1,dtype=np.int8); mu[0]=0
    lpf=np.ones(n+1,dtype=np.int32); spf=np.zeros(n+1,dtype=np.int32)
    for p in primes:
        lpf[p::p]=p; mu[p::p]=-mu[p::p]
        pp=int(p)*int(p)
        if pp<=n: mu[pp::pp]=0
    for p in primes[::-1]: spf[p::p]=p
    return mu,lpf,spf,np.cumsum(isp).astype(np.int64)
def profile(n,nb=24):
    mu,lpf,spf,PI=sieve(n)
    j=np.arange(1,n+1,dtype=np.int64)
    y=lpf[1:n+1].astype(np.int64); y[0]=1
    x=n//j; sqf=mu[1:n+1]!=0
    w=np.zeros(n,dtype=np.float64)
    nsf=~sqf; nsf[0]=False; w[nsf]=1.0
    A=sqf&(y>=x); w[A]=1.0
    B=sqf&(~A)&(y*y>=x); w[B]=(1-(PI[x[B]]-PI[y[B]])).astype(np.float64)
    C=sqf&(~A)&(y*y<x)
    cj,cy,cx=j[C],y[C],x[C]; cw=np.zeros(len(cj))
    for yv in np.unique(cy):
        s=cy==yv; xs=cx[s]; xmax=int(xs.max())
        keep=np.zeros(xmax+1,dtype=bool); keep[1]=True
        if xmax>=2: keep[2:]=spf[2:xmax+1]>yv
        cs=np.cumsum(np.where(keep,mu[:xmax+1],0).astype(np.int64))
        v=cs[xs].astype(np.float64); v[cj[s]==1]-=1.0; cw[s]=v
    w[C]=cw
    W2=float(np.sum(w**2)); L=math.log(n)
    beta=np.log(np.maximum(j,2))/L
    idx=np.minimum((beta*nb).astype(int),nb-1)
    mass=np.bincount(idx,weights=w**2,minlength=nb)
    # mass-weighted mean beta, and peak bin centre
    mb=float(np.sum(beta*w**2)/W2)
    pk=int(np.argmax(mass)); pkc=(pk+0.5)/nb
    jm=int(np.argmax(np.abs(w)))+1
    return math.sqrt(W2), mb, pkc, mass/W2, math.log(jm)/L, float(np.abs(w).max())
print("       n       ||w||     mass-mean beta   peak-bin beta   beta of argmax|w_j|   sqrt(loglog/log)")
for n in [int(v) for v in sys.argv[1:]]:
    W,mb,pkc,mass,bjm,mx=profile(n)
    L=math.log(n); pred=math.sqrt(math.log(L)/L)
    print(f"{n:9d} {W:11.1f}      {mb:.4f}          {pkc:.4f}           {bjm:.4f}            {pred:.4f}")
    print("            mass by beta-decile: "+" ".join(f"{v:.3f}" for v in
          np.add.reduceat(mass,np.arange(0,len(mass),len(mass)//8))))
