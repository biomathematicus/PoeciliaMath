# SPECS6: Corrections from Detailed Technical Review
## Supersedes SPECS5 Category A in full. All other prior specs remain in force.
## Confirmed against manuscript TeX source by symbolic algebra (SymPy).

---

## Preamble: Application Order

Before executing SPECS6, the coding agent must apply specs in order:
SPECS4 → SPECS5 (Categories B–F) → SPECS6.

SPECS5 Category A (RODE proof rewrite) is **superseded entirely** by Section 1
of this document, which uses a cleaner argument.

---

## Section 1 — RODE Lemma: Complete Proof Replacement

### What the algebra shows (confirmed by SymPy)

On the face f+m+p=1 (i.e. L=0), each birth term vanishes because each contains
L as a multiplicative factor. Computing the three partial derivatives at L=0:

    ∂ḟ/∂f|_{L=0} = −aβm(f−γp) − (1−η_f)
    ∂ṁ/∂m|_{L=0} = −(1−a)βm(f−γp) − (1−η_m)
    ∂ṗ/∂p|_{L=0} = −γβmp − (1−η_p)

Summing:

    ∇·F|_{f+m+p=1} = −βm[a(f−γp) + (1−a)(f−γp) + γp] + η_f+η_m+η_p − 3
                   = −βmf + η_f+η_m+η_p − 3

Since β > 0, m ≥ 0, f ≥ 0, the term −βmf ≤ 0, so ∇·F ≤ η_sum − 3.
The supremum η_sum − 3 is attained on the edges f = 0 or m = 0.
Therefore ∇·F < 0 on the face ⟺ η_sum < 3.

### Why the existing proof fails (two reasons)

1. **Wrong displayed derivative.** The manuscript's displayed ∂ḟ/∂f is a
   higher-degree polynomial that does NOT match the correct product-rule
   computation. Confirmed by SymPy: the two expressions differ.
   The displayed ∂ṁ/∂m also drops a term. Only ∂ṗ/∂p is correct.

2. **Unnecessary optimization machinery.** The Lagrange-multiplier /
   bordered-Hessian argument is not needed, is not the right tool for a
   compact triangle (whose maximum can occur on the edge, not just at a
   vertex), and invites exactly the criticism it received.

### Precise replacement for `poecilia_manuscript.tex`

#### 1a. Lemma statement

Locate:
```latex
\begin{lemma}[Dissipative Stochasticity Lemma]\label{lem:DissipativePoecilia}
The gynogenetic dynamical system under RODE stochasticity is dissipative when $\eta_f(t)+\eta_m(t)+\eta_p(t)<3$.
\end{lemma}
```

Replace with:
```latex
\begin{lemma}[RODE Boundary Dissipativity Lemma]\label{lem:DissipativePoecilia}
On the population ceiling $f+m+p=1$, the non-dimensional RODE system satisfies
$\nabla\cdot\mathbf{F} \le \eta_f(t)+\eta_m(t)+\eta_p(t)-3$.
In particular, the system is dissipative on that face whenever
$\eta_f(t)+\eta_m(t)+\eta_p(t)<3$.
\end{lemma}
```

#### 1b. Complete proof replacement

Locate the entire `\begin{proof}...\end{proof}` block for this lemma.
It currently begins "We wish to establish conditions under which the RODE system
contracts phase-space volume" and ends with the bordered-Hessian paragraph.

Replace the **entire proof block** (from `\begin{proof}` through `\end{proof}`)
with the following:

