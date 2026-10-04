"""Add neutral interface recombination (Hossain Table 2: 1e10 cm-2 = 1e14 m-2 both sides).
Robust: replaces only the empty interface inner block, twice with distinct names."""
import shutil

KEEP = "/home/touhid/Documents/leadpaper/defs/csPbI3-CBTS-r7.def"
SCA = "/home/touhid/.scaps-runner/scaps_dat/def/csPbI3-CBTS-r7.def"

OLD = """interfacename : 
Intraband tunneling : 0
Relative electron mass :  1.00e+00
Relative hole mass :  1.00e+00"""

def new(name):
    return """interfacename : %s
Intraband tunneling : 0
Relative electron mass :  1.00e+00
Relative hole mass :  1.00e+00

interface recombination

type : neutral
sigma_nleft : 1.000e-19 [m^2]
sigma_nright : 1.000e-19 [m^2]
sigma_pleft : 1.000e-19 [m^2]
sigma_pright : 1.000e-19 [m^2]
Tunneling to trap: 0
Relative electron mass :  1.00
Relative hole mass :  1.00
energy distribution : single
Reference for defect energy :  3
Et :  0.60 [eV]
Ekar :  0.10 [eV]
N : 1.000e+14 [/m^2]""" % name

txt = open(KEEP).read()
assert txt.count(OLD) == 2, ("count", txt.count(OLD))
txt = txt.replace(OLD, new("CBTS / CsPbI3"), 1)
txt = txt.replace(OLD, new("CsPbI3 / TiO2"), 1)
open(KEEP, "w").write(txt)
shutil.copy(KEEP, SCA)
print("interfaces added; N=1e14/m2 both sides")
