"""S7: Nt1e13@champbase (sigma question), Nif dose @Nt1e15, chi_TiO2 sweep."""
import sys, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
CH = {"load": "csPbI3-CBTS-r7.def",
      "set": {"layer2.thickness": 2.2, "layer2.NA": 3e16,
              "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
              "layer2.Eg": 1.65, "layer2.chi": 3.928},
      "workingpoint": {"temperature": 300, "illumination": 100},
      "iv": {"start": 0, "stop": 1.6, "step": 0.02}}

def S(extra):
    return dict(CH, set=dict(CH["set"], **extra))

IN = {
 "nt13_base": S({"layer2.defect1.Ntotal": 1e13}),
 "nt15_if1e9": S({"layer2.thickness": 1.0, "layer2.defect1.Ntotal": 1e15,
                  "interface1.IFdefect1.Ntotal": 1e9, "interface2.IFdefect1.Ntotal": 1e9}),
 "nt15_if1e10": S({"layer2.thickness": 1.0, "layer2.defect1.Ntotal": 1e15}),
 "nt15_if1e11": S({"layer2.thickness": 1.0, "layer2.defect1.Ntotal": 1e15,
                   "interface1.IFdefect1.Ntotal": 1e11, "interface2.IFdefect1.Ntotal": 1e11}),
 "chiTi38": S({"layer3.chi": 3.8}),
 "chiTi39": S({"layer3.chi": 3.9}),
 "chiTi41": S({"layer3.chi": 4.1}),
 "chiTi42": S({"layer3.chi": 4.2}),
}

def op(path):
    import re
    txt = open(path, errors="ignore").read(); d = {}
    for k, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"), ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                   ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"), ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt); d[k] = float(m.group(1)) if m else None
    return {"deduced": d, "error": None if d["eta"] else "no-eta"}

r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
out = r.run_inputs(IN)
res = {k: {"d": v["deduced"], "e": v["error"]} for k, v in out.items()}
print(json.dumps(res, indent=1))
open(BASE / "outputs" / "s7_r3.json", "w").write(json.dumps(res, indent=1))
