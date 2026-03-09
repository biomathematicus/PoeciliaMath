# SPECS7: Residual Fixes from SPECS4–6 Evaluation
## Addendum to prior specs. Where SPECS7 conflicts with earlier specs, SPECS7 governs.
## All items here are coding-agent-executable unless marked [AUTHOR DECISION].

---

## Preamble: Scope

SPECS7 closes the gap between the spec stack (SPECS1–6) and the compiled
manuscript as evaluated from the PDF rendering dated 2026-03-07. Six
categories of work remain. They are listed in descending severity order.

---

## Section 1 — Table 2: Restore Missing Tabular Body (BLOCKING)

### What is wrong

The compiled PDF shows Table 2 with a truncated column header ending
mid-sentence:

    "SDE variants (calibrated against Itô/common; same σ applied to
     other variants for cross-formulation com"

and zero data rows. The table body is entirely absent from the rendered
output. This is a critical defect: Table 2 is cited in the text and its
absence makes the paper non-reproducible.

### Action: replace the Table 2 `tabular` environment

Locate the Table 2 `\begin{table}...\end{table}` block in
`poecilia_manuscript.tex`. Replace the entire table block with the
following:

```latex
\begin{table}[ht]
\centering
\caption{Calibrated $\sigma$ values matching RODE threshold-exceeding
variance at $T/2$. RODE ensemble: $n=200$ paths, $\tilde\eta_{\max}=0.25$,
$v=0.02$. SDE calibration: binary search on $\sigma$ using $n=100$
It\^{o}/common paths.  The calibration targets the It\^{o}/common-noise
variant; the same $\sigma$ tuple is then applied to the remaining three
SDE variants to hold noise amplitude constant across formulations.}
\label{tab:calibration}
\begin{tabular}{lcc}
\hline
SDE Formulation & $\sigma_f = \sigma_m$ & $\sigma_p$ \\
\hline
It\^{o} / common     & \multirow{4}{*}{(see caption)} & \multirow{4}{*}{$1.5\,\sigma_f$} \\
It\^{o} / independent & & \\
Stratonovich / common & & \\
Stratonovich / independent & & \\
\hline
\multicolumn{3}{l}{\footnotesize RODE reference:
  $\mathrm{Std}[\tilde{f}(T/2)] = 9.30$ (dimensional),
  $\mathrm{Mean}[\tilde{f}(T/2)] = 46.7$} \\
\hline
\end{tabular}
\end{table}
```

**Note to coding agent:** If `calibrate_sigma()` in `stability.py` has
been run and its output is available in `verification_results.json`,
replace the `\multirow` placeholder cells with the actual calibrated
values from keys `sigma_f_calibrated` and `sigma_p_calibrated` in that
JSON. The table structure above is the minimum required to unblock
compilation. Actual numerical values must be filled in before submission.

**Note:** If the root cause is a broken `longtable` or `tabularx`
environment in the original `.tex`, remove the offending environment and
replace with the plain `tabular` above. Do not use `tabularx`,
`longtable`, or `tabu` unless they are already in the preamble.

---

## Section 2 — Figure 7 Orphan: Remove or Integrate (Major)

### What is wrong

`figures.py` defines `fig07_ito_stratonovich_divergence()` and
`run_all.py` calls it, producing `fig07_ito_stratonovich_divergence.pdf`
and `.png`. This figure is never referenced in the manuscript body. The
manuscript body references Figures 1–9, which correspond to code functions
fig01–fig06, fig08–fig10 (skipping fig07). The off-by-one mapping means
any reader checking reproducibility will find a figure file whose number
does not match any figure in the paper.

### Option A (recommended): Remove fig07 from the codebase

In `run_all.py`, delete or comment out:
```python
print("\n--- Figure 7: Ito-Stratonovich divergence ---")
figures.fig07_ito_stratonovich_divergence(sigma_cal)
```

