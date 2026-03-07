# SPECS5: Response to Technical Review — Targeted Repairs
## Addendum to prior specs. Where SPECS5 conflicts with earlier specs, SPECS5 governs.

---

## Overview

This spec addresses the review report in priority order. Six categories of changes
are required. The title is NOT changed. Items are listed from most to least
consequential.

---

## Category A — RODE Lemma: Reframe as Boundary Dissipativity

### What is wrong

The proof establishes that the maximum of ∇·F on the face f+m+p=1 (L=0) is
−3 + η_sum. This is mathematically correct. On that face the β coefficient
is exactly −f·m ≤ 0, so β terms reduce the divergence and the maximum is at
(f,m,p)=(0,0,1) with value −3 + η_sum.

However, the proof does NOT cover the full feasible simplex. At the interior
point f=0, m=½, p=0, the divergence is β(a+γ)/4 + η_sum − 3 ≈ 72 + η_sum
for the manuscript's parameters (β=300, a=0.8, γ=0.2). The condition
η_sum < 3 therefore does NOT imply global phase-space contraction.

### What the fix is

The Lemma is restated as a **boundary dissipativity** result, which is both
mathematically valid and ecologically meaningful. The three Definitions
(dissipative stochasticity, non-dissipative, threshold) are retained unchanged.

### Precise edits to `poecilia_manuscript.tex`

#### A1. Lemma statement

Replace:
```latex
\begin{lemma}[Dissipative Stochasticity Lemma]\label{lem:DissipativePoecilia}
The gynogenetic dynamical system under RODE stochasticity is dissipative when $\eta_f(t)+\eta_m(t)+\eta_p(t)<3$.
\end{lemma}
```

With:
```latex
\begin{lemma}[RODE Boundary Dissipativity Lemma]\label{lem:DissipativePoecilia}
On the population ceiling $f + m + p = 1$ (where $L = 0$), the RODE
gynogenetic system is dissipative---that is, $\nabla \cdot \mathbf{F} < 0$
on that face---if and only if $\eta_f(t)+\eta_m(t)+\eta_p(t)<3$.
\end{lemma}
```

#### A2. Proof: opening sentence

Replace:
```latex
We wish to establish conditions under which the RODE system contracts
phase-space volume, which by Liouville's theorem requires
$\nabla \cdot \mathbf{F} < 0$ everywhere in the feasible region.
```

With:
```latex
We wish to establish conditions under which the RODE system contracts
phase-space volume at the population ceiling $f + m + p = 1$.  At this
boundary face the logistic factor $L = 0$ and all birth terms vanish;
consequently, only the noise-amplitude terms and the linear death terms
contribute to the divergence.  By Liouville's theorem, phase-space volume
contracts on this face when $\nabla \cdot \mathbf{F} < 0$ there.
```

#### A3. Proof: sentence after divergence formula

Replace the sentence:
```
The key observation is that the constant (state-independent) part of the
divergence is $-3 + \eta_f + \eta_m + \eta_p$.
```

With:
```latex
A key algebraic fact is that on the constraint surface $f + m + p = 1$
(i.e.\ substituting $p = 1-f-m$), the coefficient of $\beta$ in the
divergence reduces to $-fm \leq 0$ for all $f, m \geq 0$.  Therefore, on
this face, the $\beta$-dependent terms are non-positive and do not
contribute to expanding phase-space volume.  The maximum of
$\nabla \cdot \mathbf{F}$ on this face is therefore determined entirely by
the state-independent part $-3 + \eta_f + \eta_m + \eta_p$.
```

#### A4. Proof: closing sentence, add scope note

After "...which completes the proof." and before `\end{proof}`, add:

```latex
\begin{remark}
The boundary dissipativity condition $\eta_f + \eta_m + \eta_p < 3$
characterizes contraction at the population ceiling.  In the interior of
the feasible simplex, where $L > 0$, the divergence can be positive for
the parameter regime used here; global phase-space contraction would
require a parameter-dependent bound involving $\beta$, $a$, and $\gamma$.
The boundary result is the ecologically relevant condition: it governs
whether stochastic fluctuations that drive populations toward the carrying
capacity are dissipated or amplified.
\end{remark}
```

