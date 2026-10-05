"""S16: affinity-peak extension + new-base characterization.

Grid D: chiCBTS {3.95,4.00,4.05,4.10} x chiTiO2 {3.6,3.7,3.8} (peak hunt).
New base = (3.9,3.7): Eg derate {1.68,1.70,1.72}, Rs {0.5,1,2}, Rs1+Rsh4.
Retry 3 failed Ni runs from s11.
All guardrailed (def-default Nif=1e10). Writes outputs/s16.jsonl/.json.
"""
import sys, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
GEO = {"layer2.thickness": 2.2, "layer2.NA": 3e16,
       "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
       "layer2.Eg": 1.65, "layer2.chi": 3.928}
WP = {"workingpoint": {"temperature": 300, "illumination": 100},
      "iv": {"start": 0, "stop": 1.6, "step": 0.02}}
NEW = dict(GEO, **{"layer1.chi": 3.9, "layer3.chi": 3.7})


def S(extra, load="csPbI3-CBTS-r7.def"):
    return dict({"load": load}, set=dict(extra), **WP)


IN = {}
for chih in [3.95, 4.00, 4.05, 4.10]:
    for chie in [3.6, 3.7, 3.8]:
        g = dict(GEO, **{"layer1.chi": chih, "layer3.chi": chie})
        IN[f"D_ch{chih:.2f}_ce{chie:.1f}"] = S(g)
for eg in [1.68, 1.70, 1.72]:
    g = dict(NEW, **{"layer2.Eg": eg,
                     "layer2.chi": round(3.95 + 0.5 * (eg - 1.694), 4)})
    IN[f"N_eg{eg:.2f}"] = S(g)
IN["N_rs05"] = S(dict(NEW, **{"external.Rs": 0.5}))
IN["N_rs1"] = S(dict(NEW, **{"external.Rs": 1}))
IN["N_rs2"] = S(dict(NEW, **{"external.Rs": 2}))
IN["N_rs1rsh4"] = S(dict(NEW, **{"external.Rs": 1, "external.Rsh": 1e4}))
# Ni retries (def variants already in defs/ + scadir from s11)
IN["C_ch3.6_ce4.0_ni5.0"] = S({"layer1.chi": 3.6, "layer3.chi": 4.0},
                              load="csPbI3-CBTS-ni5.0.def")
IN["C_ch3.8_ce3.8_ni5.0"] = S({"layer1.chi": 3.8, "layer3.chi": 3.8},
                              load="csPbI3-CBTS-ni5.0.def")
IN["C_ch3.8_ce3.8_ni5.2"] = S({"layer1.chi": 3.8, "layer3.chi": 3.8},
                              load="csPbI3-CBTS-ni5.2.def")


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


JSONL = BASE / "outputs" / "s16.jsonl"
done = set()
if JSONL.exists():
    for ln in JSONL.read_text().splitlines():
        if ln.strip():
            done.add(json.loads(ln)["id"])
jobs = {k: v for k, v in IN.items() if k not in done}
print("to run:", len(jobs), "already:", len(done), flush=True)
r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()
CHUNK = 12
items = list(jobs.items())
for c in range(0, len(items), CHUNK):
    chunk = dict(items[c:c + CHUNK])
    print(f"--- chunk {c // CHUNK + 1} ---", flush=True)
    out = r.run_inputs(chunk)
    with JSONL.open("a") as f:
        for k, v in out.items():
            f.write(json.dumps({"id": k, "d": v["d"], "e": v["e"],
                                "set": chunk[k]["set"],
                                "load": chunk[k]["load"]}) + "\n")
rows = [json.loads(ln) for ln in JSONL.read_text().splitlines() if ln.strip()]
res = {x["id"]: x for x in rows}
json.dump(res, open(BASE / "outputs" / "s16.json", "w"), indent=1)
ok = {k: round(x["d"]["eta"], 4) for k, x in res.items()
      if x["d"] and x["d"].get("eta")}
print("runs", len(res), "ok", len(ok))
print(json.dumps(dict(sorted(ok.items(), key=lambda kv: -kv[1])[:14]), indent=1))
print("failed:", [k for k in res if not (res[k]["d"] and res[k]["d"].get("eta"))])
