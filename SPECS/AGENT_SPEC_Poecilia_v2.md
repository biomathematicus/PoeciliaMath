# Agent Specification: *P. formosa* RODE/SDE Comparison Manuscript
## Version 2.0 — Supersedes v1.0

---

## Overview and Scientific Thesis

Produce a peer-review-ready scientific manuscript and fully reproducible Python
codebase presenting the population dynamics of *Poecilia formosa* (Trojan X
Chromosome system, TXC) under three stochastic frameworks:

1. **RODE** — Random ODE with piecewise-constant parametric noise (existing work,
   corrected and reframed)
2. **Itô SDE** — Multiplicative stochastic differential equation in Itô form
3. **Stratonovich SDE** — Same system in Stratonovich form, with drift correction

Each framework is developed under **two noise structures**:
- **Common environmental noise** — single Wiener process W(t) with
  population-specific amplitudes (mirrors RODE structure; shared habitat driver)
- **Independent diagonal noise** — separate independent Wiener processes W_f, W_m,
  W_p per population (demographic stochasticity)

This yields **five formulations total** (RODE + 4 SDE variants). The central thesis:
*the qualitative ecological conclusions (discrimination speed governs
extinction/coexistence; environmental noise can stabilize) are robust across
formulations, but the quantitative stability boundary and moment structure are
formulation-dependent.*

**Outputs** (all to `/mnt/user-data/outputs/`):
- `verification_results.json` — Phase 1 SymPy results
- `poecilia_sde/` — complete Python flat-script codebase
- `poecilia_manuscript.tex` — LaTeX manuscript
- `figures/` — all 10 publication-quality figures as PDF + PNG

---

## Phase 1: Symbolic Verification (SymPy)

Run before any LaTeX or figure code. Write results to `verification_results.json`.
All tasks from v1.0 apply unchanged. Summary:

### V1 — Verify γ_eq formula
Derive `gamma_eq = (a*f0)/(a*p0 + f0)` symbolically. Confirm:
- With a=0.8, f0=100, p0=10 → γ_eq ≈ 0.74 ✓
- With a=0.2 → record actual value (documents source error)

### V2 — Compute and verify ∇·F (divergence)
Symbolically compute ∂ḟ/∂f + ∂ṁ/∂m + ∂ṗ/∂p from the non-dimensional RODE system.
Verify the polynomial expression in the Lemma proof. Check β-factoring.

### V3 — Bordered Hessian determinant
Compute |H̄| symbolically for P(f,m,p) = ∇·F with constraint f+m+p=1.
- If |H̄| = 1 (as claimed): PASS
- If |H̄| ≠ 1: record actual value; manuscript uses correct value

### V4 — Interior critical points
Solve ∇P = 0 unconstrained. Verify (0,0,1) is the global maximum.
If interior critical points dominate: flag for proof restructuring.

### V5 — Stochastic threshold arithmetic
Verify:
- Case A: (2/3·0.1 + 2/3·0.1 + 0.1)/0.1 = 7/3 < 3
- Case B: (2/3·0.25 + 2/3·0.25 + 0.25)/0.1 → record exact fraction, confirm > 3

### V6 — NEW: Itô-Stratonovich drift correction (symbolic)
For the non-dimensional system with common geometric noise:
```
df = [aβLm(f-γp) - δf] dt + σ_f f dW
dm = [(1-a)βLm(f-γp) - δm] dt + σ_m m dW
dp = [γβLmp - δp] dt + σ_p p dW
```
The Stratonovich-to-Itô conversion adds correction term +½ σ_i² u_i to each drift.
Symbolically derive the full Itô-equivalent drift for the Stratonovich system:
- f: `a*beta*L*m*(f-gamma*p) - delta*f + (1/2)*sigma_f**2 * f`
- m: `(1-a)*beta*L*m*(f-gamma*p) - delta*m + (1/2)*sigma_m**2 * m`
- p: `gamma*beta*L*m*p - delta*p + (1/2)*sigma_p**2 * p`
Record these expressions. The manuscript Section 3.4 uses them.

### V7 — NEW: Mean-field moment equations (symbolic derivation)
Apply Itô's lemma to derive d𝔼[f]/dt for the Itô common-noise system.

The exact equation is:
```
d𝔼[f]/dt = 𝔼[aβLm(f-γp) - δf]
```
where L = 1 - f - m - p. Expanding:
```
= a*beta * 𝔼[m*f - m*(f+m+p)*f - gamma*p*m + gamma*p*m*(f+m+p)] - delta*𝔼[f]
```
This involves second and third moments. Apply **mean-field closure**:
`𝔼[u_i * u_j] ≈ 𝔼[u_i] * 𝔼[u_j]` for all pairs.

Let F = 𝔼[f], M = 𝔼[m], P = 𝔼[p]. Derive the closed ODE system for (F, M, P):
```
dF/dt = a*beta*(1 - F - M - P)*M*(F - gamma*P) - delta*F
dM/dt = (1-a)*beta*(1 - F - M - P)*M*(F - gamma*P) - delta*M
dP/dt = gamma*beta*(1 - F - M - P)*M*P - delta*P
```
Note: Under mean-field closure, the Itô moment equations for the MEANS are
identical to the deterministic ODE system. Record this result explicitly — it is
a key finding: **mean-field closure predicts that Itô noise does not shift the mean
dynamics; only the variance is affected.**

For the Stratonovich system, the Itô-equivalent drift adds +½σ_i²u_i, giving:
```
dF/dt = a*beta*(1-F-M-P)*M*(F-gamma*P) - delta*F + (1/2)*sigma_f**2 * F
dM/dt = (1-a)*beta*(1-F-M-P)*M*(F-gamma*P) - delta*M + (1/2)*sigma_m**2 * M
dP/dt = gamma*beta*(1-F-M-P)*M*P - delta*P + (1/2)*sigma_p**2 * P
```
Record. **This is the key Itô/Stratonovich difference in the moment equations.**

For the **variance equations**, apply Itô's lemma to d𝔼[f²]:
```
d𝔼[f²]/dt = 2𝔼[f * drift_f] + sigma_f² * 𝔼[f²]   (Itô, common or independent)
```
Under mean-field closure: `𝔼[f²] ≈ F² + Var[f]`. Derive the closed ODE for
Var[f] = 𝔼[f²] - F².

For **covariance** (common noise only): `Cov(f,m)` evolves with a cross-driving term
`+sigma_f*sigma_m * 𝔼[fm] ≈ sigma_f*sigma_m*(FM + Cov(f,m))`.
For **independent noise**: this cross-driving term is absent.
Record both. This is the key common/independent noise difference in the covariance.

Store all derived equations in `verification_results.json` under key `"V7"`.

---

## Phase 2: Python Codebase

### Directory Structure

