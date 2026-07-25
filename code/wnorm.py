"""||w|| for Kline's sparse matrix, via the verified closed form
   w_j = 1                (j not squarefree)
   w_j = M(n/j, P(j))     (j squarefree; minus 1 at j=1)
with the exact evaluations in regimes A (P(j)>=n/j) and B (sqrt(n/j)<=P(j)<n/j).
Only regime C needs a sieve, and there are few such j."""
import numpy as np, math, sys, time

def sieve(n):
    mu = np.ones(n+1, dtype=np.int8); mu[0] = 0
    lpf = np.ones(n+1, dtype=np.int32)
    isp = np.ones(n+1, dtype=bool); isp[:2] = False
    for i in range(2, int(n**0.5)+1):
        if isp[i]: isp[i*i::i] = False
    primes = np.nonzero(isp)[0]
    for p in primes:                      # increasing p -> last write is largest prime factor
        lpf[p::p] = p
        mu[p::p] = -mu[p::p]
        pp = int(p)*int(p)
        if pp <= n: mu[pp::pp] = 0
    spf = np.zeros(n+1, dtype=np.int32)
    for p in primes[::-1]:                # decreasing p -> last write is smallest prime factor
        spf[p::p] = p
    return mu, lpf, spf, np.cumsum(isp).astype(np.int64)

def wnorm(n, verbose=False):
    t0 = time.time()
    mu, lpf, spf, PI = sieve(n)
    j = np.arange(1, n+1, dtype=np.int64)
    y = lpf[1:n+1].astype(np.int64); y[0] = 1          # P(1):=1
    x = n // j
    sqf = mu[1:n+1] != 0
    nsf = ~sqf; nsf[0] = False
    total = float(np.count_nonzero(nsf))               # w_j = 1 on non-squarefree j
    A = sqf & (y >= x)
    total += float(np.count_nonzero(A))                # w_j = 1
    B = sqf & (~A) & (y*y >= x)
    wB = 1 - (PI[x[B]] - PI[y[B]])
    total += float(np.sum(wB.astype(np.float64)**2))
    C = sqf & (~A) & (y*y < x)
    cj, cy, cx = j[C], y[C], x[C]
    if verbose: print(f"   regimes: nsf={np.count_nonzero(nsf)} A={np.count_nonzero(A)} "
                      f"B={np.count_nonzero(B)} C={np.count_nonzero(C)}")
    for yv in np.unique(cy):
        sel = cy == yv
        xs, js = cx[sel], cj[sel]
        xmax = int(xs.max())
        keep = np.zeros(xmax+1, dtype=bool); keep[1] = True
        if xmax >= 2: keep[2:] = spf[2:xmax+1] > yv
        cs = np.cumsum(np.where(keep, mu[:xmax+1], 0).astype(np.int64))
        vals = cs[xs].astype(np.float64)
        vals[js == 1] -= 1.0
        total += float(np.sum(vals**2))
    return math.sqrt(total), time.time()-t0

if __name__ == "__main__":
    print("        n         ||w||     ||w||/n     ||w||*log n/n   ||w||*log^2n/n   local exponent   secs")
    prev = None
    for n in [int(v) for v in sys.argv[1:]]:
        W, el = wnorm(n)
        L = math.log(n)
        ex = "" if prev is None else f"{math.log(W/prev[1])/math.log(n/prev[0]):.4f}"
        print(f"{n:10d}  {W:12.1f}  {W/n:.6f}    {W*L/n:9.4f}      {W*L*L/n:9.4f}      {ex:>8}       {el:5.1f}")
        prev = (n, W)
