# Prior-art / novelty audit — working notes

Status: IN PROGRESS (written incrementally)

## Claim 1 — M(x,y) = sum_{n<=x, P^-(n)>y} mu(n) ~ -(x/log x) rho(u-1)

### KEY EARLY FINDING
The object `M(x,y) := sum_{n<=x, p_1(n)>y} mu(n)` is **not new**. It is the exact object
studied by **K. Alladi, "Asymptotic estimates of sums involving the Moebius function",
J. Number Theory 14 (1982), 86–98**, with a sequel **"... II", Trans. Amer. Math. Soc.
272 (1982), 87–105**. Alladi calls `M(x,y)` the "basic computational tool" for studying
`M_f(x) = sum_{n<=x} mu(n) f(p_1(n))`.

Confirmed via: Y. Alamoudi, "On subradically sifted sums related to Alladi's higher order
duality between prime factors", arXiv:2601.10636 (Jan 2026), §1, which reproduces
verbatim the definition
    M(x,y) = sum_{p_1(n)>y, n<=x} mu(n)
and attributes it to Alladi [3] = JNT 14 (1982) 86–98, with the convention p_1(1)=infty.
Alamoudi also notes (§5) "Buchstab iteration provides great insight. Indeed, this has
been demonstrated in [3] for the case k=1."  -> Alladi 1982 does the Buchstab iteration
for exactly our M(x,y).

### VERDICT: PRIOR ART — FOUND. Claim 1 is Alladi's 1982 theorem, verbatim.

Direct quotation, K. Alladi & A. Goswami, "Parity results concerning the generalized
divisor function involving small prime factors of integers", arXiv:2412.03088v1
(4 Dec 2024), Section 1.1 "Sums of the Möbius function", page 2:

  "Motivated by this strong link, Alladi [1], [2] studied the asymptotic behavior of the
   following two sums:
       M(x,y) = sum_{n<=x, p(n)>y} mu(n),
   where p(n) is the smallest prime factor of n if n > 1, and p(1) = infinity, and
       M*(x,y) = sum_{n<=x, P(n)<y} mu(n) ...
   The functions M(x,y) and M*(x,y) are weighted versions of the well known functions
   Phi(x,y) - the number of uncancelled elements in the sieve of Eratosthenes, and
   Psi(x,y) - the number of integers up to x free of prime factors > y.
   In [1] it is shown that if alpha := log x/log y > 1, is fixed, then
       M(x,y) = x*m(alpha)/log y + O(x/log^2 y),
   where m(alpha) satisfies a difference-differential equation and IS THE DERIVATIVE OF
   THE FAMOUS DICKMAN FUNCTION rho(alpha) that occurs in the asymptotic estimate of
   Psi(x,y). ...
   We also point out that in [1] and [2], uniform asymptotic estimates for long ranges of
   alpha are established for M(x,y) and M*(x,y)."

  [1] = K. Alladi, "Asymptotic estimates of sums involving the Möbius function",
        J. Number Theory 14 (1), 1982, 86–98.
  [2] = K. Alladi, "Asymptotic Estimates of Sums Involving the Möbius Function. II",
        Trans. Amer. Math. Soc. 272 (1), 1982, 87–105.

This is Claim 1 *identically*:
  claim:   M(x,y) = (x/log y) rho'(u) (1 + O_u(1/log y))
  Alladi:  M(x,y) = (x/log y) m(alpha) + O(x/log^2 y),  m = rho'
Same normalization x/log y, same function rho', same relative error O(1/log y), same
fixed-u hypothesis. The second form -(x/log x) rho(u-1) is the trivial rewrite via
u rho'(u) = -rho(u-1).

Moreover Alladi–Goswami explicitly flag the *pairing* the audit asked about: M(x,y) is
the mu-weighted analogue of Phi(x,y) (Buchstab omega), and its answer is rho' (Dickman),
while the LARGEST-prime-factor version M*(x,y) is the mu-weighted analogue of Psi(x,y)
and its answer is the derivative of BUCHSTAB's omega. So the "surprising crossover"
(rough+mu -> Dickman) is precisely the phenomenon Alladi published in 1982.

