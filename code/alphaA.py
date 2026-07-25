"""For fixed alpha, T(alpha,n) = sum_{p in [n^a, 2n^a]} w_p^2 = sum |M(n/p,p)|^2.
Prediction from  M(x,x^{1/u}) ~ -rho(u-1) x/log x  with u=(1-a)/a:
   T ~ rho(1/a-2)^2 * n^{2-a} * (1/2) / (a (1-a)^2 L^3)     [times (1-1/2^?) factor]
Local exponent in n should tend to 2-a."""
import numpy as np, math, sys
sys.path.insert(0, ".")
from checkA import sieve, wvec, rho

for a in [float(v) for v in sys.argv[1].split(",")]:
    print(f"\n  alpha = {a}   u = {(1-a)/a:.3f}   rho(u-1) = {float(rho((1-2*a)/a)):.4e}   "
          f"target local exponent 2-a = {2-a:.3f}")
    print("        n     #primes        T          log T/log n   loc.exp   T/pred")
    prev = None
    for n in [int(float(v)) for v in sys.argv[2:]]:
        mu, lpf, spf, PI, primes = sieve(n)
        w, tag = wvec(n, cache=(mu, lpf, spf, PI, primes))
        L = math.log(n)
        lo, hi = n ** a, 2 * n ** a
        ps = primes[(primes >= lo) & (primes <= hi)].astype(np.int64)
        if len(ps) == 0:
            print(f"{n:9d}   none"); continue
        T = float(np.sum(w[ps - 1] ** 2))
        # prediction: integral over p in [n^a,2n^a] of rho(u-1)^2 (n/p)^2/log^2(n/p) dp/log p
        t = np.linspace(lo, hi, 20001)
        uu = np.log(n / t) / np.log(t)
        integ = (rho(uu - 1) * (n / t) / np.log(n / t)) ** 2 / np.log(t)
        pred = float(np.trapezoid(integ, t))
        ex = "" if prev is None else f"{math.log(T/prev[1])/math.log(n/prev[0]):.4f}"
        print(f"{n:9d} {len(ps):8d}  {T:14.4e}   {math.log(T)/L:8.4f}  {ex:>8}  "
              f"{T/pred:8.3f}")
        prev = (n, T)
