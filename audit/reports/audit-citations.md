# Citation audit — `sparse-mertens-singular-values.tex`

Auditor: citations agent. Sources read directly from local PDFs (pdftotext + page renders).
Repo treated as read-only; no git commands run.

---

## A. Alladi, J. Number Theory 14 (1982) 86–98

### A1. Theorem `thm:alladi` = [alladiJNT, Thm. 1] — **VERIFIED (exact)**

Source, p. 87 (page render, not OCR):

> THEOREM 1. *If y ⩾ x, then M(x, y) = 1. If y = x^{1/α}, then*
> M(x,y) = xρ'(α)/log y + y/log y + O( x·α² / log² y )
> *uniformly for 2 ⩽ y < x.*

Paper's Theorem `thm:alladi` reproduces this character for character, including the
`y/log y` term, the error `O(xα²/log²y)`, and the uniformity range `2 ≤ y < x`.
Hypothesis `y ≥ x ⇒ M(x,y)=1` also exact.

### A2. Definition of `M(x,y)` (eq. `eq:defMxy`) — **VERIFIED**

Alladi (1.4): `M(x,y) = Σ_{1≤m≤x, p(m)>y} μ(m)` where `p(n)` is the **least** prime
factor, `p(1)=∞` (p. 86, l. 1 of §1). Paper: `M(x,y) := Σ_{d≤x, P⁻(d)>y} μ(d)` with
`P⁻(1)=∞`. Same object.

### A3. Definition of `ρ` — **VERIFIED**

Alladi (1.5): `ρ(α)=1 for 0<α≤1`; `= 1 − ∫₁^α ρ(t−1)dt/t for α>1`. Paper §Results
states this verbatim. Alladi introduces it via `Ψ(x,x^{1/α}) ~ xρ(α)`.

### A4. Rewrite `αρ'(α) = −ρ(α−1)` and eq. `eq:alladi2` — **VERIFIED (math checks)**

Differentiating (1.5) gives `ρ'(α) = −ρ(α−1)/α`. Independently confirmed by Alladi's
own (2.1), p. 88: `ρ'(α) = −1/α for 1<α≤2`. Substituting into Thm 1 with
`α log y = log x`:
`xρ'(α)/log y = −x ρ(α−1)/(α log y) = −x ρ(α−1)/log x`, and both the `y/log y` and
`O(xα²/log²y)` terms are `O_α(1/log y)` relative to that main term. So
`M(x,x^{1/α}) = −(x/log x)ρ(α−1)(1+O_α(1/log y))` is correct.
`ρ>0` everywhere is standard, so the sign claim ("M(x,y) is negative") holds.
Cross-check: Alladi p. 97 states "ρ'(α) < 0 for all α > 1".

### A5. p. 87 quotation — **VERIFIED (verbatim)**

Source p. 87: "Thus the main terms of Theorem 1 are smaller than the error term when α
is large." Paper (`rem:shape`) quotes: ``the main terms of Theorem 1 are smaller than
the error term when $\alpha$ is large''. Exact.

Accompanying formula, Alladi (1.6), p. 87: "if α > 3, then
`ρ'(α) = −exp{−α log α − α log log α + O(α)}`." Paper reproduces exactly, with the
`α>3` hypothesis. **VERIFIED.**

### A6. Alladi Theorem 2 decay — **VERIFIED**

Source p. 88: "THEOREM 2. Suppose that α ⩾ 2 and y = x^{1/α}. Then
`M(x,y) ≪ x(log log x)² exp{−(α/2) log α} + x/log² x` uniformly for 2 ⩽ y ⩽ √x."
Paper: "His Theorem 2 covers large α but only as an upper bound with decay
`exp{−(α/2)log α}`, half the true exponent." Accurate characterisation
(true exponent from (1.6) is `α log α`). Open Problem 1's phrasing
("improving the decay in [alladiJNT, Thm. 2] from `exp{−(α/2)logα}` to
`exp{−α log α}`") is likewise supported.

### A7. Remark `rem:buchstab` (Buchstab contrast) — **OVERSTATED / MISATTRIBUTED**

Paper, `rem:buchstab`:
> "The unweighted analogue is classical: Φ(x,y)=#{d≤x:P⁻(d)>y} ∼ x ω(α)/log y with
> Buchstab's ω. **Alladi observed** that the μ-weighted version produces Dickman's ρ'
> instead, and that the largest-prime-factor variant reverses the roles
> \cite{alladiJNT,alladiTAMS}."

and §"What is cited and what is proved":
> "Theorem \ref{thm:alladi} below is \cite[Thm.~1]{alladiJNT}, **including the contrast
> with Buchstab's function that we record in Remark \ref{rem:buchstab}**"

Checked the full JNT text (all 13 pages, incl. §5 Applications and the reference list):
- The strings "Buchstab", "ω", and "Φ(x,y)" **do not occur anywhere** in Alladi's paper.
- Alladi's only comparison object is `Ψ(x,y) = #{n≤x : P(n)≤y}` (largest prime factor),
  with `Ψ(x,x^{1/α}) ~ xρ(α)`, introduced immediately before Thm 1 and followed by
  "Similarly we derive THEOREM 1". So the ρ ↔ ρ' juxtaposition *is* in Alladi; the
  **Buchstab-ω / Φ(x,y) statement is not**.
- Alladi's bibliography has six items (Alladi 1977 JNT; de Bruijn ×2; Halberstam–Richert;
  Levin–Fainleib; Prachar). No forward reference to a Part II.

The Φ ∼ xω(α)/log y fact is classical (Buchstab), but it is **not** in `alladiJNT`, and
attaching it to "[alladiJNT, Thm. 1] ... including the contrast with Buchstab's function"
attributes to Alladi something he did not write.

**MUST-FIX:** drop "Alladi observed" from the Buchstab half of `rem:buchstab` and cite
Buchstab/Tenenbaum for `Φ(x,y) ∼ xω(α)/log y`; delete "including the contrast with
Buchstab's function" from §"What is cited and what is proved".

### A8. Content attributed to `alladiTAMS` — **UNVERIFIABLE**

No local PDF; I cannot read TAMS 272 (1982) 87–105. Two places lean on it:
1. `rem:buchstab`: "...and that the largest-prime-factor variant reverses the roles
   \cite{alladiJNT,alladiTAMS}." This is a substantive mathematical claim about the
   sequel's content. It is **not** supported by `alladiJNT` (see A7), so the whole
   weight falls on an unreadable source.
2. §"What is cited and what is proved": "\cite{alladiTAMS} is its companion." — a bare
   bibliographic statement, harmless.

**MUST-FIX:** either verify (2) against the TAMS paper or reduce the `rem:buchstab`
sentence to something `alladiJNT` supports on its own.

---

## B. Kline, LAA 584 (2020) 409–430

### B1. Matrix definition, eq. `eq:defA` — **VERIFIED**

Kline 584, p. 410:
> `Â(i,j) := 1 if i = j`; `f(i/j) if i is squarefree and i/j is the largest prime divisor of i`;
> `0 otherwise`. … "Finally, set `Ā := A + δ(1−δ)^t`" (and `Â` likewise), and
> "`R := Â(1)`" with `det R_n = Σ_{i≤n} μ(i)`.

Paper's eq. (2) is the same matrix with `f ≡ 1`: `A(i,j)=1` on the diagonal, `=1` when
`i` squarefree and `i/j = P(i)`, and `R_n := A_n + e_1(1−e_1)^T` (all-ones first row).
**Identical.** `det R_n = M(n)` correctly attributed.

