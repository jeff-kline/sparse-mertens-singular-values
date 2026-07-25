# Audit ledger

Adversarial audit of `paper/sparse-mertens-singular-values.tex`, run 2026-07-25
as five cold agents on disjoint axes, each tasked to break its axis rather than
summarize it. Every axis returned a per-claim table with stable IDs and decisive
evidence; those tables are the detailed record and live in `audit/reports/`.
This file is the index and the resolution status.

## Verdicts

| Axis | Report | Verdict | Checked | Defects |
|---|---|---|---|---|
| Mathematics | [audit-math.md](reports/audit-math.md) | SOUND-WITH-REPAIRS | 38 items, 36 in full | 2 OVERCLAIM, 3 GAP, 2 WRONG |
| Citations | [audit-citations.md](reports/audit-citations.md) | NEEDS-CORRECTION | 50 attribution claims | 1 MISQUOTED, 2 OVERSTATED, **0 uncited borrowings** |
| Numerics | [audit-numerics.md](reports/audit-numerics.md) | NEEDS-CORRECTION | 73 printed numbers | 5 WRONG, 2 OVERCLAIM, 1 UNVERIFIABLE |
| Abstract | [audit-abstract.md](reports/audit-abstract.md) | NEEDS-REVISION | 19 clauses + 1 omission | 1 WRONG, 1 OVERCLAIM, 2 IMPRECISE, 1 GAP |
| Privacy | [audit-privacy2.md](reports/audit-privacy2.md) | CLEAR-TO-PUSH | 9 checks, 19 files | 0 must-fix, 0 topical contamination |

Per-claim tables: math §appendix (44 rows), citations §J (50 rows), numerics
§ADDENDUM (23 rows), abstract (19 rows), privacy (9 check rows + per-file
coverage). All include the CONFIRMED/VERIFIED rows, so each table doubles as a
coverage record.

## Must-fix items and their resolution

All verified independently by the coordinator before being applied — the
auditors' summaries were not taken at face value.

| # | Finding | Axis | Resolution |
|---|---|---|---|
| 1 | `‖μ_n‖/√n` printed as `0.7810,0.7794,0.7818,0.7814,0.7800` — **fabricated**; no shipped script ever computed it | numerics | **FIXED.** True values are `0.77971` then `0.77970` throughout. Confirmed by two independent algorithms (direct `p²` sieve; `Q(n)=Σ_{d≤√n} μ(d)⌊n/d²⌋`) which agree exactly; `Q(n)−6n/π²` lies in `[−8.3,+20.0]`, whereas the printed spread needs `Q` off by `+3285` and `+7985` at `n=10⁶,3·10⁶`. |
| 2 | SM ratio "lies in `[0.999,1.008]` for `200≤n≤3200`" — false, and contradicts the paper's own printed `0.9896` three words earlier | numerics, math | **FIXED.** Replaced by the measured `[0.987,1.027]` over `n=200,225,…,3200`, extremes at `n=300` and `n=225`, with the non-monotonicity stated. Two sweeps (28-point and 114-point) agree to 6 s.f.; the coarser grid stepped over the true max. |
| 3 | Abstract's "`Θ(√n)` gap of the denser matrices of `\cite{kline584}`" — wrong three ways | abstract, citations, math | **FIXED.** (a) `pdftotext` on LAA 584 returns **zero** occurrences of "singular"; (b) the real Redheffer gap is `1.2243…1.2875` at `n=400…3200`, not `Θ(√n)=56.6`; (c) the direction is **inverted** — `ℛ_n` is the more non-normal at every `n` tested. Comparative claim removed from the abstract; measured numbers moved to §6 as data, reproducible via `spectra.py redheffer`. |
| 4 | `\bibitem{limathias}` cites the wrong paper | citations | **FIXED.** Was *The Lidskii–Mirsky–Wielandt theorem*, Numer. Math. 81 (1999) — perturbation theory, containing no determinant-of-a-sum inequality. Correct source is *The determinant of the sum of two matrices*, Bull. Austral. Math. Soc. 52 (1995) 425–429. |
| 5 | "was introduced in `\cite{kline584}`" — priority claim contradicted by its own sources | citations | **FIXED.** LAA 584 p. 410 and LAA 588 p. 226 both defer to Kline, LAA **581** (2019) 354–366. Added as `\bibitem{kline581}`; title taken verbatim from LAA 584's reference [9]. |
| 6 | Thm 4 (`thm:max`): statement `σ_max=√n(1+O(1/n))` **true**, proof delivers only `1+O(1/√log n)` | math | **FIXED** with a repaired proof, verified before adoption: on the Gram matrix, `b_k ∈ {1,2}` exactly, so `‖b‖²=3Q(n)+n−4 ≤ 4n`, `‖C‖ ≤ (1+√π(n))² = o(n)`, and the Schur-complement identity gives `λ_max = n+O(1)`. Measured `λ_max(RRᵀ)−n → 2.8238 = 1+18/π²`, matching `lim‖b‖²/n`. |
| 7 | Thm 4: `‖𝒜ⁿ⁻¹‖ ≍ √n` unproved — the method **provably cannot** reach `≍` | math | **FIXED** by weakening to `n^{1/2+o(1)}` (and `σ_min(𝒜)=n^{−1/2+o(1)}`). `Σ_r√(π_r′(n))/√n = 1.55,1.62,1.67,1.72,1.76` at `n=10⁴…10⁸`, monotone increasing. Conjecture recorded with its numerical support (`0.8499`, flat to `10⁷`). Cheon–Kim answer survives: `n^{1+o(1)}` is still not `O(n^{1/2+ε})`. |
| 8 | Prop (Sherman–Morrison): the `(1+o(1))` needs `\|M(n)\|/‖w‖→0`, which is **not known unconditionally** — the best bounds do not cross | math | **FIXED.** Hypothesis added to the Proposition. Thm 3 restated as an unconditional bracket `\|M(n)\|n^{−3/2+o(1)} ≤ σ_min ≤ \|M(n)\|n^{−4/3+o(1)}` (upper bound from PNT alone, already in `rem:hierarchy`), collapsing to equality under the hypothesis. **The RH equivalence remains unconditional.** |
| 9 | Thm 3's closing sentence swaps which direction uses Thm 2 | math | **FIXED.** The *reverse* direction uses the elementary upper bounds; the *forward* is what `thm:norm` buys. |
| 10 | Thm 1's `‖w‖²` display wrong at `j=1` (gives `M(n)²`, should be `(M(n)−1)²`); `P(1)` never defined | math | **FIXED.** `j=1` split out of the sum; convention `P(1):=1` stated. |
| 11 | Buchstab contrast attributed to Alladi — "Buchstab", "ω", "Φ(x,y)" appear **nowhere** in his JNT paper | citations | **FIXED.** Alladi is now credited only with the `Ψ(x,y)`/`ρ'` contrast he actually draws (p. 87); the Buchstab comparison is marked as not his. The clause resting on the unreachable TAMS sequel is gone. |
| 12 | "All values below are produced by the scripts in `code/`" — false for 7 printed quantities; no `svd`/eigenvalue call in any of the 7 scripts, and `code/out/` empty | numerics | **FIXED** by supplying the missing code rather than weakening the claim: new `code/spectra.py` computes every singular-value, eigenvalue and nilpotency figure from explicitly built matrices. Reproduces the σ_max column exactly and `det = M(n)` as a build check. |

