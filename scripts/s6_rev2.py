"""S6: sigma verify (def-copy + set-key), chi_CBTS sweep, Nt1e15 mini-grid,
realistic combo, noIF JV archival."""
import sys, json, re, shutil, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner, parse_jv_curve
from scaps_runner.script_gen import from_param_dict
import numpy as np

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
BASEDEF = BASE / "defs" / "csPbI3-CBTS-r7.def"
SCADIR = pathlib.Path("/home/touhid/.scaps-runner/scaps_dat/def")

def def_variant(name, subs):
    t = BASEDEF.read_text()
    for a, b in subs:
        assert a in t, a[:50]
        t = t.replace(a, b)
    p = BASE / "defs" / name
    p.write_text(t)
    shutil.copy(p, SCADIR / name)
    return name

SIG4 = ["sigma_nleft : 1.000e-19 [m^2]", "sigma_nright : 1.000e-19 [m^2]",
        "sigma_pleft : 1.000e-19 [m^2]", "sigma_pright : 1.000e-19 [m^2]"]
ifsig = def_variant("csPbI3-CBTS-ifsigX10.def",
                    [(s, s.replace("1.000e-19", "1.000e-18")) for s in SIG4])
ABS_SIG = "sigma_n : 1.000e-19\t[m^2]\nsigma_p : 1.000e-19\t[m^2]\nEt :   0.600\t[eV]"
t = BASEDEF.read_text(); assert t.count(ABS_SIG) == 1
bsiglo = def_variant("csPbI3-CBTS-bsigX01.def",
                     [(ABS_SIG, ABS_SIG.replace("1.000e-19", "1.000e-20"))])

CH = {"load": "csPbI3-CBTS-r7.def",
      "set": {"layer2.thickness": 2.2, "layer2.NA": 3e16,
              "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
              "layer2.Eg": 1.65, "layer2.chi": 3.928},
      "workingpoint": {"temperature": 300, "illumination": 100},
      "iv": {"start": 0, "stop": 1.6, "step": 0.02}}

def S(extra, **kw):
    d = dict(CH, set=dict(CH["set"], **extra))
    d.update(kw)
    return d

IN = {
 "ifsig_setkey": S({"interface1.IFdefect1.capture_cross_section.electron": 1e-18,
                    "interface1.IFdefect1.capture_cross_section.hole": 1e-18,
                    "interface2.IFdefect1.capture_cross_section.electron": 1e-18,
                    "interface2.IFdefect1.capture_cross_section.hole": 1e-18}),
 "ifsig_defcopy": S({}, load=ifsig),
 "bsigX01_Nt12": S({}, load=bsiglo),
 "chi34": S({"layer1.chi": 3.4}), "chi35": S({"layer1.chi": 3.5}),
 "chi37": S({"layer1.chi": 3.7}), "chi38": S({"layer1.chi": 3.8}),
 "nt15_d05": S({"layer2.thickness": 0.5, "layer2.defect1.Ntotal": 1e15}),
 "nt15_d08": S({"layer2.thickness": 0.8, "layer2.defect1.Ntotal": 1e15}),
 "nt15_d10": S({"layer2.thickness": 1.0, "layer2.defect1.Ntotal": 1e15}),
 "nt15_d15": S({"layer2.thickness": 1.5, "layer2.defect1.Ntotal": 1e15}),
 "nt15_d08_na15": S({"layer2.thickness": 0.8, "layer2.defect1.Ntotal": 1e15,
                     "layer2.NA": 1e15}),
 "realcombo": S({"layer2.thickness": 0.8, "layer2.defect1.Ntotal": 1e15},
                load="csPbI3-CBTS-wfITO44.def"),
 "noIF_JV": S({"layer2.thickness": 2.2}, load="csPbI3-CBTS-noIF.def"),
}

def op(path):
    txt = open(path, errors="ignore").read()
    d = {}
    for k, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"), ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                   ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"), ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt); d[k] = float(m.group(1)) if m else None
    out = {"deduced": d, "error": None if d["eta"] else "no-eta"}
    if "noIF_JV" in path or True:
        try:
            J, V = parse_jv_curve(path)
            out["V"] = np.array(V).tolist(); out["J"] = np.array(J).tolist()
        except Exception:
            pass
    return out

r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
out = r.run_inputs(IN)
res = {k: {"d": v["deduced"], "e": v["error"]} for k, v in out.items()}
print(json.dumps(res, indent=1))
open(BASE / "outputs" / "s6_rev2.json", "w").write(json.dumps(res, indent=1))
nj = out["noIF_JV"]
open(BASE / "outputs" / "noIF_JV.json", "w").write(json.dumps(
    {"deduced": nj["deduced"], "V": nj.get("V"), "J": nj.get("J")}, indent=1))
