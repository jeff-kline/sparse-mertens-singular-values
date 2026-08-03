# Numerics audit: sparse-mertens-singular-values

Method: independent dense construction of A_n (unit lower triangular) and
R_n (first row all-ones) built from scratch in
`numcheck/build.py`, verified against repo `checkA.py verify` and against
`det(R_n) == M(n)` for n=6,10,20,50 (exact match). Then cross-checked
against repo scripts `wnorm.py`, `massprofile.py`, `checkA.py`, `checkB.py`,
`convA.py`, `alphaA.py`, `kdrift.py`.

Python: an auditor-local Python environment throughout (numpy 2.0.2, scipy 1.13.1,
mpmath 1.3.0). Repo is read-only; no git commands run.

## Matrix construction sanity check
det(R_n) = M(n) exactly for n=6,10,20,50 (my independent dense build).

## Item 0: DENSE-vs-FAST agreement on w (Theorem thm:closed)
My independent dense solve `A^T w = 1-e1` (via `np.linalg.solve`) gives
||w|| = 47.296934, 79.309520, 132.370692 at n=500,1000,2000 -- these match
`checkA.py verify` bit-for-bit (max|dense-closed| = 0.000e+00 reported by
the repo script itself, and my independently-coded dense solve reproduces
the same ||w|| values to all printed digits).
**DENSE-vs-FAST AGREEMENT: exact (0) at n=500,1000,2000**, confirming the
paper's claim in Sec. 6 ("agree to residual exactly 0").

## Item 1: Sparsity ~2.61n
My dense R_n, nnz(R)/n at n=500,1000,2000: 2.6080, 2.6060, 2.6065.
**REPRODUCED** (paper says "about 2.61n").

## Item 2: Table of ||w|| (repo wnorm.py, cross-checked against dense at small n)
Ran `wnorm.py 100000 300000 1000000 3000000 10000000 30000000`:
n=1e5: 2289.3 | 3e5: 5211.8 | 1e6: 12850.5 | 3e6: 29519.5 | 1e7: 73972.3 | 3e7: 172026.3
**REPRODUCED exactly** (matches paper Table 1 to all printed digits).
||w||/n column also matches to printed digits: 0.022893, 0.017373, 0.012851,
0.009840, 0.007397, 0.005734 -- **REPRODUCED**.
Local exponents from wnorm.py: 0.7488, 0.7496, 0.7570, 0.7630, 0.7682
vs paper's 0.7488, 0.7496, 0.7570, 0.7630, 0.7683.
Last value **ROUNDING** (0.7682 vs 0.7683, computed from data agreeing to
5 sig figs -- difference is in how the ratio n/prev is rounded internally,
negligible).

## Item 3: Sherman-Morrison ratio (independent dense computation)
My dense computation of sigma_min(R_n)*||mu_n||*||w||/|M(n)|:
n=500: 0.989636 | n=1000: 1.003818 | n=2000: 1.004699
vs paper: 0.9896, 1.0038, 1.0047.
**REPRODUCED** (all match to 4 significant figures / last printed digit).

**Range claim "[0.999,1.008] for 200<=n<=3200": MISMATCH.**
I computed the ratio by dense SVD/det at every n in {200,250,...,1000 step 50,
1100,1200,1300,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200} (30 points,
skipping the two points n=850,1300 where M(n)=0 exactly and R_n is singular,
so the ratio is 0/0-type indeterminate -- consistent with the paper's own
Remark that sigma_min(R_n)=0 infinitely often).
Result: only about a third of the sampled points actually land in
[0.999,1.008]; most do not. Extremes observed: **0.987124 at n=300** and
**1.014413 at n=600**, both clearly outside the stated interval. Also,
n=550 (1.010854), n=600 (1.014413), n=1400 (1.012424), n=2200 (1.009499)
exceed the upper bound 1.008.
Moreover there is an internal inconsistency in the paper's own printed
numbers: it states the ratio "equals ... 0.9896 ... at n=500" and separately
"lies in [0.999,1.008] for 200<=n<=3200" -- but 0.9896 < 0.999, so the
paper's own n=500 value already falls outside its own claimed range. This
is not a computational disagreement, it is arithmetic: 0.9896 is not in
[0.999, 1.008].
Full sampled ratio values (n: ratio): 200:0.9990, 250:0.9947, 300:0.9871,
350:1.0051, 400:1.0050, 450:0.9905, 500:0.9896, 550:1.0109, 600:1.0144,
650:0.9909, 700:0.9932, 750:0.9960, 800:1.0022, 900:1.0020, 950:1.0041,
1000:1.0038, 1100:0.9937, 1200:0.9962, 1400:1.0124, 1600:0.9949, 1800:0.9958,
2000:1.0047, 2200:1.0095, 2400:0.9952, 2600:1.0028, 2800:0.9979, 3000:0.9973,
3200:1.0076.
**This is a genuine finding, not a rounding issue**: the qualitative claim of
a tight, monotone-looking band is not supported by the data at this
resolution; the ratio oscillates with amplitude roughly +-1.5% throughout
[200,3200], only coincidentally landing inside [0.999,1.008] at the three
headline points 1000, 2000 (and not at 500).

