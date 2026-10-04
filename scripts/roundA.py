"""Round A: SIMULTANEOUS 5-dim factorial (NOT one-at-a-time).
Dims: thickness x NA x Nt x ETL-ND x Eg/chi = 4x2x3x2x2 = 96 combos.
Executed in 4 persistent chunks of 24 (each chunk parallel on 4 workers).
Resume-safe: skips IDs already in results JSONL. No /tmp anywhere.
SET-UNITS (see UNITS.md): thickness um, doping/defect cm-3/cm-2, Eg/chi eV.
"""
import sys, json, re, itertools, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner, parse_jv_curve
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
JSONL = BASE / "outputs" / "roundA.jsonl"
RCP = BASE / "receipts" / "receipt_roundA.json"

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

def op(path):
    try:
        J, V = parse_jv_curve(path)
        return {"deduced": parse_deduced(path), "npts": len(V)}
    except Exception as e:
        return {"error": str(e)}

LOAD = "csPbI3-CBTS-r7.def"
EGS = [(1.694, 3.95), (1.65, 3.928)]  # chi = 3.95 + 0.5*(Eg-1.694)
grid = list(itertools.product(
    [1.0, 1.5, 1.8, 2.0],      # thickness um
    [1e15, 1e16],              # NA cm-3
    [1e12, 1e13, 1e14],        # Nt cm-3
    [9e16, 9e17],              # ETL ND cm-3
    EGS))
print("total combos:", len(grid))

done = set()
if JSONL.exists():
    for ln in JSONL.read_text().splitlines():
        if ln.strip():
            done.add(json.loads(ln)["id"])
print("already done:", len(done))

def entry(i, th, na, nt, nd, egchi):
    eg, chi = egchi
    return (f"A{i:03d}_th{th}_na{int(na):d}_nt{int(nt):d}_nd{int(nd):d}_eg{eg}",
            {"load": LOAD,
             "set": {"layer2.thickness": th, "layer2.NA": na,
                     "layer2.defect1.Ntotal": nt, "layer3.ND": nd,
                     "layer2.Eg": eg, "layer2.chi": chi},
             "workingpoint": {"temperature": 300, "illumination": 100},
             "iv": {"start": 0, "stop": 1.6, "step": 0.02}})

jobs = [entry(i, *g) for i, g in enumerate(grid) if f"A{i:03d}" not in
        {d.split("_")[0] for d in done}]
# jobs keyed by full id
jobs = [(f"A{i:03d}_th{th}_na{int(na):d}_nt{int(nt):d}_nd{int(nd):d}_eg{eg}",
         {"load": LOAD,
          "set": {"layer2.thickness": th, "layer2.NA": na,
                  "layer2.defect1.Ntotal": nt, "layer3.ND": nd,
                  "layer2.Eg": eg, "layer2.chi": chi},
          "workingpoint": {"temperature": 300, "illumination": 100},
          "iv": {"start": 0, "stop": 1.6, "step": 0.02}})
        for i, (th, na, nt, nd, (eg, chi)) in enumerate(grid)
        if f"A{i:03d}" not in {d.split('_')[0] for d in done}]
print("to run:", len(jobs))

r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
CH = 24
for c in range(0, len(jobs), CH):
    chunk = dict(jobs[c:c+CH])
    print(f"--- chunk {c//CH+1}/{(len(jobs)+CH-1)//CH} ({len(chunk)} sims) ---", flush=True)
    out = r.run_inputs(chunk)
    with JSONL.open("a") as f:
        for k, v in out.items():
            f.write(json.dumps({"id": k, "params": chunk[k].get("set"),
                                "deduced": v.get("deduced"), "npts": v.get("npts"),
                                "error": v.get("error")}) + "\n")

# leaderboard
rows = [json.loads(ln) for ln in JSONL.read_text().splitlines() if ln.strip()]
rows = [x for x in rows if x.get("deduced") and x["deduced"].get("eta") is not None]
rows.sort(key=lambda x: -x["deduced"]["eta"])
print("=== TOP 10 ===")
for x in rows[:10]:
    print(x["deduced"]["eta"], x["id"], x["deduced"])
RCP.write_text(json.dumps({"combos": len(rows), "top10": rows[:10],
    "note": "Rs=0 upper bounds; FF-derate x0.965 for Rs~1. Strict floors: Nt>=1e12, NA<=1e17."}, indent=1))
