"""Re-run champion B030 with full JV arrays for record. Persistent only."""
import sys, json, re, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
import numpy as np
from scaps_runner import SCAPSrunner, parse_jv_curve
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
OUT = BASE / "outputs" / "champion_JV.json"
RCP = BASE / "receipts" / "receipt_champion.json"

CHAMP = {"load": "csPbI3-CBTS-r7.def",
         "set": {"layer2.thickness": 2.2, "layer2.NA": 3e16,
                 "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
                 "layer2.Eg": 1.65, "layer2.chi": 3.928},
         "workingpoint": {"temperature": 300, "illumination": 100},
         "iv": {"start": 0, "stop": 1.6, "step": 0.01}}

def parse_deduced(path):
    txt = open(path, errors="ignore").read()
    d = {}
    for k, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"),
                   ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                   ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"),
                   ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt)
        d[k] = float(m.group(1)) if m else None
    return d

def op(path):
    J, V = parse_jv_curve(path)
    return {"deduced": parse_deduced(path),
            "V": np.array(V).tolist(), "J": np.array(J).tolist()}

r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
out = r.run_inputs({"champion_B030": CHAMP})
v = out["champion_B030"]
OUT.write_text(json.dumps({"params_set": CHAMP["set"], "deduced": v["deduced"],
                           "V": v["V"], "J": v["J"]}, indent=1))
RCP.write_text(json.dumps({
    "device": "ITO/TiO2/CsPbI3/CBTS/Ni",
    "absorber": {"d_um": 2.2, "Eg": 1.65, "chi": 3.928, "NA_cm3": 3e16, "Nt_cm3": 1e12,
                 "eps": 6.0, "mun_mup_cm2Vs": 25, "Nc_cm3": 1.1e19, "Nv_cm3": 8.2e19},
    "etl": {"mat": "TiO2", "d_nm": 30, "ND_cm3": 9e17, "Nt_cm3": 1e15},
    "htl": {"mat": "CBTS", "d_nm": 100, "NA_cm3": 1e18, "Nt_cm3": 1e15},
    "interfaces_cm2": 1e10, "back_eV": 5.5, "front_eV": 4.0, "T_K": 300, "sun": 1,
    "deduced": v["deduced"],
    "cbo_etl_abs_eV": 0.072, "vbo_abs_htl_eV": -0.22,
    "caveats": ["Rs=0 upper bound; x0.965 (~22.68%) at Rs~1",
                "Eg1.65 = strained lower bound for CsPbI3; FF89.9 near-ideal-diode (Rs=0)",
                "40% SJ 1-sun impossible (SQ~30%); tandem needed"]}, indent=1))
print(json.dumps(v["deduced"], indent=1))
