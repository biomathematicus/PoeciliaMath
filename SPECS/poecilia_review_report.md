# Technical Review Report: *Noise Can Save a Sperm Parasite: Stochastic Stabilization in Gynogenetic Complexes*

Prepared for downstream agent handoff.

## Overall assessment

The manuscript has an interesting biological question, a potentially useful comparison of stochastic formalisms, and a clear ecological message: discrimination speed appears to matter strongly. However, in its current form it is **not ready for submission**. There are two blocking issues:

1. A central analytical claim — the RODE “dissipative threshold” `η_f + η_m + η_p < 3` — is not established by the proof as written and appears to be false for the stated parameter regime.
2. The bibliography/cross-referencing layer is unfinished: there are unresolved citations, an incorrect discovery citation for *Poecilia formosa*, and at least one incorrect DOI.

In addition, the appendix “moment equations” are better described as **heuristic diffusion-only approximations** than full closed moment equations, because drift-induced variance/covariance terms are omitted.

## Severity summary

### Blocking / major revision required
- Invalid or unsupported RODE dissipativity lemma.
- Abstract, discussion, and conclusion rely on that threshold.
- Discovery citation for *P. formosa* is wrong.
- Unresolved bibliography entries remain in the manuscript.
- One verified DOI error (Snelson & Wetherington 1980).

### Substantial but reparable
- Moment-equation derivations are incomplete / overclaimed.
- Biological birth-term interpretation is problematic when `f - γp < 0`.
- Numerical code does not exactly match the analytic model because of clipping/reflection.
- Figure numbering and code/manuscript figure inventory are inconsistent.

### Minor / editorial
- Notation around equilibrium uses initial values in a confusing way.
- Appendix code listings and source package are not self-contained in the uploaded materials.
- Some bibliography formatting inconsistencies remain.

## 1. Major technical issues

### 1.1 RODE dissipativity lemma is not proved, and likely false
The manuscript claims that the non-dimensional RODE system is dissipative whenever

`η_f(t) + η_m(t) + η_p(t) < 3`.

The proof attempts to show `∇·F < 0` everywhere by finding the maximum of the divergence on the constraint boundary `f + m + p = 1`. That is insufficient: the feasible set is the full simplex `f ≥ 0, m ≥ 0, p ≥ 0, f + m + p ≤ 1`, not just its boundary face.

I checked the divergence algebra directly from the stated equations. Along the interior line `f = 0`, `p = 0`, the divergence simplifies to

`∇·F = β(a + γ)(m - m^2) - 3 + (η_f + η_m + η_p)`.

This is maximized at `m = 1/2`, giving

`max ∇·F = β(a + γ)/4 - 3 + η_sum`.

With the manuscript’s parameterization `β = 300`, `a = 0.8`, and `γ ∈ [0.2, 1]`, this quantity is strongly positive. Therefore the condition `η_sum < 3` does **not** imply `∇·F < 0` everywhere.

**Consequence:** Lemma 1 should be withdrawn or completely reworked. If the authors want a valid threshold, they need either:
- a different dissipativity notion,
- a parameter-dependent bound involving `β`, `a`, and `γ`, or
- a purely empirical/numerical “stability boundary” statement rather than a theorem.

### 1.2 The bordered-Hessian verification is internally inconsistent
The main text states that the bordered Hessian determinant at the constrained maximum is `β^2 > 0`.

But the appendix symbolic-verification code (`V3_bordered_hessian`) checks whether the determinant equals **1**, not `β^2`. That is an internal contradiction between text and appendix code.

**Consequence:** Either the theorem text is wrong, the verification code is wrong, or both. This must be reconciled.

### 1.3 The “closed moment equations” are incomplete
The appendix presents variance equations such as

`dVar[f]/dt = σ_f^2(F^2 + Var[f])`

and sets independent-noise covariance equations identically to zero.

That omits the drift-generated parts of second-moment evolution. In a nonlinear coupled system, even with independent Wiener drivers, deterministic coupling can generate covariance. So the implemented system is not a full second-moment closure; it is a diffusion-only approximation layered on top of the mean-field equations.

