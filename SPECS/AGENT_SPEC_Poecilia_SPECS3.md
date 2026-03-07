# SPECS3: Editorial and Structural Patch
## Addendum to AGENT_SPEC_Poecilia_v2.md + AGENT_SPEC_Poecilia_SPECS2.md
## Where SPECS3 conflicts with earlier specs, SPECS3 governs.

---

## 1. Title Options and Recommendation

The user requested an attention-grabbing title. The following five options are offered, ranked
from most to least bold. The agent should use the one chosen by the authors; if no selection
is made, use Option A as default.

**Option A (Recommended for ecology journals):**
> Noise Can Save the Host: Stochastic Stabilization in Gynogenetic Sperm-Parasite Complexes

*Rationale: Leads with the paper's most counterintuitive finding. "Noise Can Save" is
memorable and testable-sounding. "Sperm-Parasite Complexes" situates the biology precisely.*

**Option B (Recommended for math-biology journals):**
> Stochastic Coexistence and Extinction in Gynogenetic Species Complexes:
> Comparing RODE and SDE Formulations for Poecilia formosa

*Rationale: Methodologically explicit. Clearly signals the comparative framework contribution.*

**Option C (Most evocative):**
> Seduced into Extinction: Stochastic Population Dynamics of Gynogenetic Sperm Parasitism
> in Poecilia formosa

*Rationale: "Seduced" captures male mating behavior driving host decline. High click-through
potential. May be too informal for some journals.*

