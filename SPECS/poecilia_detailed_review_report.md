# Detailed technical review report for *Noise Can Save a Sperm Parasite: Stochastic Stabilization in Gynogenetic Complexes*

Prepared for downstream editorial/technical revision.

Reviewed artifacts:
- `poecilia_manuscript.pdf`
- `poecilia_manuscript.tex`
- `poecilia_references.bib`
- `JBGInvasiveSpecies.bib`

Date of review: 2026-03-07

---

## 1. Executive assessment

**Overall recommendation: major revision, with a source-sync/reproducibility repair required before technical revisions are fully actionable.**

The new PDF is substantially improved relative to the prior version in one important respect: the RODE result is now framed as a **boundary** statement rather than a fully global dissipativity theorem. That is the right direction. However, several serious problems remain:

1. **The manuscript package is internally inconsistent.** The uploaded PDF, TeX source, and bibliography files are not synchronized. Some of the PDF’s corrections are not present in the TeX, and some bibliography fixes present in the PDF are not present in the attached `.bib` files.
2. **The boundary-dissipativity proof is still not cleanly correct as written.** Even in the corrected PDF, the proof retains leftover global wording and uses an unnecessary/incorrect constrained-optimization argument.
3. **A displayed derivative in the proof is explicitly wrong.**
4. **The numerical model being simulated is not the same smooth model being analyzed.** Clipping and truncation alter the dynamics, and in the RODE case the resulting system can exhibit runaway growth far beyond carrying capacity.
5. **The stability-boundary analysis does not match the ecological question or the scalar Lyapunov analysis.** The binary “extinction probability” used in Figure 8 / Table 3 conflates parasite extinction, host extinction, and transient threshold crossings.
6. **Several central prose claims are stronger than what the figures and code actually support.**
7. **Reference verification is improved in the PDF, but the attached source bibliography remains defective.**

The single most important editorial instruction for the next agent is:

> **Do not edit the paper incrementally until the PDF, TeX, and Bib files are synchronized.** Right now there are two different manuscripts: the PDF and the source package.

---

## 2. Highest-priority findings (triage list)

### Critical (must be fixed before submission)

#### C1. The uploaded PDF and the uploaded source files are not synchronized.

This is not a cosmetic issue; it affects the core mathematics and the bibliography.

Examples:
- The **PDF** states the RODE result as a **boundary dissipativity** result at the population ceiling and explicitly notes that interior divergence can be positive (PDF Section 4.1, p. 10–12).
- The **TeX source** still contains the **older, stronger, globally false** version:
  - Lemma statement in TeX: “The gynogenetic dynamical system under RODE stochasticity is dissipative when \(\eta_f+\eta_m+\eta_p<3\).” (source lines 469–471)
  - Proof still says: “requires \(\nabla\cdot F<0\) everywhere in the feasible region” and concludes negativity “everywhere” (source lines 473–520).
- The **PDF reference list** gives the corrected Snelson DOI; the attached `poecilia_references.bib` still contains the old wrong DOI.
- The **TeX source** cites keys that are absent from the attached bib files (`Buckingham1914`, `Loyning1996`), yet the PDF reference list resolves them.

**Practical consequence:** another agent editing the TeX/Bib files will be editing an older manuscript than the one represented by the PDF.

**Required action:** create a canonical source package that reproduces the uploaded PDF exactly, then revise from that package only.

---

#### C2. The RODE lemma’s *statement* in the PDF is narrower and acceptable, but the *proof* is still internally inconsistent and should be replaced.

What is now correct in the PDF:
- The result is stated on the **population ceiling** \(f+m+p=1\), not on the full simplex.
- The manuscript now acknowledges that the divergence can be positive in the interior.

What remains wrong in the proof text:
- The proof still says, in substance, that to show dissipativity one must show negativity “everywhere in the feasible region” and then optimizes only on the boundary face. That is a leftover from the earlier, stronger, invalid theorem.
- On the ceiling face \(p=1-f-m\), the divergence simplifies immediately to
  \[
  \nabla\cdot F = -\beta f m - 3 + \eta_f + \eta_m + \eta_p.
  \]
  That is enough. One gets the bound
  \[
  \nabla\cdot F \le -3 + \eta_f + \eta_m + \eta_p,
  \]
  with equality whenever \(f=0\) **or** \(m=0\).
