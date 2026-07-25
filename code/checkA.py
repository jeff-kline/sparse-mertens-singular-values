"""Independent numerics for the ||w|| problem (method A: elementary).

Everything here is re-derived from scratch and cross-validated against a
direct dense linear solve at small n.

Usage:
  checkA.py verify           - dense solve vs closed form at n=500,1000,2000
  checkA.py norm N1 N2 ...   - ||w|| table
  checkA.py Fdelay           - solve the delay equation F'(u) = -F(u-1)/(u-1)
  checkA.py Fcheck X         - compare M(x,x^{1/u}) log x / x against F(u)
  checkA.py profile N1 ...   - mass profile in beta=log j/log n and u
  checkA.py regime N1 ...    - mass split by regime and by (alpha,gamma)
  checkA.py lower N1 ...     - the proven regime-B lower bound vs truth
"""
import numpy as np, math, sys


# ---------------------------------------------------------------- sieves
def sieve(n):
    """mu, lpf (largest prime factor, lpf[1]=1), spf (smallest, spf[1]=0),
       pi (prefix count of primes)."""
    isp = np.ones(n + 1, dtype=bool)
    isp[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if isp[i]:
            isp[i * i::i] = False
    primes = np.nonzero(isp)[0]
    mu = np.ones(n + 1, dtype=np.int8); mu[0] = 0
    lpf = np.ones(n + 1, dtype=np.int32)
    spf = np.zeros(n + 1, dtype=np.int32)
    for p in primes:
        p = int(p)
        lpf[p::p] = p
        mu[p::p] = -mu[p::p]
        if p * p <= n:
            mu[p * p::p * p] = 0
    for p in primes[::-1]:
        spf[int(p)::int(p)] = int(p)
    return mu, lpf, spf, np.cumsum(isp).astype(np.int64), primes


# ---------------------------------------------------------------- w vector
def wvec(n, cache=None):
    """w_j for j=1..n by the closed form + trichotomy.  Returns (w, tags)
       tags: 0 non-squarefree, 1 regime A, 2 regime B, 3 regime C."""
    mu, lpf, spf, PI, _ = cache if cache else sieve(n)
    j = np.arange(1, n + 1, dtype=np.int64)
    y = lpf[1:n + 1].astype(np.int64)
    x = n // j
    sqf = mu[1:n + 1] != 0
    w = np.zeros(n, dtype=np.float64)
    tag = np.zeros(n, dtype=np.int8)
    nsf = ~sqf
    w[nsf] = 1.0
    A = sqf & (y >= x)
    w[A] = 1.0; tag[A] = 1
    B = sqf & (~A) & (y * y >= x)
    w[B] = (1 - (PI[x[B]] - PI[y[B]])).astype(np.float64); tag[B] = 2
    C = sqf & (~A) & (y * y < x)
    tag[C] = 3
    cj, cy, cx = j[C], y[C], x[C]
    cw = np.zeros(len(cj))
    for yv in np.unique(cy):
        s = cy == yv
        xs = cx[s]; xmax = int(xs.max())
        keep = np.zeros(xmax + 1, dtype=bool); keep[1] = True
        if xmax >= 2:
            keep[2:] = spf[2:xmax + 1] > yv
        cs = np.cumsum(np.where(keep, mu[:xmax + 1], 0).astype(np.int64))
        v = cs[xs].astype(np.float64)
        cw[s] = v
    w[C] = cw
    w[0] -= 1.0                      # j = 1 : w_1 = M(n) - 1
    return w, tag


# ---------------------------------------------------------------- verify
def verify(n):
    mu, lpf, spf, PI, _ = sieve(n)
    S = np.zeros((n, n))
    for i in range(2, n + 1):
        if mu[i] != 0:
            S[i - 1, i // lpf[i] - 1] = 1.0
    Amat = np.eye(n) + S
    rhs = np.ones(n); rhs[0] = 0.0
    wd = np.linalg.solve(Amat.T, rhs)
    wc, _ = wvec(n)
    print(f"n={n:5d}  max|dense-closed| = {np.abs(wd-wc).max():.3e}   "
          f"||w||_dense={np.linalg.norm(wd):.6f}  ||w||_closed={np.linalg.norm(wc):.6f}")


# ---------------------------------------------------------------- delay eqn
def Fdelay(umax=12.0, h=0.0005):
    """F(u) = -1 on [1,2];  F(u) = -1 - int_1^{u-1} F(v) dv/v  for u>=2.
       Grid from u=0 with step h.  Returns (grid, F)."""
    N = int(umax / h) + 2
    u = np.arange(N) * h
    F = np.zeros(N)
    F[(u >= 1.0) & (u < 2.0)] = -1.0
    # I(t) = int_1^t F(v)dv/v accumulated on the grid
    I = np.zeros(N)
    i1 = int(round(1.0 / h))
    for i in range(1, N):
        if i > i1:
            I[i] = I[i - 1] + 0.5 * h * (F[i - 1] / u[i - 1] + F[i] / u[i])
        if u[i] >= 2.0:
            # F(u_i) needs I at u_i - 1
            k = i - i1
            F[i] = -1.0 - I[k]
            # redo the trapezoid for I[i] now that F[i] is known
            if i > i1:
                I[i] = I[i - 1] + 0.5 * h * (F[i - 1] / u[i - 1] + F[i] / u[i])
    return u, F


def Ffun():
    u, F = Fdelay()
    def f(t):
        return np.interp(t, u, F, left=0.0, right=0.0)
    return f


def Fcheck(X):
    """Direct M(x, x^{1/u}) log x / x  vs  F(u)."""
    mu, lpf, spf, PI, _ = sieve(X)
    f = Ffun()
    cmu = np.cumsum(mu[:X + 1].astype(np.int64))
    print(f"  X = {X}")
    print("     u        y     M(x,y)   M log x/x      F(u)      ratio")
    for uu in [1.5, 2.0, 2.5, 3.0, 3.5, 3.7183, 4.0, 4.5, 5.0, 6.0, 8.0]:
        y = int(X ** (1.0 / uu))
        if y < 2:
            continue
        keep = np.zeros(X + 1, dtype=bool); keep[1] = True
        keep[2:] = spf[2:X + 1] > y
        M = int(np.sum(np.where(keep, mu[:X + 1], 0).astype(np.int64)))
        val = M * math.log(X) / X
        Fu = f(uu)
        print(f"  {uu:6.3f} {y:9d} {M:10d}   {val:9.4f}   {Fu:9.4f}   "
              f"{(val/Fu if abs(Fu)>1e-6 else float('nan')):8.3f}")


# ---------------------------------------------------------------- profiles
def norm(ns):
    print("       n        ||w||    ||w||/n^(5/6)   *log^1.13   *log^1.5   Bshare  loc.exp")
    prev = None
    for n in ns:
        w, tag = wvec(n)
        W2 = float(np.sum(w * w)); W = math.sqrt(W2)
        L = math.log(n)
        Bs = float(np.sum(w[tag == 2] ** 2)) / W2
        r = W / n ** (5 / 6)
        ex = "" if prev is None else f"{math.log(W/prev[1])/math.log(n/prev[0]):.4f}"
        print(f"{n:9d} {W:12.1f}   {r:12.6f}  {r*L**1.13:10.4f} {r*L**1.5:10.4f}"
              f"  {Bs:.4f}  {ex:>8}")
        prev = (n, W)


def profile(ns, nb=40):
    for n in ns:
        mu, lpf, spf, PI, primes = sieve(n)
        w, tag = wvec(n, cache=(mu, lpf, spf, PI, primes))
        j = np.arange(1, n + 1, dtype=np.int64)
        y = lpf[1:n + 1].astype(np.int64)
        x = n // j
        L = math.log(n)
        w2 = w * w
        W2 = w2.sum()
        beta = np.log(np.maximum(j, 2)) / L
        alpha = np.log(np.maximum(y, 2)) / L
        uu = np.log(np.maximum(x, 2)) / np.log(np.maximum(y, 2))
        uu = np.where(y <= 1, 0.0, uu)
        print(f"\nn={n}  L={L:.3f}  ||w||={math.sqrt(W2):.1f}")
        print(f"  mass-mean beta  = {float((beta*w2).sum()/W2):.4f}")
        print(f"  mass-mean alpha = {float((alpha*w2).sum()/W2):.4f}")
        sel = (y > 1)
        print(f"  mass-mean u     = {float((uu[sel]*w2[sel]).sum()/w2[sel].sum()):.4f}")
        # histogram of mass in u
        ue = np.arange(0, 8.01, 0.25)
        hu = np.histogram(uu[sel], bins=ue, weights=w2[sel])[0] / W2
        print("  u-histogram (bin left edge : share):")
        for k in range(len(ue) - 1):
            if hu[k] > 0.002:
                print(f"     u in [{ue[k]:.2f},{ue[k+1]:.2f})  {hu[k]:.4f}")
        # histogram in alpha (=log P(j)/log n)
        ae = np.arange(0, 0.55, 0.025)
        ha = np.histogram(alpha[sel], bins=ae, weights=w2[sel])[0] / W2
        print("  alpha-histogram:")
        for k in range(len(ae) - 1):
            if ha[k] > 0.002:
                print(f"     a in [{ae[k]:.3f},{ae[k+1]:.3f})  {ha[k]:.4f}")
        # how much of the mass comes from j=prime, j=p*m with m small
        mvals = np.where(y > 1, j // np.maximum(y, 1), 0)
        for mm in [1, 2, 3, 4, 5, 6, 7]:
            s = mvals == mm
            print(f"   share of mass with j = {mm}*P(j): {float(w2[s].sum()/W2):.4f}")
        s = (mvals >= 8)
        print(f"   share of mass with j = m*P(j), m>=8: {float(w2[s].sum()/W2):.4f}")


def regime(ns):
    for n in ns:
        w, tag = wvec(n)
        W2 = float(np.sum(w * w))
        print(f"n={n}: ||w||={math.sqrt(W2):.1f}")
        for t, nm in [(0, "non-sqfree"), (1, "A"), (2, "B"), (3, "C")]:
            s = tag == t
            print(f"   {nm:11s} count={int(s.sum()):9d}  massshare={float((w[s]**2).sum()/W2):.4f}")


# --------------------------------------------------- proven lower bound test
def lower(ns):
    """Compare the regime-B prime-only sum  S1 = sum_{n^{1/3}<=p<=n^{1/2}} (pi(n/p)-pi(p)-1)^2
       against ||w||^2 and against the asymptotic (27/4) n^{5/3}/log^3 n."""
    print("       n      ||w||      S1^{1/2}   S1/||w||^2   asym(27/4)n^{5/3}/L^3  ratio")
    for n in ns:
        mu, lpf, spf, PI, primes = sieve(n)
        w, tag = wvec(n, cache=(mu, lpf, spf, PI, primes))
        W2 = float(np.sum(w * w))
        L = math.log(n)
        lo = int(n ** (1 / 3)); hi = int(n ** 0.5)
        ps = primes[(primes >= lo) & (primes <= hi)].astype(np.int64)
        v = (PI[n // ps] - PI[ps] - 1).astype(np.float64)
        S1 = float(np.sum(v * v))
        asym = 6.75 * n ** (5 / 3) / L ** 3
        print(f"{n:9d} {math.sqrt(W2):11.1f} {math.sqrt(S1):11.1f}   {S1/W2:.4f}"
              f"      {math.sqrt(asym):14.1f}     {S1/asym:.4f}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    args = [int(float(v)) for v in sys.argv[2:]]
    if cmd == "verify":
        for n in (args or [500, 1000, 2000]):
            verify(n)
    elif cmd == "norm":
        norm(args)
    elif cmd == "Fdelay":
        u, F = Fdelay()
        for t in np.arange(1.0, 10.01, 0.25):
            print(f"  F({t:5.2f}) = {np.interp(t,u,F):+.6f}")
    elif cmd == "Fcheck":
        for X in args:
            Fcheck(X)
    elif cmd == "profile":
        profile(args)
    elif cmd == "regime":
        regime(args)
    elif cmd == "lower":
        lower(args)


# ================================================================
#  Dickman rho, the model  M(x, x^{1/u}) ~ -rho(u-1) x/log x,
#  and the saddle-point analysis of the resulting sum.
# ================================================================
def dickman(vmax=30.0, h=0.0005):
    N = int(vmax / h) + 2
    v = np.arange(N) * h
    r = np.ones(N)
    # rho(v)=1 on [0,1];  v rho'(v) = -rho(v-1)  =>  rho(v) = rho(k) - int_k^v rho(t-1)dt/t
    i1 = int(round(1.0 / h))
    for i in range(i1 + 1, N):
        # trapezoid for int_{v_{i-1}}^{v_i} rho(t-1) dt/t
        a = r[i - 1 - i1] / v[i - 1]
        b = r[i - i1] / v[i]
        r[i] = r[i - 1] - 0.5 * h * (a + b)
    r = np.maximum(r, 0.0)
    return v, r


_VG, _RG = dickman()
def rho(t):
    return np.interp(t, _VG, _RG, left=1.0, right=0.0)


def model(ns):
    """Compare  sum_j [rho(u-1)*(pi(x)-pi(y)-1)]^2  to ||w||^2, and give
       per-u-bin ratio of true RMS |w_j| to the model."""
    for n in ns:
        mu, lpf, spf, PI, primes = sieve(n)
        w, tag = wvec(n, cache=(mu, lpf, spf, PI, primes))
        j = np.arange(1, n + 1, dtype=np.int64)
        y = lpf[1:n + 1].astype(np.int64)
        x = n // j
        BC = (tag == 2) | (tag == 3)
        xb, yb, wb = x[BC], y[BC], w[BC]
        uu = np.log(xb) / np.log(yb)
        base = (PI[xb] - PI[yb] - 1).astype(np.float64)
        mod = rho(uu - 1.0) * base
        W2 = float((w * w).sum())
        print(f"\nn={n}  ||w||^2={W2:.4g}   B+C share={float((wb**2).sum())/W2:.4f}")
        print(f"   sum model^2 / ||w||^2 = {float((mod**2).sum())/W2:.4f}")
        print("   u-bin   count      RMS|w|/RMS|base|    rho(u-1)   ratio(true/model)")
        for lo in np.arange(1.0, 6.0, 0.5):
            s = (uu >= lo) & (uu < lo + 0.5)
            if s.sum() == 0:
                continue
            r1 = math.sqrt(float((wb[s] ** 2).sum()) / float((base[s] ** 2).sum()))
            r2 = float(rho(lo + 0.25 - 1.0))
            print(f"   [{lo:.1f},{lo+0.5:.1f})  {int(s.sum()):8d}   {r1:12.4f}      "
                  f"{r2:8.4f}   {r1/r2 if r2>0 else float('nan'):8.3f}")
        # mean alpha restricted to j prime
        isprime = np.zeros(n + 1, dtype=bool); isprime[primes] = True
        pr = BC & isprime[1:n + 1]
        al = np.log(y[pr]) / math.log(n)
        wp2 = w[pr] ** 2
        print(f"   j prime: mass share {float(wp2.sum())/W2:.4f}   "
              f"mass-mean alpha {float((al*wp2).sum()/wp2.sum()):.4f}")


def saddle(Ls=None):
    """J(L) = int_0^{1/2} rho((1-2a)/a)^2 e^{-aL} / (a (1-a)^2) da
       Model:  sum over j=p prime of w_p^2  ~=  n^2 J(L)/L^2.
       Reports mean alpha = -dlogJ/dL and the effective exponent of
       ||w||_prime = n sqrt(J(L))/L  written as n^{5/6} L^{-k}."""
    if Ls is None:
        Ls = [8, 10, 11.51, 13.82, 16.12, 18, 20, 25, 30, 40, 60, 100, 200, 400, 1000, 1e4]
    a = np.linspace(1e-6, 0.5, 400001)
    g = rho((1 - 2 * a) / a) ** 2 / (a * (1 - a) ** 2)
    print("      L        J(L)        mean alpha    d log||w||/d log n     k in n^{5/6}L^{-k}")
    prev = None
    for L in Ls:
        w_ = g * np.exp(-a * L)
        J = np.trapezoid(w_, a)
        ma = float(np.trapezoid(a * w_, a) / J)
        # ||w||^2 ~ n^2 J/L^2 -> d log ||w|| / d log n = 1 - ma/2 + ...
        slope = 1 - ma / 2
        k = (5 / 6 - slope) * math.log(n_dummy) if False else None
        print(f"  {L:8.2f}  {J:12.4e}   {ma:10.5f}       {slope:10.5f}")
        prev = (L, J)
    # effective log-power: fit ||w|| = C n^{5/6} L^{-k} between consecutive L
    print("\n  effective k (from consecutive L, using n=e^L):")
    Ls2 = [11.5129, 12.6115, 13.8155, 14.9141, 16.1181, 18.0, 20.0, 25.0, 30.0, 40.0, 60.0]
    vals = []
    for L in Ls2:
        J = np.trapezoid(g * np.exp(-a * L), a)
        vals.append((L, math.exp(L) * math.sqrt(J) / L))
    for i in range(1, len(vals)):
        L0, W0 = vals[i - 1]; L1, W1 = vals[i]
        # W = C e^{5L/6} L^{-k}
        k = -(math.log(W1 / W0) - (5 / 6) * (L1 - L0)) / math.log(L1 / L0)
        print(f"    L {L0:6.2f} -> {L1:6.2f} :  k = {k:8.4f}   "
              f"(local exp d log W/d log n = {1 + math.log(W1/W0)/(L1-L0) - 1:.4f})")


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] in ("model", "saddle", "rho"):
    if sys.argv[1] == "model":
        model([int(float(v)) for v in sys.argv[2:]])
    elif sys.argv[1] == "saddle":
        n_dummy = 1
        saddle()
    else:
        for t in np.arange(0.5, 8.01, 0.5):
            print(f"  rho({t:4.1f}) = {float(rho(t)):.6e}")
