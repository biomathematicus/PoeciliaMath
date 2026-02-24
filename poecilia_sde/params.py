"""
Parameter definitions for the TXC population dynamics model.
All parameter sets as Python dataclasses.

Non-dimensionalization: u = u_tilde/K_tilde, tau = delta_tilde * t
  beta = beta_tilde * K_tilde / delta_tilde = 0.1*300/0.1 = 300
  delta = 1 (by construction)
  v_nondim = v_dim * K_tilde (since gamma uses v*p_tilde = v_nondim*p)
  t_end_nondim = delta_tilde * t_end_dim = 0.1*200 = 20
"""
from dataclasses import dataclass, field
import numpy as np


@dataclass
class BaseParams:
    """Non-dimensional parameters shared by all formulations."""
    beta: float = 300.0        # beta_tilde * K / delta_tilde = 0.1*300/0.1
    delta: float = 1.0         # non-dimensional (= 1 by construction)
    a: float = 0.8             # proportion females in bisexual progeny
    gamma_o: float = 1.0       # initial discrimination factor
    gamma_inf: float = 0.2     # asymptotic discrimination factor
    r: float = 5.0             # sigmoid shift parameter
    v: float = 60.0            # v_dim * K = 0.20 * 300 (fast, coexistence)
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
    n_steps: int = 1000


@dataclass
class SDEParams(BaseParams):
    """SDE-specific parameters.
    Non-dimensional time: t_end = delta_tilde * t_dim = 0.1 * 200 = 20.
    """
    sigma_f: float = 0.1       # default; will be varied for calibration
    sigma_m: float = 0.1
    sigma_p: float = 0.15      # p exposed more (from association data logic)
    dt: float = 0.001          # time step for Euler-Maruyama / Heun
    t_end: float = 20.0        # non-dimensional time = delta_tilde * 200
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
