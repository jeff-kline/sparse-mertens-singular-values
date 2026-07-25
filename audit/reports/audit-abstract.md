# Abstract audit — sparse-mertens-singular-values.tex

Scope: `abstract` environment (lines 38–67) checked against the full body (lines 1–668)
of `~/Documents/sparse-mertens-singular-values/paper/sparse-mertens-singular-values.tex`,
plus supporting files in the sibling repo (`proofs/smallest-singular-value.md`, `README.md`,
`audit/reports/`) read for cross-verification only (not edited, no git commands run).

## Findings

### 1. [MUST-FIX, body-level, surfaced via abstract check] `sigma_max` error term is not established by its own proof
- Abstract quote: "$\sigma_{\max}(\Rc_n)=\sqrt n\,(1+O(1/n))$" (line 46).
- Body quote: identical claim in Theorem \ref{thm:max} (line 200).
- Body's *proof* of that theorem (lines 437–443) only derives
  $\sigma_{\max}\le\sqrt n+1+\sqrt{\pi(n)}=\sqrt n(1+O(1/\sqrt{\log n}))$ — a strictly
  weaker bound. $O(1/\sqrt{\log n})\ne O(1/n)$; the stated theorem is stronger than what
  the given Schur-test argument proves.
- Corroboration: the project's own working note `proofs/smallest-singular-value.md`
  (lines 189–191) flags exactly this gap: "the excess halves at each doubling ... **far
  tighter than the proof gives**." The numerics (also reproduced in the paper at
  lines 528–529) do support $O(1/n)$, but no proof of that exponent is given anywhere
  in the paper — only the looser Schur bound.
- Consequence for the abstract: the abstract faithfully reproduces Theorem \ref{thm:max}
  as stated, so there is no abstract-vs-theorem-statement mismatch by the letter of the
  check. But the theorem statement itself outruns its own proof, and the abstract
  inherits that overclaim verbatim. This is exactly the kind of "stronger than the body
  actually establishes" defect the abstract check is meant to catch, one level removed.
  **Flagging for whoever is auditing Theorem \ref{thm:max}'s proof — this is not something
  I can fix from the abstract side without either weakening the theorem to
  $O(1/\sqrt{\log n})$ or supplying a tighter proof.**

### 2. [MUST-FIX] "denser matrices of kline584" — claim with zero support in the body text
- Abstract quote (lines 47–49): "the resulting non-normality gap
  $\sigma_{\max}/|\lambda_{\max}|\asymp\sqrt{\log n}$ is markedly smaller than the
  $\Theta(\sqrt n)$ gap of the denser matrices of \cite{kline584}."
- I grepped the entire body for "denser", "Theta", "non-normality" (only hits are the
  abstract itself and the two occurrences inside Theorem \ref{thm:max}/its proof that
  concern $\sigma_{\max}/|\lambda_{\max}|$ for *this* matrix, not kline584's other
  matrices). **This comparative claim about kline584's "denser matrices" appears
  nowhere in the body.** No section discusses it, no theorem number is cited, and
  \cite{kline584} is used bare (no `[Thm. X]` locator) at this one spot even though the
  paper is otherwise careful to give locators for every other kline584 citation
  (`[§1]`, `[Thm. 1]`).
- I checked the sibling repo for support: `README.md` line 32-34 and
  `proofs/smallest-singular-value.md` lines 200–203 both assert the same $\Theta(\sqrt n)$
  fact, attributing it to "the paper's $\bar H^{(s)}_n$" — so the claim is evidently
  grounded in real analysis the author did of kline584, not fabricated. But a reader of
  the *published paper* has no way to find or verify it: it is asserted only in the
  abstract, with no supporting sentence, theorem locator, or discussion anywhere in
  eight sections of body text.
- Fix: either (a) add one sentence to §1.1 ("The matrix"), where the paper already
  explains why $\sqrt{\pi(n)}$ replaces Redheffer's $\sqrt n$ (lines 127–132) — that is
  the natural place for the comparison — with a locator into kline584, or (b) drop the
  comparative clause from the abstract until the body supports it. I did **not**
  unilaterally delete it from my proposed rewrite (it appears to be a true, sourced
  claim, and I was told not to weaken accurate claims), but this is the single
  weakest-supported clause in the abstract as it stands.

