"""S23 stage 2: Cr + mobility pricing on the routine-defect base.

Routine base = s6 nt15_d10 (20.8197%): 1.0 um, NA 3e16, Nt 1e15, ND 9e17,
Eg 1.65/chi 3.928, surveyed affinities (r7 def), both IF at 1e10.
Stage 1 proved: set-radiative units are cm^3/s; mu set units are cm^2/Vs.
- R_rad0 must reproduce 20.8197 (routine key-path check).
- R_rad1em10 / R_rad1em9 price k_rad=0 at routine defects.
- R_mu105 prices the 25/25 mobility assumption at routine defects.
Merges into outputs/s23_krad_mu.json.
"""
import sys, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict
sys.path.insert(0, "/home/touhid/Documents/leadpaper-polish-r8/scripts")
from s16_peak import S, op

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
ROUTINE = {"layer2.thickness": 1.0, "layer2.NA": 3e16,
           "layer2.defect1.Ntotal": 1e15, "layer3.ND": 9e17,
           "layer2.Eg": 1.65, "layer2.chi": 3.928}

IN = {
    "R_rad0": S(dict(ROUTINE, **{"layer2.radiative": 0})),
    "R_rad1em10": S(dict(ROUTINE, **{"layer2.radiative": 1e-10})),
    "R_rad1em9": S(dict(ROUTINE, **{"layer2.radiative": 1e-9})),
    "R_mu105": S(dict(ROUTINE, **{"layer2.mun": 10, "layer2.mup": 5})),
}

r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
out = r.run_inputs(IN)
p = BASE / "outputs" / "s23_krad_mu.json"
res = json.load(open(p)) if p.exists() else {}
for k, v in out.items():
    res[k] = {"d": v["d"], "e": v["e"], "set": IN[k]["set"]}
    print(k, v["d"], v["e"], flush=True)
json.dump(res, open(p, "w"), indent=1)
