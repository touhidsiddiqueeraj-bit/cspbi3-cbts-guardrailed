"""s18_analytic.py: archives the three analytic computations the paper leans on.

1. detailed-balance radiative Voc from the model's own Eg-sqrt absorption
2. QE-integrated Jsc against AM1.5G (parses SCAPS QE dump + the .spe file)
3. SQ-limit Jsc row for the loss-budget table
Writes outputs/s18_analytic.json.
"""
import json, re, pathlib
import numpy as np

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
Q = 1.602176634e-19
H, C, KB = 6.62607015e-34, 2.99792458e8, 1.380649e-23
T = 300.0
A0, D = 1e7, 2.2e-6          # SCAPS absorption A [m^-1 eV^-1/2], absorber 2.2 um
OUT = {}


def radiative_voc(Eg, jsc_mA, T=300.0):
    """DB Voc: Voc = kT/q ln(Jsc/J0+1); J0 = q int B(E) A(E) dE over E>=Eg."""
    E = np.linspace(Eg, 4.0, 60001)
    EJ = E * Q
    alpha = A0 * np.sqrt(E - Eg)              # m^-1
    absorp = 1 - np.exp(-alpha * D)          # single pass, opaque Ni back contact
    phi = 2 * np.pi * EJ ** 2 / (H ** 3 * C ** 2 *
                                 (np.exp(EJ / (KB * T)) - 1))   # photons/m2/s/J
    J0 = Q * np.trapezoid(phi * absorp, EJ)
    J = jsc_mA * 10                              # mA/cm2 -> A/m2
    return float((KB * T / Q) * np.log(J / J0 + 1)), float(J0)


for Eg, J in [(1.65, 21.1974), (1.70, 20.1787)]:
    v, j0 = radiative_voc(Eg, J)
    OUT[f"db_voc_Eg{Eg}"] = {"J0_A_per_m2": j0, "Voc_V": round(v, 4),
                             "T_K": 300, "absorptance": "single pass, opaque Ni"}
for Eg, J in [(1.65, 21.357113)]:
    v, j0 = radiative_voc(Eg, J, T=275.0)
    OUT[f"db_voc_Eg{Eg}_T275"] = {"J0_A_per_m2": j0, "Voc_V": round(v, 4),
                                  "T_K": 275, "absorptance": "single pass, opaque Ni"}

# ---- QE integral ----
spe = []
p = pathlib.Path("/home/touhid/.wine/drive_c/Program Files (x86)/Scaps3309/"
                 "spectrum/AM1_5G 1 sun.spe")
for ln in open(p, errors="ignore"):
    s = ln.split()
    if len(s) >= 2:
        try:
            a, b = float(s[0]), float(s[1])
        except ValueError:
            continue
        if 200 < a < 2000 and b > 0:
            spe.append((a, b))
spe = np.array(spe)
qe = []
for ln in open(BASE / "outputs" / "adopted_qe_raw.txt"):
    s = ln.split()
    if len(s) >= 2:
        try:
            wl, v = float(s[0]), float(s[1])
        except ValueError:
            continue
        if 250 < wl < 900 and 0 <= v <= 100:
            qe.append((wl, v / 100))
qe = np.array(qe)
scale = 1000 / 962.5813
lam = spe[:, 0] * 1e-9
flux = spe[:, 1] * scale * lam / (H * C)
qei = np.interp(spe[:, 0], qe[:, 0], qe[:, 1], left=0, right=0)
jsc_int = float(np.sum(qei * flux) * Q * 0.1)      # A/m2 -> mA/cm2
OUT["qe_integral"] = {
    "Jsc_integrated_mA_cm2": round(jsc_int, 2),
    "Jsc_IV_mA_cm2": 21.1974,
    "gap_mA_cm2": round(jsc_int - 21.1974, 2),
    "plateau_350_700": round(float(np.mean(qe[(qe[:, 0] >= 350) & (qe[:, 0] <= 700), 1])), 3),
    "n_points": int(len(qe)),
    "spectrum": str(p)}

# ---- SQ-limit Jsc for the loss-budget row ----
J = 0.0
for wl, Pw in spe:
    if wl <= 1239.84 / 1.65:
        continue
    J += Pw * scale * (wl * 1e-9) / (H * C)
OUT["sq_jsc_Eg165_mA_cm2"] = round(float(J * Q * 0.1), 1)
# Green's ideal single-diode FF: (v - V_T ln(v/V_T + 1)) / (v + V_T)
for v, t in [(1.357113, 275), (1.320708, 300), (1.363445, 300)]:
    VT = 0.025692 * (t / 300.0)
    FF = (v - VT * np.log(v / VT + 1)) / (v + VT) * 100
    OUT[f"green_ff_V{v}_T{t}"] = round(float(FF), 2)

json.dump(OUT, open(BASE / "outputs" / "s18_analytic.json", "w"), indent=1)
print(json.dumps(OUT, indent=1))