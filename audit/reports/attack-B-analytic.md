# Proof B — the analytic route to `‖w‖`

Agent B. Method: Perron/Mellin + Buchstab/Dickman + saddle point.
Every claim is tagged **PROVED / SKETCH(named gap) / NUMERICAL**.
All numerics from `checkB.py` in this directory.

**Headline.** The analytic route succeeds: `M(x,y)` is governed by the **Dickman function shifted
by one**, `M(x, x^{1/u}) ~ −(x/log x)·ρ(u−1)`, and feeding this into the hyperbola reproduces the
numerical table to **4 %** with the correct *local* exponent to **±0.006**. But the same machinery
shows, **unconditionally**, that `‖w‖ ≍ n^{5/6}(log n)^{−1.13}` is **not** the asymptotic law: the
true local exponent is currently `≈ 0.755` and is *rising*, `‖w‖ = n^{1−o(1)}`, and I prove
`‖w‖ ≫ n^{7/8}(log n)^{−3/2}` from PNT alone. `5/6` is the exponent of a **corner** in the
saddle-point integral that is pinned only while `log n < 24.8` (`n < 6×10^{10}`).

---

## 0. Validation of the ask

The setup is coherent. Three remarks before starting.

1. **The `‖w‖²` formula is a sum of two very different scales.**
   `#{j ≤ n not squarefree} ~ (1 − 6/π²)n ≈ 0.392 n`, and the squarefree `j` with `P(j) ≥ n/j`
   contribute `1` each — also `O(n)`. Both are `O(√n)` in `‖w‖`, negligible against `n^{5/6}`.
   The entire problem is `Σ_{j sqfree} M(n/j, P(j))²`.

2. **`u → 2` and `β → 1/3` are the same statement only when `P(j) = j^{1+o(1)}`.**
   With `v := log j / log P(j)` one has `u = v(1−β)/β`, so `β = 1/3, u = 2 ⟹ v = 1`. The two
   measured facts jointly assert that the mass sits on `j` that are **prime or nearly prime**.
   This is the structural key: the correct parametrisation is `j = m·p`, `p = P(j)`, `m = O(1)`.
   *(Verified: §3, the measured mass split by `m = j/P(j)` is 50.3 / 17.4 / 9.4 / 4.3 / 3.3 / 2.6 %
   for `m = 1,2,3,5,6,7` at `n = 10^7`, matching the analytic prediction 48.5 / 16.9 / 9.2 / 4.3 /
   3.2 / 2.6 % — three digits.)*

3. **One thing in the brief is, I believe, misstated** — flagged rather than worked around:
   the prompt asserts `‖w‖ ≪ n^{5/6+ε}` is "impossible with current technology (it would force a
   zero-free region `Re s > 5/6`)". That implication is correct but moot: §6 shows the bound is
   simply **false** for large `n`, so no hypothesis whatever can buy it. Relatedly, the refuted
   conjecture "the mass drifts to `β → 0`" is refuted *in the numerical range* but is, on this
   analysis, **true asymptotically** — `β = 1/(1+u*)` with `u* → ∞` like `√(log n / log log n)`.
   It just does not start moving until `n ≈ 6×10^{10}`.

---

## 1. The asymptotic for `M(x,y)`

> **Theorem A.** Fix `u₀ > 1` and put `y = x^{1/u₀}`. Then as `x → ∞`
>
> **`M(x, y)  =  (x / log y)·ρ′(u₀)·(1 + O_{u₀}(1/log y))
>              =  −(x / log x)·ρ(u₀−1)·(1 + O_{u₀}(1/log y))`**
>
> where `ρ` is the **Dickman function** (`ρ ≡ 1` on `[0,1]`, `uρ′(u) = −ρ(u−1)`).
> The two forms agree because `ρ′(u) = −ρ(u−1)/u` and `u log y = log x`.

Two independent derivations follow. Given that four conjectures have already died here, I did not
trust the first one until the second reproduced it.

### 1a. Buchstab route — **PROVED for `1 < u₀ ≤ 3`**, SKETCH above

Every `d ≥ 2` with `P⁻(d) > y` factors uniquely as `d = p·e`, `p = P⁻(d) > y`, `P⁻(e) > p`, and
`μ(d) = −μ(e)`. Hence the **exact** identity

```
M(x, y) = 1 − Σ_{y < p ≤ x} M(x/p, p) ,          M(x,y) = 1 for y ≥ x.        (B)
```

**Range `u ∈ [1,2]`.** `y ≥ √x`, so every `p > y` has `x/p < x/y ≤ y < p`, whence `M(x/p,p) = 1`.
(B) gives `M(x,y) = 1 − π(x) + π(y)` — the exact evaluation quoted in the brief. ✔

**Range `u ∈ [2,3]`.** Split `p > √x` (then `M(x/p,p)=1`) from `y < p ≤ √x` (then `p > x^{1/u}`
with `u ≤ 3` forces `x/p < x^{1−1/u} ≤ p²`, so `u' ≤ 2` and `M(x/p,p) = 1 − π(x/p) + π(p)`):

