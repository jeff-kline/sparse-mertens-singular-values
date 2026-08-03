# Admission record

**Current state:** CANDIDATE PREPARATION

**Version:** 0.1.0

**Planned tag:** `v0.1.0`

**Standard:** [A Public Standard for This Work](https://jeff-kline.github.io/posts/research-program/index.html), draft 0.4, 2026-08-01

**Admission verdict:** NOT YET ADMITTED

Admission is a project release decision. It is not peer review, a correctness
certificate, or proof of global novelty.

## Principal claim

For the sparse Mertens matrix `R_n` defined in the paper,

```text
|M(n)| n^(-3/2+o(1)) <= sigma_min(R_n)
                      <= |M(n)| n^(-4/3+o(1))
```

unconditionally, and

```text
RH <=> sigma_min(R_n) <<_epsilon n^(-1+epsilon).
```

The exact asymptotic with exponent `-3/2` is proved under the rank-one
dominance condition stated in the paper; RH implies that condition.

## P1 — prior work and credit

| Check | Status | Evidence or residual |
|---|---|---|
| Closest mechanisms and parameter families compared | PASS | `audit/reports/prior-art-audit.md`; includes Alladi, Kline 581/584/588, Bordelles--Cloitre, Cheon--Kim, Hilberdink, and Clement--Steinerberger |
| Obtainable primary sources checked | PASS | Direct texts or publisher records listed in the bounded audit |
| Contribution types distinguished | PASS | README and paper separate prior analytic input, earlier matrix results, present theorems, computation, and exploration |
| Novelty bounded to searched corpus | PASS | No global priority claim; exact residual risks are named |
| Inaccessible sources visible | PASS | Alladi's TAMS companion and other access limits remain listed |

**P1 gate:** PASS.

## A1 — claim and artifact consistency

| Check | Status | Evidence or residual |
|---|---|---|
| Principal claim precise and no broader than proof | PASS | Corrected theorem, README, abstract, introduction, and proof map |
| Parameters, hypotheses, and singular cases visible | PASS | Rank-one dominance condition and `M(n)=0` case are explicit |
| Proof, exact computation, exploration, and literature separated | PASS | README evidence section and paper labels |
| Prior work credited near the claims | PASS | Paper introduction and cited-results section; bounded audit |
| Public prose plain and process-history free | PASS | README, abstract, and introduction rewritten 2026-08-03 |
| Version and status metadata agree | PASS | Candidate version, README status, PDF, citation metadata, verification record, and manifest agree |
| Fresh adversarial closure | PASS | Frozen-source Opus recheck passed at the exact paper hash recorded in `audit/reports/release-proof-closure.md`; this is not peer review |

**A1 gate:** PASS. Any material claim edit reopens this gate.

## R1 — release and stewardship

| Check | Status | Evidence or residual |
|---|---|---|
| Reproduction commands and pinned dependencies | PASS | Fresh environment, exact commands, ranges, and outputs recorded in `VERIFICATION.md` |
| Deterministic document build and visual inspection | PASS | Two byte-identical builds; all 13 pages rendered and visually inspected; exact PDF hash in `VERIFICATION.md` |
| Complete tracked-file manifest | PASS | `MANIFEST.sha256` covers every tracked candidate file except itself and passes hash verification |
| Hygiene: credentials, private paths, placeholders, links | PASS | Fresh tracked-tree and PDF metadata scans passed; local Markdown links pass the release audit |
| Correction, withdrawal, supersession policy | PASS | `CORRECTIONS.md` |
| Machine-readable citation | PASS | Candidate-safe `CITATION.cff`; no DOI or release date asserted |
| Immutable semantic tag | FAIL | Not authorized or created |
| Permanent archive and DOI | FAIL | No archive exists; route must be confirmed before freeze |
| Provider byte identity | FAIL | Requires published provider artifact |
| Living repository points to exact archive | FAIL | Post-publication action |

**R1 gate:** FAIL until the immutable release and archive are published and
verified.

## Execution boundary and owners

| Action | Owner and authority state |
|---|---|
| Local edits and tests | Root release agent, authorized by the release request |
| Review-branch push | Requires explicit author authorization |
| Default-branch update | Requires explicit author authorization |
| Public annotated tag | Requires explicit author authorization for the exact commit and tag |
| GitHub Release | Requires explicit author authorization after the provider-target archive is pinned |
| DOI/archive portal | Author only; the agent will not open or authenticate to the portal |
| Public-site listing | Separate admission authorization after archive verification |

## Archive route

**Proposed route:** Zenodo GitHub integration. Before freezing, the author must
confirm that the GitHub repository is enabled in Zenodo. No separate manual
deposit should be created for the same release. The provider byte-identity
target will be the canonical GitHub API `zipball/v0.1.0` downloaded twice and
pinned before the GitHub Release triggers Zenodo. A separate deterministic
`git archive v0.1.0` will also be recorded but will not be treated as byte
identical to the provider zipball.

## Residual risks

- Admission cannot establish correctness or global novelty.
- Alladi's 1982 TAMS companion was not read in full during the bounded audit.
- The sharper proposed shape of `||w||` and a constant-factor asymptotic for
  `||A_n^(-1)||` remain open and are not part of the principal claim.
- AI systems substantially assisted the work and its audits; process separation
  does not make those audits independent expert review.
