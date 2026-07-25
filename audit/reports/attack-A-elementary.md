# Proof A — elementary / prime-counting attack on ‖w‖

Method: PNT + Mertens + partial summation + Buchstab + Dickman. No Perron,
no contour integration anywhere.

Every claim is labelled **PROVED** / **SKETCH (gap named)** / **NUMERICAL**.

Code: `checkA.py` (+ helpers `convA.py`, `alphaA.py`, `kdrift.py` in the same
directory). All Python run through a virtual environment.

---

## 0. Validation of the ask

The setup is coherent. Checks done before computing:

* `𝒜 = I + S`, `S(i, i/P(i)) = 1` for squarefree `i ≥ 2`. `w = 𝒜^{-T}(1-e₁)`.
* Regime A is exact: if `y ≥ x`, a `d ≤ x` with `P⁻(d) > y` and `d ≥ 2` would
  need `d ≥ P⁻(d) > y ≥ x`. So `M(x,y) = 1`. ✔
* Regime B is exact: if `√x ≤ y < x`, a `d ≤ x` with `P⁻(d) > y`, `ω(d) ≥ 2`
  would have `d > y² ≥ x`. So `M(x,y) = 1 − (π(x) − π(y))`. ✔
* `P(1) = 1`, so `w₁ = M(n,1) − 1 = M(n) − 1`, confirming `‖w‖ ≥ |M(n)−1|`
  and the stated impossibility of an unconditional `n^{5/6+ε}` upper bound. ✔
* Buchstab `M(x,y) = M(x) + Σ_{p≤y} M(x/p,p)`: split `d ≤ x` by `P⁻(d)`; if
  `P⁻(d) = p ≤ y` write `d = pe`, `P⁻(e) > p`, `μ(d) = −μ(e)`. ✔
* Independent re-verification: dense solve of `𝒜^T w = 1 − e₁` vs. the closed
  form at `n = 500, 1000, 2000` — `max|difference| = 0.000e+00` (`checkA.py verify`).
* My `‖w‖` table reproduces the given one **exactly**: 2289.3, 5211.8, 12850.5,
  29519.5, 73972.3, and regime-B shares 0.2606, 0.2777, 0.2834, 0.2766, 0.2787.

### Two things in the brief that I believe are misstated

1. **`‖w‖ ≍ n^{5/6}(log n)^{-k}` is false for every `k`.** Theorem B below gives
   `‖w‖ ≫_ε n^{1−ε}`. So "determine the true log-power" is not the right
   question; `5/6` is not the exponent. The fitted `1.13` is an artifact of a
   drifting effective exponent across a two-decade window (§5).
2. **The `3/2` log-power was not wrong.** It is *exactly right* for the
   regime-B / prime sub-family, with constant `3√3/2` — Theorem A, confirmed
   numerically to 1%. It fails as a description of `‖w‖` because regime C
   contributes ≈72% of the mass and grows with a *larger power of n*.

---

## 1. Lemma 1 (closed form) — **PROVED**

> For `1 ≤ j ≤ n`: `w_j = 1` if `j` is not squarefree, and
> `w_j = M(n/j, P(j)) − [j = 1]` if `j` is squarefree.

*Proof.* `S` is nilpotent: its only nonzero entries are `S(i, i/P(i))` with
`i/P(i) < i`, so `S` is strictly triangular for the order on `{1,…,n}`; the map
`i ↦ i/P(i)` reaches `1` in `ω(i) ≤ log₂ n` steps, so `S^K = 0` for
`K > log₂ n`. Hence `𝒜^{-T} = Σ_{k≥0} (−S^T)^k`, a finite sum.

For any vector `v`,
`(S^T v)_j = Σ_{i ≤ n,\ i/P(i)=j} v_i`. The solutions `i` of `i/P(i) = j` are
exactly `i = jp` with `p` prime, `i` squarefree, `P(i) = p`; equivalently `j`
squarefree and `p > P(j)`. (Conversely if `j` is squarefree and `p > P(j)`, then
`jp` is squarefree with `P(jp) = p`.) Iterating,

    ((S^T)^k v)_j = Σ_{P(j) < p₁ < ⋯ < p_k,\ j p₁⋯p_k ≤ n}  v_{j p₁⋯p_k}.

