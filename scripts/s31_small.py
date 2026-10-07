"""S31: screen self-consistency + spectrum discrimination (small batch).

- J_dos03_cr10 / J_dos05_cr10: physical DOS + Cr 1e-10. Pre-registered
  expectation: Voc falls back under the 1.371 V screen (radiative channel
  present), making the screen self-consistent.
- SRC_base / SRC_routine: source-paper DOS (Nc 1.1e20 / Nv 8.2e20) at
  baseline {} and routine (1.0 um, Nt 1e15) sets. Shows replication
  dependence on the DOS cap.
- J_AM0: champion IV under AM0.spe. Pre-registered: 20.2 if SCAPS
  normalises to 1 sun, ~27.3 if it uses file power as-is (1347 W/m2).
- J_band500: spectrumcutoff 500-510 nm test of flux handling; expected
  Jsc = QE(505 nm) x band power / hc (computed post-hoc from .spe).
Merges into outputs/s31_small.json. Custom raw scripts where needed.
"""
import sys, json, os, re, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
NEW = {"layer2.thickness": 2.2, "layer2.NA": 3e16,
       "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
       "layer2.Eg": 1.65, "layer2.chi": 3.928,
       "layer1.chi": 3.9, "layer3.chi": 3.7}
ROUTINE = {"layer2.thickness": 1.0, "layer2.NA": 3e16,
           "layer2.defect1.Ntotal": 1e15, "layer3.ND": 9e17,
           "layer2.Eg": 1.65, "layer2.chi": 3.928}
WP = {"workingpoint": {"temperature": 300, "illumination": 100}}
IV = {"start": 0, "stop": 1.6, "step": 0.02}


def S(extra, load="csPbI3-CBTS-r7.def"):
    return dict({"load": load}, set=dict(extra), **WP, iv=dict(IV))


def op(path):
    txt = open(path, errors="ignore").read()
    d = {}
    for k, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"),
                   ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                   ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"),
                   ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt)
        d[k] = float(m.group(1)) if m else None
    return {"d": d, "e": None if d["eta"] else "no-eta"}


def raw(extra_lines, sets):
    c = ["clear actions", "load definitionfile csPbI3-CBTS-r7.def"]
    for k, val in sets.items():
        c.append(f"set {k} {val}")
    c += extra_lines
    c += ["action workingpoint.temperature 300", "action intensity.T 100", "action light",
          "action iv.startv 0", "action iv.stopv 1.6", "action iv.increment 0.02",
          "action iv.doiv", "calculate singleshot"]
    return "set quitscript.quitSCAPS\nset errorhandling.overwritefile\n" + "\n".join(c) + "\n"


def main():
    IN = {
        "J_dos03_cr10": S(dict(NEW, **{"layer2.Nv": 4.1e18, "layer2.radiative": 1e-10})),
        "J_dos05_cr10": S(dict(NEW, **{"layer2.Nv": 8.9e18, "layer2.radiative": 1e-10})),
        "SRC_base": S({"layer2.Nc": 1.1e20, "layer2.Nv": 8.2e20}),
        "SRC_routine": S(dict(ROUTINE, **{"layer2.Nc": 1.1e20, "layer2.Nv": 8.2e20})),
    }
    RAW = {
        "J_AM0": raw(["load spectrumfile AM0.spe"], NEW),
        "J_band500": raw(["action spectrumcutoff on",
                          "action spectrumcutoff shortlambda 500",
                          "action spectrumcutoff longlambda 510"], NEW),
    }
    r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
    r.sync_parameters()
    out = r.run_inputs(IN)
    r2 = SCAPSrunner(lambda q: q, op, ncores=2)
    out2 = r2.run_inputs(RAW)
    p = BASE / "outputs" / "s31_small.json"
    res = json.load(open(p)) if p.exists() else {}
    for k, v in out.items():
        res[k] = {"d": v["d"], "e": v["e"], "set": IN[k]["set"]}
        print(k, v["d"], v["e"], flush=True)
    for k, v in out2.items():
        res[k] = {"d": v["d"], "e": v["e"], "note": "raw-script illumination test"}
        print(k, v["d"], v["e"], flush=True)
    json.dump(res, open(p, "w"), indent=1)
    print("s31 done")


if __name__ == "__main__":
    main()
