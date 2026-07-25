"""Dense spectral quantities for A_n and R_n (Section 6 of the paper).

The other scripts here are O(n log n) evaluators for ||w||; this one is the
dense O(n^3) counterpart that produces the singular-value, eigenvalue and
nilpotency numbers.  It is deliberately naive: every quantity is read off an
explicitly built matrix, so it cross-checks the closed forms rather than
reusing them.

Usage:
  spectra.py smax  N1 N2 ...   - sigma_max(R)/sqrt(n), |lambda_max(R)|, ratio vs sqrt(log n)
  spectra.py smin  N1 N2 ...   - sigma_min(A)*sqrt(n), ||A^{-1}||/sqrt(n),
                                 Cheon-Kim bound, nilpotency index of S
  spectra.py munorm N1 N2 ...  - ||mu_n||/sqrt(n) vs sqrt(6/pi^2)   (sieve only, no dense work)
  spectra.py sm N1 N2 ...      - Sherman-Morrison ratio sigma_min(R)||mu||||w||/|M(n)|
  spectra.py smscan LO HI STEP - the same ratio over a grid, reporting min/max
  spectra.py redheffer N1 ...  - non-normality ratio for Redheffer's own R_n,
                                 for comparison with the sparse matrix
"""
import numpy as np, math, sys

from checkA import sieve, wvec