Bibliographic nuance: Kline 584 itself credits the *matrix* to its predecessor
[J. Kline, *A sparser matrix representation of the Mertens function*, LAA **581** (2019)
354–366] — "Recently (see [9]), it was shown that the matrix `R := Â(1)` also satisfies
`det R_n = Σ μ(i)`". The paper's `\cite[\S1]{kline584}` for "The following much sparser
(0,1) matrix … was introduced in" is therefore one step removed from the origin. Not a
misattribution (the matrix does appear in §1 of LAA 584), but LAA 581 is the true
introduction and is absent from the bibliography. **Suggest adding LAA 581.**

### B2. Eigenvalue expansion, eq. `eq:kline1` = [kline584, Thm. 1] — **VERIFIED (exact)**

Source, p. 411 (page render):

> **Theorem 1.** *Denote by r₊ and r₋ the two dominant eigenvalues of `R_n`. Then r₊, r₋
> are real-valued and*
> `r_± = 1 ± √(π(n)) + (1/2)·π₂'(n)/π(n) + O( log log² n / √(n/log n) )`.

Paper's eq. (3) reproduces this exactly, including the error term
`O(log log² n / √(n/log n))`. **VERIFIED.**

### B3. Definition of `π_k'` — **VERIFIED**

Kline 584, p. 411: "let `π_k'(n)` denote the number of squarefree integers no larger than
`n` with exactly `k` prime factors. Note that `π(n) = π₁'(n)`." Paper: "`π_k'(n)` counts
squarefree integers below `n` with exactly `k` prime factors." Same. (Kline 584 also
carefully distinguishes `π_k(n)` — Ω-counting, not squarefree — from `π_k'(n)`; the paper
only ever uses the primed version, correctly.)

### B4. ~2.61n nonzeros — **VERIFIED**

Kline 584, Lemma 2 item 1 (p. 412): "`R_n` has `(2 + 6/π²)n + o(n)` non-vanishing
entries." `2 + 6/π² = 2.6079…`. Paper's "about `2.61n`" and its decomposition
(diagonal + all-ones row + one per squarefree `i`, the last `6n/π² + O(√n)`) is right.

### B5. Barrett–Jarvis `√n`, `\cite[Thm.~1]{barrettjarvis}` — **VERIFIED (indirect)**

No local PDF of Barrett–Jarvis, but Kline 584 p. 411 quotes it explicitly:
> **Theorem** ([2], Theorem 1). *Denote by s₊ and s₋ the two dominant eigenvalues of `R_n`.
> Then* `s_± = ±√n + (1/2)log n + γ − 1/2 + O(log²n/√n)`.

So Theorem 1 of `barrettjarvis` is indeed the `±√n` dominant-eigenvalue result the paper
cites it for.

### B6. Abstract's "`1±√(π(n))+O(log log n)`" — **VERIFIED (correct weakening)**

Kline 584 p. 411 gives the looser form itself: `r_± = ±√(π(n)) + (1/2)log log n + O(1)`.
Since `π₂'(n)/π(n) = log log n + O(1)` by (8) and (6), the abstract's `O(log log n)` is a
faithful weakening of Theorem 1.

---

## C. Kline, LAA 588 (2020) 224–237

### C1. Theorem 1 — **VERIFIED (exact)**

Source, p. 225 (page render):
> **Theorem 1.** *Let `L ∈ R^{n×n}` be a lower-triangular matrix with `L(i,i)=1` for
> `1 ≤ i ≤ n`, and define `M ∈ R^{(n−1)×n}` as `M(i,j) := L(i+1,j)` … Let `l` be the first
> column of `L^{-1}`. Then* `det MM^t = ‖l‖₂²`.

