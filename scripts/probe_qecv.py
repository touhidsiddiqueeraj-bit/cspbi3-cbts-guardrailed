"""Capability probe: can the runner save QE / CV / EB / GENREC? 4 probes in parallel.
Custom script builder (from_param_dict can't express qe/cv actions). Persistent only."""
import sys, json, os, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner

CHAMP_SET = {"layer2.thickness": 2.2, "layer2.NA": 3e16,
             "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
             "layer2.Eg": 1.65, "layer2.chi": 3.928}
LOAD = "csPbI3-CBTS-r7.def"

def build(kind):
    c = ["clear actions", f"load definitionfile {LOAD}"]
    for k, v in CHAMP_SET.items():
        c.append(f"set {k} {v}")
    c += ["action workingpoint.temperature 300", "action intensity.T 100",
          "action light"]
    if kind == "iv_ctrl":
        c += ["action iv.startv 0", "action iv.stopv 1.6", "action iv.increment 0.02",
              "action iv.doiv", "calculate singleshot"]
    elif kind == "qe":
        c += ["action qe.startlambda 300", "action qe.stoplambda 850",
              "action qe.points 56", "action qe.doqe",
              "action iv.startv 0", "action iv.stopv 1.6", "action iv.increment 0.05",
              "action iv.doiv", "calculate singleshot",
              "save results.qe probe_qe.txt"]
    elif kind == "cv":
        c += ["action workingpoint.frequency 1000000",
              "action cv.startV 0", "action cv.stopV 1.0", "action cv.points 21",
              "action cv.docv", "calculate singleshot",
              "save results.cv probe_cv.txt"]
    elif kind == "ebgr":
        c += ["action iv.startv 0", "action iv.stopv 1.6", "action iv.increment 0.05",
              "action iv.doiv", "calculate singleshot",
              "save results.eb probe_eb.txt", "save results.genrec probe_gr.txt"]
    return "set quitscript.quitSCAPS\nset errorhandling.overwritefile\n" + "\n".join(c) + "\n"

def op(result_file):
    rdir = os.path.dirname(result_file)
    out = {}
    try:
        with open(result_file) as f:
            out["iv_lines"] = len(f.readlines())
    except Exception as e:
        out["iv_error"] = str(e)
    for name in ["probe_qe.txt", "probe_cv.txt", "probe_eb.txt", "probe_gr.txt"]:
        p = os.path.join(rdir, name)
        if os.path.exists(p):
            with open(p, errors="ignore") as f:
                lines = f.readlines()
            out[name] = {"nlines": len(lines), "head": "".join(lines[:12])}
        else:
            out[name] = None
    return out

r = SCAPSrunner(build, op, ncores=4)
r.sync_parameters()
out = r.run_inputs({k: k for k in ["iv_ctrl", "qe", "cv", "ebgr"]})
pathlib.Path("/home/touhid/Documents/leadpaper/outputs/probe_qecv.json").write_text(
    json.dumps(out, indent=1)[:6000])
for k, v in out.items():
    print("=" * 20, k)
    print(json.dumps(v, indent=1)[:1500])
