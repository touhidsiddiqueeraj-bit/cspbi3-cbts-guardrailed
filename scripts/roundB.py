"""Round B: refine around A087 (th2.0/NA1e16/Nt1e12/ND9e17/Eg1.65 -> 23.47%).
Dims: thickness x Eg/chi x NA x Nt = 3x3x2x2 = 36 combos, one parallel run.
Resume-safe JSONL append. SET-UNITS: um, cm-3, eV."""
import sys, json, re, itertools, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner, parse_jv_curve
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
JSONL = BASE / "outputs" / "roundB.jsonl"
RCP = BASE / "receipts" / "receipt_roundB.json"

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
EGS = [(1.65, 3.928), (1.68, 3.943), (1.72, 3.963)]  # chi = 3.95+0.5*(Eg-1.694)
grid = list(itertools.product([1.8, 2.0, 2.2], [1e16, 3e16], [1e12, 3e12], EGS))
print("total:", len(grid))

done = set()
if JSONL.exists():
    for ln in JSONL.read_text().splitlines():
        if ln.strip():
            done.add(json.loads(ln)["id"])

def mk(i, th, na, nt, egchi):
    eg, chi = egchi
    return (f"B{i:03d}_th{th}_na{na:.0e}_nt{nt:.0e}_eg{eg}",
            {"load": LOAD,
             "set": {"layer2.thickness": th, "layer2.NA": na,
                     "layer2.defect1.Ntotal": nt, "layer3.ND": 9e17,
                     "layer2.Eg": eg, "layer2.chi": chi},
             "workingpoint": {"temperature": 300, "illumination": 100},
             "iv": {"start": 0, "stop": 1.6, "step": 0.02}})

jobs = [mk(i, th, na, nt, egchi) for i, (th, na, nt, egchi) in enumerate(grid)
        if f"B{i:03d}" not in {d.split('_')[0] for d in done}]
print("to run:", len(jobs))
r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
out = r.run_inputs(dict(jobs))
with JSONL.open("a") as f:
    for k, v in out.items():
        f.write(json.dumps({"id": k, "params": dict(jobs)[k].get("set"),
                            "deduced": v.get("deduced"), "npts": v.get("npts"),
                            "error": v.get("error")}) + "\n")
rows = [json.loads(ln) for ln in JSONL.read_text().splitlines() if ln.strip()]
rows = [x for x in rows if x.get("deduced") and x["deduced"].get("eta") is not None]
rows.sort(key=lambda x: -x["deduced"]["eta"])
print("=== TOP 10 Round B ===")
for x in rows[:10]:
    print(x["deduced"]["eta"], x["id"], x["deduced"])
RCP.write_text(json.dumps({"combos": len(rows), "top10": rows[:10]}, indent=1))
