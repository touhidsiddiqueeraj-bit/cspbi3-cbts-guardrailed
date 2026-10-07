"""S28: calibration attempt (bounded, 5 runs). Routine-base toward a
Dai-like measured point: Nt 1e14, Nif 3e10, Eg 1.70 + chi-link, Rs 1,
ITO 4.2 (wfITO42 def), mu 10/5, Cr 1e-10; d in {0.6, 0.8, 1.0} +
d0.8 x Nt {3e14, 1e15}. Target: ~21.5-22% with Voc ~1.25 V.
Merges into outputs/s28_calib.json."""
import sys, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
CAL = {"layer2.NA": 3e16, "layer3.ND": 9e17, "layer2.Eg": 1.70,
       "layer2.chi": 3.953, "layer2.radiative": 1e-10,
       "external.Rs": 1, "layer2.mun": 10, "layer2.mup": 5,
       "interface1.IFdefect1.Ntotal": 3e10,
       "interface2.IFdefect1.Ntotal": 3e10}
WP = {"workingpoint": {"temperature": 300, "illumination": 100}}
IV = {"start": 0, "stop": 1.6, "step": 0.02}


def S(extra):
    return dict({"load": "csPbI3-CBTS-wfITO42.def"}, set=dict(extra),
                **WP, iv=dict(IV))


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
        "C_d06": S(dict(CAL, **{"layer2.thickness": 0.6, "layer2.defect1.Ntotal": 1e14})),
        "C_d08": S(dict(CAL, **{"layer2.thickness": 0.8, "layer2.defect1.Ntotal": 1e14})),
        "C_d10": S(dict(CAL, **{"layer2.thickness": 1.0, "layer2.defect1.Ntotal": 1e14})),
        "C_d08_nt3e14": S(dict(CAL, **{"layer2.thickness": 0.8, "layer2.defect1.Ntotal": 3e14})),
        "C_d08_nt1e15": S(dict(CAL, **{"layer2.thickness": 0.8, "layer2.defect1.Ntotal": 1e15})),
    }
    r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
    r.sync_parameters()
    out = r.run_inputs(IN)
    p = BASE / "outputs" / "s28_calib.json"
    res = json.load(open(p)) if p.exists() else {}
    for k, v in out.items():
        res[k] = {"d": v["d"], "e": v["e"], "set": IN[k]["set"]}
        print(k, v["d"], v["e"], flush=True)
    json.dump(res, open(p, "w"), indent=1)
    print("s28 done")


if __name__ == "__main__":
    main()
