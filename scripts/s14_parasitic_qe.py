"""S14: routine parasitics + adopted-base QE (Reviewer minors + QE integral).

1. rs1rsh4_adopted: Rs=1 + Rsh=1e4 at adopted champion base (was 'not run').
2. rs1_routine: Rs=1 at routine base (Nt=1e15, 1.0um, surveyed chi).
3. qe_adopted: QE curve at adopted champion base for Jsc-integral check.
Writes outputs/s14.json (+ qe txt parsed inline).
"""
import sys, json, os, re, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
CHAMP = {"layer2.thickness": 2.2, "layer2.NA": 3e16,
         "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
         "layer2.Eg": 1.65, "layer2.chi": 3.928, "layer3.chi": 3.8}
ROUTINE = {"layer2.thickness": 1.0, "layer2.NA": 3e16,
           "layer2.defect1.Ntotal": 1e15, "layer3.ND": 9e17,
           "layer2.Eg": 1.65, "layer2.chi": 3.928}
WP = {"workingpoint": {"temperature": 300, "illumination": 100},
      "iv": {"start": 0, "stop": 1.6, "step": 0.02}}


def op(path):
    txt = open(path, errors="ignore").read()
    d = {}
    for k, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"),
                   ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                   ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"),
                   ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt)
        d[k] = float(m.group(1)) if m else None
    return {"d": d, "e": None if d["eta"] else "no-eta"}


def S(extra, load="csPbI3-CBTS-r7.def"):
    return dict({"load": load}, set=dict(extra), **WP)


IN = {
    "rs1rsh4_adopted": S(dict(CHAMP, **{"external.Rs": 1, "external.Rsh": 1e4})),
    "rs1_routine": S(dict(ROUTINE, **{"external.Rs": 1})),
}

r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
out = r.run_inputs(IN)
res = {k: {"d": v["d"], "e": v["e"]} for k, v in out.items()}

# QE at adopted base (custom builder for qe action)
def build_qe(p):
    c = ["clear actions", "load definitionfile csPbI3-CBTS-r7.def"]
    for k, v in CHAMP.items():
        c.append(f"set {k} {v}")
    c += ["action workingpoint.temperature 300", "action intensity.T 100",
          "action light",
          "action qe.startlambda 300", "action qe.stoplambda 850",
          "action qe.points 56", "action qe.doqe",
          "action iv.startv 0", "action iv.stopv 1.6", "action iv.increment 0.05",
          "action iv.doiv", "calculate singleshot",
          "save results.qe adopted_qe.txt"]
    return "set quitscript.quitSCAPS\nset errorhandling.overwritefile\n" + "\n".join(c) + "\n"


def op_qe(result_file):
    import shutil
    rdir = os.path.dirname(result_file)
    p = os.path.join(rdir, "adopted_qe.txt")
    pts = []
    if os.path.exists(p):
        shutil.copy(p, BASE / "outputs" / "adopted_qe_raw.txt")
        for ln in open(p, errors="ignore"):
            if ln.startswith(("#", "w", "W", "l", "L", "Q")):
                continue
            nums = re.findall(r"[-+]?\d*\.\d+(?:[eE][-+]?\d+)?|[-+]?\d+", ln)
            if len(nums) >= 2:
                try:
                    wl, qe = float(nums[0]), float(nums[1])
                    if 250 < wl < 900 and 0 <= qe <= 1.5:
                        pts.append((wl, qe))
                except ValueError:
                    pass
    return {"qe_pts": pts}


r2 = SCAPSrunner(build_qe, op_qe, ncores=1)
r2.sync_parameters()
qe = r2.run_inputs({"qe_adopted": None})["qe_adopted"]
res["qe_adopted"] = qe
json.dump(res, open(BASE / "outputs" / "s14.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "qe_adopted"}, indent=1))
print("qe points:", len(qe.get("qe_pts", [])))
