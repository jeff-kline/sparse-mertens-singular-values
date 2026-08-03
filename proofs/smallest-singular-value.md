# Proof map for the sparse Mertens singular-value bounds

This note is a navigational companion to the authoritative proof in
[`paper/sparse-mertens-singular-values.tex`](../paper/sparse-mertens-singular-values.tex).
It records the dependency chain, the exact conditional step, and the boundary
between proof, computation, and open exploration. It is not a separate claim of
review or certification.

## 1. Setup

Let `P(i)` and `P^-(i)` denote the largest and smallest prime factors of `i`.
Write

```text
M(x)   = sum_{d <= x} mu(d),
M(x,y) = sum_{d <= x, P^-(d) > y} mu(d).
```

The sparse matrix has the form

```text
A(i,j) = 1  if i = j,
         1  if i is squarefree and i/j = P(i),
         0  otherwise,

R_n = A_n + e_1 (1 - e_1)^T.
```

Earlier work proves `det R_n = M(n)`. Set

```text
mu_n = (mu(1), ..., mu(n))^T,
w    = A_n^(-T) (1 - e_1).
```

## 2. Closed form for the inverse vector

Writing `A = I + S`, the directed graph of `S` is a forest: a squarefree
integer is joined to the integer obtained by deleting its largest prime factor.
The Neumann series for `A^(-1)` terminates, and its entries are

```text
(A^(-1))_(k,j) = mu(k/j)
```

exactly when `k` is squarefree, `j | k`, and every prime factor of `k/j`
exceeds `P(j)`.

Summing the rows indexed by `k >= 2` gives

```text
w_j = 1                         if j is not squarefree,
w_j = M(n/j, P(j))              if j is squarefree,
```

with `P(1) = 1` and the `j = 1` value reduced by `1`. Consequently

```text
||w||^2
  = #{j <= n : j is not squarefree}
    + (M(n) - 1)^2
    + sum_{2 <= j <= n, j squarefree} M(n/j, P(j))^2.
```

For squarefree `j`, put `x = n/j` and `y = P(j)`. Two useful exact regimes are

```text
y >= x           => w_j = 1,
sqrt(x) <= y < x => w_j = 1 - (pi(x) - pi(y)).
```

The dense check in `code/checkA.py verify` compares this formula with a direct
solve of `A^T w = 1 - e_1` and reports zero residual at its test sizes.

## 3. Prior analytic input

Alladi's 1982 theorem concerns exactly the rough-Moebius sum above. For
`y = x^(1/alpha)` it gives

```text
M(x,y)
  = x rho'(alpha)/log(y) + y/log(y)
    + O(x alpha^2/log(y)^2),
```

uniformly for `2 <= y < x`, where `rho` is Dickman's function. This result is
cited, not claimed as new.

Fix `alpha > 1` and take prime indices
`p in (n^(1/(alpha+1)), 2 n^(1/(alpha+1))]`. Then `x = n/p`, `y = p`, and the
first main term dominates the error; the second main term is lower order since
`y/x = n^(-(alpha-1)/(alpha+1)+o(1))`. Summing the squares of these coordinates
gives

```text
||w|| >= c_alpha n^(1 - 1/(2 alpha + 2))/log(n)^(3/2).
```

Choosing a sufficiently large fixed `alpha` for each `epsilon > 0`, and using
the trivial upper bound `||w|| <= (pi/sqrt(6)) n`, yields

```text
||w|| = n^(1+o(1))
```

unconditionally.

## 4. Sherman--Morrison and the exact conditional step

When `M(n) != 0`, Sherman--Morrison gives

```text
R_n^(-1) = A_n^(-1) - mu_n w^T/M(n).
```

The rank-one term has norm

```text
||mu_n|| ||w|| / |M(n)|.
```

Therefore

```text
sigma_min(R_n) ||mu_n|| ||w|| = |M(n)|(1 + o(1))
```

Here and below, asymptotic statements using the inverse are understood along
indices with `M(n) != 0`; at a zero of `M`, the matrix is singular and the
corresponding zero-valued identity is immediate.

under the precise dominance condition

```text
|M(n)| ||A_n^(-1)|| / (||mu_n|| ||w||) -> 0.       (D)
```

Condition `(D)` cannot be replaced in the proof by the weaker statement
`|M(n)|/||w|| -> 0`: the known estimate
`||A_n^(-1)||/||mu_n|| = n^(o(1))` need not be bounded.

RH implies `(D)`. Indeed,

```text
|M(n)|           <= n^(1/2+epsilon),
||A_n^(-1)||      = n^(1/2+o(1)),
||mu_n||          = n^(1/2+o(1)),
||w||             = n^(1+o(1)),
```

