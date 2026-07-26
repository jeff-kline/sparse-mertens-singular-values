# The smallest singular value of a sparse Mertens matrix

Redheffer's `(0,1)` matrix `R_n` has `det R_n = M(n) = sum_{k<=n} mu(k)`, and a
much sparser `(0,1)` matrix with the same determinant — roughly `2.61n` nonzeros
against Redheffer's `~n log n` — was given in

> J. Kline, *A sparser matrix representation of the Mertens function*, Linear
> Algebra Appl. **581** (2019) 354-366,

and its two dominant **eigenvalues**, `1 +/- sqrt(pi(n))`, were determined in

> J. Kline, *On the eigenstructure of sparse matrices related to the prime
> number theorem*, Linear Algebra Appl. **584** (2020) 409-430.

This repository determines the **singular values**, at both ends, and shows the
smallest one is governed by Dickman's function:

    |M(n)| n^{-3/2+o(1)}  <=  sigma_min(R_n)  <=  |M(n)| n^{-4/3+o(1)}

    RH  <=>  sigma_min(R_n) << n^{-1+eps}

The equivalence is two-sided and unconditional, but it does not follow from the
bracket alone — the two statements are established separately:

- `<=` is the lower bound rearranged: `|M(n)| <= sigma_min * n^{3/2+o(1)}`.
- `=>` does **not** go through the displayed upper bound, which under RH yields
  only `n^{-5/6+eps}`. It goes through the collapsed equality
  `sigma_min(R_n) = |M(n)| n^{-3/2+o(1)}`, valid as soon as `|M(n)|/||w|| -> 0`;
  RH supplies exactly that, since `|M(n)|/||w|| << n^{-1/2+eps}`.

That hypothesis is *not* known unconditionally, because the best available bounds
on `||w||` and on `|M(n)|` do not cross — which is why the unconditional
statement is a bracket rather than an asymptotic.

The analytic engine is **not new**: it is Alladi's 1982 asymptotic for the
Moebius function summed over integers free of small prime factors. What is
established here is the linear algebra — that the entries of a certain
inverse-matrix vector *are* Alladi's sums, and what that forces about the
spectrum.

## Independent scorecard

An independent repo-rank pass (2026-07-26, commit `ea277de`) scored four axes
qualitatively; full reasoning, external-literature checks, and each axis's own
counter-argument are in
[`audit/reports/repo-rank-scorecard.md`](audit/reports/repo-rank-scorecard.md).

| Axis | Note |
| --- | --- |
| Novelty | Analytic engine (Alladi 1982) is not new; the bridge from it to this matrix family's singular values, and the negative answer to Cheon-Kim's open question, was not located elsewhere — though the repo's own prior-art audit reads the same connection as low-weight bookkeeping. |
| Depth | Central claims proved and independently re-derived; the proof note lags one already-repaired proof (Prop. 4) and a conditional-hypothesis flag that the paper and README already carry. |
| Reach | Settles its own equivalence unconditionally and answers a real open question, but portability to sibling RH-linear-algebra criteria (Cheon-Kim, Bordelles-Cloitre) is untried and unclaimed. |
| Evidence | Most numerical claims reproduce exactly from shipped code, with a genuinely disciplined refuted-conjecture record; the `n=10^7` support for `‖A^{-1}‖/sqrt(n) ~ 0.8499` is not reproducible from anything currently in `code/`. |

## Main results

- The bracket above, and the two-sided unconditional RH equivalence.
- `||w|| = n^{1+o(1)}` unconditionally, where `w = A^{-T}(1 - e_1)`. This is what
  produces the exponent `-3/2`, and it is the analytic content of the main
  theorem.
- A closed form identifying `w_j` with Alladi's `M(n/j, P(j))`, verified against
  a dense linear solve to residual exactly zero.
- `sigma_min(A) = n^{-1/2+o(1)}` for the unmodified triangular factor `A`. This
  answers, negatively for this family, a question posed by Cheon and Kim
  (LAA **572** (2019) 252-272): their sufficient condition for RH needs the
  quantity `1 + sqrt(n-1)/sigma_min(L_n)` to be `O(n^{1/2+eps})`, and here it is
  `n^{1+o(1)}`.
- `||A^{-1}|| = n^{1/2+o(1)}`, via a **terminating** Neumann series: the nilpotent
  part has index `~ log n / log log n`, the largest number of prime factors of a
  squarefree integer below `n`. Numerically `||A^{-1}||/sqrt(n)` is flat at
  `0.8499` out to `n = 10^7`, so `~ sqrt(n)` is expected, but the method provably
  cannot prove it — see `audit/ledger.md`, item 7.
- `sigma_max(R_n) = sqrt(n)(1 + O(1/n))`, forced by a single dense row, with
  non-normality gap `sigma_max/|lambda_max| ~ sqrt(log n)`.

## Relation to earlier work