```
poecilia_sde/
├── README.md
├── requirements.txt
├── run_all.py                  # master: runs all phases, generates all figures
├── params.py                   # all parameter sets as dataclasses
├── verification.py             # SymPy tasks V1–V7
├── deterministic.py            # core ODE right-hand side (shared by all)
├── rode.py                     # RODE solver
├── sde_ito.py                  # Itô Euler-Maruyama (common + independent)
├── sde_stratonovich.py         # Stratonovich Heun method (common + independent)
├── moments.py                  # closed moment equation ODE system
├── stability.py                # RODE threshold + SDE Lyapunov/Monte Carlo
└── figures.py                  # all 10 figure functions
```

### `requirements.txt`
```
numpy>=1.24
scipy>=1.10
matplotlib>=3.7
sympy>=1.12
```
No other dependencies. No seaborn, no pandas, no plotly.

---

### `params.py`

Define all parameter sets as Python dataclasses. Do NOT use raw dicts.

```python
from dataclasses import dataclass, field
import numpy as np

@dataclass
class BaseParams:
    """Non-dimensional parameters shared by all formulations."""
    beta: float = 1.0          # scaled birth rate (beta_tilde * K / delta)
    delta: float = 1.0         # non-dimensional (= 1 by construction)
    a: float = 0.8             # proportion females in bisexual progeny
    gamma_o: float = 1.0       # initial discrimination factor
    gamma_inf: float = 0.2     # asymptotic discrimination factor
    r: float = 5.0             # sigmoid shift parameter
    v: float = 0.20            # discrimination speed (fast = coexistence case)
    # Initial conditions (non-dimensional: u = u_tilde / K)
    f0: float = 100/300        # = 1/3
    m0: float = 100/300
    p0: float = 10/300

@dataclass
class DimensionalParams:
    """Dimensional parameters for RODE simulations."""
    beta_tilde: float = 0.1
    delta_tilde: float = 0.1
    K_tilde: float = 300.0
    a: float = 0.8
    gamma_o: float = 1.0
    gamma_inf: float = 0.2
    r: float = 5.0
    v_slow: float = 0.02       # extinction case
    v_fast: float = 0.20       # coexistence case
    f0: float = 100.0
    m0: float = 100.0
    p0: float = 10.0
    t_end: float = 200.0

@dataclass
class RODEParams(DimensionalParams):
    """RODE-specific stochastic parameters."""
    eta_max_dissipative: float = 0.1    # sum < 3 (dissipative case)
    eta_max_nondissipative: float = 0.25 # sum > 3 (non-dissipative case)
    # eta_f = eta_m = (2/3)*eta, eta_p = eta
    seed: int = 42
    n_steps: int = 5000

@dataclass
class SDEParams(BaseParams):
    """SDE-specific parameters."""
    sigma_f: float = 0.1       # default; will be varied for calibration
    sigma_m: float = 0.1
    sigma_p: float = 0.15      # p exposed more (from association data logic)
    dt: float = 0.001          # time step for Euler-Maruyama / Heun
    t_end: float = 200.0
    n_paths: int = 500         # Monte Carlo ensemble size
    seed: int = 42

    def with_sigma(self, sigma_f, sigma_m, sigma_p):
        """Return a copy with modified sigma values."""
        import copy
        p = copy.copy(self)
        p.sigma_f = sigma_f
        p.sigma_m = sigma_m
        p.sigma_p = sigma_p
        return p
```

---

### `deterministic.py`

```python
"""
Core deterministic RHS for the TXC system (non-dimensional).
All stochastic modules import this.
"""
import numpy as np

def gamma_sigmoid(p, gamma_o, gamma_inf, v, r):
    """Population-dependent discrimination factor (Eq. DiscriminationFactor)."""
    return (gamma_o - gamma_inf) / (1 + np.exp(v * p - r)) + gamma_inf

def txc_rhs(t, u, params, gamma_val=None):
    """
    Deterministic RHS of non-dimensional TXC system.
    u = [f, m, p]
    gamma_val: if provided, use this value; otherwise compute sigmoid from params.
    Returns du/dt as numpy array.
    """
    f, m, p = u
    # Enforce non-negativity
    f = max(f, 0.0)
    m = max(m, 0.0)
    p = max(p, 0.0)

    L = max(1.0 - f - m - p, 0.0)

    if gamma_val is None:
        gamma = gamma_sigmoid(p, params.gamma_o, params.gamma_inf, params.v, params.r)
    else:
        gamma = gamma_val

    beta, a, delta = params.beta, params.a, params.delta

    df = a * beta * L * m * (f - gamma * p) - delta * f
    dm = (1 - a) * beta * L * m * (f - gamma * p) - delta * m
    dp = gamma * beta * L * m * p - delta * p

    return np.array([df, dm, dp])
```

---

### `rode.py`

```python
"""
RODE: Random ODE solver for TXC dimensional system.
Uses scipy solve_ivp (RK45). eta_i(t) are piecewise-constant random variables.
"""
import numpy as np
from scipy.integrate import solve_ivp

def txc_rode_rhs_dimensional(t, u, params, eta_f_t, eta_m_t, eta_p_t):
    """
    Dimensional RODE RHS. eta values are time-varying scalars.
    u = [f_tilde, m_tilde, p_tilde]
    """
    f, m, p = u
    f = max(f, 0.0); m = max(m, 0.0); p = max(p, 0.0)

    L = max(1.0 - (f + m + p) / params.K_tilde, 0.0)
    gamma = (params.gamma_o - params.gamma_inf) / (
        1 + np.exp(params.v * p - params.r)) + params.gamma_inf

    b = params.beta_tilde
    d = params.delta_tilde
    a = params.a

    df = a * b * L * m * (f - gamma * p) - d * f + eta_f_t * f
    dm = (1 - a) * b * L * m * (f - gamma * p) - d * m + eta_m_t * m
    dp = gamma * b * L * m * p - d * p + eta_p_t * p

    return np.array([df, dm, dp])

def solve_rode(params, eta_max, t_eval=None, seed=None):
    """
    Solve one RODE trajectory.
    eta(t) ~ Uniform[0, eta_max], piecewise constant, resampled at each step.
    eta_f = eta_m = (2/3)*eta, eta_p = eta.
    Returns: t_arr, sol (3 x len(t_arr))
    """
    rng = np.random.default_rng(seed)
    t_span = (0.0, params.t_end)
    u0 = np.array([params.f0, params.m0, params.p0])

    if t_eval is None:
        t_eval = np.linspace(0, params.t_end, params.n_steps)

    # Piecewise-constant noise: one value per evaluation interval
    n = len(t_eval)
    eta_vals = rng.uniform(0, eta_max, size=n)
    eta_f_arr = (2/3) * eta_vals
    eta_m_arr = (2/3) * eta_vals
    eta_p_arr = eta_vals

    # Solve segment by segment between t_eval points
    sol = np.zeros((3, n))
    sol[:, 0] = u0
    u = u0.copy()

    for i in range(n - 1):
        t0, t1 = t_eval[i], t_eval[i + 1]
        eta_f = eta_f_arr[i]
        eta_m = eta_m_arr[i]
        eta_p = eta_p_arr[i]

        result = solve_ivp(
            txc_rode_rhs_dimensional,
            (t0, t1),
            u,
            args=(params, eta_f, eta_m, eta_p),
            method='RK45',
            dense_output=False,
        )
        if result.success and result.y[:, -1].min() >= -1e-10:
            u = np.maximum(result.y[:, -1], 0.0)
        else:
            u = np.maximum(u, 0.0)
        sol[:, i + 1] = u

    return t_eval, sol
```

