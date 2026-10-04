"""S8: adopt chi_TiO2=3.8 champion; anchor set at new base."""
import sys, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner, parse_jv_curve
from scaps_runner.script_gen import from_param_dict
import numpy as np
BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
C = {"load": "csPbI3-CBTS-r7.def",
     "set": {"layer2.thickness": 2.2, "layer2.NA": 3e16,
             "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
             "layer2.Eg": 1.65, "layer2.chi": 3.928, "layer3.chi": 3.8},
     "workingpoint": {"temperature": 300, "illumination": 100},
     "iv": {"start": 0, "stop": 1.6, "step": 0.02}}
def S(extra, **kw):
    d = dict(C, set=dict(C["set"], **extra)); d.update(kw); return d
IN = {
 "champ38": S({}, iv={"start": 0, "stop": 1.6, "step": 0.01}),
 "d38_if1e8": S({"interface1.IFdefect1.Ntotal": 1e8, "interface2.IFdefect1.Ntotal": 1e8}),
 "d38_if1e9": S({"interface1.IFdefect1.Ntotal": 1e9, "interface2.IFdefect1.Ntotal": 1e9}),
 "d38_if1e11": S({"interface1.IFdefect1.Ntotal": 1e11, "interface2.IFdefect1.Ntotal": 1e11}),
 "d38_if1e12": S({"interface1.IFdefect1.Ntotal": 1e12, "interface2.IFdefect1.Ntotal": 1e12}),
 "d38_noIF": S({"layer2.thickness": 2.2}, load="csPbI3-CBTS-noIF.def"),
 "rs38_05": S({"external.Rs": 0.5}), "rs38_1": S({"external.Rs": 1}),
 "rs38_2": S({"external.Rs": 2}), "rsh38_4": S({"external.Rsh": 1e4}),
 "real38": S({"layer2.thickness": 0.8, "layer2.defect1.Ntotal": 1e15},
             load="csPbI3-CBTS-wfITO44.def"),
}
def op(path):
    import re
    txt = open(path, errors="ignore").read(); d = {}
    for k, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"), ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                   ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"), ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt); d[k] = float(m.group(1)) if m else None
    o = {"deduced": d, "error": None if d["eta"] else "no-eta"}
    try:
        J, V = parse_jv_curve(path)
        o["V"] = np.array(V).tolist(); o["J"] = np.array(J).tolist()
    except Exception: pass
    return o
r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
out = r.run_inputs(IN)
res = {k: {"d": v["deduced"], "e": v["error"]} for k, v in out.items()}
print(json.dumps(res, indent=1))
open(BASE/"outputs"/"s8_champ38.json","w").write(json.dumps(res, indent=1))
c38 = out["champ38"]
open(BASE/"outputs"/"champion_JV.json","w").write(json.dumps(
    {"params_set": dict(C["set"]), "deduced": c38["deduced"],
     "V": c38.get("V"), "J": c38.get("J")}, indent=1))
