import json
p = '/home/touhid/Documents/texflowmcp/workspace/document.tex'
t = open(p).read()

# 1. braces
t = t.replace('\\textbf\\{23.49\\%\\}', '\\textbf{23.49\\%}')

# 2. Rs table 2.0 row (note $-$ minus)
old = '2.0 & 21.93 & $-$0.09 & below record \\\\'
assert old in t, 'rs row'
t = t.replace(old, '2.0 & 22.62 & +0.60 & still above record \\\\')

# 3. Sec-3 derate sentences
a = 'plus a disclosed analytic derate ($\\times0.965$ at Rs$\\sim$1~$\\Omega$cm$^2$)'
assert a in t
t = t.replace(a, 'plus a disclosed analytic derate ($\\times0.981$ at $R_s=1~\\Omega$cm$^2$)')
b = 'equal to 0.965 at $R_s=1~\\Omega$cm$^2$'
assert b in t
t = t.replace(b, 'equal to 0.981 at $R_s=1~\\Omega$cm$^2$')

# 4. appendix titles sequential
t = t.replace('\\section{Appendix: the scripting unit trap}',
              '\\section{Appendix A: the scripting unit trap}')
t = t.replace('\\section*{Appendix B: run inventory}',
              '\\section{Appendix B: run inventory}\nAll simulation batches are inventoried in Table~\\ref{tab:runs}.')

# 5. body figure widths 0.88 -> 0.8 (space); keep side-by-side pair
t = t.replace('width=0.88\\textwidth', 'width=0.8\\textwidth')

open(p, 'w').write(t)

# 6. receipt + FINAL_DEVICE consistency
rp = '/home/touhid/Documents/leadpaper/receipts/receipt_champion.json'
r = json.load(open(rp))
r['caveats'] = ['Rs=0 upper bound; x0.981 (~23.05%) at Rs=1 ohm-cm2',
                'Eg1.65 = strained lower bound for CsPbI3; FF89.78 near-ideal-diode (Rs=0)',
                '40% SJ 1-sun impossible (SQ~30%); tandem needed']
json.dump(r, open(rp, 'w'), indent=1)

fd = '/home/touhid/Documents/leadpaper/FINAL_DEVICE.md'
f = open(fd).read()
f = f.replace('Rs-derated estimate (×0.965, Rs~1 Ω·cm²): ~22.68% — still beats cert.',
              'Rs-derated estimate (×0.981, Rs=1 Ω·cm²): ~23.05% — still beats cert.')
open(fd, 'w').write(f)
print('fixfinal done')
