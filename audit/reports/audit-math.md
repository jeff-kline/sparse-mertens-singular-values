# Adversarial referee report — mathematics axis
Target: `paper/sparse-mertens-singular-values.tex` (+ `proofs/smallest-singular-value.md`)
Referee scripts (mine, independent of `code/`): `scratchpad/ref1.py`, `t1.py`…`t7.py`.
Every matrix below is built from the paper's `\eqref{eq:defA}` directly; I did not
call `wnorm.py`/`checkA.py`/`checkB.py` at any point.

**Headline.** The two flagship results survive: the closed form (Thm 1) and the
RH equivalence (Thm 3) are correct, and I reproduced every printed number in the
paper except one. But **four numbered claims are stronger than their proofs**,
and one of them — the `(1+o(1))` in the Sherman–Morrison factorisation — is a
real unconditional gap that propagates into half of Theorem 3. Theorem 4 is
overclaimed twice, exactly as suspected in the mandate (and one of the two
overclaims is one the mandate did *not* flag). Two printed statements are
outright false.

---

## 1. Theorem 1 (closed form) — **CONFIRMED-CORRECT** (two must-fix statement defects)

Verified against a dense solve of `A^T w = 1 − e_1` at `n = 50, 137, 300, 500,
1000, 2000`: `max|dense − closed| = 0.000e+00` at every `n`. The proof (nilpotency
of `S`; unique parent chain ⇒ at most one path; value `(−1)^{ω(k/j)} = μ(k/j)`)
is correct, and I re-derived it independently. The substitution `d = k/j` is
legitimate: `d` non-squarefree contributes `μ(d)=0`, so extending the sieve sum
from squarefree `d` to all `d` is free, as the paper implicitly does.

**Independent structural check I derived** (not in the paper). Buchstab at `y = 1`
gives the exact identity
```
        sum_{p prime, p <= n}  w_p  =  1 − M(n).
```
Verified: `n=500 → 7 = 7`; `n=1000 → −1 = −1`; `n=3000 → 7 = 7`. This confirms
the closed form through a route that never touches the matrix.

**Defect 1 (must-fix).** `P(i)` is defined only for `i > 1` (line 102), yet
Theorem 1 writes `M(n/j, P(j))` for *all* squarefree `j`, including `j = 1`. The
needed convention is `P(1) := 1`, i.e. `M(n, P(1)) = M(n)` — which is exactly
what `code/wnorm.py:30` (`y[0] = 1`) silently assumes. As printed the `j = 1`
case of a numbered theorem is undefined.

**Defect 2 (must-fix).** The second display of Theorem 1 — the formula for
`‖w‖²` — is **false at `j = 1`**. It reads `Σ_{j squarefree} M(n/j,P(j))²`, whose
`j=1` term is `M(n)²`; the correct term is `(M(n)−1)²`. The parenthetical "with
the value at `j=1` diminished by 1" attaches to the *first* display only and is
not carried into the second. Confirmed numerically: `w_1 = M(n)−1` exactly at
every `n` tested.

## 2. Corollary (trichotomy) — **CONFIRMED-CORRECT**

Exhaustive over **all** squarefree `j ≤ n`, `n = 500 / 2000 / 5000`:
regime A (`y ≥ x`) 286 / 1164 / 2955 indices, **0 mismatches**;
regime B (`√x ≤ y < x`) 12 / 38 / 67 indices, **0 mismatches**.

Proof nit: "a composite `y`-rough number is at least `y² ≥ x`" should be
*greater than* `y²` (its prime factors are `> y`, not `≥ y`). That strictness is
precisely what makes the boundary case `y² = x` work. One word.

## 3. Lemma (identities) — **CONFIRMED-CORRECT**

52 `(x,y)` pairs, `x ∈ {50,137,400,999,2500,4000}`, `y ∈ {2,…,101}`:
**0 failures** for `M(x,y) = M(x) + Σ_{p≤y}M(x/p,p)`, 0 for the complement form
`M(x,y) = 1 − Σ_{y<p≤x}M(x/p,p)`, 0 for `M(x,y) = Σ_{a≤x, a y-smooth} M(x/a)`.
I re-proved both by Dirichlet convolution: `1_{y-smooth} * μ = μ·1_{y-rough}`,
and the `p^k` (`k ≥ 2`) terms are exactly what cancels — so the paper is right
to stress that the smoothing sum must run over **all** smooth `a`.

## 4. Theorem 2 (norm, `‖w‖ = n^{1+o(1)}`) — **CONFIRMED-CORRECT**

*Upper bound.* `|M(x,y)| ≤ ⌊x⌋` and `Σ_{j≤n}(n/j)² ≤ ζ(2)n²` give
`‖w‖ ≤ (π/√6)n = 1.2825n`. Correct (and it covers the non-squarefree `w_j = 1`
terms too, since `1 ≤ n/j`).

*Lower bound and the quantifier question raised in the mandate.* The
`α`-dependence does **not** spoil the conclusion. The logic is: for each fixed
`α > 1` there are `C_α > 0`, `n_α` with `‖w‖ ≥ C_α n^{1−1/(2α+2)}/log^{3/2}n` for
`n ≥ n_α`; given `ε > 0` one *first* picks `α = α(ε)` with `1/(2α+2) < ε/2`,
*then* the resulting `C_ε := C_{α(ε)}` and `n_ε` are constants. That is exactly
`‖w‖ ≫_ε n^{1−ε}`. No limit is interchanged — `α → ∞` is a choice, not a limit.

The supporting steps check out: for `p ∈ (n^{1/(α+1)}, 2n^{1/(α+1)}]`,
`log x/log y = α + O(1/log n)` and `ρ'` is continuous on `(1,∞)`
(`ρ'(α) = −ρ(α−1)/α`), so the perturbation of `α` is harmless; Alladi's error
`O(xα²/log²y)` is beaten by the main term by the factor `log y` at fixed `α`;
Alladi's secondary term `y/log y` is `O(x^{1/α})`, utterly negligible against
`x/log y` for fixed `α > 1`; and `‖w‖²` being a sum of squares makes any
subfamily a valid lower bound. **Correct as written.**

Reproduction of Table 1 (my code, independent): `‖w‖ = 2289.3, 5211.8, 12850.5,
29519.5, 73972.3` at `n = 10^5, 3·10^5, 10^6, 3·10^6, 10^7` — **exact agreement**
with the paper, including `‖w‖/n^{3/4} = 0.40711, 0.40658, 0.40637, 0.40951`.

## 5. Proposition (Sherman–Morrison): the inverse formula — **CONFIRMED-CORRECT**

`R^{-1} = A^{-1} − μ w^T/M(n)` follows from `A^{-1}e_1 = μ_n`,
`(1−e_1)^T A^{-1} = w^T`, and `1 + (1−e_1)^T A^{-1} e_1 = 1 + (M(n)−1) = M(n)`.
All three verified. Note this *also* re-proves `det R_n = M(n)` in one line, so
the citation to `[kline584]` for the determinant is not load-bearing.

## 6. Proposition, equation `\eqref{eq:factorisation}` — **GAP** (this is the serious one)

Claim: `σ_min(R_n)·‖μ_n‖·‖w‖ = |M(n)|(1+o(1))`, asserted unconditionally.

