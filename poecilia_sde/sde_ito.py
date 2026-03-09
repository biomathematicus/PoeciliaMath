"""
Ito SDE solver (Euler-Maruyama) for the Poecilia host--parasite system.
Two noise structures: common environmental noise and independent
multiplicative noise (separate Wiener processes per population).
"""
import numpy as np
from deterministic import txc_rhs


def euler_maruyama_common(params, t_eval=None, seed=None):
    """
    Single Ito SDE trajectory, common environmental noise.
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
        u = np.maximum(u, 0.0)              # nonnegative clipping (post-step projection onto nonneg orthant)
        sol[:, i + 1] = u

    return t_arr, sol


def euler_maruyama_independent(params, t_eval=None, seed=None):
    """
    Single Ito SDE trajectory, independent noise per population.
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
