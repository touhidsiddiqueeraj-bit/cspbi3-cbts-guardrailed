"""Re-run 6 char jobs with per-job save names + robust table parser. Merges into char.jsonl."""
import sys, json, os, re, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
import numpy as np
from scaps_runner import SCAPSrunner, parse_jv_curve

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
JSONL = BASE / "outputs" / "char.jsonl"
IFD = "csPbI3-CBTS-r7.def"
CHAMP = {"layer2.thickness": 2.2, "layer2.NA": 3e16, "layer2.defect1.Ntotal": 1e12,
         "layer3.ND": 9e17, "layer2.Eg": 1.65, "layer2.chi": 3.928}

def build(job):
    kind, p, jid = job["kind"], job["p"], job["id"]
    c = ["clear actions", f"load definitionfile {p.get('def', IFD)}"]
    for k, v in p.get("set", {}).items():
        c.append(f"set {k} {v}")
    c += [f"action workingpoint.temperature {p.get('T', 300)}",
          "action intensity.T 100", "action light"]
    if kind == "qe":
        c += ["action qe.startlambda 300", "action qe.stoplambda 850",
              "action qe.points 56", "action qe.doqe",
              "action iv.startv 0", "action iv.stopv 1.6", "action iv.increment 0.05",
              "action iv.doiv", "calculate singleshot",
              f"save results.qe qe_{jid}.txt"]
    elif kind == "cv":
        c += ["action workingpoint.frequency 1000000",
              "action cv.startV 0", "action cv.stopV 1.0", "action cv.points 21",
              "action cv.docv", "calculate singleshot",
              f"save results.cv cv_{jid}.txt"]
    elif kind == "eb0":
        c += ["action workingpoint.voltage 0", "calculate singleshot",
              f"save results.eb eb_{jid}.txt"]
    return "set quitscript.quitSCAPS\nset errorhandling.overwritefile\n" + "\n".join(c) + "\n"

def read_table(path, marker, cols):
    lines = open(path, errors="ignore").readlines()
    si = next(i for i, l in enumerate(lines) if marker in l)
    out = []
    for l in lines[si + 1:]:
        s = l.strip()
        if not s:
            continue
        try:
            vals = [float(x) for x in s.split()]
        except ValueError:
            if out:
                break
            continue
        if len(vals) < len(cols):
            continue
        out.append(vals[:len(cols)])
    if not out:
        raise ValueError("no data rows")
    a = np.array(out, dtype=float)
    return {c: a[:, j].tolist() for j, c in enumerate(cols)}

SPECS = {"qe": ("qe_{id}.txt", "lambda(nm)", ["lambda", "QE", "E"]),
         "cv": ("cv_{id}.txt", "v(V)", ["V", "C", "G", "W", "Napp", "jtot", "jbulk", "jifr"]),
         "eb0": ("eb_{id}.txt", "x(um)", ["i", "x_um", "y", "Ec", "Fn", "Fp", "Ev", "n", "p",
                                          "rho_def", "Ndop", "rho", "E", "jn", "jp", "jnt",
                                          "jpt", "jtot", "gen", "rec", "cumG", "cumR_LR"])}

def op(result_file):
    return {"result_file": result_file}

r = SCAPSrunner(build, op, ncores=4)
r.sync_parameters()

jobs = {}
for tag, s in [("champ", CHAMP), ("base", {})]:
    for kind in ["qe", "cv", "eb0"]:
        jid = f"{kind}_{tag}"
        jobs[jid] = {"kind": kind, "id": jid, "p": {"set": dict(s)}}
out = r.run_inputs({k: v for k, v in jobs.items()})

# parse in main process (files persist in worker results dirs)
import glob
merged = {}
for jid, info in jobs.items():
    fname, marker, cols = SPECS[info["kind"]]
    fname = fname.format(id=jid)
    hits = glob.glob(f"/home/touhid/.scaps-runner/proc*/drive_c/Program Files (x86)/Scaps3309/results/{fname}")
    if not hits:
        merged[jid] = {"error": f"{fname} not produced"}
        continue
    # newest file wins (re-run); check mtime
    hits.sort(key=os.path.getmtime, reverse=True)
    try:
        merged[jid] = {"file": hits[0], "data": read_table(hits[0], marker, cols)}
    except Exception as e:
        merged[jid] = {"error": str(e)[:200]}

# rewrite char.jsonl: drop old 6 char ids, keep IV/T/audit rows, append new
kept = [l for l in JSONL.read_text().splitlines()
        if l.strip() and json.loads(l)["id"] not in merged]
kinds = {"qe": "qe", "cv": "cv", "eb0": "eb0"}
with JSONL.open("w") as f:
    f.write("\n".join(kept) + "\n")
    for jid, v in merged.items():
        f.write(json.dumps({"id": jid, "kind": kinds[jobs[jid]["kind"]], "data": v}) + "\n")
for jid, v in merged.items():
    if "data" in v:
        dd = v["data"]
        k = list(dd.keys())[0]
        print(jid, "OK rows=", len(dd[k]))
    else:
        print(jid, "FAIL", v.get("error"))
