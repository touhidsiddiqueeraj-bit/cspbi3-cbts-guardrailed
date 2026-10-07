"""S30: Cr x affinity map. Joint chi-grid (9 x 4, s11 geometry) at
Cr = 1e-10 and 1e-11 (72 runs) + chiTiO2 3.5/3.6 extension columns at
chiCBTS {3.7, 3.8, 3.9} x Cr {0, 1e-10} (12 runs) + routine-Nt subgrid
(chiCBTS {3.7, 3.8, 3.9} x chiTiO2 {3.7, 3.8}, Nt 1e15, Cr 0; 6 runs).
Champion geometry otherwise (NEW). Writes outputs/s30_crchi.jsonl.
"""
import sys, json, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
GEO = {"layer2.thickness": 2.2, "layer2.NA": 3e16,
       "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
       "layer2.Eg": 1.65, "layer2.chi": 3.928}
WP = {"workingpoint": {"temperature": 300, "illumination": 100}}
IV = {"start": 0, "stop": 1.6, "step": 0.02}


def S(extra, load="csPbI3-CBTS-r7.def"):
    return dict({"load": load}, set=dict(extra), **WP, iv=dict(IV))


def op(path):
    import re
    txt = open(path, errors="ignore").read()
    d = {}
    for k, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"),
                   ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                   ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"),
                   ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt)
        d[k] = float(m.group(1)) if m else None
    return {"d": d, "e": None if d["eta"] else "no-eta"}


def main():
    IN = {}
    for cr, tag in [(1e-10, "cr10"), (1e-11, "cr11")]:
        for chih in [3.50, 3.55, 3.60, 3.65, 3.70, 3.75, 3.80, 3.85, 3.90]:
            for chie in [3.7, 3.8, 3.9, 4.0]:
                g = dict(GEO, **{"layer1.chi": chih, "layer3.chi": chie,
                                 "layer2.radiative": cr})
                IN[f"M_{tag}_ch{chih:.2f}_ce{chie:.1f}"] = S(g)
    for cr, tag in [(0, "cr0"), (1e-10, "cr10")]:
        for chih in [3.70, 3.80, 3.90]:
            for chie in [3.5, 3.6]:
                g = dict(GEO, **{"layer1.chi": chih, "layer3.chi": chie})
                if cr:
                    g["layer2.radiative"] = cr
                IN[f"X_{tag}_ch{chih:.2f}_ce{chie:.1f}"] = S(g)
    for chih in [3.70, 3.80, 3.90]:
        for chie in [3.7, 3.8]:
            g = dict(GEO, **{"layer1.chi": chih, "layer3.chi": chie,
                             "layer2.defect1.Ntotal": 1e15})
            IN[f"R_ch{chih:.2f}_ce{chie:.1f}"] = S(g)
    JSONL = BASE / "outputs" / "s30_crchi.jsonl"
    done = set()
    if JSONL.exists():
        for ln in JSONL.read_text().splitlines():
            if ln.strip():
                done.add(json.loads(ln)["id"])
    jobs = {k: v for k, v in IN.items() if k not in done}
    print("to run:", len(jobs), "already:", len(done), flush=True)
    r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
    r.sync_parameters()
    items = list(jobs.items())
    with JSONL.open("a") as f:
        for c in range(0, len(items), 12):
            chunk = dict(items[c:c + 12])
            print(f"--- chunk {c // 12 + 1} ---", flush=True)
            out = r.run_inputs(chunk)
            for k, v in out.items():
                f.write(json.dumps({"id": k, "d": v["d"], "e": v["e"],
                                    "set": IN[k]["set"]}) + "\n")
                print(k, v["d"], v["e"], flush=True)
    print("s30 done")


if __name__ == "__main__":
    main()