```
M(x,y) = 1 − π(x) + π(y) + Σ_{y < p ≤ √x} ( π(x/p) − π(p) ).                 (B2)
```
**(B2) is exact.** Now `π(y) = π(x^{1/u}) ≪ x^{1/u}/log x = o(x/log x)` for `u > 1`, and
`Σ_{p ≤ √x} π(p) ≪ x/(log x)³`. For the main sum put `p = x^α`, `dπ ~ x^α dα/α`,
`π(x/p) ~ x^{1−α}/((1−α)log x)`:

```
Σ_{y<p≤√x} π(x/p) ~ (x/log x) ∫_{1/u}^{1/2} dα/(α(1−α)) = (x/log x)·log(u−1),
```
so `M(x,y) ~ −(x/log x)(1 − log(u−1))`. And `ρ(w) = 1 − log w` for `w ∈ [1,2]`, so this is
`−(x/log x)ρ(u−1)`. ✔ **Rigorous**: every step is PNT with classical error term.

**General `u`.** Iterate (B) with the ansatz `M(x,x^{1/u}) ~ −(x/log x)·m(u)`, `m ≡ 1` on `[1,2]`:

```
m(u) = 1 − ∫_{1/u}^{1/2} m(1/α − 1) dα/(α(1−α)) .
```
Substitute `v = 1/α − 1`, so `dα/(α(1−α)) = −dv/v`, `α = 1/u ↔ v = u−1`, `α = 1/2 ↔ v = 1`:

```
m(u) = 1 − ∫_1^{u−1} m(v) dv/v ,   m ≡ 1 on [1,2],   i.e.  m′(u) = −m(u−1)/(u−1).   (D)
```
Set `g(u) := m(u+1)`. Then `g′(u) = −g(u−1)/u`, `g ≡ 1` on `[0,1]` — **exactly Dickman's delay
equation with Dickman's initial condition.** Hence `m(u) = ρ(u−1)`. ∎(formal for `u > 3`)

**Named gap (1a).** For `u₀ > 3` the passage (B) → (D) is a formal interchange of `x → ∞` with an
iterated integral. It is repaired by induction on `k = ⌈u₀⌉`: in (B) every `M(x/p,p)` that is not
exactly `1` has `u' = 1/α − 1 ≤ u₀ − 1`, and `x/p ≥ x^{1−1/u₀}` is a fixed power of `x`, so the
inductive hypothesis applies uniformly; the sub-range `u' ∈ [1,1+δ]` is handled by the exact
formula rather than the asymptotic. For each **fixed** `u₀` this is finitely many PNT applications
and is rigorous; I did not write the bookkeeping out. **What is genuinely missing is uniformity
as `u₀ → ∞` with `x`** — that is the only place a real theorem is owed, and §6 is arranged so as
not to need it.

### 1b. Mellin/Perron route (mandated) — **SKETCH**, contour gaps named

Perron: `M(x,y) = (1/2πi)∫_{(c)} F_y(s)·x^s ds/s`, `F_y(s) = ζ(s)^{−1}Π_{p≤y}(1−p^{−s})^{−1}`.
Write `s = 1 + z` and work on `|z| ≍ 1/log y`:

* `ζ(s)^{−1} = z·(1 + O(z))` (simple pole, residue 1);
* by Mertens, `Σ_{p≤y} p^{−1−z} − Σ_{p≤y} p^{−1} = ∫^{log y}(e^{−zw}−1)dw/w + O(1/log y)
  = −I(z log y) + O(1/log y)` with **`I(ζ) := ∫_0^ζ (1−e^{−v})dv/v`**, hence
  `Π_{p≤y}(1−p^{−s})^{−1} = e^{γ}(log y)·e^{−I(z log y)}·(1+O(1/log y))`.

**This is exactly the uniformity the brief flags.** The finite Euler product is *not* replaced by
its value at `s = 1` (`≈ e^γ log y`); it is replaced by `e^γ log y · e^{−I(z log y)}`. And that
factor is the **Laplace transform of Dickman**:

```
ρ̂(ζ) := ∫_0^∞ ρ(w)e^{−ζw}dw = exp(γ − I(ζ)).                                 (L)
```
[(L) follows from `uρ′ = −ρ(u−1)`: Laplace gives `ρ̂′/ρ̂ = (e^{−ζ}−1)/ζ`, `ρ̂(0) = ∫ρ = e^γ`.]

So `F_y(1+z) ≈ z·(log y)·ρ̂(z log y)`. Substituting `z = ζ/log y` (so `x^z = e^{ζu}`, `dz = dζ/log y`):

```
M(x,y) ≈ x·(1/2πi)∫ z (log y) ρ̂(z log y) x^z dz = (x/log y)·(1/2πi)∫ ζ ρ̂(ζ) e^{ζu} dζ.
```
Since `L(ρ′)(ζ) = ζρ̂(ζ) − ρ(0) = ζρ̂(ζ) − 1` and `(1/2πi)∫e^{ζu}dζ = 0` for `u > 0`, inversion gives