Corroborating independent sources that the object and method are Alladi's:
- Y. Alamoudi, "On subradically sifted sums related to Alladi's higher order duality
  between prime factors", arXiv:2601.10636 (15 Jan 2026), §1: reproduces
  M(x,y) = sum_{p_1(n)>y, n<=x} mu(n) verbatim, calls it (quoting Alladi) the "basic
  computational tool", and notes in §5: "Buchstab iteration provides great insight.
  Indeed, this has been demonstrated in [3] for the case k = 1" ([3] = Alladi JNT 1982).
  Alamoudi's own new work is the *small-y* regime y <= Y0 exp(p log x/(loglog x)^{1+eps})
  with the (omega(n)-1 choose k-1) weight — a different regime and a different weight.
- K. Alladi & T. Molnar, "The local distribution of the number of small prime factors",
  Ramanujan J. 51 (2020) 117–151 (arXiv:1803.08964), refs [1],[2] the same two papers.
- S. Dhavakodi, "On the parity of the number of small prime factors of integers",
  PhD thesis, Univ. of Florida, 1992 — the k=1 generalized-sieve version.

The exact ranges of uniformity in Alladi [1] I could NOT verify directly (see BLOCKED).

(more below)

### What Claim 1 is NOT
- It is *not* textbook material in Tenenbaum's *Introduction to Analytic and Probabilistic
  Number Theory* or in Hildebrand–Tenenbaum's survey. I downloaded and text-searched the
  Hildebrand–Tenenbaum survey ("Integers without large prime factors", J. Théor. Nombres
  Bordeaux 5 (1993) 411–484, numdam PDF): it cites Alladi (1982a) = the TAMS sequel, and
  Alladi (1982b) = the Turán–Kubilius paper, but does NOT state the M(x,y) asymptotic.
  So: research-paper prior art, 44 years old, by a well-known author, restated by that
  author as recently as Dec 2024 — but not a textbook exercise.
- Halberstam–Richert and Friedlander–Iwaniec were NOT directly checked (no accessible
  full text); Alladi–Goswami cite Halberstam–Richert only for the generic sieve axioms.

---

## Claim 2 — sigma_min(R_n) = |M(n)| n^{-3/2+o(1)}, and RH <=> sigma_min << n^{-1+eps}

### Kline's own three LAA papers (verified via Crossref + Semantic Scholar abstracts)
1. J. Kline, "A sparser matrix representation of the Mertens function",
   LAA **581** (2019) 354–366, doi:10.1016/j.laa.2019.07.021.
2. J. Kline, "On the eigenstructure of sparse matrices related to the prime number
   theorem", LAA **584** (2020) 409–430, doi:10.1016/j.laa.2019.09.022.
   Verified abstract: "Our main result establishes asymptotically tight estimates for the
   two dominant **eigenvalues** of R_n. We also state explicit formulae for the
   eigenvectors of R_n that are associated with the eigenvalues that are different from 1.
   Finally, we state several conjectures about the eigenstructure of a related class of
   matrix."  -> EIGENvalues only. No singular values, no sigma_min, no RH criterion.
3. J. Kline, "Bordered Hermitian matrices and sums of the Möbius function",
   LAA **588** (2020) 224–237, doi:10.1016/j.laa.2019.12.004.
   Verified abstract: "...two parameterized families of bordered Hermitian matrices...
   M_s in C^{(n-1)x(n-1)} that satisfy det M_0 = sum_{i<=n} |mu(i)|,
   det M_1 = (sum_{i<=n} mu(i))^2, and we show det M_s is a quadratic polynomial in s.
   We apply the Cauchy interlacing theorem to show that, for each matrix in one of the
   families, the product of all of the **subdominant eigenvalues** is bounded above by
   **6/pi^2 + O(n^{-1/2})**."
   >>> THIS IS THE CLOSEST PRIOR ART TO CLAIM 2, AND IT IS KLINE'S OWN.
   A *bordered Hermitian* matrix with det = M(n)^2 is precisely the singular-value
   dilation setup; "det = M(n)^2 / (product of subdominant eigenvalues bounded by
   6/pi^2 + O(n^{-1/2}))" is exactly the det-over-product-of-the-others mechanism that
   yields sigma_min ~ |M(n)| * (something)^{-1}. The constant 6/pi^2 is the same one that
   Claim 3 invokes. Anyone comparing the two will ask how Claim 2 differs from LAA 588.
   I could NOT read LAA 588 in full (paywalled) to determine whether the n^{-3/2+o(1)}
   exponent and the RH equivalence are already there or only the one-sided bound.

