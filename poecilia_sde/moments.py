"""
Closed moment equations (mean-field closure) for the Poecilia
host--parasite SDE system. Provides ODE system for ensemble means
and second-order moments under Ito and Stratonovich formulations.

Under mean-field closure:
- Ito means: identical to deterministic ODE (noise does not shift the mean)
- Stratonovich means: deterministic ODE + (1/2)*sigma_i^2 * E[u_i] per component
- Variances: driven by sigma^2 * E[u_i^2] ~ sigma^2 * (F_i^2 + Var_i)
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
    Moment equations for Ito SDE with common noise.
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

    # Variance equations (Ito)
    dVF = sigma_f**2 * (F**2 + VF)
    dVM = sigma_m**2 * (M**2 + VM)
    dVP = sigma_p**2 * (P**2 + VP)

    # Covariance equations (common noise: cross-driving term present)
    dCovFM = sigma_f * sigma_m * (F * M + CovFM)
    dCovFP = sigma_f * sigma_p * (F * P + CovFP)
    dCovMP = sigma_m * sigma_p * (M * P + CovMP)

    return [dF, dM, dP, dVF, dVM, dVP, dCovFM, dCovFP, dCovMP]


def moment_rhs_ito_independent(t, y, params):
    """
    Moment equations for Ito SDE with independent noise.
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
    dCovFM = 0.0
    dCovFP = 0.0
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


def moment_rhs_stratonovich_independent(t, y, params):
    """
    Moment equations for Stratonovich SDE with independent noise.
    Stratonovich drift correction present; no cross-driving in covariances.
    """
    F, M, P, VF, VM, VP, CovFM, CovFP, CovMP = y
    sigma_f, sigma_m, sigma_p = params.sigma_f, params.sigma_m, params.sigma_p
    a, beta, delta = params.a, params.beta, params.delta

    gamma = _gamma_sig(P, params)
    L_bar = max(1.0 - F - M - P, 0.0)

    dF = a*beta*L_bar*M*(F - gamma*P) - delta*F + 0.5*sigma_f**2*F
    dM = (1-a)*beta*L_bar*M*(F - gamma*P) - delta*M + 0.5*sigma_m**2*M
    dP = gamma*beta*L_bar*M*P - delta*P + 0.5*sigma_p**2*P

    dVF = sigma_f**2 * (F**2 + VF)
    dVM = sigma_m**2 * (M**2 + VM)
    dVP = sigma_p**2 * (P**2 + VP)

    dCovFM = 0.0
    dCovFP = 0.0
    dCovMP = 0.0

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
