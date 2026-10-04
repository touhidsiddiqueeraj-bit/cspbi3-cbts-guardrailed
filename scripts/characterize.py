"""Full characterization + guardrail audit in ONE parallel batch (20 jobs, 4 workers).
Kinds: qe/cv/eb0 (custom scripts) + iv (T-sweep, audit grids, dup).
EB file carries bands + generation + recombination (genrec save is occupation-only, skipped).
Resume-safe JSONL. SET-UNITS: um, cm-3, eV (see UNITS.md). Persistent only."""
import sys, json, os, re, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
import numpy as np
from scaps_runner import SCAPSrunner, parse_jv_curve

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
JSONL = BASE / "outputs" / "char.jsonl"
IFD = "csPbI3-CBTS-r7.def"
NOD = "csPbI3-CBTS-noIF.def"
CHAMP = {"layer2.thickness": 2.2, "layer2.NA": 3e16, "layer2.defect1.Ntotal": 1e12,
         "layer3.ND": 9e17, "layer2.Eg": 1.65, "layer2.chi": 3.928}
BASELINE_SET = {}

def build(job):
    kind, p = job["kind"], job["p"]
    c = ["clear actions", f"load definitionfile {p.get('def', IFD)}"]
    for k, v in p.get("set", {}).items():
        c.append(f"set {k} {v}")
    c += [f"action workingpoint.temperature {p.get('T', 300)}",
          "action intensity.T 100", "action light"]
    if kind == "iv":
        c += ["action iv.startv 0", "action iv.stopv 1.6", "action iv.increment 0.02",
              "action iv.doiv", "calculate singleshot"]
    elif kind == "qe":
        c += ["action qe.startlambda 300", "action qe.stoplambda 850",
              "action qe.points 56", "action qe.doqe",
              "action iv.startv 0", "action iv.stopv 1.6", "action iv.increment 0.05",
              "action iv.doiv", "calculate singleshot",
              "save results.qe save_qe.txt"]
    elif kind == "cv":
        c += ["action workingpoint.frequency 1000000",
              "action cv.startV 0", "action cv.stopV 1.0", "action cv.points 21",
              "action cv.docv", "calculate singleshot",
              "save results.cv save_cv.txt"]
    elif kind == "eb0":
        c += ["action workingpoint.voltage 0", "calculate singleshot",
              "save results.eb save_eb.txt"]
    return "set quitscript.quitSCAPS\nset errorhandling.overwritefile\n" + "\n".join(c) + "\n"

def read_table(path, marker, cols):
    lines = open(path, errors="ignore").readlines()
    si = next(i for i, l in enumerate(lines) if l.strip().startswith(marker))
    out = []
    for l in lines[si + 1:]:
        s = l.strip()
        if not s:
            break
        try:
            vals = [float(x) for x in s.split()]
        except ValueError:
            break
        if len(vals) < len(cols):
            continue
        out.append(vals[:len(cols)])
    a = np.array(out)
    return {c: a[:, j].tolist() for j, c in enumerate(cols)}

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

def op(result_file):
    rdir = os.path.dirname(result_file)
    out = {}
    try:
        J, V = parse_jv_curve(result_file)
        out["deduced"] = parse_deduced(result_file)
        out["npts"] = len(V)
    except Exception as e:
        out["iv_error"] = str(e)
    for name, marker, cols in [
            ("save_qe.txt", "lambda(nm)", ["lambda", "QE", "E"]),
            ("save_cv.txt", "v(V)", ["V", "C", "G", "W", "Napp", "jtot", "jbulk", "jifr"]),
            ("save_eb.txt", "i", ["i", "x_um", "y", "Ec", "Fn", "Fp", "Ev", "n", "p",
                                  "rho_def", "Ndop", "rho", "E", "jn", "jp", "jnt",
                                  "jpt", "jtot", "gen", "rec", "cumG", "cumR_LR"])]:
        p = os.path.join(rdir, name)
        if os.path.exists(p):
            try:
                out[name] = read_table(p, marker, cols)
            except Exception as e:
                out[name + "_error"] = str(e)[:200]
    return out

jobs = {}
# --- characterization: QE + CV + EB@0V, champion vs baseline ---
jobs["qe_champ"] = {"kind": "qe", "p": {"set": dict(CHAMP)}}
jobs["qe_base"] = {"kind": "qe", "p": {"set": {}}}
jobs["cv_champ"] = {"kind": "cv", "p": {"set": dict(CHAMP)}}
jobs["cv_base"] = {"kind": "cv", "p": {"set": {}}}
jobs["eb0_champ"] = {"kind": "eb0", "p": {"set": dict(CHAMP)}}
jobs["eb0_base"] = {"kind": "eb0", "p": {"set": {}}}
# --- T sweep champion (Hossain Fig27 parity) ---
for T in [275, 300, 350, 400, 475]:
    jobs[f"T{T}"] = {"kind": "iv", "p": {"set": dict(CHAMP), "T": T}}
# --- audit: same 4 cells with vs without interfaces ---
for th in [1.5, 2.0]:
    for na, nt in [(1e16, 1e12)]:
        s = {"layer2.thickness": th, "layer2.NA": na, "layer2.defect1.Ntotal": nt,
             "layer3.ND": 9e17, "layer2.Eg": 1.65, "layer2.chi": 3.928}
        jobs[f"audit_IF_th{th}"] = {"kind": "iv", "p": {"set": dict(s)}}
        jobs[f"audit_noIF_th{th}"] = {"kind": "iv",
                                      "p": {"set": dict(s), "def": NOD}}
# champion without interfaces (inflation demo) + reproducibility dup
s = dict(CHAMP)
jobs["audit_noIF_champ"] = {"kind": "iv", "p": {"set": dict(s), "def": NOD}}
jobs["dup_champ"] = {"kind": "iv", "p": {"set": dict(s)}}
print("jobs:", len(jobs))

done = set()
if JSONL.exists():
    for ln in JSONL.read_text().splitlines():
        if ln.strip():
            done.add(json.loads(ln)["id"])
todo = {k: v for k, v in jobs.items() if k not in done}
print("to run:", len(todo))

r = SCAPSrunner(build, op, ncores=4)
r.sync_parameters()
out = r.run_inputs(todo)
with JSONL.open("a") as f:
    for k, v in out.items():
        slim = dict(v)
        f.write(json.dumps({"id": k, "kind": jobs[k]["kind"], "data": slim}) + "\n")
print("=== IV summary ===")
for k, v in out.items():
    if jobs[k]["kind"] == "iv":
        print(k, v.get("deduced"))
