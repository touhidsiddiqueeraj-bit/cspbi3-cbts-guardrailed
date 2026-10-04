import re
p = '/home/touhid/Documents/texflowmcp/workspace/document.tex'
t = open(p).read()
b = '/home/touhid/Documents/texflowmcp/workspace/references.bib'
bb = open(b).read()

# 1. audit pointer Section 5 -> 7
old = 'Our audit in Section~5 places these numbers'
assert old in t
t = t.replace(old, 'Our audit in Section~7 places these numbers')

# 2. demote PMC2025 (keep claim via other two cites)
old = '27--28\\% low-cost and ML-guided designs~\\cite{PMC2025,PerovskiteOpt2026,Multilayer2026}'
assert old in t
t = t.replace(old, '27--28\\% low-cost and ML-guided designs~\\cite{PerovskiteOpt2026,Multilayer2026}')

# 3. champ table headers to math
old = 'Layer & d & Eg (eV) & chi (eV) & Doping (cm$^{-3}$) & Nt (cm$^{-3}$) \\\\'
assert old in t
t = t.replace(old, 'Layer & $d$ & $E_g$ (eV) & $\\chi$ (eV) & Doping (cm$^{-3}$) & $N_t$ (cm$^{-3}$) \\\\')

# 4. bibliography: real authors
def swap(key, entry):
    global bb
    pat = re.compile(r'@\w+\{' + key + r',.*?\n\}\n', re.S)
    assert pat.search(bb), key
    bb = pat.sub(entry, bb)

swap('PerovskiteOpt2026', '''@article{PerovskiteOpt2026,
 author = {Alshaikh, Mohammed Saleh},
 title = {PerovskiteOpt-AI: A Machine Learning-Driven Multi-Parameter Optimization Framework for Lead-Free Perovskite Solar Cell Device Architecture Using SCAPS-1D Simulation and Gaussian Process Surrogate Modeling},
 journal = {Crystals},
 volume = {16},
 pages = {310},
 year = {2026},
 doi = {10.3390/cryst16050310},
 note = {FTO/WS2/CsSnI3/CuSCN/Au, GP-BO to 27.83\\%},
}
''')
swap('Multilayer2026', '''@article{Multilayer2026,
 author = {Nasiri, Neda and Mastoor, Seyed Mahdi and Kordbacheh, Amirhosein Ahmadkhan},
 title = {Multilayer Screening of Double and Conventional Perovskite Solar Cells Using SCAPS-1D and Machine Learning: Optimization of ETL, HTL, and Absorber for High-Efficiency Architectures},
 journal = {arXiv:2606.12083},
 year = {2026},
 note = {125 architectures; Cs2AgInBr6 28.62\\% ML-suggested},
}
''')
swap('Zenodo2025', '''@article{Zenodo2025,
 author = {Novoselov, Ivan E. and Gvozdev, Alexander M. and Smirnov, Andrey A. and Zhidkov, Ivan S.},
 title = {Dataset of SCAPS-1D simulated halide perovskite solar cells with SHAP and machine learning-based PCE optimization},
 journal = {Data in Brief},
 volume = {60},
 pages = {111653},
 year = {2025},
 doi = {10.1016/j.dib.2025.111653},
 note = {7182 configurations; Zenodo 10.5281/zenodo.15211402},
}
''')
swap('CsSnI32024', '''@article{CsSnI32024,
 author = {Moone, Parisa Karimi and Sharifi, Nafiseh},
 title = {Comparison of Pb-based and Sn-based perovskite solar cells using SCAPS simulation: optimal efficiency of eco-friendly CsSnI3 devices},
 journal = {Environmental Science and Pollution Research},
 volume = {31},
 pages = {51447--51460},
 year = {2024},
 doi = {10.1007/s11356-024-34622-x},
 note = {CsSnI3 17.36\\% optimized},
}
''')
# demote unidentifiable PMC2025 entry
pat = re.compile(r'@misc\{PMC2025,.*?\n\}\n', re.S)
assert pat.search(bb)
bb = pat.sub('', bb)

open(p, 'w').write(t)
open(b, 'w').write(bb)
import re as _re
keys = _re.findall(r'@\w+\{(\w+),', bb)
print('bib entries:', len(keys))
