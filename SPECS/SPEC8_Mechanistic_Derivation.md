# SPEC 8 — Mechanistic Derivation, Terminology Update, Extinction Analysis

## Status: READY FOR IMPLEMENTATION
## Target files: `poecilia_manuscript.tex`, `poecilia_sde/figures.py`, `poecilia_sde/params.py`
## Depends on: nothing (first in sequence)
## Must be completed before: SPEC 9, SPEC 10

---

## 1. CONTEXT AND MOTIVATION

The current manuscript presents the three-population model (host females $f$,
host males $m$, parasite females $p$) through a *phenomenological*
characterization: it states four biological assumptions and postulates the
birth terms directly. Some reviewers and readers legitimately object that the
functional form $m(f - \gamma p)$ is asserted rather than derived.

This SPEC adds a rigorous *mechanistic* derivation from first principles using
a two-step argument:

**Step 1 (per-encounter acceptance):** Males encounter females at random
(mass-action). Upon each parasite encounter, the male accepts with probability
$\gamma$ (per-encounter behavioral decision, consistent with Riesch et al.
2008 field data showing active sperm allocation discrimination). Upon each host
female encounter, the male always accepts.

**Step 2 (finite capacity constraint):** Each accepted parasite mating
consumes one unit of male mating capacity, displacing one potential host
female mating. The displacement is additive and 1:1, giving bisexual
births $\propto m(f - \gamma p)$.

The key result: **the functional form $m(f - \gamma p)$ is a theorem of these
two steps, not an assumption.** The equations do not change. Only the
derivation section is rewritten.

The Riesch et al. (2008) field data (sperm limitation: 74% of host females vs
10% of parasite females had sperm in natural conditions) provide empirical
support for Step 1. The data show behavioral willingness discrimination, not
physiological sperm exhaustion. The simplifying assumption $c = 1$ in
Step 2 (one parasite mating forfeits exactly one host-female mating) is noted
explicitly; Riesch data on differential sperm volume suggest $c < 1$ may be
more realistic and is flagged as a future extension.

---

## 2. TERMINOLOGY CHANGES (GLOBAL, ALL FILES)

Replace all occurrences of the following terms throughout
`poecilia_manuscript.tex`. Apply with care — check mathematical context
before replacing to avoid breaking equations.

| Old term | New term |
|---|---|
| bisexual female(s) | host female(s) |
| bisexual male(s) | host male(s) |
| bisexual population | host population |
| bisexual species | host species |
| unisexual female(s) | parasite female(s) |
| unisexual population | parasite population |
| unisexual species | parasite species |
| unisexuals | parasite females |
| bisexuals | host individuals |
| gynogenetic complex | host–parasite complex |

**Variable names $f$, $m$, $p$ in equations and code do NOT change.**
Only prose labels change.

**Title change:**
```
Old: Noise Can Save a Sperm Parasite: Stochastic Stabilization in Gynogenetic Complexes
New: The Sperm Parasite Paradox: Stochastic Stabilization in Gynogenetic Complexes
```

---

## 3. MANUSCRIPT CHANGES — `poecilia_manuscript.tex`

### 3.1 Replace the existing subsection `\subsection{Mechanistic Derivation of the Mathematical Models}`

The current subsection (lines ~96–225) presents a phenomenological
characterization. Replace the **body** of this subsection (keep the
`\subsection` heading) with the following new content. The four-assumption
list and the birth/death term equations (`eq:birth_f`, `eq:birth_m`,
`eq:birth_p`, `eq:dim_f`, `eq:dim_m`, `eq:dim_p`) must be preserved in
their current LaTeX form; only the surrounding prose changes.

**New body for `\subsection{Mechanistic Derivation}`:**