## Gates

- [x] Mathematics — all must-fix applied
- [x] Citations — all must-fix applied
- [x] Numerics — all must-fix applied; missing script supplied
- [x] Abstract — rewritten; Thm 2 (`‖w‖=n^{1+o(1)}`) restored, having been absent though the body calls it "the content"
- [x] Privacy — CLEAR-TO-PUSH, 9/9
- [x] Paper rebuilds — 0 errors, 0 undefined references, 12 pp.
- [ ] **Commit authorization from the author** — required before any `git commit`

## Refuted, so it is not re-derived

- `‖w‖ ≍ C·n^{3/4}` — stable to four figures over `10⁵–10⁶` (`0.40711, 0.40658, 0.40637`), then breaks at `3·10⁶` (`0.40951`). Local exponent climbs monotonically past `3/4`.
- `‖w‖` as a cancellation-free counting quantity — the model `w_j ≈ 1−(π(x)−π(y))` overshoots by `34×→516×`, growing.
- `‖w‖(log n)^{1.13}/n^{5/6}` "stable to under 1%" — strictly increasing at every step (`2.467038→2.519324`). Stability of a ratio is not convergence; check monotonicity, not spread.
- The Bohr-twist invariance of the singular spectrum — prior art (vertical limits / Hilberdink), refuted in a previous audit.

## Not checked, and why

- **Alladi, TAMS 272 (1982)** — AMS returned 403, no abstract retrievable. The one clause resting on it has been removed rather than left unsupported.
- **Hilberdink's singular-value work** — uncited. Recorded as a coverage gap, not a defect: none of this paper's results are duplicated there (he treats dense multiplicative Toeplitz matrices, obtaining `σ_r ∼ μ_r√(F(n))`, not a smallest-singular-value asymptotic for the sparse forest factor). Adding it is discretionary and presentational.
- **`thm:alladi` and `thm:588` proofs** — taken on faith from their sources; both corroborated numerically.
- **"α=3 subfamily overtakes α=2 near `n=10¹²`"** — UNVERIFIABLE. No script computes the crossover, and it is beyond feasible computation. Stated as a model prediction, not a measurement.
- **`hildtenen` range claim** — VERIFIED on bibliographic grounds only, not document-verified; the auditor downgraded its own earlier claim here rather than let it stand.

## Method notes worth keeping

- The single highest-yield privacy finding across both passes (two contaminating
  files from an unrelated project, in the previous pass) was found by reading
  files for **topical fit**, not by any keyword search. A clean grep is not
  evidence of a clean repository. This pass therefore required per-file coverage.
- Two of the twelve must-fix items (#1, #3) were numbers that had never been
  computed by anything, carried from an unreviewed scratch note into the paper.
  Both were caught only because an auditor recomputed from scratch rather than
  re-running the author's own code. Independent reconstruction, not
  re-execution, is what catches this class of defect.