**Consequence:**
- Propositions 3 and 4 are overclaimed.
- Section 5.4 should not present this system as a validated “closed moment equation” framework for variance/covariance.
- The authors should either derive the full approximate second-moment system or clearly relabel this as a heuristic approximation.

### 1.4 Birth terms can become negative
The bisexual birth terms are proportional to `(f - γp)`. If `γp > f`, the model yields **negative births** for bisexual females and males.

That may be mathematically usable as a reduced net term, but it is biologically nonstandard if presented literally as a birth term. At minimum, the interpretation must be clarified.

**Recommendation:** Either reformulate these terms using a nonnegative mating function or explicitly state that `(f - γp)` is a reduced effective encounter balance and not a literal count of births.

### 1.5 Analytic model and numerical implementation are not the same system
The equations in the text use the logistic factor

`L = 1 - (f + m + p)`.

But the code replaces this with `max(1 - f - m - p, 0)` and also clips populations to nonnegative values after each step (RODE, Euler–Maruyama, Heun).

Those are sensible numerical safeguards, but they create a piecewise-clipped system that is not identical to the smooth model used in the analysis.

**Consequence:** The manuscript should explicitly state that the numerics solve a truncated/reflected approximation to preserve biological feasibility.

### 1.6 The scalar Lyapunov analysis is narrower than the prose suggests
The Itô and Stratonovich Lyapunov exponents are derived from a scalarized `p`-subsystem near `p ≈ 0` under quasi-steady-state assumptions for the bisexual populations.

That local result is mathematically reasonable as a heuristic, but several places in the manuscript phrase the conclusion as if it were a full-system global stability result.

**Recommendation:** Reword throughout:
- “local scalar stability heuristic near the extinction boundary”
- not “the stability boundary” for the full 3D system.

## 2. Internal consistency and structural issues

### 2.1 Unresolved references remain in the manuscript
There are still unresolved `?`-style references/citations in the PDF/source, including:
- the mass-action framework citation,
- the bark-beetle citation,
- “Figure ??” for the mating pedigrees.

These need to be fixed before any serious review.

### 2.2 Figure inventory is inconsistent
The appendix master script states that it generates **10 figures**. The script includes a “Figure 7: Ito-Stratonovich divergence.”

But the manuscript body contains only 9 main figures and skips that figure in the running text. The body’s Figure 7 is “Moment equations vs Monte Carlo,” while the code’s Figure 7 is something else entirely.

**Recommendation:** Make the figure numbering consistent across:
- main text,
- captions,
- appendix/source listings,
- run-all script.

### 2.3 Source package is not self-contained as uploaded
The `.tex` file references external figure files under `poecilia_sde/figures/...`, but those files are not included in the uploaded source package. The upload also does not include the actual `.py` source files listed in the appendix.

**Consequence:** The appendix claim that the paper is fully reproducible from the included materials is not true for the uploaded package.

### 2.4 Equilibrium notation is confusing
Section 2.2 says the steady state satisfies `u̇(u0) = 0` and then plugs in `f0 = 100`, `p0 = 10`. That conflates initial conditions with equilibrium coordinates.

**Recommendation:** Use `f^*`, `m^*`, `p^*` for equilibrium values, then specialize numerically if desired.

## 3. Reference verification

## Verified as correct (or plausibly correct)
The following references appear to match real publications and their intended use:
- Avise et al. (1991) — *Poecilia mexicana is the recent female parent of the unisexual fish P. formosa*.
- Kiester, Nagylaki & Shaffer (1981).
- Schley, Doncaster & Sluckin (2004).
- Kokko, Heubel & Rankin (2008).
- Peck, Yearsley & Barreau (1999).
- Riesch, Schlupp & Plath (2008).
- Buckingham (1914).
- Marsden & Tromba, *Vector Calculus* (2003).
- Øksendal, *Stochastic Differential Equations*.
- Kloeden & Platen, *Numerical Solution of Stochastic Differential Equations*.

## Definite reference errors

