# The smallest singular value of a sparse Mertens matrix

Redheffer's `(0,1)` matrix `R_n` has `det R_n = M(n) = sum_{k<=n} mu(k)`, and a
much sparser `(0,1)` matrix with the same determinant — roughly `2.6n` nonzeros
against Redheffer's `~n log n` — was given in

> J. Kline, *On the eigenstructure of sparse matrices related to the prime
> number theorem*, Linear Algebra Appl. **584** (2020) 409-430.

That paper determines the two dominant **eigenvalues**, `1 +/- sqrt(pi(n))`.
This repository determines the **singular values**, at both ends, and shows the
smallest one is governed by Dickman's function:

    sigma_min(R_n) = |M(n)| * n^{-3/2 + o(1)},   hence   RH  <=>  sigma_min(R_n) << n^{-1+eps}

two-sided and unconditional. The analytic engine is **not new**: it is Alladi's
1982 asymptotic for the Moebius function summed over integers free of small
prime factors. What is established here is the linear algebra — that the entries
of a certain inverse-matrix vector *are* Alladi's sums, and what that forces
about the spectrum.

## Main results

- `sigma_min(R_n) = |M(n)| n^{-3/2+o(1)}`, and the two-sided RH equivalence above.
- `sigma_min(A) ~ c n^{-1/2}` for the unmodified triangular factor `A`. This
  answers, negatively for this family, a question posed by Cheon and Kim
  (LAA **572** (2019) 252-272): their sufficient condition for RH requires
  `sigma_min(L_n) >> n^{-eps}`, and here it is `n^{-1/2}`.
- `||A^{-1}|| ~ sqrt(n)`, via a **terminating** Neumann series: the nilpotent
  part has index `~ log n / log log n`, the largest number of prime factors of a
  squarefree integer below `n`.
- `sigma_max(R_n) = sqrt(n)(1 + O(1/n))`, and a non-normality gap
  `sigma_max / |lambda_max| ~ sqrt(log n)` — against `Theta(sqrt n)` for the
  denser matrices of LAA 584.
- A closed form identifying `w_j` with Alladi's `M(n/j, P(j))`, verified against
  a dense linear solve to residual exactly zero.

## Relation to earlier work

This completes a programme begun in J. Kline, *Bordered Hermitian matrices and
sums of the Moebius function*, LAA **588** (2020) 224-237, which observes that
"the Riemann hypothesis is an assertion that the constant `1^t` is, for all `n`,
almost in the span of the rows of `B`". That distance is `|M(n)|/||mu||`. The
matrix is in fact `n^{1+o(1)}` **closer** to singular than that one direction
reveals, and the discrepancy is exactly Alladi's function summed along a
hyperbola.

## Layout

| Path | Contents |
| --- | --- |
| `proofs/smallest-singular-value.md` | The proof note: statements, proofs, status labels, and what is not established. |
| `code/` | Numerics; NumPy only, except `checkB.py` which also needs `mpmath`. `wnorm.py` is an `O(n log n)` evaluator reaching `n = 3*10^7`; `massprofile.py` adds the mass profile. |
| `audit/reports/` | Two independent attack reports (elementary and analytic, run under mandated-different methods) and the prior-art audit. |
| `paper/` | The paper (11 pp.), source and PDF. |

## Status

**Private, work in progress.** Two conditions before this goes public:

1. ~~Bordelles & Cloitre~~ — **read and cited** (JIPAM **10** (2009), art. 62).
   Their matrix is different (`det = n! * sum mu(k)/k`) and their Corollary 2.7 is
   a sufficient condition, not an asymptotic; they explicitly note that general
   bounds for the smallest singular value of a triangular matrix are exponentially
   weak. Discussed at Remark 12 of the paper. Still unread: Alladi, Trans. Amer.
   Math. Soc. **272** (1982) 87-105, the sequel to the paper supplying the engine.
2. No adversarial pass has been run on the material added after the two attack
   reports, nor on the paper itself.

The sharp constant is open. Alladi's Theorem 1 does not reach the relevant
saddle, and his Theorem 2 gives only half the true exponent; he flags this
himself.
