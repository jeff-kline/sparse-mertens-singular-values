"""Convergence of  M(x, x^{1/u}) log x / x  ->  -rho(u-1)."""
import numpy as np, math, sys
sys.path.insert(0, ".")
from checkA import rho

def mu_upto(X):
    isp = np.ones(X + 1, dtype=bool); isp[:2] = False
    for i in range(2, int(X**0.5) + 1):
        if isp[i]: isp[i*i::i] = False
    primes = np.nonzero(isp)[0]
    mu = np.ones(X + 1, dtype=np.int8); mu[0] = 0
    for p in primes:
        p = int(p)
        mu[p::p] = -mu[p::p]
        if p*p <= X: mu[p*p::p*p] = 0
    return mu, primes

def run(Xs, us):
    for X in Xs:
        mu, primes = mu_upto(X)
        muw = mu.astype(np.int64)
        print(f"\n X = {X:>12}   log X = {math.log(X):.3f}")
        print("     u       y      M(x,y)     M logx/x    -rho(u-1)    ratio")
        for uu in us:
            y = X ** (1.0 / uu)
            keep = np.ones(X + 1, dtype=bool); keep[0] = False
            for p in primes[primes <= y]:
                keep[int(p)::int(p)] = False
            keep[1] = True
            M = int(np.sum(np.where(keep, muw, 0)))
            val = M * math.log(X) / X
            tgt = -float(rho(uu - 1))
            print(f"  {uu:5.2f} {int(y):8d} {M:11d}   {val:10.5f}   {tgt:10.5f}  "
                  f"{val/tgt if tgt!=0 else float('nan'):8.3f}")

run([int(float(v)) for v in sys.argv[1:]], [1.5, 2.0, 2.5, 3.0, 4.0, 5.0])