In `figures.py`, delete or comment out the entire
`fig07_ito_stratonovich_divergence()` function definition.

Then rename code functions to match manuscript figure numbers:

| Old function name | New function name | Manuscript figure |
|---|---|---|
| `fig08_moment_vs_montecarlo` | `fig07_moment_vs_montecarlo` | Figure 7 |
| `fig09_stability_boundary` | `fig08_stability_boundary` | Figure 8 |
| `fig10_noise_structure_sensitivity` | `fig09_noise_structure_sensitivity` | Figure 9 |

Update all calls in `run_all.py` to use the new names. Update the
`_save(fig, N, name)` call inside each function so the `N` argument
matches the new number. Verify the manuscript body figure references
(Fig. 7, Fig. 8, Fig. 9) resolve to the correct content after renaming.

### Option B (if the figure is scientifically valuable): Integrate it

Add a Figure 7 reference in the manuscript body (§5.3 or a new §5.4),
renumber downstream figures, and update all `\ref{fig:...}` labels
accordingly. This option requires author sign-off before execution.

**Default for coding agent: execute Option A.**

---

## Section 3 — Code Comment: Replace "reflection boundary" (Minor)

### What is wrong

`sde_ito.py` Listing 5 contains the comment:
```python
u = np.maximum(u, 0.0)  # reflection boundary
```
SPECS6 §3c requires this wording to be replaced throughout. The
algorithms in the manuscript body and the Stratonovich code already use
correct language; only this one comment in `sde_ito.py` was missed.

### Action

In `sde_ito.py`, replace every occurrence of:
```python
# reflection boundary
```
with:
```python
# nonnegative clipping (post-step projection onto nonneg orthant)
```

Apply the same replacement to any identical comment in `sde_stratonovich.py`
if present.

---

## Section 4 — Buckingham Citation Key: Verify Consistency (Minor)

### What is wrong

SPECS5-E4 required global replacement of `\citep{Buckingham1914}` with
`\citep{Buckingham:1914}`. This was unverifiable from the PDF because
citation keys do not appear in rendered output. A silent mismatch would
produce an `[?]` in the compiled document.

### Action

In `poecilia_manuscript.tex`, run a global search for the string
`Buckingham1914` (without colon). If any `\citep{Buckingham1914}` or
`\citet{Buckingham1914}` occurrences remain, replace each with
`\citep{Buckingham:1914}` or `\citet{Buckingham:1914}` respectively.

In `poecilia_references.bib` and `JBGInvasiveSpecies.bib`, confirm that
exactly one entry with key `Buckingham:1914` exists and no entry with key
`Buckingham1914` exists. If the bib file contains `Buckingham1914`,
rename the key to `Buckingham:1914`.

---

## Section 5 — Global Search: Surviving "Globally Dissipative" Wording (Minor)

### What is wrong

SPECS6 §1e required a global search for wording that asserts global
phase-space contraction (e.g. "everywhere in the feasible region",
"global dissipativity", "the system is dissipative when"). This search
was not verifiable from the PDF rendering alone.

### Action

In `poecilia_manuscript.tex`, search for each of the following strings
and apply the corresponding replacement if found outside the Lemma proof
and Definitions blocks:

| Search string | Replacement |
|---|---|
| `everywhere in the feasible region` | `on the population ceiling` |
| `globally dissipative` | `dissipative at the population ceiling` |
| `the system is dissipative when` | `the system is dissipative on the population ceiling when` |
| `global phase-space contraction` | `phase-space contraction at the population ceiling` |
| `guarantees dissipation` | `guarantees dissipation at the carrying capacity boundary` |

Do NOT modify the three Definitions (Definition 1 "dissipative
stochasticity", Definition 2 "non-dissipative stochasticity", Definition 3
"dissipative threshold") -- those are retained as mathematical terminology
per all prior specs.

---

## Section 6 — Label Cross-Reference Audit: Retired PoecFDim Labels (Minor)

