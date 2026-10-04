p = '/home/touhid/Documents/texflowmcp/workspace/document.tex'
t = open(p).read()
n0 = len(t)

add = r'''Round~B's refinement is documented in full because its plateau is itself evidence of convergence: the best ten span only 23.32--23.50\% (Table~\ref{tab:top10b}), with thickness 1.8--2.2~$\mu$m and $N_A$ (1--3)$\times10^{16}$~cm$^{-3}$ statistically tied once $N_t=10^{12}$~cm$^{-3}$ and $E_g=1.65$~eV are fixed. The $N_t=3\times10^{12}$~cm$^{-3}$ entries trail by $\sim$0.05 points, confirming the defect floor binds the optimum.

\begin{table}[tbp]
\centering
\caption{Round~B leaderboard (best ten of 36; $N_{D,\mathrm{ETL}}=9\times10^{17}$~cm$^{-3}$).}
\label{tab:top10b}
\begin{tabular}{lllll}
\hline
$d$ ($\mu$m) & $N_A$ & $N_t$ & $E_g$ & PCE \\
\hline
2.2 & 3e16 & 1e12 & 1.65 & 23.50 \\
2.0 & 3e16 & 1e12 & 1.65 & 23.49 \\
2.2 & 1e16 & 1e12 & 1.65 & 23.48 \\
2.0 & 1e16 & 1e12 & 1.65 & 23.47 \\
1.8 & 3e16 & 1e12 & 1.65 & 23.47 \\
2.2 & 3e16 & 3e12 & 1.65 & 23.45 \\
1.8 & 1e16 & 1e12 & 1.65 & 23.45 \\
2.0 & 3e16 & 3e12 & 1.65 & 23.44 \\
1.8 & 3e16 & 3e12 & 1.65 & 23.42 \\
2.2 & 1e16 & 3e12 & 1.65 & 23.32 \\
\hline
\end{tabular}
\end{table}'''
anchor = 'i.e.\\ the landscape is converged rather than climbing.'
assert anchor in t
t = t.replace(anchor, anchor + '\n\n' + add)
open(p, 'w').write(t)
print('expanded5, delta chars:', len(t) - n0)
