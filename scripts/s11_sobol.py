"""Sobol-on-surrogate corroboration: RF trained on all standard-base runs, Saltelli indices."""
import json, pathlib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
FEATS = ["d", "logNA", "logNt", "logND", "Eg", "logNif"]
BOUNDS = {"d": (0.4, 2.2), "logNA": (15, 16.5), "logNt": (12, 15),
          "logND": (16, 19), "Eg": (1.65, 1.75), "logNif": (8, 12)}


def row_of(p, eta, tag):
    return {"x": [p["layer2.thickness"], np.log10(p["layer2.NA"]),
                  np.log10(p["layer2.defect1.Ntotal"]), np.log10(p["layer3.ND"]),
                  p["layer2.Eg"],
                  np.log10(p.get("Nif", 1e10))], "y": eta, "tag": tag}


rows = []
for fn in ["outputs/roundA.jsonl", "outputs/roundB.jsonl"]:
    for line in open(BASE / fn):
        r = json.loads(line)
        if r.get("error") or not r.get("deduced", {}).get("eta"):
            continue
        rows.append(row_of({**r["params"], "Nif": 1e10}, r["deduced"]["eta"], fn))
for line in open(BASE / "outputs/s5_morris.jsonl"):
    m = json.loads(line)
    if m.get("error") or not m.get("deduced", {}).get("eta"):
        continue
    s = m["scaled"]
    rows.append({"x": [s["thickness"], np.log10(s["NA"]), np.log10(s["Nt"]),
                       np.log10(s["ND"]), s["Eg"], np.log10(s["Nif"])],
                 "y": m["deduced"]["eta"], "tag": "morris"})
# interface-dose rows at standard base (exclude sigma/WF/Rs variants)
dose_spec = [("s1_dose.json", ["if1e8", "if3e9", "if3e10", "if1e12",
                              "ifETL1e12", "ifHTL1e12"], 2.2, 3e16, 1e12, 9e17, 1.65),
             ("s0_verify.json", ["ifN1e9"], 2.2, 3e16, 1e12, 9e17, 1.65),
             ("s4_sig.json", ["if1e11"], 2.2, 3e16, 1e12, 9e17, 1.65)]
for fn, keys, d, na, nt, nd, eg in dose_spec:
    j = json.load(open(BASE / "outputs" / fn))
    niv = {"if1e8": 8, "if3e9": 9.48, "ifN1e9": 9, "if3e10": 10.48,
           "if1e11": 11, "if1e12": 12, "ifETL1e12": 12, "ifHTL1e12": 12}
    for k in keys:
        if j[k]["e"] or not j[k]["d"]["eta"]:
            continue
        rows.append({"x": [d, np.log10(na), np.log10(nt), np.log10(nd), eg, niv[k]],
                     "y": j[k]["d"]["eta"], "tag": fn + ":" + k})
X = np.array([r["x"] for r in rows])
y = np.array([r["y"] for r in rows])
print("n =", len(X), "eta range", round(y.min(), 2), round(y.max(), 2))
rf = RandomForestRegressor(n_estimators=500, random_state=0, n_jobs=-1,
                           oob_score=True)
rf.fit(X, y)
print("OOB R2 =", round(rf.oob_score_, 4))

rng = np.random.default_rng(11)
N, k = 4096, 6
A = np.column_stack([rng.uniform(*BOUNDS[n], N) for n in FEATS])
B = np.column_stack([rng.uniform(*BOUNDS[n], N) for n in FEATS])
fA, fB = rf.predict(A), rf.predict(B)
f0sq = (np.concatenate([fA, fB]).mean()) ** 2
V = np.concatenate([fA, fB]).var()
S1, ST = {}, {}
for i in range(k):
    C = A.copy()
    C[:, i] = B[:, i]
    fC = rf.predict(C)
    S1[FEATS[i]] = float(np.mean(fB * (fC - fA)) / V)
    ST[FEATS[i]] = float(np.mean((fA - fC) ** 2) / 2 / V)
print(json.dumps({"S1": {kk: round(vv, 3) for kk, vv in S1.items()},
                  "ST": {kk: round(vv, 3) for kk, vv in ST.items()}}, indent=1))
json.dump({"n_train": len(X), "oob_R2": float(rf.oob_score_), "S1": S1, "ST": ST,
           "note": "RF surrogate on pooled standard-base runs; Saltelli N=4096"},
          open(BASE / "outputs" / "sobol_surrogate.json", "w"), indent=1)
