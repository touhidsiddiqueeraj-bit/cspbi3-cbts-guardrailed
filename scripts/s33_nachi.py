"""S33: NA x chiCBTS interaction (does the 3.9 optimum survive realistic
doping?). Joint base, NA {1e15, 3e16} x chiCBTS {3.6, 3.9} at chiTiO2 3.7.
Merges into outputs/s33_nachi.json."""
import sys, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
J = {"layer2.thickness": 2.2, "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
     "layer2.Eg": 1.65, "layer2.chi": 3.928, "layer3.chi": 3.7}
WP = {"workingpoint": {"temperature": 300, "illumination": 100}}
IV = {"start": 0, "stop": 1.6, "step": 0.02}


def S(extra):
    return dict({"load": "csPbI3-CBTS-r7.def"}, set=dict(extra), **WP, iv=dict(IV))


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
    IN = {}
    for na, ntag in [(1e15, "na15"), (3e16, "na316")]:
        for ch, ctag in [(3.6, "ch36"), (3.9, "ch39")]:
            IN[f"N_{ntag}_{ctag}"] = S(dict(J, **{"layer2.NA": na, "layer1.chi": ch}))
    r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
    r.sync_parameters()
    out = r.run_inputs(IN)
    p = BASE / "outputs" / "s33_nachi.json"
    res = json.load(open(p)) if p.exists() else {}
    for k, v in out.items():
        res[k] = {"d": v["d"], "e": v["e"], "set": IN[k]["set"]}
        print(k, v["d"], v["e"], flush=True)
    json.dump(res, open(p, "w"), indent=1)
    print("s33 done")


if __name__ == "__main__":
    main()