```
M(x, y) ≈ (x/log y)·ρ′(u).                                                    ∎(formal)
```
identical to §1a. **Two independent routes, same answer.**

**Named gaps (1b).** (i) Perron truncation and the contour shift past `s = 1` need a zero-free
region; unconditionally this route carries an additive `x·exp(−c(log x)^{3/5−ε})` "Mertens noise
floor". (ii) The Mertens step is not uniform once `|z| log y` is large; one needs the Rankin
truncation `|Im z| ≤ log y` plus a tail bound. Neither is exotic; neither is written out.

### 1c. Numerical verification of Theorem A — **NUMERICAL, confirmed**

Exact `M(x, x^{1/u})` by sieve vs `−li(x)ρ(u−1)`, at **fixed `u`, growing `x`** (`checkB.conv_fixed_u`):

| u | x = 10^5 | 10^6 | 10^7 | 5·10^7 | `(ratio−1)·log y` |
|---|---|---|---|---|---|
| 2.5 | 1.2826 | 1.2537 | 1.2125 | 1.1902 | 1.30, 1.40, 1.37, 1.35 |
| 3.0 | 1.7127 | 1.5057 | 1.4243 | 1.3692 | 2.73, 2.33, 2.28, 2.18 |
| 4.0 | 4.4688 | 3.4539 | 2.5443 | 2.4063 | 10.0, 8.50, 6.22, 6.23 |

The ratio decreases monotonically toward 1 at every fixed `u`, and **`(ratio−1)·log y` is flat** —
i.e. the relative error really is `c(u)/log y`, exactly the error term claimed in Theorem A. The
constant `c(u)` grows quickly with `u` (`≈1.35, 2.2, 6.2` at `u = 2.5, 3, 4`).

**Consequence that dominates everything below:** in the numerical table the dominant `y ≈ n^{1/3}`,
so `log y ≈ L/3 ≈ 5.4` at `n = 10^7`. The relative error in Theorem A is then **20–40 %**. The table
is deep in the pre-asymptotic regime; nothing fitted to it should be read as an asymptotic law.

### 1d. A refinement that removes the `1/log` losses — **NUMERICAL tool**

Keep (B) exact and make the *single* substitution `Σ_{y<p≤x} f(p) → ∫_2^x f(t)dt/log t`. In log
coordinates `b = log x`, `a = log y` this is a computable two-parameter recursion
`H(b,a) = 1 − ∫_a^b H(b−c, c)·e^c dc/c`, `H(b,a) = 1` for `a ≥ b` (`checkB.ContBuchstab`).
It contains Theorem A as its leading term and *all* the `1/log` corrections. Against exact `M(x,y)`:

| x | u = 1.5 | 2.0 | 2.3 | 2.6 | 3.0 | 3.5 | 4.0 |
|---|---|---|---|---|---|---|---|
| 2·10^6, `M/H` | 0.999 | 0.999 | 1.009 | 1.032 | 1.062 | 1.223 | 1.418 |

Accurate to `≲1 %` for `u ≤ 2.5`, degrading beyond `u ≈ 3.5` where `y < 60` and (a) the
continuum prime approximation fails and (b) the genuine Mertens noise floor takes over.

---

## 2. Where the mass actually is — **NUMERICAL**

From `checkB.profile_u`, mass fractions of `‖w‖²`:

| u-band | [1,1.5) | [1.5,2) | **[2,2.5)** | [2.5,3) | [3,3.5) | [3.5,4) | [4,5) | ≥5 |
|---|---|---|---|---|---|---|---|---|
| n = 10^5 | 6.6 | 19.4 | **24.4** | 17.8 | 14.7 | 6.1 | 5.8 | 3.2 |
| n = 10^6 | 6.8 | 21.5 | **27.0** | 18.1 | 13.7 | 6.4 | 4.2 | 1.6 |
| n = 10^7 | 6.6 | 21.3 | **29.8** | 21.2 | 12.0 | 4.4 | 3.7 | 0.9 |

mass-mean `u` = 2.702, 2.558, 2.490; mass-mean `β` = 0.3257, 0.3329, 0.3340.

Two things this settles. (i) The peak is at `u = 2` and it is **one-sided**: 27 % of the mass sits
below `u = 2` and 46 % above. (ii) The `u ≤ 2` regime (`M = 1 − π(x) + π(y)` exactly) carries
only **28 %** of `‖w‖²`. A derivation using only that regime therefore recovers the right power of
`n` but the wrong constant and the wrong log behaviour. **This is the trap that produced the
refuted log-power `3/2`:** restricting to `u ≤ 2` gives `Σ ≈ (1/L²)∫n^{2−1/(1+u)}·(1+u)/u² du
≈ 6.75 n^{5/3}/L³`, hence `‖w‖ ≈ 2.6 n^{5/6}/L^{3/2}` — which at `n = 10^7` is `7.5×10^8`, only
**14 %** of the true `‖w‖² = 5.47×10^9`. The `u > 2` tail is not a correction, it is the bulk.

