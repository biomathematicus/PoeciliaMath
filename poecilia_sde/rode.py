"""
RODE: Random ODE solver for TXC dimensional system.
Uses scipy solve_ivp (RK45). eta_i(t) are piecewise-constant random variables.
"""
import numpy as np
from scipy.integrate import solve_ivp


def txc_rode_rhs_dimensional(t, u, params, eta_f_t, eta_m_t, eta_p_t, v_use=None):
    """
    Dimensional RODE RHS. eta values are time-varying scalars.
    u = [f_tilde, m_tilde, p_tilde]
    v_use: discrimination speed; if None, uses params.v_fast.
    """
    f, m, p = u
    f = max(f, 0.0); m = max(m, 0.0); p = max(p, 0.0)

    L = max(1.0 - (f + m + p) / params.K_tilde, 0.0)
    v_val = v_use if v_use is not None else getattr(params, 'v_fast', 0.20)
    gamma = (params.gamma_o - params.gamma_inf) / (
        1 + np.exp(v_val * p - params.r)) + params.gamma_inf

    b = params.beta_tilde
    d = params.delta_tilde
    a = params.a

    df = a * b * L * m * (f - gamma * p) - d * f + eta_f_t * f
    dm = (1 - a) * b * L * m * (f - gamma * p) - d * m + eta_m_t * m
    dp = gamma * b * L * m * p - d * p + eta_p_t * p

    return np.array([df, dm, dp])


def solve_rode(params, eta_max, v=None, t_eval=None, seed=None):
    """
    Solve one RODE trajectory.
    eta(t) ~ Uniform[0, eta_max], piecewise constant, resampled at each step.
    eta_f = eta_m = (2/3)*eta, eta_p = eta.
    Returns: t_arr, sol (3 x len(t_arr))
    """
    rng = np.random.default_rng(seed)
    u0 = np.array([params.f0, params.m0, params.p0])

    if t_eval is None:
        t_eval = np.linspace(0, params.t_end, params.n_steps)

    # Resolve discrimination speed
    v_use = v if v is not None else getattr(params, 'v_fast', 0.20)

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
            args=(params, eta_f, eta_m, eta_p, v_use),
            method='RK45',
            dense_output=False,
        )
        if result.success and result.y[:, -1].min() >= -1e-10:
            u = np.maximum(result.y[:, -1], 0.0)
        else:
            u = np.maximum(u, 0.0)
        sol[:, i + 1] = u

    return t_eval, sol
