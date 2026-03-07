# SPECS4: Nondimensionalization Redundancy Fix
## Patch to `poecilia_manuscript.tex`
## Where SPECS4 conflicts with earlier specs, SPECS4 governs for the sections it touches.

---

## 1. Problem Statement

The manuscript currently presents the dimensional equations and the
nondimensionalization rescaling in three overlapping locations, creating
redundancy and a conceptual inconsistency:

| Location | Content | Problem |
|---|---|---|
| `\subsection*{Mechanistic Derivation}` | Dimensional equations (no η̃) + inline rescaling block | Rescaling duplicates §Non-Dimensionalization |
| `\subsection{Deterministic Core}` | Dimensional equations again (this time with η̃) + γ_eq | Equations duplicate Mechanistic Derivation; η̃ terms appear without motivation |
| `\subsection{Non-Dimensionalization}` | Rescaling + non-dimensional system | Correct home for rescaling; currently duplicate |

**Option A (adopted):** Mechanistic Derivation owns the dimensional equations
(deterministic only). Deterministic Core cross-references them and owns only
the γ_eq analysis. Non-Dimensionalization is the unique home of the rescaling
and the non-dimensional system, and introduces η̃ for the first time.

---

## 2. Surgery Instructions

The agent must make **three targeted edits** to `poecilia_manuscript.tex`.
No other sections are to be touched. The edits are listed in document order.

---

### EDIT 1 — `\subsection*{Mechanistic Derivation}`: Remove the inline rescaling block

**Locate** the following block near the end of the Mechanistic Derivation subsection
(after the dimensional equations `\eqref{eq:dim_f}`–`\eqref{eq:dim_p}` are assembled):

```latex
where tildes denote dimensional quantities throughout.  The system is
non-dimensionalized by the rescaling
%
\begin{equation}\label{eq:nondim}
  u_i = \frac{\tilde{u}_i}{\tilde{K}}, \qquad
  \tau  = \tilde{\delta}\,t, \qquad
  \beta = \frac{\tilde{\beta}\,\tilde{K}}{\tilde{\delta}},
\end{equation}
%
following Buckingham's $\Pi$ theorem~\citep{Buckingham1914}, which
reduces the four independent dimensional parameters
$(\tilde{\beta},\tilde{\delta},\tilde{K},a)$ to the single composite
$\beta = \tilde{\beta}\tilde{K}/\tilde{\delta}$.  Setting $\tilde{\delta}=1$
by the rescaling of time, the non-dimensional system is presented in full
in the following subsection.
```

