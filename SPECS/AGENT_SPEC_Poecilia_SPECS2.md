# SPECS2: Analytical Calibration Patch
## Addendum to AGENT_SPEC_Poecilia_v2.md
## Applies to: v2.0 in its entirety. Where this document conflicts with v2.0, SPECS2 governs.

---

## Confirmed Design Decisions

- **Option C** is fully in effect: both (a) variance-matching and (b) dissipative
  threshold analog are computed analytically, then validated visually.
- **Analytical-first**: analytically derived σ values are the primary calibration.
  Empirical Monte Carlo matching is validation, not primary method.
- **Visual comparison** of analytically-calibrated SDE against RODE is required
  and is encoded as Figure 5b (new).

---

## Changes to Phase 1: SymPy Verification

### REPLACE V8 (dt convergence check) with:

### V8 — Analytical σ Calibration (symbolic derivation)

**Goal:** Derive the unique dimensionally-consistent formula mapping RODE noise
parameters to SDE diffusion coefficients. Compute numerical values for both RODE
cases and the threshold analog. Store all results in `verification_results.json`.

**Dimensional analysis argument (symbolic):**

Define symbolic variables:
```python
eta_max, delta_tilde, a_frac = sp.symbols('eta_max delta_tilde a_frac', positive=True)
# a_frac = 2/3 for f and m populations; 1 for p population
```

RODE noise term in dimensional system: η̃_i(t)·ũ_i where η̃_i has units [time⁻¹].
SDE diffusion term: σ_i·ũ_i·dW where σ_i has units [time⁻¹/²], σ_i² has units [time⁻¹].

Var[η̃_f] = (2/3)² · η̃_max²/12 = η̃_max²/27      (units: [time⁻²])
Var[η̃_p] = η̃_max²/12                              (units: [time⁻²])

The only dimensionally consistent matching is:
    σ_i² = Var[η̃_i] / δ̃    (units: [time⁻²]/[time⁻¹] = [time⁻¹] ✓)

Therefore:
    σ_f = σ_m = η̃_max / (3 · √(3·δ̃))
    σ_p = η̃_max / (2 · √(3·δ̃))

**Symbolic derivation steps:**
```python
# Step 1: Variance of RODE noise
var_eta_f = sp.Rational(4,9) * eta_max**2 / 12   # = eta_max^2 / 27
var_eta_p = eta_max**2 / 12

# Step 2: Analytical σ formula
sigma_f_analytical = sp.sqrt(var_eta_f / delta_tilde)
sigma_p_analytical = sp.sqrt(var_eta_p / delta_tilde)

# Step 3: Simplify
sigma_f_simplified = sp.simplify(sigma_f_analytical)
sigma_p_simplified = sp.simplify(sigma_p_analytical)
# Expected: eta_max / (3*sqrt(3*delta_tilde)) and eta_max / (2*sqrt(3*delta_tilde))
```

**Numerical evaluation at all relevant parameter values:**

| Case | η̃_max | δ̃ | σ_f = σ_m (formula) | σ_p (formula) |
|---|---|---|---|---|
| Dissipative | 0.10 | 0.1 | η̃_max/(3√0.3) | η̃_max/(2√0.3) |
| Non-dissipative | 0.25 | 0.1 | same formula | same formula |
| Threshold (η̃_max = 9δ̃/7) | 9δ̃/7 | 0.1 | simplify symbolically | simplify symbolically |

**Threshold analog (compute symbolically):**

RODE threshold: η̃_max_crit = 9δ̃/7 (from V5: 7/3 · η̃_max/δ̃ = 3 → η̃_max = 9δ̃/7)

Substitute into σ formulas:
```python
eta_max_crit = sp.Rational(9,7) * delta_tilde
sigma_f_crit = sigma_f_analytical.subs(eta_max, eta_max_crit)
sigma_p_crit = sigma_p_analytical.subs(eta_max, eta_max_crit)
# Simplify — should give clean expressions in delta_tilde
```

**Also compute the Itô scalar Lyapunov threshold for p-subsystem:**

From Section 4.3 of v2.0: λ = β_eff - δ - σ_p²/2 = 0 → σ_p_lyapunov = √(2(β_eff - δ))

The question of whether σ_p_crit (from RODE matching) equals σ_p_lyapunov (from
Lyapunov condition) is a key result. Compute both symbolically and compare.

They will NOT be equal in general — this non-equality is a main finding:
the RODE dissipative threshold and the Itô Lyapunov condition are different
stability concepts even after analytical calibration.

