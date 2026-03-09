"""
Core deterministic RHS for the Poecilia host--parasite system (non-dimensional).
State vector u = [f, m, p]:
  f = host females (P. latipinna / P. mexicana)
  m = host males
  p = parasite females (P. formosa)
All stochastic modules import this.
"""
import numpy as np


def gamma_sigmoid(p, gamma_o, gamma_inf, v, r):
    """Population-dependent discrimination factor (Eq. DiscriminationFactor)."""
    arg = np.clip(v * p - r, -500, 500)  # prevent overflow in exp
    return (gamma_o - gamma_inf) / (1 + np.exp(arg)) + gamma_inf


def txc_rhs(t, u, params, gamma_val=None):
    """
    Deterministic RHS of the non-dimensional host--parasite system (Poecilia).
    State: u = [f, m, p]
      f: host females, m: host males, p: parasite females (P. formosa)
    gamma_val: per-encounter acceptance probability for parasite females.
      If None, computed from sigmoid discrimination function using params.
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
