p = '/home/touhid/Documents/texflowmcp/workspace/document.tex'
t = open(p).read()
n0 = len(t)

# 1. ML comparison table + paragraph
mlc = r'''The ranking agrees with Bayesian optimisation on CsSnI3, where absorber defect density likewise dominates (mean $|$SHAP$|=3.21$ versus 1.67 for thickness) and the optimal thickness shifts with $N_t$~\cite{PerovskiteOpt2026} (Table~\ref{tab:mlcmp}).

\begin{table}[tbp]
\centering
\caption{Defect-dominance across absorbers and methods.}
\label{tab:mlcmp}
\begin{tabular}{lll}
\hline
Study & Absorber / method & Top driver \\
\hline
PerovskiteOpt-AI & CsSnI3 / GP-BO + SHAP & $N_t$ ($|$SHAP$|$ 3.21) \\
Multilayer screen & mixed / XGBoost + SHAP & absorber $E_g$, HTL gap \\
This work & CsPbI3-CBTS / factorial + RF & $\log N_t$ (0.48) \\
\hline
\end{tabular}
\end{table}'''
anchor = 'its first quantification for CsPbI3-CBTS.'
assert anchor in t
t = t.replace(anchor, anchor + '\n\n' + mlc)

# 2. process table in roadmap
proc = r'''
\begin{table}[tbp]
\centering
\caption{Laboratory translation: steps, targets, and in-line controls.}
\label{tab:fab}
\begin{tabular}{lll}
\hline
Step & Target & Control (this paper) \\
\hline
TiO2 by CBD/spray & 30~nm, $N_D$ 9e17 & CBO +0.07~eV \\
CsPbI3 via DMAI+PTES & 2.0--2.2~$\mu$m, $N_t\sim$1e12 & QE edge 752~nm \\
Interface passivation & $10^{10}$~cm$^{-2}$ & TRPL lifetime \\
CBTS sputtered & 100~nm, $N_A$ 1e18 & Mott--Schottky \\
Ni evaporation & 5.5~eV, $R_s\le1$ & Table~\ref{tab:rs} \\
\hline
\end{tabular}
\end{table}'''
anchor = 'missing any one lands on the corresponding contour of Fig.~\\ref{fig:contour}.'
assert anchor in t
t = t.replace(anchor, anchor + '\n\n' + proc)

# 3. reproducibility inventory appendix
inv = r'''\section*{Appendix B: run inventory}

\begin{table}[tbp]
\centering
\caption{Simulation batches archived under \texttt{leadpaper/}.}
\label{tab:runs}
\begin{tabular}{lll}
\hline
Batch & Configurations & Receipt \\
\hline
Baseline validation & 4 (one worker-crash retry) & \texttt{baseline\_results.json} \\
Unit diagnostics & 6 + 4 retries & \texttt{diag\_units.json} \\
Round~A factorial & 96 & \texttt{roundA.jsonl} \\
Round~B refine & 36 & \texttt{roundB.jsonl} \\
Characterisation + audit + T & 17 + 6 re-runs & char.jsonl (126 converged runs feed the ML surrogate) \\
\hline
\end{tabular}
\end{table}'''
anchor = 'the archived logs record both.'
assert anchor in t
t = t.replace(anchor, anchor + '\n\n' + inv)

open(p, 'w').write(t)
print('expanded3, delta chars:', len(t) - n0)
