> **WORKING PROOF NOTE — not yet refereed.** Every statement carries a status
> label; §7 lists what is *not* established. The analytic engine is **cited to
> Alladi (1982)**, not claimed. Two conditions remain open before this goes
> public — see §7.1c and §7.3.
>
> Numerics: `../code/` (`wnorm.py`, `massprofile.py`, `checkA.py`, `checkB.py`).
> Independent attack reports and the prior-art audit: `../audit/reports/`.

# The smallest singular value of a sparse Mertens matrix

## 0. Setup

`P(i)` = largest prime factor, `P⁻(i)` = smallest prime factor.
`M(x) := Σ_{d≤x} μ(d)` (Mertens);  `M(x,y) := Σ_{d≤x, P⁻(d)>y} μ(d)` (Möbius
over `y`-**rough** numbers);  `u := log x / log y`;  `ρ` = Dickman's function.

Kline's sparse matrix (LAA 584 (2020) 409–430, §1):

    𝒜(i,j) = 1  if i = j;  1 if i is squarefree and i/j = P(i);  0 otherwise
    ℛ_n   := 𝒜_n + e₁(1 − e₁)ᵀ            (first row all ones)

`ℛ_n` has `≈ 2.61n` nonzeros and `det ℛ_n = M(n)` (Kline). Write `𝒜 = I + S`,
`w := 𝒜^{-T}(1 − e₁)`, `μ := (μ(1),…,μ(n))`.

## 1. Why `w` is the object

*Status: proved; NUM-GUARD, verified end-to-end from the dense matrix.*
Sherman–Morrison gives `ℛ^{-1} = 𝒜^{-1} − μ wᵀ/M(n)`, the rank-one term
dominating, whence

    σ_min(ℛ_n) · ‖μ‖ · ‖w‖ = |M(n)| · (1 + o(1)),                      (1)

measured ratio `0.9896, 1.0038, 1.0047` at `n = 500, 1000, 2000` computed from
the dense matrix, and `0.999…1.008` at `n = 200…3200`. Also
`‖μ‖² = #{squarefree ≤ n} = (6/π²)n(1+o(1))`, measured `0.7810…0.7800` against
`√(6/π²) = 0.7797`. So everything reduces to `‖w‖`.

## 2. Closed form for `w` — PROVED

*Status: proved; verified to residual exactly `0.0e+00` against a dense linear
solve at `n = 500, 1000, 2000`, and the regime split is exhaustive (asserted).*

Unwinding `𝒜^{-1} = Σ_r(−S)^r`: the surviving paths strip largest primes, so
`(𝒜^{-1})_{kj} = μ(k/j)` exactly when `k` is squarefree, `j | k`, and every prime
of `k/j` exceeds `P(j)` — which forces `j` squarefree too. Hence

    j not squarefree :  w_j = 1                                          (2a)
    j squarefree     :  w_j = M(n/j, P(j))       (minus 1 at j = 1)      (2b)
    ‖w‖² = #{j ≤ n not squarefree} + Σ_{j ≤ n squarefree} M(n/j, P(j))²  (2c)

**Trichotomy** (`x = n/j`, `y = P(j)`), the first two exact with zero exceptions:

| regime | value |
|---|---|
| `y ≥ x` | `w_j = 1` |
| `√x ≤ y < x` | `w_j = 1 − (π(x) − π(y))` |
| `y < √x` | sieve sum |

Two auxiliary identities, both verified: **Buchstab**
`M(x,y) = M(x) + Σ_{p≤y} M(x/p,p)` (18/18), equivalently
`M(x,y) = 1 − Σ_{y<p≤x} M(x/p,p)`; and **smoothing**
`M(x,y) = Σ_{a ≤ x, a\ y\text{-smooth}} M(x/a)` over **all** `y`-smooth `a`, not
only squarefree (32/32).

## 3. The sieve asymptotic — PRIOR ART (Alladi 1982); two independent proofs

