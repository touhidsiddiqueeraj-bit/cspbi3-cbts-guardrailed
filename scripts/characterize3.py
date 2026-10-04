"""Retry 3 crashed jobs (qe_champ, qe_base, eb0_champ) with short save names."""
import sys, json, os, glob, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
import numpy as np
from scaps_runner import SCAPSrunner

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
JSONL = BASE / "outputs" / "char.jsonl"
IFD = "csPbI3-CBTS-r7.def"
CHAMP = {"layer2.thickness": 2.2, "layer2.NA": 3e16, "layer2.defect1.Ntotal": 1e12,
         "layer3.ND": 9e17, "layer2.Eg": 1.65, "layer2.chi": 3.928}
FN = {"qe_champ": "rq1.txt", "qe_base": "rq0.txt", "eb0_champ": "re1.txt"}

def build(job):
    kind, p, jid = job["kind"], job["p"], job["id"]
    c = ["clear actions", f"load definitionfile {IFD}"]
    for k, v in p.get("set", {}).items():
        c.append(f"set {k} {v}")
    c += ["action workingpoint.temperature 300", "action intensity.T 100", "action light"]
    if kind == "qe":
        c += ["action qe.startlambda 300", "action qe.stoplambda 850",
              "action qe.points 56", "action qe.doqe",
              "action iv.startv 0", "action iv.stopv 1.6", "action iv.increment 0.05",
              "action iv.doiv", "calculate singleshot", f"save results.qe {FN[jid]}"]
    else:
        c += ["action workingpoint.voltage 0", "calculate singleshot",
              f"save results.eb {FN[jid]}"]
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

SPECS = {"qe": ("lambda(nm)", ["lambda", "QE", "E"]),
         "eb0": ("x(um)", ["i", "x_um", "y", "Ec", "Fn", "Fp", "Ev", "n", "p", "rho_def",
                           "Ndop", "rho", "E", "jn", "jp", "jnt", "jpt", "jtot", "gen",
                           "rec", "cumG", "cumR_LR"])}

jobs = {"qe_champ": {"kind": "qe", "id": "qe_champ", "p": {"set": dict(CHAMP)}},
        "qe_base": {"kind": "qe", "id": "qe_base", "p": {"set": {}}},
        "eb0_champ": {"kind": "eb0", "id": "eb0_champ", "p": {"set": dict(CHAMP)}}}
r = SCAPSrunner(build, lambda rf: {"rf": rf}, ncores=4)
r.sync_parameters()
r.run_inputs({k: v for k, v in jobs.items()})

merged = {}
for jid, info in jobs.items():
    hits = glob.glob(f"/home/touhid/.scaps-runner/proc*/drive_c/Program Files (x86)/Scaps3309/results/{FN[jid]}")
    hits.sort(key=os.path.getmtime, reverse=True)
    if not hits:
        merged[jid] = {"error": "not produced"}
        continue
    try:
        marker, cols = SPECS[info["kind"]]
        merged[jid] = {"file": hits[0], "data": read_table(hits[0], marker, cols)}
    except Exception as e:
        merged[jid] = {"error": str(e)[:200]}
kept = [l for l in JSONL.read_text().splitlines()
        if l.strip() and json.loads(l)["id"] not in merged]
with JSONL.open("w") as f:
    f.write("\n".join(kept) + "\n")
    for jid, v in merged.items():
        f.write(json.dumps({"id": jid, "kind": jobs[jid]["kind"], "data": v}) + "\n")
for jid, v in merged.items():
    print(jid, "OK" if "data" in v else "FAIL", v.get("error", ""))
