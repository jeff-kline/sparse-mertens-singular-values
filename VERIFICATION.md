# Verification record for Version 0.1.0

**Candidate date:** 2026-08-03

**State:** pre-tag release candidate. These checks were run in a fresh local
virtual environment against the working tree descended from commit
`ecc147a3e8b20d36ffeb0bbc15b3b1c9442adf74`. The final release commit and tag
do not yet exist; their identifiers will be added only after authorization.

This record reports reproducibility checks, not peer review or a certificate of
mathematical correctness.

## Environment

```text
macOS
Python 3.9.6
NumPy 2.0.2
mpmath 1.3.0
pdfTeX 3.141592653-2.6-1.40.22 (TeX Live 2021/MacPorts 2021.58693_2)
git version 2.50.1 (Apple Git-155)
```

The Python dependencies are pinned in `requirements.txt`. Setup from the
repository root was:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Exact and numerical checks

All commands below completed successfully from the repository root.

```bash
.venv/bin/python code/checkA.py verify
```

For `n = 500, 1000, 2000`, the direct dense solve and the closed coordinate
formula agreed with maximum residual `0`; the two reported vector norms also
agreed.

```bash
.venv/bin/python code/wnorm.py 100000 1000000
```

This returned `2289.3` and `12850.5`, respectively, matching the paper.

```bash
.venv/bin/python code/spectra.py munorm
.venv/bin/python code/spectra.py sm 500 1000 2000
.venv/bin/python code/spectra.py smin
.venv/bin/python code/spectra.py smax
.venv/bin/python code/spectra.py redheffer
```

The squarefree-density check printed `0.77971` and then `0.77970` through
`10^7`. The three Sherman--Morrison ratios were `0.989636`, `1.003818`, and
`1.004699`. The smallest-singular-value table matched the paper at
`n = 500, 1000, 2000, 3000`. The largest-singular-value table matched through
`n = 6400`, including `1.00046` for `sigma_max/sqrt(n)` at `n = 3200`. The
Redheffer comparison returned `1.2243`, `1.2475`, `1.2686`, and `1.2875`.

```bash
.venv/bin/python code/massprofile.py 100000 300000 1000000 3000000 10000000
```

This returned the mass values `0.3368`, `0.3354`, `0.3364`, `0.3361`, and
`0.3351`; the four indices printed in the paper agree.

The slower complete grid was also rerun:

```bash
.venv/bin/python code/spectra.py smscan 200 3200 25
```

It reported 114 usable points, with minimum `0.987124` at `n = 300` and
maximum `1.026641` at `n = 225`. It explicitly reported the singular indices
where `M(n) = 0`. This verifies the paper's rounded observed range
`[0.987, 1.027]`.

## Deterministic paper build

From `paper/`, the source was compiled to convergence with:

```bash
env SOURCE_DATE_EPOCH=1785715200 FORCE_SOURCE_DATE=1 \
  pdflatex -interaction=nonstopmode -halt-on-error sparse-mertens-singular-values.tex
env SOURCE_DATE_EPOCH=1785715200 FORCE_SOURCE_DATE=1 \
  pdflatex -interaction=nonstopmode -halt-on-error sparse-mertens-singular-values.tex
```

Two consecutive final builds were byte-identical. The resulting 13-page PDF
has size `322138` bytes and SHA-256:

```text
a2b9dba0d758def56c6c34a1fbebe5e68676ebf467f91574b0b5c8e0de576a52
```

The log had no undefined references, undefined citations, or overfull boxes.
All 13 pages were rendered to images and visually inspected; no clipping,
overlap, broken glyphs, or exposed hyperlink boxes were found.

## Scope and exclusions

- Dense spectral commands are reference computations and become slow as `n`
  grows; the complete commands and tested ranges are stated above.
- Exploratory scripts and finite-range models are not evidence for the proved
  asymptotic claims unless a specific output is cited in the paper.
- No network service, private dataset, or hidden input is required for the
  recorded computations.
- `MANIFEST.sha256` records the final tracked-file bytes separately. Archive
  identity and DOI verification necessarily occur after publication and will
  be appended to the living record without changing the tagged release.
