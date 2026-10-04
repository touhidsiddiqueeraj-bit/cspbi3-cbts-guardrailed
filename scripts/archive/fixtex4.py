import re
p = '/home/touhid/Documents/texflowmcp/workspace/document.tex'
t = open(p).read()

# Rs paragraph numbers
old = 'the champion projects to 23.08\\%, 22.68\\% and 21.93\\% respectively'
assert old in t, 'rs para'
t = t.replace(old, 'the champion projects to 23.27\\%, 23.05\\% and 22.62\\% respectively')

# Rs table 2.0 row (whatever dash variant)
t = re.sub(r'2\.0 & 21\.93 & \$[^$]*\$ & below record \\\\\\\\',
           '2.0 & 22.62 & +0.60 & still above record \\\\\\\\', t)

# second 22.68 occurrence (discussion): reword to derived value
t = t.replace('22.68\\%)', '23.05\\% at $R_s=1~\\Omega$cm$^2$)')

# move Round-B table block after Round-A table block
def block(label):
    s = t.find('\\label{' + label + '}')
    b = t.rfind('\\begin{table}', 0, s)
    e = t.find('\\end{table}', s) + len('\\end{table}')
    return b, e
bb, be = block('tab:top10b')
blk = t[bb:be]
t = t[:bb] + t[be:]
ab, ae = block('tab:top10')
t = t[:ae] + '\n\n' + blk + t[ae:]

# missing table callouts in reading order
reps = [
 ('Full input parameters are listed in Tables~\\ref{tab:in} and~\\ref{tab:if};',
  'Full input parameters are listed in Tables~\\ref{tab:in} and~\\ref{tab:if};'),
]
# champion table callout (end of Round-A paragraph)
old = 'reached 23.47\\%, already above the 22.60\\% laboratory record.'
assert old in t
t = t.replace(old, old + ' Full parameters are collected in Table~\\ref{tab:champ}.')
# audit table callout
old = 'numbers are reproducible artefacts of an omitted loss channel.'
assert old in t
t = t.replace(old, old + ' Table~\\ref{tab:audit} summarises the paired comparison.')
# ml table callout
old = 'with ETL doping (0.057) and thickness (0.014) trailing'
if old in t:
    t = t.replace(old, old + ' (Table~\\ref{tab:ml})')
else:
    # fallback anchor
    a2 = 'its first quantification for CsPbI3-CBTS.'
    assert a2 in t
    t = t.replace(a2, a2 + ' Importances are tabulated in Table~\\ref{tab:ml}.')
# fab table callout
old = 'missing any one lands on the corresponding contour of Fig.~\\ref{fig:contour}.'
assert old in t
t = t.replace(old, old + ' The translation is summarised in Table~\\ref{tab:fab}.')
# runs table callout (data availability)
old = 'are archived with the project under \\texttt{leadpaper/}'
assert old in t
t = t.replace(old, 'are archived with the project under \\texttt{leadpaper/} (inventory in Table~\\ref{tab:runs})')

open(p, 'w').write(t)

for kind in ['fig', 'tab']:
    placed = re.findall(r'\\label\{(' + kind + r':[^}]*)\}', t)
    cites = [c for c in re.findall(r'\\ref\{((?:fig|tab):[^}]*)\}', t) if c.startswith(kind + ':')]
    first = sorted(set(cites), key=cites.index)
    print(kind, 'placed:', [x.split(':')[1] for x in placed])
    print(kind, 'cite1 :', [x.split(':')[1] for x in first])
print('fixtex4 done')