**Replace** the entire block above (from "where tildes denote dimensional
quantities throughout" through "in the following subsection.") with:

```latex
where tildes denote dimensional quantities throughout.
Stochastic perturbations $\tilde{\eta}_i(t)$ are appended to each
equation in Section~\ref{sec:stochastic}; the deterministic skeleton
above is analysed first to establish the equilibrium structure.
The system is non-dimensionalized in Section~\ref{sec:nondim}.
```

**Rationale:** The rescaling belongs exclusively in §Non-Dimensionalization.
The new closing sentence provides a forward pointer and removes the
duplication without losing any information. The label `\ref{sec:nondim}`
must resolve to the `\subsection{Non-Dimensionalization}` label (see EDIT 3).

---

### EDIT 2 — `\subsection{Deterministic Core}`: Replace opening paragraph and duplicate equations

**Locate** the opening of the Deterministic Core subsection. It currently reads
(in its entirety, from the subsection heading through the γ_eq regime description):

```latex
%---------------------------------------------------------------
\subsection{Deterministic Core}
%---------------------------------------------------------------

The gynogenetic system involves three populations: bisexual females ($\tilde{f}$), males ($\tilde{m}$), and unisexual females ($\tilde{p}$).  As females compete for the service of males, sperm is assumed to be a limiting factor.  The effective bisexual female population with access to sperm is therefore $\tilde{f} - \gamma \tilde{p}$, where $\gamma$ is the sexual discrimination factor controlling the mating frequency between males and unisexuals: when $\gamma = 1$, males have equal probability of mating with unisexuals or bisexual females; when $\gamma$ is low, males preferentially mate with conspecific females.  The parameter $a$ represents the proportion of females produced in each bisexual mating event.  Field studies report that bisexual males account for less than 20\% of poeciliid populations~\citep{Balsano1989, Snelson1980}, indicating $a \approx 0.8$.  The dimensional system is
\begin{align}
  \frac{d\tilde{f}}{dt} &= a\tilde{\beta}L\tilde{m}(\tilde{f}-\gamma \tilde{p})-\tilde{\delta}\tilde{f}+\tilde{\eta}_f(t)\tilde{f}, \label{eq:PoecFDim} \\
  \frac{d\tilde{m}}{dt} &= (1-a)\tilde{\beta}L\tilde{m}(\tilde{f}-\gamma \tilde{p})-\tilde{\delta}\tilde{m}+\tilde{\eta}_m(t)\tilde{m}, \label{eq:PoecMDim} \\
  \frac{d\tilde{p}}{dt} &= \gamma\tilde{\beta}L\tilde{m} \tilde{p} -\tilde{\delta}\tilde{p} + \tilde{\eta}_p(t) \tilde{p}, \label{eq:PoecPDim}
\end{align}
where $L = 1-(\tilde{f}+\tilde{m}+\tilde{p})/\tilde{K}$ is the logistic factor representing density-dependent growth limitation, $\tilde{\beta}$ is the per-capita birth rate, $\tilde{\delta}$ is the per-capita death rate, $\tilde{K}$ is the carrying capacity, and $\tilde{\eta}_i(t)$ represents stochastic perturbations to the growth rate.

Setting $\tilde{\eta}_i = 0$ and $\gamma = $ constant, the steady state satisfies $\dot{\mathbf{u}}(\mathbf{u}_0) = \mathbf{0}$.  Solving the resulting algebraic system yields the unique equilibrium discrimination factor:
\begin{equation}\label{eq:GammaSS}
  \gamma_{eq} = \frac{a f_0}{a p_0 + f_0}.
\end{equation}
With the parameter values $a = 0.8$, $\tilde{f}_0 = 100$, and $\tilde{p}_0 = 10$, this gives $\gamma_{eq} = 80/108 \approx 0.74$.  Three qualitative regimes exist: when $\gamma < \gamma_{eq}$, unisexuals go extinct; when $\gamma = \gamma_{eq}$, coexistence obtains; when $\gamma > \gamma_{eq}$, bisexuals go extinct followed by unisexuals.
```

**Replace** the entire block above with:

```latex
%---------------------------------------------------------------
\subsection{Deterministic Core}\label{sec:deterministic}
%---------------------------------------------------------------

The dimensional system derived in the preceding subsection,
Equations~\eqref{eq:dim_f}--\eqref{eq:dim_p}, is analysed here in the
deterministic limit $\tilde{\eta}_i \equiv 0$ and with $\gamma =
\text{constant}$.  The steady state satisfies
$\dot{\mathbf{u}}(\mathbf{u}_0) = \mathbf{0}$.  Solving the resulting
algebraic system yields the unique equilibrium discrimination factor:
\begin{equation}\label{eq:GammaSS}
  \gamma_{eq} = \frac{a\tilde{f}_0}{a\tilde{p}_0 + \tilde{f}_0}.
\end{equation}
With the parameter values $a = 0.8$, $\tilde{f}_0 = 100$, and
$\tilde{p}_0 = 10$, this gives $\gamma_{eq} = 80/108 \approx 0.74$.
Three qualitative regimes exist: when $\gamma < \gamma_{eq}$, unisexuals
go extinct; when $\gamma = \gamma_{eq}$, coexistence obtains; when
$\gamma > \gamma_{eq}$, bisexuals go extinct followed by unisexuals.
```

**Rationale:** The opening paragraph duplicated the Mechanistic Derivation.
The three align equations with η̃ terms are removed here because η̃ has not
yet been formally introduced; it is introduced in EDIT 3 below.
The labels `eq:PoecFDim`, `eq:PoecMDim`, `eq:PoecPDim` are retired; any
downstream `\eqref` calls to these labels must be updated to
`\eqref{eq:dim_f}`, `\eqref{eq:dim_m}`, `\eqref{eq:dim_p}` respectively.
The agent must search the full document for `PoecFDim`, `PoecMDim`,
`PoecPDim` and perform these substitutions globally.

---

### EDIT 3 — `\subsection{Non-Dimensionalization}`: Add label and introduce η̃

**Locate** the Non-Dimensionalization subsection heading and its opening sentence:

```latex
%---------------------------------------------------------------
\subsection{Non-Dimensionalization}
%---------------------------------------------------------------

Non-dimensionalization reduces the number of independent parameters and reveals the natural scales of the problem~\citep{Buckingham:1914}.
```

**Replace** with:

```latex
%---------------------------------------------------------------
\subsection{Non-Dimensionalization}\label{sec:nondim}
%---------------------------------------------------------------

Non-dimensionalization reduces the number of independent parameters and
reveals the natural scales of the problem~\citep{Buckingham:1914}.
Stochastic perturbations to the per-capita growth rates are introduced at
this stage as dimensionless noise amplitudes $\eta_i(t) =
\tilde{\eta}_i(t)/\tilde{\delta}$; their statistical properties and
biological interpretation are developed in Section~\ref{sec:stochastic}.
```

**Rationale:** The label `\label{sec:nondim}` enables the forward reference
inserted in EDIT 1. The new sentence is the unique introduction of η̃ in the
model section, resolving the inconsistency where η̃ previously appeared in the
Deterministic Core without motivation.

The remainder of the Non-Dimensionalization subsection (the rescaling display,
the non-dimensional equations `\eqref{eq:PoeciliaF}`–`\eqref{eq:PoeciliaP}`,
and the parameter value sentences) is **unchanged**.

---

## 3. Label Consistency Check

After completing the three edits, the agent must verify:

| Old label | New label | Action |
|---|---|---|
| `eq:PoecFDim` | `eq:dim_f` | Global search-and-replace in `\eqref{}` calls |
| `eq:PoecMDim` | `eq:dim_m` | Global search-and-replace in `\eqref{}` calls |
| `eq:PoecPDim` | `eq:dim_p` | Global search-and-replace in `\eqref{}` calls |
| `\label{sec:nondim}` (new) | — | Must be present after EDIT 3 |
| `\label{sec:deterministic}` (new) | — | Must be present after EDIT 2 |
| `\ref{sec:stochastic}` | — | Must resolve to the Stochastic Formulations section label; if that label does not exist, add `\label{sec:stochastic}` to `\section{Stochastic Formulations}` |

---

## 4. Structural Outcome

After these three edits, the logical flow of Section 2 is:

```
\subsection*{Mechanistic Derivation}
  → derives dimensional equations (eq:dim_f–eq:dim_p), no η̃
  → closes with forward pointer to §Non-Dimensionalization

\subsection{Deterministic Core}  [label: sec:deterministic]
  → cross-references eq:dim_f–eq:dim_p
  → sets η̃=0, derives γ_eq
  → states three qualitative regimes

\subsection{Non-Dimensionalization}  [label: sec:nondim]
  → introduces η̃ for first time
  → states rescaling (unique occurrence)
  → presents non-dimensional system (unique occurrence)

\subsection{Sexual Discrimination Function}
  → unchanged
```

Each subsection has exactly one job. No equation block appears more than once.
The Buckingham citation appears once (§Non-Dimensionalization only).

---

## 5. What the Agent Must NOT Change

- The content of `\subsection{Sexual Discrimination Function}` and all
  subsequent sections.
- The non-dimensional equations `\eqref{eq:PoeciliaF}`–`\eqref{eq:PoeciliaP}`
  in §Non-Dimensionalization.
- The stochastic section or any analytical results.
- Any bibliography entries.
- The `\subsection*{Mechanistic Derivation}` prose content (assumptions,
  birth terms, γ discussion, Riesch paragraph) — only the closing rescaling
  block is removed and replaced with the forward pointer.
