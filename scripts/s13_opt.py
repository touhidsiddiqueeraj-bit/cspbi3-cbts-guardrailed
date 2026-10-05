"""S13: optimiser over the declared box (Reviewer concern 1).

Stage 1: LHS-48 over 7 dims (seed 13). Stage 2: pattern-search refinement
from top-2 LHS points (2 iters x 14 dirs). All checkpointed in s13_opt.jsonl.
Dims: d [0.4,2.2], logNA [15,16.5], logNt [12,15], logND [16,19],
      Eg [1.65,1.75] (chi linked), logNif [8,12], chiETL [3.8,4.2].
Writes outputs/s13_opt.json + prints optimum.
"""
import sys, json, pathlib
import numpy as np
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict
from scipy.stats import qmc

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
NAMES = ["d", "logNA", "logNt", "logND", "Eg", "logNif", "chiETL"]
BOUNDS = {"d": (0.4, 2.2), "logNA": (15, 16.5), "logNt": (12, 15),
          "logND": (16, 19), "Eg": (1.65, 1.75), "logNif": (8, 12),
          "chiETL": (3.8, 4.2)}
STEP0 = np.array([0.2, 0.25, 0.5, 0.5, 0.02, 0.5, 0.1])  # physical units

CH = {"load": "csPbI3-CBTS-r7.def",
      "workingpoint": {"temperature": 300, "illumination": 100},
      "iv": {"start": 0, "stop": 1.6, "step": 0.02}}


def to_phys(u):
    v = {}
    for i, n in enumerate(NAMES):
        lo, hi = BOUNDS[n]
        v[n] = lo + u[i] * (hi - lo)
    return v


def to_inp(v):
    return dict(CH, set={
        "layer2.thickness": round(v["d"], 3), "layer2.NA": 10**v["logNA"],
        "layer2.defect1.Ntotal": 10**v["logNt"], "layer3.ND": 10**v["logND"],
        "layer2.Eg": round(v["Eg"], 4),
        "layer2.chi": round(3.95 + 0.5 * (v["Eg"] - 1.694), 4),
        "layer3.chi": round(v["chiETL"], 3),
        "interface1.IFdefect1.Ntotal": 10**v["logNif"],
        "interface2.IFdefect1.Ntotal": 10**v["logNif"]})


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


JSONL = BASE / "outputs" / "s13_opt.jsonl"
res = {}
if JSONL.exists():
    for ln in JSONL.read_text().splitlines():
        if ln.strip():
            x = json.loads(ln)
            res[x["id"]] = x

runner = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
runner.sync_parameters()


def run_batch(jobs):
    jobs = {k: v for k, v in jobs.items() if k not in res}
    if not jobs:
        return
    print(f"running {len(jobs)}", flush=True)
    out = runner.run_inputs(jobs)
    with JSONL.open("a") as f:
        for k, v in out.items():
            rec = {"id": k, "d": v["d"], "e": v["e"],
                   "set": jobs[k]["set"], "load": jobs[k]["load"],
                   "u": jobs[k]["_u"]}
            f.write(json.dumps(rec) + "\n")
            res[k] = rec


def eta_of(r):
    d = r["d"]
    return d["eta"] if d and d.get("eta") else None


# ---- Stage 1: LHS-48 ----
lhs = qmc.LatinHypercube(d=7, seed=13).random(48)
jobs = {}
for i, u in enumerate(lhs):
    v = to_phys(u)
    inp = to_inp(v)
    inp["_u"] = u.tolist()
    jobs[f"L{i:02d}"] = inp
run_batch(jobs)

ranked = sorted(((k, eta_of(r)) for k, r in res.items() if k.startswith("L")),
                key=lambda kv: -(kv[1] or -1))
print("LHS top5:", [(k, round(e, 4)) for k, e in ranked[:5]], flush=True)

# ---- Stage 2: pattern search from top-2 ----
for s, (start_id, _) in enumerate(ranked[:2]):
    u = np.array(res[start_id]["u"])
    cur = eta_of(res[start_id])
    step = STEP0.copy()
    # physical ranges for normalisation of steps
    span = np.array([hi - lo for lo, hi in (BOUNDS[n] for n in NAMES)])
    for it in range(2):
        cand = {}
        for j in range(7):
            for sgn in (+1, -1):
                uu = u.copy()
                uu[j] = np.clip(uu[j] + sgn * step[j] / span[j], 0, 1)
                cid = f"P-s{s}i{it}d{j}{'+' if sgn > 0 else '-'}"
                inp = to_inp(to_phys(uu))
                inp["_u"] = uu.tolist()
                cand[cid] = inp
        run_batch(cand)
        best_c = max(cand, key=lambda k: eta_of(res[k]) or -1)
        be = eta_of(res[best_c])
        print(f"start{s} iter{it}: cur={cur:.4f} best_cand={be}", flush=True)
        if be and be > (cur or -1):
            u = np.array(res[best_c]["u"])
            cur = be
        else:
            step = step / 2

allok = {k: round(eta_of(r), 4) for k, r in res.items()
         if eta_of(r) is not None}
best = max(allok.items(), key=lambda kv: kv[1])
print("total", len(res), "ok", len(allok), "BEST", best)
print(json.dumps(res[best[0]], indent=1)[:1500])
json.dump(res, open(BASE / "outputs" / "s13_opt.json", "w"), indent=1)
