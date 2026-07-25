"""Analytic route (agent B): numerical checks of the M(x,y) asymptotic and of the
hyperbola integral for ||w||.

Central claim to test:   M(x, x^{1/u})  ~  - li(x) * rho(u-1)     (Dickman rho)
"""
import numpy as np, math, sys

# ---------------------------------------------------------------- Dickman rho
class Dickman:
    """rho on [0,U] via  u rho(u) = int_{u-1}^{u} rho(t) dt, trapezoid on step h."""
    def __init__(self, U=30.0, h=1.0/2048):
        self.h = h
        N = int(round(U/h))
        r = np.zeros(N+1)
        n1 = int(round(1/h))
        r[:n1+1] = 1.0
        # cumulative integral of rho, C[k] = int_0^{kh} rho
        C = np.zeros(N+1)
        C[:n1+1] = np.arange(n1+1)*h
        for k in range(n1+1, N+1):
            u = k*h
            # need rho(u) = (1/u) * (C[k] - C[k-n1]);  C[k] = C[k-1] + h/2*(r[k-1]+r[k])
            # solve linear:  r_k = (1/u)*(C[k-1] + h/2*(r[k-1]+r_k) - C[k-n1])
            a = 1.0/u
            rhs = a*(C[k-1] + 0.5*h*r[k-1] - C[k-n1])
            r[k] = rhs/(1 - a*0.5*h)
            C[k] = C[k-1] + 0.5*h*(r[k-1]+r[k])
        self.r, self.N, self.U = r, N, U
    def __call__(self, u):
        u = np.asarray(u, dtype=float)
        out = np.zeros_like(u)
        out[u <= 0] = 0.0
        m = (u > 0)
        t = np.clip(u[m]/self.h, 0, self.N-1e-9)
        i = t.astype(int); f = t - i
        out[m] = self.r[i]*(1-f) + self.r[i+1]*f
        out[u < 0] = 0.0
        return out if out.shape else float(out)

RHO = Dickman()
def rho(u):
    a = np.atleast_1d(np.asarray(u, dtype=float))
    v = RHO(a)
    return v if np.ndim(u) else float(v[0])

def li(x):
    """logarithmic integral li(x) = int_0^x dt/log t (principal value), x>1."""
    from mpmath import li as mli
    return float(mli(x))

# ---------------------------------------------------------------- sieves
def sieve(n):
    isp = np.ones(n+1, dtype=bool); isp[:2] = False
    for i in range(2, int(n**0.5)+1):
        if isp[i]: isp[i*i::i] = False
    primes = np.nonzero(isp)[0]
    mu = np.ones(n+1, dtype=np.int8); mu[0] = 0
    lpf = np.ones(n+1, dtype=np.int32); spf = np.zeros(n+1, dtype=np.int32)
    for p in primes:
        lpf[p::p] = p; mu[p::p] = -mu[p::p]
        pp = int(p)*int(p)
        if pp <= n: mu[pp::pp] = 0
    for p in primes[::-1]: spf[p::p] = p
    return mu, lpf, spf, np.cumsum(isp).astype(np.int64), primes

