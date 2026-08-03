# Release proof closure

**Date:** 2026-08-03

**Verdict:** PASS

**Audited paper source SHA-256:**
`f293fa9c04661b5de22af0cd94afbab4bb2c84906e1d9dcb27eb08f0e24e59e4`

This is the durable record of the final process-separated AI proof closure for
Version 0.1.0. It records evidence about the checking process. It is not peer
review, independent expert validation, or a certificate of correctness.

## Scope

The closure reconstructed and rechecked:

- the exact inverse-vector formula;
- the use of Alladi's rough-Moebius estimate;
- the Sherman--Morrison dominance condition;
- the unconditional lower and upper brackets;
- both directions of the RH equivalence;
- the largest-singular-value proof;
- every live distinction between `n^(-1/2+o(1))` and the stronger, unproved
  constant-factor asymptotic.

The lane independently reconstructed the numerical claims without importing
the repository's code and reproduced every printed value in its tested range.
The separate bounded prior-art audit records citation and novelty scope.

## Findings and dispositions

The first pass found no mathematical break but returned PARTIAL because the
tree was moving and four proof-hygiene steps were omitted:

1. Alladi's secondary `y/log y` term had not been explicitly controlled.
2. The Cauchy--Schwarz step behind
   `sum_r sqrt(pi'_r(n)) = n^(1/2+o(1))` was unstated.
3. The Sherman--Morrison limit statement did not explicitly restrict inverse
   asymptotics to indices with `M(n) != 0`.
4. A Vinogradov--Korobov-shaped bound was imprecisely called classical.

The paper and proof map were repaired. The final read-only recheck verified all
four repairs against the frozen source hash above:

- `y/x = n^(-(alpha-1)/(alpha+1)+o(1)) -> 0` for fixed `alpha > 1`;
- Cauchy--Schwarz uses at most `1 + floor(log_2(n))` nonzero summands and
  `sum_r pi'_r(n) <= n`;
- singular indices are handled separately and never invoke a nonexistent
  inverse;
- the classical bound `|M(n)| << n exp(-c sqrt(log n))` still makes
  `|M(n)| log n/n -> 0`, which is the load-bearing projected domination ratio.

No theorem statement, exponent, table, or printed numerical value changed in
these repairs. The final lane found no new defect in the principal theorem,
the unconditional bracket, or the RH equivalence.

## Bound artifacts

| Artifact | SHA-256 |
|---|---|
| `paper/sparse-mertens-singular-values.tex` | `f293fa9c04661b5de22af0cd94afbab4bb2c84906e1d9dcb27eb08f0e24e59e4` |
| `paper/sparse-mertens-singular-values.pdf` | `a2b9dba0d758def56c6c34a1fbebe5e68676ebf467f91574b0b5c8e0de576a52` |
| `proofs/smallest-singular-value.md` | `9ecbb0845050ec82a8f8d78bff2fe896518dee14060591a1e7e95142661cbc3e` |

Any material edit to the paper source reopens this closure.