```latex
The model is constructed from first principles using a two-step
mass-action argument. The population state is described by three
variables: host females $\tilde{f}$, host males $\tilde{m}$, and parasite
females $\tilde{p}$, all with units of individuals. Parasite females
(\textit{P.~formosa}) require sperm from host males (\textit{P.~latipinna}
or \textit{P.~mexicana}) to initiate embryogenesis; the paternal genome
is excluded from all offspring.

\noindent\textbf{Step 1: Per-encounter acceptance probability.}
In a well-mixed population, encounters between individuals occur at
rates proportional to the product of their abundances (mass action):
\begin{align*}
  \text{host male -- host female encounters:}   &\quad \alpha\,\tilde{m}\,\tilde{f}, \\
  \text{host male -- parasite female encounters:} &\quad \alpha\,\tilde{m}\,\tilde{p}.
\end{align*}
Upon each host-female encounter, the male accepts and mates; no
discrimination occurs within the host species.  Upon each parasite
encounter, the male accepts with probability $\gamma \in (0,1]$ and
rejects with probability $1-\gamma$.  The factor $\gamma$ therefore
has a precise biological meaning: it is the \emph{per-encounter
acceptance probability} for parasite females, representing the outcome
of male behavioral mate choice.  This interpretation is supported by
field data: \citet{Riesch2008} found that under natural conditions
only approximately 10\% of parasite females carried sperm, versus 74\%
of host females, confirming that discrimination operates at the
per-encounter level and not through sperm exhaustion.

The resulting effective mating rates are:
\begin{align*}
  \text{effective host-female matings:}   &\quad \alpha\,\tilde{m}\,\tilde{f}, \\
  \text{effective parasite-female matings:} &\quad \gamma\,\alpha\,\tilde{m}\,\tilde{p}.
\end{align*}
At this stage the two encounter pools are independent; parasites compete
with host females only through shared carrying capacity.

\noindent\textbf{Step 2: Finite male mating capacity.}
Field observations establish that each male has a finite number of
mating events per unit time~\citep{Balsano1989}.  When a male accepts a
parasite encounter, that mating slot is consumed and is simultaneously
unavailable for a host female: accepted parasite matings displace
host-female matings in a 1:1 ratio.  The net effective host-female
mating rate therefore becomes:
\[
  \alpha\,\tilde{m}\,\tilde{f} - \gamma\,\alpha\,\tilde{m}\,\tilde{p}
  = \alpha\,\tilde{m}\!\left(\tilde{f} - \gamma\tilde{p}\right).
\]
The term $\tilde{f} - \gamma\tilde{p}$ is thus a \emph{theorem} of
Steps~1 and~2, not an additional assumption.

\begin{remark}
The 1:1 displacement coefficient is a simplifying assumption: Riesch
et al.~\citeyearpar{Riesch2008} report that when males do accept
parasite encounters they transfer substantially less sperm (median
66{,}667 vs.\ 783{,}333 sperm units for host females).  This suggests
a displacement coefficient $c < 1$ may be more realistic, giving
$\tilde{m}(\tilde{f} - c\gamma\tilde{p})$.  The current model adopts
$c = 1$ as the parsimonious baseline; calibrating $c$ from sperm-count
field data is a natural extension.
\end{remark}

\noindent\textbf{Biological assumptions.}
The derivation rests on four simplifying assumptions.

\begin{enumerate}
  \item \textbf{Common vital rates.}  All individuals share a single
    per-capita birth coefficient $\tilde{\beta}$ and a single per-capita
    death coefficient $\tilde{\delta}$.

  \item \textbf{Per-encounter acceptance (Step~1).}  The discrimination
    factor $\gamma \in (0,1]$ is the per-encounter probability that a
    host male accepts a parasite female.

  \item \textbf{Pedigree-determined offspring sex.}  A host male--host
    female mating produces fraction $a$ female offspring and $(1-a)$
    male offspring.  A host male--parasite female mating produces only
    parasite female offspring (gynogenesis; no paternal contribution).

  \item \textbf{Logistic density dependence.}  All populations share
    carrying capacity $\tilde{K}$, entering through
    $\tilde{L} = 1 - (\tilde{f}+\tilde{m}+\tilde{p})/\tilde{K}$.
\end{enumerate}

\noindent\textbf{Birth and death terms.}
Applying Assumptions 1--4 and the two-step argument, the birth
contribution to each population per unit time is:
%
\begin{align}
  \text{host females born:}   &\quad
    a\,\tilde{\beta}\,\tilde{L}\,\tilde{m}\,(\tilde{f}-\gamma\tilde{p}),
    \label{eq:birth_f} \\[4pt]
  \text{host males born:}     &\quad
    (1-a)\,\tilde{\beta}\,\tilde{L}\,\tilde{m}\,(\tilde{f}-\gamma\tilde{p}),
    \label{eq:birth_m} \\[4pt]
  \text{parasite females born:}  &\quad
    \gamma\,\tilde{\beta}\,\tilde{L}\,\tilde{m}\,\tilde{p}.
    \label{eq:birth_p}
\end{align}
%
Each population declines at per-capita rate $\tilde{\delta}$, giving
death contributions $-\tilde{\delta}\tilde{f}$,
$-\tilde{\delta}\tilde{m}$, and $-\tilde{\delta}\tilde{p}$.
```

