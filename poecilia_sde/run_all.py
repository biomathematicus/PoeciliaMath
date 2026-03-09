"""
Master entry point for the Poecilia host--parasite manuscript figures.
Runs: symbolic verification, sigma calibration, all figures (fig00--fig09).
"""
import os
import sys
import json

# Ensure we can import local modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    os.makedirs('figures', exist_ok=True)

    # Phase 1: Symbolic verification
    print("=== Phase 1: Symbolic Verification ===")
    from verification import run_all_verifications
    results = run_all_verifications()
    with open('verification_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print_verification_summary(results)

    # Phase 2: Sigma calibration
    print("\n=== Phase 2: Sigma Calibration ===")
    from stability import calibrate_sigma
    sigma_cal = calibrate_sigma()
    results['sigma_calibration'] = sigma_cal
    with open('verification_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)

    # Phase 3: Generate all figures
    print("\n=== Phase 3: Generating Figures ===")
    import figures

    print("\n--- Figure 0: Extinction ODE ---")
    figures.fig00_extinction_ode()

    print("\n--- Figure 1: Gamma curves ---")
    figures.fig01_gamma_curves()

    print("\n--- Figure 2: Constant gamma ---")
    figures.fig02_constant_gamma()

    print("\n--- Figure 3: Sigmoid gamma ---")
    figures.fig03_sigmoid_gamma()

    print("\n--- Figure 4: RODE stochasticity ---")
    figures.fig04_rode_stochasticity()

    print("\n--- Figure 5: Single trajectory comparison ---")
    figures.fig05_single_trajectory_comparison(sigma_cal)

    print("\n--- Figure 6: Ensemble statistics ---")
    figures.fig06_ensemble_statistics(sigma_cal)

    print("\n--- Figure 7: Moment vs Monte Carlo ---")
    figures.fig07_moment_vs_montecarlo(sigma_cal)

    print("\n--- Figure 8: Stability boundary ---")
    figures.fig08_stability_boundary()

    print("\n--- Figure 9: Noise structure sensitivity ---")
    figures.fig09_noise_structure_sensitivity()

    print("\n=== Done. All figures saved to figures/ ===")


def print_verification_summary(results):
    for key, val in results.items():
        if isinstance(val, dict) and 'status' in val:
            print(f"  {key}: {val['status']}")


if __name__ == '__main__':
    main()