**Option D (User's framing, expanded):**
> Characterization of Sperm Parasites: Stochastic Dynamics of Coexistence and Extinction
> in Poecilia formosa

*Rationale: Preserves the user's phrasing while adding specificity. The word
"Characterization" is appropriate for a paper that compares multiple frameworks.*

**Option E (Paradox framing):**
> The Extinction Trap: How Gynogenetic Sperm Parasites Drive Coexistence and Collapse
> Under Environmental Stochasticity

*Rationale: "Extinction Trap" highlights the ecological paradox. Strong for broad-audience
outlets (e.g., The American Naturalist).*

**Agent instruction:** Use Option A unless a different option is specified by the authors.
The subtitle structure (main title: subtitle) is required for all options to accommodate
indexing.

---

## 2. Terminology Purge and Source Adaptation

### 2.1 Forbidden Terms

The following terms and phrases MUST NOT appear anywhere in the manuscript, including
figure captions, table headers, appendix text, and LaTeX comments:

| Forbidden | Required replacement |
|---|---|
| Trojan X Chromosome | gynogenetic chromosome mechanism |
| TXC | gynogenetic system (or simply: the model system) |
| Trojan Y Chromosome | sex-biased eradication strategy (when reference is unavoidable) |
| Ark chromosome | omit entirely |
| (any) dissertation cross-reference | inline prose |
| \cite{Gutierrez:Trojan} | DELETE, do not replace |
| \cite{Gutierrez:dissertation} | DELETE, do not replace |
| "as shown in Chapter X" | replace with: "as derived below" or "as shown in Section X" |
| "as discussed in Section \ref{chap:...}" | rewrite with inline explanation |

The term "gynogenetic" IS permitted and preferred. "Sperm parasite" IS permitted and is
the correct technical term for P. formosa's ecological role.

### 2.2 Content to Adapt from 5A_OtherCases.tex

The agent must read /mnt/project/5A_OtherCases.tex and extract the following content
verbatim or near-verbatim, then adapt it into the manuscript prose after removing
all forbidden terminology and all chapter cross-references:

**From Section 5.1 (Introduction to Sperm Parasites):**
- The opening classification: parthenogenesis vs gynogenesis; the definition of sperm
  parasite and sperm host. Preserve the biological precision; rewrite to be self-contained.
- The Hubbs and Hubbs 1932 discovery sentence. (The cite is \cite{Wetherington:Poeciliids}
  in the source; map this to Wetherington1989 in the new bib.)
- The Avise et al. mitochondrial DNA sentence. (Source year error: use 1991, not 1990.)
- The Soto La Marina field data description (20 locations, 1970–1978, habitat variation,
  dry/rainy season pool connectivity). This is rich biological context; keep it in full.
- The pedigree logic paragraph (p produces more p per mating; pressure on f-m mating).
- The discrimination behavior paragraph (population-dependent preference; dominance
  hierarchy explanation). Source cite \cite{Balsano:Poecilia} and \cite{Riesch:limitation}.
- The prior models paragraph: Kiester et al. 1981, Schley et al. 2004, Peck et al. 1999,
  Kokko et al. 2008, Heubel et al. 2009. The agent must adapt these sentences without
  using the chapter cross-reference to "Section 5.2."
- The triploid clarification sentence (P. formosa mostly diploid; triploid XXY exists but Y
  is silent and does not affect dynamics).
- The statement of gap: no prior model accounts for (i) high field variability, (ii) speed
  of discrimination as coexistence controller.

**From Section 5.2 (Mathematical Model):**
- The sperm-as-limiting-factor motivation. Keep the sentence beginning "As females compete
  for the service of the males, sperm is assumed to be a limiting factor."
- The kinetics derivation narrative (from pedigrees to ODE terms). This prose must flow
  continuously with the equations.
- The definition of γ (discrimination factor) and a (proportion of females in bisexual
  progeny). Include the biological justification that a ≈ 0.8 from Balsano et al.
- The non-dimensionalization narrative (Buckingham π theorem reference, \cite{Buckingham}).
  Note: Buckingham 1914 is already in JBGInvasiveSpecies.bib as the key Buckingham:Physical
  or similar — the agent must find the correct key in the existing bib.
- The sigmoid γ motivation: population-dependent discrimination, why it is biologically
  more realistic than constant γ.

**From Section 5.3 (Methods) and 5.4 (Results):**
- Adapt for narrative continuity; the dissertation's methods are now superseded by the
  Python implementation described in v2.0/SPECS2. Keep the biological interpretation
  language; discard the MATLAB/ode45 specifics.

**From Section 5.5 (Discussion):**
- The Travis personal communication (tank contamination anecdote). Preserve verbatim.
  Attribute as: "(J. Travis, personal communication)". Do NOT cite a dissertation.
- The interpretation of stochasticity as explaining field variability.
- The coexistence vs extinction speed-of-discrimination interpretation.

### 2.3 Self-Contained Introduction Requirement

The Introduction must be fully self-contained. No sentence may rely on a prior chapter.
Every concept must be introduced where it first appears. Specifically:
- The logistic growth term L must be defined in Section 2, not referenced from "Section 2.1"
  of a previous chapter.
- The parameter β must be defined in the model section, not via cross-reference.
- The concept of non-dimensionalization must be introduced with a brief motivation, not
  assumed as known.

---

## 3. Reference File

### 3.1 New File

Create file: `poecilia_references.bib`

All entries below are verified against primary sources (DOI, publisher page, or author
page). The agent MUST NOT add any entry not listed here or already in JBGInvasiveSpecies.bib.
If the manuscript requires a citation not covered by either file, insert a \textbf{[CITATION
NEEDED]} placeholder and a LaTeX comment noting what is needed — never fabricate.

```bibtex
%%
%% poecilia_references.bib
%% All entries verified against primary sources.
%%

@ARTICLE{Kokko2008,
  AUTHOR  = {H. Kokko and K. U. Heubel and D. J. Rankin},
  TITLE   = {How populations persist when asexuality requires sex:
             the spatial dynamics of coping with sperm parasites},
  JOURNAL = {Proceedings of the Royal Society B: Biological Sciences},
  VOLUME  = {275},
  NUMBER  = {1636},
  PAGES   = {817--825},
  YEAR    = {2008},
  DOI     = {10.1098/rspb.2007.1199},
}

@ARTICLE{Avise1991,
  AUTHOR  = {J. C. Avise and J. C. Trexler and J. Travis and W. S. Nelson},
  TITLE   = {\textit{Poecilia mexicana} is the recent female parent of the
             unisexual fish \textit{P.\ formosa}},
  JOURNAL = {Evolution},
  VOLUME  = {45},
  NUMBER  = {6},
  PAGES   = {1530--1533},
  YEAR    = {1991},
  DOI     = {10.1111/j.1558-5646.1991.tb02657.x},
}
%% NOTE: The dissertation records this as 1990; the correct year is 1991.
%% Use \cite{Avise1991} everywhere; do not use the dissertation's key.

@ARTICLE{Heubel2009,
  AUTHOR  = {K. U. Heubel and D. J. Rankin and H. Kokko},
  TITLE   = {How to go extinct by mating too much: population consequences of
             male mate choice and efficiency in a sexual--asexual species complex},
  JOURNAL = {Oikos},
  VOLUME  = {118},
  NUMBER  = {4},
  PAGES   = {513--520},
  YEAR    = {2009},
  DOI     = {10.1111/j.1600-0706.2008.17149.x},
}

@ARTICLE{Kiester1981,
  AUTHOR  = {A. R. Kiester and T. Nagylaki and B. Shaffer},
  TITLE   = {Population dynamics of species with gynogenetic sibling species},
  JOURNAL = {Theoretical Population Biology},
  VOLUME  = {19},
  NUMBER  = {3},
  PAGES   = {358--369},
  YEAR    = {1981},
  DOI     = {10.1016/0040-5809(81)90025-X},
}

@ARTICLE{Schley2004,
  AUTHOR  = {D. Schley and C. P. Doncaster and T. Sluckin},
  TITLE   = {Population models of sperm-dependent parthenogenesis},
  JOURNAL = {Journal of Theoretical Biology},
  VOLUME  = {229},
  NUMBER  = {4},
  PAGES   = {559--572},
  YEAR    = {2004},
  DOI     = {10.1016/j.jtbi.2004.04.031},
}

@ARTICLE{Peck1999,
  AUTHOR  = {J. R. Peck and J. Yearsley and G. Barreau},
  TITLE   = {The maintenance of sexual reproduction in a structured population},
  JOURNAL = {Proceedings of the Royal Society B: Biological Sciences},
  VOLUME  = {266},
  NUMBER  = {1431},
  PAGES   = {1857--1863},
  YEAR    = {1999},
  DOI     = {10.1098/rspb.1999.0862},
}

@ARTICLE{Riesch2008,
  AUTHOR  = {R. Riesch and I. Schlupp and M. Plath},
  TITLE   = {Female sperm limitation in natural populations of a
             sexual/asexual mating complex (\textit{Poecilia latipinna},
             \textit{Poecilia formosa})},
  JOURNAL = {Biology Letters},
  VOLUME  = {4},
  NUMBER  = {3},
  PAGES   = {266--269},
  YEAR    = {2008},
  DOI     = {10.1098/rsbl.2008.0019},
}

@INCOLLECTION{Balsano1989,
  AUTHOR    = {J. S. Balsano and E. M. Rasch and P. J. Monaco},
  TITLE     = {The evolutionary ecology of \textit{Poecilia formosa}
               and its triploid associate},
  BOOKTITLE = {Ecology and Evolution of Livebearing Fishes (\textit{Poeciliidae})},
  EDITOR    = {G. K. Meffe and F. F. {Snelson Jr.}},
  PAGES     = {277--297},
  PUBLISHER = {Prentice Hall},
  ADDRESS   = {Englewood Cliffs, NJ},
  YEAR      = {1989},
}

@INCOLLECTION{Wetherington1989,
  AUTHOR    = {J. D. Wetherington and R. A. Schneck and R. C. Vrijenhoek},
  TITLE     = {The origins and ecological success of unisexual
               \textit{Poeciliopsis}: The frozen niche variation model},
  BOOKTITLE = {Ecology and Evolution of Livebearing Fishes (\textit{Poeciliidae})},
  EDITOR    = {G. K. Meffe and F. F. {Snelson Jr.}},
  PAGES     = {259--275},
  PUBLISHER = {Prentice Hall},
  ADDRESS   = {Englewood Cliffs, NJ},
  YEAR      = {1989},
}

@ARTICLE{Snelson1980,
  AUTHOR  = {F. F. {Snelson Jr.} and J. D. Wetherington},
  TITLE   = {Sex ratio in the sailfin molly, \textit{Poecilia latipinna}},
  JOURNAL = {Evolution},
  VOLUME  = {34},
  NUMBER  = {2},
  PAGES   = {308--319},
  YEAR    = {1980},
  DOI     = {10.1111/j.1558-5646.1980.tb04817.x},
}

@BOOK{Oksendal2003,
  AUTHOR    = {B. {\O}ksendal},
  TITLE     = {Stochastic Differential Equations: An Introduction with Applications},
  EDITION   = {6th},
  PUBLISHER = {Springer},
  ADDRESS   = {Berlin},
  YEAR      = {2003},
  ISBN      = {978-3-540-04758-2},
}

@BOOK{KloedenPlaten1992,
  AUTHOR    = {P. E. Kloeden and E. Platen},
  TITLE     = {Numerical Solution of Stochastic Differential Equations},
  SERIES    = {Applications of Mathematics},
  VOLUME    = {23},
  PUBLISHER = {Springer},
  ADDRESS   = {Berlin},
  YEAR      = {1992},
  ISBN      = {978-3-540-54062-5},
}
```

### 3.2 Existing Bib Keys to Keep from JBGInvasiveSpecies.bib

The agent must check JBGInvasiveSpecies.bib for these keys and use them as-is if present:

| What it is | Expected key (search the bib for it) |
|---|---|
| Buckingham 1914 dimensional analysis | Search for: Buckingham |
| Marsden & Tromba Vector Calculus | Search for: Marsden |
| Strogatz Nonlinear Dynamics | Search for: Strogatz |

If any of these keys are missing from JBGInvasiveSpecies.bib, do NOT invent entries.
Insert \textbf{[CITATION NEEDED]} placeholder instead.

### 3.3 Preamble Citation Setup

```latex
\usepackage[numbers,sort&compress]{natbib}
\bibliographystyle{plainnat}
% At end of document:
\bibliography{JBGInvasiveSpecies,poecilia_references}
```

Use `\citep{}` for parenthetical and `\citet{}` for inline author-prominent citations.

### 3.4 Key Mapping from Dissertation to New File

| Dissertation key | New key to use |
|---|---|
| Kokko:persist | Kokko2008 |
| Avise:Formosa | Avise1991 |
| Heubel:extinct | Heubel2009 |
| Kiester:Gynogenetic | Kiester1981 |
| Schley:parthenogenesis | Schley2004 |
| Peck:maintenance | Peck1999 |
| Riesch:limitation | Riesch2008 |
| Balsano:Poecilia | Balsano1989 |
| Wetherington:Poeciliids | Wetherington1989 |
| Snelson:Sex | Snelson1980 |
| (SDE theory) | Oksendal2003 |
| (SDE numerics) | KloedenPlaten1992 |
| Gutierrez:Trojan | DELETE — do not replace |
| GTHT:PFormosa | DELETE — do not replace |

---

## 4. Appendix A — Code via lstinputlisting

### 4.1 Replace Appendix A Content

Appendix A in v2.0 contained narrative SymPy verification descriptions. Replace the
entire content of Appendix A with code listings. The section heading and preamble setup are:

```latex
% Preamble additions required:
\usepackage{listings}
\usepackage{xcolor}

\lstset{
  language=Python,
  basicstyle=\small\ttfamily,
  keywordstyle=\color{blue}\bfseries,
  commentstyle=\color{gray}\itshape,
  stringstyle=\color{teal},
  numberstyle=\tiny\color{gray},
  numbers=left,
  stepnumber=5,
  numbersep=8pt,
  frame=single,
  breaklines=true,
  breakatwhitespace=false,
  showspaces=false,
  showstringspaces=false,
  tabsize=4,
  captionpos=b,
}
```

```latex
\appendix
\section{Python Implementation}\label{app:code}

The complete implementation is organized as a flat collection of Python scripts.
All figures in this article can be reproduced by running \texttt{python run\_all.py}
after installing the packages listed in \texttt{requirements.txt}.
The scripts require Python 3.9 or later with \texttt{numpy}, \texttt{scipy},
\texttt{matplotlib}, and \texttt{sympy}.

\subsection*{Master Script}
\lstinputlisting[language=Python,caption={run\_all.py --- master script}]
  {poecilia_sde/run_all.py}

\subsection*{Parameters}
\lstinputlisting[language=Python,caption={params.py --- parameter dataclasses}]
  {poecilia_sde/params.py}

\subsection*{Deterministic Core}
\lstinputlisting[language=Python,caption={deterministic.py --- ODE right-hand side}]
  {poecilia_sde/deterministic.py}

\subsection*{RODE Solver}
\lstinputlisting[language=Python,caption={rode.py --- Random ODE solver}]
  {poecilia_sde/rode.py}

\subsection*{It\^{o} SDE Solver}
\lstinputlisting[language=Python,caption={sde\_ito.py --- Euler--Maruyama scheme}]
  {poecilia_sde/sde_ito.py}

\subsection*{Stratonovich SDE Solver}
\lstinputlisting[language=Python,caption={sde\_stratonovich.py --- Heun scheme}]
  {poecilia_sde/sde_stratonovich.py}

\subsection*{Moment Equations}
\lstinputlisting[language=Python,caption={moments.py --- closed moment ODE system}]
  {poecilia_sde/moments.py}

\subsection*{Stability Analysis}
\lstinputlisting[language=Python,caption={stability.py --- stability boundary computation}]
  {poecilia_sde/stability.py}

\subsection*{Figures}
\lstinputlisting[language=Python,caption={figures.py --- all figure-generating functions}]
  {poecilia_sde/figures.py}

\subsection*{Symbolic Verification}
\lstinputlisting[language=Python,caption={verification.py --- SymPy tasks V1--V9}]
  {poecilia_sde/verification.py}
```

### 4.2 Bordered Hessian Determinant

The bordered Hessian claim is simplified. The manuscript MUST state:

> One can verify that the determinant of the bordered Hessian evaluated at the critical
> point is $\beta^2 > 0$, confirming that this critical point is a constrained maximum.

Do NOT attempt to derive this symbolically in the text. Do NOT include a SymPy verification
of this value (remove task V3 from verification.py, or mark it as a separate check that
does not affect the main result). The claim $|\bar{H}| = \beta^2$ is asserted and the
positivity $\beta^2 > 0$ is the operative conclusion.

---

## 5. Bordered Hessian: In-Body Explanation at First Use

At the first occurrence of the bordered Hessian in the body (within the proof of the
Dissipative Stochasticity Lemma, Section 4.1), insert the following explanatory passage
**before** the matrix is displayed. This passage must appear as natural prose, not as a
separate subsection:

---

*Passage to insert (adapt to surrounding prose style):*

The analysis requires confirming that the critical point identified on the boundary of
the feasible region is a genuine constrained maximum of $P(\mathbf{u}) = \nabla \cdot F$,
and not merely a saddle point or local minimum. For unconstrained optimization, the
standard second-order test examines the Hessian matrix of the objective function: if the
Hessian is negative definite at a critical point, that point is a local maximum.
When, however, the optimization is constrained — here, to the invariant boundary face
$f + m + p = 1$ — the unconstrained Hessian is no longer the correct tool, because it
ignores the geometry of the constraint. The appropriate generalization is the
\textit{bordered Hessian} $\bar{H}$, which augments the Hessian of $P$ with an additional
row and column encoding the gradient of the constraint. Specifically, if the constraint is
$g(\mathbf{u}) = c$, the bordered Hessian is the $(n+1) \times (n+1)$ matrix
\begin{equation}
  \bar{H} = \begin{pmatrix} 0 & \nabla g^\top \\ \nabla g & H_P \end{pmatrix},
\end{equation}
where $H_P$ is the Hessian of $P$ and $\nabla g$ is the constraint gradient arranged as a
column vector. The sign of the determinant $|\bar{H}|$ determines the nature of the
constrained critical point: for a single equality constraint in three variables, a positive
determinant $|\bar{H}| > 0$ confirms a constrained maximum \citep{Marsden2003}. In the
present case, one can verify that $|\bar{H}| = \beta^2 > 0$, since $\beta > 0$ by
biological assumption. This confirms that the identified critical point is indeed the
constrained maximum of $P$ on the boundary, completing the second-order verification.

---

*Note on citation:* \citep{Marsden2003} refers to the Marsden \& Tromba Vector Calculus
text. Confirm the key in JBGInvasiveSpecies.bib. If the key is absent, use
\textbf{[CITATION NEEDED: Marsden \& Tromba, Vector Calculus]}.

---

## 6. Paragraph Titles — LaTeX Comment Format

All subsection-like paragraph bold titles in the manuscript body must be converted to
LaTeX comments. The paragraph text itself must follow immediately on the next line
without any heading tag.

**Rule:** Every place v2.0 instructed the agent to write a bold lead-in paragraph title
(such as **Common noise:**, **Itô:**, **Note on calibration:**, **Known limitation:**,
etc.) must be replaced with a comment line above the paragraph:

```latex
% Common environmental noise
```

**Exceptions:** True LaTeX `\section{}`, `\subsection{}`, and `\subsubsection{}` headings
are permitted and remain. Only inline paragraph-level bold labels are affected.

**Figures and tables:** Caption sub-labels (e.g., Panel A: ...) remain. Only body prose
paragraph titles are affected.

---

## 7. Proof Verbosity Standards

Every proof in the manuscript must meet the following minimum standards:

### 7.1 Structure Requirement

Each proof must contain these structural elements in order:

1. **Goal statement** (1–2 sentences): State plainly what is to be proved, in words,
   before any symbol appears.
2. **Setup** (1+ sentences): Define all symbols that appear in this proof and have not
   been defined in the surrounding text. State any assumptions being invoked.
3. **Derivation steps**: Each non-trivial step must be followed by a sentence explaining
   what was done and why. Never chain more than two algebraic manipulations without
   an intervening explanation.
4. **Conclusion**: End with a sentence of the form "Therefore, [the claimed result] holds,
   which completes the proof." or "This establishes [claim], as required." Do not end
   with a QED symbol alone.

### 7.2 Specific Standards by Proof

**Lemma 4.1 (Dissipative Stochasticity Lemma):**
- The computation of $\nabla \cdot F$ must be shown term by term. Do not collapse
  the three partial derivatives into one line.
- After computing each partial derivative, add a sentence explaining what that term
  represents biologically (e.g., "This term accounts for the rate at which an increase
  in $f$ reduces its own growth through the logistic factor $L$.").
- The factoring step must be shown explicitly with intermediate algebra visible.
- The threshold inequality must be derived from the condition $\nabla \cdot F < 0$ by
  showing each rearrangement step on its own line.
- The biological interpretation of the threshold must be given immediately after the
  mathematical conclusion: what does it mean for $\eta_f + \eta_m + \eta_p < 3$ in terms
  of noise amplitude relative to mortality?

**Proposition (Itô mean equations under mean-field closure):**
- Begin by stating what Itô's lemma says in general form for a function $h(X_t)$
  where $X_t$ satisfies an SDE. Do not assume this is known.
- Show the application to $h(f, m, p) = f$ explicitly, including the identification
  of the drift and diffusion terms.
- Show explicitly why the Itô integral has zero expectation (it is a martingale with
  zero mean), and why this justifies taking expectations of the drift term only.
- Show the mean-field closure step explicitly: write out $\mathbb{E}[f \cdot m]$ and
  then state the closure approximation $\approx \mathbb{E}[f] \cdot \mathbb{E}[m]$,
  explaining that this is exact only if $f$ and $m$ are uncorrelated.
- Conclude by stating what the result means: the mean dynamics under Itô noise with
  mean-field closure are identical to the deterministic system.

**Proposition (Stratonovich drift correction):**
- State the Itô–Stratonovich conversion theorem in full for the scalar case before
  applying it.
- Show the computation of the correction term $(1/2) g \cdot \partial g/\partial u$
  for each of the three equations separately. Do not write "by similar algebra" —
  show each one.
- Explain in words why the correction is positive for geometric noise (the correction
  acts as an effective additional birth rate term, biasing populations upward on average).

**Proposition (Lyapunov exponent for scalar p-subsystem, Itô):**
- State the general result for geometric Brownian motion: if $dp = \mu p\,dt + \sigma p\,dW$
  then $\ln p(t) / t \to \mu - \sigma^2/2$ almost surely as $t \to \infty$. Cite
  \citet{Oksendal2003} for this result.
- Explain why geometric Brownian motion is the relevant approximation for the $p$-equation
  near zero: when $p \to 0$, the logistic factor $L \to 1 - f_\infty - m_\infty > 0$
  and the mating term $m$ is approximately constant at its quasi-steady state.
- Define $\beta_\text{eff}$ explicitly in terms of the system parameters.
- Show why the stability condition $\lambda < 0$ gives $\sigma_p > \sqrt{2(\beta_\text{eff} - \delta)}$.
- Explain the biological interpretation: sufficiently intense Itô noise suppresses
  exponential growth of the parasite population, thereby protecting the host.

**Proposition (Lyapunov exponent for scalar p-subsystem, Stratonovich):**
- Apply the Itô–Stratonovich conversion to the scalar p-subsystem first.
- Show that the Stratonovich drift becomes $\beta_\text{eff} - \delta + (1/2)\sigma_p^2$,
  which is larger than the Itô drift.
- Show that the resulting Lyapunov exponent is $\lambda = \beta_\text{eff} - \delta$,
  independent of $\sigma_p$.
- Explain clearly why this independence arises: the Stratonovich correction exactly
  cancels the noise-induced suppression that appears in the Itô exponent.
- State the consequence: for Stratonovich noise, the stability boundary does not shift
  with increasing noise amplitude, unlike in the Itô case.

**Proposition (Non-equivalence of RODE and SDE stability thresholds):**
- This proof is a comparison argument, not an algebraic derivation. Structure it as:
  (i) State what the RODE threshold measures (phase-space contraction, Liouville's
  theorem argument); (ii) State what the Itô Lyapunov exponent measures (linearized
  growth rate of log p near extinction); (iii) Compute both numerically for the
  default parameter set; (iv) Observe they differ; (v) Conclude non-equivalence.
- Do not say "one can easily see." Show both numerical values explicitly.

### 7.3 General Prohibitions in Proofs

Never write:
- "It can be shown that..."
- "By standard results..."
- "The calculation is straightforward..."
- "One can verify..."
- "Similarly..."  (without showing the analogous steps for the remaining cases)
- "The proof is analogous to..."

Always write out the computation or argument fully, even at the cost of length.

---

## 8. Prose Expansion Standards

### 8.1 Introduction (target: 800–1200 words)

The current introduction in v2.0 is too thin. Expand to cover all of the following,
in order, as flowing prose without subsection headers:

**Paragraph 1 — The ecological paradox (required expansion):**
Begin with the broad puzzle: how can a sperm parasite coexist with its host when simple
ecological logic predicts the parasite should drive the host to extinction, thereby
destroying its own sperm supply and collapsing the entire system? This is not a
rhetorical question — explain the logic of the collapse: more parasites → more male
mating wasted → fewer bisexual offspring → declining male population → declining sperm
supply → parasite collapse too. Then state that field data contradict this collapse: P.
formosa has coexisted with P. mexicana and P. latipinna across a wide range of habitats
for an unknown but long evolutionary period.

**Paragraph 2 — The biology of P. formosa (required expansion):**
Introduce the species in detail. Explain what gynogenesis is, why P. formosa needs sperm
but does not use the genetic material, what "sperm parasite" means in operational terms.
Include the discovery (Hubbs and Hubbs 1932 via \citealt{Wetherington1989}), the
molecular confirmation (\citealt{Avise1991}), the geographic range (SE Texas, NE Mexico),
and the field data showing high variability in unisexual fraction across locations and
years (\citealt{Balsano1989}).

**Paragraph 3 — Prior mathematical models and their gaps:**
Survey the prior models (\citealt{Kiester1981}, \citealt{Schley2004}, \citealt{Peck1999},
\citealt{Kokko2008}, \citealt{Heubel2009}) with one sentence on each model's contribution
and one sentence on each model's limitation relative to the present work. Close with a
clear statement of the two gaps: (i) none account for the speed of discrimination as a
control variable; (ii) none produce the high field variability observed in the Balsano et
al. data through an intrinsic mechanism.

**Paragraph 4 — Male discrimination behavior (required expansion):**
Explain the discrimination mechanism in biological detail. Males of the host species
prefer conspecific females, but this preference is population-dependent: when the parasite
population is low, males mate with parasites at comparable rates to conspecifics; when
the parasite population is high, males strongly prefer conspecifics (\citealt{Riesch2008},
\citealt{Balsano1989}). Two explanations for this behavior exist in the literature:
"foreignness" (females are preferred when unfamiliar), and dominance hierarchies (dominant
males are more discriminating). The present model captures this population-dependence
through the sigmoid function $\gamma(p)$.

**Paragraph 5 — Stochastic modeling choice and contribution:**
State clearly what this paper adds: three stochastic frameworks (RODE, Itô SDE,
Stratonovich SDE), two noise structures, comparative analysis. Explain why the comparison
matters: different biological interpretations of noise (environmental buffering vs.
demographic noise) and different mathematical properties (RODE paths are smooth, SDE paths
are nowhere differentiable) lead to different quantitative predictions for stability. The
choice of framework is therefore not merely a technical preference — it has biological
consequences.

**Paragraph 6 — Paper structure:**
One paragraph listing what each section contains.

### 8.2 Discussion (target: 1500–2000 words; four substantive paragraphs)

**Paragraph 1 — Speed of discrimination is the master variable:**
Minimum 350 words. Explain the finding thoroughly. What does "speed of discrimination"
mean biologically — is it a learned behavior, an evolved trait, a developmental response?
What does the mathematical result say: below some critical speed the system goes to
extinction regardless of initial conditions; above it, coexistence is the attractor. Connect
this to the field observation that some populations coexist and others go extinct. Speculate
on what drives variation in discrimination speed across field populations (population
density, exposure history, resource availability, temperature). Discuss whether the result
is formulation-robust — it is — and what that means: this conclusion is unlikely to be an
artifact of modeling choices.

**Paragraph 2 — Noise structure and formulation-dependence:**
Minimum 400 words. Discuss the Itô vs Stratonovich distinction in biological terms. The
Wong-Zakai theorem suggests that when the environmental signal driving population
fluctuations has finite correlation time (e.g., seasonal flooding with a timescale of weeks),
the Stratonovich interpretation is the correct limit. For P. formosa, the habitat
connectivity fluctuations (pools connecting and disconnecting across dry/wet season) have
a correlation time of months — not infinitesimally short. This favors Stratonovich. But
the key result is that the Stratonovich Lyapunov exponent is noise-independent, meaning
that environmental noise of the Stratonovich type does not provide the stabilizing effect
that Itô noise does. Discuss what this means for conservation: if Stratonovich is correct,
noise-induced stabilization of the host is not available, and the only stabilizing mechanism
is discrimination speed. This is a sobering conclusion. Connect to the RODE result: the
RODE dissipative threshold is a different kind of stability, based on phase-space
contraction rather than linearized growth, and the two concepts disagree on where the
stability boundary lies. This disagreement is not a modeling failure — it reveals that
"stability" is not a single concept and different stability measures give different
answers for the same biological system.

**Paragraph 3 — Field data and model validation:**
Minimum 350 words. Return to the Balsano et al. (1989) field data: proportion of
unisexuals varying from near 0 to near 1 across 20 locations over 8 years. The ensemble
variance from the non-dissipative RODE case, and from the high-σ Itô case, is consistent
with this level of variability. However, the model makes no prediction about which
locations will be in which regime — that requires spatial data on discrimination speed and
habitat connectivity, which are not yet available. Note the Travis personal communication
(J. Travis, personal communication): the tank contamination experiment shows that even
small initial inocula of P. formosa can eventually take over a closed system, consistent
with the model's prediction that extinction is inevitable without sufficient discrimination.
Discuss limitations: the model does not include spatial structure (Kokko et al. 2008
showed this matters), does not include predation, and assumes logistic growth with a single
carrying capacity.

**Paragraph 4 — Implications for the gynogenetic eradication strategy:**
Minimum 350 words. If sperm parasites can be controlled by manipulating the discrimination
speed or the noise environment, what practical interventions are possible? Discuss the
eradication strategy concept: introducing males that preferentially mate with conspecifics
(discrimination-enhancing) or manipulating habitat connectivity to reduce effective
population size (increasing effective noise). The model predicts that increasing
discrimination speed past the critical threshold should shift the system from the extinction
basin to the coexistence basin — this is a testable prediction in aquaria. Contrast with
the finding that stochasticity alone (without discrimination) is insufficient for
coexistence in the Stratonovich case. This narrows the intervention target: discrimination
speed is the essential variable.

### 8.3 Conclusions (target: 600–900 words; minimum four paragraphs)

Each paragraph must correspond to one main finding. Do not use a bullet list. Each
paragraph must:
- State the finding in the first sentence
- Explain why it is significant (not merely that it is "consistent" or "interesting")
- Connect it to the broader literature
- State one testable prediction or direction for future work

**Paragraph 1 — Discrimination speed:**
Finding: the speed of the sigmoid discrimination function $\gamma(p)$ is the primary
determinant of extinction vs coexistence, and this conclusion is robust across all five
stochastic formulations tested. Significance: this reframes the coexistence problem from
one about stochasticity (which can be hard to control) to one about behavior (which is
measurable and potentially evolvable). Connection: Heubel et al. (2009) showed that male
efficiency matters; the present work shows that the shape of the discrimination function
matters, not just its asymptotic value. Testable prediction: populations with slower
discrimination response (lower $v$) should have higher extinction rates in mesocosm
experiments, independent of initial density.

**Paragraph 2 — Itô vs Stratonovich divergence:**
Finding: Itô noise induces noise-stabilization (the Lyapunov exponent decreases with σ)
while Stratonovich noise is stability-neutral for the scalar p-subsystem. Significance:
the choice of stochastic interpretation has biological consequences, not just mathematical
ones. Connection: the Wong-Zakai theorem provides theoretical grounding for preferring
Stratonovich when environmental drivers have finite correlation time. Testable prediction:
mesocosm experiments with controlled environmental fluctuation timescales could in
principle distinguish Itô-like (fast forcing) from Stratonovich-like (slow forcing)
dynamics by examining whether noise amplitude affects extinction rate.

**Paragraph 3 — Mean-field closure and moment structure:**
Finding: under mean-field closure, Itô noise does not shift ensemble means relative to
the deterministic system, while Stratonovich noise shifts means upward by
$(1/2)\sigma_i^2 \mathbb{E}[u_i]$ per component. Significance: this explains why
single-trajectory simulations and ensemble averages can look qualitatively different and
why the choice of summary statistic matters for comparing model output to field data.
Future work: the closure error is less than 10\% for the parameters studied here, but
formal analysis of closure accuracy for non-Gaussian population distributions (as arise
near extinction) remains an open problem.

**Paragraph 4 — RODE/SDE incommensurability:**
Finding: the RODE dissipative threshold and the Itô Lyapunov threshold are analytically
distinct concepts that cannot be directly compared without an empirical calibration,
and even after calibration they predict different stability boundaries. Significance:
this is a general result — any model using piecewise-constant parametric noise should
be carefully distinguished from models using Wiener-process noise, as the two frameworks
have structurally different stability theories. Recommendation: future ecological
modeling papers that use stochastic ODE simulation should explicitly state which
stochastic framework they are using and justify the choice biologically.

---

## 9. Summary of All Changes Relative to v2.0 + SPECS2

| Item | v2.0/SPECS2 | SPECS3 |
|---|---|---|
| Title | Fixed generic title | 5 options; use Option A as default |
| "TXC" / "Trojan" | Present throughout | Purged; map to verified terminology |
| Dissertation cite | Present | Deleted, not replaced |
| Reference file | Not provided | poecilia_references.bib (verified entries) |
| Year: Avise et al. | 1990 (wrong) | 1991 (correct) |
| Appendix A | Narrative SymPy descriptions | lstinputlisting code blocks |
| Bordered Hessian determinant | SymPy verification task V3 | Asserted as β²; V3 removed |
| Bordered Hessian explanation | Not present | In-body prose at first use |
| Paragraph titles | Bold inline labels | % LaTeX comments |
| Proof style | Compressed | Fully verbose; step-by-step |
| Introduction length | Thin (~400 words implied) | 800–1200 words |
| Discussion length | 4 paragraphs, thin | 4 paragraphs, 350–400 words each |
| Conclusions | Not specified | 4 paragraphs × 150+ words each |

---

*End of SPECS3. Governs v2.0 + SPECS2 where in conflict.*