- The manuscript instead introduces a Lagrange-multiplier / bordered-Hessian argument centered on the point \((0,0,1)\). This is unnecessary and, more importantly, not the right way to characterize the maximum on a closed triangle with inequality boundaries because the maximizer is **not unique**: the maximum occurs along the entire edge set \(\{f=0\}\cup\{m=0\}\), not just at the vertex \((0,0,1)\).

**Why this matters:** the lemma’s conclusion is salvageable, but the proof as written invites exactly the same criticism as the earlier version.

**Recommended rewrite:**
1. State explicitly that the result concerns the face \(f+m+p=1\).
2. Substitute \(p=1-f-m\) into the divergence.
3. Show the face-restricted divergence equals \(-\beta fm-3+\eta_f+\eta_m+\eta_p\).
4. Since \(f,m\ge 0\), conclude the maximum is \(-3+\eta_f+\eta_m+\eta_p\), attained whenever \(f=0\) or \(m=0\).
5. Delete the Lagrange-multiplier and bordered-Hessian discussion entirely.

---

#### C3. A displayed derivative in the proof is wrong.

The manuscript’s displayed formula for \(\partial \dot f / \partial f\) is incorrect.

The system has
\[
\dot f = a\beta L m (f-\gamma p) - (1-\eta_f)f,\qquad L=1-f-m-p.
\]
The correct derivative is
\[
\frac{\partial \dot f}{\partial f}
= a\beta\left[-m(f-\gamma p) + Lm\right] - (1-\eta_f)
= a\beta m\bigl(L-(f-\gamma p)\bigr) - (1-\eta_f).
\]

The displayed manuscript formula expands into a different polynomial and does **not** simplify to the correct derivative.

**Importance:** even if the subsequent face-restricted divergence is verified symbolically elsewhere, the proof as written contains a calculus error. A careful reviewer will catch this immediately.

**Required action:** replace the displayed derivative with the correct formula.

---

#### C4. The simulated model is not the same model as the one analyzed, and this is no longer a minor caveat.

Across the numerical sections and code appendix, the simulations implement
- population clipping: \(u_i \leftarrow \max(u_i,0)\), and
- truncated logistic factor: \(L \leftarrow \max(1-f-m-p,0)\).

This means the numerical system is a **projected/truncated** model, not the smooth ODE/SDE analyzed in Sections 2–4.

The consequences are important:
- Above carrying capacity, the logistic term does **not** become negative; it is set to zero.
- Therefore the density regulation disappears above the “ceiling” instead of pushing trajectories back down.
- In the RODE case, because the noise term is one-sided positive, the system can then undergo **runaway growth** above \(K\).

This is not hypothetical. In Figure 4(b), one population (the unisexual population \(\tilde p\), red) explodes to approximately **7,500–8,000**, despite \(\tilde K=300\). That is not a carrying-capacity-limited coexistence regime; it is numerical/model blow-up enabled by the truncation.

**Interpretive consequence:** the paper’s wording that Figure 4(b) shows “noisy coexistence” is not supportable from the figure itself. The figure shows runaway parasite growth far beyond the environmental ceiling.

**Required action:** either
- analyze and simulate the same smooth model (allowing negative logistic contribution above carrying capacity), or
- explicitly redefine the model as a truncated/projection model and stop interpreting the ceiling face as a biologically hard carrying capacity.

If the truncated model is retained, Figures 4 and 5 and the accompanying discussion need to be reframed.

---

#### C5. Figure 8 / Table 3 “extinction probability” does not measure the same thing as the scalar Lyapunov analysis.

The scalar Lyapunov analysis in Section 4.3 is about the **parasite component \(p\)** near the extinction boundary \(p=0\).

The code appendix defines the Monte Carlo extinction event differently:
- a trajectory is counted as extinct if **any** population component falls below `1e-3`
- at **any time during the last quarter** of the simulated interval.

This creates three separate mismatches:

1. **Biological mismatch:** parasite extinction, host extinction, male extinction, and full-system collapse are all treated as the same event.
2. **Analytical mismatch:** the scalar Lyapunov exponent applies to parasite extinction near \(p=0\), not to “any component near zero.”
3. **Statistical mismatch:** a transient dip below threshold during the last quarter counts as “extinction,” even if the population is not terminally extinct at \(t=T\).