### What is wrong

SPECS4 EDIT 2 retired the equation labels `eq:PoecFDim`, `eq:PoecMDim`,
`eq:PoecPDim` and directed that all downstream `\eqref` calls be updated
to `\eqref{eq:dim_f}`, `\eqref{eq:dim_m}`, `\eqref{eq:dim_p}`
respectively. Correctness of this replacement was unverifiable from the
PDF because undefined `\eqref` calls render as `(??)` only in the compiled
output, not in rendered text.

### Action

In `poecilia_manuscript.tex`, run a global search for each of the
following strings:

- `PoecFDim`
- `PoecMDim`
- `PoecPDim`

For every occurrence found (whether in `\label{}`, `\eqref{}`, or
`\ref{}`), apply the following substitutions:

| Old | New |
|---|---|
| `\label{eq:PoecFDim}` | delete (label was on the removed equation) |
| `\label{eq:PoecMDim}` | delete |
| `\label{eq:PoecPDim}` | delete |
| `\eqref{eq:PoecFDim}` | `\eqref{eq:dim_f}` |
| `\eqref{eq:PoecMDim}` | `\eqref{eq:dim_m}` |
| `\eqref{eq:PoecPDim}` | `\eqref{eq:dim_p}` |

After substitution, verify that `eq:dim_f`, `eq:dim_m`, `eq:dim_p` all
have corresponding `\label` declarations in the Mechanistic Derivation
subsection. If any label is missing, add it to the appropriate displayed
equation.

---

## Section 7 — Author Decision Items from SPECS6 §6 (NOT coding-agent tasks)

The following items from SPECS6 §6 are reproduced here for tracking. They
require author modeling or biological decisions and must not be executed
by a coding agent without explicit direction.

| ID | Issue | Recommended action |
|---|---|---|
| C4 | Nonneg clipping of L allows RODE trajectories to grow above K (Figure 4b shows runaway) | Either (a) add a smooth penalty term above K, or (b) explicitly define the model as a projected/truncated system and state this in the manuscript |
| C5 | Extinction event definition conflates parasite extinction, host extinction, and transient threshold-crossings | Separate extinction outcome classes; decide whether extinction is terminal (absorbing) or a transient event |
| M4 | a=0.8 calibrated from adult sex-ratio, not birth sex-ratio | Reinterpret a as effective female recruitment fraction, or recalibrate from brood data |
| M6 | RODE resampling interval is a model parameter with ecological meaning (environmental correlation time), not a numerical detail | Introduce an explicit correlation-time parameter; sensitivity analysis recommended |
| M7 | Figure 5 single-trajectory panel shows qualitatively different regimes across formulations, not "consistent" behavior | Soften the prose claim to say "regime membership is consistent" and add mean-drift-matched comparison |
| M8 | Figure 4(b) runaway growth above K is labelled "noisy coexistence" | Either fix C4 above, or change caption and surrounding prose to acknowledge the blow-up honestly |

---

## Summary Table

| Section | Issue | Severity | Type |
|---|---|---|---|
| 1 | Table 2 body absent | **Blocking** | Coding agent |
| 2 | fig07 orphan (code / run_all) | Major | Coding agent |
| 3 | `# reflection boundary` comment in `sde_ito.py` | Minor | Coding agent |
| 4 | Buckingham citation key consistency | Minor | Coding agent |
| 5 | Surviving globally-dissipative wording | Minor | Coding agent |
| 6 | Retired PoecFDim label cross-refs | Minor | Coding agent |
| 7 | C4/C5/M4/M6/M7/M8 | Varies | Author decision |

---

## What the Agent Must NOT Change

- The analytical content of any section (proofs, propositions, definitions).
- The three Definitions (dissipative stochasticity, non-dissipative,
  dissipative threshold).
- The discrimination speed finding and biological interpretation.
- Any prior SPECS edits not explicitly modified here.
- The title.
