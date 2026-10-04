"""Build CsPbI3-CBTS def from perovskite-mapi.def (Hossain NJC 2023 Table 1).
Persistent script (no /tmp). Run: python3 thisfile. Outputs to leadpaper/defs + scaps_dat/def.
Units: SCAPS uses m, /m^3, m^2/Vs. Paper uses cm: x1e6 for /cm3->/m3, x1e-4 for cm2/Vs->m2/Vs, nm->m.
"""
import re, shutil, pathlib

SRC = "/home/touhid/.scaps-runner/scaps_dat/def/perovskite-mapi.def"
DST_NAME = "csPbI3-CBTS-r7.def"
DST_SCA = f"/home/touhid/.scaps-runner/scaps_dat/def/{DST_NAME}"
DST_KEEP = f"/home/touhid/Documents/leadpaper/defs/{DST_NAME}"

# target uniform values per layer (layer1=HTL CBTS, layer2=CsPbI3, layer3=ETL TiO2)
T = {
    1: dict(d=1.0e-7, eps=5.4, chi=3.6, Eg=1.9, Nc=2.2e24, Nv=1.8e25,
             mun=3.0e-3, mup=1.0e-3, Na=1.0e24, Nd=0.0, Nt=1.0e21),
    2: dict(d=8.0e-7, eps=6.0, chi=3.95, Eg=1.694, Nc=1.1e25, Nv=8.2e25,
             mun=2.5e-3, mup=2.5e-3, Na=1.0e21, Nd=0.0, Nt=1.0e21),
    3: dict(d=3.0e-8, eps=9.0, chi=4.0, Eg=3.2, Nc=2.0e24, Nv=1.8e25,
             mun=2.0e-3, mup=1.0e-3, Na=0.0, Nd=9.0e22, Nt=1.0e21),
}
# NOTE Nc/Nv absorber: paper prints 1.1e20/8.2e20 cm-3 are unphysical (>solid density);
# capped to 1.1e19/8.2e19 cm-3 per skill realism table (CsPbI3 1e19). Flagged in receipt.

lines = open(SRC).read().splitlines()
# split into 3 layer blocks by lines starting with "layer"
idx = [i for i, l in enumerate(lines) if l.strip() == "layer"]
assert len(idx) == 3, len(idx)
blocks = []
for k in range(3):
    s = idx[k]
    e = idx[k+1] if k < 2 else next(i for i, l in enumerate(lines) if l.strip() == "front contact")
    blocks.append((s, e))

KEYMAP = {"eps": "eps", "chi": "chi", "Eg": "Eg", "Nc": "Nc", "Nv": "Nv",
          "mu_n": "mun", "mu_p": "mup", "Na(uniform)": "Na", "Nd(uniform)": "Nd",
          "Nt(uniform)": "Nt"}

def patch_block(blines, vals):
    out = []
    for ln in blines:
        m = re.match(r"\s*(eps|chi|Eg|Nc|Nv|mu_n|mu_p|Na\(uniform\)|Nd\(uniform\)|Nt\(uniform\))\s*:(.*)", ln)
        if m:
            key, rest = m.group(1), m.group(2)
            tgt = vals[KEYMAP[key]]
            # preserve trailing flags: last 2 tokens are like "0 2" plus optional "[unit]"
            toks = rest.strip().split()
            unit = ""
            if toks and toks[-1].startswith("["):
                unit = " " + toks.pop()
            flags = toks[-2:]  # e.g. ['0','2']
            nums = toks[:-2]
            newnums = [f"{tgt:.6e}" for _ in nums]
            ln = f"{key} :\t " + "\t ".join(newnums) + "\t " + " ".join(flags) + unit
        else:
            m2 = re.match(r"\s*(name)\s*:(.*)", ln)
            if m2:
                nm = {1: "CBTS-HTL", 2: "CsPbI3", 3: "TiO2-ETL"}[vals["_id"]]
                ln = f"name : {nm}"
            m3 = re.match(r"\s*d\s*:(.*)", ln)
            if m3 and "Relative" not in ln and "period" not in ln:
                rest = m3.group(1).strip().split()
                unit = ""
                if rest and rest[-1].startswith("["):
                    unit = " " + rest.pop()
                ln = f"d : {vals['d']:.3e} {unit}".rstrip()
        out.append(ln)
    return out

new = lines[:]
for li, (s, e) in enumerate(blocks):
    lid = li + 1
    vals = dict(T[lid]); vals["_id"] = lid
    new[s:e] = patch_block(lines[s:e], vals)

txt = "\n".join(new)
# contacts: back Au5.1 -> Ni5.5, front 4.4 -> ITO 4.0
txt = txt.replace("Fi_m :   5.1000 [eV]", "Fi_m :   5.5000 [eV]")
txt = txt.replace("Fi_m :  4.40 [eV]", "Fi_m :  4.00 [eV]")
txt = txt.replace("Perovskite solar cell: FTO / TiO2 / MAPbI3 / Spiro-OMeTAD / Au",
                  "CsPbI3 solar cell: ITO / TiO2 / CsPbI3 / CBTS / Ni (Hossain NJC2023 baseline, r7)")
open(DST_KEEP, "w").write(txt + "\n")
shutil.copy(DST_KEEP, DST_SCA)
print("wrote", DST_KEEP, "and", DST_SCA)
