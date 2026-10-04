p = '/home/touhid/Documents/texflowmcp/workspace/document.tex'
t = open(p).read()
orig = t

# 1. unify champion numbers
t = t.replace('300 & 1.234 & 21.19 & 89.87 & 23.50 \\\\',
              '300 & 1.234 & 21.19 & 89.78 & 23.49 \\\\')
t = t.replace('Champion & 23.50 & 25.16 & +1.66 \\\\',
              'Champion & 23.49 & 25.16 & +1.67 \\\\')

# 2. extend determinism sentence with Nc/Nv cap, Rs equation, reconcile, Nt12 failure
old = 'a duplicate champion run reproduces 23.5041\\% exactly, confirming determinism.'
new = ('a duplicate champion run reproduces the coarse-grid value 23.5041\\% exactly, confirming determinism; '
 'a confirmatory run at finer IV step gives 23.4874\\% (FF 89.78\\%), reported as 23.49\\% throughout. '
 'Absorber densities of states are capped at $N_c=1.1\\times10^{19}$/$N_v=8.2\\times10^{19}$~cm$^{-3}$, '
 'ten times below the Table-1 print ($10^{20}$~cm$^{-3}$, above solid density and hence unphysical). '
 'The disclosed resistance derate multiplies efficiency by $(1+J_{sc}R_s/\\mathrm{FF}_0V_{oc})^{-1}$, '
 'equal to 0.965 at $R_s=1~\\Omega$cm$^2$. '
 'One exploratory combined NA+Nt run returned no result file (worker crash) and was excluded; '
 'the combination was re-measured successfully in the retry series.')
assert old in t
t = t.replace(old, new)

# 3. cite contour in Sec 3 interaction discussion
old = 'which single-variable sweeps cannot resolve.'
assert old in t
t = t.replace(old, 'which single-variable sweeps cannot resolve (Fig.~\\ref{fig:contour}).')

# 4. move contour figure from surrogate section to champion section (before its first cite):
# cut block, paste after champion table
start = t.find('\\label{fig:contour}')
bstart = t.rfind('\\begin{figure}', 0, start)
bend = t.find('\\end{figure}', start) + len('\\end{figure}')
block = t[bstart:bend]
t = t[:bstart] + t[bend:]
anchor = 'reproducing the published 17.9--19.06\\% band and validating the harness.'
assert anchor in t
# instead: place after champion Table 1 -> find end of tab:champ table
tanchor = '\\label{tab:champ}'
ta = t.find(tanchor)
te = t.find('\\end{table}', ta) + len('\\end{table}')
t = t[:te] + '\n\n' + block + t[te:]

# 5. EB+GR side by side
eb = ('\\begin{figure}[tbp]\n\\centering\n'
      '\\includegraphics[width=0.8\\textwidth]{/home/touhid/Documents/leadpaper/outputs/figs/fig_EB.png}\n'
      '\\caption{Illuminated band diagram of the champion at short circuit (x=0 at the back contact).}\n'
      '\\label{fig:eb}\n\\end{figure}')
gr = ('\\begin{figure}[tbp]\n\\centering\n'
      '\\includegraphics[width=0.8\\textwidth]{/home/touhid/Documents/leadpaper/outputs/figs/fig_GR.png}\n'
      '\\caption{Generation and recombination profiles at short circuit (log scale).}\n'
      '\\label{fig:gr}\n\\end{figure}')
assert eb in t and gr in t
pair = ('\\begin{figure}[tbp]\n\\centering\n'
        '\\begin{minipage}{0.48\\textwidth}\n\\centering\n'
        '\\includegraphics[width=\\textwidth]{/home/touhid/Documents/leadpaper/outputs/figs/fig_EB.png}\n'
        '\\caption{Illuminated band diagram of the champion at short circuit.}\n'
        '\\label{fig:eb}\n\\end{minipage}\\hfill\n'
        '\\begin{minipage}{0.48\\textwidth}\n\\centering\n'
        '\\includegraphics[width=\\textwidth]{/home/touhid/Documents/leadpaper/outputs/figs/fig_GR.png}\n'
        '\\caption{Generation and recombination profiles (log scale).}\n'
        '\\label{fig:gr}\n\\end{minipage}\n\\end{figure}')
t = t.replace(eb + '\n\n' + gr, pair)

open(p, 'w').write(t)
print('edits applied, changed:', t != orig)
