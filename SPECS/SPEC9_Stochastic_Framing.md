# SPEC 9 — Stochastic Formulations: Biological Framing Update

## Status: READY AFTER SPEC 8 IS COMPLETE
## Target files: `poecilia_manuscript.tex` (Sections 3 and 4 only)
## Depends on: SPEC 8 (terminology changes must be applied first)
## Must be completed before: SPEC 10

---

## 1. CONTEXT AND MOTIVATION

Section 3 (Stochastic Formulations) and Section 4 (Analysis) of the
manuscript contain biological framing language that still uses the old
phenomenological vocabulary and occasionally refers to the model's
origin in ways that are now superseded by the mechanistic derivation
in SPEC 8.

This SPEC makes targeted prose updates to Sections 3 and 4:
- Tightens the biological interpretation of $\gamma$ to match the
  per-encounter acceptance probability framing from SPEC 8.
- Updates RODE noise-structure justification language to use new terminology.
- Adds a sentence in the Stratonovich remark connecting noise-induced
  growth bias to the specific context of host–parasite population dynamics.
- No equations change. No code changes.

---

## 2. TARGETED PROSE CHANGES — Section 3

### 2.1 RODE noise structure paragraph (currently ~line 359)

Locate the paragraph beginning:
> "Experimental data on fish association in populations containing
> *P. formosa* show that bisexual females associate preferentially..."

Replace with:

```latex
Experimental data on fish association in populations containing
\textit{P.~formosa} show that host females associate preferentially
in small groups of their own kind, and dominant males direct
approximately one third of their activity toward females with
preference for conspecifics~\citep{Balsano1989}.  These spatial
clustering patterns create a population-dependent bias in exposure
to environmental perturbations: host populations cluster more tightly
and are therefore less exposed to stochastic environmental effects
than parasite females.  To reflect this, the noise amplitudes are
structured as $\tilde{\eta}_f = \tilde{\eta}_m = (2/3)\tilde{\eta}$
and $\tilde{\eta}_p = \tilde{\eta}$: the parasite female population
bears the full environmental noise load, while host populations bear
two-thirds of it.
```

### 2.2 Relationship Between Formulations subsection (~line 465)

At the end of the `\begin{remark}[Noise-induced growth bias]` block,
append the following sentence before `\end{remark}`:

```latex
In the host--parasite context, this bias is ecologically meaningful:
under Stratonovich noise, environmental stochasticity provides an
effective growth bonus to all three populations, and the \emph{relative}
bonus is largest for whichever population is currently smallest---a
mechanism that can delay or prevent extinction independently of the
deterministic discrimination dynamics.
```

### 2.3 RODE-to-SDE Calibration subsection (~line 485)

Locate the sentence:
> "The RODE and SDE formulations are not related by a simple parameter
> substitution."

Add the following sentence immediately after it:

```latex
This incommensurability is itself a finding: it means that conclusions
about extinction probability in the host--parasite complex depend
quantitatively on the choice of stochastic framework, even when all
formulations share the same deterministic skeleton.
```

---

## 3. TARGETED PROSE CHANGES — Section 4

### 3.1 RODE Boundary Dissipativity Lemma context (~line 503)

Locate the paragraph opening Section 4.1:
> "The following result characterizes the dissipative behavior of
> the RODE system at the population ceiling."

Replace the second sentence ("It applies specifically to the RODE
formulation...") with:

```latex
It applies specifically to the RODE formulation---a pathwise,
Liouville-based phase-space contraction argument---and does not
extend directly to It\^{o} or Stratonovich SDEs.  Ecologically,
the lemma identifies the noise regime in which the host--parasite
complex is self-correcting at the carrying capacity: when the sum
of noise amplitudes exceeds the dissipative threshold, environmental
fluctuations can push populations through the ceiling and generate
persistent excursions rather than bounded oscillations.
```

### 3.2 Stratonovich mean equation remark (~line 479)

Locate `\begin{remark}[Noise-induced growth bias]` and its content:
> "Under mean-field closure, Itô noise does not shift ensemble
> means..."

Append before `\end{remark}`:

```latex
For the host--parasite system, Proposition~\ref{prop:strat_means}
implies that under Stratonovich noise the parasite female population
receives an effective growth increment of $+\tfrac{1}{2}\sigma_p^2 P$
per unit time.  Since $\sigma_p > \sigma_f = \sigma_m$ by calibration
(Table~\ref{tab:calibration}), this increment is largest for the
parasite population, providing a noise-mediated growth advantage that
partially offsets the deterministic suppression from male discrimination.
This is the mechanism by which noise can save the sperm parasite.
```

---

## 4. SECTION 3 INTRODUCTORY SENTENCE UPDATE

Locate the opening of Section 3 (`\section{Stochastic Formulations}`).
After the section heading, locate the first paragraph of
`\subsection{Random ODE (RODE) Formulation}` and ensure it opens by
referring to the mechanistic model derived in Section 2:

If the subsection opens with a sentence about RODE replacing something,
insert the following as a new first sentence of Section 3 (before the
RODE subsection heading):

```latex
The deterministic skeleton derived in Section~\ref{sec:deterministic}
is now extended to three stochastic formulations, each encoding a
different assumption about how environmental variability enters the
host--parasite dynamics.
```

---

## 5. ACCEPTANCE CRITERIA

After implementation:

1. `pdflatex poecilia_manuscript.tex` compiles without errors or
   new warnings.
2. The words "bisexual" and "unisexual" do not appear in Sections 3
   or 4 in active prose.
3. All `\ref` and `\cite` commands in modified paragraphs still resolve.
4. No equation environments have been altered.
5. The RODE noise-structure paragraph correctly reads "host females"
   and "parasite females" throughout.

---

## 6. DO NOT CHANGE

- Any `\begin{align}`, `\begin{equation}`, or `\begin{algorithm}` blocks.
- Any `\label` or `\ref` identifiers.
- The `\begin{proof}` blocks for Propositions 1 and 2.
- The Lemma statement and its proof.
- Sections 1, 2, 5, 6, 7 (those belong to SPEC 8 and SPEC 10).
- Any Python source files.
- Any `.bib` files.