### 3.1 The discovery citation for *P. formosa* is wrong
The manuscript says the first gynogenetic vertebrate, *P. formosa*, was discovered by Hubbs and Hubbs in 1932, but cites reference [14].

Reference [14] is Wetherington, Schneck & Vrijenhoek (1989) on unisexual *Poeciliopsis*, not Hubbs & Hubbs 1932.

**Action:** Replace this citation with the actual Hubbs & Hubbs 1932 discovery paper.

### 3.2 Snelson & Wetherington DOI is incorrect
The manuscript lists the DOI for

Snelson Jr. & Wetherington (1980), *Sex ratio in the sailfin molly, Poecilia latipinna*

as `10.1111/j.1558-5646.1980.tb04817.x`.

The correct DOI is

`10.1111/j.1558-5646.1980.tb04819.x`.

### 3.3 Missing Løyning/Kirkendall citation
The bark-beetle comparison is cited in the source as `Loyning1996`, but that key is absent from the supplied `.bib` files. This is why the manuscript shows an unresolved citation.

**Action:** Add the missing bibliography entry and verify that it is the intended bark-beetle mate-discrimination paper.

### 3.4 Buckingham key mismatch
The source cites `Buckingham1914` in one place and `Buckingham:1914` in another. The available `.bib` entry uses `Buckingham:1914`.

**Action:** Standardize the key usage throughout the source.

## Probably fine, but worth a quick manual spot-check
- Heubel et al. (2009) metadata look plausible, though some databases format the DOI year component differently.
- Balsano et al. (1989) chapter pagination may vary slightly by source; not flagged as definite error.

## 4. Claims that should be softened or rewritten

### 4.1 Abstract point (b) depends on an invalid threshold theorem
Because the RODE threshold result is not currently established, the abstract should not present `η_f + η_m + η_p < 3` as a firm analytical result.

### 4.2 “Noise can save a sperm parasite” is stronger than the validated evidence
The title is catchy, but in the current manuscript the strongest defensible statement is narrower:
- discrimination speed robustly changes outcomes in simulations and across formulations,
- stochastic formulation affects quantitative predictions,
- the scalar Itô vs Stratonovich distinction matters locally near extinction.

Given the problems with Lemma 1 and the moment-closure overreach, the title may currently oversell the validated conclusions.

### 4.3 “Stochasticity alone is insufficient in any framework” should be toned down
That statement is too broad given the unresolved RODE analysis and the heuristic status of the moment equations.

## 5. Suggested revision plan

### Priority 1: fix the mathematics
1. Remove or repair Lemma 1 and all downstream claims that rely on it.
2. Reconcile main text and symbolic-verification appendix.
3. Re-derive second-moment equations properly, or relabel them as heuristic approximations.
4. Narrow the interpretation of the scalar Lyapunov results.

### Priority 2: fix references and cross-references
1. Replace the incorrect discovery citation with Hubbs & Hubbs (1932).
2. Correct the Snelson & Wetherington DOI.
3. Add the missing Løyning/Kirkendall reference.
4. Fix Buckingham key mismatch.
5. Resolve all `?` citations and “Figure ??” placeholders.

### Priority 3: align text, code, and reproducibility claims
1. Make figure numbering consistent.
2. State clearly that the numerics use clipping/reflection and `max(L,0)`.
3. Either supply the actual code/figures as supplementary material or soften the reproducibility claim.

## 6. Recommendation to downstream agent

Treat this manuscript as a **major-revision technical rescue**, not a light copyedit.

The correct workflow is:
1. repair the bibliography and cross-references,
2. rewrite or remove the dissipativity theorem,
3. revise the abstract/conclusion to avoid unsupported analytical claims,
4. relabel the moment-closure section unless a full derivation is added,
5. then do stylistic cleanup and final consistency checks.

## 7. Bottom line

The paper contains promising ideas and a potentially publishable stochastic-comparison framework, but at present its central theoretical claim about the RODE threshold is not reliable, and the reference layer is unfinished. The manuscript should not proceed unchanged.