**Why this matters:** the paper treats Figure 8 as empirical support for the Lyapunov discussion, but the figure is measuring a different binary event.

**Recommended action:** replace the single “extinction probability” with a multiclass outcome summary:
- parasite extinction while host persists,
- host extinction while parasite persists (if possible),
- total collapse,
- coexistence.

At minimum, report separate probabilities for
- parasite extinction \(p\to 0\), and
- “any population below threshold.”

Also decide whether extinction means
- terminal extinction at \(t=T\),
- absorbing hit to zero, or
- sustained sub-threshold occupation over a window.

---

### Major (should be fixed in current revision)

#### M1. The RODE noise is one-sided positive and therefore changes the mean drift, not just the variance.

The RODE uses piecewise-constant noise with
\[
\tilde\eta_i(t)\sim \mathrm{Uniform}[0,\tilde\eta_{\max}],
\]
entering as \(+\tilde\eta_i(t)\tilde u_i\).

This is **not** mean-zero environmental noise.

In particular, for the “non-dissipative” RODE case with \(\tilde\eta_{\max}=0.25\) and \(\tilde\delta=0.1\):
- \(\mathbb E[\tilde\eta_p]=0.125 > \tilde\delta\),
- so the average noise contribution alone can outweigh the death rate for \(\tilde p\).

Thus the RODE does not merely add variability; it adds a positive mean growth bias.

**Why this matters:** many of the paper’s comparisons between RODE and Itô/Stratonovich SDEs are framed as comparisons of stochastic formulation. But the RODE and SDEs are also being driven by **different mean drifts**.

**Required action:** either
- center the RODE noise around zero, or
- explicitly acknowledge that the RODE is a positive-growth random environment model, not a mean-zero noise analog of the SDEs.

---

#### M2. The paper overstates the effect of noise structure on extinction classification.

The abstract says that common vs independent noise structure affects covariance dynamics and coherence but **not** the extinction-probability classification.

This is contradicted by the manuscript’s own stability-boundary summary:
- Itô/common: boundary \(\sigma\approx 1.12\)
- Itô/independent: boundary \(\sigma\approx 0.86\)
- Stratonovich/common: boundary not reached by \(\sigma=2\)
- Stratonovich/independent: boundary \(\sigma\approx 1.01\)

These are not negligible differences. In the Stratonovich case they change the binary classification over a large part of the plotted \(\sigma\)-range.

**Recommended action:** narrow the claim. A defensible version would be something like:

> “At the calibrated baseline noise amplitude used for the trajectory/ensemble comparisons, common versus independent noise does not change the extinction/coexistence class, although it does change covariance structure and can shift the stability boundary at larger amplitudes.”

---

#### M3. Proposition 4 is still too strong: under independent noise, covariance is not generally zero.

The manuscript’s covariance approximation says that under independent noise the cross-driving diffusion term is absent and then effectively sets
\[
\frac{d}{dt}\operatorname{Cov}(f,m)=0,
\]
and similarly for the other cross-covariances.

That is not a valid **full covariance equation** for a nonlinear coupled drift system.

Even when the diffusion cross-term vanishes, the deterministic coupling can generate covariance via terms analogous to
\[
J C + C J^\top,
\]
where \(J\) is the Jacobian of the drift and \(C\) the covariance matrix.

This matters here because all three populations are coupled through the same nonlinear deterministic drift. Independent multiplicative noise does **not** imply zero cross-covariance.

I also checked this numerically by reconstructing the manuscript’s independent-noise Euler–Maruyama model from the appendix and running a small Monte Carlo ensemble: \(\operatorname{Cov}(f,m)\) quickly becomes nonzero (in my test, negative) even under independent noise.

**Recommended action:** relabel Proposition 4 as a statement about the **absence of direct diffusion cross-driving**, not as a full covariance evolution law. Alternatively derive a proper linearized covariance system.

---

#### M4. The use of \(a=0.8\) as “female fraction in bisexual progeny” is not supported by the cited sex-ratio evidence.

The biological assumption in Section 2.1 is that a bisexual male–bisexual female encounter produces a fraction \(a\) of **female offspring** and \(1-a\) of male offspring.

The manuscript then uses field observations that natural populations have fewer than 20% males to motivate \(a\approx 0.8\).