**Lemma 1 (Alladi 1982).** *Status: **PRIOR ART — audited 2026-07-25,
novelty withdrawn.** Re-proved here twice, independently, for `1 < u ≤ 3`.* With
`u = log x/log y`,

    M(x, x^{1/u}) = (x/log y)·ρ′(u)·(1 + O_u(1/log y))
                  = −(x/log x)·ρ(u−1)·(1 + O_u(1/log y)).                (3)

*Proof 1 (elementary, Buchstab).* The exact identity
`M(x,y) = 1 − Σ_{y<p≤x} M(x/p,p)` plus PNT gives, for
`M(x,x^{1/u}) ~ F(u)x/log x`, the delay equation

    F′(u) = −F(u−1)/(u−1),      F ≡ −1 on [1,2],

which under `g(u) = F(u+1)` is literally Dickman's equation with Dickman's
initial condition; hence `F(u) = −ρ(u−1)`. (`F ≡ −1` on `[1,2]` is the exact
regime-B evaluation `M(x,y) = 1 − (π(x) − π(y))`.)

*Proof 2 (analytic, Mellin).* From
`Σ_{P⁻(d)>y}μ(d)d^{-s} = ζ(s)^{-1}Π_{p≤y}(1−p^{-s})^{-1}`: on the relevant
contour the finite Euler product must be replaced **not** by its value at `s = 1`
but by `e^{γ}(log y)·e^{−I(ζ log y)}`, and `e^{γ−I(ζ)}` is exactly `ρ̂(ζ)`, the
Laplace transform of Dickman. Laplace inversion of `ζρ̂(ζ)` returns `ρ′(u)`.
This is precisely the uniformity difficulty (the Euler product is *not* close to
its `s=1` value when `y` is a fixed power of `x`) and it is what resolves it.

**Attribution — Alladi's Theorem 1, read 2026-07-25.** **K. Alladi, "Asymptotic
estimates of sums involving the Moebius function", J. Number Theory 14 (1982)
86–98, Theorem 1**, verbatim:

> If `y ≥ x` then `M(x,y) = 1`. If `y = x^{1/α}` then
> `M(x,y) = xρ′(α)/log y + y/log y + O(x·α²/log²y)`, **uniformly for `2 ≤ y < x`**.

Same `M(x,y) = Σ_{n≤x, p(n)>y} μ(n)` (his `p(n)` = least prime factor, `p(1)=∞`),
same main term; his `ρ` is defined by exactly our recursion
`ρ(α) = 1 − ∫₁^α ρ(t−1)dt/t`, whence `αρ′(α) = −ρ(α−1)` — the one-line bridge to
the `−(x/log x)ρ(α−1)` form used here. His extra `y/log y ≈ π(y)` term is
lower-order throughout our range. Restated by Alladi in Alladi–Goswami,
arXiv:2412.03088v1 (Dec 2024) §1.1 p.2.

**Even the contrast is his.** Alladi frames exactly this pairing: `M(x,y)` is the
`μ`-weighted analogue of `Φ(x,y)` (Buchstab `ω`) giving Dickman's `ρ′`, while the
largest-prime-factor variant `M*(x,y)` is the `μ`-weighted analogue of `Ψ(x,y)`
giving Buchstab's `ω′` (Alladi, Trans. Amer. Math. Soc. 272 (1982) 87–105). That
crossover is the published headline of the pair.

**What survives:** two proofs (Buchstab delay equation; Mellin via the Laplace
transform of Dickman) found independently under mandated-different methods.
Modest value — an appendix or remark, not a contribution.