so the left side of `(D)` is `n^(-1/2+epsilon+o(1))` for any fixed
`epsilon < 1/2`.

## 5. The unconditional lower bracket

The inverse formula and the triangle inequality give

```text
sigma_min(R_n)
  >= |M(n)| / (|M(n)| ||A_n^(-1)|| + ||mu_n|| ||w||).
```

Using

```text
|M(n)| <= n,
||A_n^(-1)|| = n^(1/2+o(1)),
||mu_n|| <= sqrt(n),
||w|| <= (pi/sqrt(6)) n,
```

gives

```text
sigma_min(R_n) >= |M(n)| n^(-3/2+o(1))
```

without a dominance hypothesis. If `M(n) = 0`, the matrix is singular and the
scaled inequality is immediate.

## 6. The unconditional upper bracket

Let `Q` project onto prime coordinates
`p in [n^(1/3), 2 n^(1/3)]`. The prime number theorem and the exact regime in
Section 2 give

```text
|w_p| = pi(n/p) - pi(p) - 1 = n^(2/3+o(1)),
||Qw|| = n^(5/6+o(1)).
```

The column of `A_n^(-1)` indexed by `p` is supported on squarefree `k` whose
least prime factor is `p`. These supports are disjoint for distinct primes, so

```text
||A_n^(-1) Q||
  = max_p sqrt(1 + pi(n/p) - pi(p))
  = n^(1/3+o(1)).
```

The classical zero-free-region estimate

```text
|M(n)| << n exp(-c sqrt(log n))
```

makes the projected rank-one term dominate. Hence

```text
||R_n^(-1) Q||
  >= ||mu_n|| ||Qw||/|M(n)| - ||A_n^(-1)Q||
  = n^(4/3+o(1))/|M(n)|,
```

and therefore

```text
sigma_min(R_n) <= |M(n)| n^(-4/3+o(1)).
```

Together with Section 5 this proves the unconditional bracket.

## 7. The RH equivalence

If RH holds, Section 4 gives the exact rank-one asymptotic and therefore

```text
sigma_min(R_n) <<_epsilon n^(-1+epsilon).
```

Conversely, the unconditional lower bracket rearranges to

```text
|M(n)| <= sigma_min(R_n) n^(3/2+o(1)).
```

Thus the singular-value bound implies
`M(n) = O(n^(1/2+epsilon))` for every `epsilon > 0`, which is RH. The two
directions are unconditional even though the exact rank-one asymptotic is only
invoked under RH.

## 8. The other end and the unmodified factor

The dense first row gives `sigma_max(R_n) >= sqrt(n)`. A Schur-complement
argument for `R_n R_n^T`, using an off-diagonal block of squared norm at most
`4n` and a lower block of norm `o(n)`, gives

```text
sigma_max(R_n) = sqrt(n) (1 + O(1/n)).
```

The known dominant eigenvalue has size `sqrt(pi(n))`, so

```text
sigma_max(R_n)/|lambda_max(R_n)| asymp sqrt(log n).
```

For `A_n`, the nilpotent part has index of order `log n/log log n`. Its
terminating Neumann series gives

```text
||A_n^(-1)|| <= sum_r sqrt(pi'_r(n)) = n^(1/2+o(1)),
```

The final equality follows from Cauchy--Schwarz: there are at most
`1 + floor(log_2(n))` nonzero summands and `sum_r pi'_r(n) <= n`.

while its first column is `mu_n`, giving the matching exponent from below.
Therefore

```text
||A_n^(-1)|| = n^(1/2+o(1)),
sigma_min(A_n) = n^(-1/2+o(1)).
```

The stronger estimates `||A_n^(-1)|| asymp sqrt(n)` and
`sigma_min(A_n) asymp n^(-1/2)` are suggested by small dense computations but
are not proved.

## 9. Evidence boundaries

- **Proved:** the closed form, `||w|| = n^(1+o(1))`, the unconditional bracket,
  the RH equivalence, the largest-singular-value estimate, and the exponent for
  the unmodified factor.
- **Exact computation:** closed-form residuals, determinant checks, and the
  finite spectral tables printed in the paper.
- **Prior work:** the sparse matrix and determinant identity, Alladi's
  rough-Moebius asymptotic, and earlier one-directional singular-value criteria.
- **Open:** the sharper shape
  `||w|| = n exp(-(1+o(1)) sqrt(log n log log n))`, a sharp constant, and the
  stronger two-sided constant-factor estimate for `||A_n^(-1)||`.

The historical finding and disposition record is in
[`audit/ledger.md`](../audit/ledger.md). Process-separated AI checks are useful
for finding errors, but they are not peer review or independent expert
validation.
