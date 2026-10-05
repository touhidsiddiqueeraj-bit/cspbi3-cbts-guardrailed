"""R2 stage 1: joint chi_CBTS x chi_TiO2 search + contact (ITO/Ni) probes.

Champion geometry, step 0.02, 4 workers. Contacts changed via def copies
(proven route in s0/s1; the script `set contact.workfunction` key exists in
scriptdescription3310.txt but is untested in this harness).

Grid A: chi_CBTS {3.50..3.90} x chi_TiO2 {3.7,3.8,3.9,4.0} at ITO 4.0/Ni 5.5
Grid B: ITO {4.2,4.4,4.6,4.8} at affinity pairs (3.6,4.0), (3.8,4.0), (3.8,3.8)
Grid C: Ni {5.0,5.2} at (3.6,4.0) and (3.8,3.8)

Writes outputs/s11_joint_chi.json.
"""
import sys, json, re, shutil, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
BASEDEF = BASE / "defs" / "csPbI3-CBTS-r7.def"
SCADIR = pathlib.Path("/home/touhid/.scaps-runner/scaps_dat/def")

BACK = "Fi_m :   5.5000 [eV]"
FRONT = "Fi_m :  4.00 [eV]"


def wf_variant(name, back=None, front=None):
    t = BASEDEF.read_text()
    if back is not None:
        assert BACK in t
        t = t.replace(BACK, f"Fi_m :   {back:.4f} [eV]")
    if front is not None:
        assert FRONT in t
        t = t.replace(FRONT, f"Fi_m :  {front:.2f} [eV]")
    p = BASE / "defs" / name
    p.write_text(t)
    shutil.copy(p, SCADIR / name)
    return name


CH = {"load": "csPbI3-CBTS-r7.def",
      "set": {"layer2.thickness": 2.2, "layer2.NA": 3e16,
              "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
              "layer2.Eg": 1.65, "layer2.chi": 3.928},
      "workingpoint": {"temperature": 300, "illumination": 100},
      "iv": {"start": 0, "stop": 1.6, "step": 0.02}}


def S(extra, **kw):
    d = dict(CH, set=dict(CH["set"], **extra))
    d.update(kw)
    return d


IN = {}
# --- Grid A: joint affinities (ITO 4.0 / Ni 5.5) ---
for chih in [3.50, 3.55, 3.60, 3.65, 3.70, 3.75, 3.80, 3.85, 3.90]:
    for chie in [3.7, 3.8, 3.9, 4.0]:
        IN[f"A_ch{chih:.2f}_ce{chie:.1f}"] = S({"layer1.chi": chih, "layer3.chi": chie})

# --- Grid B: ITO sweep at three affinity pairs ---
for chih, chie in [(3.6, 4.0), (3.8, 4.0), (3.8, 3.8)]:
    for ito in [4.2, 4.4, 4.6, 4.8]:
        nm = wf_variant(f"csPbI3-CBTS-ito{ito:.1f}.def", front=ito)
        IN[f"B_ch{chih:.1f}_ce{chie:.1f}_ito{ito:.1f}"] = S(
            {"layer1.chi": chih, "layer3.chi": chie}, load=nm)

# --- Grid C: Ni sweep at two affinity pairs ---
for chih, chie, ni in [(3.6, 4.0, 5.0), (3.6, 4.0, 5.2), (3.8, 3.8, 5.0), (3.8, 3.8, 5.2)]:
    nm = wf_variant(f"csPbI3-CBTS-ni{ni:.1f}.def", back=ni)
    IN[f"C_ch{chih:.1f}_ce{chie:.1f}_ni{ni:.1f}"] = S(
        {"layer1.chi": chih, "layer3.chi": chie}, load=nm)


def op(path):
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


r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
r.sync_parameters()

JSONL = BASE / "outputs" / "s11_joint_chi.jsonl"
done = set()
if JSONL.exists():
    for ln in JSONL.read_text().splitlines():
        if ln.strip():
            done.add(json.loads(ln)["id"])

jobs = [(k, v) for k, v in IN.items() if k not in done]
print("to run:", len(jobs), "already:", len(done), flush=True)
CHUNK = 24
for c in range(0, len(jobs), CHUNK):
    chunk = dict(jobs[c:c + CHUNK])
    print(f"--- chunk {c // CHUNK + 1} ({len(chunk)} sims) ---", flush=True)
    out = r.run_inputs(chunk)
    with JSONL.open("a") as f:
        for k, v in out.items():
            f.write(json.dumps({"id": k, "d": v["d"], "e": v["e"],
                                "set": chunk[k]["set"], "load": chunk[k]["load"]}) + "\n")

rows = [json.loads(ln) for ln in JSONL.read_text().splitlines() if ln.strip()]
res = {x["id"]: x for x in rows}
open(BASE / "outputs" / "s11_joint_chi.json", "w").write(json.dumps(res, indent=1))
ok = {k: round(x["d"]["eta"], 4) for k, x in res.items()
      if x["d"] and x["d"].get("eta")}
fails = {k: x["e"] for k, x in res.items() if not (x["d"] and x["d"].get("eta"))}
print("runs", len(res), "ok", len(ok), "failed", fails)
print(json.dumps(dict(sorted(ok.items(), key=lambda kv: -kv[1])[:20]), indent=1))