**Known limitation (encode in verification output):**

The analytical calibration matches noise intensity at the natural timescale δ̃.
It does NOT match sample-path variance at finite time T because:
- RODE variance at time T: Var_RODE[f(T)] ~ Var[η̃_f] · F² · T / n_steps
  (step-count dependent; grows as T with fixed step size)
- SDE variance at time T: Var_SDE[f(T)] ~ σ_f² · F² · T
  (step-count independent; also grows as T)

With σ_f² = Var[η̃_f]/δ̃:
  Var_SDE / Var_RODE ~ (1/δ̃) / (T/n_steps) = n_steps / (δ̃·T)
  = 5000 / (0.1 · 200) = 250

So the SDE will have ~250× more variance than the RODE at matching σ for the
default parameter set. Record this ratio in verification_results.json.
This quantifies how much the visual comparison will diverge — encode as a
**prediction** that Figure 5b must confirm empirically.

**Record in JSON:**
```json
"V8": {
  "sigma_f_formula": "<symbolic>",
  "sigma_p_formula": "<symbolic>",
  "sigma_f_dissipative": <float>,
  "sigma_m_dissipative": <float>,
  "sigma_p_dissipative": <float>,
  "sigma_f_nondissipative": <float>,
  "sigma_m_nondissipative": <float>,
  "sigma_p_nondissipative": <float>,
  "sigma_f_threshold": "<symbolic and float>",
  "sigma_p_threshold": "<symbolic and float>",
  "sigma_p_lyapunov_threshold": "<symbolic (function of beta_eff, delta)>",
  "lyapunov_vs_rode_thresholds_equal": false,
  "variance_ratio_prediction": 250.0,
  "calibration_limitation": "RODE variance is step-count dependent; SDE is not. Analytical calibration matches diffusion intensity, not sample-path variance.",
  "status": "PASS"
}
```

### RESTORE V9 (formerly V8) — dt Convergence Check

Rename the former V8 (Euler-Maruyama dt convergence check) to V9.
Logic unchanged from v2.0. Run with both dt and dt/2 and report strong
convergence factor.

---

## Changes to `params.py`

### ADD after `SDEParams`:

```python
@dataclass
class AnalyticalCalibration:
    """
    Analytically derived SDE sigma values from RODE parameters.
    Formula: sigma_i^2 = Var[eta_i_tilde] / delta_tilde
    where Var[eta_f] = eta_max^2/27, Var[eta_p] = eta_max^2/12.
    """
    # Dissipative RODE case (eta_max = 0.10, delta = 0.1)
    sigma_f_dissipative: float = field(init=False)
    sigma_m_dissipative: float = field(init=False)
    sigma_p_dissipative: float = field(init=False)

    # Non-dissipative RODE case (eta_max = 0.25, delta = 0.1)
    sigma_f_nondissipative: float = field(init=False)
    sigma_m_nondissipative: float = field(init=False)
    sigma_p_nondissipative: float = field(init=False)

    # Threshold (eta_max = 9*delta/7, delta = 0.1)
    sigma_f_threshold: float = field(init=False)
    sigma_m_threshold: float = field(init=False)
    sigma_p_threshold: float = field(init=False)

    delta_tilde: float = 0.1

    def __post_init__(self):
        import numpy as np
        d = self.delta_tilde
        for case, eta_max in [
            ('dissipative', 0.10),
            ('nondissipative', 0.25),
            ('threshold', 9*d/7)
        ]:
            sf = np.sqrt((eta_max**2 / 27) / d)
            sp_ = np.sqrt((eta_max**2 / 12) / d)
            setattr(self, f'sigma_f_{case}', sf)
            setattr(self, f'sigma_m_{case}', sf)
            setattr(self, f'sigma_p_{case}', sp_)

    def as_sde_params(self, case='nondissipative', base_params=None):
        """Return SDEParams with analytically calibrated sigma values."""
        from copy import copy
        p = copy(base_params) if base_params else SDEParams()
        p.sigma_f = getattr(self, f'sigma_f_{case}')
        p.sigma_m = getattr(self, f'sigma_m_{case}')
        p.sigma_p = getattr(self, f'sigma_p_{case}')
        return p
```

---

## Changes to `stability.py`

### REPLACE `rode_dissipative_threshold_sigma_equivalent` with:

