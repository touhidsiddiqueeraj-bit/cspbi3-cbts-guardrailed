"""S23 stage 1: radiative-coefficient + mobility key-path checks on the joint base.

Appendix-A discipline: every new `set` key is validated by a same-value
run that must reproduce the s22 joint receipt (24.9464%) digit-for-digit.
- layer2.radiative 0  -> must reproduce baseline (key-path check; Cr default 0).
- layer2.mun/mup 25/25 -> must reproduce baseline (practical-unit check).
Cr grid {1e-16, 1e-10, 1e-9} disambiguates set units by effect:
  cm^3/s units -> 1e-16 no-op, 1e-10/1e-9 bite (review Fig.15 scale);
  SI m^3/s units -> 1e-10/1e-9 diverge, 1e-16 bites moderately.
Mobility literature points (DFT 5-10 e- / 1-5 h): 10/5 and 5/2.
Writes outputs/s23_krad_mu.json (merged if exists).
"""
import sys, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict
sys.path.insert(0, "/home/touhid/Documents/leadpaper-polish-r8/scripts")
from s16_peak import S, NEW, op

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")

IN = {
    "J_rad0": S(dict(NEW, **{"layer2.radiative": 0})),
    "J_rad1em16": S(dict(NEW, **{"layer2.radiative": 1e-16})),
    "J_rad1em10": S(dict(NEW, **{"layer2.radiative": 1e-10})),
    "J_rad1em9": S(dict(NEW, **{"layer2.radiative": 1e-9})),
    "J_mu2525": S(dict(NEW, **{"layer2.mun": 25, "layer2.mup": 25})),
    "J_mu105": S(dict(NEW, **{"layer2.mun": 10, "layer2.mup": 5})),
    "J_mu52": S(dict(NEW, **{"layer2.mun": 5, "layer2.mup": 2})),
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