---

### `sde_ito.py`

```python
"""
Itô SDE solver for TXC non-dimensional system.
Implements Euler-Maruyama for both noise structures.

Common noise:  dU = mu(U)dt + sigma_i * U_i * dW      (single W)
Independent:   dU = mu(U)dt + sigma_i * U_i * dW_i    (separate W per population)

Note on positivity: Euler-Maruyama does not guarantee non-negativity.
Apply reflection: U_i = max(U_i, 0) after each step. Document this.
"""
import numpy as np
from deterministic import txc_rhs

def euler_maruyama_common(params, t_eval=None, seed=None):
    """
    Single Itô SDE trajectory, common environmental noise.
    Returns: t_arr, sol (3 x len(t_eval))
    """
    rng = np.random.default_rng(seed)
    dt = params.dt
    t_arr = np.arange(0, params.t_end + dt, dt) if t_eval is None else t_eval
    n = len(t_arr)

    sol = np.zeros((3, n))
    u = np.array([params.f0, params.m0, params.p0])
    sol[:, 0] = u

    sigma = np.array([params.sigma_f, params.sigma_m, params.sigma_p])

    for i in range(n - 1):
        dt_i = t_arr[i + 1] - t_arr[i]
        dW = rng.normal(0, np.sqrt(dt_i))   # single Wiener increment

        drift = txc_rhs(t_arr[i], u, params)
        diffusion = sigma * u * dW           # common: same dW for all

        u = u + drift * dt_i + diffusion
        u = np.maximum(u, 0.0)              # reflection boundary
        sol[:, i + 1] = u

    return t_arr, sol

def euler_maruyama_independent(params, t_eval=None, seed=None):
    """
    Single Itô SDE trajectory, independent noise per population.
    Returns: t_arr, sol (3 x len(t_eval))
    """
    rng = np.random.default_rng(seed)
    dt = params.dt
    t_arr = np.arange(0, params.t_end + dt, dt) if t_eval is None else t_eval
    n = len(t_arr)

    sol = np.zeros((3, n))
    u = np.array([params.f0, params.m0, params.p0])
    sol[:, 0] = u

    sigma = np.array([params.sigma_f, params.sigma_m, params.sigma_p])

    for i in range(n - 1):
        dt_i = t_arr[i + 1] - t_arr[i]
        dW = rng.normal(0, np.sqrt(dt_i), size=3)   # independent increments

        drift = txc_rhs(t_arr[i], u, params)
        diffusion = sigma * u * dW                   # elementwise

        u = u + drift * dt_i + diffusion
        u = np.maximum(u, 0.0)
        sol[:, i + 1] = u

    return t_arr, sol

def monte_carlo_ensemble(solver_fn, params, n_paths=None, seed=None):
    """
    Run n_paths trajectories using solver_fn.
    Returns: t_arr, ensemble (n_paths x 3 x n_t)
    """
    n_paths = n_paths or params.n_paths
    rng = np.random.default_rng(seed)
    seeds = rng.integers(0, 2**31, size=n_paths)

    # Run first path to get shape
    t_arr, sol0 = solver_fn(params, seed=int(seeds[0]))
    ensemble = np.zeros((n_paths, 3, len(t_arr)))
    ensemble[0] = sol0

    for k in range(1, n_paths):
        _, sol = solver_fn(params, seed=int(seeds[k]))
        ensemble[k] = sol

    return t_arr, ensemble

def ensemble_statistics(ensemble):
    """
    Compute mean, 2.5th, and 97.5th percentile across ensemble axis 0.
    Returns: mean (3xn), lower (3xn), upper (3xn)
    """
    mean = np.mean(ensemble, axis=0)
    lower = np.percentile(ensemble, 2.5, axis=0)
    upper = np.percentile(ensemble, 97.5, axis=0)
    return mean, lower, upper
```

---

### `sde_stratonovich.py`

```python
"""
Stratonovich SDE solver for TXC non-dimensional system.
Implements Heun method (explicit 2-stage predictor-corrector).

Heun for Stratonovich:
  U_bar = U_n + g(U_n)*sqrt(dt)*xi     (predictor)
  U_{n+1} = U_n + f(U_n)*dt + (1/2)*(g(U_n) + g(U_bar))*dW   (corrector)
where g(U) = sigma * U (geometric noise) and dW = xi*sqrt(dt).

IMPORTANT: The Heun method converges to the Stratonovich integral, NOT Itô.
Document this distinction clearly in the code.

The Itô-equivalent drift for this Stratonovich system is:
  f_Ito(U) = f_Strat(U) + (1/2) * sigma_i^2 * U_i  (for each component)
This correction must appear in the moment equations (see moments.py).
"""
import numpy as np
from deterministic import txc_rhs

def heun_common(params, t_eval=None, seed=None):
    """
    Single Stratonovich SDE trajectory, common environmental noise.
    """
    rng = np.random.default_rng(seed)
    dt = params.dt
    t_arr = np.arange(0, params.t_end + dt, dt) if t_eval is None else t_eval
    n = len(t_arr)

    sol = np.zeros((3, n))
    u = np.array([params.f0, params.m0, params.p0])
    sol[:, 0] = u

    sigma = np.array([params.sigma_f, params.sigma_m, params.sigma_p])

    for i in range(n - 1):
        dt_i = t_arr[i + 1] - t_arr[i]
        dW = rng.normal(0, np.sqrt(dt_i))

        g_u = sigma * u                          # diffusion at current step
        u_bar = u + g_u * dW                     # predictor (rough)
        u_bar = np.maximum(u_bar, 0.0)

        g_ubar = sigma * u_bar                   # diffusion at predictor
        drift = txc_rhs(t_arr[i], u, params)

        u = u + drift * dt_i + 0.5 * (g_u + g_ubar) * dW   # Heun corrector
        u = np.maximum(u, 0.0)
        sol[:, i + 1] = u

    return t_arr, sol

def heun_independent(params, t_eval=None, seed=None):
    """
    Single Stratonovich SDE trajectory, independent noise per population.
    """
    rng = np.random.default_rng(seed)
    dt = params.dt
    t_arr = np.arange(0, params.t_end + dt, dt) if t_eval is None else t_eval
    n = len(t_arr)

    sol = np.zeros((3, n))
    u = np.array([params.f0, params.m0, params.p0])
    sol[:, 0] = u

    sigma = np.array([params.sigma_f, params.sigma_m, params.sigma_p])

    for i in range(n - 1):
        dt_i = t_arr[i + 1] - t_arr[i]
        dW = rng.normal(0, np.sqrt(dt_i), size=3)

        g_u = sigma * u
        u_bar = u + g_u * dW
        u_bar = np.maximum(u_bar, 0.0)

        g_ubar = sigma * u_bar
        drift = txc_rhs(t_arr[i], u, params)

        u = u + drift * dt_i + 0.5 * (g_u + g_ubar) * dW
        u = np.maximum(u, 0.0)
        sol[:, i + 1] = u

    return t_arr, sol
```