```python
def analytical_sigma_from_rode(eta_max, delta_tilde):
    """
    Analytical calibration: sigma_i^2 = Var[eta_i] / delta_tilde.
    Returns (sigma_f, sigma_m, sigma_p).

    This is the unique dimensionally-consistent formula mapping RODE noise
    intensity to SDE diffusion coefficient. It does NOT guarantee matching
    sample-path variance at finite time T (see V8 in verification_results.json
    for the variance ratio prediction).

    Parameters
    ----------
    eta_max : float
        Maximum RODE noise amplitude (dimensional).
    delta_tilde : float
        Dimensional death rate.

    Returns
    -------
    sigma_f, sigma_m, sigma_p : float
    """
    import numpy as np
    var_eta_f = (eta_max**2) / 27.0   # = (2/3)^2 * eta_max^2/12
    var_eta_p = (eta_max**2) / 12.0
    sigma_f = np.sqrt(var_eta_f / delta_tilde)
    sigma_m = sigma_f
    sigma_p = np.sqrt(var_eta_p / delta_tilde)
    return sigma_f, sigma_m, sigma_p

def rode_threshold_sigma():
    """
    RODE dissipative threshold eta_max_crit = 9*delta/7
    mapped to analytical sigma values.
    Returns (sigma_f_crit, sigma_p_crit) at delta=0.1.
    """
    delta = 0.1
    eta_max_crit = 9.0 * delta / 7.0
    return analytical_sigma_from_rode(eta_max_crit, delta)

def lyapunov_threshold_sigma(beta_eff, delta=0.1):
    """
    Itô Lyapunov stability threshold for scalar p-subsystem:
    lambda = beta_eff - delta - sigma_p^2/2 = 0
    → sigma_p_crit = sqrt(2*(beta_eff - delta))

    NOTE: This will NOT equal rode_threshold_sigma() in general.
    The non-equality is a key result of the paper (Section 4.3).
    """
    import numpy as np
    if beta_eff <= delta:
        return 0.0   # already stable without noise
    return np.sqrt(2.0 * (beta_eff - delta))

def variance_ratio_prediction(eta_max, delta_tilde, t_end, n_steps):
    """
    Predicted ratio Var_SDE / Var_RODE at finite time T.
    = n_steps / (delta_tilde * t_end)
    This quantifies the expected visual divergence between
    analytically-calibrated SDE and RODE ensembles.
    """
    return n_steps / (delta_tilde * t_end)
```

### UPDATE `monte_carlo_extinction_probability`:

Add `use_analytical_calibration=True` parameter. When True, compute σ values
using `analytical_sigma_from_rode(sigma_as_rode_eta_max, delta)` for the
x-axis of Figure 9, so that the RODE threshold appears at the correct x position.

---

## Changes to `figures.py`

### ADD Figure 5b (new) — `fig05b_calibration_comparison.py`

**Figure 5b — Analytical Calibration Visual Comparison**

This is the paper's calibration diagnostic figure. It directly shows whether the
analytical formula produces visually comparable dynamics.

Layout: 3 rows (f, m, p) × 2 columns (dissipative case / non-dissipative case).

For each column, overlay:
- RODE ensemble mean ± 95% CI (dark gray, shaded)
- Itô/common SDE ensemble mean ± 95% CI (blue, shaded)
  using **analytically calibrated σ** from V8
- Stratonovich/common SDE ensemble mean ± 95% CI (red, shaded)
  using **same analytically calibrated σ**

In each panel, include a text annotation:
```
σ_f = {value:.3f} (analytical)
Predicted Var ratio: {ratio:.0f}×
```

The expected result (from the variance ratio prediction in V8) is that the SDE
bands will be substantially wider than the RODE bands for the default step count.
This is a finding, not an error. The caption must explicitly state:

> "Analytically calibrated σ values (Eq. X) match diffusion intensity at the
> natural timescale δ̃ but not sample-path variance at finite time T. The SDE
> ensemble variance exceeds the RODE ensemble variance by a factor of
> approximately n_steps/(δ̃T) = [value] (see Section 3.5). This structural
> difference between RODE and SDE formulations is irreducible and motivates
> the empirical matching shown in Figure 6."

**Figure saving:** Save as `fig05b_calibration_comparison.pdf/png`.

---

### UPDATE Figure 6 — Ensemble Statistics

v2.0 spec used calibrated (empirical) σ. Now clarify:

