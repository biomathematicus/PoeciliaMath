# Poecilia formosa RODE/SDE Comparison Codebase

Reproducible Python codebase for comparing stochastic formulations of the
*P. formosa* Trojan X Chromosome (TXC) population dynamics model.

## Five Formulations

1. **RODE** — Random ODE with piecewise-constant parametric noise
2. **Ito SDE / Common noise** — Multiplicative SDE, single Wiener process
3. **Ito SDE / Independent noise** — Multiplicative SDE, per-population Wiener processes
4. **Stratonovich SDE / Common noise** — Same system in Stratonovich form
5. **Stratonovich SDE / Independent noise** — Stratonovich with per-population processes

## Quick Start

```bash
pip install -r requirements.txt
python run_all.py
```

This runs symbolic verification (Phase 1), sigma calibration (Phase 2),
and generates all 10 figures (Phase 3) into `figures/`.

## File Structure

| File | Role |
|------|------|
| `params.py` | Parameter dataclasses |
| `deterministic.py` | Core ODE right-hand side |
| `rode.py` | RODE solver (piecewise-constant noise + solve_ivp) |
| `sde_ito.py` | Ito Euler-Maruyama (common + independent) |
| `sde_stratonovich.py` | Stratonovich Heun method (common + independent) |
| `moments.py` | Closed moment equation ODE system |
| `stability.py` | RODE threshold + SDE Lyapunov/Monte Carlo |
| `verification.py` | SymPy tasks V1-V8 |
| `figures.py` | All 10 figure functions |
| `run_all.py` | Master entry point |
