# Bounded prior-art audit

**Status:** COMPLETE for release candidate 0.1.0
**Search closed:** 2026-08-03
**Verdict:** PASS with named residual risks

This is a bounded literature comparison, not a claim of exhaustive search or
global priority. Sources that could not be obtained are named and are not
counted as negative evidence.

## Principal contribution under review

For the sparse Mertens matrix `R_n = A_n + e_1(1-e_1)^T`, the manuscript claims:

1. an exact inverse-vector identity
   `w_j = M(n/j,P(j))` for squarefree `j`;
2. the unconditional norm estimate `||w|| = n^(1+o(1))` obtained by applying
   Alladi's rough-Moebius asymptotic to that identity;
3. the unconditional bracket
   `|M(n)|n^(-3/2+o(1)) <= sigma_min(R_n)
   <= |M(n)|n^(-4/3+o(1))`;
4. the equivalence
   `RH <=> sigma_min(R_n) <<_epsilon n^(-1+epsilon)`;
5. the estimates at the other end and for the unmodified sparse factor:
   `sigma_max(R_n) = sqrt(n)(1+O(1/n))` and
   `sigma_min(A_n) = n^(-1/2+o(1))`.

No earlier statement of items 1--4 for this sparse family was located in the
searched corpus. This conclusion is limited to the corpus below.

## Closest mechanisms and parameter families

### Alladi's rough-Moebius sums

K. Alladi's 1982 JNT paper studies exactly

```text
M(x,y) = sum_{d <= x, P^-(d) > y} mu(d)
```

and proves the asymptotic used in the manuscript. This analytic estimate is
prior work and is cited as such. The present contribution is the identification
of the coordinates of a sparse inverse-matrix vector with Alladi's sums and the
singular-value consequences.

Alladi's companion TAMS paper was verified bibliographically but its full text
was not obtained during this audit. It remains a named residual risk and was
not used as negative evidence.

### Earlier sparse Mertens matrices

Kline's LAA 581 paper introduced the sparse `(0,1)` matrix and its determinant
identity. LAA 584 determined its dominant eigenvalues and restated the family.
LAA 588 supplied the bordered-Hermitian and row-span geometry, including the
`||mu_n||` factor. These are foundations of the current paper, not competing
claims.

The quantitative distinction is:

```text
LAA 588 direction:  distance = |M(n)|/||mu_n||,
current rank-one regime: sigma_min(R_n)
  = |M(n)|/(||mu_n|| ||w||) (1+o(1)).
```

The extra `||w|| = n^(1+o(1))` factor and the exact dominance condition are the
new parts claimed here.

### Smallest-singular-value criteria for RH

The earliest instance located in the searched corpus is Bordelles and Cloitre
(2009). Their upper-triangular factor belongs to a different matrix built from
the weighted sum `sum mu(k)/k`; they give sufficient singular-value conditions
for PNT and RH but do not determine the relevant singular value.

Cheon and Kim (2019) give a one-directional sufficient condition for the
unmodified triangular factor of a Mertens equimodular matrix and ask which
families satisfy it. The present paper studies both its own unmodified sparse
factor and the modified determinant matrix. It proves that the unmodified
factor fails their sufficient condition and obtains a two-sided equivalence for
the modified matrix.

### Hilberdink's dense divisibility factor

Hilberdink (2017), Section 4(b), is material adjacent work. For the dense
divisibility matrix `M_n(1)` underlying Redheffer's matrix, he proves

```text
sigma_min(M_n(1))
  ~ sqrt(zeta(2)/nu_1) n^(-1/2),
```

where `nu_1` is the largest eigenvalue of his Hilbert--Schmidt operator `G_0`.
This matches the exponent obtained here for the unmodified sparse factor
`A_n`. It does not treat the sparse forest factor, the vector `w`, the modified
matrix `R_n`, the bracket, or the two-sided RH equivalence. The paper now cites
and distinguishes this result.

### Other Redheffer singular-value work

Clement and Steinerberger (2025) study the largest singular value and vector of
Redheffer's matrix. They do not treat the smallest singular value of this sparse
family. The older Redheffer literature reached in this audit concerns
eigenvalues, determinants, permanents, or other matrix families.

## Contribution classification

- **Prior transfer:** Alladi's rough-Moebius asymptotic; the sparse matrix and
  determinant identity; the `||mu_n||` estimate; earlier sufficient
  singular-value criteria.
- **Theorem in this manuscript:** the inverse-vector identity, the norm
  consequence for `w`, the bracket, the RH equivalence, and the two endpoint
  estimates for this sparse family.
- **Exact computation:** finite residual, determinant, singular-value, and
  eigenvalue checks. These support but do not prove the asymptotic statements.
- **Exploration:** the sharper proposed shape of `||w||`; it is not part of the
  admitted claim.

## Searched corpus

Primary texts or publisher records checked through 2026-08-03:

- K. Alladi, *Asymptotic estimates of sums involving the Moebius function*,
  J. Number Theory 14 (1982) 86--98.
- K. Alladi, *Asymptotic estimates of sums involving the Moebius function. II*,
  Trans. Amer. Math. Soc. 272 (1982) 87--105; metadata only.
- O. Bordelles and B. Cloitre, *A matrix inequality for Moebius functions*,
  JIPAM 10 (2009), art. 62.
- G.-S. Cheon and H. Kim, *Mertens equimodular matrices of Redheffer type*,
  LAA 572 (2019) 252--272.
- J. Kline, LAA 581 (2019) 354--366; LAA 584 (2020) 409--430; and LAA 588
  (2020) 224--237.
- T. W. Hilberdink, *Singular values of multiplicative Toeplitz matrices*,
  Linear Multilinear Algebra 65 (2017) 813--829.
- F. Clement and S. Steinerberger, *On the largest singular vector of the
  Redheffer matrix*, LAA 725 (2025) 96--114.
- A. Pierro de Camargo, *Dirichlet matrices: determinants, permanents and the
  Factorisatio Numerorum problem*, LAA 628 (2021) 115--129.
- J. B. Oon, adjacent Liouville-matrix work (2013); different determinant and
  family.
- Exact-phrase and metadata searches for combinations of “smallest singular
  value,” “Mertens,” “Redheffer,” “sparse Mertens,” and the inverse-vector
  rough-Moebius formula.

## Residual risks

- Alladi's 1982 TAMS companion was not read in full.
- Several older paywalled or book-length sources in sieve theory and the
  Redheffer literature were reached only through metadata or citations.
- Terminology can differ across multiplicative Toeplitz, divisibility,
  equimodular, and arithmetic-matrix literatures; the search may have missed an
  equivalent formulation.
- No absence result from this search is promoted to a worldwide novelty claim.

## P1 disposition

**PASS.** The closest mechanisms and parameter families are compared, the
analytic and matrix foundations are credited, contribution types are separated,
and inaccessible sources remain visible. “Not located in the searched corpus”
is the strongest novelty language supported by this audit.
