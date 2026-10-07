"""S35: baseline validation (source DOS + no interfaces) and Eperon
hindcast pair. (NA x chiCBTS already covered by s33_nachi.py.)
Merges into outputs/s35_phys.json."""
import sys, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
J = {"layer2.thickness": 2.2, "layer2.NA": 3e16, "layer2.defect1.Ntotal": 1e12,
     "layer3.ND": 9e17, "layer2.Eg": 1.65, "layer2.chi": 3.928, "layer3.chi": 3.7}
SRC_DOS = {"layer2.Nc": 1.1e20, "layer2.Nv": 8.2e20}
WP = {"workingpoint": {"temperature": 300, "illumination": 100}}
IV = {"start": 0, "stop": 1.6, "step": 0.02}


def S(extra, load="csPbI3-CBTS-r7.def"):
    return dict({"load": load}, set=dict(extra), **WP, iv=dict(IV))


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
    return {"d": d, "e": None if d["eta"] else "no-eta"}


def main():
    IN = {
        # baseline validation: source DOS, no interfaces (Hossain 19.06 test)
        "V_srcnoif": S(dict(SRC_DOS), load="csPbI3-CBTS-noIF.def"),
        # Eperon hindcast: 260 nm, Nt from measured tau (sigma=1e-19 m2)
        # vapour tau~10us -> Nt 1e13; spin tau~0.2us -> Nt 5e14; mu 25 measured
        "H_vapour": S({"layer2.thickness": 0.26, "layer2.NA": 1e15,
                       "layer2.defect1.Ntotal": 1e13, "layer3.ND": 9e16}),
        "H_spin": S({"layer2.thickness": 0.26, "layer2.NA": 1e15,
                     "layer2.defect1.Ntotal": 5e14, "layer3.ND": 9e16}),
    }
    r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
    r.sync_parameters()
    out = r.run_inputs(IN)
    p = BASE / "outputs" / "s35_phys.json"
    res = json.load(open(p)) if p.exists() else {}
    for k, v in out.items():
        res[k] = {"d": v["d"], "e": v["e"], "set": IN[k]["set"]}
        print(k, v["d"], v["e"], flush=True)
    json.dump(res, open(p, "w"), indent=1)
    print("s35 done")


if __name__ == "__main__":
    main()
