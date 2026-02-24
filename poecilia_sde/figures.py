"""
All 10 publication-quality figure functions for the TXC manuscript.
Each function saves both PDF and PNG at 300 dpi.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from params import BaseParams, DimensionalParams, RODEParams, SDEParams
from deterministic import gamma_sigmoid, txc_rhs
from rode import solve_rode, txc_rode_rhs_dimensional
from sde_ito import (euler_maruyama_common, euler_maruyama_independent,
                     monte_carlo_ensemble, ensemble_statistics)
from sde_stratonovich import heun_common, heun_independent
from moments import (moment_rhs_ito_common, moment_rhs_ito_independent,
                     moment_rhs_stratonovich_common, moment_rhs_stratonovich_independent,
                     solve_moments)
from stability import (lyapunov_ito_scalar, lyapunov_stratonovich_scalar,
                       monte_carlo_extinction_probability, find_stability_boundary,
                       rode_dissipative_threshold_sigma_equivalent)

# ---------- Color palette ----------
COLORS = {
    'deterministic': '#1a1a1a',
    'rode':          '#2d2d2d',
    'ito_common':    '#1f77b4',
    'ito_indep':     '#aec7e8',
    'strat_common':  '#d62728',
    'strat_indep':   '#ff9896',
    'f_pop':         '#2ca02c',
    'm_pop':         '#1f77b4',
    'p_pop':         '#d62728',
}
LINE_STYLES = {
    'mean': '-', 'ci_fill': 0.15, 'moment': '--', 'single_traj': '-'
}

def _save(fig, num, name):
    fig.savefig(f'figures/fig{num:02d}_{name}.pdf', dpi=300, bbox_inches='tight')
    fig.savefig(f'figures/fig{num:02d}_{name}.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved fig{num:02d}_{name}")


def _solve_dimensional_det(params, gamma_val=None, v=None, t_end=200):
    """Solve deterministic dimensional system."""
    def rhs(t, u):
        f, m, p = u
        f = max(f, 0.0); m = max(m, 0.0); p = max(p, 0.0)
        L = max(1.0 - (f + m + p) / params.K_tilde, 0.0)
        if gamma_val is not None:
            g = gamma_val
        else:
            v_use = v if v is not None else params.v_fast
            g = (params.gamma_o - params.gamma_inf) / (
                1 + np.exp(v_use * p - params.r)) + params.gamma_inf
        b = params.beta_tilde; d = params.delta_tilde; a_val = params.a
        df = a_val * b * L * m * (f - g * p) - d * f
        dm = (1 - a_val) * b * L * m * (f - g * p) - d * m
        dp = g * b * L * m * p - d * p
        return [df, dm, dp]

    t_span = (0, t_end)
    t_eval = np.linspace(0, t_end, 5000)
    u0 = [params.f0, params.m0, params.p0]
    result = solve_ivp(rhs, t_span, u0, t_eval=t_eval, method='RK45',
                       rtol=1e-10, atol=1e-12)
    return result.t, result.y


# ===========================================================================
# Figure 1: Sigmoid gamma discrimination curves
# ===========================================================================
def fig01_gamma_curves():
    """Fig 1: Sigmoid gamma discrimination curves (3 speeds)."""
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    p_arr = np.linspace(0, 1, 500)
    gamma_o, gamma_inf, r = 1.0, 0.2, 5.0

    # Use non-dimensional v = v_dim * K. Show dimensional v in labels.
    K = 300.0
    for v_dim, ls in zip([0.05, 0.10, 0.20], ['-', '--', '-.']):
        v_nd = v_dim * K  # non-dimensional v
        gamma_arr = gamma_sigmoid(p_arr, gamma_o, gamma_inf, v_nd, r)
        ax.plot(p_arr, gamma_arr, ls, label=f'$v = {v_dim}$', linewidth=1.5)
        # Inflection point: at v_nd * p = r -> p = r / v_nd
        p_infl = r / v_nd
        if 0 < p_infl < 1:
            g_infl = gamma_sigmoid(p_infl, gamma_o, gamma_inf, v_nd, r)
            ax.plot(p_infl, g_infl, 'ko', markersize=4)

    ax.set_xlabel('Population $p$ (non-dimensional)')
    ax.set_ylabel('$\\gamma$')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.1)
    ax.legend()
    ax.set_title('Male Mate Discrimination Curves')
    ax.annotate(f'$\\gamma_o = {gamma_o}$, $\\gamma_\\infty = {gamma_inf}$, $r = {r}$',
                xy=(0.55, 0.95), xycoords='axes fraction', fontsize=9)
    fig.tight_layout()
    _save(fig, 1, 'gamma_curves')


# ===========================================================================
# Figure 2: Constant gamma, three-panel deterministic
# ===========================================================================
def fig02_constant_gamma():
    """Fig 2: Constant gamma: three-panel deterministic cases."""
    params = DimensionalParams()
    gammas = [0.50, 0.74, 0.90]
    titles = [
        f'(a) $\\gamma = 0.50 < \\gamma_{{eq}}$',
        f'(b) $\\gamma = 0.74 = \\gamma_{{eq}}$',
        f'(c) $\\gamma = 0.90 > \\gamma_{{eq}}$'
    ]

    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
    for ax, g_val, title in zip(axes, gammas, titles):
        t, y = _solve_dimensional_det(params, gamma_val=g_val)
        ax.plot(t, y[0], color=COLORS['f_pop'], label='$\\tilde{f}$')
        ax.plot(t, y[1], color=COLORS['m_pop'], label='$\\tilde{m}$')
        ax.plot(t, y[2], color=COLORS['p_pop'], label='$\\tilde{p}$')
        ax.set_xlabel('Time $t$')
        ax.set_title(title)
        ax.set_xlim(0, 200)
        ax.legend(fontsize=8)

    axes[0].set_ylabel('Population')
    fig.suptitle('Constant $\\gamma$: Deterministic Dynamics ($a = 0.8$)', fontsize=12)
    fig.tight_layout()
    _save(fig, 2, 'constant_gamma')


# ===========================================================================
# Figure 3: Sigmoid gamma, slow vs fast
# ===========================================================================
def fig03_sigmoid_gamma():
    """Fig 3: Sigmoid gamma: slow vs fast discrimination, no stochasticity."""
    params = DimensionalParams()

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    for ax, v_val, title in zip(axes,
                                 [params.v_slow, params.v_fast],
                                 ['(a) $v = 0.02$ (slow) — Extinction',
                                  '(b) $v = 0.20$ (fast) — Coexistence']):
        t, y = _solve_dimensional_det(params, v=v_val)
        ax.plot(t, y[0], color=COLORS['f_pop'], label='$\\tilde{f}$')
        ax.plot(t, y[1], color=COLORS['m_pop'], label='$\\tilde{m}$')
        ax.plot(t, y[2], color=COLORS['p_pop'], label='$\\tilde{p}$')
        ax.set_xlabel('Time $t$')
        ax.set_title(title)
        ax.set_xlim(0, 200)
        ax.legend(fontsize=8)

    axes[0].set_ylabel('Population')
    fig.suptitle('Sigmoid $\\gamma$: Effect of Discrimination Speed ($a = 0.8$)', fontsize=12)
    fig.tight_layout()
    _save(fig, 3, 'sigmoid_gamma')


# ===========================================================================
# Figure 4: RODE stochasticity
# ===========================================================================
def fig04_rode_stochasticity():
    """Fig 4: RODE: dissipative vs non-dissipative cases."""
    params = RODEParams()

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    cases = [
        (params.eta_max_dissipative, '(a) Dissipative: $\\sum\\eta/\\delta = 7/3 < 3$'),
        (params.eta_max_nondissipative, '(b) Non-dissipative: $\\sum\\eta/\\delta = 35/6 > 3$')
    ]

    for ax, (eta_max, title) in zip(axes, cases):
        t, sol = solve_rode(params, eta_max=eta_max, v=params.v_slow, seed=params.seed)
        ax.plot(t, sol[0], color=COLORS['f_pop'], label='$\\tilde{f}$', linewidth=0.8)
        ax.plot(t, sol[1], color=COLORS['m_pop'], label='$\\tilde{m}$', linewidth=0.8)
        ax.plot(t, sol[2], color=COLORS['p_pop'], label='$\\tilde{p}$', linewidth=0.8)
        ax.set_xlabel('Time $t$')
        ax.set_title(title, fontsize=10)
        ax.set_xlim(0, 200)
        ax.legend(fontsize=8)

    axes[0].set_ylabel('Population')
    fig.suptitle('RODE: Effects of Stochasticity ($v = 0.02$, $a = 0.8$)', fontsize=12)
    fig.tight_layout()
    _save(fig, 4, 'rode_stochasticity')


# ===========================================================================
# Figure 5: Single trajectory comparison (all 5 formulations)
# ===========================================================================
def fig05_single_trajectory_comparison(sigma_cal=None):
    """Fig 5: Single trajectory: all 5 formulations, same seed.
    All plotted in non-dimensional units (populations / K, time * delta_tilde).
    """
    rode_params = RODEParams()
    sde_params = SDEParams()
    if sigma_cal:
        sde_params = sde_params.with_sigma(
            sigma_cal.get('sigma_f_calibrated', 0.1),
            sigma_cal.get('sigma_m_calibrated', 0.1),
            sigma_cal.get('sigma_p_calibrated', 0.15))

    seed = 42
    # RODE (dimensional)
    t_rode, sol_rode = solve_rode(rode_params, eta_max=rode_params.eta_max_nondissipative,
                                  v=rode_params.v_slow, seed=seed)
    # Convert RODE to non-dimensional: u_nd = u/K, t_nd = delta_tilde * t
    t_rode_nd = t_rode * rode_params.delta_tilde
    sol_rode_nd = sol_rode / rode_params.K_tilde

    # SDE trajectories (already non-dimensional)
    t_ito_c, sol_ito_c = euler_maruyama_common(sde_params, seed=seed)
    t_ito_i, sol_ito_i = euler_maruyama_independent(sde_params, seed=seed)
    t_str_c, sol_str_c = heun_common(sde_params, seed=seed)
    t_str_i, sol_str_i = heun_independent(sde_params, seed=seed)

    pop_labels = ['$f$ (bisexual females)', '$m$ (males)', '$p$ (unisexual females)']
    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    for row, (pop_label, pop_idx) in enumerate(zip(pop_labels, range(3))):
        ax = axes[row]
        step = max(1, len(t_rode_nd) // 2000)
        ax.plot(t_rode_nd[::step], sol_rode_nd[pop_idx, ::step],
                color=COLORS['rode'], label='RODE', linewidth=0.8, alpha=0.8)
        step_sde = max(1, len(t_ito_c) // 2000)
        ax.plot(t_ito_c[::step_sde], sol_ito_c[pop_idx, ::step_sde],
                color=COLORS['ito_common'], label='Ito/common', linewidth=0.8, alpha=0.8)
        ax.plot(t_ito_i[::step_sde], sol_ito_i[pop_idx, ::step_sde],
                color=COLORS['ito_indep'], label='Ito/indep', linewidth=0.8, alpha=0.8)
        ax.plot(t_str_c[::step_sde], sol_str_c[pop_idx, ::step_sde],
                color=COLORS['strat_common'], label='Strat/common', linewidth=0.8, alpha=0.8)
        ax.plot(t_str_i[::step_sde], sol_str_i[pop_idx, ::step_sde],
                color=COLORS['strat_indep'], label='Strat/indep', linewidth=0.8, alpha=0.8)
        ax.set_ylabel(pop_label)
        if row == 0:
            ax.legend(fontsize=7, ncol=5, loc='upper right')

    axes[-1].set_xlabel('Non-dimensional time $\\tau$')
    fig.suptitle('Single Trajectory Comparison: All 5 Formulations', fontsize=12)
    fig.tight_layout()
    _save(fig, 5, 'single_trajectory_comparison')


# ===========================================================================
# Figure 6: Ensemble statistics
# ===========================================================================
def fig06_ensemble_statistics(sigma_cal=None):
    """Fig 6: Ensemble mean +/- 95% CI across all 5 formulations."""
    sde_params = SDEParams()
    sde_params.n_paths = 500
    sde_params.dt = 0.01  # slightly coarser for ensemble speed
    if sigma_cal:
        sde_params = sde_params.with_sigma(
            sigma_cal.get('sigma_f_calibrated', 0.1),
            sigma_cal.get('sigma_m_calibrated', 0.1),
            sigma_cal.get('sigma_p_calibrated', 0.15))

    solvers = [
        (euler_maruyama_common, 'Ito/common', COLORS['ito_common']),
        (euler_maruyama_independent, 'Ito/indep', COLORS['ito_indep']),
        (heun_common, 'Strat/common', COLORS['strat_common']),
        (heun_independent, 'Strat/indep', COLORS['strat_indep']),
    ]

    pop_labels = ['$f$', '$m$', '$p$']

    # Run all ensembles once and cache results
    cached = []
    for solver_fn, label, color in solvers:
        print(f"    Running ensemble for {label}...", flush=True)
        t_arr, ens = monte_carlo_ensemble(solver_fn, sde_params, n_paths=200, seed=42)
        mean, lower, upper = ensemble_statistics(ens)
        cached.append((t_arr, mean, lower, upper, label, color))

    # --- Fig 6a: with CI bands ---
    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    for t_arr, mean, lower, upper, label, color in cached:
        step = max(1, len(t_arr) // 2000)
        for row in range(3):
            ax = axes[row]
            ax.plot(t_arr[::step], mean[row, ::step], color=color,
                    label=label, linewidth=1.2)
            ax.fill_between(t_arr[::step], lower[row, ::step], upper[row, ::step],
                            color=color, alpha=LINE_STYLES['ci_fill'])
    for row in range(3):
        axes[row].set_ylabel(pop_labels[row])
        if row == 0:
            axes[row].legend(fontsize=7, ncol=4, loc='upper right')
    axes[-1].set_xlabel('Time $t$')
    fig.suptitle('Ensemble Mean $\\pm$ 95% CI: All SDE Formulations', fontsize=12)
    fig.tight_layout()
    _save(fig, 6, 'ensemble_statistics')

    # --- Fig 6b: means only ---
    fig2, axes2 = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    for t_arr, mean, lower, upper, label, color in cached:
        step = max(1, len(t_arr) // 2000)
        for row in range(3):
            axes2[row].plot(t_arr[::step], mean[row, ::step], color=color,
                            label=label, linewidth=1.5)
    for row in range(3):
        axes2[row].set_ylabel(pop_labels[row])
        if row == 0:
            axes2[row].legend(fontsize=7, ncol=4, loc='upper right')
    axes2[-1].set_xlabel('Time $t$')
    fig2.suptitle('Ensemble Means Only: All SDE Formulations', fontsize=12)
    fig2.tight_layout()
    _save(fig2, 6, 'ensemble_means_only')


# ===========================================================================
# Figure 7: Ito vs Stratonovich divergence
# ===========================================================================
def fig07_ito_stratonovich_divergence(sigma_cal=None):
    """Fig 7: Ito vs Stratonovich mean divergence over time (3x2 grid)."""
    sde_params = SDEParams()
    sde_params.dt = 0.01
    if sigma_cal:
        sde_params = sde_params.with_sigma(
            sigma_cal.get('sigma_f_calibrated', 0.1),
            sigma_cal.get('sigma_m_calibrated', 0.1),
            sigma_cal.get('sigma_p_calibrated', 0.15))

    # Deterministic solution
    det_params = BaseParams()
    t_det = np.linspace(0, sde_params.t_end, 2000)
    det_result = solve_ivp(lambda t, u: txc_rhs(t, u, det_params),
                           (0, sde_params.t_end),
                           [det_params.f0, det_params.m0, det_params.p0],
                           t_eval=t_det, method='RK45', rtol=1e-10)

    # Moment equation solutions
    t_mom_ic, means_ic, _, _ = solve_moments(moment_rhs_ito_common, sde_params)
    t_mom_sc, means_sc, _, _ = solve_moments(moment_rhs_stratonovich_common, sde_params)
    t_mom_ii, means_ii, _, _ = solve_moments(moment_rhs_ito_independent, sde_params)
    t_mom_si, means_si, _, _ = solve_moments(moment_rhs_stratonovich_independent, sde_params)

    # MC ensembles
    n_mc = 200
    print("    Running Ito/common ensemble...")
    t_ic, ens_ic = monte_carlo_ensemble(euler_maruyama_common, sde_params, n_paths=n_mc, seed=42)
    print("    Running Strat/common ensemble...")
    t_sc, ens_sc = monte_carlo_ensemble(heun_common, sde_params, n_paths=n_mc, seed=42)
    print("    Running Ito/indep ensemble...")
    t_ii, ens_ii = monte_carlo_ensemble(euler_maruyama_independent, sde_params, n_paths=n_mc, seed=42)
    print("    Running Strat/indep ensemble...")
    t_si, ens_si = monte_carlo_ensemble(heun_independent, sde_params, n_paths=n_mc, seed=42)

    mean_ic, _, _ = ensemble_statistics(ens_ic)
    mean_sc, _, _ = ensemble_statistics(ens_sc)
    mean_ii, _, _ = ensemble_statistics(ens_ii)
    mean_si, _, _ = ensemble_statistics(ens_si)

    pop_labels = ['$E[f]$', '$E[m]$', '$E[p]$']
    fig, axes = plt.subplots(3, 2, figsize=(12, 10), sharex=True)

    step_mc = max(1, len(t_ic) // 1000)
    for row in range(3):
        # Common noise (left)
        ax = axes[row, 0]
        ax.plot(det_result.t, det_result.y[row], COLORS['deterministic'],
                ls='--', label='Deterministic', linewidth=1)
        ax.plot(t_ic[::step_mc], mean_ic[row, ::step_mc],
                COLORS['ito_common'], label='Ito MC', linewidth=1)
        ax.plot(t_sc[::step_mc], mean_sc[row, ::step_mc],
                COLORS['strat_common'], label='Strat MC', linewidth=1)
        ax.plot(t_mom_ic, means_ic[row], COLORS['ito_common'],
                ls='--', label='Ito moment', linewidth=0.8, alpha=0.7)
        ax.plot(t_mom_sc, means_sc[row], COLORS['strat_common'],
                ls='--', label='Strat moment', linewidth=0.8, alpha=0.7)
        ax.set_ylabel(pop_labels[row])
        if row == 0:
            ax.set_title('Common Noise')
            ax.legend(fontsize=6, ncol=3)

        # Independent noise (right)
        ax = axes[row, 1]
        ax.plot(det_result.t, det_result.y[row], COLORS['deterministic'],
                ls='--', label='Deterministic', linewidth=1)
        ax.plot(t_ii[::step_mc], mean_ii[row, ::step_mc],
                COLORS['ito_indep'], label='Ito MC', linewidth=1)
        ax.plot(t_si[::step_mc], mean_si[row, ::step_mc],
                COLORS['strat_indep'], label='Strat MC', linewidth=1)
        ax.plot(t_mom_ii, means_ii[row], COLORS['ito_indep'],
                ls='--', label='Ito moment', linewidth=0.8, alpha=0.7)
        ax.plot(t_mom_si, means_si[row], COLORS['strat_indep'],
                ls='--', label='Strat moment', linewidth=0.8, alpha=0.7)
        if row == 0:
            ax.set_title('Independent Noise')
            ax.legend(fontsize=6, ncol=3)

    axes[-1, 0].set_xlabel('Time $t$')
    axes[-1, 1].set_xlabel('Time $t$')
    fig.suptitle('Ito vs Stratonovich Mean Divergence', fontsize=12)
    fig.tight_layout()
    _save(fig, 7, 'ito_stratonovich_divergence')


# ===========================================================================
# Figure 8: Moment equations vs Monte Carlo
# ===========================================================================
def fig08_moment_vs_montecarlo(sigma_cal=None):
    """Fig 8: Moment equations vs Monte Carlo: mean and variance."""
    sde_params = SDEParams()
    sde_params.dt = 0.01
    if sigma_cal:
        sde_params = sde_params.with_sigma(
            sigma_cal.get('sigma_f_calibrated', 0.1),
            sigma_cal.get('sigma_m_calibrated', 0.1),
            sigma_cal.get('sigma_p_calibrated', 0.15))

    n_mc = 300
    # Ito common
    t_mom_ic, means_ic, vars_ic, _ = solve_moments(moment_rhs_ito_common, sde_params)
    t_ic, ens_ic = monte_carlo_ensemble(euler_maruyama_common, sde_params, n_paths=n_mc, seed=42)
    mc_mean_ic = np.mean(ens_ic, axis=0)
    mc_var_ic = np.var(ens_ic, axis=0)

    # Stratonovich common
    t_mom_sc, means_sc, vars_sc, _ = solve_moments(moment_rhs_stratonovich_common, sde_params)
    t_sc, ens_sc = monte_carlo_ensemble(heun_common, sde_params, n_paths=n_mc, seed=42)
    mc_mean_sc = np.mean(ens_sc, axis=0)
    mc_var_sc = np.var(ens_sc, axis=0)

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    step_mc = max(1, len(t_ic) // 1000)

    # Top row: means (f and p)
    for col, pop_idx, pop_name in [(0, 0, '$f$'), (1, 2, '$p$')]:
        ax = axes[0, col]
        ax.set_title(f'Mean {pop_name}')
        ax.plot(t_ic[::step_mc], mc_mean_ic[pop_idx, ::step_mc],
                COLORS['ito_common'], label='Ito MC', linewidth=1)
        ax.plot(t_mom_ic, means_ic[pop_idx], COLORS['ito_common'],
                ls='--', label='Ito moment', linewidth=1)
        ax.plot(t_sc[::step_mc], mc_mean_sc[pop_idx, ::step_mc],
                COLORS['strat_common'], label='Strat MC', linewidth=1)
        ax.plot(t_mom_sc, means_sc[pop_idx], COLORS['strat_common'],
                ls='--', label='Strat moment', linewidth=1)
        ax.legend(fontsize=7)
        ax.set_xlabel('Time $t$')

        # Relative error annotation
        from scipy.interpolate import interp1d
        mc_interp = interp1d(t_ic, mc_mean_ic[pop_idx], fill_value='extrapolate')
        mc_val = mc_interp(t_mom_ic[-1])
        mom_val = means_ic[pop_idx, -1]
        if abs(mc_val) > 1e-10:
            rel_err = abs(mom_val - mc_val) / abs(mc_val) * 100
            ax.text(0.02, 0.02, f'Ito err: {rel_err:.1f}%',
                    transform=ax.transAxes, fontsize=7,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Bottom row: variances (f and p)
    for col, pop_idx, pop_name in [(0, 0, '$f$'), (1, 2, '$p$')]:
        ax = axes[1, col]
        ax.set_title(f'Var[{pop_name}]')
        ax.plot(t_ic[::step_mc], mc_var_ic[pop_idx, ::step_mc],
                COLORS['ito_common'], label='Ito MC', linewidth=1)
        ax.plot(t_mom_ic, vars_ic[pop_idx], COLORS['ito_common'],
                ls='--', label='Ito moment', linewidth=1)
        ax.plot(t_sc[::step_mc], mc_var_sc[pop_idx, ::step_mc],
                COLORS['strat_common'], label='Strat MC', linewidth=1)
        ax.plot(t_mom_sc, vars_sc[pop_idx], COLORS['strat_common'],
                ls='--', label='Strat moment', linewidth=1)
        ax.legend(fontsize=7)
        ax.set_xlabel('Time $t$')

    fig.suptitle('Moment Equations vs Monte Carlo', fontsize=12)
    fig.tight_layout()
    _save(fig, 8, 'moment_vs_montecarlo')


# ===========================================================================
# Figure 9: Stability boundary
# ===========================================================================
def fig09_stability_boundary():
    """Fig 9: Stability boundary: RODE threshold vs SDE analog."""
    sde_params = SDEParams()
    sde_params.dt = 0.005
    sde_params.t_end = 10.0  # non-dimensional T/2 for stability assessment

    sigma_range = np.linspace(0.2, 2.0, 12)

    print("    Computing extinction probabilities (Ito/common)...", flush=True)
    _, probs_ic = monte_carlo_extinction_probability(
        euler_maruyama_common, sde_params, sigma_range, n_paths=100, seed=42)

    print("    Computing extinction probabilities (Ito/indep)...", flush=True)
    _, probs_ii = monte_carlo_extinction_probability(
        euler_maruyama_independent, sde_params, sigma_range, n_paths=100, seed=42)

    print("    Computing extinction probabilities (Strat/common)...", flush=True)
    _, probs_sc = monte_carlo_extinction_probability(
        heun_common, sde_params, sigma_range, n_paths=100, seed=42)

    print("    Computing extinction probabilities (Strat/indep)...", flush=True)
    _, probs_si = monte_carlo_extinction_probability(
        heun_independent, sde_params, sigma_range, n_paths=100, seed=42)

    # RODE threshold
    rode_params = RODEParams()
    rode_threshold = rode_dissipative_threshold_sigma_equivalent(rode_params)

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))

    ax.plot(sigma_range, probs_ic, 'o-', color=COLORS['ito_common'],
            label='Ito/common MC', linewidth=1.5)
    ax.plot(sigma_range, probs_ii, 's-', color=COLORS['ito_indep'],
            label='Ito/indep MC', linewidth=1.5)
    ax.plot(sigma_range, probs_sc, '^-', color=COLORS['strat_common'],
            label='Strat/common MC', linewidth=1.5)
    ax.plot(sigma_range, probs_si, 'v-', color=COLORS['strat_indep'],
            label='Strat/indep MC', linewidth=1.5)

    # RODE threshold line
    ax.axvline(rode_threshold, color=COLORS['rode'], ls=':', linewidth=1.5,
               label=f'RODE threshold ($\\tilde{{\\eta}}_{{max}} = 9\\tilde{{\\delta}}/7 \\approx {rode_threshold:.2f}$)')

    # P(extinction) = 0.5 line
    ax.axhline(0.5, color='gray', ls='--', linewidth=0.8, alpha=0.5)
    ax.text(0.05, 0.52, '$P(\\mathrm{extinction}) = 0.5$', fontsize=8, color='gray')

    # Print boundaries for reference
    for name, probs in [('Ito/common', probs_ic), ('Ito/indep', probs_ii),
                        ('Strat/common', probs_sc), ('Strat/indep', probs_si)]:
        boundary = find_stability_boundary(sigma_range, probs)
        if boundary:
            print(f"    {name}: boundary sigma = {boundary:.3f}", flush=True)

    ax.set_xlabel('Noise amplitude $\\sigma$')
    ax.set_ylabel('$P(\\mathrm{extinction})$')
    ax.set_xlim(0, 2.1)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(fontsize=7, loc='lower right')
    ax.set_title('Stability Boundary: RODE Threshold vs SDE Analog')
    fig.tight_layout()
    _save(fig, 9, 'stability_boundary')


# ===========================================================================
# Figure 10: Noise structure sensitivity
# ===========================================================================
def fig10_noise_structure_sensitivity():
    """Fig 10: Noise structure sensitivity: 2x2 panel."""
    sde_params = SDEParams()
    sde_params.dt = 0.01
    sde_params = sde_params.with_sigma(0.3, 0.3, 0.3 * 1.5)

    n_mc = 200
    solvers = [
        (euler_maruyama_common, 'Ito Common'),
        (euler_maruyama_independent, 'Ito Independent'),
        (heun_common, 'Stratonovich Common'),
        (heun_independent, 'Stratonovich Independent'),
    ]
    colors_fp = [COLORS['f_pop'], COLORS['p_pop']]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)
    axes_flat = [axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]]

    for ax, (solver_fn, title) in zip(axes_flat, solvers):
        print(f"    Running ensemble for {title}...")
        t_arr, ens = monte_carlo_ensemble(solver_fn, sde_params, n_paths=n_mc, seed=42)
        mean, lower, upper = ensemble_statistics(ens)
        step = max(1, len(t_arr) // 1000)

        for pop_idx, pop_label, color in [(0, '$f$', colors_fp[0]), (2, '$p$', colors_fp[1])]:
            ax.plot(t_arr[::step], mean[pop_idx, ::step], color=color,
                    label=pop_label, linewidth=1.2)
            ax.fill_between(t_arr[::step], lower[pop_idx, ::step], upper[pop_idx, ::step],
                            color=color, alpha=0.15)

        ax.set_title(title, fontsize=10)
        ax.legend(fontsize=8)

    axes[1, 0].set_xlabel('Time $t$')
    axes[1, 1].set_xlabel('Time $t$')
    axes[0, 0].set_ylabel('Population')
    axes[1, 0].set_ylabel('Population')
    fig.suptitle('Noise Structure Sensitivity ($\\sigma = 0.3$)', fontsize=12)
    fig.tight_layout()
    _save(fig, 10, 'noise_structure_sensitivity')
