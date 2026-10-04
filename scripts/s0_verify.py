"""S0: verify set-commandability of interfaces/Rs/Rsh + WF via def copies."""
import sys, json, re, shutil, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
BASEDEF = BASE / "defs" / "csPbI3-CBTS-r7.def"
SCADIR = pathlib.Path("/home/touhid/.scaps-runner/scaps_dat/def")

def wf_variant(name, back=None, front=None):
    t = BASEDEF.read_text()
    if back: t = t.replace("Fi_m :   5.5000 [eV]", f"Fi_m :   {back:.4f} [eV]")
    if front: t = t.replace("Fi_m :  4.00 [eV]", f"Fi_m :  {front:.2f} [eV]")
    p = BASE / "defs" / name
    p.write_text(t)
    shutil.copy(p, SCADIR / name)
    return name

CH = {"load": "csPbI3-CBTS-r7.def",
      "set": {"layer2.thickness": 2.2, "layer2.NA": 3e16,
              "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
              "layer2.Eg": 1.65, "layer2.chi": 3.928},
      "workingpoint": {"temperature": 300, "illumination": 100},
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
    return {"deduced": d, "error": None if d["eta"] else "no-eta"}

IN = {
 "ifN1e9": dict(CH, set=dict(CH["set"], **{"interface1.IFdefect1.Ntotal": 1e9,
                                            "interface2.IFdefect1.Ntotal": 1e9})),
 "rs1": dict(CH, set=dict(CH["set"], **{"external.Rs": 1})),
 "rsh3": dict(CH, set=dict(CH["set"], **{"external.Rsh": 1e3})),
 "wfNi50": dict(CH, load=wf_variant("csPbI3-CBTS-wfNi50.def", back=5.0)),
 "wfITO44": dict(CH, load=wf_variant("csPbI3-CBTS-wfITO44.def", front=4.4)),
}
r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
out = r.run_inputs(IN)
res = {k: {"d": v["deduced"], "e": v["error"]} for k, v in out.items()}
print(json.dumps(res, indent=1))
open(BASE / "outputs" / "s0_verify.json", "w").write(json.dumps(res, indent=1))