---

### `moments.py`

```python
"""
Closed moment equations for the TXC Itô and Stratonovich SDE systems.
Mean-field closure: E[u_i * u_j] ≈ E[u_i] * E[u_j].

Under mean-field closure:
- Itô means: identical to deterministic ODE (noise does not shift the mean)
- Stratonovich means: deterministic ODE + (1/2)*sigma_i^2 * E[u_i] per component
- Variances: driven by sigma^2 * E[u_i^2] ≈ sigma^2 * (F_i^2 + Var_i)
- Covariances (common noise only): driven by sigma_i*sigma_j * E[u_i*u_j]
- Covariances (independent noise): no cross-driving term

State vector for moment ODE:
  y = [F, M, P,           <- means (indices 0,1,2)
       VF, VM, VP,        <- variances (indices 3,4,5)
       CovFM, CovFP, CovMP]   <- covariances (indices 6,7,8)
"""
import numpy as np
from scipy.integrate import solve_ivp

def moment_rhs_ito_common(t, y, params):
    """
    Moment equations for Itô SDE with common noise.
    Under mean-field closure.
    """
    F, M, P, VF, VM, VP, CovFM, CovFP, CovMP = y
    sigma_f, sigma_m, sigma_p = params.sigma_f, params.sigma_m, params.sigma_p
    a, beta, delta = params.a, params.beta, params.delta

    gamma = _gamma_sig(P, params)
    L_bar = max(1.0 - F - M - P, 0.0)

    # Mean equations (same as deterministic under mean-field)
    dF = a * beta * L_bar * M * (F - gamma * P) - delta * F
    dM = (1 - a) * beta * L_bar * M * (F - gamma * P) - delta * M
    dP = gamma * beta * L_bar * M * P - delta * P

    # Variance equations (Itô)
    # d(Var[f])/dt = 2*E[f * drift_f] - 2*F*dF + sigma_f^2 * E[f^2]
    # Under mean-field: E[f*drift_f] ≈ F*dF (leading order)
    # Net: d(Var[f])/dt ≈ sigma_f^2 * (F^2 + VF)
    dVF = sigma_f**2 * (F**2 + VF)
    dVM = sigma_m**2 * (M**2 + VM)
    dVP = sigma_p**2 * (P**2 + VP)

    # Covariance equations (common noise: cross-driving term present)
    # d(Cov(f,m))/dt = sigma_f*sigma_m * E[fm] ≈ sigma_f*sigma_m*(FM + CovFM)
    dCovFM = sigma_f * sigma_m * (F * M + CovFM)
    dCovFP = sigma_f * sigma_p * (F * P + CovFP)
    dCovMP = sigma_m * sigma_p * (M * P + CovMP)

    return [dF, dM, dP, dVF, dVM, dVP, dCovFM, dCovFP, dCovMP]

def moment_rhs_ito_independent(t, y, params):
    """
    Moment equations for Itô SDE with independent noise.
    Key difference: no cross-driving in covariance equations.
    """
    F, M, P, VF, VM, VP, CovFM, CovFP, CovMP = y
    sigma_f, sigma_m, sigma_p = params.sigma_f, params.sigma_m, params.sigma_p
    a, beta, delta = params.a, params.beta, params.delta

    gamma = _gamma_sig(P, params)
    L_bar = max(1.0 - F - M - P, 0.0)

    dF = a * beta * L_bar * M * (F - gamma * P) - delta * F
    dM = (1 - a) * beta * L_bar * M * (F - gamma * P) - delta * M
    dP = gamma * beta * L_bar * M * P - delta * P

    dVF = sigma_f**2 * (F**2 + VF)
    dVM = sigma_m**2 * (M**2 + VM)
    dVP = sigma_p**2 * (P**2 + VP)

    # Independent noise: no cross-driving; only deterministic coupling
    dCovFM = 0.0   # zero noise cross-driving; deterministic coupling negligible
    dCovFP = 0.0   #   at mean-field level
    dCovMP = 0.0

    return [dF, dM, dP, dVF, dVM, dVP, dCovFM, dCovFP, dCovMP]

def moment_rhs_stratonovich_common(t, y, params):
    """
    Moment equations for Stratonovich SDE with common noise.
    Key difference: means shifted by +(1/2)*sigma_i^2 * F_i.
    """
    F, M, P, VF, VM, VP, CovFM, CovFP, CovMP = y
    sigma_f, sigma_m, sigma_p = params.sigma_f, params.sigma_m, params.sigma_p
    a, beta, delta = params.a, params.beta, params.delta

    gamma = _gamma_sig(P, params)
    L_bar = max(1.0 - F - M - P, 0.0)

    # Stratonovich drift correction: +0.5*sigma^2*F per component
    dF = a*beta*L_bar*M*(F - gamma*P) - delta*F + 0.5*sigma_f**2*F
    dM = (1-a)*beta*L_bar*M*(F - gamma*P) - delta*M + 0.5*sigma_m**2*M
    dP = gamma*beta*L_bar*M*P - delta*P + 0.5*sigma_p**2*P

    dVF = sigma_f**2 * (F**2 + VF)
    dVM = sigma_m**2 * (M**2 + VM)
    dVP = sigma_p**2 * (P**2 + VP)

    dCovFM = sigma_f*sigma_m*(F*M + CovFM)
    dCovFP = sigma_f*sigma_p*(F*P + CovFP)
    dCovMP = sigma_m*sigma_p*(M*P + CovMP)

    return [dF, dM, dP, dVF, dVM, dVP, dCovFM, dCovFP, dCovMP]

def solve_moments(rhs_fn, params, t_eval=None):
    """
    Solve moment equations. Returns t, means (3xn), variances (3xn), covs (3xn).
    """
    F0 = params.f0; M0 = params.m0; P0 = params.p0
    y0 = [F0, M0, P0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # zero initial variance/cov
    t_span = (0, params.t_end)
    if t_eval is None:
        t_eval = np.linspace(0, params.t_end, 2000)

    result = solve_ivp(rhs_fn, t_span, y0, args=(params,),
                       t_eval=t_eval, method='RK45', rtol=1e-8)
    means = result.y[:3, :]      # F, M, P
    variances = result.y[3:6, :] # VF, VM, VP
    covs = result.y[6:, :]       # CovFM, CovFP, CovMP
    return result.t, means, variances, covs

def _gamma_sig(P, params):
    return (params.gamma_o - params.gamma_inf) / (
        1 + np.exp(params.v * P - params.r)) + params.gamma_inf
```

