# The smallest singular value of a sparse Mertens matrix

**Status: release candidate 0.1.0.** This manuscript and its verification code
are being prepared under the project's
[public research standard](https://jeff-kline.github.io/posts/research-program/index.html).
No stable archive or DOI exists yet. Admission under that standard will be a
project release decision, not peer review or a correctness certificate.

Redheffer's matrix is a `(0,1)` matrix whose determinant is the Mertens function

```text
M(n) = sum_{k <= n} mu(k).
```

This repository studies a much sparser matrix `R_n` with the same determinant:
it has about `2.61n` nonzero entries, compared with roughly `n log n` for
Redheffer's matrix. The paper determines its largest singular value and gives
two-sided control of its smallest singular value:

```text
|M(n)| n^(-3/2+o(1)) <= sigma_min(R_n) <= |M(n)| n^(-4/3+o(1)),

RH  <=>  sigma_min(R_n) <<_eps n^(-1+eps).
```

Both statements are unconditional. The two directions of the RH equivalence
use different parts of the bracket argument; the forward direction uses the
stronger rank-one asymptotic available under RH.

The matrix is singular whenever `M(n) = 0`, so the displayed bracket may vanish
at infinitely many indices. The result concerns the scale of the smallest
singular value relative to `|M(n)|`, not a positive unconditional lower bound.

## Main result and mechanism

Write the sparse matrix as

```text
R_n = A_n + e_1 (1 - e_1)^T,
```

where `A_n` is unit lower triangular, and set

```text
w = A_n^(-T) (1 - e_1).
```

The paper proves the exact coordinate formula

```text
w_j = M(n/j, P(j))
```

for squarefree `j`, with the stated convention at `j = 1`; here `P(j)` is the
largest prime factor and `M(x,y)` is the Moebius function summed over integers
whose prime factors all exceed `y`. Nonsquarefree coordinates equal `1`.

K. Alladi determined the asymptotic behavior of these rough-Moebius sums in
1982. Applying that prior result along the hyperbola `x = n/j`, `y = P(j)` gives

```text
||w|| = n^(1+o(1))
```

unconditionally. This is the analytic input behind the exponent `-3/2`.
Sherman--Morrison then gives

```text
R_n^(-1) = A_n^(-1) - mu_n w^T / M(n).
```

When the rank-one term dominates, equivalently when

```text
|M(n)| ||A_n^(-1)|| / (||mu_n|| ||w||) -> 0,
```

the smallest singular value satisfies

```text
sigma_min(R_n) = |M(n)| n^(-3/2+o(1)).
```

RH implies this dominance condition. The weaker condition
`|M(n)|/||w|| -> 0` alone is not asserted here.

At the other end, the paper proves

```text
sigma_max(R_n) = sqrt(n) (1 + O(1/n))
```

and a non-normality gap of order `sqrt(log n)`. For the unmodified triangular
factor it proves

```text
||A_n^(-1)|| = n^(1/2+o(1)),
sigma_min(A_n) = n^(-1/2+o(1)).
```

## What is new, and what is not

The analytic estimate for `M(x,y)` is not new; it is Alladi's 1982 theorem.
The determinant identity and the sparse matrix family come from Jeffery
Kline's earlier papers. The earliest use of a smallest singular value to
approach PNT or RH located in the bounded search is due to Bordelles and
Cloitre; Cheon and Kim later gave a one-directional sufficient condition for
triangular factors of Mertens equimodular matrices. Hilberdink proved an
`n^(-1/2)` smallest-singular-value asymptotic for the dense divisibility
triangular factor underlying Redheffer's matrix. That result matches the
exponent found here for `A_n`, but it does not treat this sparse forest factor
or the modified matrix `R_n`.

The contribution claimed here is narrower:

1. the inverse-vector identity connecting this sparse matrix to Alladi's
   rough-Moebius sums;
2. the unconditional estimate `||w|| = n^(1+o(1))` obtained from that
   connection;
3. the resulting two-sided bracket and two-sided RH equivalence for the
   modified sparse matrix;
4. the asymptotics at the largest singular value and for the unmodified
   triangular factor.

A bounded prior-art search found no earlier treatment of the smallest singular
value of this sparse family or this two-sided equivalence. That search is
recorded in [`audit/reports/prior-art-audit.md`](audit/reports/prior-art-audit.md).
It does not establish global novelty. In particular, one 1982 companion paper
by Alladi could not be obtained during the earlier audit and remains a named
coverage gap.

## Evidence and limits

The repository separates four kinds of support:

- **Proof.** The authoritative argument is
  [`paper/sparse-mertens-singular-values.tex`](paper/sparse-mertens-singular-values.tex),
  with a compiled reading copy in
  [`paper/sparse-mertens-singular-values.pdf`](paper/sparse-mertens-singular-values.pdf).
- **Exact computation.** The scripts construct the matrices, compare the closed
  form for `w` with a dense solve, check determinants, and reproduce the printed
  spectral values.
- **Literature.** Alladi's rough-Moebius estimate and the earlier matrix results
  are cited rather than presented as new.
- **Exploration.** Finite computations motivate a sharper conjectural shape for
  `||w||`, but that refinement is not proved and is not used in the main theorem.

Important limits remain:

- The sharper conjecture
  `||w|| = n exp(-(1+o(1)) sqrt(log n log log n))` is open.
- The data are severely pre-asymptotic; several plausible finite-range laws
  failed and are retained in the audit history.
- Some original sources were inaccessible during the bounded literature search.
- AI-assisted audits can expose errors, but they are not peer review or
  independent expert validation.

## Reproduce the main checks

Requirements are Python 3, NumPy, and mpmath. From the repository root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

.venv/bin/python code/checkA.py verify
.venv/bin/python code/wnorm.py 100000 1000000
.venv/bin/python code/spectra.py smax
.venv/bin/python code/spectra.py smin
.venv/bin/python code/spectra.py munorm
.venv/bin/python code/spectra.py sm 500 1000 2000
.venv/bin/python code/spectra.py redheffer
```

The first command compares the closed form for `w` with a dense linear solve
and reports zero residual. `wnorm.py` is an `O(n log n)` evaluator.
`spectra.py` builds dense matrices, checks `det R_n = M(n)`, and uses direct
singular-value and eigenvalue computations as a slower reference.

The extended grid behind the printed Sherman--Morrison range is substantially
slower:

```bash
.venv/bin/python code/spectra.py smscan 200 3200 25
```

To rebuild the paper with a local TeX installation:

```bash
cd paper
env SOURCE_DATE_EPOCH=1785715200 FORCE_SOURCE_DATE=1 \
  pdflatex -interaction=nonstopmode -halt-on-error sparse-mertens-singular-values.tex
env SOURCE_DATE_EPOCH=1785715200 FORCE_SOURCE_DATE=1 \
  pdflatex -interaction=nonstopmode -halt-on-error sparse-mertens-singular-values.tex
```

Exact tool versions, expected outputs, and the deterministic PDF hash are in
[`VERIFICATION.md`](VERIFICATION.md). Tracked-file hashes will be frozen in
`MANIFEST.sha256` before tagging.

## Repository map

- `paper/` — authoritative paper source and compiled PDF.
- `proofs/smallest-singular-value.md` — detailed proof and exploration note.
- `code/` — exact and numerical checks.
- `audit/ledger.md` — historical finding and disposition record.
- `audit/reports/` — mathematical, citation, numerical, privacy, and prior-art
  audits. Process-separated AI reports are evidence about the checking process,
  not expert review.
- `ADMISSION.md` — live P1/A1/R1 release gate, added during release preparation.
- `VERIFICATION.md` and `MANIFEST.sha256` — pinned rerun record and tracked-file
  hashes.
- `CITATION.cff` and `CORRECTIONS.md` — citation and stewardship metadata, added
  before release.

## AI assistance and responsibility

Large language models substantially assisted with mathematical exploration,
proof drafting, code, literature search, exposition, and adversarial checks.
Their agreement is evidence about a process, not a certificate of correctness.
Jeffery Kline directs the work, is responsible for the claims released under
his name, and will record material corrections or withdrawals in the public
history.

## Citation

Version 0.1.0 is still a release candidate and has no active DOI. Until an
immutable archive is published, cite the repository and paper directly:

```bibtex
@misc{kline2026sparsemertens,
  author       = {Kline, Jeffery},
  title        = {The smallest singular value of a sparse Mertens matrix},
  year         = {2026},
  version      = {0.1.0-rc},
  note         = {Release candidate; no permanent archive yet},
  howpublished = {\url{https://github.com/jeff-kline/sparse-mertens-singular-values}}
}
```

## License

Copyright (C) 2026 Jeffery Kline. Released under the GNU General Public License,
version 3 only (GPL-3.0-only); see [`LICENSE`](LICENSE).
