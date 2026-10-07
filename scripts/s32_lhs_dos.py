"""S29: prior-predictive UQ (frozen priors in priors.md, seed 13).

N = 96 LHS over 8 factors + 8-run Cr=0 sensitivity (seed 14).
Def variants for (ITO, Ni) combos created from r7 (Fi_m replaces).
Per-run screens (Voc <= 1.418 at Eg 1.70, Green FF) applied in ANALYSIS,
not as exclusion: outputs/s32_analysis.json reports flagged count.
Writes outputs/s32_lhs_dos.jsonl (checkpointed per chunk like s16).
"""
import sys, json, shutil, pathlib
import numpy as np
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scipy.stats import qmc
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
BASEDEF = BASE / "defs" / "csPbI3-CBTS-r7.def"
SCADIR = pathlib.Path("/home/touhid/.scaps-runner/scaps_dat/def")
FIXED = {"layer2.NA": 3e16, "layer3.ND": 9e17, "layer2.Eg": 1.70,
         "layer2.chi": 3.953}
WP = {"workingpoint": {"temperature": 300, "illumination": 100}}
IV = {"start": 0, "stop": 1.6, "step": 0.02}
ITO_DEFS = {4.0: "csPbI3-CBTS-r7.def", 4.2: "csPbI3-CBTS-wfITO42.def",
            4.4: "csPbI3-CBTS-wfITO44.def"}


def ni_variant(ito_def, ni):
    if ni == 5.5:
        return ito_def
    name = f"csPbI3-CBTS-ito{ito_def.split('wfITO')[1][:2] if 'wfITO' in ito_def else '40'}-ni{int(ni * 10)}.def" \
        if ito_def != "csPbI3-CBTS-r7.def" else f"csPbI3-CBTS-wfNi{int(ni * 10)}.def"
    p = BASE / "defs" / name
    if not p.exists():
        src = ito_def if ito_def != "csPbI3-CBTS-r7.def" else "csPbI3-CBTS-r7.def"
        t = (BASE / "defs" / src).read_text() if (BASE / "defs" / src).exists() else BASEDEF.read_text()
        if ito_def == "csPbI3-CBTS-wfITO42.def":
            t = BASEDEF.read_text().replace("Fi_m :  4.00 [eV]", "Fi_m :  4.20 [eV]")
        elif ito_def == "csPbI3-CBTS-wfITO44.def":
            t = BASEDEF.read_text().replace("Fi_m :  4.00 [eV]", "Fi_m :  4.40 [eV]")
        assert "Fi_m :   5.5000 [eV]" in t
        t = t.replace("Fi_m :   5.5000 [eV]", f"Fi_m :   {ni:.4f} [eV]")
        p.write_text(t)
        shutil.copy(p, SCADIR / name)
    return name


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


def sample_row(u, cr_fixed=None):
    logNt = 13 + u[0] * 3
    logNif = 10 + u[1] * 3
    logCr = -11 + u[2] * 2
    mu = 25 * (0.2 + u[3] * 0.8)
    rs = 0.5 + u[4] * 2.5
    ito = [4.0, 4.2, 4.4][min(int(u[5] * 3), 2)]
    ni = [5.0, 5.2, 5.5][min(int(u[6] * 3), 2)]
    d = 0.4 + u[7] * 1.1
    logNv = 18.6 + u[8] * 1.3
    cr = 0.0 if cr_fixed == 0 else 10 ** logCr
    sets = dict(FIXED, **{"layer2.thickness": round(d, 3),
                          "layer2.defect1.Ntotal": 10 ** logNt,
                          "interface1.IFdefect1.Ntotal": 10 ** logNif,
                          "interface2.IFdefect1.Ntotal": 10 ** logNif,
                          "layer2.radiative": cr,
                          "layer2.mun": round(mu, 2), "layer2.mup": round(mu, 2),
                          "layer2.Nv": 10 ** logNv,
                          "external.Rs": round(rs, 3)})
    meta = {"logNt": round(logNt, 3), "logNif": round(logNif, 3),
            "Cr": cr, "mu": round(mu, 2), "Rs": round(rs, 3),
            "ITO": ito, "Ni": ni, "d": round(d, 3), "logNv": round(logNv, 3)}
    return sets, meta, ni_variant(ITO_DEFS[ito], ni)


def main():
    IN, META = {}, {}
    eng = qmc.LatinHypercube(d=9, seed=13)
    for i, u in enumerate(eng.random(96)):
        sets, meta, load = sample_row(u)
        sid = f"Q{i:03d}"
        IN[sid] = dict({"load": load}, set=sets, **WP, iv=dict(IV))
        META[sid] = meta
    eng2 = qmc.LatinHypercube(d=9, seed=14)
    for i, u in enumerate(eng2.random(8)):
        sets, meta, load = sample_row(u, cr_fixed=0)
        sid = f"Q0_{i}"
        IN[sid] = dict({"load": load}, set=sets, **WP, iv=dict(IV))
        META[sid] = dict(meta, sensitivity_Cr0=True)
    JSONL = BASE / "outputs" / "s32_lhs_dos.jsonl"
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
                rec = {"id": k, "d": v["d"], "e": v["e"],
                       "set": IN[k]["set"], "meta": META[k]}
                f.write(json.dumps(rec) + "\n")
                print(k, v["d"], v["e"], flush=True)
    print("s32 done")


if __name__ == "__main__":
    main()