### 3. [should-fix] Notation inconsistency: eigenvalues named one way, referenced another
- Abstract first introduces the dominant eigenvalues unnamed ("its two dominant
  eigenvalues were shown to be $1\pm\sqrt{\pi(n)}+O(\log\log n)$") then, two sentences
  later, uses $\lambda_{\max}$ without ever connecting it back ("$\sigma_{\max}/|\lambda_{\max}|$").
  A reader must infer $\lambda_{\max}$ is the larger of the two just-mentioned
  eigenvalues. Body doesn't have this problem because $r_\pm$ (eq:kline1) and
  $\lambda_{\max}(\Rc_n)$ (Theorem \ref{thm:max}, derived at line 445) are introduced far
  apart with intervening explanation. Fixed in my rewrite by stating the eigenvalue fact
  directly in terms of $\lambda_{\max}$ (which is in fact literally what the body derives
  at line 445: "$|\lambda_{\max}(\Rc_n)|=(1+o(1))\sqrt{\pi(n)}$"), so the same symbol is
  used both times.

### 4. [should-fix] Simplification of eq:kline1 elides the middle term, but this is defensible
- Abstract: "$1\pm\sqrt{\pi(n)}+O(\log\log n)$."
- Body eq:kline1 (line 121-123): $r_\pm = 1\pm\sqrt{\pi(n)} + \tfrac12\frac{\pi_2'(n)}{\pi(n)} + O(\log\log^2 n/\sqrt{n/\log n})$.
- Since $\pi_2'(n)/\pi(n)=\Theta(\log\log n)$ (standard: $\pi_2'(n)\sim n\log\log n/\log n$),
  bundling the middle term and the (much smaller) error term into a single
  $O(\log\log n)$ is a **valid, weaker** restatement — not stronger than the body, so not
  an accuracy violation. It does lose the explicit $\tfrac12$ coefficient, but that
  coefficient is cited (kline584's), not this paper's contribution, so eliding it in the
  abstract is a reasonable simplification. Not fixed in the rewrite for its own sake;
  superseded there by point 3's cleaner fix, which sidesteps this simplification issue
  entirely by quoting the $\lambda_{\max}$ consequence instead of the two-term $r_\pm$ formula.

### 5. [should-fix] Self-containedness — $\pi(n)$ never glossed
- $\pi(n)$ (prime-counting function) is used bare in "$1\pm\sqrt{\pi(n)}$" with no gloss.
  Standard to number theorists, but this is nominally a linear-algebra-journal paper
  (LAA is the author's stated venue precedent) and $\pi$ is a heavily overloaded
  symbol (also used for Dickman's $\rho$'s domain variable, and easily confused with
  the constant $\pi\approx3.14159$, which the same abstract *also* uses implicitly via
  $\sqrt6/\pi$ elsewhere in the body, thankfully not in the abstract). A four-word gloss
  ("$\pi(n)$ the prime-counting function") costs little and removes the ambiguity.
  Added in the rewrite.

### 6. [taste] $P^-(d)$ used without a symbol-level gloss
- Abstract: "$M(x,y)=\sum_{d\le x,\Pm(d)>y}\mu(d)$ ... over integers free of small prime
  factors" — the English clause does the explanatory work informally, so this is not a
  hard self-containedness failure, but it doesn't literally say what $P^-$ denotes.
  Tightened in the rewrite to "no prime factor below $y$," which is a more precise
  paraphrase of the actual condition $P^-(d)>y$ (the original "free of small prime
  factors" is vaguer — "small" is undefined, whereas the threshold is exactly $y$).

### 7. [taste] Font-only distinction between $R_n$ (Redheffer) and $\Rc_n$ (this paper's matrix)
- Both render as "R_n" to the eye except for a calligraphic vs. roman font, and font
  information is exactly what plain-text abstract harvesters (arXiv listing pages,
  Google Scholar, screen readers) tend to lose. This mirrors the body's own convention
  throughout, so it's not an abstract-specific defect, and I have not changed it in the
  rewrite — but it's worth the author's attention if the abstract will be indexed as
  plain text anywhere.

### 8. [completeness — judged defensible omission] Theorem \ref{thm:norm} not stated explicitly
- The original abstract never states $\|w\|=n^{1+o(1)}$ (Theorem \ref{thm:norm}) as such,
  even though the body explicitly calls this "the content" of the main theorem (lines
  190–195: "The content of Theorem \ref{thm:main} is the conversion factor
  $\|\mu_n\|\|w\|=n^{3/2+o(1)}$, that is, Theorem \ref{thm:norm}: without it the
  equivalence is unavailable in either direction at the stated exponent"). Given the
  body's own emphasis, I judge this worth restoring in the abstract (added at ~6 words'
  cost: "of overall size $\|w\|=n^{1+o(1)}$") rather than leaving it as a pure inference
  from the $-3/2$ exponent. This is the one place I added content rather than only
  cutting; see word-count note below.

### 9. [completeness — defensible omission, no fix needed] "Relation to earlier work" (§1.1.3, eq:compare) and the "hierarchy of cheaper bounds" (Remark \ref{rem:hierarchy}) are absent from the abstract
- Both are genuine, interesting content (the "RH is a distance-to-hyperplane" reading of
  kline588, and the elementary $n^{-4/3+o(1)}$/$n^{-1/3+o(1)}$ bounds reachable without
  Alladi) but are expository/contextual rather than new sharp results, and the abstract
  is already carrying the paper's four theorems plus the pre-asymptotic warning. Omitting
  these is a reasonable editorial choice for length; not flagged as a defect.

### 10. Attribution — clear
- "which we cite rather than claim" (line 60) is unambiguous and does exactly the work
  required. "What is cited and what is proved" section (lines 235–244) matches it
  precisely: the analytic engine (Alladi 1982) is explicitly not claimed; the linear
  algebra (Theorem \ref{thm:closed}, \ref{thm:norm}) is explicitly claimed. Cheon–Kim
  attribution ("this answers, negatively for this family, a question of Cheon and Kim")
  is also clean and matches Remark \ref{rem:cheonkim} and the negative-answer framing
  there (line 488–489). No reader of the abstract alone could come away thinking the
  sieve asymptotic is new. **ATTRIBUTION CLEAR: YES.**

### 11. Honesty about limits — no oversell found
- The $o(1)$ in the main formula is stated explicitly, both in Theorem \ref{thm:norm}'s
  restatement and the RH equivalence; nothing in the abstract claims the refined shape
  (Remark \ref{rem:shape}, explicitly flagged "not established" in the body) is known.
  The closing sentence about pre-asymptotic behavior actively undersells rather than
  oversells. No defect.

### 12. Prose (Orwell) and length
- Raw word count (LaTeX tokens, `wc -w`): **233**. Prose-only word count (formulas
  stripped): **186**. By either measure this is long for an abstract, though not
  outrageous for a paper with four theorems plus a numerics/pre-asymptotic remark.
- The two longest sentences (the kline584 background sentence, and the $\sigma_{\max}$/
  non-normality sentence) each pack 3–4 distinct facts into one clause chain with two
  em-dash parentheticals; split in the rewrite for a single-parse read.
- "We also record why the problem is severely pre-asymptotic" — "We also record why" is
  four words of throat-clearing; cut to "Finally, the problem is severely
  pre-asymptotic:" (Orwell: cut every word that does not work).
- No needless passive voice beyond the standard, appropriate mathematical passive used
  to attribute results to cited papers ("was introduced in," "were shown to be") — this
  usage is idiomatic in the genre and not a defect.
- Opening sentence: earns its place — leads with a named, citable classical object
  (Redheffer's matrix) and the RH equivalence, which is exactly the hook a
  linear-algebra readership needs before the paper's own contribution can register.
  Not changed.
- Closing sentence: leaves the reader with the paper's actual epistemic stance (numerics
  here are misleading, treat conjectures below $n=10^8$ with suspicion) rather than a
  triumphant restatement of the main result. This is a deliberate and defensible choice
  given the paper's own emphasis on honesty (§5.1); kept, tightened.

## Proposed rewrite

See `<scratchpad>/abstract_rewrite3.tex`
for the drop-in LaTeX. Reproduced here:

```latex
Redheffer's $(0,1)$ matrix $R_n$ satisfies $\det R_n = M(n) := \sum_{k\le n}\mu(k)$, and the
Riemann hypothesis is equivalent to $M(n) = O(n^{1/2+\varepsilon})$. A far sparser $(0,1)$
matrix $\Rc_n$ with the same determinant --- about $2.61n$ nonzero entries against
Redheffer's $\sim n\log n$ --- was introduced in \cite{kline584}, where its dominant
eigenvalue was shown to satisfy $|\lambda_{\max}(\Rc_n)|=(1+o(1))\sqrt{\pi(n)}$, $\pi(n)$
the prime-counting function. We determine its \emph{singular values} at both ends.

The largest is $\sigma_{\max}(\Rc_n)=\sqrt n\,(1+O(1/n))$, forced by a single dense row. The
resulting non-normality gap $\sigma_{\max}/|\lambda_{\max}|\asymp\sqrt{\log n}$ is markedly
smaller than the $\Theta(\sqrt n)$ gap of the denser matrices in \cite{kline584}. The
smallest satisfies
\[
  \sigma_{\min}(\Rc_n) \;=\; |M(n)|\cdot n^{-3/2+o(1)},
  \qquad\text{whence}\qquad
  \text{RH}\iff \sigma_{\min}(\Rc_n)\ll_\varepsilon n^{-1+\varepsilon},
\]
two-sided and unconditional. The mechanism: writing $\Ac$ for the unit lower-triangular
factor of $\Rc_n$, the entries of $w:=\Ac^{-\mathsf T}(\mathbf 1-e_1)$ are exactly the sums
$M(x,y)=\sum_{d\le x,\,\Pm(d)>y}\mu(d)$ of the M\"obius function over integers with no
prime factor below $y$, of overall size $\|w\|=n^{1+o(1)}$. The analytic input is Alladi's
asymptotic $M(x,x^{1/\alpha})\sim x\rho'(\alpha)/\log y$ with $\rho$ Dickman's function
\cite{alladiJNT}, which we cite rather than claim.

Along the way we show $\|\Ac^{-1}\|\asymp\sqrt n$ via a Neumann series that terminates
after $\sim\log n/\log\log n$ terms, hence $\sigma_{\min}(\Ac)\asymp n^{-1/2}$; this
answers, negatively for this family, a question of Cheon and Kim \cite{cheonkim}. Finally,
the problem is severely pre-asymptotic: computation to $n=10^7$ suggests several
conjectures about $\|w\|$ that are false, for an identified reason, so the $o(1)$ above
cannot yet be pinned down numerically.
```

Word count of rewrite: raw 239 / prose-only 188 — essentially unchanged from the
original (233 / 186). **I did not achieve a large cut**, and I want to be explicit about
why: I spent the length budget on fixing point 3 (notation), point 5 (self-containedness),
and point 8 (completeness) rather than on pure compression, while also cutting real
filler (point 12). Those three fixes cost roughly the same number of words the filler-cut
saved. If the priority is strictly "make it shorter" over "make it more complete/precise,"
point 8's addition ($\|w\|=n^{1+o(1)}$, ~6 words) is the first thing I'd cut — the
$n^{-3/2+o(1)}$ exponent in the main display already carries the same information for a
reader who follows the mechanism sentence, just less explicitly.

I did **not** touch: the $\Theta(\sqrt n)$/kline584 clause (point 2 — accurate but
unsupported in-body; a body fix, not an abstract fix), or the $\sigma_{\max}=O(1/n)$ claim
(point 1 — inherited from Theorem \ref{thm:max} verbatim; a body/proof fix, not an
abstract fix). Both are flagged above for escalation rather than silently patched, per
the instruction not to invent or strengthen results.

```
ORIGINAL WORD COUNT: 233   PROPOSED: 239
ACCURACY DEFECTS: 2  (sigma_max O(1/n) claim outruns its own proof [body-level, inherited
  by abstract verbatim]; "denser matrices of kline584" Theta(sqrt n) claim has no support
  anywhere in the body text)
COMPLETENESS GAPS: 1  (Theorem \ref{thm:norm}, ||w||=n^{1+o(1)}, stated only implicitly
  in the original abstract despite the body calling it "the content" of the main result —
  restored in the rewrite)
ATTRIBUTION CLEAR: YES
VERDICT: ABSTRACT-NEEDS-REVISION
```

## Addendum (appended after initial submission — coordinator request)

### Correction to Finding 2, folded in as instructed

The coordinator checked the actual source (Kline, LAA 584) and reports: the paper's
non-normality corollary states
$|\lambda_n|/\sigma_{\min}(\bar H_n) = \sqrt{B_1K_1n}\,(1+o(1))$ — a ratio of
**smallest** eigenvalue to **smallest** singular value. The present abstract's clause
(line 48) compares that against $\sigma_{\max}/|\lambda_{\max}|$ for *this* paper's
matrix — **largest** singular value to **largest** eigenvalue. These are not the same
quantity measured on two different matrices; they are two *different ratios*
(opposite ends of the spectrum) being placed on either side of "markedly smaller
than." No algebraic identity forces $\sigma_{\max}/|\lambda_{\max}|$ of one matrix and
$|\lambda_n|/\sigma_{\min}$ of another to be comparable at all — a matrix can be very
non-normal at the top of its spectrum and well-conditioned at the bottom, or vice versa,
with no forced relation between the two ratios. This raises the earlier finding from
"unsupported in the body" (originally graded accuracy-defect / must-fix on the grounds
that it cites no locator and appears nowhere in body text) to a **category error**: even
if a locator were added, the comparison as worded juxtaposes non-comparable quantities.
Recorded at that severity in the table below as row `abstract:L47-49` (outcome
**WRONG**, not merely UNVERIFIABLE). Original Finding 2's prose above is left as written
per instruction not to rewrite existing text; this addendum supersedes its severity
characterization.

### Per-claim findings table

Every clause in the abstract environment (lines 38–67 of the original, pre-rewrite
text) that carries a truth-apt claim, in reading order. "Evidence" cites the specific
body location, proof step, or search that settled the outcome.

| ID | Claim (short) | Outcome | Evidence | Must-fix? |
|---|---|---|---|---|
| abstract:L39-40 | $\det R_n = M(n) := \sum_{k\le n}\mu(k)$ | CONFIRMED | Body lines 71–81 (classical, Redheffer \cite{redheffer}); intro states the identical identity. | No |
| abstract:L40 | RH $\iff M(n)=O(n^{1/2+\varepsilon})$ | CONFIRMED | Body eq:rh, lines 76–79, stated as classical equivalence. | No |
| abstract:L41-43 | $\Rc_n$: same determinant as $R_n$, $\sim2.61n$ nonzeros vs. Redheffer's $\sim n\log n$, introduced in \cite{kline584} | CONFIRMED | Body lines 101–118: "$\det\Rc_n=M(n)$", "$\Rc_n$ has about $2.61n$ nonzero entries," "$R_n$ has $\sum d(i)=n\log n+(2\gamma-1)n+O(n^\theta)$ nonzeros" (abstract's "$\sim n\log n$" is the correct leading term). | No |
| abstract:L43-44 | Two dominant eigenvalues "$1\pm\sqrt{\pi(n)}+O(\log\log n)$" (kline584) | IMPRECISE | Body eq:kline1 (line 121-123) has an extra explicit term $\tfrac12\pi_2'(n)/\pi(n)$ before the error term. Since $\pi_2'(n)/\pi(n)=\Theta(\log\log n)$ (standard), folding that term into "$O(\log\log n)$" is a *valid but coarser* restatement — not stronger than the body, so not an accuracy violation, but it discards the explicit $\tfrac12$ coefficient and the term's identity (which resurfaces later in Open Problem 3, line 588, "$\pi_2'(n)$ already visible in eq:kline1"). | Should-fix (taste-adjacent) |
| abstract:L45 | "We determine its singular values at both ends" (scope claim) | CONFIRMED | Body has exactly two extremal results: Theorem \ref{thm:main} ($\sigma_{\min}$) and Theorem \ref{thm:max} ($\sigma_{\max}$), sections \ref{sec:sigmamin} and \ref{sec:max}. | No |
| abstract:L45-46 | $\sigma_{\max}(\Rc_n)=\sqrt n\,(1+O(1/n))$ | OVERCLAIM | Body Theorem \ref{thm:max} (line 200) states this identically, but its own proof (lines 437–443) only derives $\sigma_{\max}\le\sqrt n+1+\sqrt{\pi(n)}=\sqrt n(1+O(1/\sqrt{\log n}))$, a strictly weaker bound. `proofs/smallest-singular-value.md:189-191` (sibling repo) explicitly flags: "far tighter than the proof gives." Numerics (paper lines 528–529) support $O(1/n)$ but no proof of that exponent is given anywhere. | **Yes** (body/proof-level; escalate to whoever audits Thm 4) |
| abstract:L46 | "forced by a single dense row" | CONFIRMED | Body lines 437–438: $\Rc_n$'s first row (all-ones, from $\Rc_n=\Ac_n+e_1(\mathbf1-e_1)^{\mathsf T}$) has norm $\sqrt n$, giving the matching lower bound $\sigma_{\max}\ge\sqrt n$. | No |
| abstract:L47 | $\sigma_{\max}/|\lambda_{\max}|\asymp\sqrt{\log n}$ | CONFIRMED | Body Theorem \ref{thm:max} (line 201), proof lines 445–446: $|\lambda_{\max}(\Rc_n)|=(1+o(1))\sqrt{\pi(n)}$ and $\sqrt{n/\pi(n)}\asymp\sqrt{\log n}$; numerically verified lines 530–531 (ratio rising toward $\sqrt{\log n}$ values, e.g. measured $2.592$ vs. $\sqrt{\log n}=2.960$). | No |
| abstract:L47-49 | "markedly smaller than the $\Theta(\sqrt n)$ gap of the denser matrices of \cite{kline584}" | **WRONG** (category error) | Grep of full body for "denser"/"Theta"/"non-normality" finds no supporting sentence, locator, or discussion anywhere (confirmed via `grep -n` over the whole `.tex`). Beyond being uncited: per coordinator's source check, kline584's actual corollary gives $|\lambda_n|/\sigma_{\min}(\bar H_n)=\sqrt{B_1K_1n}(1+o(1))$ — smallest eigenvalue over smallest singular value — which is compared here against *this* paper's $\sigma_{\max}/|\lambda_{\max}|$ — largest singular value over largest eigenvalue. Different ratio, opposite end of the spectrum, no algebraic relation forces them to be comparable. | **Yes** — highest severity in this audit |
| abstract:L49-53 (display) | $\sigma_{\min}(\Rc_n)=|M(n)|\cdot n^{-3/2+o(1)}$ | CONFIRMED | Body Theorem \ref{thm:main} (line 183), proof lines 396–399, exact match. | No |
| abstract:L52-53 (display) | RH $\iff \sigma_{\min}(\Rc_n)\ll_\varepsilon n^{-1+\varepsilon}$ | CONFIRMED | Body Theorem \ref{thm:main} (lines 183–187), proof lines 401–407 (both directions shown explicitly). | No |
| abstract:L54 | "two-sided and unconditional" | CONFIRMED | Body line 190, verbatim: "The equivalence is two-sided and unconditional." | No |
| abstract:L55-58 | Entries of $w=\Ac^{-\mathsf T}(\mathbf1-e_1)$ are exactly $M(x,y)=\sum_{d\le x,P^-(d)>y}\mu(d)$ | CONFIRMED | Body Theorem \ref{thm:closed} (lines 156–170), proof (lines 295–311), eq:defw (line 148). | No |
| abstract:L58-60 | Alladi's asymptotic $M(x,x^{1/\alpha})\sim x\rho'(\alpha)/\log y$, $\rho$ Dickman's function | IMPRECISE | Body Theorem \ref{thm:alladi} (lines 262–269, cited not proved here) has additional terms $+y/\log y+O(x\alpha^2/\log^2y)$; dropping to "$\sim$" is a valid asymptotic for fixed $\alpha>1$ (both omitted terms are lower order in that regime) but is stated without the fixed-$\alpha$ qualifier. Same category of simplification as the eq:kline1 row above. | Should-fix (taste-adjacent) |
| abstract:L60 | "which we cite rather than claim" | CONFIRMED | Matches §1.5 "What is cited and what is proved" (lines 235–244) exactly — analytic engine (Alladi) explicitly not claimed; linear algebra (Thms \ref{thm:closed}, \ref{thm:norm}) explicitly claimed. | No |
| abstract:L61-62 | $\|\Ac^{-1}\|\asymp\sqrt n$ via Neumann series terminating after $\sim\log n/\log\log n$ terms | CONFIRMED | Body Theorem \ref{thm:max} (lines 202–203), proof lines 448–456: $\omega_{\max}(n)\sim\log n/\log\log n$, $S^{\omega_{\max}(n)+1}=0$. | No |
| abstract:L63 | $\sigma_{\min}(\Ac)\asymp n^{-1/2}$ | CONFIRMED | Body Theorem \ref{thm:max} (line 203), proof line 457: $\sigma_{\min}(\Ac_n)=1/\|\Ac_n^{-1}\|$ combined with the row above. | No |
| abstract:L63-64 | "answers, negatively for this family, a question of Cheon and Kim" | CONFIRMED | Body line 206–207 and Remark \ref{rem:cheonkim} (lines 482–494), explicit: "answers the question negatively for the present family." | No |
| abstract:L64-66 | Several natural conjectures suggested by computation to $n=10^7$ are false; finite-range mechanism identified | CONFIRMED | Body §\ref{sec:preasymptotic} (lines 538–564): explicit false conjectures (the $\|w\|/n^{3/4}$ and $\|w\|(\log n)^{1.13}/n^{5/6}$ near-power illusions, lines 543–549) and identified mechanism (the "corner" at $\beta=1/3$/$\alpha=2$ from Dickman's $\rho$ having a corner at 1, lines 551–560). | No |
| Thm \ref{thm:norm} (absent from abstract) | $\|w\|=n^{1+o(1)}$, unconditionally | GAP | Body explicitly names this "the content" of the main theorem (lines 190–195: "The content of Theorem \ref{thm:main} is the conversion factor $\|\mu_n\|\|w\|=n^{3/2+o(1)}$, that is, Theorem \ref{thm:norm}: without it the equivalence is unavailable in either direction at the stated exponent") but the original abstract never states it — only implies it via the $-3/2$ exponent. Restored explicitly in the proposed rewrite ("of overall size $\|w\|=n^{1+o(1)}$"). | Should-fix (already fixed in rewrite) |

### Coverage

- **Distinct checkable claims in the abstract's own text: 19** (rows `abstract:L39-40` through `abstract:L64-66` above), covering every truth-apt clause from the first sentence to the closing sentence, in order.
- **Checked: 19/19 (100%).** No clause in the abstract was skipped.
- **Additional item checked beyond the abstract's text: 1** — the absent Theorem \ref{thm:norm} statement (row `Thm \ref{thm:norm} (absent from abstract)`), included because its omission is itself a checkable completeness claim ("does the abstract state everything a reader needs"), not because it's abstract text.
- **Outcome tally:** 14 CONFIRMED, 2 IMPRECISE (should-fix, taste-adjacent — both are valid-but-lossy simplifications of cited asymptotics, not accuracy violations), 1 OVERCLAIM (must-fix, body/proof-level), 1 WRONG (must-fix, category error), 1 GAP (already remedied in the rewrite).
- **Nothing left unreached.** Symbol-level self-containedness checks ($\pi(n)$, $P^-$, font collision between $R_n$/$\Rc_n$, $\lambda_{\max}$-naming consistency) were covered in the prose findings above (points 3, 5, 6, 7) rather than in this claim table, since they are presentation defects, not truth-apt claims — they don't have an "outcome" in the CONFIRMED/WRONG/etc. sense used here.