### Independent prior art for "RH criterion via smallest singular value"
**Gi-Sang Cheon & Hana Kim, "Mertens equimodular matrices of Redheffer type",
Linear Algebra and its Applications 572 (2019) 252–272, doi:10.1016/j.laa.2019.03.009.**
Verified abstract (Semantic Scholar, full text):
  "... An infinite matrix whose nth leading principal minor is equal to M(n) for all n>=1
   is called a Mertens equimodular matrix. We use Riordan matrices to find a large class
   of Mertens equimodular matrices, each element of which is called by us a
   Riordan-Redheffer matrix, briefly an R-R matrix. ... Finally, **we find a sufficient
   condition for the Riemann hypothesis using the smallest singular value of a R-R
   matrix.**"
So the *idea* "bound sigma_min of a matrix whose determinant is M(n) => RH" was published
in LAA in March 2019, six months BEFORE Kline's LAA 584. Different matrix family
(Riordan–Redheffer, not Kline's A + e1(1-e1)^T), and only a SUFFICIENT condition, not an
equivalence, and (as far as the abstract goes) no asymptotic formula for sigma_min.
PAYWALLED — I could not read the exact theorem.

### Everything else on singular values of Redheffer-type matrices
- F. Clément & S. Steinerberger, "On the largest singular vector of the Redheffer matrix",
  LAA (2025), doi:10.1016/j.laa.2025.07.003, arXiv:2502.09489. Read in full.
  They state plainly that **"less is known about the singular values"**, and study only the
  LARGEST singular value/vector. They cite Barrett–Forcade–Pollington [3], Barrett–Jarvis
  [4], Jarvis [16], Kline [17,18,19], Hilberdink [13]. No sigma_min, no condition number,
  no RH criterion via singular values. Their only RH statement is the classical
  det(A_n) = O(n^{1/2+eps}).
- T. Hilberdink, "Singular values of multiplicative Toeplitz matrices",
  Linear and Multilinear Algebra — adjacent (singular values of a multiplicative matrix),
  not the Redheffer/Mertens sigma_min question. Not read.
- arXiv full-text-metadata search (`all:"Redheffer matrix"`, all time, 60 results) returns
  only FIVE papers ever: the Redheffer Matrix Parity Problem (2026, combinatorial, not
  relevant), Fibonacci–Redheffer (2025), Clément–Steinerberger (2025), a unitary analog
  (2019), and Redheffer matrix of a poset (2004). Nothing on sigma_min.
- A. P. de Camargo, "Dirichlet matrices: Determinants, permanents and the Factorisatio
  Numerorum problem", LAA (2021), doi:10.1016/j.laa.2021.07.006 — the ONLY external
  citation of Kline LAA 584 in OpenAlex. Determinants/permanents, not singular values.
- OpenAlex citation counts (checked 2026-07-25): Kline LAA 584 has 3 citations
  (Camargo 2021, Kline's own LAA 588, and one other), LAA 581 has 4, LAA 588 has 1
  (Clément–Steinerberger). The literature directly downstream of Kline is essentially
  empty — this makes independent duplication of Claim 2 very unlikely.
- Vaughan I/II, Barrett–Forcade–Pollington, Barrett–Jarvis, Cardon: all concern
  EIGENvalues (the trivial eigenvalue 1 of huge multiplicity, and the two outliers) and
  the determinant. None was found to treat sigma_min. I did not obtain full texts.

### VERDICT Claim 2: ADJACENT (with one uncomfortable neighbour)
No one has published sigma_min(R_n) = |M(n)| n^{-3/2+o(1)} for Kline's matrix, and no one
has published the *equivalence* RH <=> sigma_min(R_n) << n^{-1+eps}. But:
 (a) the one-directional criterion "small sigma_min of a Mertens-determinant matrix => RH"
     is already in print (Cheon–Kim, LAA 572 (2019)); and
 (b) the det = M(n)^2 / product-of-subdominant-eigenvalues mechanism, with the 6/pi^2
     constant, is already in print in Kline's OWN LAA 588 (2020).
The novel content is therefore the *sharp two-sided asymptotic* and the *equivalence*,
not the idea. Both (a) and (b) must be cited and explicitly distinguished.

---

## Claim 3 — ||mu||^2 = #squarefree <= n ~ 6n/pi^2; w = A^{-T}(1-e1) with w_j = M(n/j, P(j))

- `#{squarefree <= n} = 6n/pi^2 + O(sqrt n)` is Gegenbauer (1885); utterly classical.
  It is ALREADY the constant appearing in Kline LAA 588's bound `6/pi^2 + O(n^{-1/2})`
  on the product of subdominant eigenvalues, and in the same matrix context.
- The entries `M(n/j, P(j))` are Alladi's M(x,y) evaluated with roughness threshold
  P(j) = largest prime factor of j. The underlying combinatorics — every integer factors
  uniquely as (P(j)-smooth part) x (P(j)-rough part), giving the Buchstab/de Bruijn
  recursion `M(x,y) = 1 - sum_{y<p<=x} M(x/p, p)` — is exactly what Alladi [1] iterates,
  and it is standard in de Bruijn (1950, 1966) and in the smooth/rough literature.
- What I did NOT find anywhere: a statement identifying the entries of an
  INVERSE-MATRIX-times-vector with these rough-Möbius sums. Nothing in the Redheffer
  literature (5 arXiv papers total) and nothing in Alladi's line of work computes matrix
  inverses. Searched: "inverse of the Redheffer matrix", "Redheffer matrix inverse Möbius
  smallest prime factor". Only the classical fact that the Redheffer *transpose* inverse
  has Möbius-function entries.
- VERDICT: ADJACENT. Every ingredient is standard (Gegenbauer; Alladi's M(x,y); the
  smooth/rough splitting). The specific identification is a bookkeeping observation about
  Kline's A that I could not find stated. Low novelty weight — do not lead with it.

---

## SOURCES REACHED
- arXiv (API metadata search + full PDFs downloaded and pdftotext'd):
  2412.03088 (Alladi–Goswami, DECISIVE for Claim 1), 2601.10636 (Alamoudi),
  1803.08964 (Alladi–Molnar), 2604.17832, 2410.18259, 2502.09489 (Clément–Steinerberger,
  read in full), 2607.08962.
- Alladi's UF-hosted PDF alladi-johnson-l.pdf.
- Numdam: Hildebrand–Tenenbaum, "Integers without large prime factors", JTNB 5 (1993)
  411–484 — full PDF downloaded and text-searched.
- Crossref API (Kline's three LAA papers, exact volume/page/DOI; Cheon–Kim metadata).
- Semantic Scholar Graph API (verified abstracts for Kline LAA 584, Kline LAA 588,
  Cheon–Kim LAA 572, Camargo LAA 2021).
- OpenAlex API (citation graph for all three Kline papers).
- Unpaywall API (confirmed all four LAA papers are closed access).

## SOURCES BLOCKED / NOT REACHED
- ScienceDirect / Elsevier full texts (HTTP 403 to both WebFetch and curl): Alladi JNT 14
  (1982) 86–98 itself; Kline LAA 581/584/588 full texts; Cheon–Kim LAA 572 full text;
  Camargo LAA 2021. Confirmed non-OA by Unpaywall.
- AMS journals site (403 on WebFetch; the curl'd issue page is a JS shell): Alladi's
  TAMS 272 (1982) 87–105 sequel.
- zbMATH Open (403) and MathSciNet (no subscription) — could not pull reviews.
- Halberstam–Richert *Sieve Methods*, Friedlander–Iwaniec *Opera de Cribro*,
  Tenenbaum *Introduction to Analytic and Probabilistic Number Theory* — books, no
  accessible full text. Not searched directly.
- Semantic Scholar rate-limited (429) on one call; retried successfully.