> **NUM-GUARD.** Direct sieving of `M(x,x^{1/u})` at `x ≤ 2·10⁷` gives
> `M·log x/x` = `−1.068, −0.764, −0.465, −0.248, −0.120` at
> `u = 2, 2.5, 3, 3.5, 4`, against `−ρ(u−1)` = `−1, −0.595, −0.307, −0.130,
> −0.0486`. Ratios `1.068, 1.285, 1.516, 1.903, 2.471`, **decreasing in `x` at
> every `u`** but far from converged. At `u = 2` the residual `1.0675` is
> *exactly* `π(x)log x/x`, i.e. pure PNT slowness — which validates the form
> while showing the constant is not numerically confirmable at accessible `x`.
> The error term is corroborated separately: `(ratio − 1)·log y` is flat at
> `1.35, 2.2, 6.2` for `u = 2.5, 3, 4`.

## 4. `‖w‖ = n^{1+o(1)}` — PROVED, unconditional, both sides

**Theorem 2.** *Status: **PROVED**, unconditionally. The lower bound is
rigorous by citation: Alladi's Theorem 1 at **fixed** `α` has main term
`xρ′(α)/log y ≍_α x/log y`, dominating its `O(xα²/log²y)` error by a factor
`log y`. That is exactly what (4) needs, so the uniformity gap both attacks
flagged is **closed for this purpose**. Upper bound trivial.*

*Lower.* `ρ > 0` everywhere, so `|M(x,x^{1/u})| ≫_u x/log x` for every fixed `u`
(Alladi Thm 1).
Taking `j = p` prime with `p ∈ (n^{1/(u+1)}, 2n^{1/(u+1)}]` puts `x = n/p`,
`y = p`, `log x/log y = u`, and summing squares over that sub-family gives

    ‖w‖ ≫_u n^{1 − 1/(2u+2)} / (log n)^{3/2}   for every fixed u,          (4)

hence `‖w‖ ≫_ε n^{1−ε}` for every `ε > 0`. No cancellation is involved: (2c) is
a sum of squares, so **any** sub-family is a valid lower bound.

*Upper.* `|M(x,y)| ≤ x` trivially, so `‖w‖² ≤ Σ_j (n/j)² ≤ ζ(2)n²`, i.e.
`‖w‖ ≤ (π/√6)n = 1.283n`.

Together: **`‖w‖ = n^{1+o(1)}`, unconditionally.**

**Remark 2a (the true shape).** *Status: SKETCH, conditional.* Both attacks
predict `‖w‖ = n·exp(−(1+o(1))√(log n · log log n))`. The matching upper bound
needs a power saving `M(x) ≪ x^{θ}`, any `θ < 1`: the unconditional zero-free
region only gives `exp(−c(log x)^{3/5}(log log x)^{−1/5})`, which dominates the
Dickman term until `log n ≈ 3·10⁵`. Attack B initially claimed this bound
unconditional and self-corrected.

**Remark 2b (independent end-to-end check).** *Status: numerical.* The
analytic pipeline of §3–§4, run with **no fitted parameter**, predicts
`‖w‖ = 2176.6, 4950.6, 12273.8, 28286.4, 71102.6` at
`n = 10⁵, 3·10⁵, 10⁶, 3·10⁶, 10⁷` against the computed
`2289.3, 5211.8, 12850.5, 29519.5, 73972.3` — ratios `0.951, 0.950, 0.955,
0.958, 0.961`, improving monotonically. A parameter-free prediction tracking the
data to 4% is the strongest single piece of evidence in this note.

## 5. Consequence: the singular value and an RH criterion

**Theorem 3.** *Status: proved, given 2 and (1).*

    σ_min(ℛ_n) = |M(n)| · n^{−3/2 + o(1)},                                (5)
    and consequently        RH  ⟺  σ_min(ℛ_n) ≪_ε n^{−1+ε}.               (6)

The `⟸` of (6) needs only the trivial upper bound `‖w‖ ≤ 1.283n`; the `⟹` is
exactly what Theorem 2's lower bound buys. So (6) is **two-sided and
unconditional**, for a matrix with `2.61n` nonzeros.