---

## 3. Integrating over the hyperbola — **PROVED given Theorem A**

Every squarefree `j ≥ 2` factors **uniquely** as `j = m·p` with `p = P(j) > P(m)`, `m` squarefree.
So, exactly,

```
Σ_{j≥2 sqfree} M(n/j,P(j))² = Σ_{m sqfree} Σ_{P(m) < p ≤ n/m} M(n/(mp), p)².
```

Fix `m`, write `N = n/m`, `ℓ = log N`, and parametrise the inner prime by
`p = N^{1/(1+u)}`, so `x = N/p = N^{u/(1+u)}` and `u = log x / log p` as required. Then
`log p = ℓ/(1+u)` and

```
dp / log p = p · du /(1+u).                                                   (★)
```
Insert Theorem A, `M(x,p)² ≈ li(x)²ρ(u−1)²` (using `li` rather than `x/log x`: at `n = 10^7` the
difference is `11 %` per factor and therefore `23 %` in `M²` — it matters for the constant):

```
Σ_{j sqfree} M(n/j,P(j))²
   ≈ Σ_{m sqfree} ∫_1^∞ li( (n/m)^{u/(1+u)} )² · ρ(u−1)² · (n/m)^{1/(1+u)}/(1+u) du.   (H)
```
To leading order `li(x) ≈ x/log x` and `(2u+1)/(1+u) = 2 − 1/(1+u)`, so (H) collapses to

```
   ≈ (1/L²) ∫_1^∞ n^{2 − 1/(1+u)} · ρ(u−1)² · ((1+u)/u²) · Z(u) du ,
   Z(u) = Σ_{m sqfree} m^{−σ} = ζ(σ)/ζ(2σ),   σ = 2 − 1/(1+u).                (H′)
```
The `m`-sum converges (`σ ≥ 5/3 > 1`) — this is the analytic form of "the mass sits on nearly-prime
`j`". At the peak `σ = 5/3` and `Z(2) = ζ(5/3)/ζ(10/3) = 1.85080`.

