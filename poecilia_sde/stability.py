"""
Stability boundary computation.

RODE: Algebraic threshold eta_f + eta_m + eta_p < 3 (from Lemma, v1.0 spec).
SDE:  Two approaches:
  1. Analytical: top Lyapunov exponent (where tractable -- scalar subsystem)
  2. Empirical: Monte Carlo extinction probability as function of sigma.
     Stability boundary = sigma at which P(extinction by T) = 0.5.
     Extinction defined as: any population drops below threshold epsilon.
"""
import numpy as np
from sde_ito import monte_carlo_ensemble, euler_maruyama_common, euler_maruyama_independent
from sde_stratonovich import heun_common, heun_independent

EXTINCTION_THRESHOLD = 1e-3   # non-dimensional population floor


def lyapunov_ito_scalar(sigma, delta, beta_eff):
    """
    Top Lyapunov exponent for scalar Ito geometric SDE:
    dp = (beta_eff - delta)*p dt + sigma*p dW
    lambda = beta_eff - delta - 0.5*sigma^2
    Stable (extinction) when lambda < 0 -> sigma > sqrt(2*(beta_eff - delta))
    """
    return beta_eff - delta - 0.5 * sigma**2


def lyapunov_stratonovich_scalar(sigma, delta, beta_eff):
    """
    Top Lyapunov exponent for scalar Stratonovich geometric SDE:
    dp = (beta_eff - delta)*p dt + sigma*p circ dW
    Stratonovich -> Ito conversion: beta_eff - delta + 0.5*sigma^2 -> net drift
    lambda = beta_eff - delta
    NOTE: Stratonovich Lyapunov exponent is INDEPENDENT of sigma for geometric noise.
    This is a key analytical result: Stratonovich noise does not affect scalar stability.
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
    """
    for i in range(len(probs) - 1):
        if probs[i] <= target <= probs[i + 1]:
            frac = (target - probs[i]) / (probs[i + 1] - probs[i])
            sigma_boundary = sigma_range[i] + frac * (sigma_range[i+1] - sigma_range[i])
            return sigma_boundary
    return None


def rode_dissipative_threshold_sigma_equivalent(params):
    """
    RODE threshold: eta_f + eta_m + eta_p = 3 (non-dimensional).
    Compute the eta_max_crit at which sum = 3:
      (2/3 + 2/3 + 1) * eta_max / delta = 7/3 * eta_max / delta = 3
      -> eta_max = 3 * delta / (7/3) = 9*delta/7
    """
    delta = getattr(params, 'delta_tilde', getattr(params, 'delta', 1.0))
    return 9.0 * delta / 7.0


def calibrate_sigma(rode_params=None, sde_params=None, n_rode=200, n_sde=100,
                    seed=42):
    """
    Calibrate SDE sigma values to match RODE variance.
    1. Run RODE ensemble, compute Std[f(T/2)]
    2. Binary search on sigma to match this value
    Returns dict with calibrated sigma values.
    """
    import sys
    from params import RODEParams, SDEParams
    from rode import solve_rode

    if rode_params is None:
        rode_params = RODEParams()
    if sde_params is None:
        sde_params = SDEParams()

    rng = np.random.default_rng(seed)

    # Step 1: RODE ensemble statistics
    rode_seeds = rng.integers(0, 2**31, n_rode)
    rode_finals_f = []
    t_mid_idx = None

    for i, s in enumerate(rode_seeds):
        if (i + 1) % 50 == 0:
            print(f"    RODE path {i+1}/{n_rode}...", flush=True)
        t_arr, sol = solve_rode(rode_params,
                                eta_max=rode_params.eta_max_nondissipative,
                                v=rode_params.v_slow,
                                seed=int(s))
        if t_mid_idx is None:
            t_mid_idx = len(t_arr) // 2
        rode_finals_f.append(sol[0, t_mid_idx])

    rode_std_f = np.std(rode_finals_f)
    rode_mean_f = np.mean(rode_finals_f)

    # Normalize to non-dimensional
    rode_std_f_nd = rode_std_f / rode_params.K_tilde

    print(f"  RODE Std[f(T/2)] = {rode_std_f:.4f} (dimensional)")
    print(f"  RODE Std[f(T/2)] = {rode_std_f_nd:.6f} (non-dimensional)")
    sys.stdout.flush()

    # Step 2: Binary search on sigma for Ito common noise
    sigma_lo, sigma_hi = 0.01, 1.0
    target = rode_std_f_nd

    for it in range(15):  # binary search iterations
        sigma_mid = (sigma_lo + sigma_hi) / 2
        p = sde_params.with_sigma(sigma_mid, sigma_mid, sigma_mid * 1.5)
        # SDE uses non-dimensional time; keep its default t_end
        p.dt = 0.005  # coarser dt for calibration speed

        sde_seeds = rng.integers(0, 2**31, n_sde)
        sde_finals_f = []

        t_arr_sde = np.arange(0, p.t_end + p.dt, p.dt)
        sde_t_mid_idx = len(t_arr_sde) // 2

        for s in sde_seeds:
            _, sol = euler_maruyama_common(p, t_eval=t_arr_sde, seed=int(s))
            sde_finals_f.append(sol[0, sde_t_mid_idx])

        sde_std = np.std(sde_finals_f)
        print(f"    Binary search iter {it+1}: sigma={sigma_mid:.4f}, sde_std={sde_std:.6f}, target={target:.6f}", flush=True)

        if sde_std < target:
            sigma_lo = sigma_mid
        else:
            sigma_hi = sigma_mid

    sigma_cal = (sigma_lo + sigma_hi) / 2

    result = {
        'rode_std_f_T2_dimensional': float(rode_std_f),
        'rode_std_f_T2_nondimensional': float(rode_std_f_nd),
        'rode_mean_f_T2_dimensional': float(rode_mean_f),
        'sigma_f_calibrated': float(sigma_cal),
        'sigma_m_calibrated': float(sigma_cal),
        'sigma_p_calibrated': float(sigma_cal * 1.5),
        'n_rode_paths': n_rode,
        'n_sde_paths_calibration': n_sde,
    }

    print(f"  Calibrated sigma_f = sigma_m = {sigma_cal:.4f}")
    print(f"  Calibrated sigma_p = {sigma_cal * 1.5:.4f}")
    sys.stdout.flush()

    return result