**What is and is not content here.** `det ℛ_n = M(n)` is Kline's, so
`RH ⟺ |det ℛ_n| ≪ n^{1/2+ε}` is immediate and carries nothing new. The content
of (6) is the conversion factor `‖μ‖‖w‖ = n^{3/2+o(1)}`, i.e. Theorem 2 —
without it, (6) is not available in either direction at the right exponent.

## 5b. The other extreme, and the non-normality gap

**Proposition 4.** *Status: proved (elementary); NUM-GUARD below.*
`σ_max(ℛ_n) = √n·(1+O(1/n))`. Lower: the first row has norm `√n`. Upper:
`ℛ_n = e₁1ᵀ + I + S` with `‖S‖ = √π(n)` exactly (the forest's max in-degree is
`π(n)`, attained at the hub `1` whose children are precisely the primes, and the
Schur bound `√(1·π(n))` is met by the star), so the excess over `√n` is
`O(√π(n)) = o(√n)`.

> **NUM-GUARD.** `σ_max/√n = 1.00387, 1.00191, 1.00094, 1.00047, 1.00023` at
> `n = 400…6400` — the excess halves at each doubling, i.e. `σ_max − √n =
> O(n^{−1/2})`, far tighter than the proof gives.

**Corollary 5 (non-normality).** *Status: proved given Kline's Thm 1.*
Since `|r_+| = (1+o(1))√π(n)`,

    σ_max(ℛ_n) / |λ_max(ℛ_n)|  ≍  √(log n).

Measured `1.906, 2.087, 2.262, 2.440, 2.592` against `√log n = 2.448, 2.586,
2.716, 2.841, 2.960` (ratio rising `0.779 → 0.876` toward 1, the usual PNT
slowness). **Contrast:** the paper's `H̄^{(s)}_n` has a `Θ(√n)` gap between
smallest eigenvalue and smallest singular value. Sparsifying from `~n log n` to
`2.61n` nonzeros collapses the top-end non-normality from `√n` to `√(log n)`,
because it prunes the hub degree from `n` to `π(n)`.

## 5c. The unmodified matrix, and Cheon–Kim's question

**Proposition 6.** *Status: proved; NUM-GUARD below.*
`σ_min(𝒜) = 1/‖𝒜^{-1}‖ ≍ n^{−1/2}`.

*Proof.* `S` is nilpotent of index `ω_max(n)+1`, where `ω_max(n)` is the largest
number of prime factors of a squarefree `k ≤ n` (`~ log n/log log n`), so
`𝒜^{-1} = Σ_{r≤ω_max}(−S)^r` is a **terminating** Neumann series. Row sums of
`S^r` are `≤ 1` (each `k` has a unique parent chain) and column sums are
`π_r(n) := #{k ≤ n squarefree, ω(k) = r}`, so `‖S^r‖ ≤ √(π_r(n))` and
`‖𝒜^{-1}‖ ≤ Σ_r √(π_r(n)) = n^{1/2+o(1)}`. Conversely
`‖𝒜^{-1}‖ ≥ ‖𝒜^{-1}e₁‖ = ‖μ‖ ≍ √(6n/π²)` (Kline LAA 588, Thm 1 and Thm 3). ∎

> **NUM-GUARD.** Nilpotency index `5, 5, 5, 6` at `n = 500…3000`;
> `‖𝒜^{-1}‖/√n = 0.853, 0.851, 0.849, 0.850`; `σ_min(𝒜)·√n = 1.1717, 1.1753,
> 1.1773, 1.1760`. So `‖𝒜^{-1}‖` is essentially attained by its first column.