### 3.2 Delete the commented-out TYC block

Remove the commented-out block from line ~227 to line ~280 (the block
beginning `% \subsection{Mechanistic Derivation of the Mathematical Models}`
through `% which is the same as Equation \ref{eq:fTYC} in the TYC model`).
This block is now superseded by the new derivation above. Do not alter
any active (uncommented) LaTeX code surrounding it.

### 3.3 Add new subsection `\subsection{Extinction and Coexistence Conditions}`

Insert this new subsection **immediately after** the existing
`\subsection{Deterministic Core}\label{sec:deterministic}` subsection
(i.e., after line ~308, before `\subsection{Non-Dimensionalization}`).

```latex
%---------------------------------------------------------------
\subsection{Extinction and Coexistence Conditions}\label{sec:extinction}
%---------------------------------------------------------------

In the absence of noise ($\eta_i \equiv 0$) and with $\gamma = \text{constant}$,
the system \eqref{eq:PoeciliaF}--\eqref{eq:PoeciliaP} admits three
qualitatively distinct long-term outcomes determined by the value of $\gamma$
relative to an equilibrium threshold $\gamma_{eq}$.

At a coexistence steady state $\mathbf{u}^* = (f^*, m^*, p^*)$ with all
three populations positive, setting $\dot{p} = 0$ in
Equation~\eqref{eq:PoeciliaP} and $\dot{f}/\dot{m} = a/(1-a)$ (from
Equations~\eqref{eq:PoeciliaF}--\eqref{eq:PoeciliaM}) yields the unique
equilibrium discrimination factor:
\begin{equation}\label{eq:GammaSS}
  \gamma_{eq} = \frac{a\,f^*}{a\,p^* + f^*}.
\end{equation}
With the biologically motivated values $a = 0.8$, $f^* = 100/K$,
$p^* = 10/K$ this gives $\gamma_{eq} = 80/108 \approx 0.74$.

Three regimes follow directly:

\begin{itemize}
  \item $\gamma < \gamma_{eq}$: male discrimination against parasite
    females is insufficient to protect the host population. The parasite
    female population grows unchecked, diverting increasing male mating
    effort from host females. The host population declines, reducing
    sperm availability to all females. The positive feedback drives all
    three populations to extinction.

  \item $\gamma = \gamma_{eq}$: the discrimination level exactly balances
    parasite growth, and coexistence is possible at the steady state
    $\mathbf{u}^*$.

  \item $\gamma > \gamma_{eq}$: parasite females are strongly rejected by
    host males. Parasite females go extinct first; the host population
    recovers toward its two-population (host female -- host male) equilibrium.
\end{itemize}

The extinction regime $\gamma < \gamma_{eq}$ is illustrated numerically
in Figure~\ref{fig:extinction}, which integrates
Equations~\eqref{eq:PoeciliaF}--\eqref{eq:PoeciliaP} in non-dimensional
time with slow discrimination speed $v = 6$ (corresponding to dimensional
$v_{\mathrm{dim}} = 0.02$) and $\eta_i \equiv 0$.  All three populations
decay to zero: the parasite initially grows, drawing down host male
abundance, which in turn starves both host females and eventually
parasite females of reproductive opportunity.

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.7\textwidth]{poecilia_sde/figures/fig00_extinction_ode.png}
  \caption{Extinction dynamics under slow male discrimination
    ($v = 6$, non-dimensional; $\eta_i \equiv 0$).  Host females
    (green), host males (blue), and parasite females (red) all
    decay to zero. Non-dimensional time $\tau = \tilde{\delta}\,t$;
    $\tau = 20$ corresponds to 200 days.  Parameters: Table~\ref{tab:parameters}.}
  \label{fig:extinction}
\end{figure}
```