That inference is problematic. The Snelson & Wetherington study reports that in *Poecilia latipinna*:
- sex ratio at birth is very close to 1:1,
- juvenile sex ratio is also near 1:1,
- adult sex ratio is female-biased due largely to differential male mortality.

So adult sex ratio is **not** a direct estimate of offspring sex fraction.

**Consequence:** parameter \(a\) is being interpreted as an offspring-production parameter but calibrated using what appears to be an adult survivorship phenomenon.

**Recommended action:** either
- reinterpret \(a\) as an effective female recruitment fraction after early survival/maturation, or
- choose \(a\) from actual brood/neonate sex-ratio data and separate survivorship from birth sex ratio.

---

#### M5. The manuscript labels \(\sigma_i u_i\,dW_i\) as “independent demographic noise,” but that is not demographic-noise scaling.

Independent Wiener processes do not make the noise “demographic” if the amplitude remains geometric (proportional to \(u_i\)). That scaling is characteristic of environmental/parametric multiplicative noise.

A genuine diffusion approximation to demographic noise in counts typically produces standard deviation scaling like \(\sqrt{u_i}\), not linearly like \(u_i\).

**Why this matters:** the paper claims to compare common environmental noise against independent demographic noise, but what it actually compares is
- common geometric multiplicative noise, versus
- independent geometric multiplicative noise.

That distinction is still scientifically interesting, but it is not the same biological interpretation.

**Recommended action:** rename the cases as
- common multiplicative noise, and
- independent multiplicative noise,
or else change the diffusion scaling if the goal is to model demographic noise.

---

#### M6. The RODE resampling interval is a substantive modeling parameter but is not analyzed as one.

In the RODE solver, the piecewise-constant noise is resampled once per evaluation interval. That means the choice of `n_steps` fixes the noise correlation time.

This is not merely a numerical discretization detail; it is part of the stochastic model itself.

Yet the manuscript provides
- no biological calibration of that timescale,
- no sensitivity analysis with respect to resampling interval, and
- no comparison of how the dissipative/non-dissipative behavior changes when the resampling interval changes.

**Recommended action:** introduce an explicit random-environment correlation timescale parameter and perform a sensitivity analysis.

---

#### M7. Figure 5 does not support the claim of qualitative agreement across all five formulations.

The text says that the timing and character of population transitions are “consistent across formulations.” Figure 5 does not support that claim.

In the plotted single-trajectory comparison:
- the RODE trajectory (gray) shows the parasite population \(p\) growing to roughly **26** in non-dimensional units,
- while the SDE parasite trajectories remain near **0.05–0.1**,
- and the host components behave qualitatively differently as well.

These are not small quantitative differences; they are different qualitative regimes.

**Recommended action:** either
- soften the prose to “single trajectories are not directly comparable and can differ strongly across formulations,” or
- choose a different comparison figure and/or different calibration target.

---

#### M8. Figure 4(b) is mislabeled/interpreted as “noisy coexistence.”

The figure shows the parasite population blowing up far beyond carrying capacity. Because the y-axis is dominated by this blow-up, the host components are visually compressed near zero.

This is not a clear visualization of bounded coexistence. At best it is “runaway growth under threshold-exceeding positive random forcing in the truncated model.”

**Recommended action:** revise the text and caption, and consider replacing Figure 4(b) with either
- a bounded model variant, or
- a normalized plot that makes the biological state clearer.

---

#### M9. The “non-dissipative case” label for \(\tilde\eta_{\max}=0.25\) is too absolute.

The RODE noise is random in time. The condition \(\eta_f+\eta_m+\eta_p>3\) is an **instantaneous** condition.

For \(\tilde\eta_{\max}=0.25\), the system does **not** remain above threshold at every time; rather, its support includes both dissipative and non-dissipative realizations. The current label makes it sound as though the trajectory is always in the non-dissipative regime.

**Better wording:** “threshold-exceeding noise range” or “noise range that permits non-dissipative intervals.”

---

### Moderate

#### O1. The deterministic \(\gamma_{eq}\) presentation remains conceptually muddy.

The equilibrium identity
\[
\gamma_{eq}=\frac{a f^*}{a p^*+f^*}
\]
(or the source version with \(f_0,p_0\)) is not a complete equilibrium solution. It is one algebraic relation among equilibrium quantities.

Plugging the initial values 100 and 10 into that identity makes it look as though the threshold is obtained from the chosen initial condition, which is conceptually wrong.