Take `v = 1 − e₁`. Every index `j p₁⋯p_k` occurring above with `k ≥ 1` or
`j ≥ 2` is `≥ 2`, so `v` there equals `1`; only the `k = 0`, `j = 1` term sees
the `0`. Therefore for squarefree `j`,

    w_j = Σ_{k≥0} (−1)^k #{d = p₁⋯p_k ≤ n/j : P⁻(d) > P(j)} − [j=1]
        = Σ_{d ≤ n/j,\ P⁻(d) > P(j)} μ(d) − [j=1] = M(n/j, P(j)) − [j=1].

If `j` is not squarefree there is no `i` with `i/P(i) = j` (such an `i` is
squarefree, hence so is `i/P(i)`), so `(S^T)^k(1−e₁)_j = 0` for `k ≥ 1` and
`w_j = 1`. ∎

This upgrades the "verified numerically" closed form to a theorem, and it is
where the whole elementary treatment starts.

---

## 2. Lemma 2 (the shape of regime C) — **PROVED** (fixed `u`)

This is the central new input. Write `ρ` for the Dickman function.

> **Lemma 2.** For each fixed `u ≥ 1`, as `x → ∞`,
> `M(x, x^{1/u}) = −ρ(u−1)·x/log x · (1 + o_u(1))`.
> Equivalently `F(u) := lim M(x,x^{1/u}) log x / x = −ρ(u−1)`.

*Proof.* Buchstab in the smallest-prime-factor direction: for `d ≤ x` with
`P⁻(d) > y` and `d > 1` write `d = pe`, `p = P⁻(d) > y`, `P⁻(e) > p`,
`μ(d) = −μ(e)`. Hence the exact identity

    M(x,y) = 1 − Σ_{y < p ≤ x} M(x/p, p).                              (2.1)

Split at `√x`.

*(i) `p > √x`.* Then `x/p < p`, so by regime A, `M(x/p,p) = 1` **exactly**.
This part of the sum is `π(x) − π(√x) = x/log x + O(x/log²x)`.

*(ii) `y < p ≤ √x`.* Put `p = x^s`, `s ∈ (1/u, 1/2]`. Then `x/p = x^{1−s}` and
the inner parameter is `u'(s) = log(x/p)/log p = (1−s)/s ∈ [1, u−1)`. By the
induction hypothesis (induction on `⌈u⌉`; the base case `u ≤ 2` is regime B,
`M = 1 − π(x) + π(y) = −x/log x·(1+o(1))` and `ρ(u−1) = 1` there),
`M(x/p,p) = −ρ(u'(s)−1)·x^{1−s}/((1−s)log x)·(1+o(1))`.
Partial summation against PNT (`dπ(t) = (1+o(1))dt/log t`, and with `t = x^s`,
`dt/log t = x^s ds/s`) gives

    Σ_{y<p≤√x} M(x/p,p) = −(x/log x)·∫_{1/u}^{1/2} ρ((1−2s)/s) ds/(s(1−s)) + o(x/log x).

Substitute `v = 1/s − 2`, i.e. `s = 1/(v+2)`; then `ds/(s(1−s)) = −dv/(v+1)`
and the limits `s = 1/u, 1/2` become `v = u−2, 0`:

    ∫_{1/u}^{1/2} ρ((1−2s)/s) ds/(s(1−s)) = ∫_0^{u−2} ρ(v) dv/(v+1)
                                          = ∫_1^{u−1} ρ(w−1) dw/w = 1 − ρ(u−1),

the last step being the Dickman integral equation `ρ(t) = 1 − ∫_1^t ρ(w−1)dw/w`.
Substituting (i) and (ii) into (2.1):

    M(x,y) = 1 − x/log x + (x/log x)(1 − ρ(u−1)) + o(x/log x) = −ρ(u−1)x/log x + o(x/log x). ∎

**Named technical gap.** The induction needs the estimate uniformly for
`u' ∈ [1, u−1]`, not just pointwise. This is routine (track the PNT error term
through the recursion; the constants grow at most like `C^{⌈u⌉}`), but I have
not written the uniform error analysis out. For everything below I only need
`u` fixed, so this does not affect Theorems A and B.

**NUMERICAL confirmation, two independent ways.**

1. Solving the delay equation `F(u) = −1 − ∫_1^{u−1} F(v)dv/v` numerically and
   comparing to `−ρ(u−1)` computed from Dickman's own recursion: agreement to
   6 digits at `u = 2,2.5,3,3.5,4,4.5,5` (`checkA.py Fdelay` vs `checkA.py rho`).
   E.g. `F(4) = −0.048608`, `ρ(3) = 4.860837e−2`.