This completes a programme begun in J. Kline, *Bordered Hermitian matrices and
sums of the Moebius function*, LAA **588** (2020) 224-237, which observes that
"the Riemann hypothesis is an assertion that the constant `1^t` is, for all `n`,
almost in the span of the rows of `B`". That distance is `|M(n)|/||mu||`. The
matrix is in fact `n^{1+o(1)}` **closer** to singular than that one direction
reveals, and the discrepancy is exactly Alladi's function summed along a
hyperbola.

## How to use this repository

This repository was written with substantial assistance from large language
models and is designed, in part, for other language models to ingest. The
intended workflow is:

1. Give an AI agent access to the repository.
2. Ask it to trace definitions, proofs, computations, and dependencies across the
   paper, the proof note, the code, and the audit records.
3. Interrogate its answers as a human reader — request derivations, file
   references, counterexamples, assumptions, and supporting evidence.

The proof note occupies a space between prose and source code: structured
precisely enough for an agent to navigate, while remaining readable by humans. It
is not an automatic guarantee of correctness. `audit/ledger.md` records, per
claim, what was checked and how — including what is *conditional*, what is
merely numerical, and what was refuted.

### Quick start

Point your agent here and try:

- Which results are proved unconditionally, which are conditional, and on what?
- Where exactly does the chain from `sigma_min` to RH become conditional, and why
  do the two bounds fail to cross?
- What is the dependency chain for the main theorem?
- Which scripts test a given claim, and what do those tests actually establish?
- Which conjectures were refuted along the way, and by what evidence?

For important conclusions, ask for exact files, theorem labels, and line numbers —
and verify against the source.

## Reproduce

NumPy only, except `checkB.py` which also needs `mpmath`. Use a virtual
environment:

```sh
python3 -m venv .venv && .venv/bin/pip install numpy mpmath
cd code

.venv/bin/python checkA.py verify        # closed form vs dense solve, residual 0
.venv/bin/python wnorm.py 100000 1000000 # ||w|| table, O(n log n), reaches 3*10^7
.venv/bin/python spectra.py smax         # sigma_max, |lambda_max|, non-normality
.venv/bin/python spectra.py smin         # sigma_min(A), ||A^{-1}||, nilpotency
.venv/bin/python spectra.py munorm       # ||mu_n||/sqrt(n) vs sqrt(6/pi^2)
.venv/bin/python spectra.py smscan 200 3200 25   # Sherman-Morrison ratio, min/max
.venv/bin/python spectra.py redheffer    # Redheffer's own gap, for comparison
```

`spectra.py` builds the matrices explicitly and calls a dense SVD, checking
`det = M(n)` as it goes; it is the slow reference against which the `O(n log n)`
evaluators are validated.

## Layout

| Path | Contents |
| --- | --- |
| `paper/` | The paper (12 pp.), source and PDF. |
| `proofs/smallest-singular-value.md` | The proof note: statements, proofs, status labels, and what is not established. |
| `code/` | Numerics. `wnorm.py` and `massprofile.py` are `O(n log n)`; `spectra.py` is the dense reference for every spectral quantity. |
| `audit/ledger.md` | Per-claim audit record: what was checked, the evidence, and the resolution. Start here. |
| `audit/reports/` | The five audit-axis reports, plus two independent attack reports (run under mandated-different methods) and the prior-art audit. |

## Status

The paper has been through a five-axis adversarial audit (mathematics,
citations, numerics, abstract, privacy), run as cold agents on disjoint axes.
Twelve must-fix items were found and applied; the per-claim record is in
[`audit/ledger.md`](audit/ledger.md). Notably, two printed quantities turned out
never to have been computed by any script, and one comparative claim was
inverted — both are documented there rather than quietly removed.

Open:

- **The sharp constant.** Alladi's Theorem 1 does not reach the relevant saddle,
  and his Theorem 2 gives only half the true exponent; he flags this himself.
- **The unconditional collapse of the bracket**, i.e. `|M(n)|/||w|| -> 0`.
- Still unread: Alladi, Trans. Amer. Math. Soc. **272** (1982) 87-105, the sequel
  to the paper supplying the engine. AMS returned 403.

## How to cite

This is an unpublished manuscript; cite the repository and PDF directly.

```bibtex
@misc{kline2026sparsemertens,
  author       = {Kline, Jeffery},
  title        = {The smallest singular value of a sparse Mertens matrix},
  year         = {2026},
  note         = {Unpublished manuscript},
  howpublished = {\url{https://github.com/jeff-kline/sparse-mertens-singular-values}}
}
```

The matrix studied here originates in:

```bibtex
@article{kline2019sparser,
  author  = {Kline, Jeffery},
  title   = {A sparser matrix representation of the {M}ertens function},
  journal = {Linear Algebra and its Applications},
  volume  = {581},
  pages   = {354--366},
  year    = {2019}
}

@article{kline2020eigenstructure,
  author  = {Kline, Jeffery},
  title   = {On the eigenstructure of sparse matrices related to the prime
             number theorem},
  journal = {Linear Algebra and its Applications},
  volume  = {584},
  pages   = {409--430},
  year    = {2020}
}
```

## License

Copyright (C) 2026 Jeffery Kline. Released under the GNU General Public
License, version 3 (GPL-3.0); see `LICENSE`.