---

### `stability.py`

```python
"""
Stability boundary computation.

RODE: Algebraic threshold eta_f + eta_m + eta_p < 3 (from Lemma, v1.0 spec).
SDE:  Two approaches:
  1. Analytical: top Lyapunov exponent (where tractable — scalar subsystem)
  2. Empirical: Monte Carlo extinction probability as function of sigma.
     Stability boundary = sigma at which P(extinction by T) = 0.5.
     Extinction defined as: any population drops below threshold epsilon.
"""
import numpy as np
from sde_ito import monte_carlo_ensemble, euler_maruyama_common

EXTINCTION_THRESHOLD = 1e-3   # non-dimensional population floor

def lyapunov_ito_scalar(sigma, delta, beta_eff):
    """
    Top Lyapunov exponent for scalar Itô geometric SDE:
    dp = (beta_eff - delta)*p dt + sigma*p dW
    lambda = beta_eff - delta - 0.5*sigma^2
    Stable (extinction) when lambda < 0 → sigma > sqrt(2*(beta_eff - delta))
    """
    return beta_eff - delta - 0.5 * sigma**2

def lyapunov_stratonovich_scalar(sigma, delta, beta_eff):
    """
    Top Lyapunov exponent for scalar Stratonovich geometric SDE:
    dp = (beta_eff - delta)*p dt + sigma*p circ dW
    Stratonovich → Itô conversion: beta_eff - delta + 0.5*sigma^2 → net drift
    lambda = beta_eff - delta
    NOTE: Stratonovich Lyapunov exponent is INDEPENDENT of sigma for geometric noise.
    This is a key analytical result: Stratonovich noise does not affect scalar stability.
    Document this prominently in the manuscript (Section 4.3).
    """
    return beta_eff - delta

def monte_carlo_extinction_probability(solver_fn, params, sigma_range,
                                       n_paths=200, seed=42):
    """
    For each sigma in sigma_range, run n_paths trajectories and compute
    the fraction that go extinct (any population < EXTINCTION_THRESHOLD).
    Returns: sigma_range, extinction_probs
    """
    rng = np.random.default_rng(seed)
    probs = []

    for sigma in sigma_range:
        p = params.with_sigma(sigma, sigma, sigma * 1.5)
        seeds = rng.integers(0, 2**31, n_paths)
        extinct_count = 0

        for s in seeds:
            _, sol = solver_fn(p, seed=int(s))
            if np.any(sol[:, -int(len(sol[0])//4):] < EXTINCTION_THRESHOLD):
                extinct_count += 1

        probs.append(extinct_count / n_paths)

    return np.array(sigma_range), np.array(probs)

def find_stability_boundary(sigma_range, probs, target=0.5):
    """
    Find sigma at which extinction probability crosses target (default 0.5).
    Uses linear interpolation between bracketing points.
    Returns boundary sigma and 95% CI (binomial).
    """
    from scipy.stats import norm
    for i in range(len(probs) - 1):
        if probs[i] <= target <= probs[i + 1]:
            # Linear interpolation
            frac = (target - probs[i]) / (probs[i + 1] - probs[i])
            sigma_boundary = sigma_range[i] + frac * (sigma_range[i+1] - sigma_range[i])
            return sigma_boundary
    return None

def rode_dissipative_threshold_sigma_equivalent(params, eta_max_crit=None):
    """
    RODE threshold: eta_f + eta_m + eta_p = 3 (non-dimensional).
    In dimensional terms: eta_max / delta_tilde = 3/(7/3) * some_factor.
    Compute the eta_max_crit at which sum = 3:
      (2/3 + 2/3 + 1) * eta_max / delta = 7/3 * eta_max / delta = 3
      → eta_max = 3 * delta / (7/3) = 9*delta/7
    Return this value.
    """
    delta = getattr(params, 'delta_tilde', getattr(params, 'delta', 1.0))
    return 9.0 * delta / 7.0
```

---

### `figures.py`

**Color palette (use consistently across ALL figures):**
```python
COLORS = {
    'deterministic': '#1a1a1a',   # near-black
    'rode':          '#2d2d2d',   # dark gray
    'ito_common':    '#1f77b4',   # blue
    'ito_indep':     '#aec7e8',   # light blue
    'strat_common':  '#d62728',   # red
    'strat_indep':   '#ff9896',   # light red
    'f_pop':         '#2ca02c',   # green
    'm_pop':         '#1f77b4',   # blue
    'p_pop':         '#d62728',   # red
}
LINE_STYLES = {
    'mean': '-', 'ci_fill': 0.15, 'moment': '--', 'single_traj': '-'
}
```

**Figure specifications:**

---

**Figure 1 — `fig01_gamma_curves.py`**
*Sigmoid γ discrimination curves (3 speeds)*

- 3 panels in a row OR 3 curves on one plot
- x-axis: population p (non-dimensional), range [0, 1]
- y-axis: γ, range [0, 1.1]
- Curves: v = 0.05, 0.10, 0.20
- Annotate γ_o = 1, γ_∞ = 0.2, r = 5
- Mark the inflection point for each curve

---

**Figure 2 — `fig02_constant_gamma.py`**
*Constant γ: three-panel deterministic cases*

- 3 panels (1×3 layout), each showing f̃, m̃, p̃ vs t (dimensional, t up to ~200)
- Panel A: γ = 0.50 < γ_eq → unisexual extinction
- Panel B: γ = 0.74 = γ_eq → coexistence
- Panel C: γ = 0.90 > γ_eq → bisexual then unisexual extinction
- Parameter a = 0.8 (NOT 0.2). Caption must state this.
- Legend: f̃ (green), m̃ (blue), p̃ (red)
- Mark γ_eq value in subtitle of panel B

---

**Figure 3 — `fig03_sigmoid_gamma.py`**
*Sigmoid γ: slow vs fast discrimination, no stochasticity*

- 2 panels side by side
- Panel A: v = 0.02 (slow) → extinction
- Panel B: v = 0.20 (fast) → coexistence
- Same dimensional axes as Fig 2
- a = 0.8

---

**Figure 4 — `fig04_rode_stochasticity.py`**
*RODE: dissipative vs non-dissipative cases*

- 2 panels side by side
- Panel A: η̃ ∈ [0, 0.1] (dissipative, sum = 7/3 < 3) → extinction with noise
- Panel B: η̃ ∈ [0, 0.25] (non-dissipative, sum = 35/6 > 3) → noisy coexistence
- Include annotation showing sum calculation in each panel
- v = 0.02 for both (slow discrimination)
- a = 0.8

---

**Figure 5 — `fig05_single_trajectory_comparison.py`**
*Single trajectory: all 5 formulations, same seed*