---

## 4. NEW PYTHON FIGURE — `poecilia_sde/figures.py`

Add the following function to `figures.py`. Insert it **before** `fig01_gamma_curves`.
Also add a call to it in `run_all.py` so it runs as part of the standard pipeline.

```python
def fig00_extinction_ode():
    """
    Fig 00: Pure ODE extinction dynamics (no noise, slow discrimination).
    Shows host females (f), host males (m), and parasite females (p)
    all decaying to zero under slow male discrimination speed v=6 (nondim).
    Non-dimensional time axis.
    Saved as fig00_extinction_ode.pdf/.png
    """
    from params import BaseParams
    from deterministic import txc_rhs
    from scipy.integrate import solve_ivp

    # Use slow discrimination: v=6 nondim (= 0.02 * 300 dim)
    params = BaseParams()
    params.v = 6.0  # slow: leads to extinction

    t_end = 20.0   # non-dimensional time (= 200 days dimensional)
    t_eval = np.linspace(0, t_end, 5000)
    u0 = [params.f0, params.m0, params.p0]

    sol = solve_ivp(
        lambda t, u: txc_rhs(t, u, params),
        (0, t_end), u0, t_eval=t_eval,
        method='RK45', rtol=1e-10, atol=1e-12
    )

    # Convert to dimensional-scale for readability (multiply by K=300)
    K = 300.0
    f_dim = sol.y[0] * K
    m_dim = sol.y[1] * K
    p_dim = sol.y[2] * K

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(sol.t, f_dim, color=COLORS['f_pop'], lw=2, label='Host females ($f$)')
    ax.plot(sol.t, m_dim, color=COLORS['m_pop'], lw=2, label='Host males ($m$)')
    ax.plot(sol.t, p_dim, color=COLORS['p_pop'], lw=2, label='Parasite females ($p$)')

    ax.set_xlabel(r'Non-dimensional time $\tau = \tilde{\delta}\,t$', fontsize=12)
    ax.set_ylabel('Population (individuals)', fontsize=12)
    ax.set_title('Extinction under slow discrimination ($v=6$, no noise)', fontsize=12)
    ax.legend(fontsize=11)
    ax.set_xlim(0, t_end)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)

    _save(fig, 0, 'extinction_ode')
```

---

## 5. PARAMETERS VERIFICATION

In `params.py`, verify that `BaseParams` has:
- `v: float = 60.0` (fast, coexistence — default)
- No change needed; the figure function above overrides `v=6.0` locally.
- `DimensionalParams` should retain `v_slow: float = 0.02` and
  `v_fast: float = 0.20` unchanged.

---

## 6. ACCEPTANCE CRITERIA

After implementation:

1. `pdflatex poecilia_manuscript.tex` compiles without errors.
2. The new figure `fig00_extinction_ode.png` is generated in
   `poecilia_sde/figures/` and shows all three populations decaying to zero.
3. The words "bisexual" and "unisexual" do not appear in active (uncommented)
   LaTeX prose. They may remain in `\cite` keys and bibliography entries.
4. The title reads "The Sperm Parasite Paradox: Stochastic Stabilization
   in Gynogenetic Complexes".
5. All equation labels (`eq:birth_f`, `eq:birth_m`, `eq:birth_p`,
   `eq:dim_f`, `eq:dim_m`, `eq:dim_p`, `eq:GammaSS`) still resolve.
6. The `\ref{fig:extinction}` reference resolves in the compiled PDF.

---

## 7. DO NOT CHANGE

- Any equation in `\begin{align}...\end{align}` blocks.
- Variable names `f`, `m`, `p` in LaTeX math mode.
- Variable names `f`, `m`, `p`, `f0`, `m0`, `p0` in Python code.
- Any function signatures in `deterministic.py`, `params.py`, or `rode.py`.
- The `\label` identifiers of any existing equations or figures.
- Any `.bib` files.
