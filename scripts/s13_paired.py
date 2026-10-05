"""S13-analysis: paired Morris bootstrap, tau/S table, gap-step audit, 22.51 check.

No SCAPS calls. Writes outputs/s13_analysis.json.
"""
import json, pathlib
import numpy as np

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
OUT = {}
rng = np.random.default_rng(7)
p, r, k = 4, 8, 6
DELTA = p / (2 * (p - 1))
NAMES = ["d", "logNA", "logNt", "logND", "Eg", "logNif"]

# --- reconstruct Morris trajectories (same code/order as s5_morris.py) ---
seqs = []
for t in range(r):
    x0 = rng.integers(0, p, size=k) / (p - 1)
    order = rng.permutation(k)
    signs = rng.choice([-1.0, 1.0], size=k)
    x = x0.copy(); seq = []
    for j in order:
        step = signs[j] * DELTA
        if not (0 <= x[j] + step <= 1):
            step = -step
        x = x.copy(); x[j] += step
        seq.append((int(j), float(step)))
    seqs.append(seq)

rows = [json.loads(l) for l in open(BASE / "outputs" / "s5_morris.jsonl")]
by_traj = {}
for x in rows:
    by_traj.setdefault(x["traj"], {})[tuple(x["u"]).__hash__] = x
# order points within traj by matching u to regenerated path
traj_pts = []
for t in range(r):
    x0 = None
    # regenerate path points
    rr = np.random.default_rng(7)
    paths = []
    for tt in range(r):
        a = rr.integers(0, p, size=k) / (p - 1)
        o = rr.permutation(k); s = rr.choice([-1.0, 1.0], size=k)
        xx = a.copy(); pts = [xx.copy()]
        for j in o:
            st = s[j] * DELTA
            if not (0 <= xx[j] + st <= 1):
                st = -st
            xx = xx.copy(); xx[j] += st
            pts.append(xx.copy())
        paths.append(pts)
    traj_pts = paths
    break

fx = {n: [] for n in NAMES}   # per-factor elementary effects across trajs
pair_diff = []                # |EE_Nif| - |EE_Nt| per traj
for t in range(r):
    pts = traj_pts[t]
    etas = []
    for u in pts:
        match = None
        for x in rows:
            if x["traj"] == t and np.allclose(x["u"], u):
                match = x
                break
        assert match is not None, (t, u)
        etas.append(match["deduced"]["eta"])
    for s, (j, step) in enumerate(seqs[t]):
        ee = (etas[s + 1] - etas[s]) / step  # per normalized unit
        fx[NAMES[j]].append(ee)
    # paired: Nif traj effect vs Nt traj effect (each traj has exactly one of each)
    dnif = [((etas[s + 1] - etas[s]) / st) for s, (j, st) in enumerate(seqs[t]) if NAMES[j] == "logNif"][0]
    dnt = [((etas[s + 1] - etas[s]) / st) for s, (j, st) in enumerate(seqs[t]) if NAMES[j] == "logNt"][0]
    pair_diff.append(abs(dnif) - abs(dnt))

pair_diff = np.array(pair_diff)
B = 20000
bs = rng.normal(0, 1, (B, r))  # placeholder
means = np.array([np.mean(rng.choice(pair_diff, r, replace=True)) for _ in range(B)])
OUT["paired_Nif_minus_Nt"] = {
    "mean": round(float(np.mean(pair_diff)), 3),
    "ci95": [round(float(np.quantile(means, 0.025)), 3),
             round(float(np.quantile(means, 0.975)), 3)],
    "frac_positive": round(float(np.mean(pair_diff > 0)), 3),
    "n": r}
# per-factor mu* check
OUT["mustar_check"] = {n: round(float(np.mean(np.abs(fx[n]))), 3) for n in NAMES}

# --- tau / S table ---
vth = 1e7  # cm/s (1e5 m/s)
sig = 1e-15  # cm^2 (1e-19 m^2)
def tau(Nt):
    return 1 / (sig * vth * Nt)
def Svel(Nif):
    return sig * vth * Nif
OUT["tau_S"] = {
    "bulk_tau_us": {f"Nt=1e{e}": round(tau(10**e) * 1e6, 3) for e in [12, 13, 14, 15]},
    "interface_S_cms": {f"Nif=1e{e}": round(Svel(10**e), 3) for e in [8, 9, 10, 11, 12]}}

# --- gap-step audit: Eg+chi confounding ---
s10 = json.load(open(BASE / "outputs" / "s10_r4.json"))
OUT["s10_keys"] = {k: (v["d"]["eta"] if v.get("d") else None) for k, v in s10.items()}
rb = [json.loads(l) for l in open(BASE / "outputs" / "roundB.jsonl")]
egpts = [(x.get("set", {}).get("layer2.Eg"), (x.get("d") or x.get("deduced") or {}).get("eta")) for x in rb]
OUT["roundB_Eg_eta"] = sorted([(e, eta) for e, eta in egpts if e],
                              key=lambda t: t[0])[:40]

json.dump(OUT, open(BASE / "outputs" / "s13_analysis.json", "w"), indent=1)
print(json.dumps({k: v for k, v in OUT.items() if k != "roundB_Eg_eta"}, indent=1))
print("roundB points:", len(OUT["roundB_Eg_eta"]))