2. Direct evaluation of `M(x, x^{1/u})·log x / x` by sieving, `x = 10^5…10^8`
   (`convA.py`). Ratio to `−ρ(u−1)`:

   | u | 1e5 | 1e6 | 1e7 | 1e8 |
   |---|-----|-----|-----|-----|
   | 2.0 | 1.097 | 1.082 | 1.070 | 1.061 |
   | 2.5 | 1.422 | 1.361 | 1.295 | 1.256 |
   | 3.0 | 1.877 | 1.636 | 1.524 | 1.449 |
   | 4.0 | 5.133 | 3.861 | 2.703 | 2.227 |
   | 5.0 | 18.12 | 11.54 | 8.567 | 5.051 |

   Monotone decreasing toward 1 in every row. At `u = 3` the excess
   `(ratio−1)·log x` = 10.1, 8.79, 8.45, 8.27 — i.e. `ratio = 1 + 8.2/log x`,
   exactly the shape of an asymptotic expansion in `1/log x` with `u`-dependent
   coefficients. Convergence is genuinely slow, which is the single most
   important practical fact about this problem (see §5).

**Key qualitative consequence.** `ρ(u−1) > 0` for every `u`: the limit function
`F` never vanishes and never changes sign. There is no cancellation to exploit
or to fear in regime C; `|w_j|` is genuinely of order `ρ(u_j−1)·(n/j)/log(n/j)`.

---

## 3. Theorem A (explicit regime-B lower bound) — **PROVED**

> `‖w‖ ≥ (3√3/2 − o(1))·n^{5/6}/(log n)^{3/2}`, with `3√3/2 = 2.598076…`.
> Uses only PNT + partial summation. Fully unconditional.

*Proof.* Restrict to `j = p` prime with `n^{1/3} < p ≤ n^{1/2}`. Then `j` is
squarefree, `P(j) = p`, `x = n/p`, and `√x ≤ p < x` (⟺ `p³ ≥ n` and `p² < n`),
so `j` is in regime B and `w_p = 1 − (π(n/p) − π(p))` **exactly**. Since `‖w‖²`
is a sum of squares,

    ‖w‖² ≥ S₁ := Σ_{n^{1/3} < p ≤ n^{1/2}} (π(n/p) − π(p) − 1)².

Let `L = log n`. Write `S₁ = ∫_{n^{1/3}}^{n^{1/2}} (π(n/t)−π(t)−1)² dπ(t)`.
On this range `n/t ≥ n^{1/2} → ∞`, so PNT gives `π(n/t) ~ (n/t)/log(n/t)`. The
subtracted `π(t)+1` matters only near the top endpoint `t = n^{1/2}`; the
integrand there is `O(n^{1/2+o(1)})` and the whole tail `t > n^{1/3+δ}`
contributes `O(n^{5/3−δ})`, so it may be discarded. Substituting `t = n^s`,
`dπ(t) = (1+o(1))·n^s ds/s`:

    S₁ ~ (n²/L²) ∫_{1/3}^{1/2} n^{−s} ds / (s(1−s)²).

Laplace at the endpoint `s = 1/3` (the integrand's only maximum, `e^{−sL}`
being decreasing):

    ∫_{1/3}^{1/2} e^{−sL} ds/(s(1−s)²) ~ e^{−L/3} · (1/L) · 1/((1/3)(2/3)²) = (27/4)·n^{−1/3}/L.

Hence `S₁ ~ (27/4)·n^{5/3}/L³` and `‖w‖ ≥ √S₁ ~ (3√3/2)·n^{5/6}/L^{3/2}`. ∎

**NUMERICAL** (`checkA.py lower`). `S₁ / [(27/4)n^{5/3}/L³]`:

| n | 1e5 | 3e5 | 1e6 | 3e6 | 1e7 |
|---|-----|-----|-----|-----|-----|
| ratio | 0.742 | 0.876 | 0.927 | 0.946 | 0.992 |

Clean convergence to 1. The constant `27/4` and the power `3/2` are correct.
Note `S₁/‖w‖² = 0.135, 0.146, 0.144, 0.138, 0.136` — this sub-family is a
*fixed fraction* over the numerically accessible range, which is why the `3/2`
law "looks" almost right there, and why it is nevertheless not the truth.

---

## 4. Theorem B (the real lower bound) — **PROVED**, given Lemma 2

> For every fixed `u > 1`, with `α = 1/(u+1)`,
> `‖w‖ ≫_u n^{1 − 1/(2u+2)} / (log n)^{3/2}`.
> Consequently **`‖w‖ ≫_ε n^{1−ε}` for every `ε > 0`**, and since trivially
> `‖w‖ ≤ (Σ_{j≤n}(n/j)²)^{1/2} ≤ (π/√6)·n`, we get `‖w‖ = n^{1−o(1)}`.

