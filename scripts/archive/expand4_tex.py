import re
p = '/home/touhid/Documents/texflowmcp/workspace/document.tex'
t = open(p).read()
n0 = len(t)

# cite the 3 remaining keys in the ML comparison paragraph
old = 'The ranking agrees with Bayesian optimisation on CsSnI3, where absorber defect density likewise dominates (mean $|$SHAP$|=3.21$ versus 1.67 for thickness) and the optimal thickness shifts with $N_t$~\\cite{PerovskiteOpt2026} (Table~\\ref{tab:mlcmp}).'
assert old in t
new = ('The ranking agrees with Bayesian optimisation on CsSnI3, where absorber defect density likewise dominates '
 '(mean $|$SHAP$|=3.21$ versus 1.67 for thickness) and the optimal thickness shifts with $N_t$~\\cite{PerovskiteOpt2026} '
 '(Table~\\ref{tab:mlcmp}). Independent surrogate studies concur: FAPbI3 with a CsSnI3 hole contact reaches 23.94\\% with '
 'defect density as the leading feature~\\cite{Azar2023}, surface-passivated CsPbI3 cells confirm that interface-adjacent '
 'defects gate the voltage~\\cite{Li2018}, and the 7182-configuration open dataset now makes such cross-study surrogate '
 'comparisons routine~\\cite{Zenodo2025}.')
t = t.replace(old, new)

# widen body figures 0.8 -> 0.88 (keep side-by-side pair as is)
t = t.replace('\\includegraphics[width=0.8\\textwidth]{/home/touhid/Documents/leadpaper/outputs/figs/',
              '\\includegraphics[width=0.88\\textwidth]{/home/touhid/Documents/leadpaper/outputs/figs/')

open(p, 'w').write(t)
print('expanded4, delta chars:', len(t) - n0)
