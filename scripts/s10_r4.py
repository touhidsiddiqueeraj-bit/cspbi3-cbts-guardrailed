"""S10: attainable-gap points (Eg 1.68/1.70/1.72, +Rs1 at 1.70) and Et sweep (def-copy)."""
import sys, json, shutil, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict
BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
BASEDEF = BASE / "defs" / "csPbI3-CBTS-r7.def"
SCADIR = pathlib.Path("/home/touhid/.scaps-runner/scaps_dat/def")

def def_variant(name, old, new):
    t = BASEDEF.read_text()
    assert t.count(old) == 1, old[:60]
    p = BASE / "defs" / name
    p.write_text(t.replace(old, new))
    shutil.copy(p, SCADIR / name)
    return name

# absorber Et block is unique (sigma pair + Et 0.600)
ABS_ET = "sigma_n : 1.000e-19\t[m^2]\nsigma_p : 1.000e-19\t[m^2]\nEt :   0.600\t[eV]"
et03 = def_variant("csPbI3-CBTS-et03.def", ABS_ET, ABS_ET.replace("Et :   0.600", "Et :   0.300"))
et09 = def_variant("csPbI3-CBTS-et09.def", ABS_ET, ABS_ET.replace("Et :   0.600", "Et :   0.900"))

C = {"load": "csPbI3-CBTS-r7.def",
     "set": {"layer2.thickness": 2.2, "layer2.NA": 3e16,
             "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
             "layer2.Eg": 1.65, "layer2.chi": 3.928, "layer3.chi": 3.8},
     "workingpoint": {"temperature": 300, "illumination": 100},
     "iv": {"start": 0, "stop": 1.6, "step": 0.02}}

def S(extra, **kw):
    d = dict(C, set=dict(C["set"], **extra))
    d.update(kw)
    return d

def chilink(eg):
    return round(3.95 + 0.5 * (eg - 1.694), 4)

IN = {
 "eg168": S({"layer2.Eg": 1.68, "layer2.chi": chilink(1.68)}),
 "eg170": S({"layer2.Eg": 1.70, "layer2.chi": chilink(1.70)}),
 "eg172": S({"layer2.Eg": 1.72, "layer2.chi": chilink(1.72)}),
 "eg170_rs1": S({"layer2.Eg": 1.70, "layer2.chi": chilink(1.70), "external.Rs": 1}),
 "et03": S({}, load=et03),
 "et09": S({}, load=et09),
}

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
out = r.run_inputs(IN)
res = {k: {"d": v["deduced"], "e": v["error"]} for k, v in out.items()}
print(json.dumps(res, indent=1))
open(BASE / "outputs" / "s10_r4.json", "w").write(json.dumps(res, indent=1))