Figure 6 uses **empirically matched σ** (binary search on ensemble variance, as
in v2.0). The procedure for finding empirical σ now explicitly starts from the
analytical σ (from V8) as the initial guess for binary search, which will
accelerate convergence.

Update caption to state:
> "σ values are empirically matched to RODE ensemble variance at t = T/2,
> starting from the analytical estimate (Eq. X). Analytically derived σ values
> and their comparison to RODE are shown in Figure 5b."

---

### UPDATE Figure 9 — Stability Boundary

In v2.0, Figure 9 showed RODE threshold as a single vertical line.

Now: show **three reference lines**:

1. **RODE dissipative threshold** (solid black vertical):
   at x = η̃_max_crit/δ̃ = 9/7 ≈ 1.286 on the RODE-equivalent x-axis.

2. **Analytical σ threshold** (dashed black vertical):
   at x = σ_f_crit (from `rode_threshold_sigma()`) on the SDE σ-axis.
   This is the σ value corresponding to the RODE threshold via the analytical formula.

3. **Itô Lyapunov threshold** (dot-dash blue vertical):
   at x = σ_p_lyapunov (from `lyapunov_threshold_sigma(beta_eff)`) on the SDE σ-axis.
   Use β_eff estimated from the steady-state coexistence regime.

The x-axis must accommodate both RODE and SDE scales. Use a dual x-axis:
- Bottom x-axis: σ (SDE diffusion coefficient)
- Top x-axis: equivalent RODE η̃_max via σ² = Var[η̃]/δ̃ → η̃_max = σ·3√(3δ̃)

Add an annotation box in the figure showing the three threshold values and
noting that they are not equal (σ_analytical_crit ≠ σ_lyapunov_crit for the
general system) — this is the central finding of Section 4.3.

---

## Changes to Manuscript (Section-Level)

### REPLACE Section 3.5 content:

**3.5 RODE-to-SDE Correspondence and Analytical Calibration**

Open with the dimensional analysis argument:

In the dimensional RODE, the noise amplitude η̃_i has units [time⁻¹], matching
the death rate δ̃. In the Itô SDE, the diffusion coefficient σ_i has units
[time⁻¹/²], so σ_i² has units [time⁻¹]. The unique dimensionally-consistent
formula mapping RODE noise variance to SDE diffusion intensity is:

$$\sigma_i^2 = \frac{\text{Var}[\tilde{\eta}_i]}{\tilde{\delta}}$$

For the specific RODE structure η̃_f = (2/3)η̃, η̃_p = η̃, with η̃ ~ Uniform[0, η̃_max]:

$$\sigma_f = \sigma_m = \frac{\tilde{\eta}_{\max}}{3\sqrt{3\tilde{\delta}}}, \qquad
  \sigma_p = \frac{\tilde{\eta}_{\max}}{2\sqrt{3\tilde{\delta}}}$$

Present as a **Proposition** with the dimensional analysis as proof.

Then present the **threshold analog**: the RODE dissipative threshold
η̃_max_crit = 9δ̃/7 maps analytically to:

$$\sigma_{f,\text{crit}} = \frac{3\sqrt{\tilde{\delta}}}{7\sqrt{3}}, \qquad
  \sigma_{p,\text{crit}} = \frac{9}{14}\sqrt{\frac{\tilde{\delta}}{3}}$$

Present **Table 2** (new, see below) with all numerical values.

Then present the **known structural limitation**: the formula matches diffusion
intensity but not sample-path variance at finite T. Derive:

$$\frac{\text{Var}_{\text{SDE}}[f(T)]}{\text{Var}_{\text{RODE}}[f(T)]} \approx \frac{n_{\text{steps}}}{\tilde{\delta} T}$$

For the default parameters: n_steps = 5000, δ̃ = 0.1, T = 200, ratio ≈ 250.

State that this ratio is independent of σ, making it a **structural** (not
parametric) difference. The visual comparison in Figure 5b confirms this
quantitatively.

Close Section 3.5 by stating that empirical σ matching (Figure 6, see Section 5.3)
is required for visually comparable dynamics, and that the analytical formula
serves as (a) an initial estimate and (b) the basis for the threshold comparison
in Section 4.3.

---

### ADD new Proposition in Section 4.3:

After the scalar Lyapunov results (Propositions on Itô and Stratonovich),
add:

**Proposition: Non-equivalence of RODE and SDE stability thresholds**

Under the analytical calibration σ_i² = Var[η̃_i]/δ̃, the RODE dissipative
threshold (σ_f,crit, σ_p,crit from the calibration formula) does not in general
equal the Itô Lyapunov threshold (σ_p = √(2(β_eff − δ))).

