# SPEC 10 — Source Code Updates: Terminology, Docstrings, Pipeline

## Status: READY AFTER SPEC 8 IS COMPLETE
## Target files: ALL Python files in `poecilia_sde/`
## Depends on: SPEC 8 (fig00 function must exist in figures.py)
## Runs independently of: SPEC 9

---

## 1. CONTEXT AND MOTIVATION

The Python codebase uses "TXC" (Trojan X Chromosome) as the system name in
module docstrings, function names, and comments. This is a carryover from an
earlier project. The model is the host–parasite Poecilia formosa system, not
a TXC system. Additionally, variable descriptions in docstrings use
"bisexual/unisexual" language inconsistent with SPEC 8 terminology.

This SPEC updates terminology in docstrings and comments only. No function
signatures, variable names, equation implementations, or algorithmic logic
change.

The model code is correct and validated. Do not alter any numerical logic.

---

## 2. GLOBAL TERMINOLOGY REPLACEMENTS (DOCSTRINGS AND COMMENTS ONLY)

Apply these replacements in `# comments` and `"""docstrings"""` throughout
all `.py` files. Do NOT apply inside string literals that are passed to
matplotlib (axis labels, titles) unless they are also being updated in
Section 3 below.

| Old | New |
|---|---|
| TXC system | host–parasite system |
| TXC | Poecilia |
| bisexual female(s) | host female(s) |
| bisexual male(s) | host male(s) |
| unisexual female(s) | parasite female(s) |
| bisexual population | host population |
| unisexual population | parasite population |
| Trojan X Chromosome | host–parasite gynogenetic |
| txc\_rhs (in docstrings only, NOT the function name) | describe as "Poecilia host–parasite RHS" |

**Critical: do NOT rename the function `txc_rhs` itself.** Only update its
docstring. All callers import `txc_rhs` by name; renaming it breaks the
entire codebase.

---

## 3. FILE-BY-FILE CHANGES

### 3.1 `deterministic.py`

Update module docstring from:
```python
"""
Core deterministic RHS for the TXC system (non-dimensional).
All stochastic modules import this.
"""
```
to:
```python
"""
Core deterministic RHS for the Poecilia host--parasite system (non-dimensional).
State vector u = [f, m, p]:
  f = host females (P. latipinna / P. mexicana)
  m = host males
  p = parasite females (P. formosa)
All stochastic modules import this.
"""
```

Update `txc_rhs` docstring from:
```python
"""
Deterministic RHS of non-dimensional TXC system.
u = [f, m, p]
gamma_val: if provided, use this value; otherwise compute sigmoid from params.
Returns du/dt as numpy array.
"""
```
to:
```python
"""
Deterministic RHS of the non-dimensional host--parasite system (Poecilia).
State: u = [f, m, p]
  f: host females, m: host males, p: parasite females (P. formosa)
gamma_val: per-encounter acceptance probability for parasite females.
  If None, computed from sigmoid discrimination function using params.
Returns du/dt as numpy array.
"""
```

### 3.2 `params.py`

Update module docstring to:
```python
"""
Parameter definitions for the Poecilia host--parasite population dynamics model.
All parameter sets as Python dataclasses.

Non-dimensionalization: u = u_tilde/K_tilde, tau = delta_tilde * t
  beta = beta_tilde * K_tilde / delta_tilde = 0.1*300/0.1 = 300
  delta = 1 (by construction)
  v_nondim = v_dim * K_tilde (since gamma uses v*p_tilde = v_nondim*p)
  t_end_nondim = delta_tilde * t_end_dim = 0.1*200 = 20

Variables:
  f = host females (P. latipinna or P. mexicana)
  m = host males
  p = parasite females (P. formosa)
"""
```

In `BaseParams`, update inline comments:
- `beta`: `# beta_tilde * K / delta_tilde = 0.1*300/0.1`
- `a`: `# proportion host females in host progeny`
- `gamma_o`: `# initial per-encounter acceptance probability (no preference)`
- `gamma_inf`: `# asymptotic per-encounter acceptance probability (strong discrimination)`
- `v`: `# discrimination speed (nondim); v=60 fast (coexistence), v=6 slow (extinction)`
- `f0`, `m0`, `p0`: `# initial conditions: host females, host males, parasite females (nondim)`

In `DimensionalParams`:
- `v_slow`: `# slow discrimination speed: leads to extinction`
- `v_fast`: `# fast discrimination speed: leads to coexistence`

### 3.3 `figures.py`

Update module docstring to:
```python
"""
Publication-quality figure functions for the Poecilia host--parasite manuscript.
Each function saves both PDF and PNG at 300 dpi to figures/.

Fig 00: Extinction ODE dynamics (no noise, slow discrimination)
Fig 01: Sigmoid gamma discrimination curves
Fig 02: Constant gamma -- deterministic trajectories
...
"""
```

Update the `COLORS` dictionary comment:
```python
# Color palette: f_pop=host females, m_pop=host males, p_pop=parasite females
```