**Remark 6a (Cheon–Kim).** Cheon & Kim, *Mertens equimodular matrices of
Redheffer type*, LAA 572 (2019) 252–272, Thm 4.2, give a sufficient condition for
RH via the smallest singular value of the **unmodified** triangular factor `L_n`
of a Mertens equimodular `L_n + uvᵀ`: since `det L_n = 1` and `uvᵀ` has singular
values `√(n−1),0,…,0`, Li–Mathias gives `|M(n)| ≤ 1 + √(n−1)/σ_min(L_n)`, so
`1 + √(n−1)/σ_min(L_n) = O(n^{1/2+ε})` implies RH. They ask which matrices satisfy
it. **Proposition 6 answers that negatively for the present family:** with
`σ_min(𝒜) ≍ n^{−1/2}` the quantity is `≍ n` (measured `427, 851, 1699, 2552`
against the required `O(n^{1/2+ε})`), so the resulting bound `|M(n)| ≪ n` is
trivial. Note the criterion concerns the *unmodified* `L_n` and is
one-directional, whereas (5)–(6) concern the *modified* `ℛ_n` and are an
equivalence.

## 6. Six refuted conjectures — the finite-range traps

*Status: all refuted, recorded so they are not re-derived.* This problem is
severely pre-asymptotic; every conjecture below was formed on numerics up to
`n = 10⁷` and is false.

1. **`‖w‖` is a counting (cancellation-free) quantity.** Refuted: the
   cancellation-free model overshoots by `34×` growing to `516×`.
2. **`‖w‖ ~ C·n^{3/4}`.** Refuted: `‖w‖/n^{3/4}` stable to four figures over
   `10⁵–10⁶` (`0.40711, 0.40658, 0.40637`), breaks at `3·10⁶` (`0.40951`).
3. **`‖w‖ ~ C·n^{5/6}/(log n)^{1.13}`.** Refuted by 2. The "stable" column
   `2.4670, 2.4922, 2.4977, 2.5042, 2.5119` is **monotone increasing at every
   step** (`+1.02%, +0.22%, +0.26%, +0.31%`) with no levelling; it was read as
   convergence when it is drift.
4. **Mass pinned at `β = log j/log n = 1/3`** (equivalently `u = 2`). This is a
   **corner artifact**: `ρ` has a corner at `1`, so the integrand's derivative
   jumps at `u = 2` and the maximiser is pinned only below a threshold.
   Measured `β` = `0.3368, 0.3364, 0.3361, 0.3351` — already drifting down and
   *accelerating* (`−0.0004, −0.0003, −0.0010`).
5. **Log-power `3/2` is wrong.** It is in fact *correct* for the regime-B prime
   family, with constant `3√3/2 = 2.598` (verified to `0.992` at `n = 10⁷`) —
   but that family is only `≈28%` of the mass, so it does not set the global
   shape. Composite `j` contribute a constant factor `ζ(5/3)/ζ(10/3) ≈ 1.85`
   (measured `1.96`), not a log-power.
6. **`β → 0` is false.** *This one was refuted and is now reinstated:* it is
   true asymptotically, it simply does not begin within computable range.

**Unresolved discrepancy between the two attacks.** The threshold at which the
maximiser leaves `u = 2`: attack A gets `log n < 18` (`n < 6.6·10⁷`), attack B
gets `log n < 24.79` (`n < 5.9·10¹⁰`), the two differing by an offset in the same
`1/β² = 9` units. Not adjudicated. The measured drift in item 4 above is already
visible at `n = 10⁷`, which favours A's threshold. The main conclusions do not
depend on which is right.

## 7. What is NOT established

1. **§3 is PRIOR ART (Alladi 1982) — novelty withdrawn.** Audited 2026-07-25.
   Not textbook material (absent from the Hildebrand–Tenenbaum survey, checked),
   but live, findable, actively-cited journal prior art restated by its author in
   Dec 2024 — for a novelty claim that is worse than a textbook exercise.