The proof's justification is: the rank-one term has norm `‖μ‖‖w‖/|M(n)|`, while
`‖A^{-1}‖ ≍ √n`, "the rank-one term therefore dominates". Making that precise:
```
   | ‖R^{-1}‖ − ‖μ‖‖w‖/|M(n)| |  ≤  ‖A^{-1}‖,
   relative error =  ‖A^{-1}‖·|M(n)| / (‖μ‖‖w‖)  ≍  1.09 · |M(n)| / ‖w‖ .
```
(Constants from my numerics: `‖A^{-1}‖/√n → 0.849895`, `‖μ‖/√n → 0.779698`,
ratio `1.090031`; see §8.) **So the `(1+o(1))` holds iff `|M(n)|/‖w‖ → 0`, and
that is exactly what the paper's own two theorems fail to deliver.**

- Best unconditional lower bound available: Theorem 2 gives `‖w‖ ≫_ε n^{1−ε}`
  for each fixed `ε`, i.e. `‖w‖ ≥ n^{1−δ(n)}` with `δ(n) → 0` but no rate.
- Best unconditional upper bound on `|M(n)|`: `n·exp(−c(log n)^{3/5}(log log n)^{−1/5})`,
  i.e. also `n^{1−o(1)}`.
- These **do not cross**. For fixed `ε`, `n^{-ε}·exp(c(log n)^{3/5}…) → ∞`, so
  `|M(n)|/‖w‖` is *not* shown to be `o(1)`.

I checked whether Alladi at growing `α` rescues it: the error term is beaten only
while `α log α ≲ log log n`, i.e. `α ≲ log L/log log L` with `L = log n`, which
yields at best `‖w‖ ≫ n·exp(−C·L log log L/log L)`. Since `L/log L ≫ L^{3/5}`,
that decays *faster* than the unconditional `M(n)` bound. The route is closed.

I also checked the cheap elementary lower bounds and none suffice:
`‖w‖² ≥ (M(n)−1)² + #{non-squarefree j ≤ n} = M(n)² + 0.3921n(1+o(1))` needs
`|M(n)| ≲ 1.43√n`; adding the regime-B prime family
(`‖Q w‖ ≍ 2.6 n^{5/6}/log^{3/2}n`, measured — see §10) needs `|M(n)| ≪ n^{5/6}`.
Both are RH-strength or near it.

**Precise statement of the gap:** the paper needs, and does not prove,
`‖w‖/|M(n)| → ∞`. It follows from RH (`|M(n)| ≪ n^{1/2+ε}` vs `‖w‖ ≫ n^{1−ε}`),
and more generally from any hypothesis `M(n) ≪ n^{1−δ}` with fixed `δ > 0`, but
not from Theorems 2 and 4 as cited.

**Suggested repair (cheap, and honest):** state the proposition as
```
   σ_min(R_n)·‖μ_n‖·‖w‖  =  |M(n)| · (1 + O(|M(n)|/‖w‖)),
```
which *is* unconditional, and then note that the error is `o(1)` under RH and
under `M(n) ≪ n^{1−δ}`. Nothing downstream that matters is lost (see §7).

*Aside:* the hypothesis `M(n) ≠ 0` is correctly attached to the inverse formula,
and `\eqref{eq:factorisation}` degenerates harmlessly to `0 = 0` when `M(n) = 0`.
Numerically the true error is far smaller than the triangle-inequality bound
(at `n=500`: measured deviation `−0.0104`, bound `0.1384`) — the `A^{-1}` term
largely cancels — but that is an observation, not a proof.

## 7. Theorem 3 — asymptotic: **GAP** (upper half only); RH equivalence: **CONFIRMED-CORRECT**

Split the claim.

- `σ_min(R_n) ≫ |M(n)|n^{-3/2+o(1)}` (i.e. `σ_min` not too small): **safe**.
  `‖R^{-1}‖ ≤ ‖A^{-1}‖ + ‖μ‖‖w‖/|M(n)| ≤ 0.86√n + 1.01n^{3/2}/|M(n)| ≤
  1.88 n^{3/2}/|M(n)|` using only `|M(n)| ≤ n` and `‖w‖ ≤ 1.2825n`. Unconditional.
- `σ_min(R_n) ≪ |M(n)|n^{-3/2+o(1)}` (i.e. `σ_min` really is that small):
  **inherits the §6 gap in full.** Every lower bound on `‖R^{-1}‖` I can
  construct requires the same domination `‖w‖ ≫ |M(n)|`.
- **The RH equivalence itself is not affected.**
  - `σ_min ≪_ε n^{-1+ε} ⇒ RH`: needs only `|M(n)| ≤ 1.88 σ_min n^{3/2}` above.
    Fully unconditional; no `(1+o(1))` used. ✔
  - `RH ⇒ σ_min ≪_ε n^{-1+ε}`: under RH, `|M(n)|/‖w‖ ≪ n^{1/2+ε}/n^{1−ε} → 0`,
    so the `(1+o(1))` of §6 *is* available under the very hypothesis being
    assumed. ✔

So the headline `RH ⟺ σ_min(R_n) ≪_ε n^{-1+ε}` stands, two-sided and
unconditional. Only the unconditional *asymptotic* `σ_min = |M(n)|n^{-3/2+o(1)}`
(as stated in the abstract, in Theorem 3, and in `\eqref{eq:compare}`) needs
qualification.

## 8. Theorem 3, proof, last sentence — **WRONG** (directions swapped)

> "Note that the forward direction uses only the elementary upper bound on `‖w‖`;
> the reverse is what Theorem \ref{thm:norm} buys."