# ---------------------------------------------------------------- test 1
def test_Mxy(X=4_000_000):
    """M(x,y) vs -li(x) rho(u-1) for a grid of (x,u)."""
    mu, lpf, spf, PI, primes = sieve(X)
    print(f"# M(x,y) vs -li(x)*rho(u-1),  x up to {X}")
    print(f"{'x':>10} {'u':>6} {'y':>9} {'M(x,y)':>12} {'-li(x)rho(u-1)':>16} "
          f"{'ratio':>8} {'-x/logx*rho':>13} {'ratio2':>8}")
    for x in [X//8, X//2, X]:
        for u in [1.5, 2.0, 2.3, 2.6, 3.0, 3.5, 4.0, 5.0]:
            y = int(round(x**(1.0/u)))
            if y < 2: continue
            keep = np.zeros(x+1, dtype=bool); keep[1] = True
            keep[2:] = spf[2:x+1] > y
            M = int(np.sum(np.where(keep, mu[:x+1], 0).astype(np.int64)))
            ueff = math.log(x)/math.log(y)
            pred = -li(x)*rho(ueff-1)
            pred2 = -(x/math.log(x))*rho(ueff-1)
            r  = M/pred  if pred  else float('nan')
            r2 = M/pred2 if pred2 else float('nan')
            print(f"{x:10d} {ueff:6.3f} {y:9d} {M:12d} {pred:16.1f} {r:8.4f} "
                  f"{pred2:13.1f} {r2:8.4f}")

# ---------------------------------------------------------------- exact ||w||^2
def wnorm2_exact(n, split=False):
    mu, lpf, spf, PI, primes = sieve(n)
    j = np.arange(1, n+1, dtype=np.int64)
    y = lpf[1:n+1].astype(np.int64); y[0] = 1
    x = n // j
    sqf = mu[1:n+1] != 0
    nsf = ~sqf; nsf[0] = False
    tot_nsf = float(np.count_nonzero(nsf))
    A = sqf & (y >= x); tot_A = float(np.count_nonzero(A))
    B = sqf & (~A) & (y*y >= x)
    wB = (1 - (PI[x[B]] - PI[y[B]])).astype(np.float64)
    tot_B = float(np.sum(wB**2))
    C = sqf & (~A) & (y*y < x)
    cj, cy, cx = j[C], y[C], x[C]
    tot_C = 0.0
    for yv in np.unique(cy):
        s = cy == yv
        xs, js = cx[s], cj[s]
        xmax = int(xs.max())
        keep = np.zeros(xmax+1, dtype=bool); keep[1] = True
        if xmax >= 2: keep[2:] = spf[2:xmax+1] > yv
        cs = np.cumsum(np.where(keep, mu[:xmax+1], 0).astype(np.int64))
        vals = cs[xs].astype(np.float64)
        vals[js == 1] -= 1.0
        tot_C += float(np.sum(vals**2))
    T = tot_nsf + tot_A + tot_B + tot_C
    if split:
        return T, dict(nsf=tot_nsf, A=tot_A, B=tot_B, C=tot_C)
    return T

# ---------------------------------------------------------------- prediction
def zeta(s):
    from mpmath import zeta as mz
    return float(mz(s))

def predict(n, umax=14.0, nu=6000, use_li=True, Aexp=True):
    """  sum_{j sqfree>=2} M(n/j,P(j))^2
         ~ (n^2/?) int_1^inf  A(u) * rho(u-1)^2 * (1+u)/u^2 * [li(x)^2/x^2 * x] du
      Derivation (see report): with j=m*p, p=P(j), x=n/(mp), u=log x/log p,
      the p-sum -> int  (n/m)^{... }.  Written directly in terms of x:
         contribution = sum_m  int  li(x)^2 * (dp/log p),  x=(n/m)/p.
    """
    L = math.log(n)
    us = np.linspace(1.0001, umax, nu)
    vals = np.zeros(nu)
    from mpmath import li as mli
    for i, u in enumerate(us):
        logp = L/(1+u); logx = u*L/(1+u)
        x = math.exp(logx)
        if x < 2: continue
        lix = float(mli(x)) if use_li else x/logx
        p = math.exp(logp)
        # dp/log p = p*du/(1+u)   (see report)
        # sum over m: m^{-2+1/(1+u)} weight from (n/m) scaling, squarefree m
        s = 2 - 1.0/(1+u)
        Am = zeta(s)/zeta(2*s) if Aexp else 1.0
        vals[i] = lix**2 * p/(1+u) * rho(u-1)**2 * Am
    return np.trapezoid(vals, us) if hasattr(np, 'trapezoid') else np.trapz(vals, us), us, vals

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "M"
    if which == "M":
        test_Mxy(int(sys.argv[2]) if len(sys.argv) > 2 else 2_000_000)
    elif which == "w":
        for n in [int(v) for v in sys.argv[2:]]:
            T, d = wnorm2_exact(n, split=True)
            W = math.sqrt(T)
            P, _, _ = predict(n)
            print(f"n={n:9d} ||w||={W:12.2f}  T={T:.4e}  pred={P:.4e} ratio={T/P:.4f}")
            print(f"        split: nsf={d['nsf']:.3e} A={d['A']:.3e} "
                  f"B={d['B']:.3e} ({d['B']/T*100:5.2f}%) C={d['C']:.3e} ({d['C']/T*100:5.2f}%)")

# ================================================================ continuum Buchstab
# H(b,a) models M(e^b, e^a) via the EXACT Buchstab identity
#     M(x,y) = 1 - sum_{y<p<=x} M(x/p, p),   M(x,y)=1 for y>=x
# with the single approximation  sum_p f(p)  ->  int_2^. f(t) dt/log t.
# Grid: h = log2/K so that log 2 is grid point K.  Htab[i,j] = H(i*h, j*h).
class ContBuchstab:
    def __init__(self, B, K=24):
        self.h = h = math.log(2.0)/K
        self.K = K
        self.N = N = int(math.ceil(B/h)) + 2
        H = np.ones((N+1, N+1))          # H[i,j]; default 1 (covers j>=i)
        c = np.arange(N+1)*h
        wt = np.zeros(N+1)               # e^c/c * h, trapezoid handled by half weights
        wt[K:] = np.exp(c[K:])/c[K:]*h
        for i in range(K+1, N+1):
            k = np.arange(K, i+1)
            V = H[i-k, k]                     # M(x/p, p) along the diagonal
            integ = V*wt[k]
            integ[0] *= 0.5; integ[-1] *= 0.5
            # suffix sums: S[j] = sum_{k=j}^{i}
            S = np.concatenate(([0.0], np.cumsum(integ[::-1])))[::-1]  # S[t]=sum_{k>=K+t}
            H[i, K:i+1] = 1.0 - S[:i+1-K]
            H[i, :K] = H[i, K]                # y<2 : no constraint
            # j>i stays 1
        self.H = H
    def __call__(self, logx, logy):
        h, N = self.h, self.N
        if logy >= logx: return 1.0
        bi = logx/h; aj = logy/h
        i0 = int(bi); j0 = int(aj)
        if i0 >= N: i0 = N-1
        if j0 >= N: j0 = N-1
        fb = bi-i0; fa = aj-j0
        Hh = self.H
        return float((1-fb)*((1-fa)*Hh[i0,j0]+fa*Hh[i0,j0+1])
                     + fb*((1-fa)*Hh[i0+1,j0]+fa*Hh[i0+1,j0+1]))

def test_cont(X=2_000_000, K=24):
    mu, lpf, spf, PI, primes = sieve(X)
    CB = ContBuchstab(math.log(X)+0.5, K=K)
    print(f"# continuum-Buchstab model vs exact M(x,y)   (K={K})")
    print(f"{'x':>9} {'u':>6} {'y':>8} {'M exact':>11} {'H model':>11} {'ratio':>7} "
          f"{'-li*rho':>11} {'ratio':>7}")
    from mpmath import li as mli
    for x in [X//8, X//2, X]:
        for u in [1.5,2.0,2.3,2.6,3.0,3.5,4.0,5.0,6.0]:
            y = int(round(x**(1.0/u)))
            if y < 2: continue
            keep = np.zeros(x+1, dtype=bool); keep[1]=True
            keep[2:] = spf[2:x+1] > y
            M = int(np.sum(np.where(keep, mu[:x+1],0).astype(np.int64)))
            ue = math.log(x)/math.log(y)
            hm = CB(math.log(x), math.log(y))
            pr = -float(mli(x))*rho(ue-1)
            print(f"{x:9d} {ue:6.3f} {y:8d} {M:11d} {hm:11.1f} {M/hm if hm else 0:7.4f} "
                  f"{pr:11.1f} {M/pr if pr else 0:7.4f}")

# ================================================================ mass profile in u and m
def wvec(n):
    """exact w_j for all j<=n, plus P(j)."""
    mu, lpf, spf, PI, primes = sieve(n)
    j = np.arange(1, n+1, dtype=np.int64)
    y = lpf[1:n+1].astype(np.int64); y[0] = 1
    x = n // j
    sqf = mu[1:n+1] != 0
    w = np.zeros(n, dtype=np.float64)
    nsf = ~sqf; nsf[0] = False; w[nsf] = 1.0
    A = sqf & (y >= x); w[A] = 1.0
    B = sqf & (~A) & (y*y >= x); w[B] = (1-(PI[x[B]]-PI[y[B]])).astype(np.float64)
    C = sqf & (~A) & (y*y < x)
    cj, cy, cx = j[C], y[C], x[C]; cw = np.zeros(len(cj))
    for yv in np.unique(cy):
        s = cy == yv; xs = cx[s]; xmax = int(xs.max())
        keep = np.zeros(xmax+1, dtype=bool); keep[1] = True
        if xmax >= 2: keep[2:] = spf[2:xmax+1] > yv
        cs = np.cumsum(np.where(keep, mu[:xmax+1], 0).astype(np.int64))
        v = cs[xs].astype(np.float64); v[cj[s] == 1] -= 1.0; cw[s] = v
    w[C] = cw
    return w, y, x, sqf, mu, lpf, spf

def profile_u(n):
    w, y, x, sqf, mu, lpf, spf = wvec(n)
    j = np.arange(1, n+1, dtype=np.int64)
    L = math.log(n)
    W2 = float(np.sum(w**2))
    sel = sqf & (j >= 2) & (y < x)          # only these carry big |w|
    lx = np.log(np.maximum(x[sel], 2)); ly = np.log(np.maximum(y[sel], 2))
    u = lx/ly
    m2 = w[sel]**2
    print(f"n={n}  ||w||={math.sqrt(W2):.2f}  W2={W2:.4e}   L={L:.3f}")
    print("  mass fraction by u:")
    edges = [1,1.5,2,2.5,3,3.5,4,5,6,8,100]
    for lo,hi in zip(edges[:-1],edges[1:]):
        s = (u>=lo)&(u<hi)
        f = float(np.sum(m2[s]))/W2
        if f > 1e-5: print(f"    u in [{lo:4.1f},{hi:5.1f}): {f*100:6.2f}%")
    ubar = float(np.sum(u*m2)/np.sum(m2))
    print(f"  mass-mean u = {ubar:.4f}")
    # by m = j/P(j)
    m_of_j = j[sel]//y[sel]
    print("  mass fraction by m = j/P(j):")
    tot = 0.0
    for mv in [1,2,3,4,5,6,7,10]:
        s = m_of_j == mv
        f = float(np.sum(m2[s]))/W2; tot += f
        print(f"    m={mv:3d}: {f*100:6.2f}%")
    print(f"    (m<=10 total {tot*100:.2f}%)")
    bet = np.log(np.maximum(j[sel],2))/L
    print(f"  mass-mean beta = {float(np.sum(bet*m2)/np.sum(m2)):.4f}")
    return W2

# ================================================================ Check A
def Hgrid(CB, logx, logy):
    """vectorised bilinear lookup of the continuum-Buchstab table"""
    h, N, Ht = CB.h, CB.N, CB.H
    bi = np.clip(logx/h, 0, N-1e-9); aj = np.clip(logy/h, 0, N-1e-9)
    i0 = bi.astype(int); j0 = aj.astype(int)
    fb = bi-i0; fa = aj-j0
    v = ((1-fb)*((1-fa)*Ht[i0,j0]+fa*Ht[i0,j0+1])
         + fb*((1-fa)*Ht[i0+1,j0]+fa*Ht[i0+1,j0+1]))
    return np.where(logy >= logx, 1.0, v)

def checkA(n, K=32):
    """sum_j M_model(n/j,P(j))^2  vs  exact, and vs the pure Dickman leading term."""
    mu, lpf, spf, PI, primes = sieve(n)
    j = np.arange(1, n+1, dtype=np.int64)
    y = lpf[1:n+1].astype(np.int64); y[0] = 1
    x = n//j
    sqf = mu[1:n+1] != 0
    W2ex, d = wnorm2_exact(n, split=True)
    CB = ContBuchstab(math.log(n)+0.5, K=K)
    sel = sqf.copy(); sel[0] = False        # j>=2 squarefree
    lx = np.log(x[sel].astype(float)); ly = np.log(y[sel].astype(float))
    Hm = Hgrid(CB, lx, ly)
    modelC = float(np.sum(Hm**2))
    # pure leading Dickman:  -li(x) rho(u-1)
    from mpmath import li as mli
    u = np.where(ly > 0, lx/np.maximum(ly,1e-9), 1.0)
    lix = np.zeros_like(lx)
    xs = x[sel].astype(float)
    lix = xs/np.maximum(lx,1e-9)*(1 + 1/np.maximum(lx,1e-9) + 2/np.maximum(lx,1e-9)**2
                                  + 6/np.maximum(lx,1e-9)**3)   # li asymptotic
    lead = np.where(ly >= lx, 1.0, -lix*rho(u-1))
    leadS = float(np.sum(lead**2))
    base = d['nsf'] + 1.0            # j=1 term handled inside; nsf part
    print(f"n={n:9d}  exact W2={W2ex:.5e}  ||w||={math.sqrt(W2ex):.2f}")
    print(f"   model(cont-Buchstab) sqfree-part = {modelC:.5e} ; +nsf = {modelC+d['nsf']:.5e}"
          f"  ratio={(modelC+d['nsf'])/W2ex:.4f}   ||w||_model={math.sqrt(modelC+d['nsf']):.2f}")
    print(f"   leading -li*rho       sqfree-part = {leadS:.5e} ; +nsf = {leadS+d['nsf']:.5e}"
          f"  ratio={(leadS+d['nsf'])/W2ex:.4f}   ||w||_lead={math.sqrt(leadS+d['nsf']):.2f}")
    return W2ex, modelC+d['nsf'], leadS+d['nsf']

# ================================================================ u-resolved residual
_LI_CACHE = {}
def li_arr(x):
    """li(x) for an array x>=2 via interpolation of mpmath li on a log grid."""
    key = 'g'
    if key not in _LI_CACHE:
        from mpmath import li as mli
        g = np.linspace(math.log(2.0), 40.0, 4000)
        _LI_CACHE[key] = (g, np.array([float(mli(math.exp(t))) for t in g]))
    g, v = _LI_CACHE[key]
    lx = np.log(np.maximum(x, 2.0))
    return np.interp(lx, g, v)

def resid_u(n, K=32):
    mu, lpf, spf, PI, primes = sieve(n)
    j = np.arange(1, n+1, dtype=np.int64)
    y = lpf[1:n+1].astype(np.int64); y[0] = 1
    x = n//j
    sqf = mu[1:n+1] != 0
    w, _, _, _, _, _, _ = wvec(n)
    CB = ContBuchstab(math.log(n)+0.5, K=K)
    sel = sqf.copy(); sel[0] = False
    xs = x[sel].astype(float); ys = y[sel].astype(float)
    lx = np.log(xs); ly = np.log(ys)
    u = np.where(ly > 0, lx/np.maximum(ly, 1e-9), 0.0)
    ex = w[sel]**2
    Hm = Hgrid(CB, lx, ly)**2
    lead = np.where(ly >= lx, 1.0, -li_arr(xs)*rho(np.maximum(u-1, 0)))**2
    print(f"n={n}: exact={ex.sum():.4e} model={Hm.sum():.4e} lead={lead.sum():.4e}")
    print(f"{'u-bin':>14} {'exact':>11} {'model':>11} {'m/e':>6} {'lead':>11} {'l/e':>6}")
    edges = [0,1.0,1.5,2.0,2.5,3.0,3.5,4.0,5.0,6.0,8.0,1e9]
    for lo,hi in zip(edges[:-1],edges[1:]):
        s = (u>=lo)&(u<hi)
        e_,m_,l_ = ex[s].sum(), Hm[s].sum(), lead[s].sum()
        if e_ < 1e-9: continue
        print(f"[{lo:5.1f},{hi:6.1f}) {e_:11.4e} {m_:11.4e} {m_/e_:6.3f} {l_:11.4e} {l_/e_:6.3f}")

# ================================================================ Check B: the analytic integral
def lead_sum_exact_j(n, umin=1.0):
    """sum over ACTUAL squarefree j>=2 with u>umin of (li(n/j) rho(u-1))^2 -- the object
       the analytic integral is supposed to reproduce."""
    mu, lpf, spf, PI, primes = sieve(n)
    j = np.arange(1, n+1, dtype=np.int64)
    y = lpf[1:n+1].astype(np.int64); y[0] = 1
    x = n//j
    sqf = mu[1:n+1] != 0; sqf[0] = False
    xs = x[sqf].astype(float); ys = y[sqf].astype(float)
    lx = np.log(xs); ly = np.log(np.maximum(ys, 2.0))
    u = lx/ly
    s = u > umin
    v = li_arr(xs[s])*rho(u[s]-1)
    return float(np.sum(v**2))

def analytic_integral(n, Mmax=4000, umin=1.0, umax=12.0, nu=2400, respectPm=True):
    """sum_{m sqfree} int_{umin}^{umax} li(x)^2 rho(u-1)^2 * t/(1+u) du ,
       N=n/m, t=N^{1/(1+u)}, x=N/t.   Optional constraint p=t > P(m)."""
    mu, lpf, spf, PI, primes = sieve(Mmax)
    us = np.linspace(umin, umax, nu)
    tot = 0.0; per = []
    for m in range(1, Mmax+1):
        if mu[m] == 0: continue
        N = n/m
        if N < 4: continue
        lN = math.log(N)
        logt = lN/(1+us); logx = us*lN/(1+us)
        ok = (logx > math.log(2.0))
        if respectPm and m > 1:
            ok &= (logt > math.log(float(lpf[m])))
        x = np.exp(np.minimum(logx, 700)); t = np.exp(np.minimum(logt, 700))
        f = np.where(ok, li_arr(x)**2 * rho(us-1)**2 * t/(1+us), 0.0)
        c = float(np.trapezoid(f, us)) if hasattr(np,'trapezoid') else float(np.trapz(f,us))
        tot += c; per.append((m, c))
    return tot, per

# ================================================================ large-x safe li, and H-integral
def li_big(x):
    """li(x) for arrays: mpmath-interpolated below e^40, asymptotic series above."""
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    lo = x < math.exp(40.0)
    if lo.any(): out[lo] = li_arr(x[lo])
    hi = ~lo
    if hi.any():
        l = np.log(x[hi])
        s = np.ones_like(l); term = np.ones_like(l)
        for k in range(1, 12):
            term = term*k/l; s = s + term
        out[hi] = x[hi]/l*s
    return out

def analytic_integral_gen(n, kernel, Mmax=2000, umin=1.0, umax=25.0, nu=3000,
                          respectPm=True, CB=None):
    mu, lpf, spf, PI, primes = sieve(Mmax)
    us = np.linspace(umin, umax, nu)
    tot = 0.0
    for m in range(1, Mmax+1):
        if mu[m] == 0: continue
        N = n/m
        if N < 4: continue
        lN = math.log(N)
        logt = lN/(1+us); logx = us*lN/(1+us)
        ok = logx > math.log(2.0)
        if respectPm and m > 1: ok &= (logt > math.log(float(lpf[m])))
        val = kernel(logx, logt, us)
        f = np.where(ok, val**2 * np.exp(np.minimum(logt,700))/(1+us), 0.0)
        tot += float(np.trapezoid(f, us)) if hasattr(np,'trapezoid') else float(np.trapz(f,us))
    return tot

def kern_lead(logx, logt, us):
    return -li_big(np.exp(np.minimum(logx,700)))*rho(us-1)

def make_kern_H(CB):
    def k(logx, logt, us):
        return Hgrid(CB, logx, logt)
    return k

# ================================================================ fixed-u window scaling test
def window_mass(n, u0, ratio=2.0):
    """sum over primes p in [n^{1/(1+u0)}, ratio*n^{1/(1+u0)}] of M(n/p,p)^2  (exact)."""
    P0 = n**(1.0/(1.0+u0)); P1 = ratio*P0
    xmax = int(n//max(2, int(P0)))+1
    mu, lpf, spf, PI, primes = sieve(max(xmax, int(P1)+10))
    ps = primes[(primes >= P0) & (primes <= P1)]
    tot = 0.0; vals = []
    for p in ps:
        x = int(n//p)
        keep = np.zeros(x+1, dtype=bool); keep[1] = True
        if x >= 2: keep[2:] = spf[2:x+1] > p
        M = int(np.sum(np.where(keep, mu[:x+1], 0).astype(np.int64)))
        tot += float(M)**2; vals.append((int(p), M, math.log(x)/math.log(p)))
    return tot, len(ps), vals

# ================================================================ fixed-u convergence of Thm A
def conv_fixed_u(u0, xs):
    from mpmath import li as mli
    print(f"# fixed u={u0}: exact M(x,x^(1/u)) vs -li(x)rho(u-1);  err ~ c/log y ?")
    print(f"{'x':>12} {'y':>7} {'u_eff':>7} {'M exact':>12} {'-li rho':>12} {'ratio':>7} "
          f"{'(ratio-1)*log y':>16}")
    for x in xs:
        mu, lpf, spf, PI, primes = sieve(x)
        y = int(round(x**(1.0/u0)))
        keep = np.zeros(x+1, dtype=bool); keep[1] = True
        keep[2:] = spf[2:x+1] > y
        M = int(np.sum(np.where(keep, mu[:x+1], 0).astype(np.int64)))
        ue = math.log(x)/math.log(y)
        pred = -float(mli(x))*rho(ue-1)
        r = M/pred
        print(f"{x:12d} {y:7d} {ue:7.4f} {M:12d} {pred:12.1f} {r:7.4f} {(r-1)*math.log(y):16.4f}")
