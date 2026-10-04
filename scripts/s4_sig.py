"""S4: rerun lost if1e11 + bulk Nt x sigma joint via def copies."""
import sys, json, re, shutil, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
BASEDEF = BASE / "defs" / "csPbI3-CBTS-r7.def"
SCADIR = pathlib.Path("/home/touhid/.scaps-runner/scaps_dat/def")

ABS_SIG = "sigma_n : 1.000e-19\t[m^2]\nsigma_p : 1.000e-19\t[m^2]\nEt :   0.600\t[eV]"
def sig_variant(name, scale):
    t = BASEDEF.read_text()
    assert t.count(ABS_SIG) == 1
    rep = f"sigma_n : {1e-19*scale:.3e}\t[m^2]\nsigma_p : {1e-19*scale:.3e}\t[m^2]\nEt :   0.600\t[eV]"
    p = BASE / "defs" / name
    p.write_text(t.replace(ABS_SIG, rep))
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
 "if1e11": dict(CH, set=dict(CH["set"], **{"interface1.IFdefect1.Ntotal": 1e11,
                                            "interface2.IFdefect1.Ntotal": 1e11})),
 "sigX10_Nt12": dict(CH, load=sig_variant("csPbI3-CBTS-sigX10.def", 10)),
 "sigX10_Nt15": dict(CH, load=sig_variant("csPbI3-CBTS-sigX10.def", 10),
                     set=dict(CH["set"], **{"layer2.defect1.Ntotal": 1e15})),
}
r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
out = r.run_inputs(IN)
res = {k: {"d": v["deduced"], "e": v["error"]} for k, v in out.items()}
print(json.dumps(res, indent=1))
open(BASE / "outputs" / "s4_sig.json", "w").write(json.dumps(res, indent=1))