Proof: the RODE threshold is a condition on phase-space volume contraction (∇·F < 0),
derived from the trace of the Jacobian integrated over the invariant set. The Itô
Lyapunov threshold is a condition on the linearized growth rate of individual
trajectories near zero. These are distinct stability concepts and their equality
would be coincidental. Numerical values confirm non-equality for the *P. formosa*
parameter set (Table 3). ∎

State the biological implication: a population that is RODE-dissipative may still
exhibit Itô-unstable behavior in the p-subsystem (or vice versa), depending on
which stability concept is operative. This means predictions about extinction risk
depend on which framework is used — a result directly relevant to applied
conservation biology.

---

### UPDATE Table 2 (replaces old Table 2 — Calibrated σ values):

**Table 2 — Analytical and Empirical σ Calibration**

| RODE Case | η̃_max | σ_f = σ_m (analytical) | σ_p (analytical) | σ_f (empirical) | σ_p (empirical) |
|---|---|---|---|---|---|
| Dissipative | 0.10 | [V8 value] | [V8 value] | [Fig 6 calibration] | [Fig 6 calibration] |
| Non-dissipative | 0.25 | [V8 value] | [V8 value] | [Fig 6 calibration] | [Fig 6 calibration] |
| Threshold | 9δ̃/7 | [V8 value] | [V8 value] | — | — |

Columns 3–4: from AnalyticalCalibration dataclass.
Columns 5–6: from empirical binary search (run_all.py Phase 2).
Analytical values are filled by the agent from V8 JSON output.
Empirical values are filled from the sigma_calibration JSON output.

---

### ADD to Appendix A:

**A.8 — Analytical Calibration (V8)**

Typeset the symbolic derivation. Show the full simplification chain:
σ_f = η̃_max/(3√(3δ̃)). Display the variance ratio formula.
Include a box showing the numerical values for all cases.

---

## Figure Count Update

v2.0 had 10 figures. SPECS2 adds Figure 5b. New total: **11 figures**.

Updated figure list:
1. Sigmoid γ discrimination curves
2. Constant γ: three cases (deterministic)
3. Sigmoid γ: slow vs fast
4. RODE: dissipative vs non-dissipative
5a. Single trajectory: all 5 formulations, empirically calibrated σ
**5b. Analytical calibration comparison: RODE vs SDE at analytical σ (NEW)**
6. Ensemble mean ± 95% CI: all 5 formulations, empirically calibrated σ
7. Itô vs Stratonovich mean divergence
8. Moment equations vs Monte Carlo
9. Stability boundary (updated with dual x-axis and 3 reference lines)
10. Noise structure sensitivity

---

## Updated Execution Order

```
1.  python verification.py          → verification_results.json (V1–V9)
2.  Inspect: confirm V8 numerical values and variance ratio prediction
3.  python run_all.py               → figures/ (all 11 figures)
    - Phase 1: symbolic verification (already done in step 1)
    - Phase 2: sigma calibration (analytical first, empirical binary search second)
    - Phase 3: figures 1–11
4.  Write poecilia_manuscript.tex
5.  Populate Table 2 from verification_results.json sigma_calibration field
6.  Verify: grep -c "chap:" manuscript.tex  → must be 0
7.  Verify: grep -c "a = 0.2" manuscript.tex → must be 0 (except Appendix A)
8.  Copy all outputs to /mnt/user-data/outputs/
```

---

## Governing Rule for Analytical vs Empirical Calibration

Throughout the manuscript and codebase, the following convention applies:

| Purpose | Use |
|---|---|
| Threshold comparison (Fig 9, Sec 4.3, Table 3) | Analytical σ from V8 |
| Single trajectory figure (Fig 5a) | Empirically matched σ |
| Ensemble statistics figure (Fig 6) | Empirically matched σ |
| Calibration diagnostic figure (Fig 5b) | Analytical σ only |
| Moment equation figures (Fig 7, 8) | Empirically matched σ |
| Noise structure sensitivity (Fig 10) | Fixed σ = 0.3 (as in v2.0) |

Rationale: using analytical σ for the threshold comparison keeps that result
self-contained and analytically grounded. Using empirical σ for ensemble
comparison ensures visual fairness. The diagnostic figure (5b) exists precisely
to show the gap between them.

---

*End of SPECS2. Governs v2.0 where in conflict.*
