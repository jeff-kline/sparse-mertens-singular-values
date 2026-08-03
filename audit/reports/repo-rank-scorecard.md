# Independent scorecard — repo-rank pass

Run 2026-07-26 at commit `ea277de84e368e22b2af9d4fe013bfa6faed13e0` (branch
`main`, clean). Four fresh, isolated subagents graded Novelty, Depth, Reach,
and Evidence independently and in parallel — no cross-visibility between
them — each given only its own axis's rubric, pointers into this repo, and
(for Novelty/Reach) instructed to search external literature rather than
rely on memory; the Evidence agent additionally re-ran the `code/` scripts
in a fresh venv. Synthesis below is by the orchestrating session, not an
average of the four. Per the repo-rank skill's own privacy rule, numeric
scores are never written into this repository; this file records the
qualitative reasoning only. A private numeric log is kept outside this
repo's tree, in an auditor-local private score log keyed to this
same commit.

## Novelty

No external prior work was located that connects Alladi's 1982 rough-Möbius
sieve asymptotic to any singular-value or inverse-matrix statement, or that
proves a two-sided RH equivalence via `sigma_min` of an explicit
Mertens-determinant matrix. What exists in the target field (RH-equivalent
linear-algebra criteria: Redheffer, Cheon–Kim LAA 572 (2019),
Bordelles–Cloitre) is one-directional — `sigma_min -> RH`, no rate — since
2009; this repo sharpens that into a two-sided equivalence and separately
answers, negatively for this family, a question Cheon–Kim posed about their
own sufficient condition. The analytic engine itself is explicitly not
claimed as new, and the repo's own `audit/reports/prior-art-audit.md`
frames the load-bearing identification (`w_j = M(n/j,P(j))`) as low-weight
"bookkeeping" — a real, defensible pull toward a lower score, since the
matrix, its determinant identity, and the distance-to-singularity framing
are all the same author's own earlier LAA papers, narrowing how independent
the target problem really is. The two readings did not fully converge, and
that tension is left standing rather than resolved.

## Depth

Central claims — the bracket, the two-sided RH equivalence, `‖w‖ =
n^{1+o(1)}`, the closed form for `w_j`, `sigma_min(A)`, `‖A^{-1}‖` — are
proved, not merely asserted, and were independently re-derived by a cold
reviewer against the paper text. The one substantive conditionality (the
bracket-collapse hypothesis `|M(n)|/‖w‖ -> 0`) is stated precisely and
proved in the special case that matters (RH). Two concrete, disclosed
gaps were found, both about **document synchronization rather than
mathematics**:

1. `proofs/smallest-singular-value.md`'s Proposition 4 still carries the
   pre-repair proof (the one that delivered only `O(1/sqrt(log n))` before
   the ledger's fix #6 repaired it to `O(1/n)` in the paper). The true,
   fixed proof exists in `paper/sparse-mertens-singular-values.tex` but not
   in the proof note.
2. The proof note's status lines do not yet carry the conditional flag on
   the bracket-collapse hypothesis that the README and paper now state
   explicitly.

Neither undermines the mathematics itself, which is sound and
independently checked, but a reader relying on the proof note alone
(rather than the paper) currently gets a weaker proof and an unflagged
conditionality for two claims.

## Reach

The result settles its own question fully and unconditionally, and does
one genuine piece of extra work beyond the headline claim — computing
`sigma_min(A)` for the unmodified triangular factor, which answers
Cheon–Kim's question. But the method's portability beyond this one matrix
family is untested and unclaimed: the repo does not attempt, or even
conjecture, whether the same inverse-matrix-vector identification and
Sherman–Morrison decomposition would say anything about sibling
RH-linear-algebra criteria (Cheon–Kim's own Riordan–Redheffer family,
Bordelles–Cloitre's `Gamma_n`). The two explicitly open problems (the sharp
constant; the unconditional bracket-collapse) are honestly flagged as not
obviously unlocking anything beyond this paper's own internal bracket even
if solved — the README states the two known bounds "do not cross," and
closing that gap would need power-saving bounds on `M(x)` well beyond
current unconditional zero-free-region results. External search found this
sub-literature small but not dormant (a handful of 2024–2025 papers on
Redheffer/Mertens singular values exist), and Kline's own three
antecedent papers have single-digit citation counts each.

## Evidence

Most numerically-supported claims reproduce exactly from the shipped
`code/` scripts, independently re-run this session: `checkA.py verify`
reproduces the closed-form-vs-dense-solve residual of exactly zero;
`wnorm.py` matches the paper's `‖w‖` table to all printed digits out to
`n=10^7`; `spectra.py smax` matches the printed non-normality ratios
exactly. The refuted-conjecture record (`audit/ledger.md`, "Refuted, so it
is not re-derived") is unusually disciplined — four separate conjectures
that failed are kept on record with the numerical evidence that broke them,
rather than quietly dropped, and two previously-fabricated printed
quantities were caught and corrected with the correction documented rather
than laundered. The one open gap: the `‖A^{-1}‖/sqrt(n) ~ 0.8499` flatness
claim, stated as holding "out to n=10^7," is not reproducible from anything
currently in `code/` — the shipped scripts cap out at dense-SVD scale
(order `10^3`–`10^4`); the n=10^7-scale evidence for it currently exists
only inside `audit/reports/audit-math.md`, quoting an external auditor's
unshipped script. This is disclosed as a conjecture the method "provably
cannot prove," which is good practice, but the reader cannot currently
reproduce its numerical support from this repository alone.

## What would move each axis

- **Novelty up**: an exhaustive check of whether the
  inverse-matrix-vector/Alladi identification has appeared anywhere as an
  incidental observation in the Cheon–Kim or Bordelles–Cloitre lineage,
  closing the tension between the "bridging contribution" and "bookkeeping"
  readings.
- **Novelty down**: if such a prior observation is found.
- **Depth up**: sync `proofs/smallest-singular-value.md`'s Proposition 4
  proof and status lines to match the paper's already-repaired versions.
- **Reach up**: a stated (even conjectural) attempt to carry the
  inverse-matrix-vector method to a sibling RH-linear-algebra criterion.
- **Evidence up**: ship a sparse/iterative (not dense-SVD) script in
  `code/` that reaches `n=10^7` for `‖A^{-1}‖`, matching what the README
  and paper currently claim as reproducible.
