"""S17: joint-optimum T-sweep + attainable-gap Rs (Reviewer minor: new-base parasitics)."""
import sys, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
GEO = {"layer2.thickness": 2.2, "layer2.NA": 3e16,
       "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
       "layer2.Eg": 1.65, "layer2.chi": 3.928}
NEW = dict(GEO, **{"layer1.chi": 3.9, "layer3.chi": 3.7})
WP = {"workingpoint": {"temperature": 300, "illumination": 100},
      "iv": {"start": 0, "stop": 1.6, "step": 0.02}}


def S(extra, T=300):
    d = dict({"load": "csPbI3-CBTS-r7.def"}, set=dict(extra))
    d["workingpoint"] = {"temperature": T, "illumination": 100}
    d["iv"] = WP["iv"]
    return d


IN = {}
for T in [275, 300, 350, 400, 475]:
    IN[f"T{T}"] = S(dict(NEW), T=T)
IN["N_eg170_rs1"] = S(dict(NEW, **{"layer2.Eg": 1.70, "layer2.chi": 3.943,
                                  "external.Rs": 1}))


def op(path):
    import re
    try:
        txt = open(path, errors="ignore").read()
    except OSError:
        return {"d": None, "e": "missing-result-file"}
    d = {}
    for k, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"),
                   ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                   ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"),
                   ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt)
        d[k] = float(m.group(1)) if m else None
    return {"d": d, "e": None if d["eta"] else "no-eta"}


r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
out = r.run_inputs(IN)
json.dump({k: {"d": v["d"], "e": v["e"], "set": IN[k]["set"]} for k, v in out.items()},
          open(BASE / "outputs" / "s17.json", "w"), indent=1)
print(json.dumps({k: v["d"] for k, v in out.items()}, indent=1))
