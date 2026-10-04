"""Normalize char.jsonl schema to {id, kind, data:{table}} + ingest qq/re files. No sims."""
import json, glob, os, pathlib
import numpy as np

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
JSONL = BASE / "outputs" / "char.jsonl"

def read_table(path, marker, ncols):
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
        if len(vals) < ncols:
            continue
        out.append(vals[:ncols])
    a = np.array(out, dtype=float)
    return a

def newest(pat):
    hits = glob.glob(f"/home/touhid/.scaps-runner/proc*/drive_c/Program Files (x86)/Scaps3309/results/{pat}")
    hits.sort(key=os.path.getmtime, reverse=True)
    return hits[0] if hits else None

# ingest QE + champ EB from worker files
fresh = {}
f = newest("qq1.txt")
if f: fresh["qe_champ"] = ("qe", read_table(f, "lambda(nm)", 3), ["lambda", "QE", "E"])
f = newest("qq0.txt")
if f: fresh["qe_base"] = ("qe", read_table(f, "lambda(nm)", 3), ["lambda", "QE", "E"])
f = newest("re1.txt")
if f: fresh["eb0_champ"] = ("eb0", read_table(f, "x(um)", 22),
    ["i", "x_um", "y", "Ec", "Fn", "Fp", "Ev", "n", "p", "rho_def", "Ndop", "rho",
     "E", "jn", "jp", "jnt", "jpt", "jtot", "gen", "rec", "cumG", "cumR_LR"])

rows = {}
for l in JSONL.read_text().splitlines():
    if l.strip():
        r = json.loads(l)
        rows[r["id"]] = r
for jid, (kind, arr, cols) in fresh.items():
    rows[jid] = {"id": jid, "kind": kind,
                 "data": {"table": {c: arr[:, j].tolist() for j, c in enumerate(cols)}}}
# normalize any table-like data -> {data: {table}}
for r in rows.values():
    d = r.get("data", {})
    if "table" not in d:
        for k in list(d.keys()):
            if isinstance(d[k], dict):
                r["data"] = {"table": d[k]}
                break
        else:
            if d and all(isinstance(v, list) for v in d.values()):
                r["data"] = {"table": d}
with JSONL.open("w") as fo:
    for r in rows.values():
        fo.write(json.dumps(r) + "\n")
print("ids:", sorted(rows))
for jid in ["qe_champ", "qe_base", "cv_champ", "cv_base", "eb0_champ", "eb0_base"]:
    t = rows.get(jid, {}).get("data", {}).get("table")
    print(jid, "rows=", len(t[list(t.keys())[0]]) if t else None)