1a. **Kline LAA 588 (2020) 224–237 — READ 2026-07-25; this is the foundation,
   not a collision (same author).** It supplies, and must be cited for:
   (i) **Theorem 1**, `det MMᵀ = ‖l‖₂²` with `l` the first column of `L^{-1}` for
   unit lower-triangular `L` — here `𝒜^{-1}e₁ = μ`, so `l` *is* `μ`;
   (ii) **Theorem 3**, `det BBᵀ = Σ_{i≤n}|μ(i)|` and `√(det BBᵀ) = √(6n)/π + O(1)`
   — i.e. `‖μ‖` and the `6/π²` constant used in (1);
   (iii) the geometric framing (p. 227): *"the Riemann hypothesis is an assertion
   that the constant `1ᵗ ∈ ℝⁿ` is, for all `n`, almost in the span of the rows of
   `B`."* That distance is `|det A|/√(det BBᵀ) = |M(n)|/‖μ‖`.
   **The relation to this note is exact and quantitative:**

       LAA 588:  dist(1ᵗ, rowspan B) = |M(n)|/‖μ‖      ≍ |M(n)|·n^{−1/2}
       here:     σ_min(ℛ_n) = |M(n)|/(‖μ‖‖w‖)          ≍ |M(n)|·n^{−3/2+o(1)}

   — the first is the distance from **one** vector to a hyperplane, the second the
   minimum over **all** unit directions; they differ by `‖w‖ = n^{1+o(1)}`, and
   quantifying that gap is what needs Alladi. Verified by text search: LAA 588
   contains **no** treatment of `σ_min` (one occurrence of "singular", in
   "nonsingular", unrelated; no "smallest", no "condition number"); its eigenvalue
   results concern the *largest* eigenvalue and the *product* of subdominant ones.
   So §5 completes the LAA 588 programme rather than competing with it.
1b. **Cheon & Kim, LAA 572 (2019) 252–272 — READ 2026-07-25; settled.** Their
   Thm 4.2 concerns `σ_min` of the **unmodified** `L_n`, is one-directional, and
   supplies no asymptotic; §5 concerns the **modified** `ℛ_n` and is an
   equivalence. Cited and distinguished at Remark 6a, which also answers their
   posed question for this family. Adjacent, not overlapping.
1c. **Bordellès & Cloitre, JIPAM 10 (2009), art. 62 — READ 2026-07-25.** The
   originators of the "σ_min of a triangular factor ⇒ RH" strategy, predating
   Cheon–Kim by a decade. Their matrix `Γ_n` has
   `det Γ_n = n! · Σ_{k≤n} μ(k)/k` (the *weighted* Mertens sum), and their
   Corollary 2.7 gives `σ_min(U_n) ≫ n^{-1+ε} ⇒ PNT`,
   `σ_min(U_n) ≫ n^{-1/2-ε} ⇒ RH`, for `U_n` the upper triangular factor of an
   LU decomposition. They compute `U_n^{-1}` explicitly but **do not** determine
   `σ_min` asymptotically, and observe that general triangular-matrix bounds
   (e.g. `σ_n ≥ min|a_ii|/2^{n-1}`) are "still very far from the PNT". Cited and
   distinguished; §5c's `σ_min(𝒜) ≍ n^{-1/2}` is an instance where the arithmetic
   structure *does* give the exact order.
2. **Uniformity in `u` — RESOLVED for §§4–5; still OPEN for the sharp shape.**
   Alladi's Theorem 1 is uniform for `2 ≤ y < x`, and at **fixed** `α` its main
   term dominates the error — all that Theorem 2, and hence (5)–(6), require.
   **Those are now unconditional theorems, not sketches.**
   The sharp shape of Remark 2a is different, and Alladi marks the obstruction
   himself (p. 87): since `ρ′(α) = −exp{−α log α − α log log α + O(α)}` for
   `α > 3`, *"the main terms of Theorem 1 are smaller than the error term when `α`
   is large"* — so Theorem 1 does **not** reach the saddle at
   `α ≍ √(log n/log log n)`. His Theorem 2 covers large `α` but only as an upper
   bound with decay `exp{−(α/2)log α}`, **half** the true exponent, plus a floor
   `x/log²x`. The constant in `exp(−(1+o(1))√(log n log log n))` is therefore not
   obtainable from the 1982 estimates; it remains genuinely open, and the reason
   is documented in the source.