- 3 rows (f, m, p populations), 1 column
- Overlay 5 curves per panel:
  - RODE (dark gray)
  - Itô/common (blue)
  - Itô/independent (light blue)
  - Stratonovich/common (red)
  - Stratonovich/independent (light red)
- Same initial conditions, calibrated σ (see calibration note below)
- Non-dimensional axes
- Include a panel title row
- Legend in top panel only

**Calibration note:** σ values for SDEs must be chosen to produce visually comparable
spread to the RODE non-dissipative case. The spec requires: (1) run RODE ensemble
(n=500) and compute Std[f(T)] at T = t_end/2. (2) Binary search on σ to match this
standard deviation using 100-path SDE ensemble. (3) Record calibrated σ values in
`verification_results.json` under key `"sigma_calibration"`. Use these values for
all SDE figures unless otherwise specified.

---

**Figure 6 — `fig06_ensemble_statistics.py`**
*Ensemble mean ± 95% CI across all 5 formulations*

- 3 rows (f, m, p), layout matching Fig 5
- For each formulation: plot ensemble mean as solid line, 95% CI as shaded band
- Use calibrated σ values
- Axis: non-dimensional t vs population
- This figure is the paper's primary comparison figure — make it clean and publication-ready
- Include a second version (Fig 6b, same data) showing only the MEAN lines without
  CI bands, to make the formulation differences visible without visual clutter

---

**Figure 7 — `fig07_ito_stratonovich_divergence.py`**
*Itô vs Stratonovich mean divergence over time*

- Focus: show how E[f], E[m], E[p] diverge between Itô and Stratonovich
- 3 panels (one per population)
- Each panel: Itô/common mean (blue), Stratonovich/common mean (red),
  deterministic ODE (black dashed)
- Include moment equation solutions (dashed) overlaid on Monte Carlo means
- Two sub-cases: common noise (left column) and independent noise (right column)
  → This becomes a 3×2 figure
- Annotate the Stratonovich correction term +(1/2)σ²E[u_i] in the figure

---

**Figure 8 — `fig08_moment_vs_montecarlo.py`**
*Moment equations vs Monte Carlo: mean and variance*

- 4-panel layout: 2 rows (mean / variance) × 2 columns (f population / p population)
- Mean panels: moment equation solution (dashed) vs MC mean ± 95% CI (solid + band)
- Variance panels: moment equation Var[f](t) (dashed) vs MC empirical Var[f](t) (solid)
- Show both Itô and Stratonovich on same panel (different colors)
- Include a text box in each panel showing the relative error at t_end:
  |moment_mean - MC_mean| / MC_mean × 100%
- This quantifies the closure error explicitly

---

**Figure 9 — `fig09_stability_boundary.py`**
*Stability boundary: RODE threshold vs SDE analog*

- x-axis: noise amplitude (σ for SDE, η̃_max/δ̃ for RODE)
- y-axis: extinction probability (0 to 1)
- Curves: Itô/common (blue), Itô/independent (light blue),
  Stratonovich/common (red), Stratonovich/independent (light red)
- Vertical line: RODE dissipative threshold at η̃_max = 9δ̃/7
- Horizontal dashed line at P(extinction) = 0.5 (stability boundary definition)
- For scalar p-subsystem: overlay analytical Lyapunov exponent result
  (Itô: dashed blue; Stratonovich: dashed red horizontal line showing independence)
- Include 95% CI bands on Monte Carlo curves (Wilson score interval or bootstrap)
- This is the paper's key quantitative comparison figure

---

**Figure 10 — `fig10_noise_structure_sensitivity.py`**
*Noise structure sensitivity: 2×2 panel*

- 2×2 layout:
  - Top-left: Itô common noise, extinction case
  - Top-right: Itô independent noise, same σ
  - Bottom-left: Stratonovich common noise, same σ
  - Bottom-right: Stratonovich independent noise, same σ
- Each panel: ensemble mean ± 95% CI for f̃ and p̃ only (to keep clean)
- Same σ values (non-calibrated; use σ = 0.3 for both to exaggerate differences)
- Caption must clearly state that common noise produces correlated fluctuations
  (f and p move together) while independent noise does not

---

### `run_all.py`

```python
"""
Master script: runs all phases and generates all figures.
Usage: python run_all.py
Output: figures/ directory with all 10 figures as PDF + PNG
"""
import os
import json

def main():
    os.makedirs('figures', exist_ok=True)

    # Phase 1: Symbolic verification
    print("=== Phase 1: Symbolic Verification ===")
    from verification import run_all_verifications
    results = run_all_verifications()
    with open('verification_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print_verification_summary(results)

    # Phase 2: Sigma calibration
    print("\n=== Phase 2: Sigma Calibration ===")
    from stability import calibrate_sigma
    sigma_cal = calibrate_sigma()
    results['sigma_calibration'] = sigma_cal
    with open('verification_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)

    # Phase 3: Generate all figures
    print("\n=== Phase 3: Generating Figures ===")
    import figures
    figures.fig01_gamma_curves()
    figures.fig02_constant_gamma()
    figures.fig03_sigmoid_gamma()
    figures.fig04_rode_stochasticity()
    figures.fig05_single_trajectory_comparison(sigma_cal)
    figures.fig06_ensemble_statistics(sigma_cal)
    figures.fig07_ito_stratonovich_divergence(sigma_cal)
    figures.fig08_moment_vs_montecarlo(sigma_cal)
    figures.fig09_stability_boundary()
    figures.fig10_noise_structure_sensitivity()

    print("\n=== Done. All figures saved to figures/ ===")

def print_verification_summary(results):
    for key, val in results.items():
        if isinstance(val, dict) and 'status' in val:
            print(f"  {key}: {val['status']}")

if __name__ == '__main__':
    main()
```

**Figure saving convention:** every figure function must save both PDF and PNG:
```python
plt.savefig(f'figures/fig{N:02d}_{name}.pdf', dpi=300, bbox_inches='tight')
plt.savefig(f'figures/fig{N:02d}_{name}.png', dpi=300, bbox_inches='tight')
plt.close()
```

---

## Phase 3: LaTeX Manuscript

### Document Class and Preamble

```latex
\documentclass[12pt]{article}
\usepackage{amsmath, amssymb, amsthm}
\usepackage{graphicx}
\usepackage{subfig}
\usepackage{natbib}
\usepackage{hyperref}
\usepackage{geometry}\geometry{margin=1in}
\usepackage{lineno}\linenumbers
\usepackage{booktabs}     % for professional tables
\usepackage{algorithm2e}  % for pseudocode of Euler-Maruyama / Heun
\newtheorem{lemma}{Lemma}
\newtheorem{proposition}{Proposition}
\newtheorem{definition}{Definition}
\newtheorem{remark}{Remark}
```

### Author Block