Paper's Theorem `thm:588`: "Let `L` be unit lower triangular, let `B` be `L` with its
first row deleted, and let `l` be the first column of `L^{-1}`. Then `det BB^T = ‖l‖₂²`."
Same statement (the paper uses `B`, which is Kline 588's own symbol in Theorem 3).

### C2. Theorem 3 — **VERIFIED (exact)**

Source, p. 226:
> **Theorem 3.** *Let `A ∈ R^{n×n}` satisfy (2). Define `B ∈ R^{(n−1)×n}` as
> `B(i,j) := A(i+1,j)` … Then* `det BB^t = Σ_{i≤n}|μ(i)|`. *Additionally,*
> `√(det BB^t) = √(6n)/π + O(1)`.

Paper (§Relation to earlier work): "`√(det BB^T) = √(6n)/π + O(1)`". Exact.

### C3. `l = μ_n` and `‖μ_n‖² = 6n/π² + O(√n)` — **VERIFIED (minor locus nit)**

Kline 588 proof of Thm 3, p. 227: "Denote by `μ_n := (μ(1),…,μ(n))`. Let `L` be the
lower-triangular portion of `A`. Then `L(i,i)=1` for all `i` and `μ_n` is the first column
of `L^{-1}`." and "The asymptotic estimate `Σ_{i≤n}|μ(i)| = 6n/π² + O(n^{1/2})` (see [4],
Section 334)". Kline 588 also states (p. 226) that the sparse `R` satisfies (2), so
`L = A_n` here.

Nit: the `6n/π² + O(√n)` asymptotic sits in the *proof* of Theorem 3 and is itself
Hardy–Wright §334, not a Kline result; `\cite[Thms.~1 and 3]{kline588}` slightly
over-credits. Harmless — the equivalent `√(det BB^T)=√(6n)/π+O(1)` *is* Theorem 3.

### C4. The parallelotope quotation — **VERIFIED (near-verbatim; one silent elision)**

Source, p. 227:
> "Informally, the Riemann hypothesis is an assertion that the constant `1^t ∈ R^n` is,
> for all `n`, almost in the span of the rows of `B`."

Paper's block quote:
> "*the Riemann hypothesis is an assertion that the constant `1^T` is, for all `n`, almost
> in the span of the rows of `B`.*"

Word-for-word except that "`∈ R^n`" is dropped without ellipsis. Cosmetic; meaning
unchanged. Suggest `\mathbf 1^{\mathsf T}\in\mathbb R^n` or an ellipsis.

---

## D. Cheon–Kim, LAA 572 (2019) 252–272

### D1. Theorem 4.2 — **VERIFIED**

Source, p. 269:
> **Theorem 4.2.** *If there exists a Mertens equimodular matrix `L + uv^T` such that the
> smallest singular value `σ_n` of `L_n` satisfies* `1 + √(n−1)/σ_n = O(n^{1/2+ε})` *for
> all positive ε, then the Riemann hypothesis is true.*

- It **is** about the **unmodified** triangular factor `L_n` (`L` is a Riordan / lower
  triangular matrix; `L + uv^T` is the modified one). Paper's "their criterion concerns
  the *unmodified* factor" — **correct**.
- It **is** one-directional ("then the Riemann hypothesis is true", no converse). Paper's
  "is one-directional", and the intro's "a *sufficient condition* awaiting verification"
  — **correct**.
- No asymptotic for `σ_n` is supplied anywhere in §4; Theorem 4.4 only reduces the matrix
  size. Paper's "in neither is the relevant singular value determined" — **correct**.

### D2. The derivation `|M(n)| ≤ 1 + √(n−1)/σ_min(L_n)` — **VERIFIED**

Source, p. 268: singular values of `uv^T` are `√(n−1), 0, …, 0`; `det(L_n)=σ₁⋯σ_n=1`;
hence `|det(L_n+uv^T)| ≤ (σ₁)(σ₂)⋯(σ_n+√(n−1)) = 1 + √(n−1)/σ_n`. Combined with
"Mertens equimodular" (`|det A_k| = |M(k)|`, p. 253) this gives exactly the paper's
`|M(n)| ≤ 1 + √(n−1)/σ_min(L_n)`.

### D3. "ask which matrices satisfy it" — **VERIFIED (directly supported)**

Source, p. 269, immediately after Corollary 4.3:
> "Consider all possible Mertens equimodular matrices of the form `L_n + uv^T`. We can then
> ask the question: **For which of these matrices does the smallest singular value of `L_n`
> satisfy (15)?** A bigger singular value `σ_n` will give a better bound for `M(n)`."

The paper's characterisation is exact, and calling it "a question of Cheon and Kim" is
warranted.

### D4. Li–Mathias attribution — **MISQUOTED (wrong paper cited)**  ⚠ MUST-FIX

Paper, `rem:cheonkim`: "the determinantal inequality of Li and Mathias \cite{limathias}",
with bibliography entry

> C.-K. Li, R. Mathias, *The Lidskii–Mirsky–Wielandt theorem — additive and multiplicative
> versions*, Numer. Math. **81** (1999) 377–413.

The inequality actually used is Cheon–Kim's Theorem 4.1, which they attribute to their
reference **[17]**:

> [17] C.-K. Li, R. Mathias, *The determinant of the sum of two matrices*, Bull. Aust.
> Math. Soc. **52** (1995) 425–429.

I fetched the 1995 BAMS paper. Its abstract: "Let `A` and `B` be `n × n` matrices over the
real or complex field. **Lower and upper bounds for `|det(A + B)|` are given in terms of
the singular values of `A` and `B`.**" Its Theorem 1 is exactly the two-sided bound
`Π(a_j + b_{n−j+1}) ≥ |det(A+B)| ≥ Π(a_j − b_{n−j+1})` (with the `0` case when
`[a_n,a_1] ∩ [b_n,b_1] = ∅`) that Cheon–Kim reproduce verbatim as their Theorem 4.1.

The 1999 *Numer. Math.* paper is a different result — additive/multiplicative
Lidskii–Mirsky–Wielandt perturbation bounds and matching distances for eigenvalues and
singular values. It contains no determinant-of-a-sum inequality.

**MUST-FIX:** replace `\bibitem{limathias}` with
`C.-K. Li, R. Mathias, The determinant of the sum of two matrices, Bull. Austral. Math.
Soc. 52 (1995) 425–429.`

### D5. "Much less is known about singular values; Clément and Steinerberger say so explicitly, and treat only the largest" — **VERIFIED**

Clément–Steinerberger, introduction (arXiv:2502.09489): "Less is known about the singular
values, we refer to Cheon-Kim [9] and Hilberdink [12, 13]." Abstract confirms they study
only the largest singular value/vector. Both halves of the paper's sentence check out.

*Note (not a citation defect):* Cheon–Kim make the same observation independently (p. 267:
"Unlike in the case of the eigenvalues of the Redheffer matrix, there were not so many
results on the singular values of a matrix related to the Mertens function"), and
Clément–Steinerberger's other pointer, **Hilberdink** — *Singular values of multiplicative
Toeplitz matrices*, Linear Multilinear Algebra **65** (2017) 813–829, and *Multiplicative
Toeplitz matrices and the Riemann zeta function*, in *Four Faces of Number Theory*, EMS
2015, 77–122 — is **not cited** by the paper. Hilberdink studies the asymptotics of the
singular values of exactly the matrices the paper calls `A(f)_n`. This is a **prior-art
gap**, not a misattribution. (Both Hilberdink PDFs sit in the same local download folder,
so they were evidently seen.)

---

## E. Bordellès–Cloitre, JIPAM 10 (2009), art. 62

### E1. `det Γ_n = n! Σ_{k≤n} μ(k)/k` — **VERIFIED**

Source, Theorem 2.1 (p. 7): "Let `n ⩾ 2` be an integer and `Γ_n` defined as above. Then we
have `det Γ_n = n! Σ_{k=1}^n μ(k)/k`."

### E2. `U_n` is the upper-triangular `LU` factor — **VERIFIED**

Source §2.1 and Lemma 2.2: `Γ_n = L_n U_n` with `U_n = (u_ij)` upper triangular (`= γ_ij`
except two entries) and `L_n` lower triangular. Paper: "`U_n` is the upper triangular
factor of `Γ_n`". Correct.

### E3. Corollary 2.7 and both thresholds — **VERIFIED (exact)**

Source, p. 15:
> **Corollary 2.7.** *For all integers `i ⩾ 1` and `n ⩾ 2` we have*
> `|Σ_{k=i}^n μ_i(k)/k| ⩽ 1/(n σ_n)`, *where `σ_n` is the smallest singular value of `U_n`.
> Thus any estimate of the form* `σ_n ≫_ε n^{−1+ε}` *… is sufficient to prove the PNT.
> Similarly, any estimate of the form* `σ_n ≫_ε n^{−1/2−ε}` *… is sufficient to prove the RH.*

Paper reproduces the inequality, the `n^{−1+ε}` PNT threshold and the `n^{−1/2−ε}` RH
threshold exactly.

Minor wording nit: the paper calls `U_n^{-1}=(θ_{ij})` "given explicitly in terms of
**iterated** Möbius functions". Bordellès–Cloitre's Definition 2.4 introduces a *family*
`μ_i` of "Möbius-type" functions indexed by `i` (defined from `μ(m/i)` and `μ(m/(i+1))`) —
they are not iterates. Suggest "a family of Möbius-type functions".

### E4. `σ_n ≥ min|a_ii|/2^{n−1}` and its hypothesis — **VERIFIED (hypothesis loosely paraphrased)**

Source, p. 15:
> "For example (see [2, 4]), it is known that, if `A_n = (a_ij)` is an invertible upper
> triangular matrix such that `|a_ii| ⩾ |a_ij|` for `i < j`, then we have
> `σ_n ⩾ min|a_ii| / 2^{n−1}`"

Paper: "for instance `σ_n ≥ min_i|a_{ii}|/2^{n−1}` under a diagonal dominance hypothesis".
Bound exact. The hypothesis `|a_ii| ⩾ |a_ij|` for `i<j` is *entrywise* dominance within a
row, weaker than textbook diagonal dominance (`|a_ii| ≥ Σ_{j≠i}|a_ij|`); "a diagonal
dominance hypothesis" is loose but not wrong. Optional tightening: "under the row-wise
hypothesis `|a_{ii}|\ge|a_{ij}|` for `i<j`".

Attribution nit: Bordellès–Cloitre credit this bound to their [2] (Higham, *A survey of
condition numbers for triangular matrices*, SIAM Rev. 29 (1987) 575–596) and [4] (Lemeire,
BIT 15 (1975) 58–64), not to themselves. The paper says only that "The authors observe
that …", which is accurate for the *observation*; the bound itself is Higham/Lemeire.

### E5. The quotation "still very far from the PNT" — **VERIFIED (verbatim)**

Source, p. 15: "… but, applied here, such a bound is **still very far from the PNT**."

### E6. Bordellès–Cloitre originate the strategy and predate Cheon–Kim — **VERIFIED**

Cheon–Kim open their §4 (p. 267) with: "Bordellès and Cloitre [5] introduced an integer
matrix whose determinant is a weighted partial sum of the Möbius function. They derived a
sufficient condition for the Riemann hypothesis in terms of the smallest singular value of
the upper triangular matrix in the LU decomposition of their matrix." 2009 < 2019, and the
later authors themselves credit the earlier. The paper's hedged "appears to originate with"
is well supported.

### E7. Redheffer's theorem — **VERIFIED**

Bordellès–Cloitre §1.1: "In 1977, Redheffer [5] introduced the matrix `R_n = (r_ij)` defined
by `r_ij = 1` if `i | j` or `j = 1`; `0` otherwise, and has shown that `det R_n = M(n)`."
Matches the paper's opening sentence, including the `j=1` convention.

---

## F. Hildebrand–Tenenbaum

`\cite{hildtenen}` is invoked once, for "Hildebrand's range for `Ψ(x,y) ∼ xρ(α)`" in Open
Problem 1. No local PDF, but the reference is the standard survey *Integers without large
prime factors*, JTNB **5** (1993) 411–484, which contains Hildebrand's theorem
(`Ψ(x,y)=xρ(u)(1+O(log(u+1)/log y))` uniformly for `y ≥ exp((log log x)^{5/3+ε})`), a range
that comfortably covers `α ≍ √(log x/log log x)`. **VERIFIED** as a survey citation.

---

## G. Uncited borrowings — **NONE FOUND**

I checked each result the paper claims as its own against the full text of all five
readable sources:

| Paper's claim | Present in a source? |
|---|---|
| Thm `thm:closed` (`w_j = M(n/j, P(j))`) | No. Neither Kline 584 nor 588 computes the row-sums of `A^{-1}`; Kline 588's only inverse-related object is the *first column* `l = μ_n` (Thm 1) and an unrelated vector `W` inside the proof of its Thm 4. |
| Thm `thm:norm` (`‖w‖ = n^{1+o(1)}`) | No. Alladi never forms such a sum of squares. |
| Thm `thm:main` (`σ_min = |M(n)|n^{−3/2+o(1)}`) | No. Cheon–Kim and Bordellès–Cloitre give only one-sided sufficient conditions; neither determines a singular value. |
| Prop `prop:sm` (Sherman–Morrison for `R_n^{-1}`) | No. Kline 588 uses Sherman–Morrison at p. 233 but for an entirely different bordered-Hermitian family (`I_n + r^{-1}S^tS − δδ^t`). |
| Thm `thm:max` (`σ_max`, `‖A_n^{-1}‖ ≍ √n` via terminating Neumann series) | No. `grep` for "singular value" in Kline 584 returns nothing; Kline 584 is purely about eigenvalues. |
| Cor `cor:trichotomy` | No. |
| Lemma `lem:identities` | Stated by the paper as "standard … immediate from unique factorisation" — appropriate; Alladi's (1.2)/(1.4) are related but the paper does not claim novelty. |

The paper's §"What is cited and what is proved" is otherwise an honest and unusually
explicit division of labour.

---

## H. Bibliography hygiene (18 entries)

| Key | Status | Evidence |
|---|---|---|
| `alladiJNT` | **VERIFIED** | PDF header: "JOURNAL OF NUMBER THEORY **14**, 86–98 (1982)". |
| `alladiTAMS` | **VERIFIED (bibliographic only)** | Web-confirmed: TAMS **272** (1982) 87–105. *Content* claims unverified — see A8. |
| `bordellescloitre` | **VERIFIED** | PDF: "vol. 10, iss. 3, art. 62, 2009"; "Page 17 of 17" ⇒ 17 pp. |
| `bfp` | **VERIFIED** | Cheon–Kim [2] and Kline 584 [1]: LAA **107** (1988) 151–159. Cheon–Kim spell the title "Mertens' function" (as the paper does); Kline 584 has "Merten's". |
| `barrettjarvis` | **VERIFIED** | Kline 584 [2]: LAA **162** (1992) 673–683. (Cheon–Kim [3] cite the combined issue "162–164"; both forms are used in the literature.) |
| `camargo` | **VERIFIED** | LAA **628** (2021) 115–129, André Pierro de Camargo. |
| `cardon` | **VERIFIED** | Kline 584 [3] / Cheon–Kim [6]: J. Number Theory **130** (2010) 27–39. |
| `cheonkim` | **VERIFIED** | PDF running head: LAA **572** (2019) 252–272. |
| `clementsteinerberger` | **VERIFIED** | LAA **725** (2025) 96–114; authors François Clément, Stefan Steinerberger. |
| `debruijn` | **VERIFIED but UNCITED** | Alladi [3]: "Indag. Math. **13** (1951), 50–60" — the same publication as Nederl. Akad. Wetensch. Proc. Ser. A **54**. **No `\cite{debruijn}` occurs in the body.** |
| `dickman` | **VERIFIED (minor) but UNCITED** | Canonical: Ark. Mat. Astron. Fys. **22A**, no. 10 (1930) 1–14. The paper drops the "A" and the issue number. **No `\cite{dickman}` occurs in the body.** |
| `hildtenen` | **VERIFIED** | JTNB **5** (2) (1993) 411–484. |
| `kline584` | **VERIFIED** | PDF: LAA **584** (2020) 409–430. |
| `kline588` | **VERIFIED** | PDF: LAA **588** (2020) 224–237. |
| `limathias` | **MISQUOTED — wrong paper** | See D4. Should be Bull. Austral. Math. Soc. **52** (1995) 425–429. |
| `redheffer` | **VERIFIED** | Cheon–Kim [21] gives the full form: "Numerische Methoden bei Optimierungsaufgaben, **Band 3**, …, Internat. Ser. Numer. Math. 36, **Birkhäuser**, Basel, 1977, pp. 213–216" — confirming the paper's "Band 3, Birkhäuser". (Kline 584's own "Springer" is the erroneous version; the paper does *not* repeat it.) |
| `vaughanI` | **VERIFIED** | Cheon–Kim [26] / Bordellès–Cloitre [6]: Lecture Notes in Pure and Appl. Math. **147**, **Dekker**, New York, 1993, pp. 283–296. |
| `vaughanII` | **VERIFIED** | Cheon–Kim [27] / Kline 584 [17]: J. Austral. Math. Soc. **60** (1996) 260–273. |

**Hygiene actions:**
1. Fix `limathias` (MUST).
2. `dickman` and `debruijn` are in the bibliography but never `\cite`d — either cite them
   (natural spot: the definition of `ρ` in §1.2, and Alladi's (1.6)) or drop them. With
   `thebibliography` LaTeX issues no warning, so this is easy to miss.
3. Consider adding J. Kline, *A sparser matrix representation of the Mertens function*,
   LAA **581** (2019) 354–366 — the actual origin of `R_n` (see B1).
4. Consider adding Hilberdink (see D5) as prior art on singular values.

---

## I. One item outside the citation axis, flagged for the correctness auditor

Abstract: "the resulting non-normality gap `σ_max/|λ_max| ≍ √(log n)` is markedly smaller
than the **Θ(√n) gap of the denser matrices of \cite{kline584}**."

`grep -i "singular value"` over the full text of Kline 584 returns **zero hits** — that
paper contains no singular-value results at all. So the `Θ(√n)` figure is the present
paper's own unproved assertion, not something `kline584` supplies, and the phrase reads as
if it were sourced. It is also ambiguous which "denser matrices" are meant: for Redheffer's
`R_n` one has `|λ_max| ∼ √n` (Barrett–Jarvis) and `√n ≤ σ_max ≤ ‖R_n‖_F = √(n log n)`, so
the gap there is at most `Θ(√(log n))`, **not** `Θ(√n)`; the `Θ(√n)` figure fits the
*unmodified* triangular `A(1)_n` (all eigenvalues `1`). Recommend naming the matrix
explicitly and either proving or hedging the `Θ(√n)`.

---

## Tally

32 in-text attributions (§§A–F) + 17 further bibliography entries (§H; `limathias` is
counted once, under D4) = 49.

```
CITATIONS CHECKED: 49
VERIFIED: 46  MISQUOTED: 1  OVERSTATED: 1  UNVERIFIABLE: 1  UNCITED-BORROWING: 0
MUST-FIX:
  1. \bibitem{limathias} points at the wrong Li-Mathias paper. The determinantal
     inequality used in Remark rem:cheonkim (= Cheon-Kim Thm 4.1, their ref [17]) is
     C.-K. Li, R. Mathias, "The determinant of the sum of two matrices", Bull. Austral.
     Math. Soc. 52 (1995) 425-429 -- NOT "The Lidskii-Mirsky-Wielandt theorem", Numer.
     Math. 81 (1999) 377-413, which contains no such inequality.
  2. Remark rem:buchstab attributes the Buchstab-omega / Phi(x,y) contrast to Alladi.
     "Buchstab", "omega", and "Phi(x,y)" appear nowhere in Alladi, JNT 14 (1982) 86-98.
     Remove "Alladi observed" from that half and cite Buchstab/Tenenbaum instead.
  3. Section "What is cited and what is proved" claims Thm thm:alladi is [alladiJNT,
     Thm. 1] "including the contrast with Buchstab's function". Delete that clause --
     it asserts content Alladi's Thm 1 does not have.
  4. rem:buchstab's clause "the largest-prime-factor variant reverses the roles
     \cite{alladiJNT,alladiTAMS}" rests entirely on the TAMS sequel, which is not
     available and which alladiJNT does not corroborate. Verify against TAMS 272
     (1982) 87-105 or delete the clause.
SHOULD-FIX (non-blocking):
  5. \bibitem{dickman} and \bibitem{debruijn} are never \cite'd in the body.
  6. Add J. Kline, LAA 581 (2019) 354-366 -- the actual origin of the sparse matrix.
  7. Add Hilberdink (LMA 65 (2017) 813-829) as prior art on singular values of
     arithmetical matrices; Clement-Steinerberger name him as one of only two
     references on the topic.
  8. Abstract's "Theta(sqrt n) gap of the denser matrices of \cite{kline584}" is not
     in kline584 (that paper has no singular-value content) and is false for
     Redheffer's R_n; name the matrix and hedge or prove.
  9. Cosmetic: kline588 quotation silently drops "in R^n"; "iterated Moebius
     functions" should be "a family of Moebius-type functions"; Bordelles-Cloitre's
     hypothesis is |a_ii| >= |a_ij| for i<j, not full diagonal dominance.
VERDICT: NEEDS-CORRECTION
```

---
---

# ADDENDUM (requested by coordinator): per-citation table, coverage record, two added rows

Appended, not rewritten. Nothing above this line was modified.

## J. Per-citation table

Page numbers are the **printed journal page** I read the text on (via Read-tool page
renders or `pdftotext -layout`), except Bordellès–Cloitre, which is paginated "Page k of
17" internally.

### J.1 Alladi, JNT 14 (1982) 86–98 — `alladiJNT`

| ID | claim (short) | outcome | evidence | must-fix? |
|---|---|---|---|---|
| `alladiJNT:Thm1` | `M(x,y)=xρ'(α)/log y + y/log y + O(xα²/log²y)`, unif. `2≤y<x`; `y≥x ⇒ M=1` | VERIFIED | p. 87, THEOREM 1, read as a page render. Reproduced character for character incl. `y/log y`, the `α²` error and the range. | no |
| `alladiJNT:defM` | `M(x,y)=Σ_{d≤x, P⁻(d)>y} μ(d)`, `P⁻(1)=∞` | VERIFIED | p. 87 eq. (1.4) + p. 86 l. 1 ("let `p(n)` denote its least prime factor and put `p(1)=∞`"). | no |
| `alladiJNT:defRho` | `ρ=1` on `(0,1]`; `ρ(α)=1−∫₁^α ρ(t−1)dt/t` | VERIFIED | p. 87 eq. (1.5). | no |
| `alladiJNT:rewrite` | `αρ'(α)=−ρ(α−1)`, hence eq. (7) `M=−(x/log x)ρ(α−1)(1+O_α(1/log y))` | VERIFIED | Differentiating (1.5); independently confirmed by Alladi's own p. 88 eq. (2.1) `ρ'(α)=−1/α` on `1<α≤2`. Error-term bookkeeping recomputed and correct. | no |
| `alladiJNT:p87quote` | "the main terms of Theorem 1 are smaller than the error term when α is large" | VERIFIED (verbatim) | p. 87, sentence beginning "Thus…". Exact. | no |
| `alladiJNT:1.6` | `ρ'(α)=−exp{−α log α − α log log α + O(α)}` for `α>3` | VERIFIED | p. 87 eq. (1.6), incl. the `α>3` hypothesis. | no |
| `alladiJNT:Thm2` | large-`α` upper bound with decay `exp{−(α/2)log α}` | VERIFIED | p. 88, THEOREM 2: `M(x,y) ≪ x(log log x)² exp{−(α/2)log α} + x/log²x`, unif. `2≤y≤√x`. "Half the true exponent" is a fair reading against (1.6). | no |
| `alladiJNT:sign` | `ρ>0`, so `M(x,y)<0` at fixed `α` | VERIFIED | p. 97: "ρ'(α) < 0 for all α > 1". | no |
| `alladiJNT:buchstab` | "Alladi observed" the `Φ(x,y)∼xω(α)/log y` Buchstab contrast (`rem:buchstab` + §"What is cited") | **OVERSTATED** | "Buchstab", "ω", "Φ(x,y)" occur **nowhere** in the 13-page paper (full-text grep). Alladi's only comparison object is `Ψ(x,y)∼xρ(α)`, p. 87. His 6-item bibliography has no Part II forward-reference. | **YES** |

### J.2 Alladi, TAMS 272 (1982) 87–105 — `alladiTAMS`

| ID | claim (short) | outcome | evidence | must-fix? |
|---|---|---|---|---|
| `alladiTAMS:content` | "the largest-prime-factor variant reverses the roles" | **UNVERIFIABLE** | No local PDF; AMS page returned HTTP 403; no abstract obtainable. `alladiJNT` does not corroborate it (see `alladiJNT:buchstab`), so the whole claim rests on an unread source. | **YES** |
| `alladiTAMS:bib` | TAMS **272** (1982) 87–105 | VERIFIED (bibliographic only) | Web-confirmed volume/year/pages. Content not reachable. | no |

### J.3 Kline, LAA 584 (2020) 409–430 — `kline584`

| ID | claim (short) | outcome | evidence | must-fix? |
|---|---|---|---|---|
| `kline584:defA` | paper's eq. (2) is that paper's `R` (script-R) | VERIFIED | p. 410: `Â(i,j) := 1 if i=j; f(i/j) if i squarefree and i/j is the largest prime divisor of i; 0 otherwise`, with `Â := A + δ(1−δ)^t` and `R := Â(1)`. Identical at `f≡1`. | no |
| `kline584:§1-origin` | "The following much sparser (0,1) matrix … **was introduced in** `\cite[\S1]{kline584}`" | **OVERSTATED** | p. 410 of the cited source itself defers priority: "Recently (see **[9]**), it was shown that the matrix `R := Â(1)` also satisfies `det R_n = Σ μ(i)`", where [9] = **Kline, LAA 581 (2019) 354–366** (p. 430). Kline 588 p. 226 agrees: "More recently (see **[8]**) the following much sparser (0,1) matrix was described", [8] = the same LAA 581 (p. 237). Both cited sources point elsewhere for the introduction. | **YES** (see J.8a) |
| `kline584:Thm1` | eq. (3) `r_± = 1 ± √π(n) + ½π₂'(n)/π(n) + O(log log²n/√(n/log n))` | VERIFIED (exact) | p. 411, Theorem 1, page render. Every term incl. the error matches. | no |
| `kline584:piPrime` | `π_k'(n)` = # squarefree `≤n` with exactly `k` prime factors | VERIFIED | p. 411: "let `π_k'(n)` denote the number of squarefree integers no larger than `n` with exactly `k` prime factors. Note that `π(n)=π₁'(n)`." Paper never conflates it with Kline's Ω-counting `π_k(n)` (p. 412). | no |
| `kline584:det` | `det R_n = M(n)` | VERIFIED | p. 410, and Lemma 2 item 3, p. 412. | no |
| `kline584:nnz` | "about `2.61n` nonzero entries" | VERIFIED | p. 412, Lemma 2 item 1: "`R_n` has `(2 + 6/π²)n + o(n)` non-vanishing entries"; `2+6/π² = 2.6079…`. | no |
| `kline584:absLoose` | abstract's `1±√π(n)+O(log log n)` | VERIFIED | p. 411 gives the looser form itself: `r_± = ±√π(n) + ½log log n + O(1)`; consistent with (7)/(8) on p. 412. | no |

### J.4 Kline, LAA 588 (2020) 224–237 — `kline588`

| ID | claim (short) | outcome | evidence | must-fix? |
|---|---|---|---|---|
| `kline588:Thm1` | `det BB^T = ‖l‖₂²` for unit lower-triangular `L`, `l` = first column of `L⁻¹` | VERIFIED (exact) | p. 225, Theorem 1 (page render). Paper substitutes `B` for Kline's `M`, which is Kline's own symbol in Thm 3. | no |
| `kline588:Thm3a` | `det BB^T = Σ_{i≤n}|μ(i)|` | VERIFIED (exact) | p. 226, Theorem 3. | no |
| `kline588:Thm3b` | `√(det BB^T) = √(6n)/π + O(1)` | VERIFIED (exact) | p. 226, Theorem 3, "Additionally". | no |
| `kline588:l=mu` | `l = μ_n` for `L = A_n` | VERIFIED | p. 227 proof: "`μ_n` is the first column of `L⁻¹`", `L` = lower-triangular portion of `A`; p. 226 states the sparse `R` satisfies (2). | no |
| `kline588:normMu` | `‖μ_n‖² = 6n/π² + O(√n)` | VERIFIED (locus nit) | p. 227, inside the **proof** of Thm 3, and there credited to Hardy–Wright §334 — so `\cite[Thms.~1 and 3]` slightly over-credits. Statement itself correct. | no |
| `kline588:quote` | "the Riemann hypothesis is an assertion that the constant `1^T` is, for all `n`, almost in the span of the rows of `B`" | VERIFIED (near-verbatim) | p. 227: identical except the source reads "the constant `1^t ∈ R^n` is"; the paper drops "`∈ R^n`" without ellipsis. Meaning unchanged. | no |

### J.5 Cheon–Kim, LAA 572 (2019) 252–272 — `cheonkim`

| ID | claim (short) | outcome | evidence | must-fix? |
|---|---|---|---|---|
| `cheonkim:Thm4.2` | `1+√(n−1)/σ_min(L_n) = O(n^{1/2+ε}) ⇒ RH` | VERIFIED (exact) | p. 269, Theorem 4.2 + eq. (15). | no |
| `cheonkim:unmodified` | criterion is about the **unmodified** triangular factor `L_n` | VERIFIED | p. 269: `σ_n` is "the smallest singular value of `L_n`", where `L+uv^T` is the modified matrix; `L` is a Riordan (lower-triangular) matrix, `det L_n = 1` (p. 268). | no |
| `cheonkim:oneDirectional` | one-directional, no converse | VERIFIED | p. 269, "then the Riemann hypothesis is true". §4 contains no converse and no asymptotic for `σ_n`; Thm 4.4 only reduces matrix size. | no |
| `cheonkim:derivation` | `|M(n)| ≤ 1 + √(n−1)/σ_min(L_n)` | VERIFIED | p. 268: `uv^T` has singular values `√(n−1),0,…,0`; `det L_n = σ₁⋯σ_n = 1`; chain ending `= 1 + √(n−1)/σ_n`. Combined with the equimodular definition, p. 253. | no |
| `cheonkim:question` | "ask which matrices satisfy it" | VERIFIED (directly supported) | p. 269: "Consider all possible Mertens equimodular matrices of the form `L_n + uv^T`. We can then ask the question: For which of these matrices does the smallest singular value of `L_n` satisfy (15)?" | no |
| `cheonkim:priority` | BC originate the strategy and predate CK | VERIFIED | p. 267, §4 opening credits "Bordellès and Cloitre [5]" with the first such sufficient condition. 2009 < 2019. | no |

### J.6 Li–Mathias — `limathias`

| ID | claim (short) | outcome | evidence | must-fix? |
|---|---|---|---|---|
| `limathias:bib` / `rem:cheonkim` | "the determinantal inequality of Li and Mathias" cited to *Numer. Math.* **81** (1999) 377–413 | **MISQUOTED (wrong paper)** | Cheon–Kim's Thm 4.1 (p. 268) is credited to their **[17]** (p. 272) = *The determinant of the sum of two matrices*, **Bull. Aust. Math. Soc. 52 (1995) 425–429**. I fetched that 1995 paper: abstract reads "Lower and upper bounds for `|det(A+B)|` are given in terms of the singular values of `A` and `B`", and its Theorem 1 (p. 425) is exactly Cheon–Kim's Thm 4.1 incl. the `[a_n,a_1]∩[b_n,b_1]=∅` case. The 1999 Numer. Math. paper is LMW perturbation theory and has no determinant-of-a-sum inequality. | **YES** |

### J.7 Bordellès–Cloitre, JIPAM 10 (2009) art. 62 — `bordellescloitre`

| ID | claim (short) | outcome | evidence | must-fix? |
|---|---|---|---|---|
| `bordellescloitre:Thm2.1` | `det Γ_n = n! Σ_{k≤n} μ(k)/k` | VERIFIED | p. 7 of 17, Theorem 2.1. | no |
| `bordellescloitre:U` | `U_n` = upper-triangular `LU` factor of `Γ_n` | VERIFIED | pp. 7–8, definition of `u_ij` and Lemma 2.2 `Γ_n = L_n U_n`. | no |
| `bordellescloitre:Cor2.7ineq` | `\|Σ_{k=i}^n μ_i(k)/k\| ≤ 1/(nσ_n)` | VERIFIED (exact) | p. 15 of 17, Corollary 2.7. | no |
| `bordellescloitre:thresholds` | `σ_n ≫_ε n^{−1+ε}` ⇒ PNT; `σ_n ≫_ε n^{−1/2−ε}` ⇒ RH | VERIFIED (exact) | p. 15 of 17, same corollary, both displayed. | no |
| `bordellescloitre:2^n` | `σ_n ≥ min\|a_ii\|/2^{n−1}` under a dominance hypothesis | VERIFIED (hypothesis loosely paraphrased) | p. 15 of 17. Source hypothesis is `\|a_ii\| ⩾ \|a_ij\|` for `i<j` (row-wise entrywise), weaker than textbook diagonal dominance. Bound itself exact; BC credit it to Higham [2] / Lemeire [4], not themselves. | no |
| `bordellescloitre:quote` | "still very far from the PNT" | VERIFIED (verbatim) | p. 15 of 17: "…but, applied here, such a bound is still very far from the PNT." | no |
| `bordellescloitre:redheffer` | Redheffer's `R(i,j)=1` iff `j=1` or `i\|j`, `det R_n=M(n)` | VERIFIED | p. 3 of 17, §1.1, incl. the `j=1` convention. | no |
| `bordellescloitre:mu_i` | `U_n^{-1}=(θ_ij)` "in terms of **iterated** Möbius functions" | VERIFIED (wording nit) | pp. 11, 13 of 17: Def. 2.4 gives a *family* `μ_i` indexed by `i`, built from `μ(m/i)`, `μ(m/(i+1))` — "Möbius-type", not iterates. Cor. 2.6 gives `θ_ij`. | no |

### J.8 Cross-checked bibliography entries (no in-text claim beyond the reference itself)

| ID | claim (short) | outcome | evidence | must-fix? |
|---|---|---|---|---|
| `bfp:bib` | LAA **107** (1988) 151–159 | VERIFIED | Cheon–Kim [2] (p. 272) and Kline 584 [1] (p. 430) agree. Title "Mertens' function" matches Cheon–Kim's spelling. | no |
| `barrettjarvis:bib` | LAA **162** (1992) 673–683 | VERIFIED | Kline 584 [2] (p. 430); Cheon–Kim [3] cites the combined issue "162–164". Both forms current. | no |
| `barrettjarvis:Thm1` | the `√n` dominant eigenvalue of Redheffer's matrix | VERIFIED (via verbatim quotation) | Kline 584 p. 411 quotes it in full: "Theorem ([2], Theorem 1) … `s_± = ±√n + ½log n + γ − ½ + O(log²n/√n)`". So Thm 1 is indeed the `±√n` result. | no |
| `cardon:bib` | J. Number Theory **130** (2010) 27–39 | VERIFIED | Kline 584 [3], Kline 588 [3], Cheon–Kim [6] all agree. | no |
| `redheffer:bib` | Band 3, Birkhäuser, 1977, 213–216 | VERIFIED | Cheon–Kim [21] (p. 272) gives the full form: "…Band 3, …Internat. Ser. Numer. Math., Oberwolfach, 36, **Birkhauser, Basel**, 1977, pp. 213–216". (Kline 584/588 say "Springer"; the paper does **not** repeat that error.) | no |
| `vaughanI:bib` | Dekker, 1993, 283–296 | VERIFIED | Cheon–Kim [26] and BC [6] (p. 17 of 17): Lecture Notes in Pure and Appl. Math. **147**, Dekker, New York. | no |
| `vaughanII:bib` | J. Austral. Math. Soc. **60** (1996) 260–273 | VERIFIED | Cheon–Kim [27], Kline 584 [17]. | no |
| `debruijn:bib` | Nederl. Akad. Wetensch. Proc. Ser. A **54** (1951) 50–60 | VERIFIED — **but UNCITED in body** | Alladi [3] (p. 98) gives the twin form "Indag. Math. **13** (1951), 50–60" — same publication. `grep` finds **no `\cite{debruijn}`** anywhere in the `.tex`. | no (hygiene) |
| `dickman:bib` | Ark. Mat. Astr. Fys. **22** (1930) 1–14 | VERIFIED (minor) — **but UNCITED in body** | Canonical form is vol. **22A**, no. 10, 1–14; the paper drops the "A" and issue number. `grep` finds **no `\cite{dickman}`**. | no (hygiene) |
| `camargo:bib` | LAA **628** (2021) 115–129 | VERIFIED | Web: André Pierro de Camargo, ScienceDirect S0024379521002640. | no |
| `clementsteinerberger:bib` | LAA **725** (2025) 96–114; F. Clément, S. Steinerberger | VERIFIED | Web + arXiv:2502.09489 (François Clément, Stefan Steinerberger). | no |
| `clementsteinerberger:claim` | "say so explicitly, and treat only the largest" | VERIFIED (verbatim) | arXiv:2502.09489 introduction: "**Less is known about the singular values, we refer to Cheon-Kim [9] and Hilberdink [12, 13].**" Abstract confirms only the largest singular value/vector is studied. | no |
| `cheonkim:bib` | LAA **572** (2019) 252–272 | VERIFIED | PDF running head. | no |
| `bordellescloitre:bib` | JIPAM **10** (2009) art. 62, 17 pp. | VERIFIED | PDF masthead "vol. 10, iss. 3, art. 62, 2009"; final page "Page 17 of 17". | no |
| `alladiJNT:bib` | J. Number Theory **14** (1982) 86–98 | VERIFIED | PDF header p. 86. | no |
| `kline584:bib` | LAA **584** (2020) 409–430 | VERIFIED | PDF header. | no |
| `kline588:bib` | LAA **588** (2020) 224–237 | VERIFIED | PDF header. | no |
| `hildtenen:bib` | JTNB **5** (1993) 411–484 | VERIFIED | Web: numdam JTNB_1993__5_2_411_0, Hildebrand & Tenenbaum, pp. 411–484. | no |
| `hildtenen:range` | "Hildebrand's range for `Ψ(x,y)∼xρ(α)`" covers `α≍√(log x/log log x)` | VERIFIED (bibliographic + standard; **document not read**) | The cited survey is the standard reference for Hildebrand's theorem (`y ≥ exp((log log x)^{5/3+ε})`), which covers the stated range. I did **not** obtain the PDF — flagged in §K. | no |

### J.8a–b Two added rows (raised in prose above; now citable)

| ID | claim (short) | outcome | evidence | must-fix? |
|---|---|---|---|---|
| `kline581:MISSING` | **(a)** origin of the sparse matrix | **MISSING CITATION** (mechanism of `kline584:§1-origin`) | **Paper currently says:** "The following much sparser (0,1) matrix with the same determinant was introduced in `\cite[\S1]{kline584}`." **Should say:** introduced in **J. Kline, *A sparser matrix representation of the Mertens function*, Linear Algebra Appl. 581 (2019) 354–366**, with LAA 584 §1 cited for the restatement. **Evidence:** LAA 584 p. 410 ("Recently (see [9])…", [9] = LAA 581, p. 430) and LAA 588 p. 226 ("More recently (see [8])…", [8] = LAA 581, p. 237) — both of the author's own later papers defer priority to LAA 581. | **MUST-FIX.** It is a priority claim contradicted by the very source cited to support it, and self-citation makes it more conspicuous, not less. One new `\bibitem` and a four-word edit. |
| `hilberdink:MISSING` | **(b)** prior art on singular values | **COVERAGE GAP** (not a misattribution; no citation exists to check) | **Paper currently says:** "Much less is known about *singular* values; Clément and Steinerberger `\cite{clementsteinerberger}` say so explicitly, and treat only the largest." **Should say:** the same, with Hilberdink added — **T. Hilberdink, *Singular values of multiplicative Toeplitz matrices*, Linear Multilinear Algebra 65 (2017) 813–829**, and *Multiplicative Toeplitz matrices and the Riemann zeta function*, in *Four Faces of Number Theory*, EMS 2015, 77–122. **Evidence:** the sentence the paper leans on names him — "we refer to Cheon-Kim [9] **and Hilberdink [12, 13]**". Hilberdink's 2017 abstract: "We study the asymptotic behaviour of the **singular values** of matrices with entries `a_ij = f(i/j)` if `j\|i` and zero otherwise" — i.e. precisely the `A(f)_n` the paper defines in §2. Both PDFs are in the same local download folder. | **DISCRETIONARY.** No result of the paper is duplicated (Hilberdink treats dense multiplicative Toeplitz matrices with regularly-varying `F`, not the sparse forest factor, and gives `σ_r ∼ μ_r√(F(n))` rather than a smallest-singular-value asymptotic). But quoting a sentence and dropping half of what it points to is a bad look for a paper whose opening move is a priority survey. Two `\bibitem`s. |

## K. Coverage record

**Denominators.** The `.tex` contains **18 `\bibitem` entries**, **16 distinct `\cite` keys**
in the body, across **29 `\cite` commands**.

- **18 / 18** bibliography entries checked. 2 (`dickman`, `debruijn`) are **never `\cite`d**
  in the body — rows in J.8 above.
- **16 / 16** cited keys checked.
- **6 source documents read directly, in full or at the decisive pages:** Alladi JNT 1982;
  Kline LAA 584; Kline LAA 588; Cheon–Kim LAA 572; Bordellès–Cloitre JIPAM 10;
  Li–Mathias BAMS 52 (1995) — the last fetched during the audit precisely because the
  paper cites a different one.
- **1 source read partially, online:** Clément–Steinerberger (arXiv:2502.09489 abstract +
  introduction; verbatim sentence obtained). Sufficient for the claim made.
- **8 entries verified indirectly**, by cross-checking against the reference lists of
  sources I did read, and — for `barrettjarvis:Thm1` — against a verbatim quotation of the
  theorem inside Kline 584 p. 411: `bfp`, `barrettjarvis`, `cardon`, `redheffer`,
  `vaughanI`, `vaughanII`, `debruijn`, plus `alladiJNT`/`kline584`/`kline588` mastheads.
- **3 entries verified by web search only** (bibliographic data, no document obtained):
  `alladiTAMS`, `camargo`, `dickman`.

**Documents I could not reach — explicit list:**

| Source | Why | Consequence |
|---|---|---|
| **Alladi, TAMS 272 (1982) 87–105** | No local copy; ams.org returned HTTP 403; no abstract or review text retrievable by search. | The **only** genuine UNVERIFIABLE finding. The paper asserts mathematical content of this paper (`rem:buchstab`) that `alladiJNT` does not corroborate. Must be verified or deleted. |
| **Hildebrand–Tenenbaum, JTNB 5 (1993) 411–484** | Bibliographic data confirmed (numdam), PDF not retrieved. | Low risk: `hildtenen` is invoked once for a textbook-standard fact that is unambiguously the survey's content. Marked VERIFIED on bibliographic + standard grounds, **not** document-verified. |
| **Barrett–Forcade–Pollington; Cardon; Camargo; Vaughan I & II; Redheffer; de Bruijn; Dickman** | No PDFs sought — these appear only in a single undifferentiated `\cite{bfp,barrettjarvis,vaughanI,vaughanII,cardon,camargo}` ("a long line of work has studied the spectrum of `R_n`") with no specific claim attached. | No attribution risk: a survey-style citation makes no checkable assertion. Bibliographic data verified for all. |
| **Barrett–Jarvis, LAA 162 (1992)** | No PDF, but Theorem 1 is quoted verbatim inside Kline 584 p. 411. | Adequate for the one specific claim (`\cite[Thm.~1]`). |

## L. Revised tally

Splitting `kline584:§1-origin` out of the former single `kline584` row adds one row and moves
it from VERIFIED to OVERSTATED. `hilberdink:MISSING` is a coverage gap with no citation to
adjudicate, so it is **excluded** from the tally and reported separately.

```
CITATIONS CHECKED: 50   (33 in-text attributions + 17 further bibliography entries;
                         limathias counted once; hilberdink:MISSING excluded)
VERIFIED: 46  MISQUOTED: 1  OVERSTATED: 2  UNVERIFIABLE: 1  UNCITED-BORROWING: 0
                                                    + 1 COVERAGE GAP (hilberdink)
DELTA vs. the pre-addendum tally: total 49 -> 50; OVERSTATED 1 -> 2. No outcome
above was revised downward on re-examination; the change is a row split forced by
the coordinator's request for a citable kline581 row.

MUST-FIX:
  1. limathias:bib   -- wrong Li-Mathias paper. Use Bull. Austral. Math. Soc. 52
                        (1995) 425-429.
  2. alladiJNT:buchstab -- remove "Alladi observed" from the Buchstab half of
                        rem:buchstab; cite Buchstab/Tenenbaum.
  3. alladiJNT:buchstab -- delete "including the contrast with Buchstab's function"
                        from the section "What is cited and what is proved".
  4. alladiTAMS:content -- verify against TAMS 272 (1982) 87-105 or delete the
                        "largest-prime-factor variant reverses the roles" clause.
  5. kline584:§1-origin / kline581:MISSING -- the matrix was introduced in Kline,
                        LAA 581 (2019) 354-366; both LAA 584 and LAA 588 say so.
                        Add the bibitem and reword "was introduced in".
DISCRETIONARY:
  6. hilberdink:MISSING -- add Hilberdink (LMA 65 (2017) 813-829; EMS 2015, 77-122).
  7. dickman, debruijn  -- bibitems never cited; cite or drop.
  8. Cosmetic: kline588 quotation drops "in R^n"; "iterated Moebius functions" ->
                        "a family of Moebius-type functions"; Bordelles-Cloitre's
                        hypothesis is |a_ii| >= |a_ij| for i<j.
VERDICT: NEEDS-CORRECTION
```

## M. Note on the abstract's non-normality comparison (coordinator's measurement)

The coordinator's dense SVD/eig computation on the genuine Redheffer matrix
(`R[i,j]=1` iff `j=1` or `i|j`, validated by `det = M(n)`) gives
`σ_max/|λ_max|` = 1.2243, 1.2475, 1.2686, 1.2875 at `n` = 400, 800, 1600, 3200 — against
the paper's own tabulated 1.906, 2.087, 2.262, 2.440 for `R_n`. This is consistent with my
`Θ(√log n)` bound in §I and settles the matter empirically: `Θ(√n)` would be 56.6 at
`n=3200`.

So the abstract's clause is wrong in **three** independent ways, not one:
(i) it sources a singular-value figure to a paper containing **zero** occurrences of the
string "singular" (`grep -c -i singular` on LAA 584 = 0 — I re-ran it);
(ii) the figure `Θ(√n)` is off by orders of magnitude for Redheffer's matrix; and
(iii) the direction is **inverted** — this paper's `R_n` is *more* non-normal than
Redheffer's at every `n` tested, not "markedly smaller".

This is a correctness defect rather than a citation defect, so it stays out of the tally,
but the `\cite{kline584}` inside it makes it partly mine: the clause reads as sourced when
nothing in the cited paper supports it. Recommend deleting the comparison or replacing it
with the measured Redheffer ratio and an explicit statement of which matrix is meant.