#### A5. Abstract: soften point (b)

Locate the abstract sentence that reads (approximately):
```
(b) the RODE dissipative threshold ($\eta_f + \eta_m + \eta_p < 3$) has
no exact SDE analog
```

Replace with:
```latex
(b)~the RODE boundary dissipativity condition ($\eta_f + \eta_m + \eta_p
< 3$) characterises phase-space contraction at the population ceiling and
has no exact SDE analog---
```

#### A6. Discussion and Conclusion: global search

Search the full document for every occurrence of the phrase "dissipative"
or "$\eta_f + \eta_m + \eta_p < 3$" or "RODE threshold" outside the Lemma
and proof themselves.  For each occurrence, ensure that the phrasing is
limited to the boundary/ceiling context and does not assert global
phase-space contraction.  Specific replacements:

- "the system is globally dissipative" → "the system is dissipative at the
  population ceiling"
- "the RODE threshold guarantees dissipation" → "the RODE threshold
  guarantees dissipation at the carrying capacity boundary"

---

## Category B — Bordered Hessian: Fix Verification Code Only

### What is wrong

The current manuscript text correctly states $|\bar{H}| = \beta^2 > 0$.
The SymPy verification (V3 in `verification.py`) checks whether the
determinant equals **1** (the old dissertation value) and reports
"CORRECTED" with actual value "beta**2". This creates an internal
inconsistency between the manuscript text and the appendix verification.

### Fix: update `verification.py` task V3

In `poecilia_sde/verification.py`, locate the V3 function
`V3_bordered_hessian`. Change the pass/fail check from testing equality
to 1, to testing equality to β²:

Replace:
```python
result = {
    'bordered_hessian_det': str(det_H),
    'det_equals_1': bool(sp.simplify(det_H - 1) == 0),
    'status': 'PASS' if sp.simplify(det_H - 1) == 0 else 'CORRECTED',
    'actual_value': str(det_H)
}
print(f"  V3: |H_bar| = {det_H}")
print(f"      Equals 1: {result['det_equals_1']}")
print(f"      Status: {result['status']}")
```

With:
```python
beta_sym = sp.Symbol('beta', positive=True)
expected = beta_sym**2
check = sp.simplify(det_H - expected) == 0
result = {
    'bordered_hessian_det': str(det_H),
    'det_equals_beta_squared': check,
    'status': 'PASS' if check else 'FAIL',
    'actual_value': str(det_H)
}
print(f"  V3: |H_bar| = {det_H}")
print(f"      Equals beta^2: {result['det_equals_beta_squared']}")
print(f"      Status: {result['status']}")
```

The manuscript text (`$|\bar{H}| = \beta^2 > 0$`) is correct and is
NOT changed.

---

## Category C — Moment Equations: Relabel as Heuristic Approximation

### What is wrong

The variance/covariance equations retain diffusion-driven terms but omit
drift-generated second-moment contributions. Under mean-field closure the
full second-moment system would include terms from
$\mathrm{d}\mathbb{E}[f^2]/\mathrm{d}t = 2\mathbb{E}[f \cdot \dot{f}] + \sigma_f^2 \mathbb{E}[f^2]$,
where the drift term $\mathbb{E}[f \cdot \dot{f}]$ involves cross-products
with $m$ and $p$ that were not included. The implemented system is a
diffusion-only approximation layered on the mean-field equations.

### Fix: Propositions 3 and 4

Locate the statements of Propositions 3 and 4 (variance divergence and
covariance structure). Change the proposition labels and opening text:

For **Proposition 3** (wherever it appears), change:
```latex
\begin{proposition}[Variance divergence]
```
To:
```latex
\begin{proposition}[Diffusion-driven variance approximation]
```

And add after the statement (before the proof or immediately after):
```latex
\begin{remark}
This expression retains only the diffusion-driven contribution to variance
growth.  Under mean-field closure, drift-generated second-moment terms of
the form $2\mathbb{E}[u_i \cdot \mu_i(\mathbf{u})]$ are omitted; those
terms involve products of means and covariances that are negligible when
population fluctuations are small relative to the mean trajectory.  The
implemented system is therefore a heuristic approximation that is
accurate near the mean-field solution and becomes less reliable as
variance grows large.
\end{remark}
```