```latex
\title{Stochastic Formulations of Gynogenetic Population Dynamics:
       A Comparison of Random ODE and Stochastic Differential Equation
       Approaches for \textit{Poecilia formosa}}
\author{Author One\textsuperscript{1} \and Author Two\textsuperscript{2}}
\date{
  \textsuperscript{1}Affiliation One, City, Country \\
  \textsuperscript{2}Affiliation Two, City, Country \\[0.5em]
  \texttt{author@institution.edu}
}
```

---

### Section-by-Section Instructions

#### Abstract (~300 words)

Cover all five points:
1. Biological problem: *P. formosa* as gynogenetic sperm parasite; the
   coexistence/extinction puzzle.
2. Model: three-population ODE with logistic growth, population-dependent
   discrimination, stochastic forcing.
3. Three formulations: RODE, Itô SDE, Stratonovich SDE; two noise structures each.
4. Key results: (a) speed of discrimination governs extinction/coexistence across
   all formulations; (b) the RODE dissipative threshold has no exact SDE analog —
   the Stratonovich scalar Lyapunov exponent is noise-independent, while Itô shifts
   it by −σ²/2; (c) mean-field moment closure predicts Itô noise does not shift
   ensemble means but Stratonovich noise does; (d) common vs independent noise
   structure affects covariance dynamics but not extinction probability.
5. Implication: formulation choice matters quantitatively for stability predictions
   but not qualitatively for the ecological conclusions.

---

#### 1. Introduction

Self-contained. Replace all dissertation cross-references with inline prose.
Include a paragraph on the methodological contribution: why comparing RODE and SDE
formulations matters for ecological modeling broadly (not just TXC). Cite relevant
SDE ecology literature if available from the existing `.bib`; do not add new keys.

End with explicit statement of paper structure (last paragraph of Introduction).

---

#### 2. Biological Model

**2.1 Deterministic Core**
Present the dimensional and non-dimensional systems. a = 0.8 everywhere.
Derive γ_eq using V1 results.

**2.2 Non-Dimensionalization**
Present rescaling. Non-dimensional system.

**2.3 Sexual Discrimination Function**
Sigmoid γ. Figure 1 reference.

---

#### 3. Stochastic Formulations

**3.1 Random ODE (RODE) Formulation**

Define η̃_i(t) ~ Uniform[0, η̃_max], piecewise-constant. State:
- This is a RODE, not an SDE in the Itô/Stratonovich sense
- ode45 / solve_ivp (RK45) is appropriate for RODEs
- η̃_i enters multiplicatively: η̃_i(t)·ũ_i
- Biological interpretation: environmental surplus/deficit; η > δ̃ gives net growth

**3.2 Itô SDE Formulation**

Present both noise structures. Typeset as:

*Common noise:*
$$d\tilde{f} = \mu_f(\tilde{\mathbf{u}})\,dt + \sigma_f \tilde{f}\,dW$$
$$d\tilde{m} = \mu_m(\tilde{\mathbf{u}})\,dt + \sigma_m \tilde{m}\,dW$$
$$d\tilde{p} = \mu_p(\tilde{\mathbf{u}})\,dt + \sigma_p \tilde{p}\,dW$$

*Independent noise:*
$$d\tilde{f} = \mu_f(\tilde{\mathbf{u}})\,dt + \sigma_f \tilde{f}\,dW_f$$
(etc., with independent W_f, W_m, W_p)

State that geometric multiplicative noise ensures near-zero positivity
(reflection applied numerically). Note the Euler-Maruyama solver.

Include pseudocode (algorithm2e environment) for Euler-Maruyama.

**3.3 Stratonovich SDE Formulation**

Present as:
$$d\tilde{f} = \mu_f\,dt + \sigma_f \tilde{f} \circ dW$$

State the Wong-Zakai justification: when noise represents a physical environmental
process with finite (but small) correlation time, the Stratonovich interpretation
is the correct limit of a smooth approximation. For *P. formosa*, seasonal
flooding and connectivity changes have finite correlation time → Stratonovich is
physically preferred.

Include pseudocode for Heun method.

**3.4 Relationship Between Formulations**

Present the Itô-Stratonovich bridge. For each equation:
$$\text{Stratonovich drift} = \text{Itô drift} + \tfrac{1}{2}\sigma_i^2 \tilde{u}_i$$

Use V6 symbolic results. State:
> Under mean-field closure, Itô noise does not shift ensemble means (the additional
> drift is zero in expectation for the mean-field system). Stratonovich noise shifts
> means upward by $+\tfrac{1}{2}\sigma_i^2 \mathbb{E}[\tilde{u}_i]$ — this acts as
> an effective noise-induced birth rate increment.

Present as a **Remark** or **Proposition** (not a Lemma — it follows directly from
the Stratonovich-Itô conversion and V6 results).

**3.5 RODE-to-SDE Correspondence and Calibration**

Present the σ-to-η̃ calibration: because RODE and SDE are not related by a simple
parameter substitution (RODE variance is bounded; SDE variance grows as σ²E[u²]t),
empirical matching is required. Present the calibration procedure:
1. Run RODE ensemble (n=500), compute Std[f(T/2)]
2. Binary search on σ (SDE common noise) to match this value
3. Record calibrated σ values in Table 2

This section makes explicit that direct parameter comparison is impossible, which
is itself a finding that motivates the Monte Carlo stability comparison in Section 5.

---

#### 4. Analysis

**4.1 RODE: Dissipative Stochasticity Lemma**

Scope statement first (RODE / pathwise / Liouville — as per v1.0 spec).
Present Lemma with corrected proof (using V2, V3, V4 results from Phase 1).
Three Definitions (dissipative, non-dissipative, threshold).

**4.2 SDE: Moment Equations**

Present the closed moment ODE system derived in V7 for all four SDE variants.
Organize as:

*Proposition 1 (Mean equations, Itô, any noise structure):*
Under mean-field closure, the ensemble mean (F, M, P) satisfies the deterministic
TXC ODE. Include proof: the Itô integral has zero expectation; mean-field removes
the cross-terms; result follows.

*Proposition 2 (Mean equations, Stratonovich, any noise structure):*
Under mean-field closure, the ensemble mean satisfies the deterministic TXC ODE
augmented by $+\tfrac{1}{2}\sigma_i^2 F_i$ per component. This acts as an
effective noise-induced growth bias.

*Proposition 3 (Variance divergence):*
Under Itô or Stratonovich (both), variances grow as
$d\text{Var}[f]/dt \approx \sigma_f^2(F^2 + \text{Var}[f])$.
This implies exponential growth of variance in the absence of population-level
damping — which is provided by the logistic L term.

*Proposition 4 (Covariance structure):*
Common noise: Cov(f,m) is driven by σ_f·σ_m·(FM + Cov(f,m)).
Independent noise: no such driving term.
Consequence: under common noise, f and p fluctuate coherently, which can
*reduce* the effective competition pressure when p > f (the critical regime).
This is a new mechanistic insight not available from the RODE.

**4.3 Scalar Stability: Lyapunov Exponent Analysis**