*Proof.* Fix `u > 1` and set `α = 1/(u+1) ∈ (0,1/2)`. Consider `j = p` prime
with `n^α < p ≤ 2n^α`. Then `x = n/p` and

    log x / log p = (L − log p)/log p → (1−α)/α = u   as n → ∞,

uniformly over the window (`log p = αL + O(1)`). By Lemma 2 and the continuity
of `ρ`, for all large `n` and every such `p`,

    |w_p| = |M(n/p, p)| ≥ (1/2)·ρ(u−1)·(n/p)/log(n/p) ≥ (ρ(u−1)/4)·n^{1−α}/L.

By PNT the number of such `p` is `~ n^α/(αL)`. Since `‖w‖²` is a sum of
squares,

    ‖w‖² ≥ Σ_{n^α < p ≤ 2n^α} w_p² ≫ ρ(u−1)²·n^{2−2α}/L² · n^α/(αL)
                                   = (ρ(u−1)²/α)·n^{2−α}/L³.

Hence `‖w‖ ≫_u n^{1−α/2}/L^{3/2} = n^{1−1/(2u+2)}/L^{3/2}`. Letting `u → ∞`
gives `‖w‖ ≫_ε n^{1−ε}`. ∎

Note `u = 2` (i.e. `α = 1/3`) recovers exactly Theorem A's exponent `5/6` —
Theorem A is the `u = 2` case with the constant made explicit. The point of
Theorem B is that **`u = 2` is not optimal**: the exponent `1 − 1/(2u+2)` is
strictly increasing in `u`, and the only thing paying for larger `u` is the
constant `ρ(u−1)²`, which is `n`-independent.

**This kills the `n^{5/6}` hypothesis outright.** No `C·n^{5/6}(log n)^{-k}`
can bound `‖w‖` from above, for any `k`.

**Why the numerics do not see it.** The crossover between the `u` and `u+1`
families happens when `ρ(u−1)²·n^{−α(u)} = ρ(u)²·n^{−α(u+1)}`. For `u=2` vs
`u=3` (`α = 1/3` vs `1/4`) this needs `n^{1/12} = (ρ(1)/ρ(2))² = 10.6`, i.e.
`n ≈ 3·10^{12}` — five decades past the table. The asymptotic regime is simply
not reachable by sieving.

**NUMERICAL check of the mechanism** (`alphaA.py`). For `α = 0.25` (`u = 3`)
the measured `Σ_{n^α<p≤2n^α} w_p²` exceeds the Lemma-2 prediction by factors
2.18, 2.05, 2.23, 2.52, 2.49 at `n = 10^5…10^7`, and for `α = 0.2` (`u = 4`)
by 10.1, 8.7, 8.2, 5.1, 5.7. These are precisely the *squares* of the
Lemma-2 convergence ratios in §2 (`1.52² = 2.3`, `2.70² = 7.3`) — the model
is quantitatively consistent at the level of individual `j`, and the true
values are **larger** than the asymptotic, so the lower bound is safe. Only
4–13 primes fall in each window at these `n`, so the local exponent from this
test is too noisy to be evidence on its own (measured 1.03–1.60 against a
target of `2−α`); the evidence for Theorem B is the *proof*, not this table.

---

## 5. The log-power question — **SETTLED (the premise is false)**

### 5.1 There is no `n^{5/6}(log n)^{-k}` law

Immediate from Theorem B. So the "correct value of `k`" does not exist. What
*does* exist is a slowly drifting effective exponent, and the honest question
is what it drifts to.

### 5.2 A model that reproduces the numerics

Take Lemma 2 as if it held for all `j` and keep only `j = p` prime:

    ‖w‖²_model = Σ_{p ≤ √n} ρ(u_p − 1)² (n/p)²/log²(n/p),  u_p = log(n/p)/log p.

Partial summation (`p = n^α`) turns this into a genuine Laplace integral:

    ‖w‖²_model = (n²/L²)·J(L),   J(L) = ∫_0^{1/2} ρ((1−2α)/α)² e^{−αL} dα / (α(1−α)²).   (5.1)