```latex
\begin{proof}
We establish that $\nabla\cdot\mathbf{F} < 0$ on the population ceiling
$f+m+p=1$.  On this face the logistic factor $L = 1-f-m-p = 0$, so every
birth term vanishes---each contains $L$ as a multiplicative factor.  The
non-dimensional system therefore reduces to the pure death system
$\dot{f}=-(1-\eta_f)f$, $\dot{m}=-(1-\eta_m)m$, $\dot{p}=-(1-\eta_p)p$
augmented by the logistic structure.  More precisely, at any point on the
face we compute the partial derivatives using the product rule with
$\partial L/\partial f = \partial L/\partial m = \partial L/\partial p = -1$:
\begin{align}
  \frac{\partial\dot{f}}{\partial f}\bigg|_{L=0}
    &= a\beta m\bigl[0 - (f-\gamma p)\bigr] - (1-\eta_f)
     = -a\beta m(f-\gamma p) - (1-\eta_f), \\
  \frac{\partial\dot{m}}{\partial m}\bigg|_{L=0}
    &= (1-a)\beta m\bigl[0 - (f-\gamma p)\bigr] - (1-\eta_m)
     = -(1-a)\beta m(f-\gamma p) - (1-\eta_m), \\
  \frac{\partial\dot{p}}{\partial p}\bigg|_{L=0}
    &= \gamma\beta m\bigl[0 - p\bigr] - (1-\eta_p)
     = -\gamma\beta mp - (1-\eta_p).
\end{align}
Summing these three contributions:
\begin{equation}\label{eq:divF_face}
  \nabla\cdot\mathbf{F}\big|_{f+m+p=1}
  = -\beta m\bigl[(f-\gamma p)+(1-a)(f-\gamma p)/a \cdot a + \gamma p\bigr]
    - 3 + \eta_f+\eta_m+\eta_p.
\end{equation}
Collecting the $m$-bracket:
$a(f-\gamma p)+(1-a)(f-\gamma p)+\gamma p = (f-\gamma p)+\gamma p = f$, so
\begin{equation}\label{eq:BetaFactorPoecilia}
  \nabla\cdot\mathbf{F}\big|_{f+m+p=1} = -\beta m f - 3 + \eta_f+\eta_m+\eta_p.
\end{equation}
Since $\beta>0$, $m\ge 0$, and $f\ge 0$ throughout the feasible region, the
term $-\beta mf \le 0$.  Therefore
\begin{equation}
  \nabla\cdot\mathbf{F}\big|_{f+m+p=1}
  \;\le\; -3 + \eta_f+\eta_m+\eta_p,
\end{equation}
with equality on the edges $\{f=0\}$ or $\{m=0\}$ of the ceiling face.
This upper bound is negative if and only if $\eta_f+\eta_m+\eta_p < 3$.

\begin{remark}
This result is specific to the population ceiling $f+m+p=1$.  In the
interior of the feasible simplex where $L>0$, the birth terms contribute
positive terms to $\nabla\cdot\mathbf{F}$, and the condition
$\eta_f+\eta_m+\eta_p<3$ does not imply global phase-space contraction.
The boundary result is the ecologically meaningful condition: it governs
whether stochastic fluctuations that drive populations toward the
carrying capacity are dissipated (absorbed back) or amplified.
\end{remark}
\end{proof}
```

#### 1c. Introductory scope sentence before the lemma

The sentence immediately before `\begin{lemma}` currently reads:
```
It applies specifically to the RODE formulation---a pathwise,
Liouville-based phase-space contraction argument---and does not extend
directly to Itô or Stratonovich SDEs.
```

This is correct and is kept unchanged.

#### 1d. Abstract: soften point (b)

Find the abstract clause (approximately):
```
the RODE dissipative threshold ($\eta_f + \eta_m + \eta_p < 3$) has
no exact SDE analog
```

Replace with:
```latex
the RODE boundary dissipativity condition ($\eta_f+\eta_m+\eta_p<3$)
characterises phase-space contraction at the population ceiling and has
no exact SDE analog
```

#### 1e. Global search for leftover global-contraction wording

Search the full document for any of: "everywhere in the feasible region",
"global dissipativity", "negative everywhere", "the system is (globally)
dissipative when".  For each occurrence outside the new proof text itself,
add the qualifier "on the population ceiling" or "at the carrying capacity
boundary."

---

## Section 2 — C3 Status: Resolved by Section 1

The incorrect displayed formula for ∂ḟ/∂f (and the partial error in
∂ṁ/∂m) are eliminated by the proof replacement above. No additional
action is required for C3.

---