**Recommended action:** either solve the full equilibrium explicitly or state clearly that this is an equilibrium identity evaluated at the coexistence equilibrium, not at arbitrary initial values.

---

#### O2. The Wong–Zakai discussion is directionally sensible but overextended.

The manuscript repeatedly argues that because habitat connectivity has finite correlation time, the Stratonovich interpretation is physically preferred.

The issue is more subtle:
- Wong–Zakai justifies Stratonovich as the limit of **rapidly varying smooth approximations** to white noise.
- Environmental forcing with correlation times of weeks or months is not automatically well represented by a white-noise Stratonovich SDE; it may instead call for an explicit colored-noise/random-environment model.

**Recommended action:** soften the language. “Stratonovich is often the natural white-noise limit of smooth fast forcing” is safer than “therefore Stratonovich is physically preferred here.”

---

#### O3. The manuscript still uses “reflection boundary” for what is actually projection/clipping.

The code does
\[
 u_i \leftarrow \max(u_i,0).
\]
That is not reflection in the standard stochastic-numerics sense.

**Recommended action:** replace “reflection” with “projection,” “clipping,” or “post-step truncation to maintain nonnegativity.”

---

#### O4. Table 2 overclaims by presenting one calibration as if it applies equally to “All SDE variants.”

Only the Itô/common system is calibrated directly by the binary search described in Section 3.5. The resulting sigma tuple is then reused across the other SDE variants.

That is a modeling choice, but the wording “All SDE variants” suggests that each formulation has been separately calibrated to match the RODE variance, which is not the case.

**Recommended action:** relabel Table 2 accordingly.

---

#### O5. Appendix B.2 convergence verification is much narrower than the prose suggests.

The code appendix checks an Euler–Maruyama \(\Delta t\) refinement for one Itô/common configuration. That is useful, but it is not the same as verifying:
- Heun convergence,
- independent-noise convergence,
- RODE resampling-interval sensitivity, or
- stability-boundary robustness.

**Recommended action:** narrow the prose or expand the convergence study.

---

#### O6. Figure numbering remains out of sync between the main paper and the code appendix.

Main paper:
- Figure 7 = moment equations vs Monte Carlo
- Figure 8 = stability boundary
- Figure 9 = noise structure sensitivity

Appendix `run_all.py` listing:
- Figure 7 = Itô–Stratonovich divergence
- Figure 8 = moment vs Monte Carlo
- Figure 9 = stability boundary
- Figure 10 = noise structure sensitivity

This is a direct reproducibility/traceability problem.

---

## 3. Source-package-specific defects (important for the next agent)

These are issues in the attached source files, regardless of the PDF.

### S1. Missing cite keys in the attached source package

The TeX file cites keys not present in the attached `.bib` files:
- `Buckingham1914`
- `Loyning1996`

This means the attached source package, as provided, is bibliographically incomplete.

### S2. Wrong DOI still present in attached `poecilia_references.bib`

The entry for `Snelson1980` still gives the wrong DOI (`...tb04817.x`) rather than the correct paper DOI (`...tb04819.x`).

### S3. Duplicate placeholder keys remain in `JBGInvasiveSpecies.bib`

The file contains repeated template entries and duplicate keys, including:
- `author:keyword` (multiple times)
- `Hale:Dynamics` (duplicate)
- `GTHT:PFormosa` (duplicate)

This is poor bibliography hygiene and may trigger BibTeX warnings/errors.

### S4. The TeX source cannot be compiled from the uploaded package as-is

The attached `.tex` references external assets that are not included in the upload:
- `poecilia_sde/run_all.py`
- `poecilia_sde/params.py`
- `poecilia_sde/deterministic.py`
- `poecilia_sde/rode.py`
- `poecilia_sde/sde_ito.py`
- `poecilia_sde/sde_stratonovich.py`
- `poecilia_sde/moments.py`
- `poecilia_sde/stability.py`
- `poecilia_sde/figures.py`
- all figure image files under `poecilia_sde/figures/`
- `requirements.txt`

Yet Appendix A claims that the complete implementation is organized and reproducible from `python run_all.py`.

**Action:** the next agent should request or reconstruct the full source bundle before attempting technical edits that depend on recompilation.

---

## 4. Reference-verification notes

