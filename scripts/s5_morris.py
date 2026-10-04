"""S5: Morris sensitivity (r=8 trajectories, k=6 factors, p=4 levels) on champion stack."""
import sys, json, re, pathlib
import numpy as np
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
rng = np.random.default_rng(7)
p, r, k = 4, 8, 6
DELTA = p / (2 * (p - 1))
NAMES = ["d", "logNA", "logNt", "logND", "Eg", "logNif"]
BOUNDS = {"d": (0.4, 2.2), "logNA": (15, 16.5), "logNt": (12, 15),
          "logND": (16, 19), "Eg": (1.65, 1.75), "logNif": (8, 12)}

def scale(u):
    v = {}
    for i, n in enumerate(NAMES):
        lo, hi = BOUNDS[n]
        v[n] = lo + u[i] * (hi - lo)
    return {"thickness": v["d"], "NA": 10**v["logNA"], "Nt": 10**v["logNt"],
            "ND": 10**v["logND"], "Eg": v["Eg"],
            "chi": 3.95 + 0.5 * (v["Eg"] - 1.694), "Nif": 10**v["logNif"]}

def traj():
    x0 = rng.integers(0, p, size=k) / (p - 1)
    order = rng.permutation(k)
    signs = rng.choice([-1.0, 1.0], size=k)
    pts, seq = [x0.copy()], []
    x = x0.copy()
    for j in order:
        step = signs[j] * DELTA
        if not (0 <= x[j] + step <= 1):
            step = -step
        x = x.copy(); x[j] += step
        pts.append(x.copy()); seq.append((j, step))
    return pts, seq

CH = {"load": "csPbI3-CBTS-r7.def", "workingpoint": {"temperature": 300, "illumination": 100},
      "iv": {"start": 0, "stop": 1.6, "step": 0.02}}

def op(path):
    txt = open(path, errors="ignore").read()
    d = {}
    for kk, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"), ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                    ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"), ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt); d[kk] = float(m.group(1)) if m else None
    return {"deduced": d, "error": None if d["eta"] else "no-eta"}

IN, META = {}, {}
for t in range(r):
    pts, seq = traj()
    prev = None
    for s, u in enumerate(pts):
        sid = f"M{t:02d}s{s}"
        sv = scale(u)
        IN[sid] = dict(CH, set={"layer2.thickness": round(sv["thickness"], 3),
                                "layer2.NA": sv["NA"], "layer2.defect1.Ntotal": sv["Nt"],
                                "layer3.ND": sv["ND"], "layer2.Eg": round(sv["Eg"], 4),
                                "layer2.chi": round(sv["chi"], 4),
                                "interface1.IFdefect1.Ntotal": sv["Nif"],
                                "interface2.IFdefect1.Ntotal": sv["Nif"]})
        META[sid] = {"traj": t, "u": u.tolist(), "scaled": sv}

runner = SCAPSrunner(lambda q: from_param_dict(q), op, ncores=4)
runner.sync_parameters()
out = runner.run_inputs(IN)
rows = []
for sid, v in out.items():
    m = META[sid]; m.update({"deduced": v["deduced"], "error": v["error"]})
    rows.append(m)
jsonl = BASE / "outputs" / "s5_morris.jsonl"
jsonl.write_text("\n".join(json.dumps(x) for x in rows))

# elementary effects on eta
byT = {}
for m in rows:
    byT.setdefault(m["traj"], []).append(m)
EE = {n: [] for n in NAMES}
for t, ms in byT.items():
    ms = sorted(ms, key=lambda m: 0)  # insertion order preserved in dict? re-sort by run seq
    # recover order: s index from scaled? use file order via u sequence is lost; recompute: order by matching trajectory gen is unavailable -> use eta diffs along stored seq? Instead store order: regenerate not possible. Use index in rows list.
    pass
# simpler: rebuild order from jsonl sequence is run order, not traj order. Recompute EE by pairing consecutive same-traj points via u-difference:
for t, ms in byT.items():
    for a in ms:
        for b in ms:
            if a is b: continue
            ua, ub = np.array(a["u"]), np.array(b["u"])
            d = np.round(ub - ua, 6)
            nz = np.nonzero(np.abs(d) > 1e-9)[0]
            if len(nz) == 1 and abs(abs(d[nz[0]]) - DELTA) < 1e-6 \
               and a["deduced"]["eta"] and b["deduced"]["eta"]:
                EE[NAMES[nz[0]]].append((b["deduced"]["eta"] - a["deduced"]["eta"]) / d[nz[0]])
summ = {n: {"mu_star": float(np.mean(np.abs(v))), "sigma": float(np.std(v)), "n": len(v)}
        for n, v in EE.items()}
print(json.dumps(summ, indent=1))
open(BASE / "outputs" / "s5_morris_summary.json", "w").write(json.dumps(
    {"bounds": BOUNDS, "p": p, "r": r, "delta": DELTA, "seed": 7, "summary": summ}, indent=1))