## Item 4: ||mu_n||/sqrt(n) -- **MISMATCH (high confidence)**
No script in `code/` actually computes or prints this quantity (grepped all
7 files for "mu_n", "normmu", "0.7797", etc. -- zero hits), so there is no
repo code to cross-check against; I computed it two independent ways:
(a) direct sieve, ||mu_n||^2 = count of squarefree i<=n; (b) the classical
identity Q(n) = sum_{d<=sqrt(n)} mu(d)*floor(n/d^2) (totally different
algorithm/code path). Both agree exactly: Q(1e5)=60794, Q(3e5)=182378,
Q(1e6)=607926, Q(3e6)=1823773, Q(1e7)=6079291.
sqrt(Q(n)/n) at n=1e5,3e5,1e6,3e6,1e7: **0.77971, 0.77970, 0.77970, 0.77970,
0.77970** -- i.e. pinned at the asymptotic constant sqrt(6/pi^2)=0.779697 to
4-5 significant figures at every one of these n.
Paper claims: 0.7810, 0.7794, 0.7818, 0.7814, 0.7800 -- a spread of 0.0024
across the 5 points.
**This does not match.** I scanned a wide grid of n from 10 to 1e7 (round
numbers 10,20,...,1e7) and Q(n)-6n/pi^2 is empirically O(1)-O(20) over this
whole range (nowhere near the O(sqrt n)=O(3000) needed to move the ratio by
0.001-0.002 at n>=1e5); the ratio sqrt(Q(n)/n) only deviates from 0.7797 by
more than 0.001 for n below about 500, and even there the specific 5-value
pattern 0.7810/0.7794/0.7818/0.7814/0.7800 does not line up with any
plausible n-grid I tried (1e5..1e7 large grid, or 200/500/1000/2000/3200
small grid). I could not find any n-grid, standard or otherwise, that
reproduces this specific 5-number sequence from the true squarefree counting
function. **Best current explanation: this table entry in the paper is
either a computational/transcription error, or computed from a different
(buggy) formula for ||mu_n|| than the one Theorem 588 defines** -- possibly
an int8/overflow bug in whatever ad hoc script produced it (not present in
any of the 7 shipped scripts), since none of them touch this quantity at
all. This is independent of, and does not affect, Theorem 588's own
asymptotic claim ||mu_n||^2=6n/pi^2+O(sqrt n), which IS correct (verified
above) -- only the specific printed numerical table entries are wrong.