## Section 3 — Terminology Fixes

### 3a. "Independent demographic noise" → "Independent multiplicative noise"

The scaling σ_i u_i dW_i is geometric/multiplicative (environmental) noise,
not demographic noise. Demographic noise in a count model scales as
√u_i, not u_i.

**Action:** Global search-and-replace in `poecilia_manuscript.tex`:
- "independent diagonal noise" → "independent multiplicative noise"
- "independent demographic noise" → "independent multiplicative noise"
- "demographic stochasticity" (when used to describe the independent-noise
  case specifically) → "independent multiplicative noise"

In the model description table / list of five formulations, change:
```
independent diagonal noise — separate independent Wiener processes W_f, W_m,
W_p per population (demographic stochasticity)
```
to:
```
independent multiplicative noise — separate independent Wiener processes
$W_f, W_m, W_p$ per population (independent geometric noise)
```

In the Discussion / biological interpretation of the two noise cases,
add one sentence acknowledging the distinction:
```latex
True demographic noise in birth--death count models typically scales as
$\sqrt{u_i}$~\citep{Gardiner2009}; the independent multiplicative
($\sigma_i u_i$) scaling used here is appropriate for independent
environmental variation in per-capita rates rather than individual
birth--death events.
```
If `Gardiner2009` is not in the bibliography, use `\citet{Oksendal}` or
omit the citation and write "in the diffusion-approximation literature"
instead.

### 3b. "Non-dissipative case" label

The parameter case η̃_max=0.25 has noise that can exceed the threshold but
also can fall below it at any given time instant. The label "non-dissipative
case" is therefore too absolute.

**Action:** Every occurrence of "non-dissipative case" when describing the
η̃_max=0.25 parameter set should be replaced with
"threshold-exceeding noise range" or "high-amplitude noise case." The
formal Definitions (state of dissipative stochasticity, state of
non-dissipative stochasticity, dissipative threshold) are retained as
mathematical terminology and are NOT changed.

### 3c. "Reflection boundary" → "post-step projection"

The code uses `u_i ← max(u_i, 0)`, which is post-step clipping
(projection onto the nonnegative orthant), not reflection.

**Action:** Replace every occurrence of "reflection boundary", "reflective
boundary", or "reflecting boundary" in the manuscript prose and code
comments with "post-step projection to the nonnegative orthant" or simply
"nonnegative clipping."

---

## Section 4 — RODE One-Sided Noise: Explicit Acknowledgment

### What the issue is

The RODE draws η̃_i(t) ~ Uniform[0, η̃_max], which has positive mean
E[η̃_i] = η̃_max/2 > 0. This is not mean-zero environmental noise; it adds
a positive mean growth bias to all three populations. For the
"threshold-exceeding" case η̃_max = 0.25, δ̃ = 0.1:
E[η̃_i] = 0.125 > δ̃ = 0.1 for each population.

This means the RODE is not a variance-only analogue of the SDEs; it also
changes the mean drift.

### Action: add one paragraph in Section 3 (RODE formulation)

In the subsection describing the RODE formulation, after the sentence that
introduces Uniform[0, η̃_max] sampling, add:

```latex
\begin{remark}
The uniform distribution $\tilde\eta_i(t)\sim\mathrm{Uniform}[0,\tilde\eta_{\max}]$
has positive mean $\mathbb{E}[\tilde\eta_i]=\tilde\eta_{\max}/2$, so the RODE
introduces both variance and a positive mean growth bias compared to a
mean-zero noise model.  For the parameter values used here
($\tilde\eta_{\max}=0.1$, $\tilde\delta=0.1$ in the dissipative case),
the mean noise contribution equals the death rate; in the
threshold-exceeding case ($\tilde\eta_{\max}=0.25$) it exceeds it.
This positive bias is a feature of the random-environment model: it
represents a habitat whose average condition favours growth above the
baseline death rate.  Comparisons between RODE trajectories and SDE
trajectories therefore reflect both differences in stochastic formalism
and differences in mean drift; this distinction is acknowledged
throughout the Results.
\end{remark}
```

