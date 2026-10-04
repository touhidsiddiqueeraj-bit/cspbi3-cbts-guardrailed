import re
p = '/home/touhid/Documents/texflowmcp/workspace/document.tex'
t = open(p).read()

def cut(label):
    s = t.find('\\label{' + label + '}')
    b = t.rfind('\\begin{table}', 0, s)
    e = t.find('\\end{table}', s) + len('\\end{table}')
    blk = t[b:e]
    return t[:b] + t[e:], blk

# A. move tab:in + tab:if to end of framework section (before champion section)
t, bin_ = cut('tab:in')
t, bif_ = cut('tab:if')
anchor = '\\section{Simultaneous optimisation and champion device}'
i = t.find(anchor)
t = t[:i] + bin_ + '\n\n' + bif_ + '\n\n' + t[i:]

# B. move tab:champ before Round-A paragraph
t, bch = cut('tab:champ')
anchor = "Round~A's top ten"
i = t.find(anchor)
# back up to paragraph start (previous blank line)
ps = t.rfind('\n\n', 0, i) + 2
t = t[:ps] + bch + '\n\n' + t[ps:]

# C. move tab:ml before mlcmp paragraph
t, bml = cut('tab:ml')
anchor = 'The ranking agrees with Bayesian optimisation on CsSnI3'
i = t.find(anchor)
ps = t.rfind('\n\n', 0, i) + 2
t = t[:ps] + bml + '\n\n' + t[ps:]

# D. explicit Rs table callout in Rs subsection
old = 'the champion projects to 23.27\\%, 23.05\\% and 22.62\\% respectively'
assert old in t
t = t.replace(old, old + ' (Table~\\ref{tab:rs})')

open(p, 'w').write(t)
for kind in ['fig', 'tab']:
    placed = re.findall(r'\\label\{(' + kind + r':[^}]*)\}', t)
    cites = [c for c in re.findall(r'\\ref\{((?:fig|tab):[^}]*)\}', t) if c.startswith(kind + ':')]
    first = sorted(set(cites), key=cites.index)
    P = [x.split(':')[1] for x in placed]
    F = [x.split(':')[1] for x in first]
    print(kind, 'match:', P == F)
    if P != F:
        print(' placed:', P, '\n cite1 :', F)
print('fixtex5 done')