Focus on the p-subsystem as the driver of extinction. When p is large and f is
declining, approximate the p equation as:
$$dp = (\gamma\beta L_0 m_0 - \delta)p\,dt + \sigma_p p\,dW$$
where L_0 m_0 is treated as a slowly varying coefficient.
Let β_eff = γβL_0m_0 − δ.

*Itô:* Top Lyapunov exponent λ = β_eff − σ_p²/2.
Stability (extinction of p) requires λ < 0 → σ_p > √(2β_eff).
**Noise promotes stability in the Itô case.**

*Stratonovich:* Top Lyapunov exponent λ = β_eff (independent of σ_p).
**Stratonovich noise does not affect scalar stability.**

Present this as a **Proposition** with proof (direct application of stochastic
stability theory for geometric Brownian motion). This is the paper's key
analytical result differentiating Itô and Stratonovich.

The RODE threshold (η_f + η_m + η_p = 3) has no direct SDE analog because
it is a phase-space contraction condition, not a Lyapunov stability condition.
State this explicitly and argue that the two conditions measure different aspects
of stability: RODE measures global phase-space volume contraction; SDE Lyapunov
measures linearized growth rate of individual trajectories.

---

#### 5. Numerical Results

**5.1 RODE Results** — Figures 2, 3, 4. Reproduce all original results in Python.
Confirm a = 0.8 in all captions.

**5.2 Single Trajectory Comparison** — Figure 5. Note that single trajectories
are insufficient for comparison; they motivate the ensemble analysis.

**5.3 Ensemble Statistics** — Figure 6. Primary comparison. Discuss how
Itô/common and Stratonovich/common diverge in means (as predicted by Proposition 2).
Show that all formulations agree on extinction/coexistence classification at
calibrated σ.

**5.4 Moment Equations vs Monte Carlo** — Figure 8. Report closure error
quantitatively. State whether mean-field closure is acceptable (< 10% error in mean
is a reasonable threshold; state this criterion explicitly).

**5.5 Stability Boundary** — Figure 9. Compare RODE threshold to SDE
Monte Carlo boundary. Show Itô-specific noise-induced stabilization vs
Stratonovich independence. This section contains the paper's quantitative comparison.

**5.6 Noise Structure Sensitivity** — Figure 10. Interpret covariance structure
difference in biological terms.

---

#### 6. Discussion

Structure as four paragraphs:

1. **Speed of discrimination** — Consistent finding across all formulations;
   evolutionary interpretation; connection to prior literature.

2. **Noise-induced stabilization** — Itô vs Stratonovich difference; which
   is more appropriate for *P. formosa*; argue for Stratonovich; implication:
   if Stratonovich is correct, the stabilizing noise effect found in the RODE
   is *not* noise-amplitude-dependent (Proposition on Lyapunov).

3. **Modeling limitations** — Mean-field closure accuracy; RODE vs SDE
   fundamental incommensurability; Fokker-Planck as future work; spatial
   structure (Kokko et al. 2008) not captured.

4. **Implications for the TYC eradication strategy** — What this analysis
   predicts about conditions under which TYC would succeed or fail; role of
   environmental noise in the field.

Retain the Travis personal communication and tank contamination anecdote.

---

#### 7. Conclusion

One paragraph per main finding:
1. Discrimination speed is formulation-robust.
2. Mean dynamics differ between Itô and Stratonovich by the drift correction term.
3. The RODE dissipative threshold is a phase-space concept; the SDE analog is
   the Lyapunov exponent, and they are not equivalent.
4. Common vs. independent noise affects covariance structure and hence the
   coherence of population fluctuations.

---

#### Appendix A — Symbolic Verification

For each V1–V7: brief description, key result typeset in LaTeX, PASS/CORRECTED status.
V3 bordered Hessian: show corrected matrix if needed.
V6–V7: typeset the derived moment equations.

#### Appendix B — Numerical Methods

Algorithm pseudocode (algorithm2e) for:
- RODE solver (piecewise-constant noise + solve_ivp)
- Euler-Maruyama (Itô common + independent)
- Heun method (Stratonovich common + independent)

Note the step-size sensitivity: all SDE results should be verified with dt/2
to confirm numerical convergence (strong order 0.5 for Euler-Maruyama).

Include dt convergence check as a required task in `verification.py` (V8):
Run Euler-Maruyama with dt and dt/2, compute L2 distance between ensemble means.
Report strong convergence factor.

#### Appendix C — Python Codebase

List of files, their roles, and the `run_all.py` entry point.
Note that all figures can be reproduced with `python run_all.py` after installing
`requirements.txt` (`pip install -r requirements.txt`).

---

### Tables

**Table 1** — Parameter values (update of source Table 5.1)
Columns: Parameter, Symbol, Value, Units, Source/Justification
Must include: a=0.8 (Balsano et al. 1989), all β̃, δ̃, K̃, γ_o, γ_∞, r values.

**Table 2** — Calibrated σ values (new)
Columns: SDE Formulation, σ_f, σ_m, σ_p, Target Std[f(T/2)], Achieved Std
This documents the calibration procedure output.

**Table 3** — Stability boundary summary (new)
Columns: Formulation, Noise Structure, RODE equiv., SDE boundary (σ), CI
Last row: Analytical Lyapunov (Itô/Stratonovich scalar result)

---

## Constraints and Guardrails

| Do | Don't |
|---|---|
| Use verified SymPy results for all math | Silently preserve a wrong result |
| Use a = 0.8 everywhere | Use a = 0.2 anywhere |
| Call the noise RODE or SDE/Itô/Stratonovich explicitly | Mix terminology |
| Justify Stratonovich via Wong-Zakai | Assert it without argument |
| State scalar Lyapunov result as a Proposition with proof | Leave it as a remark |
| Compare mean-field closure error quantitatively | Claim closure is exact |
| Use `numpy` random state (default_rng) with explicit seeds | Use `random.random()` |
| Save figures as both PDF and PNG at 300 dpi | Use interactive matplotlib |
| Report dt convergence check (V8) | Assume Euler-Maruyama is converged |
| Replace all chapter cross-references with prose | Leave `\ref{chap:...}` |
| Keep all original citation keys | Add new `.bib` entries |
| Preserve Travis anecdote | Remove empirical support |
| Add new scope statement before Lemma (RODE / pathwise) | Apply Lemma to SDEs |

---

## Execution Order

```
1.  python verification.py          → verification_results.json
2.  Inspect verification summary    → confirm PASS/CORRECTED flags
3.  python run_all.py               → figures/ (all 10 figures)
4.  Write poecilia_manuscript.tex   → using verified results + figures
5.  Verify: grep -c "chap:" manuscript.tex  → must be 0
6.  Verify: grep -c "a = 0.2" manuscript.tex → must be 0 (except Appendix A)
7.  Copy outputs to /mnt/user-data/outputs/
```

---

*End of Specification v2.0*
