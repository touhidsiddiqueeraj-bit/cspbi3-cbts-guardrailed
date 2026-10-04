"""Baseline verification: 4 combos SIMULTANEOUSLY (not one-at-a-time).
Persistent paths only. Run: PYTHONPATH=~/scaps-runner/src python3 thisfile."""
import sys, json, re, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
import numpy as np
from scaps_runner import SCAPSrunner, parse_jv_curve
from scaps_runner.script_gen import from_param_dict

OUT = pathlib.Path("/home/touhid/Documents/leadpaper/outputs/baseline_results.json")
RCP = pathlib.Path("/home/touhid/Documents/leadpaper/receipts/receipt_baseline.json")

def parse_deduced(path):
    txt = open(path, errors="ignore").read()
    d = {}
    for k, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"),
                   ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                   ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"),
                   ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt)
        d[k] = float(m.group(1)) if m else None
    return d

def ip(p):
    return from_param_dict(p)

def op(path):
    try:
        J, V = parse_jv_curve(path)
        ded = parse_deduced(path)
        # PCE cross-check from JV max power (1-sun 100 mW/cm2)
        pmax = float(np.max(np.array(V) * np.array(J))) if len(V) else None
        return {"deduced": ded, "pmax_mWcm2": pmax, "npts": len(V),
                "V": np.array(V).tolist(), "J": np.array(J).tolist()}
    except Exception as e:
        return {"error": str(e)}

r = SCAPSrunner(ip, op, ncores=4)
r.sync_parameters()

LOAD = "csPbI3-CBTS-r7.def"
inputs = {
    # baseline per Hossain Table 1 (800nm, NA1e15, Nt1e15)
    "base_800nm": {"load": LOAD,
        "workingpoint": {"temperature": 300, "illumination": 100},
        "iv": {"start": 0, "stop": 1.4, "step": 0.02}},
    # paper optimum thickness 1500nm = 1.5 um (SCAPS set uses um, NOT m)
    "opt_1500nm": {"load": LOAD, "set": {"layer2.thickness": 1.5},
        "workingpoint": {"temperature": 300, "illumination": 100},
        "iv": {"start": 0, "stop": 1.4, "step": 0.02}},
    # paper optimum NA 1e16 cm-3 (set uses cm-3 — see UNITS.md)
    "opt_NA16": {"load": LOAD, "set": {"layer2.thickness": 1.5, "layer2.NA": 1e16},
        "workingpoint": {"temperature": 300, "illumination": 100},
        "iv": {"start": 0, "stop": 1.4, "step": 0.02}},
    # paper optimum Nt 1e12 cm-3 (set uses cm-3)
    "opt_Nt12": {"load": LOAD, "set": {"layer2.thickness": 1.5, "layer2.NA": 1e16,
                                       "layer2.defect1.Ntotal": 1e12},
        "workingpoint": {"temperature": 300, "illumination": 100},
        "iv": {"start": 0, "stop": 1.4, "step": 0.02}},
}
out = r.run_inputs(inputs)
# strip JV arrays for receipt lightness, keep full in OUT
lite = {k: {"deduced": v.get("deduced"), "pmax": v.get("pmax_mWcm2"),
            "npts": v.get("npts"), "error": v.get("error")} for k, v in out.items()}
OUT.write_text(json.dumps(out, indent=1))
RCP.write_text(json.dumps({"inputs": inputs, "summary": lite,
    "def": LOAD, "note": "Hossain NJC2023 repro; Nc/Nv capped (see REFERENCES T0a)"}, indent=1))
print(json.dumps(lite, indent=1))