Update `_solve_dimensional_det` docstring to:
```python
"""Solve deterministic dimensional system for the host--parasite model."""
```

For each existing `fig0N_*` function, update the one-line docstring to
replace "TXC" or "bisexual/unisexual" language. Examples:
- `fig02_constant_gamma`: update to mention "host and parasite populations"
- `fig03_sigmoid_gamma`: update to mention "host and parasite populations"
- Any figure description mentioning "unisexual" → "parasite female"
- Any figure description mentioning "bisexual" → "host"

### 3.4 `rode.py`

Update module docstring to:
```python
"""
RODE (Random ODE) solver for the Poecilia host--parasite system.
Noise enters as piecewise-constant parametric perturbations resampled
at each time step, applied to the non-dimensional death rate.
"""
```

Update `txc_rode_rhs_dimensional` docstring if present to describe
host females, host males, and parasite females.

### 3.5 `sde_ito.py`

Update module docstring to:
```python
"""
Ito SDE solver (Euler-Maruyama) for the Poecilia host--parasite system.
Two noise structures: common environmental noise and independent
multiplicative noise (separate Wiener processes per population).
"""
```

### 3.6 `sde_stratonovich.py`

Update module docstring to:
```python
"""
Stratonovich SDE solver (Heun method) for the Poecilia host--parasite system.
Two noise structures: common environmental noise and independent
multiplicative noise (separate Wiener processes per population).
"""
```

### 3.7 `moments.py`

Update module docstring to:
```python
"""
Closed moment equations (mean-field closure) for the Poecilia
host--parasite SDE system. Provides ODE system for ensemble means
and second-order moments under Ito and Stratonovich formulations.
"""
```

### 3.8 `stability.py`

Update module docstring to:
```python
"""
Stability analysis for the Poecilia host--parasite system.
Includes: RODE dissipative threshold, SDE scalar Lyapunov exponents
(Ito and Stratonovich), Monte Carlo extinction probability estimation,
and stability boundary search.
"""
```

### 3.9 `verification.py`

Update module docstring to:
```python
"""
Symbolic verification tasks (V1--V8) for the Poecilia host--parasite
system using SymPy. Verifies Ito--Stratonovich conversion, moment
equations, and Lyapunov exponent expressions.
"""
```

### 3.10 `run_all.py`

Ensure `fig00_extinction_ode()` is called in the figure generation
pipeline, before `fig01_gamma_curves()`. If it is not already present
(it was added by SPEC 8), add:

```python
from figures import fig00_extinction_ode
# ... in the figure generation block:
fig00_extinction_ode()
```

Update the module docstring or header comment to read:
```python
"""
Master entry point for the Poecilia host--parasite manuscript figures.
Runs: symbolic verification, sigma calibration, all figures (fig00--fig10).
"""
```

### 3.11 `README.md`

Update the title line from:
```
# Poecilia formosa RODE/SDE Comparison Codebase
```
to:
```
# The Sperm Parasite Paradox — Poecilia Stochastic Modeling Codebase
```

Update the description paragraph to use "host females", "host males",
"parasite females" language.

Update the file table entry for `deterministic.py`:
```
| `deterministic.py` | Core ODE RHS: host females, host males, parasite females |
```

---

## 4. MATPLOTLIB AXIS LABELS AND TITLES

For `fig00_extinction_ode` (added in SPEC 8), the axis labels and title
are already specified in SPEC 8 and should not be altered here.

For all other figures, update any axis label or title string that contains:
- "bisexual" → "host"
- "unisexual" → "parasite"
- "TXC" → "Poecilia"

Do NOT change any mathematical symbols, units, or numerical annotations
in figures.

---

## 5. ACCEPTANCE CRITERIA

After implementation:

1. `python run_all.py` completes without errors.
2. `fig00_extinction_ode.pdf` and `fig00_extinction_ode.png` are present
   in `figures/`.
3. `grep -rn "TXC" poecilia_sde/*.py` returns only occurrences inside
   function names (i.e., `txc_rhs`, `txc_rode_rhs_dimensional`) and
   no occurrences in docstrings or comments.
4. `grep -rn "bisexual\|unisexual" poecilia_sde/*.py` returns zero results.
5. All figure files `fig01` through `fig10` are regenerated successfully
   (no changes to their content expected, only docstring updates to their
   generating functions).
6. `python -c "from deterministic import txc_rhs; print('OK')"` passes
   (function name unchanged).

---

## 6. DO NOT CHANGE

- Any function signature (name, arguments, return type).
- Any variable name inside function bodies (`f`, `m`, `p`, `df`, `dm`, `dp`,
  `beta`, `delta`, `gamma`, `L`, etc.).
- Any numerical constant or parameter value.
- Any algorithmic logic (ODE RHS, solver steps, noise generation).
- The function name `txc_rhs` — only its docstring changes.
- The function name `txc_rode_rhs_dimensional` — only its docstring changes.
- Any `.tex` or `.bib` files (those are handled by SPEC 8 and SPEC 9).
