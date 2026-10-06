"""S22: joint-optimum interface dose check (explicit N_if sets)."""
import sys, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict
sys.path.insert(0, "/home/touhid/Documents/leadpaper/scripts")
from s16_peak import S, NEW, op

IN = {
    "J_if1e10_explicit": S(dict(NEW, **{"interface1.IFdefect1.Ntotal": 1e10,
                                         "interface2.IFdefect1.Ntotal": 1e10})),
    "J_if1e11": S(dict(NEW, **{"interface1.IFdefect1.Ntotal": 1e11,
                               "interface2.IFdefect1.Ntotal": 1e11})),
}
r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=2)
r.sync_parameters()
out = r.run_inputs(IN)
p = pathlib.Path("/home/touhid/Documents/leadpaper/outputs/s22_jointIF.json")
res = json.load(open(p)) if p.exists() else {}
for k, v in out.items():
    res[k] = {"d": v["d"], "e": v["e"], "set": IN[k]["set"]}
    print(k, v["d"], flush=True)
json.dump(res, open(p, "w"), indent=1)
