"""R1b: saved-definition readback (the `set`/`get` console is not captured by
the runner, so we save the definition file after set commands and read the
stored field back) + two base_c4 determinism repeats that crashed in the R1
batch while stale wine/X sessions were being torn down.

Writes outputs/s10_checkdef.json (fields + base repeats).
"""
import sys, json, re, pathlib, glob, os
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")

CH = {"load": "csPbI3-CBTS-r7.def",
      "set": {"layer2.thickness": 2.2, "layer2.NA": 3e16,
              "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
              "layer2.Eg": 1.65, "layer2.chi": 3.928},
      "workingpoint": {"temperature": 300, "illumination": 100},
      "iv": {"start": 0, "stop": 1.6, "step": 0.02}}

RAW = ("clear actions\n"
       "load definitionfile csPbI3-CBTS-r7.def\n"
       "set layer2.NA 1e16\n"
       "set interface1.IFdefect1.capture_cross_section.electron 1e-14\n"
       "set interface1.IFdefect1.capture_cross_section.hole 1e-14\n"
       "save settings definitionfile R1_checkdef.def\n")

IN = {"base_c4_b2": dict(CH), "base_c4_b3": dict(CH),
      "raw_script": {"raw": RAW}}


def proc(p):
    if isinstance(p, dict) and "raw" in p:
        return p["raw"]
    return from_param_dict(p)


def op(path):
    try:
        txt = open(path, errors="ignore").read()
    except OSError:
        return {"d": None, "e": "missing-result-file"}
    d = {}
    for k, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"),
                   ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                   ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"),
                   ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt)
        d[k] = float(m.group(1)) if m else None
    return {"d": d, "e": None if d["eta"] else "no-eta"}


def op2(path):
    """raw job: only need the result file to exist (IV parse optional)."""
    return op(path)


r = SCAPSrunner(proc, op, ncores=4)
r.sync_parameters()
out = r.run_inputs(IN)

readback = {"runs": {k: v for k, v in out.items()},
            "found": [], "fields": []}
hits = glob.glob(os.path.expanduser("~/.scaps-runner/proc*/**/R1_checkdef.def"),
                 recursive=True)
hits.sort(key=os.path.getmtime, reverse=True)
readback["found"] = hits[:3]
if hits:
    lines = open(hits[0], errors="ignore").read().splitlines()
    for ln in lines:
        s = ln.strip()
        if s.startswith(("sigma_nleft", "sigma_nright", "sigma_pleft", "sigma_pright")):
            readback["fields"].append(s)
        if s.startswith("Nleft") or s.startswith("Nright"):
            readback["fields"].append(s)
open(BASE / "outputs" / "s10_checkdef.json", "w").write(json.dumps(readback, indent=1))
print(json.dumps(readback, indent=1))
