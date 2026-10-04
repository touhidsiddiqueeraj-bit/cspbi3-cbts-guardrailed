"""S1: interface N dose + sigma test, Rs/Rsh grid, WF grid, bulk Nt x sigma."""
import sys, json, re, shutil, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
BASEDEF = BASE / "defs" / "csPbI3-CBTS-r7.def"
SCADIR = pathlib.Path("/home/touhid/.scaps-runner/scaps_dat/def")

def def_variant(name, subs):
    t = BASEDEF.read_text()
    for a, b in subs:
        assert a in t, a
        t = t.replace(a, b)
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

def S(extra):
    return dict(CH, set=dict(CH["set"], **extra))

IN = {
 # interface N dose (both sides, cm-2)
 "if1e8": S({"interface1.IFdefect1.Ntotal": 1e8, "interface2.IFdefect1.Ntotal": 1e8}),
 "if3e9": S({"interface1.IFdefect1.Ntotal": 3e9, "interface2.IFdefect1.Ntotal": 3e9}),
 "if3e10": S({"interface1.IFdefect1.Ntotal": 3e10, "interface2.IFdefect1.Ntotal": 3e10}),
 "if1e11": S({"interface1.IFdefect1.Ntotal": 1e11, "interface2.IFdefect1.Ntotal": 1e11}),
 "if1e12": S({"interface1.IFdefect1.Ntotal": 1e12, "interface2.IFdefect1.Ntotal": 1e12}),
 # asymmetric: ETL-side only vs HTL-side only at 1e12
 "ifETL1e12": S({"interface2.IFdefect1.Ntotal": 1e12}),
 "ifHTL1e12": S({"interface1.IFdefect1.Ntotal": 1e12}),
 # interface sigma x10 syntax test
 "ifsigX10": S({"interface1.IFdefect1.capture_cross_section.electron": 1e-18,
                "interface1.IFdefect1.capture_cross_section.hole": 1e-18}),
 # Rs/Rsh grid (have Rs0, Rs1)
 "rs05": S({"external.Rs": 0.5}),
 "rs2": S({"external.Rs": 2}),
 "rsh4": S({"external.Rsh": 1e4}),
 "rs1rsh4": S({"external.Rs": 1, "external.Rsh": 1e4}),
}
# WF grid via def copies (have 5.5/4.0 baseline, Ni5.0, ITO4.4)
IN["wfNi52"] = dict(CH, load=def_variant("csPbI3-CBTS-wfNi52.def", [("Fi_m :   5.5000 [eV]", "Fi_m :   5.2000 [eV]")]))
IN["wfITO47"] = dict(CH, load=def_variant("csPbI3-CBTS-wfITO47.def", [("Fi_m :  4.00 [eV]", "Fi_m :  4.70 [eV]")]))

r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
out = r.run_inputs(IN)
res = {k: {"params": dict(IN[k].get("set", {})), "load": IN[k]["load"],
           "d": v["deduced"], "e": v["error"]} for k, v in out.items()}
print(json.dumps({k: (v["d"], v["e"]) for k, v in res.items()}, indent=1))
open(BASE / "outputs" / "s1_dose.json", "w").write(json.dumps(res, indent=1))