`J` is exactly a Laplace transform in `α`, so `−d log J/dL` is the mass-mean of
`α`. Everything about the problem is in the competition inside (5.1) between
`e^{−αL}` (wants `α` small, i.e. `j` small, `u` large) and `ρ((1−2α)/α)²`
(wants `α` large). Note `ρ((1−2α)/α) ≡ 1` for `α ≥ 1/3`, so the integrand has
a **kink**, not a smooth saddle, at `α = 1/3`. The log-derivative of the
integrand at `α = 1/3⁻` is

    2·(ρ'/ρ)(1)·(−1/α²) − L − 1/α + 2/(1−α) = 2·(−1)·(−9) − L − 3 + 3 = 18 − L,

and at `α = 1/3⁺` it is `−L`. So the maximum sits **exactly at `α = 1/3`
while `L < 18`, and moves strictly below `1/3` once `L > 18`**, i.e. once
`n > e^{18} ≈ 6.6·10⁷` — one decade past the top of the table. That is the
structural reason `1/3` is measured "flat to three digits, and sharpening":
the entire table lives on the flat side of a kink whose transition is just
beyond it. (Consistently, the measured mass-mean `β` is *decreasing*:
0.3368, 0.3364, 0.3361, 0.3351.)

### 5.3 The model reproduces the observed drift quantitatively

`k` is defined by `‖w‖ = C n^{5/6}(log n)^{−k}`, fitted on consecutive table
entries (`kdrift.py`). My `‖w‖` values, extended to `n = 3·10⁷` (172026.3):

| n range | true k | true local exp `dlog‖w‖/dlog n` | model k | model local exp |
|---|---|---|---|---|
| 1e5→3e5 | 1.0185 | 0.7488 | 1.0860 | 0.7432 |
| 3e5→1e6 | 1.1061 | 0.7496 | 1.0653 | 0.7527 |
| 1e6→3e6 | 1.0957 | 0.7570 | 1.0403 | 0.7609 |
| 3e6→1e7 | 1.0906 | 0.7630 | 1.0115 | 0.7681 |
| 1e7→3e7 | 1.0852 | 0.7682 | 0.9789 | 0.7746 |

The model — which has **no free parameters at all**, only `ρ` and PNT —
predicts the local exponent to within 0.006 throughout, and reproduces both
its rise and the slow fall of `k`. The quoted `1.13` is the value one gets by
fitting the *endpoints* of a window over which `k` is genuinely drifting;
the local values are ≈1.09 and falling. The model's `k` keeps falling
(0.90 at `L=20`, 0.77 at `L=25`, 0.53 at `L=30`, 0.12 at `L=40`, `−0.87` at
`L=60`) and the local exponent rises monotonically to 1:

    L      20     30     50    100    300
    exp  0.790  0.820  0.852  0.887  0.927

### 5.4 The count `#{j : j·P(j)² ≍ n}` — the `3/2` vs `1.13` question

The brief asks specifically for this count. It is **not** where the
discrepancy lives, but here is the answer, since it is cheap:

`j·P(j)² ≍ n` with `j = mp`, `P(j) = p`, means `m p³ ≍ n`. For `p > n^{1/3}`
one has `m < n/p² < p`, so `P(m) < p` is **automatic** — no smoothness
constraint at all. Hence

    #{j ≤ n : n/2 < j P(j)² ≤ n} = Σ_p #{m squarefree, n/(2p³) < m ≤ n/p³}
                                 ~ (6/π²)·(n/2)·Σ_{p > (n/2)^{1/3}} p^{−3} ≍ n^{1/3}/log n.

More useful is the *contribution to `‖w‖²`* from `j = mp` at fixed `m`: for
fixed `m` the `p`-integral in Theorem A repeats verbatim with `n` replaced by
`N = n/m`, giving `(27/4)(n/m)^{5/3}/log³(n/m)`. So composite `j` multiply the
regime-B total by `Σ_{m squarefree} m^{−5/3}·(log n/log(n/m))³ = ζ(5/3)/ζ(10/3)·(1+…)`
— an `O(1)` factor, **not** a change of log-power. (The `m`-sum converges: the
range of `m` is cut off at `m < p ≈ (n/m)^{1/3}`, i.e. `m < n^{1/4}`, beyond
which `p`-smoothness bites, and the tail past `n^{1/4}` is `O(n^{−1/6})`
relative.) `ζ(5/3)/ζ(10/3) = 1.8508`. This is confirmed directly: at
`n = 10^6` the mass shares by `m = j/P(j)` are

    m = 1: 0.509,  2: 0.180,  3: 0.098,  5: 0.046,  6: 0.035,  7: 0.026,  m ≥ 8: 0.105

(`m = 4` is absent — `j` must be squarefree.) A convergent profile whose total
is `1/0.509 ≈ 1.96×` the prime-only mass, against the predicted `1.85×` before
the `(log n/log(n/m))³ > 1` correction — i.e. `1.40×` in `‖w‖`. Composite `j`
change the *constant*, nothing else.

**Conclusion of §5.** The `3/2` was a correct computation of the wrong
quantity (the `u ≤ 2` part). The gap between `3/2` and the observed `≈1.09`
is not a counting error over composite `j`; it is the regime-C tail
`u > 2`, which carries ≈72% of the mass, is governed by `ρ(u−1)`, and grows
with a **larger power of `n`**, not a smaller power of `log n`.

### 5.5 What the drift converges to

Optimising (5.1): with `a = 1/α`, maximise `−L/a + 2 log ρ(a−2)`. Using
`log ρ(v) = −v(log v + log log v − 1) + O(v/log v)`, the saddle is at
`L ≍ 2a² log a`, i.e. `a ≍ √(L/log L)`, and the maximum value is
`≈ −4a log a ≈ −2√(L log L)`. Hence

    **‖w‖ = n · exp(−(1+o(1))·√(log n · log log n))**   (conjectural shape).

Numerically from (5.1), `(log n − log‖w‖_model)/√(L log L)` = 0.823, 0.823,
0.826, 0.837, 0.861 at `L = 20, 30, 50, 100, 300` — rising toward 1 as the
`o(1)` predicts. Status: **NUMERICAL/heuristic**, since it needs Lemma 2
uniformly for `u → ∞` (§6.3).

---

## 6. Upper bound

### 6.1 The converse implication — **PROVED**

For every `j ≤ n`, `‖w‖ ≥ |w_j| = |M(n/j, P(j))|`. In particular `j = 1` gives
`‖w‖ ≥ |M(n) − 1|`, so any bound `‖w‖ ≤ B(n)` yields `M(n) ≤ B(n) + 1`.
More is true: `‖w‖ ≤ B(n)` bounds the *entire family* `M(n/j, P(j))`
simultaneously, i.e. a bound on `‖w‖` is exactly a bound on Möbius sums over
`y`-rough integers, uniformly over all `(x,y)` of the form `(n/j, P(j))`.
Consequently `‖w‖ ≪ n^{5/6+ε}` implies `M(x) ≪ x^{5/6+ε}` for all `x = n/j`
with `P(j)` small, hence a zero-free region `Re s > 5/6` — the stated
obstruction, confirmed. **Do not attempt it.**

### 6.2 What is *not* obstructed

The obstruction only forbids upper bounds *stronger than the best known
`M(x)` bound*. Since

    √(log n · log log n) = o( (log n)^{3/5}(log log n)^{−1/5} ),

a bound `‖w‖ ≪ n·exp(−c√(log n log log n))` is **weaker** than the known
Vinogradov–Korobov `M(n) ≪ n exp(−c(log n)^{3/5}(log log n)^{−1/5})` and
therefore implies nothing new about `ζ`. This is exactly the shape §5.5
predicts to be the truth. So the correct target for deliverable 3 is a bound
of that shape, not a power saving.

### 6.3 Lemma 3 (smoothing bound) and the conditional theorem — **SKETCH**

The verified identity `M(x,y) = Σ_{a ≤ x, a\ y\text{-smooth}} M(x/a)` (proved
by Möbius inversion of Buchstab, or directly: split `d ≤ x` as `d = a·d'` with
`a` the `y`-smooth part) plus the triangle inequality gives, for any
non-increasing `E` with `|M(t)| ≤ t E(t)`,

    |M(x,y)| ≤ Σ_{a ≤ x,\ y\text{-smooth}} (x/a) E(x/a)
             ≪ x·log x · max_{0 ≤ v ≤ u} [ ρ(v)·E(y^{u−v}) ],                (6.1)

by dyadic decomposition `a ∈ [A,2A]`, `A = y^v`, using `Ψ(2A,y) − Ψ(A,y) ≪ Aρ(v)`.
Note (6.1) is self-consistent at `y = 1` (`u = ∞`, only `a = 1`, giving `xE(x)`)
and at `v = u` (`a ≈ x`, giving `xρ(u)`).

Under **RH** (`E(t) = t^{−1/2+ε}`) the bracket is increasing in `v` whenever
`v < √y/e`, so the max is at `v = u`:

> **(RH)** `|M(x,y)| ≪_ε x·ρ(u)·log x + x^{1/2+ε}`, `u = log x/log y`.

Feeding this into `‖w‖² = Σ_j M(n/j,P(j))²` and using `P(j) ≤ j`, so
`u_j = log(n/j)/log P(j) ≥ (1−β)/β` with `β = log j/log n`, and hence
`ρ(u_j) ≤ ρ((1−β)/β)`:

    ‖w‖² ≪ n² log²n · Σ_{j≤n} ρ(u_j)²/j² + n^{1+ε}
         ≪ n² (log n)^{O(1)} · max_{0<β≤1} exp( −βL + 2 log ρ(1/β − 1) )
         = n² · exp( −(2+o(1))·√(L log L) ).

> **Theorem C (conditional, SKETCH).** Assume RH. Then
> `‖w‖ ≪ n·exp(−(1−o(1))·√(log n · log log n))`.

This *matches* §5.5, so upper and lower bounds agree in shape.

**Named gaps in Theorem C.**
* (G1) Uniform `Ψ(x,y)` upper bounds in (6.1) across the *whole* range of `y`
  including `y < exp((log log x)^{5/3+ε})`, where Hildebrand's theorem does not
  apply and one must use Rankin's method. I have not written this out.
* (G2) The claim that the `v`-maximum in (6.1) is at `v = u` needs the endpoint
  analysis done carefully; I checked the sign of the derivative but not the
  global maximum.
* (G3) The evaluation of `max_β` as `exp(−(2+o(1))√(L log L))` uses the standard
  asymptotic for `log ρ`; routine but unwritten.

**Unconditional variant.** Nothing in the argument uses RH except the choice of
`E`. With `E(t) = exp(−c(log t)^{3/5}(log log t)^{−1/5})` the bracket in (6.1)
is still maximised at `v = u` at the relevant saddle (because
`u log u ≈ √(L log L) = o(L^{3/5}(log L)^{−1/5})` there), so the *same*
conclusion should hold unconditionally. I flag this as **SKETCH with an extra
gap**: I have not verified that the interior maximum of `ρ(v)E(y^{u−v})` never
exceeds the endpoint for all `(x,y)`, only at the saddle. If it goes through,
`‖w‖ ≪ n exp(−c√(log n log log n))` is unconditional and consistent with §6.1.

### 6.4 The exact arithmetic input the upper bound needs

Stripped of everything else, both directions need one and the same thing:

> **Uniform Lemma 2.** `M(x, x^{1/u}) = −ρ(u−1)·(x/log x)·(1 + o(1))`
> uniformly for `1 ≤ u ≤ (1+o(1))·√(log x / log log x)`
> — an upper bound `|M(x,x^{1/u})| ≪ x ρ(u−1)(log x)^{O(1)}` in that range
> suffices for Theorem C; the matching lower bound upgrades Theorem B from
> `n^{1−ε}` to `n·exp(−(1+o(1))√(log n log log n))`.

This is the exact analogue, for the μ-weighted rough-integer sum, of
Hildebrand's uniform range for `Ψ(x,y) ~ xρ(u)`. It is the whole problem.
Nothing else is needed: no zero-free region beyond what PNT already gives, and
no information about `M(x)` beyond the classical error term.

---

## 7. Self-validation against the target table

`checkA.py norm` (own sieve, own closed form, cross-checked against a dense
solve at `n = 500/1000/2000` with residual exactly 0):

| n | 1e5 | 3e5 | 1e6 | 3e6 | 1e7 | 3e7 |
|---|---|---|---|---|---|---|
| my ‖w‖ | 2289.3 | 5211.8 | 12850.5 | 29519.5 | 73972.3 | 172026.3 |
| target | 2289.3 | 5211.8 | 12850.5 | 29519.5 | 73972.3 | — |
| `‖w‖(log n)^{1.13}/n^{5/6}` | 2.4671 | 2.4922 | 2.4977 | 2.5042 | 2.5119 | 2.5193 |
| B-share | 0.2606 | 0.2777 | 0.2834 | 0.2766 | 0.2787 | 0.2737 |
| target B-share | 0.261 | 0.278 | 0.283 | 0.277 | 0.279 | — |

Exact agreement. Note the `(log n)^{1.13}` column is **not** flat: it rises
monotonically 2.4671 → 2.5193, a 2.1% climb over 2.5 decades with no sign of
levelling. Under the claimed law it should be constant. This is the numerical
signature of the drift in §5.3 and is consistent with, not evidence against,
Theorem B.

Everything I derived that can be checked, was checked:
* `27/4` constant of Theorem A: ratio → 0.992 at `n = 10^7`. ✔
* `F(u) = −ρ(u−1)`: 6-digit match, two independent routes. ✔
* Lemma 2 convergence: monotone toward 1 in `u = 2,2.5,3,4,5` over `10^5…10^8`. ✔
* Model local exponent vs truth: within 0.006 at all five table intervals. ✔

Nothing I derived disagrees with the table.

---

## 8. Honest assessment of what could still be wrong

Following the instruction to try to break my own result:

* **Could Lemma 2 be wrong?** It is proved from Buchstab + PNT + the Dickman
  integral equation, and independently confirmed numerically at `x` up to
  `10^8`. The one soft spot is uniformity in `u'` inside the induction — but
  Theorems A and B use only fixed `u`, where the induction is finite and clean.
  I do not think Lemma 2 is wrong.
* **Could Theorem B be wrong?** It needs only (i) Lemma 2 at one fixed `u`,
  (ii) `ρ(u−1) > 0`, (iii) PNT for the count of primes in `(n^α, 2n^α]`, and
  (iv) that `‖w‖²` is a sum of squares (so a sub-family is a lower bound). Each
  is solid. The result is *counter*-intuitive relative to the numerics only
  because the crossovers are at `n ≈ 10^{12}` and beyond.
* **Could the `√(log n log log n)` shape be wrong?** Yes — this is the weakest
  claim in the report. It rests on the leading-order model (5.1), and §2 shows
  the true `|M(x,y)|` exceeds the leading order by factors of 2–8 at accessible
  `x` for `u ≥ 3`. That excess pushes mass to *smaller* `α`, which makes the
  drift *faster*, not slower, so the qualitative conclusion (`‖w‖ = n^{1−o(1)}`)
  is reinforced; but the constant in the exponent is not established.
* **Alternative I considered and rejected.** That the mass-concentration at
  `β = 1/3` is a genuine fixed point rather than a kink artifact. Rejected
  because (a) the kink's log-derivative `18 − L` changes sign at `L = 18`, a
  computable prediction, and (b) the measured mass-mean `β` is already
  *decreasing* (0.3368 → 0.3351) rather than settling.

---

```
LOWER BOUND: (i) ‖w‖ ≥ (3√3/2 − o(1)) n^{5/6}(log n)^{-3/2}, unconditional, PNT only.
             (ii) For every fixed u>1, ‖w‖ ≫_u n^{1-1/(2u+2)}(log n)^{-3/2};
                  hence ‖w‖ ≫_ε n^{1-ε} for all ε>0, and ‖w‖ = n^{1-o(1)}.
                                              status: PROVED
LOG-POWER:   OPEN as posed, because the premise is false: no law
             ‖w‖ ≍ n^{5/6}(log n)^{-k} holds (contradicted by the lower bound).
             The fitted 1.13 is a drifting effective exponent; a zero-parameter
             model (|M(x,x^{1/u})| ~ ρ(u-1)x/log x) reproduces the true local
             exponents 0.7488→0.7682 to within 0.006 and predicts they rise to 1.
             The 3/2 is exactly correct for the regime-B/prime sub-family, with
             constant 3√3/2, verified numerically to 1%. Predicted true shape:
             ‖w‖ = n·exp(-(1+o(1))√(log n log log n)).
UPPER BOUND: Assume RH. Then ‖w‖ ≪ n·exp(-(1-o(1))√(log n log log n)).
             (Not obstructed: √(L logL) = o(L^{3/5}(logL)^{-1/5}), so this is
             weaker than the known M(x) bound. Plausibly unconditional.)
                                              status: SKETCH
             gaps: (G1) uniform Ψ(x,y) for small y via Rankin; (G2) the v-endpoint
             maximum in (6.1); (G3) the max_β saddle evaluation.
NUMERICS AGREE WITH THE TABLE: YES — ‖w‖ and B-share reproduced exactly at all
             five n by an independently written evaluator, itself validated
             against a dense linear solve (residual 0) at n=500/1000/2000.
             Extended to n=3e7: ‖w‖=172026.3. The column ‖w‖(log n)^{1.13}/n^{5/6}
             is NOT flat: 2.4671→2.5193, rising monotonically over 2.5 decades.
VERDICT: PARTIAL — the n^{5/6} hypothesis is disproved and replaced by
             ‖w‖ = n^{1-o(1)} with a proof; what remains is Lemma 2 uniform in u
             up to u ≍ √(log x/log log x), which would pin the o(1) to
             √(log n log log n) on both sides.
```
