"""S12: fine-IV-step confirmatory run at surveyed base (archives the Table 8 300K row)."""
import sys, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict
BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
P = {"load": "csPbI3-CBTS-r7.def",
     "set": {"layer2.thickness": 2.2, "layer2.NA": 3e16, "layer2.defect1.Ntotal": 1e12,
             "layer3.ND": 9e17, "layer2.Eg": 1.65, "layer2.chi": 3.928},
     "workingpoint": {"temperature": 300, "illumination": 100},
     "iv": {"start": 0, "stop": 1.6, "step": 0.01}}

def op(path):
    import re
    txt = open(path, errors="ignore").read()
    d = {}
    for k, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"),
                   ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                   ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"),
                   ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt)
        d[k] = float(m.group(1)) if m else None
    return {"deduced": d, "error": None if d["eta"] else "no-eta"}

r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
v = r.run_inputs({"fine_surveyed": P})["fine_surveyed"]
print(json.dumps(v["deduced"]))
open(BASE / "outputs" / "s12_fine.json", "w").write(
    json.dumps({"fine_surveyed": {"d": v["deduced"], "e": v["error"]}}))