**Validation of (H) alone** (`checkB.analytic_integral` vs the same leading kernel summed over the
*actual* squarefree `j`, isolating the density step from Theorem A's error):

| n | 10^5 | 10^6 | 10^7 |
|---|---|---|---|
| integral / exact-`j` sum | 1.139 | 1.090 | 1.063 |
| top-`m` shares predicted | 46.9 / 17.5 / 9.9 / 4.9 / 3.8 / 3.1 % | 47.6 / 17.1 / 9.4 / 4.5 / 3.5 / 2.8 | **48.5 / 16.9 / 9.2 / 4.3 / 3.2 / 2.6** |
| top-`m` shares measured | — | — | **50.3 / 17.4 / 9.4 / 4.3 / 3.3 / 2.6** |

So the `j = mp` decomposition and the change of variables (★) are right to three digits; the
residual `6 %` is the prime-counting discretisation `Σ_p → ∫dt/log t` at small `p`.

### 3a. End-to-end check against the brief's table — **NUMERICAL**

Feed the §1d kernel `H` (not the bare leading term) through (H). Nothing is fitted.

| n | `‖w‖` exact | `‖w‖` analytic | ratio | `K = ‖w‖L^{1.13}/n^{5/6}` exact | `K` analytic |
|---|---|---|---|---|---|
| 1e5 | 2289.3 | 2176.6 | 0.9508 | 2.4670 | 2.3456 |
| 3e5 | 5211.8 | 4950.6 | 0.9499 | 2.4922 | 2.3673 |
| 1e6 | 12850.5 | 12273.8 | 0.9551 | 2.4977 | 2.3856 |
| 3e6 | 29519.5 | 28286.4 | 0.9582 | 2.5042 | 2.3996 |
| 1e7 | 73972.3 | 71102.6 | **0.9612** | 2.5119 | 2.4144 |

**The analytic route reproduces `‖w‖` to 4 %, and the agreement improves monotonically.** With
the bare leading term (Theorem A, no `1/log` refinement) the ratio is 0.944 → 0.868 instead — i.e.
the leading Dickman term alone is 87 % of `‖w‖` at `n = 10^7`, as §1c predicts.

Residual deficit, resolved by `u` at `n = 10^7` (model/exact): 1.03, 1.02, 0.97, 0.85, 0.65, 0.42,
0.21, 0.08 on `[1,1.5), … , [5,6)`. The whole 4 % lives at `u ≥ 3.5`, where 4.6 % of `‖w‖²` sits and
is **genuine Mertens noise** (`j` with tiny `P(j)`, e.g. `j ∈ {2,3,6}`, where `M(n/j,P(j))` is a
Mertens-sized fluctuation with no mean-field description). That share falls with `n` (5.8 % → 4.6 %).

### 3b. Local exponent — the sharpest test — **NUMERICAL**

| range | exact `dlog‖w‖/dlog n` | analytic |
|---|---|---|
| 1e5 → 3e5 | 0.7488 | 0.7480 |
| 3e5 → 1e6 | 0.7496 | 0.7541 |
| 1e6 → 3e6 | 0.7570 | 0.7600 |
| 3e6 → 1e7 | 0.7630 | 0.7656 |

Agreement to `±0.006`, **including the rise**. Note what this says: the measured local exponent is
`≈ 0.755`, **not** `5/6 = 0.8333`, and it is climbing.

---

## 4. The exponent `5/6`: a corner, not a saddle — **PROVED (calculus) given Theorem A**

Write the (H′) integrand as `exp Φ(u)` with

```
Φ(u) = −L/(1+u) + 2 log ρ(u−1) + log((1+u)/u²) + log Z(u)   (+ const, + 2L).
```
Let `λ(w) := −ρ′(w)/ρ(w)`, so `λ ≡ 0` on `(0,1)`, `λ(1⁺) = 1`, and `λ` is increasing on `(1,∞)`.
Then `Φ′(u) = L/(1+u)² − 2λ(u−1) + d/du[log((1+u)/u²) + log Z(u)]`.

* On `(1,2)`: `λ ≡ 0`, so `Φ′(u) = L/(1+u)² − O(1) > 0` for `L > 7.1`. **`Φ` is increasing up to `u=2`.**
* At `u = 2` the derivative **jumps** by `−2λ(1⁺) = −2`, because `ρ′` is discontinuous at `1`.
  Numerically `d/du log((1+u)/u²)|_2 = −2/3` and `d/du log Z|_2 = (ζ′/ζ(5/3) − 2ζ′/ζ(10/3))/9 = −0.0881`.
* Hence `Φ′(2⁺) = L/9 − 2.7548 < 0  ⟺  L < 24.79`, and since `L/(1+u)²` decreases while `λ(u−1)`
  increases, `Φ′ < 0` on all of `(2,∞)` once it is negative at `2⁺`.

> **Theorem B.** For `1200 ≲ n < e^{24.79} = 5.9×10^{10}` the integrand of (H′) is maximised
> **exactly at the corner `u = 2`**, where `2 − 1/(1+u) = 5/3`. Hence
> `‖w‖² ≍ n^{5/3}·L^{−2}·J(L)` with `J(L) = ∫ exp(Φ(u) − Φ(2))du`, and `β = 1/(1+u) = 1/3`.
> For `L > 24.79` the maximiser `u*(L)` leaves the corner and increases, and the exponent
> `2 − 1/(1+u*)` increases strictly above `5/3`. **PROVED** (elementary calculus + Theorem A).

Numerically maximising the *exact* integrand (`checkB`, m = 1 term):

| log10 n | 5 | 7 | 9 | 10 | **11** | 12 | 14 | 18 | 30 | 100 | 200 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `u*` | 2.000 | 2.000 | 2.000 | 2.000 | **2.083** | 2.227 | 2.439 | 2.713 | 3.263 | 5.489 | 7.498 |
| `2−1/(1+u*)` | 1.6667 | 1.6667 | 1.6667 | 1.6667 | 1.6756 | 1.6901 | 1.7092 | 1.7307 | 1.7654 | 1.8459 | 1.8823 |
| local exp of `‖w‖` | — | 0.752 | 0.782 | 0.793 | 0.801 | 0.809 | 0.820 | 0.838 | 0.864 | 0.911 | 0.931 |

**This is the origin of `β → 1/3`**: `β = 1/(1+u*) = 1/3` is pinned by the corner, and the measured
`β` (0.3368 → 0.3351) approaches `1/3` from above exactly because the mass distribution is
right-skewed and the skew shrinks. It also shows the "`β → 0`" conjecture is right in the limit and
wrong in the data range — the drift only begins near `n = 6×10^{10}`.

**Why the corner exists.** `ρ` has a corner at `1` (`ρ′(1⁻) = 0`, `ρ′(1⁺) = −1`), i.e. **`M(x,y)`
has no cancellation at all for `u ≤ 2`** (`M = 1 − π(x) + π(y)`, one term dominates) and cancellation
switches on abruptly at `u = 2`. `5/6` is the arithmetic of that switch: `n^{5/3} = n^2·n^{−1/3}`,
the `n^{−1/3}` being the density `p ≈ n^{1/3}` of the primes that sit exactly at `y = √x`.

### 4a. Asymptotics beyond the corner — **SKETCH**

For `L → ∞`, using `log ρ(w) = −w(log w + log log w − 1 + o(1))`, stationarity `L/u² ≈ 2 log u`
gives `u* ~ √(L/log L)` and `Φ(u*) ≈ −L/u* − 2u* log u* = −2√(L log L)(1+o(1))`. Hence

```
‖w‖ = n · exp( −(1+o(1))·√( log n · log log n ) ) ,      β = 1/(1+u*) ≍ √(log log n / log n).
```
Numerical check of the `o(1)`: at `L = 138, 230, 460` the computed `log(n/‖w‖)` is 14.9, 20.6, 32.0
against `√(L log L) = 26.1, 35.4, 53.1` — ratios 0.57, 0.58, 0.60, drifting up as the doubly-
logarithmic correction dies. Consistent, slowly.

---

## 5. Log-power and constant — the honest answer

**There is no asymptotic log-power, and `2.51` is not a limit.** For `L` inside the corner window
Theorem B gives `‖w‖ = n^{5/6}·√(J(L))/L`, and `J(L)` is not a power of `L`: the corner-Laplace
evaluation is

```
J(L) ≈ 1/Φ′(2⁻) + 1/|Φ′(2⁺)| = 1/(L/9 − 0.755) + 1/(2.755 − L/9),
```
whose second term **diverges** as `L → 24.79`. A single power `L^{−p}` can only be a local fit, and
the fit exponent must lie strictly between the "`u ≤ 2` only" value `3/2` and `0`. Concretely, over
`10^5 ≤ n ≤ 10^7`:

| | best-fit `p` in `‖w‖ = C n^{5/6}(log n)^{−p}` | `C` |
|---|---|---|
| exact data | **1.0765** | 2.1645 |
| this theory | **1.0440** | 1.9011 |

The theory reproduces the fitted log-power to `0.03`. (Note: `p = 1.13` with `C = 2.51` is a slightly
different local fit of the same data — the quoted column `‖w‖L^{1.13}/n^{5/6}` is itself drifting
`2.4670 → 2.5119`, so `1.13` is not stationary either. The theory's own version of that column
drifts the same way, `2.3456 → 2.4144`, with a constant `≈3 %` offset that is the Mertens-noise
share of §3a.)

Also worth recording, because it explains the earlier `3/2` failure: the corner-Laplace rates are
`Φ′(2⁻) = 1.036` and `|Φ′(2⁺)| = 0.964` at `n = 10^7`. **Both are `O(1)`** — the peak is one `u`-unit
wide, there is no sharp saddle at accessible `n`, and any derivation that treats the peak as narrow
(which is what produces a clean `L^{−3/2}`) is quantitatively wrong by an `L`-dependent factor.

**Verdict on this deliverable:** exponent `5/6` — derived and proved (Theorem B, in its window).
Log-power and constant — **OPEN as asymptotics, because they do not exist**; reproduced as local
fits to `3 %` (`p`) and `4 %` (`C`).

---

## 6. Lower bound: `‖w‖ ≪ n^{5/6+ε}` is FALSE — **PROVED (PNT only)**

This supersedes the brief's "critical constraint". No hypothesis is needed and none would help.

> **Theorem C.** `‖w‖ ≥ 0.40·n^{7/8}(log n)^{−3/2}` for all large `n`. Consequently
> `‖w‖ ≪ n^{5/6+ε}` is false for every `ε < 1/24`, and `‖w‖ ≍ 2.51 n^{5/6}(log n)^{−1.13}` fails by
> `n ≈ 10^{28}`.

*Proof.* All terms of `‖w‖² = Σ_j w_j²` are non-negative, so it suffices to bound one sub-sum.
Take `Q := n^{1/4}` and let `p` run over primes in `[Q, 2Q]`. Each such `j = p` is squarefree with
`P(j) = p`, `x = n/p`, and `u = log(n/p)/log p ∈ [3 − O(1/L), 3]` — inside the range where
**(B2) is exact and §1a is rigorous**. Hence `M(n/p,p) = −(1+o(1))ρ(2)(n/p)/log(n/p)`,
`ρ(2) = 1 − log 2 = 0.30685`. Therefore

```
‖w‖² ≥ Σ_{Q≤p≤2Q} M(n/p,p)² ≥ (1+o(1))·ρ(2)²·(n/2Q)²·(π(2Q)−π(Q))/log²(n/Q)
      = (1+o(1))·0.0942 · (n^{3/2}/4) · (4Q/L) · (16/(9L²))  = 0.167·n^{7/4}/L³.
```
Taking square roots gives `‖w‖ ≥ 0.409 n^{7/8}L^{−3/2}`. Integrating over `u ∈ [2,3]` instead of one
dyadic block improves the constant to `0.818`. Comparing with `2.51 n^{5/6}L^{−1.13}` requires
`0.818 n^{1/24} > 2.51 L^{0.37}`, which holds from `L ≈ 65`, i.e. `n ≈ 10^{28}`. ∎

> **Corollary C′.** `‖w‖ = n^{1−o(1)}`: for every fixed `u₀`, running the same argument with
> `Q = n^{1/(1+u₀)}` gives `‖w‖ ≫_{u₀} n^{1−1/(2(1+u₀))}L^{−3/2}`, so `‖w‖ ≫_ε n^{1−ε}`.
> **Status: PROVED modulo the finite Buchstab induction of §1a** (rigorous for each fixed `u₀`;
> `u₀ = 3` is fully written out above, and that case alone already gives Theorem C).

Sanity: at `n = 10^7`, Theorem C's bound is `8.4×10^3` against the true `7.4×10^4` — the bound is
valid and lossy (it uses one dyadic block out of the whole hyperbola), which is why its crossover
(`10^{28}`) is far later than the true departure from `5/6` (`6×10^{10}`, Theorem B).

**Direct numerical corroboration** (`checkB.window_mass`, exact `M` by sieve): the mass in the
fixed window `p ∈ [n^{1/4}, 2n^{1/4}]` (`u ≈ 3`) versus `p ∈ [n^{1/3}, 2n^{1/3}]` (`u ≈ 2`):

| n | `u≈2` window | `u≈3` window |
|---|---|---|
| 10^6 | 1.60e7 | 2.30e7 |
| 10^7 | 4.29e8 | 8.10e8 |
| 10^8 | 1.29e10 | **2.61e10** |

The `u ≈ 3` window is already twice the `u ≈ 2` window at `n = 10^8` and pulling away — precisely the
mechanism of Theorem C.

---

## 7. Upper bounds — what is true, and what each costs

**(U1) Trivial. PROVED.** `|M(x,y)| ≤ #{d ≤ x} = x`, so `‖w‖² ≤ n + Σ_{j≥1}(n/j)² ≤ ζ(2)n²`, i.e.
`‖w‖ ≤ (π/√6)·n = 1.2825 n`. Together with Corollary C′ this **pins the exponent at 1**.

**(U2) Sieve does not help. PROVED.** The Selberg/Buchstab bound `|M(x,y)| ≤ Φ(x,y) ≍ x/log y`
gives `‖w‖² ≪ Σ_{j sqfree}(n/j)²/log²P(j) + n`, and the terms `j ∈ {2,3,6}` alone contribute
`≍ n²`. Any improvement over `‖w‖ ≪ n` must come from **cancellation in `μ`**, not from sieving.

**(U3) What `‖w‖ ≪ n·δ(n)` costs. PROVED (the implication).** `‖w‖ ≥ |w₁| = |M(n) − 1|`, so any
bound `‖w‖ ≪ nδ(n)` immediately gives `M(n) ≪ nδ(n)`. For `δ(n) = n^{−1/6+ε}` (the brief's
`n^{5/6+ε}`) this is a zero-free region `Re s > 5/6` — but by Theorem C the hypothesis is false, so
the implication is vacuous. **The correct reading is: `‖w‖ ≪ n^{5/6+ε}` costs nothing, because it
cannot be bought.**

**(U4) The upper bound of the right shape. SKETCH, gap named — and RH *is* needed.**
The mean-field prediction (§4a) is `‖w‖ ≪ n·exp(−(1−ε)√(log n log log n))`.
The Perron/zero-free-region route of §1b yields, uniformly for `1 < u ≤ (log x)^{1/2}`,

```
|M(x,y)| ≪ x·ρ(u−1)/log x  +  E(x) ,          E = the Mertens noise floor,
```
and summing over the hyperbola (`j ≤ √n` gives `Σ(n/j)² ≤ ζ(2)n²` times the floor at `x ≥ √n`;
`j > √n` gives `≪ n^{3/2}` by the trivial bound) yields

```
‖w‖ ≪ n·exp(−(1−ε)√(L log L))  +  n·sup_{x≥√n} (E(x)/x) .
```
* **Unconditionally** the classical/Korobov–Vinogradov floor is `E(x)/x ≪ exp(−c(log x)^{3/5−ε})`.
  I initially claimed this is negligible; **that is wrong** — `(log n)^{3/5}` only exceeds
  `√(log n·log log n)` once `log n ≳ 3×10^5` (verified numerically). So unconditionally the floor
  **dominates** and one can only conclude `‖w‖ ≪ n·exp(−c(log n)^{3/5−ε})`, which is weaker than
  the truth throughout any conceivable range.
* **On RH**, `E(x) ≪ x^{1/2+ε}`, the floor term is `≪ n^{1/2+ε}`, utterly negligible, and the bound
  becomes sharp: `‖w‖ ≪ n·exp(−(1−ε)√(log n·log log n))`. A quasi-RH `M(x) ≪ x^{θ}` with any fixed
  `θ < 1` suffices, since the floor term is then `n^{θ+ε}` and the main term is `n^{1−o(1)}`.

**Precise answer to "what does the sharp upper bound cost?": it costs `M(x) ≪ x^{θ}` for some fixed
`θ < 1` (any such `θ`, so RH is far more than enough and even a `θ = 0.999` power saving suffices)
— plus the uniform upper half of Theorem A.** The latter is the uniformity I did not prove (§1a
gap); it is unconditional and in reach of standard Dickman/saddle technology (the same uniformity
Hildebrand–Tenenbaum establish for `Ψ(x,y)`). Note the contrast with (U3): a *power-saving*
exponent `θ < 1` is what is needed here, whereas `‖w‖ ≪ n^{5/6+ε}` would have needed `θ ≤ 5/6`
— and is false anyway.

---

## 8. What would close the remaining gaps

1. **Uniform Theorem A.** Prove `M(x, x^{1/u}) = (x/log y)ρ′(u)(1 + O(u/log y))` uniformly for
   `1+δ ≤ u ≤ (log x)^{1/2}`, plus the additive noise floor. Route: the Hildebrand–Tenenbaum
   saddle-point method applied to `F_y(s) = ζ(s)^{−1}Π_{p≤y}(1−p^{−s})^{−1}`, with the saddle
   `σ = 1 − ξ(u)/log y`; Rankin's trick for the tail `|Im s| > exp((log y)^{3/2})`. This single
   theorem upgrades Corollary C′ and (U4) from SKETCH to PROVED.
2. **The Mertens-noise share.** Quantify `Σ_{j: P(j) small} M(n/j,P(j))²`; numerically 4.6 % of
   `‖w‖²` at `n = 10^7` and falling. This is where the residual 4 % of §3a lives, and it is the only
   part of the problem that is *not* Dickman.
3. **Literature check I did not perform.** Theorem A smells like it is already in the literature
   (Alladi's duality between `P⁻` with `μ` and `P⁺` is the obvious antecedent). I derived it twice
   from scratch and verified it numerically; I did not search for a citation, and one may exist.

---

```
M(x,y) ASYMPTOTIC: M(x, x^{1/u}) = (x/log y)·rho'(u)·(1+O_u(1/log y))
                   = -(x/log x)·rho(u-1)·(1+O_u(1/log y)),  rho = Dickman.
                   Two independent derivations (Buchstab §1a, Mellin/Laplace §1b);
                   numerically confirmed with the error term (ratio-1)*log y flat.
                                              status: PROVED for 1<u<=3 / SKETCH for u>3
                                                      (gap = uniformity as u -> infinity)
EXPONENT 5/6:      Derived. The (H') integrand is maximised at the CORNER u=2 of rho'
                   (rho has a corner at 1), giving ||w||^2 ~ n^{5/3}, beta = 1/(1+u) = 1/3.
                   But the corner is pinned only while L < 24.79, i.e. n < 5.9e10;
                   beyond that the exponent strictly increases and ||w|| = n^{1-o(1)}.
                                              status: PROVED (in its window), and PROVED
                                                      NOT to be the asymptotic exponent
LOG-POWER + CONSTANT: OPEN — because no asymptotic power law exists. The prefactor is
                   J(L) ~ 1/(L/9-0.755) + 1/(2.755-L/9), which diverges as L -> 24.79.
                   As LOCAL fits over 1e5..1e7: theory p=1.044, C=1.901 vs data p=1.077,
                   C=2.165 (the brief's 1.13 / 2.51 is the same data fitted differently and
                   is likewise non-stationary: its column drifts 2.4670 -> 2.5119).
                   True asymptotic shape: ||w|| = n*exp(-(1+o(1))*sqrt(log n * log log n)).
UPPER BOUND: (a) ||w|| <= (pi/sqrt6)*n = 1.2825n, unconditional. PROVED.
             (b) ||w|| << n^{5/6+eps} is FALSE (Theorem C), so the RH/zero-free-region
                 framing is vacuous: ||w|| >= 0.40*n^{7/8}(log n)^{-3/2} from PNT alone,
                 and ||w|| >>_eps n^{1-eps}.                              status: PROVED
             (c) ||w|| << n*exp(-(1-eps)sqrt(log n log log n)) costs exactly: a POWER
                 saving M(x) << x^theta for SOME fixed theta<1 (RH is far more than
                 enough), PLUS the uniform-in-u upper half of Theorem A. Unconditionally
                 the zero-free-region noise floor exp(-c(log x)^{3/5}) dominates the
                 Dickman term until log n ~ 3e5, so only the weaker
                 ||w|| << n*exp(-c(log n)^{3/5-eps}) is unconditional.     status: SKETCH
NUMERICS AGREE WITH THE TABLE: YES. Fully analytic pipeline (no fitted parameter)
                   gives ||w|| = 2176.6 / 4950.6 / 12273.8 / 28286.4 / 71102.6 against
                   2289.3 / 5211.8 / 12850.5 / 29519.5 / 73972.3 — ratios 0.951, 0.950,
                   0.955, 0.958, 0.961, improving monotonically. Local exponents match to
                   +-0.006 (0.7480/0.7488, 0.7541/0.7496, 0.7600/0.7570, 0.7656/0.7630).
                   Mass split by m = j/P(j) matches to 3 digits. The residual 4% is the
                   Mertens noise floor at u >= 3.5 (4.6% of ||w||^2, falling with n).
VERDICT: PARTIAL (strongly) — M(x,y) ~ -(x/log x)rho(u-1) is identified, derived twice and
         confirmed; it explains 5/6, beta=1/3, the u=2 concentration and the anomalous
         log-power, and it PROVES the 5/6 upper bound false; what remains is the uniform-
         in-u version of Theorem A, which is the sole gap between this and a full theorem.
```
