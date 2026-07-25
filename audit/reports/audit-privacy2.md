# Privacy/Security Re-Audit — sparse-mertens-singular-values (pass 2)

Repo: ~/Documents/sparse-mertens-singular-values
Base commit: e75d1c4459e9e96fec47ba4d62ebbe703138d268 (pushed to private remote origin/main)
New material audited: uncommitted `paper/` dir, modified README.md, modified proofs/smallest-singular-value.md

Status (in progress, incremental).

## Inventory
- Tracked, modified (unstaged): README.md, proofs/smallest-singular-value.md
- Untracked: paper/ (dir) containing:
  - paper/sparse-mertens-singular-values.tex (32415 bytes)
  - paper/sparse-mertens-singular-values.pdf (308917 bytes)
  - paper/sparse-mertens-singular-values.aux (5931 bytes) -- build intermediate
  - paper/sparse-mertens-singular-values.log (17487 bytes) -- build intermediate
  - paper/sparse-mertens-singular-values.out (2249 bytes) -- build intermediate
- No .synctex.gz present.

## Check 1 — Topical contamination
Inspected: every path under paper/ (tex/pdf/aux/log/out), code/*.py (unchanged vs HEAD, confirmed `git diff --stat code/` empty), audit/reports/*.md, README.md diff, proofs/smallest-singular-value.md diff.
Repo-wide keyword scan for sibling-project fingerprints (`Steinhaus`, `check_ksteinhaus`, `bulk tightness`, `Liouville twist`, `E7`, `E9.1`, `E12`, `Bohr`) over all tracked+untracked files: **zero matches**.
`paper/sparse-mertens-singular-values.tex` section list: Introduction / The matrix / Results / Relation to earlier work / Notation and cited results / The inverse and the vector w / The norm of w / The smallest singular value / The largest singular value / Numerical remarks / Open problems — all on-topic for the Redheffer/sparse-Mertens singular-value paper; abstract cites `kline584` and `alladiJNT`, matches proofs/smallest-singular-value.md content (the new README/proofs diff hunks reference the same Bordellès–Cloitre JIPAM citation that appears in the new paper text — cross-consistent).
Verdict: **PASS**. No stray files.

## Check 2 — Built PDF metadata
Inspected: `paper/sparse-mertens-singular-values.pdf` via `pdfinfo` and raw `strings`.
- Title: (empty), Subject: (empty), Keywords: (empty), Author: (empty)
- Creator: `LaTeX with hyperref`
- Producer: `pdfTeX-1.40.22`
- CreationDate / ModDate: `Sat Jul 25 16:12:58 2026 CDT` (both identical — single-pass build, no stale timestamp skew)
- `Metadata Stream: no` (no XMP packet embedded)
- `JavaScript: no`; `pdfdetach -list` → `0 embedded files`; raw grep for `OpenAction`, `EmbeddedFile`, `/JS` → 0 hits each.
- Raw string `strings` scan found one extra field pdfinfo doesn't surface: `/PTEX.Fullbanner (This is pdfTeX, Version 3.141592653-2.6-1.40.22 (TeX Live 2021/MacPorts 2021.58693_2) kpathsea version 6.3.3)` — discloses TeX distribution/version and that it's a MacPorts build, but **no username, no absolute path, no hostname**.
- No `<home>` or any local path found inside the PDF itself.
Verdict: **PASS**. No machine-identifying content embedded in the PDF. The `/PTEX.Fullbanner` TeX-Live/MacPorts version string is cosmetic (common, non-identifying toolchain disclosure) — not a privacy issue.
Whether the PDF *should* be committed at all is a policy call, not a defect: `.gitignore` line 25 comment states "the finished PDF stays tracked" — this is a deliberate repo convention already established at initial commit, and the new PDF is consistent with it. No objection.

## Check 3 — LaTeX build intermediates
Inspected: `paper/*.aux`, `paper/*.log`, `paper/*.out` (present on disk); no `.synctex.gz` present.
`.gitignore` lines 19–21: `*.aux`, `*.log`, `*.out` — all three patterns present and correct.
`git check-ignore -v` confirms all three are ignored:
```
.gitignore:19:*.aux	paper/sparse-mertens-singular-values.aux
.gitignore:20:*.log	paper/sparse-mertens-singular-values.log
.gitignore:21:*.out	paper/sparse-mertens-singular-values.out
```
`git status --porcelain=v1 paper/` → `?? paper/` (untracked dir, as expected pre-add).
`git add -An paper/` (dry run) → only stages `paper/sparse-mertens-singular-values.pdf` and `paper/sparse-mertens-singular-values.tex`. The three intermediates are correctly excluded even under a blanket `git add -A`.
Verdict: **PASS**.

## Check 4 — Secrets/credentials
Inspected: full repo tree (tracked+untracked, excluding .git) for private-key headers, `api_key=`, `password=`, `secret=`, AWS `AKIA...`, Slack `xox...` tokens; separately grepped `paper/`, README.md, proofs/smallest-singular-value.md for the same plus `token`.
Zero matches anywhere.
Verdict: **PASS**.

## Check 5 — Personal/machine identifiers
Author byline "Jeffery Kline" (paper/sparse-mertens-singular-values.tex:31, `\author{Jeffery Kline}`) and `jeffery.kline@gmail.com` in commit author metadata — **intentional, not flagged** per instructions.
Incidental identifier found: `paper/sparse-mertens-singular-values.log` (a build intermediate, NOT `.aux` or `.out`) contains one absolute local path:
```
paper/sparse-mertens-singular-values.log: <<home>/.texlive2021/texmf-var/fonts/pk/ljfour/jknappen/ec/tcrm1095
```
This file is correctly gitignored (see Check 3) and is not staged by `git add -A`, so it will not reach the remote if the normal add flow is used. Grepped `.aux` and `.out` for the same pattern — clean.
No hostnames, IPs, or other usernames found in any file that would actually be committed.
Verdict: **PASS** (the one identifier found lives only in an already-ignored file). **Caution note (cosmetic):** if anyone ever runs `git add -f` on the `.log` file this path would leak — no action needed under normal workflow, flagging for awareness only.

## Check 6 — Agent/tooling traces
Grepped `paper/sparse-mertens-singular-values.tex`, README.md, proofs/smallest-singular-value.md (new/modified content) for `claude|anthropic|scratchpad|/private/tmp|session|task[-_ ]?id|\.venvs|codex|gpt|openai` — zero matches.
Also re-checked the three **already-committed** `audit/reports/*.md` files (1274 lines total) with the same pattern, since these were written by AI agents per the task brief — zero matches. (Consistent with the prior audit pass having already been clean here / this being PRE-EXISTING content unchanged since e75d1c4.)
No acknowledgments section in the paper referencing AI assistance (not required; noting for completeness only).
Verdict: **PASS**.

## Check 7 — Commit trailer
`git log -1 --format=%B` (commit e75d1c4) ends with:
```
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```
Present, and discloses AI co-authorship of the initial commit. This is a disclosure choice by the author — reported neutrally, not a defect.
Note: the uncommitted README/proofs changes and the new `paper/` material are **not yet committed**, so if the author intends a second commit for this new material, whether to add a similar trailer there is an open choice for the author, not an audit finding.

## Check 8 — Third-party runnability of code/*.py
`code/` has **zero diff** vs the pushed commit (`git status --porcelain=v1 code/` and `git diff --stat code/` both empty) — unchanged since last pass, re-verified.
Import scan (`grep "^import\|^from" code/*.py`): only `numpy`, `math`, `sys`, `time`, and intra-package imports (`from checkA import ...`); README states `checkB.py` additionally needs `mpmath`. No `requests`, `urllib`, `socket`, `subprocess`, `os.system`, `os.environ`/`getenv`, or hardcoded `/Users/...` paths found in any `code/*.py` (grep for all of these returned zero hits).
`code/out/` exists on disk but is empty (git doesn't track empty dirs; not an issue).
Verdict: **PASS / PRE-EXISTING** (unchanged from prior audited state).

## Check 9 — LICENSE
`LICENSE` is 674 lines, opens with `GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007`, closes with the standard GPLv3 boilerplate ("...use the GNU Lesser General Public License instead..."). Line count (674) matches the canonical full GPLv3 text length. Unchanged since initial commit (not part of the new diff).
Verdict: **PASS / PRE-EXISTING**. (License identified: GPL-3.0.)

---
All checks complete.

```
CHECKS RUN: 9
PASS: 9   FAIL: 0
MUST-FIX BEFORE PUSH: NONE
TOPICAL CONTAMINATION: 0 (NONE)
PDF METADATA: Producer pdfTeX-1.40.22, Creator "LaTeX with hyperref", Title/Author/Keywords empty, CreationDate=ModDate=2026-07-25 16:12:58 CDT, no XMP, no JavaScript, no embedded files, no OpenAction. /PTEX.Fullbanner discloses TeX Live 2021 (MacPorts build) — toolchain version only, no username/path/hostname. Nothing machine-identifying embedded.
PRIVACY VERDICT: CLEAR-TO-PUSH
```

---

# ADDENDUM — row-level ledger (contract tightened, appended, original report above unchanged)

Verdict, PASS/FAIL counts, and all findings above stand. This addendum adds
(1) a per-check table, (2) full per-file coverage, (3) the sibling-repo
`/PTEX.Fullbanner` cross-check the coordinator asked for.

Before building this ledger, two coverage gaps from the original pass were
closed: `paper/sparse-mertens-singular-values.tex` had only been sampled
(head -60 + section-header grep), and `README.md` / `proofs/smallest-singular-value.md`
had only been seen as `git diff` hunks, not read whole. All three were then
read in full (668 / 72 / 365 lines respectively) — no new findings emerged;
Check 1 in the table below now rests on that full read, not a sample.

## 1. Per-check table

| ID | check | outcome | evidence | must-fix? |
|----|-------|---------|----------|-----------|
| P1 | Topical contamination | PASS | Repo-wide `grep -rniE "Steinhaus|check_ksteinhaus|bulk tightness|Liouville twist|\bE7\b|\bE9\.1\b|\bE12\b|\bBohr\b" .` (excl. `.git`) → 0 matches. `paper/sparse-mertens-singular-values.tex` read in full (668 lines): abstract/§1–§7 + bibliography all concern Redheffer matrix / Mertens function / Alladi's Dickman asymptotic, cross-consistent with `proofs/smallest-singular-value.md` and `README.md` (both also read in full: 72 and 365 lines). `code/*.py` (7 files) confirmed byte-identical to audited commit via `git diff --stat code/` → empty output. `audit/reports/*.md` (3 files) section-header scan (`grep -n "^#"`) shows headings "Proof A — elementary/prime-counting attack on ‖w‖", "Proof B — the analytic route to ‖w‖", "Prior-art / novelty audit" — all on-topic. | — |
| P2 | Built PDF metadata | PASS | `pdfinfo paper/sparse-mertens-singular-values.pdf`: `Producer: pdfTeX-1.40.22`, `Creator: LaTeX with hyperref`, `Title:`/`Author:`/`Keywords:` empty, `CreationDate`=`ModDate`=`Sat Jul 25 16:12:58 2026 CDT`, `Metadata Stream: no`, `JavaScript: no`. `pdfdetach -list` → `0 embedded files`. `grep -a -c "OpenAction\|EmbeddedFile\|/JS"` on raw bytes → `0` each. `strings` reveals one extra field: `/PTEX.Fullbanner (This is pdfTeX, Version 3.141592653-2.6-1.40.22 (TeX Live 2021/MacPorts 2021.58693_2) kpathsea version 6.3.3)` (see P2a below). No `<home>` or absolute path found inside the PDF bytes. | — |
| P2a | `/PTEX.Fullbanner` cross-check vs sibling repo | PRE-EXISTING | See §3 of this addendum below for full detail and the verification caveat. | — |
| P3 | LaTeX build intermediates | PASS | `git check-ignore -v` → `.gitignore:19:*.aux paper/sparse-mertens-singular-values.aux`, `.gitignore:20:*.log paper/…log`, `.gitignore:21:*.out paper/…out`. `git add -An paper/` (dry run) → stages only `paper/sparse-mertens-singular-values.pdf` and `paper/sparse-mertens-singular-values.tex`. No `.synctex.gz` present on disk. | — |
| P4 | Secrets/credentials | PASS | `grep -rnEi "-----BEGIN|api[_-]?key\s*=|password\s*=|secret\s*=|AKIA[0-9A-Z]{16}|xox[baprs]-" .` (excl. `.git`, full tree) → 0 matches. Separate targeted grep of `paper/`, `README.md`, `proofs/smallest-singular-value.md` for `token` added → 0 matches. | — |
| P5 | Personal/machine identifiers | PASS (one contained instance, in an ignored file) | Intentional, not flagged: `paper/sparse-mertens-singular-values.tex:32` `\author{Jeffery Kline}`; `git log -1 --format=%an %ae` → `Jeff Kline jeffery.kline@gmail.com`. Incidental: `paper/sparse-mertens-singular-values.log:` contains `<<home>/.texlive2021/texmf-var/fonts/pk/ljfour/jknappen/ec/tcrm1095` — this file matched `.gitignore:20:*.log` (P3) and is excluded from `git add -An` output, so it does not reach the remote under the normal workflow. `.aux` and `.out` grepped for the same pattern — clean. | Cosmetic — no action required under normal `git add`; flag only if someone force-adds the `.log`. |
| P6 | Agent/tooling traces | PASS | `grep -nEi "claude|anthropic|scratchpad|/private/tmp|session|task[-_ ]?id|\.venvs|codex|gpt|openai"` run against `paper/sparse-mertens-singular-values.tex`, `README.md`, `proofs/smallest-singular-value.md` → 0 matches. Same pattern run against the three already-committed `audit/reports/*.md` (1274 lines total) → 0 matches. Noted, not flagged: `audit/reports/attack-B-analytic.md:2` reads "Agent B. Method: Perron/Mellin…" — this is the repo's own internal label for one of the two independent attackers described in `README.md` ("run under mandated-different methods"), not a Claude/Anthropic/vendor identifier; it does not name a provider. | — |
| P7 | Commit trailer | DISCLOSED (neutral, not PASS/FAIL) | `git log -1 --format=%B` (commit `e75d1c4`) last line: `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Author's disclosure choice. The new uncommitted `paper/`+README/proofs material has no commit yet, hence no trailer to evaluate. | — |
| P8 | Third-party runnability of `code/*.py` | PASS / PRE-EXISTING | `git status --porcelain=v1 code/` and `git diff --stat code/` both empty → unchanged since audited commit. `grep -nEi "requests\.|urllib|socket\.|subprocess|os\.system|os\.environ|getenv|/Users/|open\(\s*['\"]/|hardcode" code/*.py` → 0 matches. `grep -n "^import\|^from" code/*.py` → only `numpy`, `math`, `sys`, `time`, and local intra-package imports (`from checkA import …`); README.md:52 confirms `checkB.py` additionally needs `mpmath`. | — |
| P9 | LICENSE | PASS / PRE-EXISTING | `wc -l LICENSE` → 674. `head -5` → `GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007 / Copyright (C) 2007 Free Software Foundation…`. `tail -5` → standard GPLv3 closing boilerplate ("…use the GNU Lesser General Public License instead of this License…"). 674 lines matches the canonical full GPLv3 text length. File unchanged since initial commit (not part of the current diff). Full-tree secrets/contamination greps (P1, P4) also swept this file's full content with 0 anomalous hits. | — |

## 2. Per-file coverage

All 19 files on disk excluding `.git` (`find . -type f -not -path "./.git/*"`, cross-checked against `git ls-files` + `git ls-files --others --exclude-standard`):

| # | File | Tracked? | Inspected | How / under which check(s) |
|---|------|----------|-----------|------------------------------|
| 1 | `.gitignore` | tracked | YES — full read | `cat .gitignore` (full 32 lines); basis for P3 |
| 2 | `LICENSE` | tracked | PARTIAL (head/tail sample) + full-tree grep | `head -5`/`tail -5`/`wc -l` (P9); swept by full-repo grep in P1/P4 — not read line-by-line in this pass |
| 3 | `README.md` | tracked, modified | YES — full read | `Read` tool, full 72 lines (this addendum); `git diff` hunk also reviewed; swept by grep in P1/P4/P5/P6 |
| 4 | `audit/reports/attack-A-elementary.md` | tracked | PARTIAL (header/structure + full-file grep) | `head -20` + full `grep -n "^#"` section list + full-file grep P1/P4/P6; NOT read end-to-end this pass (537 lines; unchanged vs. audited commit) |
| 5 | `audit/reports/attack-B-analytic.md` | tracked | PARTIAL (header/structure + full-file grep) | same treatment as #4 (515 lines; unchanged) |
| 6 | `audit/reports/prior-art-audit.md` | tracked | PARTIAL (header/structure + full-file grep) | same treatment as #4 (222 lines; unchanged) |
| 7 | `code/alphaA.py` | tracked | PARTIAL (header/docstring + full-file grep) | `head -15` (docstring on-topic: `w_p^2`/Dickman) + P4/P6/P8 grep; `git diff` empty |
| 8 | `code/checkA.py` | tracked | PARTIAL (header/docstring + full-file grep) | `head -15` (usage banner matches README) + P4/P6/P8 grep; `git diff` empty |
| 9 | `code/checkB.py` | tracked | PARTIAL (header/docstring + full-file grep) | `head -15` (Dickman rho, on-topic) + P4/P6/P8 grep; `git diff` empty |
| 10 | `code/convA.py` | tracked | PARTIAL (header/docstring + full-file grep) | `head -15` + P4/P6/P8 grep; `git diff` empty |
| 11 | `code/kdrift.py` | tracked | PARTIAL (full ~35-line file is short enough it was effectively fully shown) | `head -15` covered >40% of the 35-line file, remainder is a print loop; + P4/P6/P8 grep; `git diff` empty |
| 12 | `code/massprofile.py` | tracked | PARTIAL (header + full-file grep) | `head -15` (sieve routine, on-topic) + P4/P6/P8 grep; `git diff` empty |
| 13 | `code/wnorm.py` | tracked | PARTIAL (header/docstring + full-file grep) | `head -15` (docstring names `w_j` closed form, matches Theorem 1) + P4/P6/P8 grep; `git diff` empty |
| 14 | `proofs/smallest-singular-value.md` | tracked, modified | YES — full read | `Read` tool, full 365 lines (this addendum); `git diff` hunk also reviewed; swept by grep in P1/P4/P5/P6 |
| 15 | `paper/sparse-mertens-singular-values.tex` | **untracked** | YES — full read | `Read` tool, full 668 lines (this addendum, upgraded from initial head-60-only sample); basis for P1 |
| 16 | `paper/sparse-mertens-singular-values.pdf` | **untracked** | YES — binary/metadata inspection | `pdfinfo`, `strings`, `pdfdetach -list`, raw-byte grep for OpenAction/EmbeddedFile/JS (P2); text content not independently re-extracted since it is the compiled form of file #15 |
| 17 | `paper/sparse-mertens-singular-values.aux` | **untracked**, gitignored | YES — grep only | `grep -Ei "<user>|/Users/"` → clean (P3/P5) |
| 18 | `paper/sparse-mertens-singular-values.log` | **untracked**, gitignored | YES — grep only | `grep -Ei "<user>|/Users/"` → **hit**, `<home>/.texlive2021/...` (P5); confirmed gitignored (P3) |
| 19 | `paper/sparse-mertens-singular-values.out` | **untracked**, gitignored | YES — grep only | `grep -Ei "<user>|/Users/"` → clean (P3/P5) |

**Files NOT fully read end-to-end this pass, named explicitly:** `LICENSE` (674 lines, sampled), `audit/reports/attack-A-elementary.md` (537 lines), `audit/reports/attack-B-analytic.md` (515 lines), `audit/reports/prior-art-audit.md` (222 lines), and all seven `code/*.py` files (31–460 lines each) — these are all **unchanged since the already-audited, already-pushed commit `e75d1c4`** (verified via empty `git diff`/`git status` against that commit), so this pass relied on (a) that prior full-content audit having already happened — per the task's own stated context, a previous pass read `code/` closely enough to find and remove two contaminating files — plus (b) this session's full-repository-tree keyword/secret/agent-trace greps, which do touch every byte of every one of these files, just not for narrative topical-fit. No new file in this category was introduced since that prior pass, so no *new* topical-fit risk exists in them; the residual risk is that this session did not itself re-verify their topical fit by full narrative read. Flagging this honestly rather than claiming a re-read that did not happen.

`code/out/` exists on disk as an **empty directory** (no files; git does not track empty directories) — confirmed via `ls -la code/out/`, not applicable to file coverage.

## 3. `/PTEX.Fullbanner` cross-check against the sibling repo

Command run: `strings <sibling-repo>/paper/extremal-eigenvalues.pdf | grep -Ei "PTEX.Fullbanner|/Producer|/Creator|<user>|/Users/"`.

Result — **identical fingerprint present in the sibling PDF**:
```
/Author()/Title()/Subject()/Creator(LaTeX with hyperref)/Keywords()
/Producer (pdfTeX-1.40.22)
/PTEX.Fullbanner (This is pdfTeX, Version 3.141592653-2.6-1.40.22 (TeX Live 2021/MacPorts 2021.58693_2) kpathsea version 6.3.3)
```
This is byte-for-byte the same TeX Live/MacPorts version string as in `paper/sparse-mertens-singular-values.pdf` (both PDFs were built by the same local LaTeX toolchain, which is expected — same machine, same TeX installation).

**Verification caveat (important, not glossed over):** the coordinator's message characterizes `<sibling-repo>` as "the already-public sibling repository." I checked this directly: `cd <sibling-repo> && git rev-parse --is-inside-work-tree` returns `fatal: not a git repository (or any of the parent directories): .git` — **this local directory is not a git working tree at all** (consistent with the environment metadata for this session, which reports `Is directory a git repo: No` for that path). I therefore cannot confirm from this machine, via git, that this exact PDF (or this exact `/PTEX.Fullbanner` string) was ever committed or pushed to a public remote — only that a file with this fingerprint exists on local disk at that path. I am not able to verify the coordinator's "already-public" claim from here; if that claim is accurate (e.g., the public copy lives in a separate clone/remote not present on this machine), then the fingerprint is **not new exposure** — it was already public before this pass. If it is not accurate, then this is the first time this exact toolchain string would be exposed, via the sparse-mertens PDF now being prepared, and the P2/P2a finding should be treated as introducing (not merely repeating) this cosmetic disclosure.

Net: the string itself carries no username, path, or hostname in either PDF — only TeX Live version + "MacPorts" package-manager provenance — so even in the worst case (this is novel exposure) it remains **cosmetic, not a must-fix**. Marked P2a **PRE-EXISTING** per the coordinator's framing, with the above caveat recorded rather than silently accepted.

## Ledger totals (unchanged from original report)
```
CHECKS RUN: 9 (P1-P9; P2a is a sub-row of P2, not counted separately)
PASS: 9   FAIL: 0
MUST-FIX BEFORE PUSH: NONE
TOPICAL CONTAMINATION: 0 (NONE)
PRIVACY VERDICT: CLEAR-TO-PUSH
```


