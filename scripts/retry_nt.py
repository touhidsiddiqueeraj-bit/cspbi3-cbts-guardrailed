"""Retry Nt combos with interfaces present. 4 combos SIMULTANEOUSLY. Persistent only."""
import sys, json, re, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
import numpy as np
from scaps_runner import SCAPSrunner, parse_jv_curve
from scaps_runner.script_gen import from_param_dict

OUT = pathlib.Path("/home/touhid/Documents/leadpaper/outputs/retry_nt.json")

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
    try:
        J, V = parse_jv_curve(path)
        return {"deduced": parse_deduced(path), "npts": len(V)}
    except Exception as e:
        return {"error": str(e)}

r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
LOAD = "csPbI3-CBTS-r7.def"
def base(**kw):
    d = {"load": LOAD, "workingpoint": {"temperature": 300, "illumination": 100},
         "iv": {"start": 0, "stop": 1.6, "step": 0.02}}
    if kw:
        d["set"] = kw
    return d

inputs = {
    "nt12_only": base(**{"layer2.defect1.Ntotal": 1e12}),
    "nt13_only": base(**{"layer2.defect1.Ntotal": 1e13}),
    "nt12_na16": base(**{"layer2.NA": 1e16, "layer2.defect1.Ntotal": 1e12}),
    "nt12_th15": base(**{"layer2.thickness": 1.5, "layer2.defect1.Ntotal": 1e12}),
}
out = r.run_inputs(inputs)
lite = {k: v.get("deduced", v) for k, v in out.items()}
OUT.write_text(json.dumps({"summary": lite}, indent=1))
print(json.dumps(lite, indent=1))
