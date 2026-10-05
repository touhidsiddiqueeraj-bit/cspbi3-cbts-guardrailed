"""S21: thickness x Nt factorial at the joint-optimum base (Reviewer major 6).

2 factors: absorber thickness {0.5, 0.8, 1.0, 1.5} um x Nt {1e14, 1e15} cm-3,
Rs = 0 throughout. Writes outputs/s21_thNt.json.
"""
import sys, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
GEO = {"layer2.NA": 3e16, "layer3.ND": 9e17, "layer2.Eg": 1.65,
       "layer2.chi": 3.928, "layer1.chi": 3.9, "layer3.chi": 3.7}
WP = {"workingpoint": {"temperature": 300, "illumination": 100},
      "iv": {"start": 0, "stop": 1.6, "step": 0.02}}


def S(extra):
    return dict({"load": "csPbI3-CBTS-r7.def"}, set=dict(GEO, **extra), **WP)


IN = {}
for Nt in [1e14, 1e15]:
    for th in [0.5, 0.8, 1.0, 1.5]:
        IN[f"th{th:g}_nt{Nt:.0e}"] = S(
            {"layer2.thickness": th, "layer2.defect1.Ntotal": Nt})


def op(path):
    import re
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


def run_one(jobs):
    r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=1)
    r.sync_parameters()
    return r.run_inputs(jobs)


JSONL = BASE / "outputs" / "s21_thNt.jsonl"
done = {json.loads(l)["id"] for l in JSONL.read_text().splitlines() if l.strip()} \
    if JSONL.exists() else set()
jobs = {k: v for k, v in IN.items() if k not in done}
print("to run:", len(jobs), "already:", len(done), flush=True)

out = run_one(jobs)
bad = [k for k, v in out.items() if not (v["d"] and v["d"].get("eta"))]
for k in bad:                       # solo retry: worker file misses only
    print("solo retry", k, flush=True)
    out.update(run_one({k: jobs[k]}))
with JSONL.open("a") as f:
    for k, v in out.items():
        f.write(json.dumps({"id": k, "d": v["d"], "e": v["e"],
                            "set": jobs[k]["set"]}) + "\n")
rows = [json.loads(l) for l in JSONL.read_text().splitlines() if l.strip()]
res = {x["id"]: x for x in rows}
json.dump(res, open(BASE / "outputs" / "s21_thNt.json", "w"), indent=1)
print("runs", len(res), "ok",
      sum(1 for x in res.values() if x["d"] and x["d"].get("eta")))
print(json.dumps({k: (round(v["d"]["eta"], 4) if v["d"] else None)
                  for k, v in sorted(res.items())}, indent=1))