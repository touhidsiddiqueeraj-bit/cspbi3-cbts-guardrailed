"""S14b: QE-only rerun at adopted champion base (raw capture for integral check)."""
import sys, os, re, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
sys.path.insert(0, "/home/touhid/Documents/leadpaper/scripts")
from s14_parasitic_qe import build_qe, op_qe, BASE

r2 = SCAPSrunner(build_qe, op_qe, ncores=1)
r2.sync_parameters()
qe = r2.run_inputs({"qe_adopted": None})["qe_adopted"]
s14 = json.load(open(BASE / "outputs" / "s14.json"))
s14["qe_adopted"] = qe
json.dump(s14, open(BASE / "outputs" / "s14.json", "w"), indent=1)
print("qe points:", len(qe.get("qe_pts", [])))
print("head:", qe.get("qe_pts", [])[:4])
print("tail:", qe.get("qe_pts", [])[-3:])
