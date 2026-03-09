"""
Stratonovich SDE solver (Heun method) for the Poecilia host--parasite system.
Two noise structures: common environmental noise and independent
multiplicative noise (separate Wiener processes per population).

Heun for Stratonovich:
  U_bar = U_n + g(U_n)*sqrt(dt)*xi     (predictor)
  U_{n+1} = U_n + f(U_n)*dt + (1/2)*(g(U_n) + g(U_bar))*dW   (corrector)
where g(U) = sigma * U (geometric noise) and dW = xi*sqrt(dt).

IMPORTANT: The Heun method converges to the Stratonovich integral, NOT Ito.
Document this distinction clearly in the code.

The Ito-equivalent drift for this Stratonovich system is:
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