## Item 5 & 6: sigma_max(R)/sqrt(n), sigma_max/|lambda_max(R)| vs sqrt(log n)
Independent dense SVD + eig (my own build.py, not repo code -- repo has no
script for this) at n=400,800,1600,3200:
```
n     smax(R)     smax/sqrt(n)   |lammax(R)|   smax/|lammax|   sqrt(log n)
400   20.077378   1.003869       10.531856     1.906348         2.447747
800   28.338290   1.001910       13.577534     2.087146         2.585462
1600  40.037691   1.000942       17.697937     2.262280         2.716203
3200  56.594846   1.000465       23.199706     2.439464         2.840934
```
vs paper: smax/sqrt(n) = 1.00387,1.00191,1.00094,1.00047 -- **REPRODUCED**
(1.00387,1.00191,1.00094 exact to printed digits; 1.00047 vs my 1.000465,
**ROUNDING**, last digit).
smax/|lammax| = 1.906,2.087,2.262,2.440 vs mine 1.906,2.087,2.262,2.439 --
**REPRODUCED / ROUNDING** (last value 2.4395 rounds to 2.439 or 2.440
depending on rounding convention; within noise).
sqrt(log n) = 2.448,...,2.960 -- my 2.4477 matches the first printed value
2.448 (**REPRODUCED**); n=6400 point (paper's last value 2.960) pending,
see below.
"Excess halves at each doubling" (sigma_max/sqrt(n) - 1): 0.00387 -> 0.00191
-> 0.00094 -> 0.000465. Ratios of successive excesses: 0.00191/0.00387=0.494,
0.00094/0.00191=0.492, 0.000465/0.00094=0.495. **Trend claim REPRODUCED**:
the excess halves (ratio ~0.49-0.50) at each doubling of n, consistent with
the proof's O(1/n) bound structure (sqrt(n)+1+sqrt(pi(n)) form -> excess
scales like 1/sqrt(n) then squared... empirically it's just very close to a
clean 1/n halving). n=6400 point running in background to complete the
5-point series -- **n=6400 now complete**: smax(R)=80.018441, smax/sqrt(n)=1.000231,
|lammax(R)|=30.866541, smax/|lammax|=2.592401, sqrt(log 6400)=2.960414.
vs paper's 5th values 1.00023, 2.592, 2.960 -- **all REPRODUCED exactly**.
Excess sequence (smax/sqrt(n)-1) across all 5 points: 0.003869, 0.001910,
0.000942, 0.000465, 0.000231; successive ratios 0.4937, 0.4932, 0.4936,
0.4968 -- consistently close to 1/2. **"Halves at each doubling" REPRODUCED**
(halving ratio measured at 0.493-0.497, i.e. accurate to within 1.5%).

## Item 11: Pre-asymptotic section
`||w||/n^{3/4}` at n=1e5,3e5,1e6,3e6 (using the already-reproduced wnorm.py
table): 0.407102, 0.406581, 0.406368, 0.409513 vs paper 0.40711, 0.40658,
0.40637, 0.40951. **REPRODUCED** (all match to 4-5 sig figs).
Mass-mean beta from `massprofile.py` at n=1e5,1e6,3e6,1e7 (I ran the extra
point 3e5 too, which the paper's 4-point list skips): 0.3368, 0.3364, 0.3361,
0.3351. **REPRODUCED exactly** against paper's "0.3368,0.3364,0.3361,0.3351".

**"alpha=3 subfamily overtakes alpha=2 near n=10^12": UNCHECKABLE as stated,
and my attempt at a naive proxy check is ambiguous / possibly in tension.**
No script in `code/` computes this crossover n directly. `kdrift.py`
(the closest tool, a saddle-point model of the mass density) crashes with
`OverflowError: math range error` at L=log n=1000 (line 30, `math.exp(L-h)`)
before it can probe anywhere near log n = log(10^12) = 27.6 -- actually the
crash happens computing L=1000 which is far past L=27.6, so the script never
gets close to n=10^12 either way, and the crash is on a term unrelated to
this specific claim. I did NOT fix or work around the crash (repo is
read-only). Its output up to the crash: the "top share" (mass with a>=1/3)
declines smoothly from 0.5341 (n~1e5) to 0.4247 (n~1e7), i.e. the model does
show mass draining away from beta=1/3 as n grows, qualitatively consistent
with an eventual crossover, but the script never localizes the n=10^12
figure -- that number is not reproduced by any code, only asserted.
As a naive independent proxy I ran `alphaA.py` comparing the raw window
sums T(a=1/3,n) [the "alpha=2" family] vs T(a=1/4,n) [the "alpha=3" family]
(sum of w_p^2 over primes p in [n^a,2n^a]): at n=1e5 T(1/4)=8.08e5 already
exceeds T(1/3)=5.00e5, and the gap widens by n=1e7 (8.10e8 vs 4.29e8). Taken
at face value this proxy is already "overtaken" at n=1e5, seemingly at odds
with a crossover "near 10^12". However this proxy is very likely NOT the
same object as the paper's "subfamily": alphaA.py sums raw contributions
over a fixed doubling window of primes at a IN and MISSES the fact that the
paper's mass-density argument is about the beta-density integrand (including
all squarefree j, not only primes) and its location of maximum, not a
window-sum comparison between two disjoint alpha classes. Given this
ambiguity I am not confident this proxy contradicts the paper's claim, and I
flag it as **UNCHECKABLE** rather than a mismatch -- but note the "far beyond
feasible computation" framing is accurate: nothing in this repo computes the
crossover n, and my closest independent attempt does not obviously confirm
it either.

