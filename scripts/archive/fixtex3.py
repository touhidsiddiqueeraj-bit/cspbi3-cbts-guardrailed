import re
p = '/home/touhid/Documents/texflowmcp/workspace/document.tex'
t = open(p).read()

# 1. merge JV figures: delete champion-only block, keep JVboth
s = t.find('\\label{fig:jv}')
b = t.rfind('\\begin{figure}', 0, s)
e = t.find('\\end{figure}', s) + len('\\end{figure}')
assert 'champion_JV.png' in t[b:e]
t = t[:b] + t[e:].lstrip('\n')
t = t.replace('(Fig.~\\ref{fig:jv})', '(Fig.~\\ref{fig:jvboth})')
t = t.replace('Fig.~\\ref{fig:jv}', 'Fig.~\\ref{fig:jvboth}')

# 2. audit numbers: +1.66, coarse/fine wording
t = t.replace('Champion & 23.49 & 25.16 & +1.67 \\\\',
              'Champion & 23.49 & 25.16 & +1.66 \\\\')
t = t.replace("23.50 to 25.16\\% (Fig.~\\ref{fig:audit})",
              "23.50\\% coarse (23.49\\% fine) to 25.16\\% (Fig.~\\ref{fig:audit})")

# 3. Rs table recompute (factor 1/(1+Jsc*Rs/FF0*Voc), Jsc=21.19mA, FF0=0.8978, Voc=1.234)
t = t.replace('0.5 & 23.08 & +1.06 & realistic good contact \\\\',
              '0.5 & 23.27 & +1.25 & realistic good contact \\\\')
t = t.replace('1.0 & 22.68 & +0.66 & realistic typical \\\\',
              '1.0 & 23.05 & +1.03 & realistic typical \\\\')
t = t.replace('2.0 & 21.93 & $-0.09$ & below record \\\\',
              '2.0 & 22.62 & +0.60 & still above record \\\\')
t = t.replace('($\\sim$22.68\\%) after a disclosed series-resistance derate',
              '($\\sim$23.05\\% at $R_s=1~\\Omega$cm$^2$) after a disclosed series-resistance derate')
t = t.replace('remaining above it ($\\sim$22.68\\%) after a disclosed series-resistance derate',
              'remaining above it ($\\sim$23.05\\% at $R_s=1~\\Omega$cm$^2$) after a disclosed series-resistance derate')
t = t.replace('The disclosed Rs derate ($\\times0.965$ at Rs$\\sim$1~$\\Omega$cm$^2$)',
              'The disclosed Rs derate ($\\times0.981$ at $R_s=1~\\Omega$cm$^2$)')
t = t.replace('clearing the 22.02\\% certified record up to $\\sim$1~$\\Omega$cm$^2$, the practical value used in comparable studies',
              'clearing the 22.02\\% certified record up to $\\sim$2~$\\Omega$cm$^2$, covering the practical range used in comparable studies')
t = t.replace('($\\sim$22.68\\%, the practical value',
              '($\\sim$23.05\\%, the practical value')

# 4. FF 87.05 with explicit provenance
t = t.replace('Fill factor moves non-monotonically (89.8 to 87.0\\%) on the champion) as the recombination profile reshapes.',
              'Fill factor moves non-monotonically (89.87 to 87.05\\% on the champion, char.jsonl) as the recombination profile reshapes.')

# 5. EB/GR back to stacked full width
pair_start = t.find('minipage')
assert pair_start != -1
b = t.rfind('\\begin{figure}', 0, pair_start)
e = t.find('\\end{figure}', pair_start) + len('\\end{figure}')
FIG = '/home/touhid/Documents/leadpaper/outputs/figs/'
stacked = ('\\begin{figure}[tbp]\n\\centering\n'
 ' accessed via stacked pair '.replace(' accessed via stacked pair ', '') +
 '\\includegraphics[width=0.85\\textwidth]{' + FIG + 'fig_EB.png}\n'
 '\\caption{Illuminated band diagram of the champion at short circuit (x=0 at the back contact).}\n'
 '\\label{fig:eb}\n\\end{figure}\n\n'
 '\\begin{figure}[tbp]\n\\centering\n'
 '\\includegraphics[width=0.85\\textwidth]{' + FIG + 'fig_GR.png}\n'
 '\\caption{Generation and recombination profiles at short circuit (log scale).}\n'
 '\\label{fig:gr}\n\\end{figure}')
t = t[:b] + stacked + t[e:]

# 6. champion result row -> multicolumn note
t = t.replace('Result & Voc 1.234 V & Jsc 21.19 & FF 89.78\\% & PCE 23.49\\% &  \\\\',
              '\\multicolumn{6}{l}{Result: Voc 1.234~V, Jsc 21.19~mA/cm$^2$, FF 89.78\\%, PCE 23.49\\%} \\\\')

# 7. runs table small + short receipt
t = t.replace('\\caption{Simulation batches archived under \\texttt{leadpaper/}.}',
              '\\small\\caption{Simulation batches archived under \\texttt{leadpaper/}.}')
t = t.replace('char.jsonl (126 converged runs feed the ML surrogate) \\\\', 'char.jsonl \\\\')

# 8. timeline/align widths 0.85 -> 0.8 (economy)
t = t.replace('width=0.85\\textwidth]{' + FIG + 'fig_timeline.png',
              'width=0.8\\textwidth]{' + FIG + 'fig_timeline.png')
t = t.replace('width=0.85\\textwidth]{' + FIG + 'fig_align.png',
              'width=0.8\\textwidth]{' + FIG + 'fig_align.png')

open(p, 'w').write(t)

# 9. callout-order audit: figure/table labels in source order vs first-cite order
for kind, pat in [('fig', r'\\label\{(fig:[^}]*)\}'), ('tab', r'\\label\{(tab:[^}]*)\}')]:
    placed = re.findall(pat, t)
    cites = re.findall(r'\\ref\{((?:fig|tab):[^}]*)\}', t)
    cites = [c for c in cites if c.startswith(kind + ':')]
    first = sorted(set(cites), key=cites.index)
    print(kind, 'placed:', [x.split(':')[1] for x in placed])
    print(kind, 'cite-order:', [x.split(':')[1] for x in first])
print('fixtex3 done')