# ---------------------------------------------------------------- matrices
def build(n):
    """Return (A, R, mu) with A = I + S, R = A + e_1 (1 - e_1)^T."""
    mu, lpf, _, _, _ = sieve(n)
    S = np.zeros((n, n))
    for i in range(2, n + 1):
        if mu[i] != 0:
            S[i - 1, i // lpf[i] - 1] = 1.0
    A = np.eye(n) + S
    R = A.copy()
    R[0, :] = 1.0
    return A, R, mu


def nilpotency_index(n):
    """Smallest r with S^r = 0, via depth in the forest j -> j/P(j).

    Computed from the forest directly, not by multiplying S, so it is an
    independent check on the depth argument in the proof.
    """
    mu, lpf, _, _, _ = sieve(n)
    depth = np.zeros(n + 1, dtype=np.int64)
    for i in range(2, n + 1):
        if mu[i] != 0:
            depth[i] = depth[i // lpf[i]] + 1
    return int(depth.max()) + 1


def mertens(n):
    mu, _, _, _, _ = sieve(n)
    return int(np.cumsum(mu[1:n + 1].astype(np.int64))[-1])


def munorm(n):
    """||mu_n|| = sqrt(#{i <= n squarefree})."""
    mu, _, _, _, _ = sieve(n)
    return math.sqrt(int(np.count_nonzero(mu[1:n + 1])))


# ---------------------------------------------------------------- reports
def smax(ns):
    print(f"{'n':>7} {'sigma_max(R)':>13} {'/sqrt(n)':>10} {'|lam_max(R)|':>13} "
          f"{'ratio':>8} {'sqrt(log n)':>11}")
    for n in ns:
        _, R, _ = build(n)
        s = np.linalg.svd(R, compute_uv=False)
        lam = np.abs(np.linalg.eigvals(R)).max()
        print(f"{n:>7} {s[0]:>13.6f} {s[0]/math.sqrt(n):>10.5f} {lam:>13.6f} "
              f"{s[0]/lam:>8.4f} {math.sqrt(math.log(n)):>11.4f}")


def smin(ns):
    print(f"{'n':>7} {'sigma_min(A)':>13} {'*sqrt(n)':>10} {'||Ainv||':>11} "
          f"{'/sqrt(n)':>10} {'Cheon-Kim':>10} {'sqrt(n)':>8} {'nilp':>5}")
    for n in ns:
        A, _, _ = build(n)
        s = np.linalg.svd(A, compute_uv=False)
        smn = s[-1]
        ck = 1.0 + math.sqrt(n - 1) / smn
        print(f"{n:>7} {smn:>13.6f} {smn*math.sqrt(n):>10.4f} {1/smn:>11.5f} "
              f"{1/(smn*math.sqrt(n)):>10.4f} {ck:>10.1f} {math.sqrt(n):>8.1f} "
              f"{nilpotency_index(n):>5}")


def munorm_table(ns):
    c = math.sqrt(6) / math.pi
    print(f"{'n':>10} {'||mu_n||':>13} {'/sqrt(n)':>10} {'sqrt(6/pi^2)':>13} {'diff':>10}")
    for n in ns:
        m = munorm(n)
        r = m / math.sqrt(n)
        print(f"{n:>10} {m:>13.4f} {r:>10.5f} {c:>13.6f} {r-c:>+10.6f}")


def sm_ratio(n, cache=None):
    """sigma_min(R) * ||mu|| * ||w|| / |M(n)|; None if M(n) = 0."""
    A, R, mu = build(n)
    M = int(np.cumsum(mu[1:n + 1].astype(np.int64))[-1])
    if M == 0:
        return None
    s = np.linalg.svd(R, compute_uv=False)[-1]
    w, _ = wvec(n)
    nm = math.sqrt(int(np.count_nonzero(mu[1:n + 1])))
    return s * nm * np.linalg.norm(w) / abs(M)


def sm(ns):
    print(f"{'n':>7} {'M(n)':>8} {'ratio':>10}")
    for n in ns:
        r = sm_ratio(n)
        print(f"{n:>7} {mertens(n):>8} " + ("  singular" if r is None else f"{r:>10.6f}"))


def smscan(lo, hi, step):
    vals = []
    print(f"{'n':>7} {'ratio':>10}")
    for n in range(lo, hi + 1, step):
        r = sm_ratio(n)
        if r is None:
            print(f"{n:>7}   M(n)=0, singular")
            continue
        vals.append((n, r))
        print(f"{n:>7} {r:>10.6f}")
    if vals:
        lo_n, lo_v = min(vals, key=lambda t: t[1])
        hi_n, hi_v = max(vals, key=lambda t: t[1])
        print(f"\n{len(vals)} usable points in [{lo},{hi}]")
        print(f"min {lo_v:.6f} at n={lo_n}    max {hi_v:.6f} at n={hi_n}")
        print(f"observed range [{lo_v:.4f}, {hi_v:.4f}]")


def redheffer_matrix(n):
    """Redheffer's R(i,j) = 1 iff j = 1 or i | j."""
    R = np.zeros((n, n))
    R[:, 0] = 1.0
    for i in range(1, n + 1):
        R[i - 1, i - 1::i] = 1.0
    return R


def redheffer_table(ns):
    """Sanity-checked against det = M(n) before the ratios are reported."""
    print(f"{'n':>7} {'det':>8} {'M(n)':>8} {'nnz/n':>7} {'smax':>10} "
          f"{'|lam_max|':>10} {'ratio':>8} {'sqrt(n)':>8}")
    for n in ns:
        R = redheffer_matrix(n)
        s = np.linalg.svd(R, compute_uv=False)[0]
        lam = np.abs(np.linalg.eigvals(R)).max()
        sg, ld = np.linalg.slogdet(R)
        det = int(round(sg * math.exp(ld)))
        print(f"{n:>7} {det:>8} {mertens(n):>8} {np.count_nonzero(R)/n:>7.3f} "
              f"{s:>10.4f} {lam:>10.4f} {s/lam:>8.4f} {math.sqrt(n):>8.2f}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "smax"
    args = [int(a) for a in sys.argv[2:]]
    if cmd == "smax":
        smax(args or [400, 800, 1600, 3200, 6400])
    elif cmd == "smin":
        smin(args or [500, 1000, 2000, 3000])
    elif cmd == "munorm":
        munorm_table(args or [10**5, 3 * 10**5, 10**6, 3 * 10**6, 10**7])
    elif cmd == "sm":
        sm(args or [500, 1000, 2000])
    elif cmd == "smscan":
        smscan(*(args or [200, 3200, 100]))
    elif cmd == "redheffer":
        redheffer_table(args or [400, 800, 1600, 3200])
    else:
        print(__doc__)