### Verified bibliographic items (PDF version)

The following reference facts were checked and are correct in the **PDF**:
- **Hubbs & Hubbs (1932)** discovery paper exists: *Science* 76(1983):628–630; DOI `10.1126/science.76.1983.628`.
- **Avise et al. (1991)** is indeed 1991 (not 1990): *Evolution* 45(6):1530–1533; DOI `10.1111/j.1558-5646.1991.tb02657.x`.
- **Buckingham (1914)** exists: *Physical Review* 4(4):345–376.
- **Løyning & Kirkendall (1996)** bark-beetle paper exists and matches the manuscript’s citation intent.
- **Snelson & Wetherington (1980)** correct article DOI is `10.1111/j.1558-5646.1980.tb04819.x`.

### Reference-use mismatch that affects the biology

Even though the Snelson reference is bibliographically correct in the PDF, the manuscript appears to use it incorrectly: the paper reports near-equal sex ratio at birth and juvenile stages, whereas the manuscript uses adult sex-ratio evidence to motivate \(a\approx 0.8\) as female offspring proportion.

### Low-confidence note (do not act without checking publisher metadata)

I saw conflicting external metadata for the DOI year-code segment of the Heubel–Rankin–Kokko (2009) Oikos paper (`...2008.17024.x` vs `...2009.17024.x`). Many citations use the 2008-coded DOI, but some institutional pages display 2009-coded metadata. I would verify this directly against the publisher DOI metadata before doing a final bibliography cleanup.

---

## 5. Suggested revision plan for the next agent

### Phase 1 — Synchronize artifacts
1. Establish one canonical source tree that reproduces the uploaded PDF exactly.
2. Replace the attached `.bib` files with the bibliography actually used to build the PDF.
3. Remove duplicate template entries from `JBGInvasiveSpecies.bib`.
4. Ensure every cite key in the TeX exists exactly once in the bibliography.
5. Restore the missing `poecilia_sde/` directory and figure assets or convert the appendix to embedded listings/figures that compile from the shared package.

### Phase 2 — Repair the mathematics
1. Replace the displayed \(\partial\dot f/\partial f\) formula with the correct derivative.
2. Rewrite the boundary-dissipativity proof using direct substitution on \(f+m+p=1\).
3. Delete the Lagrange-multiplier / bordered-Hessian material.
4. Ensure all discussion/conclusion language consistently says **boundary** contraction, not global contraction.
5. Decide whether the scalar Lyapunov analysis is purely heuristic/local or whether it is being used to explain Figure 8. If the latter, the extinction event in Figure 8 must be redefined.

### Phase 3 — Repair the modeling and numerics
1. Decide whether the logistic term should remain smooth above carrying capacity or be truncated.
2. If truncation is retained, acknowledge that the simulated model is a different model.
3. Reconsider the one-sided positive RODE forcing. A zero-mean piecewise-constant random environment would make the RODE/SDE comparison far cleaner.
4. Redefine the Monte Carlo outcome classes so that parasite extinction, host extinction, and coexistence are separated.
5. Rework Proposition 4 / covariance language for independent noise.
6. Reassess the use and interpretation of \(a=0.8\).
7. Add sensitivity analysis for the RODE resampling interval.

### Phase 4 — Rebuild the results section
1. Recompute Figure 4 under a bounded model or relabel it honestly as runaway growth.
2. Rewrite the discussion of Figure 5; do not claim qualitative similarity that the plot does not show.
3. Clarify that Table 2 calibration is performed only against Itô/common and then transferred to the other variants.
4. Rewrite the abstract/result (d) so it does not contradict Table 3.

---

## 6. Bottom line

The manuscript contains a promising core idea and the new PDF shows that the authors are already responding to technical criticism. But the current submission still has **three different levels of problem**:

1. **Scientific/mathematical:** the boundary proof needs to be cleaned up, the displayed derivative is wrong, the covariance and stability interpretations are overstated, and the biological meaning of some parameters/noise choices remains unclear.
2. **Numerical/methodological:** the simulated model differs materially from the analyzed model, and some of the headline figures are being overinterpreted.
3. **Production/reproducibility:** the PDF, TeX, and Bib files are not synchronized, and the shared source package is incomplete.

I would not move this manuscript forward without first fixing the **artifact synchronization problem** and then re-running the results from a single canonical source.