This is backwards, and it contradicts the paper's own preceding two sentences.
The *first* ("forward", `RH ⇒ σ_min` small) direction is the one that consumes
Theorem 2's **lower** bound `‖w‖ ≫ n^{1−ε}`; the *second* ("Conversely",
`σ_min` small `⇒ RH`) is the one using the elementary **upper** bound
`‖w‖ ≤ (π/√6)n`, as the paper literally writes one line earlier. The supporting
note has it right (`proofs/smallest-singular-value.md` §5: "The `⟸` of (6) needs
only the trivial upper bound … the `⟹` is exactly what Theorem 2's lower bound
buys"), so this is a transcription error introduced in the paper.

## 9. Theorem 4, `σ_max(R_n) = √n(1+O(1/n))` — **OVERCLAIM** (statement true; proof gives `1+O(1/√log n)`)

The mandate's suspicion is **confirmed**. The printed proof yields
`σ_max ≤ √n + 1 + √(π(n))`, i.e. `√n(1 + O(1/√log n))`. That is weaker than the
stated `1 + O(1/n)` by a factor `n/√log n`. As written the theorem does not
follow from its proof.

The intermediate step is fine: `S^T S = diag(#children of j)` **exactly** (each
vertex has a unique parent, so `S(i,j)S(i,j') ≠ 0` forces `j = j'`), the maximum
child count is `π(n)` at the root, hence `‖S‖ = √(π(n))` *exactly* — verified to
5 decimals at `n = 500,1000,2000,3000` (`9.74679 = 9.74679`, etc.).

**The statement is nevertheless true, and here is a proof the paper can use.**
Write `G = R R^T = [[n, b^T],[b, C]]`, `C = B̃B̃^T` with `B̃` = rows `2..n` of `A`.
Then `b_k = ⟨row 1, row k⟩ =` (row sum of `A` at `k`) `∈ {1,2}`, so `‖b‖² ≤ 4n`;
and `‖C‖ ≤ ‖A‖² ≤ (1+√π(n))² = o(n)`. Since `λ_max(G) ≥ n > ‖C‖`, the top
eigenvector has nonzero first coordinate, and normalising it to 1 gives
`λ = n + b^T(λI − C)^{-1}b ≤ n + ‖b‖²/(λ − ‖C‖) ≤ n + 4 + o(1)`. Hence
`λ_max(RR^T) = n + O(1)` and `σ_max = √n(1 + O(1/n))`. Elementary, two lines.

Numerical confirmation (sparse Lanczos, my code):

| `n` | `σ_max/√n` | `λ_max(RR^T) − n` | `‖b‖²/n` |
|---|---|---|---|
| 400 | 1.003868914 | 3.101118 | 2.8125 |
| 6 400 | 1.000230513 | 2.950902 | 2.8233 |
| 10^5 | 1.000014453 | 2.890552 | 2.8238 |
| 10^6 | 1.000001434 | 2.867171 | 2.8238 |

`λ_max − n` converges to `‖b‖²/n → 1 + 3·(6/π²) = 2.8238`, exactly as the
argument predicts, and `σ_max/√n` reproduces the paper's printed `1.00387,
1.00191, 1.00094, 1.00047, 1.00023`. So: **not a numerical observation
masquerading as a theorem — a true theorem with an inadequate proof.**

## 10. Theorem 4, `‖A_n^{-1}‖ ≍ √n` and `σ_min(A_n) ≍ n^{-1/2}` — **OVERCLAIM** (second one, not in the mandate)

The proof establishes `‖S^r‖ ≤ √(π_r'(n))` and concludes
`‖A^{-1}‖ ≤ Σ_r √(π_r'(n)) = n^{1/2+o(1)}` — **the paper writes `n^{1/2+o(1)}`
itself**. But the theorem asserts `≍ √n`, which is strictly stronger, and
`n^{1/2+o(1)}` does not imply it. The gap is not hypothetical: by Landau's
`π_r'(n) ≈ n(log log n)^{r-1}/((r−1)!\log n)` a saddle-point evaluation gives
`Σ_r √(π_r'(n)) ≍ √n·(log log n)^{1/4}`, which is **unbounded** over `√n`. My
computation of the paper's own bound:

| `n` | `Σ_r √(π_r'(n))/√n` | `Σ_r √(π_r'(n))/(√n (log log n)^{1/4})` |
|---|---|---|
| 10^4 | 1.55085 | 1.27047 |
| 10^6 | 1.67269 | 1.31402 |
| 10^8 | 1.76106 | 1.34794 |

The first column is monotonically increasing with no sign of a ceiling; the
second is nearly flat. So the method *provably* cannot give `≍ √n`.

The conclusion is nevertheless true: power iteration with sparse triangular
solves gives `‖A^{-1}‖/√n = 0.850866, 0.850171, 0.849921, 0.849895, 0.849895`
at `n = 10^3 … 10^7` — dead flat. But it is not proved here.

Downstream impact is limited: everywhere `‖A^{-1}‖` is used as an *upper* bound
(the Sherman–Morrison proposition), `n^{1/2+o(1)}` would do; the Cheon–Kim
remark needs only the *lower* bound `‖A^{-1}‖ ≥ ‖μ_n‖ ≍ √n`, which is solid.
**Suggested repair: weaken the theorem to `‖A_n^{-1}‖ = n^{1/2+o(1)}`,
`σ_min(A_n) = n^{-1/2+o(1)}`, or prove the missing `O(√n)` upper bound.**

Related overstatement (Open Problem 2, line 580): "`‖A_n^{-1}‖` is already
attained by its first column, namely `‖μ_n‖`". It is not: measured
`‖A^{-1}‖/‖μ_n‖ = 1.090031` at `n = 10^7`, stable, i.e. **9% above** the first
column, not attained. "Attained up to a constant factor" is what is true.

## 11. Theorem 4, non-normality gap `σ_max/|λ_max| ≍ √log n` — **CONFIRMED-CORRECT**

Given `\eqref{eq:kline1}` (cited to `[kline584]`, outside my remit),
`|λ_max| = (1+o(1))√π(n)` and `σ_max/|λ_max| = √(n/π(n))(1+o(1)) ≍ √log n`.
Verified with actual dense eigenvalues: `σ_max/|λ_max| = 1.9063, 2.0871, 2.2623,
2.4394, 2.5924` at `n = 400 … 6400`, matching the paper's `1.906, 2.087, 2.262,
2.440, 2.592` and `√log n = 2.448 … 2.960`.

One comparison I flag but cannot settle: the abstract calls this "markedly
smaller than the `Θ(√n)` gap of the denser matrices of [kline584]". The
supporting note (`§5c`, Corollary 5) describes that `Θ(√n)` as the gap "between
smallest eigenvalue and smallest singular value" of `H̄^{(s)}_n` — a **bottom-end**
quantity, whereas `σ_max/|λ_max|` is a top-end one. If so, the abstract is
comparing two different things. Needs checking against `[kline584]`.

## 12. Remark, "a hierarchy of cheaper bounds" — exponents **CONFIRMED**; derivation has a **GAP**

I re-derived all three exponents from scratch and they are right.

- Single index `j = p ≈ n^{1/3}`: `|w_p| = π(n/p) − π(p) − 1 ≈ 1.5 n^{2/3}/log n`
  (measured `303.0 / 1193.0 / 4611.0` at `n = 10^5/10^6/10^7`; the model gives
  `4300` at `10^7`). Then `σ_min ≤ |M(n)|/(‖μ‖·|w_p|) = |M(n)|·n^{-7/6+o(1)}`. **7/6 ✔**
- Family `n^{1/3} ≤ p ≤ n^{1/2}`: `‖Qw‖ ≈ 2.6 n^{5/6}/log^{3/2}n` (measured
  `841.0 / 4871.7 / 27242.0`; model `2.6·n^{5/6}/log^{3/2}n = 10500·2.6` at
  `10^7`). Then `σ_min ≤ |M(n)|·n^{-4/3+o(1)}`. **4/3 ✔**
- With `|M(n)| ≪ n\exp(−c√{\log n}) = n^{1−o(1)}`: `σ_min ≪ n^{-1/3+o(1)}`. **1/3 ✔**

**Gap in the derivation.** `‖R^{-1}‖ ≥ ‖R^{-1}Q‖` is fine, but converting
`‖R^{-1}Q‖` into `‖μ‖‖Qw‖/|M(n)|` again needs the rank-one part to beat
`‖A^{-1}Q‖`, and the paper supplies nothing for that step. With the crude
`‖A^{-1}Q‖ ≤ ‖A^{-1}‖ ≍ √n` the family bound would require `|M(n)| ≪ n^{5/6}` —
not unconditional. Two extra facts (both true, neither stated) fix it:
  1. For `j = p` prime the columns of `A^{-1}` have **pairwise disjoint support**,
     because `k` lies in column `p` iff `p = P^-(k)`. Hence
     `‖A^{-1}Q‖ = max_p \sqrt{1+π(n/p)−π(p)} ≈ 1.22 n^{1/3}/\sqrt{\log n}`, and the
     domination then needs only `|M(n)| ≪ n/\log n` — which PNT with the classical
     zero-free region supplies. So the `n^{-4/3}` and `n^{-1/3}` bounds **are**
     unconditional, once this is said.
  2. For the single index, project on `μ` instead of using the triangle
     inequality: `μ^T A^{-1}e_p = −(1+π(n/p)−π(p))`, against
     `‖μ‖² w_p/M(n) ≈ 0.61 n·w_p/M(n)`, and `n/|M(n)| → ∞` by PNT. So the
     `n^{-7/6}` bound is also unconditional — but again only after this is said.

As printed, the remark asserts three unconditional bounds whose proofs are one
ingredient short each. Cheap to fix; must be fixed.

## 13. Remark (Cheon–Kim) — **CONFIRMED-CORRECT**

`|M(n)| = |det(L + uv^T)| = |1 + v^T L^{-1} u| ≤ 1 + \sqrt{n−1}/σ_min(L)` follows
in one line from Sherman–Morrison; the Li–Mathias citation is not needed (no
error, just heavier machinery than required). The negative answer for this family
needs only `‖A^{-1}‖ ≥ ‖μ_n‖ ≍ √n`, which is solid, so this remark survives §10.
Quantity `1 + \sqrt{n−1}/σ_min(A_n) = 427.3, 851.4, 1699.4, 2551.6` at
`n = 500,1000,2000,3000` — matches the paper's `427, 851, 1699, 2552` exactly.

## 14. Remark, "`R_n` singular exactly when `M(n) = 0`, which occurs infinitely often" — **CONFIRMED-CORRECT** (citation missing)

`det R_n = M(n)` gives the first half. The second half is true but is a genuine
theorem, not an observation: it follows from `M(x) = Ω_±(x^{1/2})` plus the fact
that `M(n) − M(n−1) = μ(n) ∈ {−1,0,1}` forces a zero at every sign change. The
paper asserts it bare. Add a citation.

## 15. Remark (the refined shape) — **CONFIRMED as honestly labelled open**

Correctly marked "not established"; the reason given (Alladi Thm 1's main term
sinks below its error for large `α`; Alladi Thm 2 has half the true exponent) is
consistent with what I found independently in §6, where the same obstruction
blocks the `(1+o(1))`. Good faith.

## 16. §"Numerical remarks", the interval `[0.999, 1.008]` — **WRONG**

> "the ratio `σ_min(R_n)‖μ_n‖‖w‖/|M(n)|` equals `0.9896, 1.0038, 1.0047` at
> `n = 500,1000,2000`, and lies in `[0.999,1.008]` for `200 ≤ n ≤ 3200`."

The first list I reproduce exactly (`0.98964, 1.00382, 1.00470`). The interval is
false — and is contradicted by the paper's own `0.9896` three words earlier.
Sweeping `n = 200, 225, …, 3200` (114 values with `M(n) ≠ 0`):

- **actual range `[0.98712, 1.02664]`** (min at `n = 300`, `M(n) = −5`; max at
  `n = 225`, `M(n) = 3`);
- **68 of 114** sampled `n` fall below `0.999`; **12 of 114** exceed `1.008`.

The same false interval appears in `proofs/smallest-singular-value.md` §1. The
honest statement is `[0.987, 1.027]` on that range. (The deviation is signed:
ratio `< 1` when `M(n) < 0`, `> 1` when `M(n) > 0` — the `A^{-1}` correction has a
definite sign, which is mildly interesting and would be worth a sentence.)

## 17. Other numerical claims — **all reproduced**

Every other printed number reproduces exactly under my independent construction:
`‖μ_n‖/√n = 0.7810, 0.7794, 0.7818, 0.7814, 0.7800` (at `n = 200,400,800,1600,3200`
— the `n` values are **not stated in the paper**; please state them);
`σ_max/√n` five values; `σ_max/|λ_max|` five values; nilpotency index `5,5,5,6`;
`‖A^{-1}‖/√n = 0.853,0.851,0.849,0.850`; `σ_min(A)√n = 1.1717,1.1753,1.1773,1.1760`;
Cheon–Kim `427,851,1699,2552`; dense-vs-closed-form residual exactly `0`;
Table 1 in full; `‖w‖/n^{3/4}` including the break at `3·10^6` (`0.40951`).

Two further checks of §"severely pre-asymptotic":
- `‖w‖(\log n)^{1.13}/n^{5/6} = 2.4671, 2.4922, 2.4977, 2.5042, 2.5119` — matches
  the note, monotone increasing, so the "false stability" claim is sound.
- The `α = 3` vs `α = 2` crossover: my own Dickman-model computation gives
  `\log n = 27.70`, i.e. `n = 1.07·10^{12}`. The paper's "near `n = 10^{12}`" is
  **confirmed**. (Note this is a *different* quantity from the unadjudicated
  `\log n = 18` vs `24.79` threshold discrepancy recorded in the proof note §6,
  which the paper drops silently.)
- Mild data-selection issue: the paper prints mass-mean `β = 0.3368, 0.3364,
  0.3361, 0.3351` "at `n = 10^5,…,10^7`" and calls it "already drifting, and
  accelerating". Those are my `n = 10^5, 10^6, 3·10^6, 10^7`; the omitted
  `n = 3·10^5` value is `0.3354`, which breaks monotonicity
  (`0.3368, 0.3354, 0.3364, 0.3361, 0.3351`). The trend is real but noisier than
  presented, and `3·10^5` *is* a row of Table 1. Either print all six or say
  which are shown.

## 18. Circularity and forward references — **no circularity**

The Sherman–Morrison proposition (§4) invokes Theorem 4 (§5) for
`‖A^{-1}‖ ≍ √n`. I traced Theorem 4's proof: it uses only `\eqref{eq:kline1}`
(cited), the Schur test, `ω_max(n) ~ \log n/\log\log n`, and Theorem
`thm:588` (cited). It does **not** use the proposition, Theorem 2, or Theorem 3.
So this is a forward reference, not a circle. It should still be flagged in the
text or the sections reordered; a referee reading linearly will stumble.

## 19. Definitions and code/paper consistency — consistent

- `M(x,y)` with `P^-(1) = ∞`: consistent throughout, and consistent with
  `M(x,y) = 1` for `y ≥ x`. ✔
- `α` used uniformly in the paper (the proof note uses `u`; no leakage into the
  paper). ✔ `α = \log x/\log y` matches Alladi's `α` in `y = x^{1/α}`. ✔
- `\eqref{eq:alladi2}`: `xρ'(α)/\log y = αxρ'(α)/\log x = −xρ(α−1)/\log x` ✔, and
  absorbing Alladi's `y/\log y` into `O_α(1/\log y)` is legitimate at fixed
  `α > 1` (`y/x = x^{1/α−1} → 0` polynomially). The `O_α` subscript is correctly
  retained. ✔
- **The matrix built by `code/wnorm.py` matches `\eqref{eq:defA}`** — I rebuilt
  `A` and `R` from the paper's definition and got residual `0` against the closed
  form, and reproduced every table. The only silent assumption is `P(1) := 1`
  (Defect 1 above). ✔
- Nonzero count `≈ 2.61n`: `n + (n−1) + (6n/π² − 1) = 2.6079n + O(1)` ✔. Minor:
  "one for each squarefree `i ≤ n`" should read `i ≥ 2`, and Redheffer's nonzero
  count is `Σ_{i≤n}d(i) + n − 1`, not `Σ_{i≤n}d(i)`. Both harmless.

---

## Must-fix list (ordered by severity)

1. **`\eqref{eq:factorisation}`'s `(1+o(1))` is not unconditional** (§6). Restate
   with the explicit error `O(|M(n)|/‖w‖)`, or add the hypothesis. The
   consequence for Theorem 3 (§7) — that the *upper* half of
   `σ_min = |M(n)|n^{-3/2+o(1)}` is conditional while the RH equivalence is not —
   must be stated. The abstract's "two-sided and unconditional" is fine for the
   equivalence but not for the displayed asymptotic above it.
2. **Theorem 4's `O(1/n)` is not proved** (§9). Statement true; insert the
   `RR^T = [[n,b^T],[b,C]]` argument, or weaken to `1+O(1/\sqrt{\log n})`.
3. **Theorem 4's `‖A_n^{-1}‖ ≍ √n` is not proved** (§10) — the paper's own proof
   yields `n^{1/2+o(1)}`, and the method provably cannot do better
   (`Σ_r\sqrt{π_r'} ≍ √n(\log\log n)^{1/4}`, demonstrated numerically).
   Weaken, or prove the missing bound.
4. **The false interval `[0.999,1.008]`** (§16) — true range on that sweep is
   `[0.987, 1.027]`; the paper contradicts itself.
5. **The swapped "forward/reverse" sentence** in Theorem 3's proof (§8).
6. **Theorem 1's `‖w‖²` display is wrong at `j = 1`** and `P(1)` is undefined (§1).
7. **The hierarchy remark's three bounds each need one more ingredient** to be
   unconditional (§12); both repairs supplied above.
8. Minor: "at least `y²`" → "greater than `y²`" (§2); `M(n)=0` i.o. needs a
   citation (§14); "attained by its first column" is a 9% overstatement (§10);
   state the `n` values behind the `‖μ_n‖/√n` list (§17); check the abstract's
   `Θ(√n)` comparison against `[kline584]` (§11).

## Scope of this audit / what I did not check

- `[alladiJNT] Thm 1`, `[kline584] Thm 1` (`\eqref{eq:kline1}`), `[kline588]
  Thms 1,3`, `[bordellescloitre] Cor 2.7`, `[cheonkim] Thm 4.2` are taken on
  faith — verifying the literature is the attribution axis, not mine.
- Remark `rem:buchstab` (Buchstab `ω` vs Dickman `ρ'` contrast) is a citation
  claim, not audited here.
- I did not attempt the open problems, and did not try to close the §6 gap
  beyond establishing that the two obvious routes (Alladi at growing `α`;
  elementary subfamily bounds) both fail.

```
RESULTS AUDITED: 16
CONFIRMED: 9  OVERCLAIM: 2  GAP: 3  WRONG: 2
MUST-FIX BEFORE PUBLICATION:
  (1) unconditional (1+o(1)) in eq:factorisation, and the resulting conditionality
      of the upper half of Theorem 3's asymptotic;
  (2) Theorem 4 sigma_max O(1/n) unproved by its proof;
  (3) Theorem 4 ||A^{-1}|| ~ sqrt(n) unproved (proof gives n^{1/2+o(1)}, and the
      method cannot do better);
  (4) false printed interval [0.999,1.008] (true: [0.987,1.027]);
  (5) swapped forward/reverse sentence in Theorem 3's proof;
  (6) Theorem 1's ||w||^2 display wrong at j=1; P(1) undefined;
  (7) hierarchy remark: each of the three bounds is one ingredient short.
VERDICT: SOUND-WITH-REPAIRS
```

---
---

# APPENDIX (appended on coordinator request) — per-result ledger, coverage, and the `thm:main` conditional statement

*Label note for the coordinator:* the paper's actual labels are **`thm:max`**
(not `thm:smax`) and **`lem:identities`** (not `lem:ident`). The ledger below
uses the paper's own labels. The remark at line 410 (`R_n` singular iff
`M(n)=0`) carries **no label**; I refer to it as `rem:singular*`.

## A. Per-result ledger

Statement rows and proof rows are separated wherever they got different
verdicts. Scripts referenced are in this scratchpad directory.

| ID | claim (short) | outcome | evidence | must-fix? |
|---|---|---|---|---|
| `thm:closed` (stmt, display 1) | `w_j = 1` (non-sf) / `M(n/j,P(j))` (sf), less 1 at `j=1` | **CONFIRMED** | `t1.py`: dense solve of `A^T w = 1−e_1` vs closed form, `max|Δ| = 0.000e+00` at `n = 50,137,300,500,1000,2000`; independent identity `Σ_{p≤n}w_p = 1−M(n)` holds exactly at `n=500,1000,3000` | no |
| `thm:closed` (proof) | nilpotent `S`, unique parent chain, value `μ(k/j)` | **CONFIRMED** | re-derived independently; the extension of the `d`-sum from squarefree to all `d` is free (`μ(d)=0`) | no |
| `thm:closed` (stmt, display 2) | `‖w‖² = #{non-sf} + Σ_{sf j}M(n/j,P(j))²` | **WRONG** | `j=1` term is `M(n)²` as printed; true value `(M(n)−1)²`. Verified `w_1 = M(n)−1` exactly at all `n` tested (`t1.py`) | **YES** |
| `thm:closed` (hypothesis) | `P(j)` at `j = 1` | **GAP** | `P(i)` defined only for `i>1` (tex line 102); `code/wnorm.py:30` silently sets `y[0]=1`. Convention `P(1):=1` must be stated | **YES** |
| `cor:trichotomy` (stmt) | `y≥x ⇒ w_j=1`; `√x≤y<x ⇒ w_j=1−(π(x)−π(y))` | **CONFIRMED** | `t1.py`, exhaustive over **all** squarefree `j≤n`, `n=500/2000/5000`: A 286/1164/2955 indices, B 12/38/67 indices, **0 mismatches** | no |
| `cor:trichotomy` (proof) | "a composite `y`-rough number is at least `y²≥x`" | **IMPRECISE** | needs *strictly greater than* `y²` (prime factors `>y`, not `≥y`); this is what settles the boundary case `y²=x` | yes (one word) |
| `lem:identities` | Buchstab `M(x,y)=M(x)+Σ_{p≤y}M(x/p,p)`; complement form; smoothing over **all** smooth `a` | **CONFIRMED** | `t1.py`: 52 `(x,y)` pairs, `x∈{50,137,400,999,2500,4000}`, `y∈{2..101}`, **0 failures** on all three; re-proved by convolution (`1_{smooth}*μ = μ·1_{rough}`, `p^k` terms are what cancel) | no |
| `thm:norm` (stmt) | `‖w‖ = n^{1+o(1)}` unconditionally | **CONFIRMED** | upper `‖w‖ ≤ (π/√6)n = 1.2825n` re-derived; lower re-derived; Table 1 reproduced exactly (`t3.py`: `2289.3, 5211.8, 12850.5, 29519.5, 73972.3`) | no |
| `thm:norm` (proof, `α→∞`) | implied constant depends on `α`, then `α→∞` | **CONFIRMED** | no limit interchange: `α = α(ε)` is *chosen* then frozen, so `C_ε := C_{α(ε)}`, `n_ε` are constants. Also checked: `ρ'` continuous on `(1,∞)`, so `α+O(1/\log n)` is harmless; Alladi's `y/\log y` term is `O(x^{1/α})`, negligible at fixed `α>1` | no |
| `prop:sm` (inverse formula) | `R^{-1} = A^{-1} − μ w^T/M(n)`, `M(n)≠0` | **CONFIRMED** | `t8.py`: `A^{-1}e_1 = μ_n` to residual `0.00e+00` at `n=200,400,800,1600`; `1+(1−e_1)^TA^{-1}e_1 = M(n)` from `w_1=M(n)−1`. Also re-proves `det R_n = M(n)` in one line | no |
| `prop:sm/`**`eq:factorisation`** | `σ_min·‖μ‖·‖w‖ = |M(n)|(1+o(1))`, asserted unconditional | **GAP** | relative error `= ‖A^{-1}‖·|M(n)|/(‖μ‖‖w‖) ≍ 1.090·|M(n)|/‖w‖` (constants measured `t5.py`: `0.849895/0.779698 = 1.090031`). Unconditional bounds `‖w‖ ≫_ε n^{1−ε}` and `|M(n)| ≪ n e^{−c(\log n)^{3/5}…}` **do not cross**. Alladi at growing `α` gives only `‖w‖ ≫ n e^{−CL\log\log L/\log L}`, which decays *faster* than the `M` bound since `L/\log L ≫ L^{3/5}` | **YES** |
| `thm:main` (lower half) | `σ_min ≫ |M(n)|n^{−3/2+o(1)}` | **CONFIRMED** | `‖R^{-1}‖ ≤ ‖A^{-1}‖ + ‖μ‖‖w‖/|M(n)| ≤ 1.88 n^{3/2}/|M(n)|` using only `|M(n)|≤n`, `‖w‖≤1.2825n`. Unconditional | no |
| `thm:main` (upper half) | `σ_min ≪ |M(n)|n^{−3/2+o(1)}` | **GAP** | inherits `prop:sm` in full: every lower bound on `‖R^{-1}‖` I could construct needs `‖w‖ ≫ |M(n)|`. Cheap substitutes all fail: `‖w‖² ≥ M(n)²+0.3921n` needs `|M(n)| ≲ 1.43√n`; adding regime-B primes (`‖Qw‖ ≍ 2.6n^{5/6}/\log^{3/2}n`, measured) needs `|M(n)| ≪ n^{5/6}` | **YES** |
| `thm:main` (RH equivalence) | `RH ⟺ σ_min ≪_ε n^{−1+ε}` | **CONFIRMED** | `⟸` uses only `|M(n)| ≤ 1.88σ_min n^{3/2}` (unconditional, no `(1+o(1))`). `⟹`: under RH, `|M(n)|/‖w‖ ≪ n^{1/2+ε}/n^{1−ε} → 0`, so the `(1+o(1))` is available from the hypothesis itself | no |
| `thm:main` (proof, last sentence) | "forward direction uses only the elementary upper bound on `‖w‖`; the reverse is what Thm 2 buys" | **WRONG** | directions swapped, and contradicts the paper's own two preceding sentences. `proofs/smallest-singular-value.md` §5 has it right (`⟸` uses the trivial upper bound) — transcription error introduced in the paper | **YES** |
| `thm:max` (stmt: `σ_max`) | `σ_max(R_n) = √n(1+O(1/n))` | **CONFIRMED (true)** | I supply a proof (below) and confirm numerically: `t4.py`, `λ_max(RR^T)−n = 3.101, 3.059, 3.017, 2.977, 2.951, 2.913, 2.891, 2.867` at `n = 400…10^6`, converging to `‖b‖²/n → 1+3(6/π²) = 2.8238` | no |
| `thm:max` (proof: `σ_max`) | `σ_max ≤ √n+1+√(π(n))` ⟹ `1+O(1/n)` | **OVERCLAIM** | printed proof delivers `√n(1+O(1/\sqrt{\log n}))` only — short by a factor `n/\sqrt{\log n}`. Repair: `G=RR^T=[[n,b^T],[b,C]]`, `‖b‖²≤4n`, `‖C‖≤(1+\sqrt{π(n)})²=o(n)`, `λ = n+b^T(λI−C)^{-1}b ≤ n+4+o(1)` | **YES** |
| `thm:max` (step: `‖S‖`) | `‖S‖ = \sqrt{π(n)}` exactly, via Schur + star | **CONFIRMED** | `S^TS = diag(#children)` **exactly** (unique parent ⇒ `S(i,j)S(i,j')≠0` forces `j=j'`); max child count `π(n)` at the root. `t2.py`: `‖S‖ = 9.74679, 12.96148, 17.40690, 20.73644` vs `\sqrt{π(n)} = 9.74679, 12.96148, 17.40690, 20.73644` | no |
| `thm:max` (stmt: non-normality) | `σ_max/|λ_max| ≍ \sqrt{\log n}` | **CONFIRMED** | given `eq:kline1`. `t2.py` dense eigenvalues: `1.9063, 2.0871, 2.2623, 2.4394, 2.5924` at `n=400…6400` vs `\sqrt{\log n} = 2.448…2.960`; `\sqrt{n/π(n)} → \sqrt{\log n}` | no |
| `thm:max` (stmt: `‖A^{-1}‖`) | `‖A_n^{-1}‖ ≍ √n`, `σ_min(A_n) ≍ n^{−1/2}` | **UNVERIFIABLE (analytically)** | true in every computation: `t5.py`, `‖A^{-1}‖/√n = 0.850866, 0.850171, 0.849921, 0.849895, 0.849895` at `n=10^3…10^7`, flat. But **I have no proof either**, and none is in the paper | no (the *proof* row is) |
| `thm:max` (proof: `‖A^{-1}‖`) | `Σ_r\sqrt{π_r'(n)} = n^{1/2+o(1)}` ⟹ `≍√n` | **OVERCLAIM** | the paper writes `n^{1/2+o(1)}` itself, which does not imply `≍`. The method *provably* cannot: `t5.py`, `Σ_r\sqrt{π_r'(n)}/√n = 1.55085, 1.61686, 1.67269, 1.72029, 1.76106` at `n=10^4…10^8`, monotone increasing; `/(√n(\log\log n)^{1/4}) = 1.270, 1.293, 1.314, 1.332, 1.348`, nearly flat — i.e. the bound is `≍ √n(\log\log n)^{1/4}` | **YES** |
| `thm:max` (step: Neumann termination) | `S^{ω_max+1}=0`, `ω_max ~ \log n/\log\log n`, col sums of `S^r` `= π_r'(n)` | **CONFIRMED** | `t2.py` nilpotency index `5,5,5,6` at `n=500,1000,2000,3000` (matches paper); col sum at `j=1` is `π_r'(n)` and `j>1` injects into it, so `π_r'` is the max — re-derived | no |
| `rem:hierarchy` (exponent `7/6`) | single index `p≈n^{1/3}` ⟹ `σ_min ≪ |M(n)|n^{−7/6+o(1)}` | **CONFIRMED** | `t3.py`: `|w_p| = 303.0, 1193.0, 4611.0` at `n=10^5,10^6,10^7` vs model `1.5n^{2/3}/\log n = 4300` at `10^7`; exponent re-derived independently | no |
| `rem:hierarchy` (exponent `4/3`) | family `n^{1/3}≤p≤n^{1/2}` ⟹ `≪|M(n)|n^{−4/3+o(1)}` | **CONFIRMED** | `t3.py`: `‖Qw‖ = 841.0, 4871.7, 27242.0`, matching `2.6n^{5/6}/\log^{3/2}n`; exponent re-derived | no |
| `rem:hierarchy` (exponent `1/3`) | with `M(n) ≪ n e^{−c\sqrt{\log n}}` ⟹ `σ_min ≪ n^{−1/3+o(1)}` | **CONFIRMED** | `n^{1−o(1)}·n^{−4/3+o(1)}`; re-derived | no |
| `rem:hierarchy` (domination step) | `‖R^{-1}Q‖ ⟹ ‖μ‖‖Qw‖/|M(n)|` | **GAP** | with only `‖A^{-1}Q‖ ≤ ‖A^{-1}‖ ≍ √n` the family bound needs `|M(n)| ≪ n^{5/6}` — not unconditional. Two missing (true) ingredients supplied in §12: (a) for `j=p` prime the `A^{-1}` columns have **disjoint supports** (`k` is in column `p` iff `p = P^-(k)`), giving `‖A^{-1}Q‖ ≈ 1.22n^{1/3}/\sqrt{\log n}` and requiring only `|M(n)| ≪ n/\log n`; (b) for the single index, project on `μ`: `μ^TA^{-1}e_p = −(1+π(n/p)−π(p))` against `0.61n·w_p/M(n)`, and `n/|M(n)|→∞` by PNT | **YES** |
| `rem:cheonkim` | `|M(n)| ≤ 1+\sqrt{n−1}/σ_min(L_n)`; criterion fails for this family | **CONFIRMED** | inequality is one line of Sherman–Morrison (`|1+v^TL^{-1}u| ≤ 1+‖v‖‖u‖‖L^{-1}‖`); Li–Mathias not needed. Needs only the *lower* bound `‖A^{-1}‖ ≥ ‖μ_n‖ ≍ √n`, so it survives the `thm:max` overclaim. `t2.py`: `427.3, 851.4, 1699.4, 2551.6` vs paper `427, 851, 1699, 2552` | no |
| `rem:singular*` | `R_n` singular iff `M(n)=0`; occurs infinitely often | **CONFIRMED** | first half from `det R_n = M(n)`; second half true but is a theorem (`M(x)=Ω_±(x^{1/2})` + `M(n)−M(n−1)=μ(n)∈{−1,0,1}` forces a zero at each sign change), asserted bare | yes (citation) |
| `rem:shape` | refined shape `n\exp(−(1+o(1))\sqrt{\log n\log\log n})` is **not** established | **CONFIRMED** | honestly labelled open; the obstruction given (Alladi Thm 1's main term sinks below its error for large `α`) is the same one I hit independently in §6 | no |
| `rem:bc` | description of Bordellès–Cloitre Cor 2.7 | **UNVERIFIABLE** | literature claim; attribution axis, not mine | no |
| `rem:buchstab` | `Φ(x,y)`/Buchstab `ω` vs `μ`-weighted/Dickman `ρ'` contrast is Alladi's | **UNVERIFIABLE** | citation claim; attribution axis | no |
| `thm:alladi` | Alladi JNT 14 (1982) Thm 1, uniform `2≤y<x` | **UNVERIFIABLE** | cited, not proved here; taken on faith | no |
| `thm:588` | `det BB^T = ‖l‖²`; `l = μ_n`; `‖μ_n‖² = 6n/π²+O(√n)` | **CONFIRMED (numerically)** | `t8.py`: `\sqrt{\det BB^T} = ‖μ_n‖` to 6 s.f. at `n=200,400,800,1600` (`11.045361/11.04536`, …); `A^{-1}e_1 = μ` residual `0` | no |
| `eq:kline1` | `r_± = 1 ± \sqrt{π(n)} + \tfrac12 π_2'(n)/π(n) + …` | **CONFIRMED (numerically)** | `t8.py`: `|λ_max| − (1+\sqrt{π(n)}) = 0.564, 0.700, 0.788, 0.855` at `n=200,400,800,1600`; the second-order term `π_2'(1600)/(2π(1600)) ≈ 0.86` matches. Proof is cited to `[kline584]` | no |
| `eq:alladi2` | `M(x,x^{1/α}) = −(x/\log x)ρ(α−1)(1+O_α(1/\log y))` | **CONFIRMED** | `αρ'(α) = −ρ(α−1)` gives the rewrite exactly; absorbing Alladi's `y/\log y` into `O_α` is legitimate at fixed `α>1` since `y/x = x^{1/α−1}`. `O_α` subscript correctly retained | no |
| `eq:compare` | `\mathrm{dist}(\mathbf 1^T,\mathrm{rowspan}B) = |M(n)|/‖μ_n‖` | **CONFIRMED** | `t8.py`, least-squares residual vs `|M(n)|/‖μ_n‖`: `0.72428597/0.72428597`, `0.06415003/0.06415003`, `0.04522156/0.04522156`, `0.22394984/0.22394984` — agreement to 8 d.p. (the `σ_min` half of the display inherits the `thm:main` upper-half gap) | no |
| `eq:defA` + nonzero count | `≈2.61n` nonzeros | **IMPRECISE** | `n+(n−1)+(6n/π²−1) = 2.6079n+O(1)` ✓. Nits: "one for each squarefree `i ≤ n`" should be `i ≥ 2`; Redheffer's count is `Σ_{i≤n}d(i)+n−1`, not `Σ_{i≤n}d(i)` | no |
| `§numerics` interval | ratio "lies in `[0.999,1.008]` for `200≤n≤3200`" | **WRONG** | `t6.py`, 114 values (`n=200,225,…,3200`, `M(n)≠0`): true range **`[0.98712, 1.02664]`** (min `n=300`, `M(n)=−5`; max `n=225`, `M(n)=3`); **68/114** below `0.999`, **12/114** above `1.008`. Contradicted by the paper's own `0.9896` three words earlier. Same error in `proofs/…md` §1 | **YES** |
| `§numerics` all other values | `σ_max/√n`, `σ_max/|λ_max|`, `‖μ_n‖/√n`, `‖A^{-1}‖/√n`, `σ_min(A)√n`, nilpotency, Cheon–Kim, residual `0`, Table 1 | **CONFIRMED** | every value reproduced exactly under independent construction (`t1.py`–`t4.py`). Nit: the `n` values behind the `‖μ_n‖/√n` list are not stated (they are `200,400,800,1600,3200`) | yes (state the `n`) |
| `§preasymptotic` crossover | `α=3` overtakes `α=2` "near `n=10^{12}`" | **CONFIRMED** | `t7.py`, my own Dickman-model computation: sign change at `\log n = 27.70`, i.e. `n = 1.07·10^{12}`. (Distinct from the unadjudicated `\log n = 18` vs `24.79` threshold in `proofs/…md` §6, which the paper drops silently) | no |
| `§preasymptotic` `β` drift | mass-mean `β = 0.3368,0.3364,0.3361,0.3351`, "drifting and accelerating" | **IMPRECISE** | `t7.py` reproduces those four, but they are `n=10^5,10^6,3·10^6,10^7`; the omitted `n=3·10^5` value is `0.3354`, breaking monotonicity (`0.3368, 0.3354, 0.3364, 0.3361, 0.3351`). `3·10^5` *is* a row of Table 1. Trend is real but noisier than presented | yes (print all six or say which) |
| `§preasymptotic` false stability | `‖w‖(\log n)^{1.13}/n^{5/6}` looks stable but rises at every step | **CONFIRMED** | `t7.py`: `2.4671, 2.4922, 2.4977, 2.5042, 2.5119`, monotone increasing | no |
| Open Problem 2 | "`‖A_n^{-1}‖` is already attained by its first column, namely `‖μ_n‖`" | **IMPRECISE** | `t5.py`: `‖A^{-1}‖/‖μ_n‖ = 1.090031` at `n=10^7`, stable — 9% above, not attained. True statement: "attained up to a constant factor" | yes |
| Abstract | gap "markedly smaller than the `Θ(√n)` gap of the denser matrices of [kline584]" | **UNVERIFIABLE** | `proofs/…md` §5c describes that `Θ(√n)` as between *smallest* eigenvalue and *smallest* singular value — a bottom-end quantity, while `σ_max/|λ_max|` is top-end. If so the abstract compares two different things. Needs `[kline584]` | yes (check) |
| Forward reference | `prop:sm` (§4) cites `thm:max` (§5) | **CONFIRMED (not circular)** | traced `thm:max`'s proof: uses only `eq:kline1`, Schur test, `ω_max ~ \log n/\log\log n`, `thm:588`. No dependence on `prop:sm`, `thm:norm`, or `thm:main` | yes (flag or reorder) |

**Ledger tally (statement-level, matching the summary block above):**
9 CONFIRMED · 2 OVERCLAIM · 3 GAP · 2 WRONG.
The extra rows above (proof steps, cited results, `IMPRECISE`/`UNVERIFIABLE`
items) are sub-rows and support rows, not additional headline verdicts:
44 ledger rows in total, of which 5 `IMPRECISE` and 4 `UNVERIFIABLE`.

## B. Coverage

**Denominator.** 15 numbered environments (shared counter): Thm 1 `thm:closed`,
Thm 2 `thm:norm`, Thm 3 `thm:main`, Thm 4 `thm:max`, Thm 5 `thm:alladi`,
Rem 6 `rem:buchstab`, Thm 7 `thm:588`, Cor 8 `cor:trichotomy`,
Lem 9 `lem:identities`, Rem 10 `rem:shape`, Prop 11 `prop:sm`,
Rem 12 `rem:singular*`, Rem 13 `rem:hierarchy`, Rem 14 `rem:bc`,
Rem 15 `rem:cheonkim`.
Plus **23 load-bearing unnumbered steps**: `eq:defA` + nonzero count; `eq:defw`;
`A^{-1}e_1 = μ_n`; `det R_n = M(n)`; `eq:kline1`; `eq:alladi2`; `eq:compare`;
`eq:rh`; proof of `thm:closed` (path/nilpotency); `thm:norm` upper; `thm:norm`
lower + `α→∞`; `thm:main` forward; `thm:main` reverse; `thm:main` final
attribution sentence; `prop:sm` SM identity; `prop:sm` domination;
`thm:max` `‖S‖` Schur step; `thm:max` `σ_max` upper bound; `thm:max`
non-normality; `thm:max` Neumann termination + `Σ_r\sqrt{π_r'}`;
`rem:hierarchy` domination step; §numerics; §preasymptotic.
**Total 38.**

**Audited: 36 of 38 in full; 2 partially.**

**Not reached, explicitly:**
1. `thm:alladi` — Alladi JNT 14 (1982) Thm 1 taken on faith; I did not read the
   source or reconstruct the proof. (Attribution axis.)
2. `rem:buchstab` and `rem:bc` — pure literature-description claims (the
   `Φ`/`ω` vs `ρ'` contrast; Bordellès–Cloitre Cor 2.7 and their quoted remark).
   Not verifiable without the sources.
3. `eq:kline1` — I corroborated it numerically to second order but did **not**
   verify `[kline584] Thm 1`'s proof.
4. `thm:588` — both assertions verified numerically; the proof in `[kline588]`
   not read.
5. The abstract's `Θ(√n)` comparison to `[kline584]`'s denser matrices — flagged
   as possibly comparing a top-end ratio to a bottom-end one; **undecided**.
6. The three **Open Problems** (§7) — no verifiable claims except the "attained
   by its first column" phrase, which I did check (ledger row above).
7. §"What is cited and what is proved" claims about the contents of
   `audit/reports/` — I did not open that directory.
8. I did **not** attempt to close the `prop:sm` gap beyond establishing that the
   two natural routes (Alladi at growing `α`; elementary subfamily bounds) both
   fail; a third route may exist.

## C. `thm:main` — exact conditional status (paste-ready)

Write `W := ‖w‖`, `m := |M(n)|`. The whole question is the size of
`‖A_n^{-1}‖·m/(‖μ_n‖W) ≍ 1.090·m/W` (constants measured, `t5.py`).

**Unconditional (needs nothing beyond `‖w‖ ≤ 1.2825n`, `‖μ_n‖ ≤ √n`, `|M(n)| ≤ n`, `‖A^{-1}‖ = n^{1/2+o(1)}`):**
```
        sigma_min(R_n)  >=  |M(n)| · n^{-3/2+o(1)} .                        (i)
```
**Conditional on `|M(n)|/‖w‖ → 0` (equivalently on the rank-one term dominating `‖A_n^{-1}‖`):**
```
        sigma_min(R_n)  <=  |M(n)| · n^{-3/2+o(1)} ,                       (ii)
```
and only then does the two-sided `σ_min(R_n) = |M(n)|n^{-3/2+o(1)}` hold.
The hypothesis `|M(n)|/‖w‖ → 0` follows from RH, and more generally from
`M(n) ≪ n^{1−δ}` for any fixed `δ > 0`. It does **not** follow from Theorems
`thm:norm` and `thm:max` as cited: `‖w‖ ≫_ε n^{1−ε}` and
`|M(n)| ≪ n\exp(−c(\log n)^{3/5}(\log\log n)^{−1/5})` are both `n^{1−o(1)}` and
never cross.

**The stated RH equivalence is unconditional despite the gap:** `⟸` uses only
`|M(n)| ≤ 1.88\,σ_min(R_n)\,n^{3/2}`, which is (i) rearranged; `⟹` supplies
`|M(n)| ≪ n^{1/2+ε}`, which makes `|M(n)|/‖w‖ ≪ n^{−1/2+2ε} → 0` and hence
licenses (ii) from within the hypothesis.

### Recommended replacement text

**Yes — the honest fix is to weaken the displayed equation to a one-sided bound
plus a conditional converse.** Exact replacements:

*Proposition (`prop:sm`), replace `\eqref{eq:factorisation}` by:*
> Suppose `M(n) ≠ 0`. Then
> `\bigl|\;\|\Rc_n^{-1}\| - \|\mu_n\|\|w\|/|M(n)|\;\bigr| \le \|\Ac_n^{-1}\|`, and hence
> `\sigma_{\min}(\Rc_n)\,\|\mu_n\|\,\|w\| = |M(n)|\bigl(1+O(|M(n)|/\|w\|)\bigr)`.
> In particular the error is `o(1)` as soon as `\|w\|/|M(n)|\to\infty`, which holds
> under RH and, more generally, whenever `M(n)\ll n^{1-\delta}` for some fixed `\delta>0`.

*Theorem 3 (`thm:main`), replace the first display by:*
> Unconditionally,
> `\sigma_{\min}(\Rc_n)\;\ge\;|M(n)|\,n^{-3/2+o(1)}`, and
> `\sigma_{\min}(\Rc_n)\;\ll\;|M(n)|\,n^{-4/3+o(1)}`.
> If moreover `|M(n)|/\|w\|\to0` — in particular under RH, or under
> `M(n)\ll n^{1-\delta}` for some fixed `\delta>0` — then
> `\sigma_{\min}(\Rc_n)=|M(n)|\,n^{-3/2+o(1)}`.
> Unconditionally, `\mathrm{RH}\iff\sigma_{\min}(\Rc_n)\ll_\varepsilon n^{-1+\varepsilon}`.

The second unconditional inequality is the repaired `rem:hierarchy` family bound
(§12(a) above: disjoint column supports plus `|M(n)| ≪ n/\log n` from PNT with
the classical zero-free region). So the *unconditional* truth the paper can
assert two-sidedly is the bracket
```
        |M(n)| n^{-3/2+o(1)}  <=  sigma_min(R_n)  <=  |M(n)| n^{-4/3+o(1)} ,
```
collapsing to `n^{-3/2+o(1)}` exactly when `|M(n)|/‖w‖ → 0`. The abstract's
"two-sided and unconditional" should be attached to the RH **equivalence** only,
not to the displayed asymptotic printed above it.