### Action: one sentence in Results / Figure 5 caption

In the discussion of Figure 5 (or wherever the single-trajectory
formulation comparison is presented), add:

```
Because the RODE noise is strictly positive-valued, RODE trajectories
reflect a higher mean growth environment than the SDEs and are not
expected to match SDE trajectories in absolute magnitude; the comparison
targets qualitative regime membership (extinction versus coexistence)
rather than quantitative agreement.
```

---

## Section 5 — Minor Prose Fixes

### 5a. Soften Wong–Zakai claim (O2)

Locate the sentence(s) that assert Stratonovich is "physically preferred"
or "the natural interpretation" for this system on grounds of habitat
connectivity / Wong–Zakai.

Replace a strong claim like:
```
therefore the Stratonovich interpretation is physically preferred here
```
with a softer version:
```latex
the Stratonovich interpretation is natural when the environmental noise
arises as the white-noise limit of smooth fast-varying forcing; for
environmental drivers with longer correlation times an explicit
random-environment (RODE-type) model may be more appropriate.
```

### 5b. Table 2 calibration scope (O4)

Locate the Table 2 caption or the surrounding prose that says the
calibrated σ applies to "All SDE variants."

Replace "All SDE variants" with:
"SDE variants (calibrated against Itô/common; same σ applied to other
variants for cross-formulation comparison)."

And add a footnote or parenthetical:
```latex
The calibration targets the It\^{o}/common-noise variant; the same
$\sigma$ tuple is then used for the remaining three SDE variants to
hold noise amplitude constant across formulations.
```

### 5c. Abstract result (d) — Proposition 4 covariance claim

The abstract should not assert that independent noise implies zero
cross-covariance. Locate result (d) and narrow it to:
```latex
under independent multiplicative noise the diffusion cross-driving
between populations vanishes, though deterministic coupling can still
generate covariance through the shared nonlinear drift.
```

---

## Section 6 — Items Flagged for Author Decision (Not Coding Agent)

The following issues identified in the review are **valid** but require
substantive modeling or biological decisions that cannot be resolved by
a coding agent without new author guidance. They are listed here as open
items with recommended courses of action.

| ID | Issue | Options |
|---|---|---|
| C4 | Clipping of L and populations can enable runaway growth above K in RODE | (a) switch to smooth negative logistic above K, or (b) formally define the model as a truncated/projected system |
| C5 | Extinction event definition conflates parasite extinction with host extinction and transient threshold-crossings | Separate outcome classes; decide whether extinction = terminal or absorbing |
| M4 | a=0.8 calibrated from adult sex-ratio (mortality effect) not birth sex-ratio | Reinterpret a as effective female recruitment fraction, or recalibrate from brood data |
| M6 | RODE resampling interval is a model parameter, not just a numerical detail | Introduce explicit correlation-time parameter; sensitivity analysis |
| M7 | Figure 5 shows qualitatively different regimes not "consistent" behavior | Soften prose OR redesign the comparison figure with matched mean-drift calibration |
| M8 | Figure 4(b) shows runaway growth far above K, labelled "noisy coexistence" | Either fix the model (C4) or change the caption and description to be honest about blow-up |

These are recorded here so that the senior author can provide direction
before the manuscript is resubmitted.

---

## Summary: What SPECS6 Adds to the Prior Spec Stack

| Issue | Source | Section here |
|---|---|---|
| Proof rewrite (supercedes SPECS5-A) | C2, C3 | §1 |
| Displayed derivative wrong | C3 | Resolved by §1 |
| "Demographic noise" misnaming | M5 | §3a |
| "Non-dissipative case" too absolute | M9 | §3b |
| "Reflection" vs "projection" | O3 | §3c |
| RODE one-sided mean bias | M1 | §4 |
| Wong–Zakai overreach | O2 | §5a |
| Table 2 calibration claim | O4 | §5b |
| Prop 4 / abstract covariance | M3, M2 | §5c |
| Author decisions flagged | C4,C5,M4,M6,M7,M8 | §6 |