For **Proposition 4** (covariance structure), change:
```latex
\begin{proposition}[Covariance structure]
```
To:
```latex
\begin{proposition}[Diffusion-driven covariance approximation]
```

### Fix: Section 5.4 heading

In the numerical results section, wherever the moment equations are
compared to Monte Carlo, ensure the figure caption and surrounding prose
say "diffusion-approximated moment equations" rather than "closed moment
equations." Specifically, locate the phrase "closed moment equation
framework" or "validated closed moment" and replace with "diffusion-
approximated moment equation framework."

---

## Category D — Minor Model and Numerical Clarifications

### D1. The (f − γp) term: add one sentence of interpretation

In the Deterministic Core subsection, after the γ_eq analysis, add:

```latex
When $\gamma p > f$, the term $f - \gamma p$ becomes negative,
representing a net diversion of male mating effort so complete that it
exceeds the available bisexual female population; in this regime the model
predicts net decline of the bisexual population from competition for male
attention alone.  The numerical implementation clips populations to
nonnegative values at each step to maintain biological feasibility.
```

### D2. Numerical clipping: add one sentence

In the Numerical Methods appendix section describing the RODE and SDE
solvers, add the following sentence at the end of each solver description:

```latex
Population values are clipped to $[0, \infty)$ after each step, and the
logistic factor is evaluated as $L = \max(1 - f - m - p,\, 0)$; the
simulated system therefore solves a truncated approximation to the smooth
analytical model.
```

### D3. Lyapunov prose scope: narrow two sentences

Locate the prose that describes the Lyapunov/stability boundary results.
Any sentence that uses "stability boundary of the system" or "the system
is stable/unstable" should be preceded by the qualifier "of the scalar
$p$-subsystem near the extinction boundary $p \approx 0$." Specifically:

Replace (wherever this phrasing or equivalent appears):
```
the stability boundary
```
With:
```
the local scalar stability boundary near extinction ($p \approx 0$)
```

### D4. Equilibrium notation: f* instead of f₀

In the Deterministic Core subsection, the steady-state analysis currently
uses $f_0$, $m_0$, $p_0$ for both initial conditions and equilibrium
coordinates. Replace all equilibrium occurrences with $f^*$, $m^*$, $p^*$
to avoid conflation with the initial conditions $\tilde{f}_0 = 100$, etc.

Specifically: in the γ_eq derivation block and the equation
`\label{eq:GammaSS}`, replace:
- `f_0` → `f^*` (equilibrium only; do NOT change initial condition uses)
- `p_0` → `p^*` (equilibrium only)

The numerical substitution sentence then reads:
```latex
With the parameter values $a = 0.8$, $f^* = 100$, and $p^* = 10$, this
gives $\gamma_{eq} = 80/108 \approx 0.74$.
```

---

## Category E — Bibliography Repairs

### E1. Discovery citation for *P. formosa*

The sentence stating that *P. formosa* was discovered by Hubbs and Hubbs
in 1932 currently cites `\citet{Wetherington1989}`, which is wrong
(that paper is about *Poeciliopsis*). 

**Action:** Replace the citation with the correct reference. Add the
following entry to the bibliography (`.bib` file):

```bibtex
@ARTICLE{Hubbs1932,
  AUTHOR  = {C. L. Hubbs and L. C. Hubbs},
  TITLE   = {Apparent parthenogenesis in nature, in a form of fish of
             hybrid origin},
  JOURNAL = {Science},
  VOLUME  = {76},
  NUMBER  = {1983},
  PAGES   = {628--630},
  YEAR    = {1932},
  DOI     = {10.1126/science.76.1983.628},
}
```

In the text, change `\citet{Wetherington1989}` (in the discovery sentence
only) to `\citet{Hubbs1932}`.

### E2. Snelson & Wetherington DOI correction

Locate the bibliography entry for Snelson & Wetherington (1980). The DOI
`10.1111/j.1558-5646.1980.tb04817.x` is incorrect.