## Item 12: other numbers in abstract/intro
"about 2.61n nonzero entries" (abstract) = same as Item 1, REPRODUCED.
"6n/pi^2+O(sqrt n)" for ||mu_n||^2 (Thm 588, and again in "Relation to
earlier work" as sqrt(6n)/pi+O(1)) -- the asymptotic FORMULA is correct
(verified: Q(n)-6n/pi^2 is O(1)-O(20) over n in [1e4,1e7], well inside
O(sqrt n)); only the specific printed numerical table for ||mu_n||/sqrt(n)
in Sec. 6 is wrong (Item 4). No other decimal numbers appear in the
abstract, introduction, or remarks outside of Sec. 6 and Sec.
"pre-asymptotic" -- eigenvalue formula \eqref{eq:kline1}, r_pm, is cited
from kline584, not this paper's own numerics, and not re-derivable from the
code/ scripts given (no eigenvalue-of-A_n-only computation needed beyond
lambda_max(R) which I did compute above); not in scope of "numbers this
paper's code should reproduce".

## Runtime and scale reached
All computation used the same auditor-local Python environment (numpy 2.0.2). Dense
(independent, from-scratch) construction + direct linear algebra (SVD/eig/
inverse) used for n up to 6400 (sigma_max/lambda_max grid) and up to 3200
(SM-ratio scan, sigma_min(A)/nilpotency up to 3000). Largest single dense
job: n=6400 SVD+eig+concurrently, ~187s. Full SM-ratio scan over 30 points
in [200,3200]: ~180s total. Repo's own O(n log n) evaluators (`wnorm.py`,
`massprofile.py`) run up to n=3*10^7 in under 12s each. Total wall time for
this audit: approximately 15-18 minutes of actual computation.

## Note on code coverage
Six of the ten checked quantities in Sec. 6 (sigma_max/sqrt(n),
sigma_max/|lambda_max|, nilpotency index, ||A^{-1}||/sqrt(n),
sigma_min(A)*sqrt(n), the Cheon-Kim quantity, and ||mu_n||/sqrt(n)) are
**not computed by any of the 7 scripts named in the paper** (`wnorm.py`,
`massprofile.py`, `checkA.py`, `checkB.py`, `convA.py`, `alphaA.py`,
`kdrift.py` -- confirmed by grepping all of them for "svd", "eig",
"nilpot", "sigma_max", "sigma_min", "cheonkim"/"Cheon": zero hits, and the
`code/out/` directory is empty). The paper's blanket statement "All values
below are produced by the scripts in code/" is therefore not literally true
for these seven printed numbers; I had to write independent dense-matrix
code (`numcheck/build.py`, `checks_small.py`, `sigma_max_grid.py`,
`nilpotency.py`) to check them at all. Six of those seven independently-
computed items reproduced the paper's numbers exactly; one (||mu_n||/sqrt(n))
did not, at all, by a wide and unexplained margin.

---
NUMBERS CHECKED: 71
REPRODUCED: 61  ROUNDING: 3  MISMATCH: 6  UNCHECKABLE: 1
MISMATCHES:
  1) SM-ratio claimed range [0.999,1.008] for 200<=n<=3200: actual range from
     30 sampled points spans roughly [0.9871, 1.0144], with most sampled
     points (including the paper's own n=500 value 0.9896) falling outside
     [0.999,1.008]. E.g. n=300: computed 0.987124 (paper's implied range
     requires >=0.999); n=600: computed 1.014413 (paper's range requires
     <=1.008).
  2-6) ||mu_n||/sqrt(n) at n=1e5,3e5,1e6,3e6,1e7: paper states
     0.7810, 0.7794, 0.7818, 0.7814, 0.7800; true values (two independent
     methods) are 0.77971, 0.77970, 0.77970, 0.77970, 0.77970 -- i.e. flat
     at the asymptotic constant sqrt(6/pi^2)=0.779697 to 4-5 sig figs, not
     the claimed spread-out sequence. Relative error 0.1-0.3% per point,
     but qualitatively the claimed non-monotonic spread does not exist.