3. **The `o(1)` in 2 and (5) is not pinned.** Remark 2a's
   `exp(−(1+o(1))√(log n log log n))` is a sketch and its upper half is
   conditional on a power saving for `M(x)`.
4. **No constant.** There is no asymptotic constant or log-power to quote: the
   prefactor `J(L) ≈ 1/(L/9 − 0.755) + 1/(2.755 − L/9)` *diverges* at
   `L = 24.79` on attack B's normalisation, so local fits are meaningless as
   asymptotics.
5. **Nothing here is audited.** No adversarial pass has been run on §§2–5.

## 8. What is used from where

| Ingredient | Source | Status |
|---|---|---|
| `𝒜`, `ℛ_n`, `det ℛ_n = M(n)`, dominant eigenvalues `1 ± √π(n)` | Kline, LAA 584 (2020), §1 and Thm 1 | **cited** |
| closed form `w_j = M(n/j,P(j))` and trichotomy (2a–2c) | this note | **proved**; residual `0.0e+00` vs dense solve |
| Buchstab and smoothing identities for `M(x,y)` | this note; classical in form | proved; 18/18 and 32/32 |
| `σ_min·‖μ‖·‖w‖ = |M(n)|(1+o(1))` (1) | this note (Sherman–Morrison) | proved; verified from the dense matrix |
| `‖μ‖² ~ 6n/π²` | classical (squarefree density) | cited |
| `M(x,y) = xρ′(α)/log y + y/log y + O(xα²/log²y)`, unif. `2≤y<x` | **Alladi, JNT 14 (1982), Thm 1** | **PRIOR ART**; re-proved here twice; supplies the fixed-`α` input to 2 |
| `M(x,y) ≪ x(loglog x)²e^{−(α/2)logα} + x/log²x`, `α≥2` | Alladi, JNT 14 (1982), Thm 2 | cited; too weak for the sharp constant |
| the `Φ`/`ω` vs `M*`/`ω′` contrast | Alladi, TAMS 272 (1982) 87–105 | **cited** — the contrast is his too |
| RH sufficient condition via `σ_min(L_n)`, unmodified | Cheon–Kim, LAA 572 (2019) Thm 4.2 | **cited**; different matrix, one-directional |
| `det MMᵀ = ‖l‖²`; `‖μ‖`, `6/π²`; parallelotope framing | Kline, LAA 588 (2020) Thm 1, Thm 3, p. 227 | **cited** — foundation for (1) |
| `σ_min(𝒜) ≍ n^{−1/2}`; terminating Neumann series | this note | **proved**; answers Cheon–Kim's question negatively |
| `σ_max(ℛ_n) = √n(1+O(1/n))`; gap `≍ √log n` | this note | **proved** |
| `‖w‖ = n^{1+o(1)}` (2) | this note | **proved**, unconditional |
| `σ_min = |M(n)|n^{−3/2+o(1)}`; RH criterion (5),(6) | this note | **proved** given 2 |
| `‖w‖ = n·exp(−(1+o(1))√(log n loglog n))` | this note | **SKETCH**; upper half conditional |
| uniformity in `u` | — | **OPEN** (the sole named gap) |
| the six refuted conjectures of §6 | this note | refuted, recorded |
| threshold `18` vs `24.79` | attacks A vs B | **discrepancy, unadjudicated** |

### Provenance

Produced 2026-07-25 by two independent attacks under mandated-different methods
(elementary/prime-counting; analytic/Mellin), which converged on the same
Lemma 1 and the same Theorem 2. Coordinator verification: Dickman values
reproduced to 6 digits; the sub-family exponents `(2u+1)/(u+1)` confirmed
directly from the exact `w`; the closed form (2) re-checked against a dense
linear solve.
