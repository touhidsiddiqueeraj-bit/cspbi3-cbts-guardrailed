p = '/home/touhid/Documents/texflowmcp/workspace/document.tex'
t = open(p).read()
n0 = len(t)
FIG = '/home/touhid/Documents/leadpaper/outputs/figs/'

def ins(anchor, add, after=True):
    global t
    assert anchor in t, anchor[:70]
    if after:
        i = t.find(anchor) + len(anchor)
        t = t[:i] + '\n\n' + add + t[i:]
    else:
        i = t.find(anchor)
        t = t[:i] + add + '\n\n' + t[i:]

# ---- A. JV overlay figure + gain-stacking paragraph (champion section) ----
jv = (r'''\begin{figure}[tbp]
\centering
\includegraphics[width=0.85\textwidth]{FIGfig_JVboth.png}
\caption{Illuminated current--voltage curves: baseline (800~nm, 18.99\%) versus champion (2.2~$\mu$m, 23.49\%).}
\label{fig:jvboth}
\end{figure}

The 4.50-point stacked gain decomposes along the optimisation path (Fig.~\ref{fig:jvboth}): thickness 800~nm to 1.5~$\mu$m adds 0.19 points (19.18\%), acceptor doping to $10^{16}$~cm$^{-3}$ adds 0.93 points (20.11\%), bulk-defect reduction to $10^{12}$~cm$^{-3}$ adds $\sim$1.6 points ($\sim$21.7\%), and the joint $E_g$--$\chi$ move to 1.65~eV with ETL donor optimisation contributes the remaining $\sim$1.8 points. Open-circuit voltage climbs 1.122 to 1.234~V while the fill factor rises 86.0 to 89.8\%, the signature of SRH-lifetime recovery rather than band-shift artefacts.'''.replace('FIG', FIG))
anchor = 'with a Voc deficit of 0.42~V against $E_g/q$---typical of realistic rather than idealised cells.'
assert anchor in t
t = t.replace(anchor, anchor + '\n\n' + jv)

# ---- B. audit mechanism + derate table ----
mech = r'''\subsection{Where the missing points go}

The inflation is almost entirely a Voc effect ($+$0.13~V) with Jsc unchanged to within 0.02~mA/cm$^2$: removing the $10^{10}$~cm$^{-2}$ interface states eliminates the dominant SRH channel at the heterojunctions, unpinning the quasi-Fermi splitting toward the radiative limit. Fill factor moves non-monotonically (89.8 to 87.0\% on the champion) as the recombination profile reshapes. The analytic resistance derate applied to the guarded champion is tabulated below.

\begin{table}[tbp]
\centering
\caption{Guarded champion under analytic series-resistance derate.}
\label{tab:rs}
\begin{tabular}{llll}
\hline
$R_s$ ($\Omega$cm$^2$) & PCE (\%) & vs 22.02\% cert. & Status \\
\hline
0 & 23.49 & +1.47 & SCAPS upper bound \\
0.5 & 23.08 & +1.06 & realistic good contact \\
1.0 & 22.68 & +0.66 & realistic typical \\
2.0 & 21.93 & $-$0.09 & below record \\
\hline
\end{tabular}
\end{table}'''
anchor = 'numbers are reproducible artefacts of an omitted loss channel.'
assert anchor in t
t = t.replace(anchor, anchor + '\n\n' + mech)

# ---- C. experimental roadmap section before Limitations ----
road = r'''\section{Experimental roadmap}

A laboratory translation can follow demonstrated routes for each layer. The TiO2 electron contact is deposited by chemical-bath or spray pyrolysis at 30~nm with niobium or donor doping toward $9\times10^{17}$~cm$^{-3}$; the CsPbI3 absorber follows the dimethylammonium-iodide intermediate route with propyltriethoxysilane-assisted crystallisation that already delivered 22.60\% in the laboratory~\cite{Dai2026}, targeting 2.0--2.2~$\mu$m films with bulk lifetimes consistent with $N_t\sim10^{12}$~cm$^{-3}$ (single-crystal-grade grains, verified by time-resolved photoluminescence). Interface passivation uses the fluorinated-dipole~\cite{Qiu2025} or dual-interface co-passivation~\cite{Zhang2026} chemistries to approach the modelled $10^{10}$~cm$^{-2}$ state density, and CBTS is sputtered at 100~nm with $N_A\sim10^{18}$~cm$^{-3}$ before Ni evaporation. In-line controls map directly onto the paper's figures: QE edge at 752~nm (Fig.~\ref{fig:qe}), Mott--Schottky depletion collapse near 0.5~V (Fig.~\ref{fig:cv}), and the temperature coefficient from Table~\ref{tab:temp} ($-0.29$\%/K in PCE over 300--400~K). Hitting all four simultaneously reproduces the 23.49\% upper bound; missing any one lands on the corresponding contour of Fig.~\ref{fig:contour}.'''
ins(r'\section{Limitations and outlook}', road, after=False)

# ---- D. back matter before appendix ----
back = r'''\section{Data availability}

All definition files (\texttt{csPbI3-CBTS-r7.def} with interfaces, \texttt{csPbI3-CBTS-noIF.def} without), sweep receipts (\texttt{roundA.jsonl}, \texttt{roundB.jsonl}, \texttt{char.jsonl}), raw curves (\texttt{champion\_JV.json}), analysis (\texttt{analysis.json}) and figure scripts are archived with the project under \texttt{leadpaper/} (directories \texttt{defs/}, \texttt{outputs/}, \texttt{receipts/}, \texttt{logs/}). No intermediate data were held in temporary storage.

\section{Author contributions}

The authors designed the factorial study, built the SCAPS definition files, executed the simulation campaign, performed the audit and surrogate analysis, and wrote the manuscript.

\section*{Acknowledgements}

The SCAPS-1D program was kindly provided by Prof.~M.~Burgelman of the University of Gent. Simulation time was provided by local workstation hardware (four parallel workers).'''
ins(r'\section{Appendix: the scripting unit trap}', back, after=False)

open(p, 'w').write(t)
print('expanded2, delta chars:', len(t) - n0)