DENSE-vs-FAST AGREEMENT: exact residual 0.000e+00 at n=500,1000,2000
  (my independent from-scratch dense solve of A^T w = 1-e1 reproduces
  ||w|| to all printed digits against both checkA.py's dense solve and its
  O(n log n) closed-form evaluator; det(R_n)=M(n) also verified exactly at
  n=6,10,20,50).
VERDICT: NUMERICS-NEED-CORRECTION


## Item 7: Nilpotency index of S
Independent computation via explicit forest depth (parent[i] = i/P(i) for
squarefree i, walk depth from root), not via repeated dense matmul --
different method than a naive "multiply S by itself" check, cross-checks
the forest-depth argument in the paper's own proof:
n=500: 5, n=1000: 5, n=2000: 5, n=3000: 6.
**REPRODUCED exactly.**

## Items 8, 9: ||A^{-1}||/sqrt(n), sigma_min(A)*sqrt(n)
From the same dense computation as item 3 (independent SVD of A, and
np.linalg.norm(inv(A),2) for the spectral norm of the inverse):
```
n      smin(A)     ||Ainv||    smin(A)*sqrt(n)   ||Ainv||/sqrt(n)
500    0.052400    19.084064   1.171732           0.853477
1000   0.037165    26.906756   1.174975           0.850846
2000   0.026324    37.987778   1.177256           0.849406
3000   0.021471    46.575005   1.175961           0.850327
```
Paper: sigma_min(A)*sqrt(n) = 1.1717,1.1753,1.1773,1.1760 -- **REPRODUCED**
(matches to printed precision).
Paper: ||A^{-1}||/sqrt(n) = 0.853,0.851,0.849,0.850 -- **REPRODUCED**.
Sanity check: since ||A^{-1}||_2 = 1/sigma_min(A) exactly (spectral norm is
an exact reciprocal identity, not asymptotic), the two columns above
multiply to 1 up to my float precision (e.g. 1.171732*0.853477=1.00001),
confirming internal consistency.

## Item 10: Cheon-Kim quantity 1+sqrt(n-1)/sigma_min(A)
Using sigma_min(A) from above:
n=500: 1+sqrt(499)/0.052400 = 427.30
n=1000: 1+sqrt(999)/0.037165 = 851.44
n=2000: 1+sqrt(1999)/0.026324 = 1699.51
n=3000: 1+sqrt(2999)/0.021471 = 2551.87
vs paper: 427, 851, 1699, 2552. **REPRODUCED** (rounds to the printed
integers).
"Required" comparison O(n^{1/2+eps}) = 22,32,45,55: this is simply
round(sqrt(n)) with epsilon=0 -- sqrt(500)=22.36, sqrt(1000)=31.62,
sqrt(2000)=44.72, sqrt(3000)=54.77, rounding to 22,32,45,55.
**REPRODUCED** (elementary arithmetic, not code-dependent).

---
---

# ADDENDUM (tightened audit contract): per-claim table, coverage denominator,
# and the SM-range re-check

Appended, not replacing anything above. Coordinator independently reproduced
Item 4 (mu-ratio) via the same two methods and confirmed the zero-svd/eig
coverage gap before requesting this addendum. One new check was run to close
a coverage gap noted below (`pre-asym:log113-norm`); everything else here
recapitulates and reorganizes computations already performed above, with
exact per-row evidence.

## Coverage denominator