Replace with: `10.1111/j.1558-5646.1980.tb04819.x`

### E3. Add missing Løyning & Kirkendall (1996) entry

The bark-beetle comparison in the Mechanistic Derivation cites
`\citep{Loyning1996}` but the key is absent from the `.bib` file (causing
an unresolved `[?]`). Add:

```bibtex
@ARTICLE{Loyning1996,
  AUTHOR  = {M. K. L{\o}yning and L. R. Kirkendall},
  TITLE   = {Mate discrimination in a pseudogamous bark beetle
             ({C}oleoptera: {S}colytidae): male \textit{Ips acuminatus}
             prefer sexual to clonal females},
  JOURNAL = {Oikos},
  VOLUME  = {77},
  NUMBER  = {2},
  PAGES   = {336--344},
  YEAR    = {1996},
  DOI     = {10.2307/3546074},
}
```

### E4. Buckingham citation key: standardize

The source uses both `Buckingham1914` and `Buckingham:1914`. The available
`.bib` entry uses `Buckingham:1914`. 

**Action:** Global search-and-replace in the `.tex` file:
- `\citep{Buckingham1914}` → `\citep{Buckingham:1914}`
- `\citet{Buckingham1914}` → `\citet{Buckingham:1914}`

### E5. Mass-action citation

The Mechanistic Derivation cites `\citep{Buckingham1914}` for the
mass-action framework. Verify this resolves after E4. If a separate
mass-action citation is needed, the Buckingham (1914) reference is
appropriate for the dimensionality/scaling justification; no additional
entry is required.

---

## Category F — Figure and Cross-Reference Consistency

### F1. Pedigree figure placeholder

Search the document for `Figure~\ref{fig:pedigrees}` or `Figure~??` in
the Mechanistic Derivation. If the pedigree figure label does not exist
or does not resolve, either:
(a) Add `\label{fig:pedigrees}` to the appropriate existing pedigree
    figure, or
(b) Replace the reference with a description: "the mating pedigrees
    (see Figure~\ref{fig:constant_gamma})" if no separate pedigree figure
    exists in the current manuscript.

### F2. Figure inventory

Ensure the run script `run_all.py` and the manuscript body agree on figure
count and numbering. If Figure 7 in the code generates "Itô–Stratonovich
divergence" but Figure 7 in the manuscript body is "Moment equations vs
Monte Carlo," renumber the code figures to match the manuscript body order.
The manuscript body ordering takes precedence.

---

## Summary Table

| Category | Issue | Action | Severity |
|---|---|---|---|
| A | RODE Lemma invalid as global claim | Reframe as boundary dissipativity | **Blocking** |
| B | V3 verification code checks wrong value | Update V3 to check β² | Major |
| C | Moment equations overclaimed | Relabel as heuristic approximation | Major |
| D1 | (f−γp) sign interpretation | Add one clarifying sentence | Minor |
| D2 | Numerical clipping undisclosed | Add one sentence per solver | Minor |
| D3 | Lyapunov scope too broad | Narrow qualifier in prose | Minor |
| D4 | Equilibrium notation ambiguous | Replace f₀/p₀ with f*/p* in γ_eq | Minor |
| E1 | Wrong discovery citation | Replace with Hubbs1932 | Major |
| E2 | Snelson DOI wrong | Correct DOI | Major |
| E3 | Løyning citation missing | Add bib entry | Major |
| E4 | Buckingham key mismatch | Standardize key | Minor |
| F1 | Pedigree figure unresolved | Add label or redirect | Minor |
| F2 | Figure numbering inconsistent | Align code to manuscript | Minor |

## What the Agent Must NOT Change

- The title.
- The three Definitions (dissipative stochasticity, non-dissipative, threshold) —
  these are retained as useful biological terminology.
- The Itô/Stratonovich Lyapunov exponent analysis — this is local and is
  already correctly scoped as a scalar p-subsystem result.
- The discrimination speed finding — this is robust and unaffected by
  any of the above issues.
- Any prior SPECS edits (SPECS1–SPECS4) not explicitly superseded here.
