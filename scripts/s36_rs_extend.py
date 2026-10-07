"""S36: Rs=3/4/5 extension on ceiling + routine bases (reviewer FF-gap request)."""
import sys, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
CEIL = {"layer2.thickness": 2.2, "layer2.NA": 3e16,
        "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
        "layer2.Eg": 1.65, "layer2.chi": 3.928,
        "layer1.chi": 3.9, "layer3.chi": 3.7}
ROUT = {"layer2.thickness": 1.0, "layer2.NA": 3e16,
        "layer2.defect1.Ntotal": 1e15, "layer3.ND": 9e17,
        "layer2.Eg": 1.65, "layer2.chi": 3.928}
WP = {"workingpoint": {"temperature": 300, "illumination": 100}}
IV = {"start": 0, "stop": 1.6, "step": 0.02}

def S(extra):
    return dict({"load": "csPbI3-CBTS-r7.def"}, set=dict(extra), **WP, iv=dict(IV))

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
    return {"d": d, "e": None if d["eta"] else "no-eta"}

IN = {}
for rs in (3, 4, 5):
    IN[f"J_rs{rs}"] = S(dict(CEIL, **{"external.Rs": rs}))
    IN[f"R_rs{rs}"] = S(dict(ROUT, **{"external.Rs": rs}))
# reference Rs=1,2 on same bases for a clean column
for rs in (1, 2):
    IN[f"J_rs{rs}"] = S(dict(CEIL, **{"external.Rs": rs}))
    IN[f"R_rs{rs}"] = S(dict(ROUT, **{"external.Rs": rs}))

r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
out = r.run_inputs(IN)
res = {k: {"d": v["d"], "e": v["e"], "set": IN[k]["set"]} for k, v in out.items()}
for k, v in res.items():
    print(k, v["d"], v["e"], flush=True)
json.dump(res, open(BASE / "outputs" / "s36_rs.json", "w"), indent=1)
print("s36 done")