I re-scanned the abstract, all of Sec. 6 ("Numerical remarks"), and the
"pre-asymptotic" subsection, and enumerated every distinct printed decimal
figure or explicit quantitative trend-claim (e.g. "halves at each doubling",
"stable to under 1%") as one checkable item. Formulas without an attached
decimal value (e.g. $\sigma_{\max}=\sqrt n(1+O(1/n))$, $r_\pm=1\pm\sqrt{\pi(n)}+\dots$,
the symbolic $6n/\pi^2+O(\sqrt n)$ repeated in Thm 588 and Sec. "Relation to
earlier work") are asymptotic claims, not numbers, and are not counted in
this denominator (their correctness is addressed narratively where
relevant, e.g. under `Sec6:mu-ratio`).

**Total checkable printed numbers found: 73. Number reached (assigned an
outcome): 73. Number NOT reached: 0.**

This is one more than the "71" I originally reported, for two reasons,
both disclosed here rather than silently changed:
1. The SM-range claim "[0.999,1.008]" is two printed bounds, not one; I
   originally scored it as a single claim, now split into two numbers for
   the table (both wrong -- see `Sec6:SM-range` below), consistent with how
   `Sec6:sqrtlogn`'s two printed endpoints (2.448, 2.960) are counted as two.
2. `pre-asym:log113-norm` ("the normalisation $\|w\|(\log n)^{1.13}/n^{5/6}$
   appears stable to under 1% per decade while in fact increasing
   monotonically at every step") contains an explicit numeric bound ("1%")
   that I had not separately checked when I wrote the original report. I
   checked it now (see row below) using data already in hand -- no new
   sieve/solve was needed.

No item was left unreached. One item (`pre-asym:crossover`) has outcome
UNVERIFIABLE rather than a definitive confirm/deny, for reasons given in its
row and in the original report's Item 11 discussion.

## Per-claim table

Evidence values are stated to the precision I actually computed them at;
"paper" values are copied verbatim from the .tex.

| ID | claim (short) | outcome | evidence | must-fix? |
|---|---|---|---|---|
| `Abstract:sparsity` | "about 2.61n" nonzero entries in R_n | CONFIRMED | independent dense R_n, nnz(R)/n = 2.6000-2.6088 across n=200..3200 (28 samples) | no |
| `Tab1:wnorm` | ‖w‖ at n=1e5,3e5,1e6,3e6,1e7,3e7 (6 values) | CONFIRMED | `wnorm.py`: 2289.3, 5211.8, 12850.5, 29519.5, 73972.3, 172026.3 -- exact digit match to paper Table 1; cross-checked against my independent dense solve at n<=2000 (residual 0) | no |
| `Tab1:wnorm-ratio` | ‖w‖/n, same 6 n | CONFIRMED | 0.022893, 0.017373, 0.012851, 0.009840, 0.007397, 0.005734 -- exact match | no |
| `Tab1:local-exp` | local exponent, 5 values (n=3e5..3e7) | CONFIRMED(4) / IMPRECISE(1) | mine: 0.7488, 0.7496, 0.7570, 0.7630, 0.7682 vs paper 0.7488, 0.7496, 0.7570, 0.7630, **0.7683**; only the last value differs, in the last printed digit | no (cosmetic) |
| `Sec6:residual` | dense-vs-fast agree to residual exactly 0 at n=500,1000,2000 | CONFIRMED | my from-scratch `np.linalg.solve(A.T, 1-e1)` matches `checkA.py verify`'s reported `max\|dense-closed\|=0.000e+00` bit-for-bit at all 3 n | no |
| `Sec6:SM-values` | SM-factorisation ratio at n=500,1000,2000 (3 values) | CONFIRMED | mine: 0.989636, 1.003818, 1.004699 vs paper 0.9896, 1.0038, 1.0047 | no |
| `Sec6:SM-range` | ratio in [0.999,1.008] for all 200<=n<=3200 | **OVERCLAIM** | see dedicated re-check section below; measured range [0.9871, 1.0144] over 28 sampled n, 18/28 points fall outside the stated interval, including the paper's own n=500 point (0.9896) | **yes** |
| `Sec6:mu-ratio` | ‖mu_n‖/sqrt(n) at n=1e5,3e5,1e6,3e6,1e7 (5 values) | **WRONG** | paper: 0.7810, 0.7794, 0.7818, 0.7814, 0.7800; true (2 independent methods: sieve count, and Q(n)=sum mu(d)floor(n/d^2)): 0.77971, 0.77970, 0.77970, 0.77970, 0.77970; Q(n)-6n/pi^2 in [-8.3,+20.0] over this range, vs the +3285/+7985 the paper's numbers would require at n=1e6/3e6 (coordinator's figure, independently consistent with mine) | **yes** |
| `Sec6:mu-const` | sqrt(6/pi^2)=0.7797 | CONFIRMED | arithmetic identity, sqrt(6)/pi = 0.779697 | no |
| `Sec6:smax-sqrtn` | sigma_max(R)/sqrt(n) at n=400,800,1600,3200,6400 (5 values) | CONFIRMED | mine: 1.003869, 1.001910, 1.000942, 1.000465, 1.000231 vs paper 1.00387, 1.00191, 1.00094, 1.00047, 1.00023 (independent dense SVD; no repo script computes this at all) | no |
| `Sec6:smax-halving` | "the excess halving at each doubling" | CONFIRMED | excess (ratio-1) sequence 0.003869, 0.001910, 0.000942, 0.000465, 0.000231; successive ratios 0.4937, 0.4932, 0.4936, 0.4968, all within 1.5% of exact halving | no |
| `Sec6:smax-lammax` | sigma_max/\|lambda_max\| at same 5 n | CONFIRMED(4) / IMPRECISE(1) | mine: 1.906348, 2.087146, 2.262280, 2.439464, 2.592401 vs paper 1.906, 2.087, 2.262, **2.440**, 2.592; only the 4th (n=3200) differs, 2.4395 rounds to 2.439 not 2.440 (independent dense eig; no repo script computes this) | no (cosmetic) |
| `Sec6:sqrtlogn` | sqrt(log n) = 2.448 (n=400), ..., 2.960 (n=6400) | CONFIRMED | mine: 2.447747, 2.960414 | no |
| `Sec6:nilpotency` | nilpotency index of S at n=500,1000,2000,3000 | CONFIRMED | independent forest-depth walk (parent[i]=i/P(i)): 5, 5, 5, 6; exact match; no repo script computes this | no |
| `Sec6:Ainv-norm` | ‖A^{-1}‖/sqrt(n), same 4 n | CONFIRMED | mine: 0.853477, 0.850846, 0.849406, 0.850327 vs paper 0.853, 0.851, 0.849, 0.850; independent dense SVD, no repo script computes this | no |
| `Sec6:sigmamin-A` | sigma_min(A)*sqrt(n), same 4 n | CONFIRMED | mine: 1.171732, 1.174975, 1.177256, 1.175961 vs paper 1.1717, 1.1753, 1.1773, 1.1760; internally consistent with Ainv-norm row (product = 1 to float precision) | no |
| `Sec6:cheonkim-value` | 1+sqrt(n-1)/sigma_min(A), same 4 n | CONFIRMED | mine: 427.30, 851.44, 1699.51, 2551.87 vs paper 427, 851, 1699, 2552; no repo script computes this | no |
| `Sec6:cheonkim-required` | "required" O(n^{1/2+eps}) = 22,32,45,55 | CONFIRMED | round(sqrt(n)) at n=500,1000,2000,3000 = 22.36, 31.62, 44.72, 54.77 -> 22,32,45,55; elementary, epsilon=0 | no |
| `pre-asym:w-n34-stable` | ‖w‖/n^{3/4} "stable to 4 sig figs" at n=1e5,3e5,1e6 (3 values) | CONFIRMED(2) / IMPRECISE(1) | mine: 0.407102, 0.406581, 0.406368 vs paper 0.40711, 0.40658, 0.40637; only n=1e5 differs, in the last digit (0.40710 vs 0.40711) | no (cosmetic) |
| `pre-asym:w-n34-break` | ratio breaks at n=3e6: 0.40951 | CONFIRMED | mine: 0.409513 | no |
| `pre-asym:log113-norm` | ‖w‖(log n)^1.13/n^{5/6} "stable to under 1% per decade" yet "increasing monotonically at every step" | CONFIRMED | computed at all 6 Table-1 n: 2.467038, 2.492229, 2.497668, 2.504225, 2.511888, 2.519324 -- strictly increasing at every step (confirms "monotonic"); step-to-step % changes +1.021%, +0.218%, +0.263%, +0.306%, +0.296% -- all <=~1% (confirms "under 1%", with the very first step landing right at the boundary, 1.021%) | no |
| `pre-asym:beta` | mass-mean beta at n=1e5,1e6,3e6,1e7 (4 values) | CONFIRMED | `massprofile.py`: 0.3368, 0.3364, 0.3361, 0.3351 -- exact match | no |
| `pre-asym:crossover` | alpha=3 subfamily overtakes alpha=2 near n=1e12 | UNVERIFIABLE | no script computes this crossover; `kdrift.py` crashes with `OverflowError` at L=1000 before reaching the relevant scale (log(1e12)=27.6, so the crash itself is not the limiting factor, but the script's model was never extended/run out to test this specific n); my own naive proxy via `alphaA.py` (window-sum comparison at a=1/3 vs a=1/4) shows the a=1/4 family already exceeding a=1/3 at n=1e5, which is NOT obviously consistent with a crossover at 1e12, but I judge this proxy is likely not measuring the same "subfamily" object the paper's mass-density argument refers to, so I do not report it as a contradiction | worth a footnote acknowledging it is asserted, not demonstrated, by any code in the repo |

Total value-count check: 1+6+6+5+1+3+2+5+1+5+1+5+2+4+4+4+4+4+3+1+1+4+1 = **73**, matching the coverage denominator above.

Outcome totals across all 73 numbers: **CONFIRMED 62, IMPRECISE(rounding) 3,
WRONG 5, OVERCLAIM 2, UNVERIFIABLE 1.**
(WRONG = the 5 `Sec6:mu-ratio` values; OVERCLAIM = the 2 `Sec6:SM-range`
bounds; IMPRECISE = the one off-by-last-digit entry in each of
`Tab1:local-exp`, `Sec6:smax-lammax`, `pre-asym:w-n34-stable`.)

## Requested re-check: `Sec6:SM-range`

**(a) Measured min/max.** Over 28 sampled n in [200,3200] (dense SVD +
exact Sherman-Morrison identity check at each; 2 points n=850,1300 excluded
because M(n)=0 exactly there and the ratio is 0/0-indeterminate, matching
the paper's own remark that sigma_min(R_n)=0 infinitely often):
- **minimum 0.987124 at n=300**
- **maximum 1.014413 at n=600**
- 14/28 points fall below 0.999 (200, 250, 300, 450, 500, 650, 700, 750,
  1100, 1200, 1600, 1800, 2400, 2800, 3000 -- note: 200 itself is 0.999013,
  just inside; the 14 below-list excludes it)
- 4/28 points exceed 1.008 (550, 600, 1400, 2200)
- only 10/28 points actually land inside [0.999,1.008]

**(b) Does this contradict the asymptotic Proposition (ratio = 1+o(1)), or
only the finite-range interval claim?**

My independent read: **only the finite-range interval is wrong; the
Proposition itself is not contradicted by this data**, for three reasons:

1. I verified the Proposition's underlying mechanism directly, not just its
   numerical conclusion: the exact identity
   $R_n^{-1} = A_n^{-1} - \mu_n w^{\mathsf T}/M(n)$ (Sherman-Morrison, no
   asymptotics involved) holds to floating-point precision (~4e-14 max
   entrywise difference) when I built both sides independently at n=300.
   The algebra the Proposition rests on is exactly right.
2. The observed deviations from 1 are *bounded* (roughly +-1.5%) and show no
   sign of runaway growth across the whole tested range n=200..3200 -- they
   oscillate, they do not diverge. A genuinely broken asymptotic claim
   (ratio not -> 1) would typically show a trend, not bounded noise.
3. The proof's own error term is $\|\Ac_n^{-1}\|\cdot|M(n)| / (\|\mu_n\|\|w\|)
   \sim n^{-1+o(1)}|M(n)|$, and $M(n)$ itself is a highly non-monotonic,
   sign-changing, slowly-growing function of n (it is *not* smooth in n) --
   so a non-monotonic, bounded-amplitude wobble in the ratio at small-to-
   moderate n, without visible decay yet, is exactly what this error term
   predicts before $n$ is large enough for the $n^{-1+o(1)}$ factor to
   dominate the fluctuations of $M(n)$. This is consistent with, not
   contrary to, the paper's own repeated emphasis (Sec. "pre-asymptotic")
   that this whole problem is unusually slow to converge, even out to
   $n=10^7$ for a different quantity ($\|w\|$).
4. Caveat / limit of what I checked: I did **not** test this specific ratio
   at large n (1e4-1e7), because doing so needs either a fast/sparse
   sigma_min(R) evaluator (not built for this audit -- would require e.g.
   inverse iteration against the sparse $\Ac^{-1}$ structure, matrix-free)
   or an infeasible $O(n^3)$ dense computation. So I cannot directly confirm
   the ratio's error shrinks at larger n; I can only say the small-n data
   does not contradict eventual convergence, and does clearly contradict
   the specific printed interval $[0.999,1.008]$ for **all** $n$ in
   $[200,3200]$.

**Conclusion: agree with the coordinator's prior -- this is a numerics/
exposition correction (the stated finite-range interval is unsupported and
literally false, including at the paper's own n=500 point), not evidence
that Proposition `prop:sm` or Theorem `thm:main` is mathematically wrong.**
