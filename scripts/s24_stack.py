"""S24: stacked realistic variants + joint-base char regen + real baseline JV.

STACK (surveyed affinities, r7 def unless noted): NA 3e16, ND 9e17,
Eg 1.70/chi 3.953 (chi-link), Nt 1e15, Cr 1e-10, Rs 1, mu 10/5,
ITO 4.4 via wfITO44 def, d in {0.6, 0.8, 1.0} + d1.0/Rs2.
JOINT CHAR: qe/cv/eb custom scripts with full NEW (chi 3.9/3.7) sets.
BASE JV: real baseline IV curve (replaces hand-drawn Fig.2 baseline).
Merges into outputs/s24_stack.json; curves to outputs/baseline_JV.json.
"""
import sys, json, os, re, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
import numpy as np
from scaps_runner import SCAPSrunner, parse_jv_curve
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
NEW = {"layer2.thickness": 2.2, "layer2.NA": 3e16,
       "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
       "layer2.Eg": 1.65, "layer2.chi": 3.928,
       "layer1.chi": 3.9, "layer3.chi": 3.7}
WP = {"workingpoint": {"temperature": 300, "illumination": 100}}
IV = {"start": 0, "stop": 1.6, "step": 0.02}
STACK = {"layer2.NA": 3e16, "layer3.ND": 9e17, "layer2.Eg": 1.70,
         "layer2.chi": 3.953, "layer2.defect1.Ntotal": 1e15,
         "layer2.radiative": 1e-10, "external.Rs": 1,
         "layer2.mun": 10, "layer2.mup": 5}


def S(extra, load="csPbI3-CBTS-r7.def"):
    return dict({"load": load}, set=dict(extra), **WP, iv=dict(IV))


def op(path):
    txt = open(path, errors="ignore").read()
    d = {}
    for k, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"),
                   ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                   ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"),
                   ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt)
        d[k] = float(m.group(1)) if m else None
    return {"d": d, "e": None if d["eta"] else "no-eta"}


IN = {
    "ST_d06": S(dict(STACK, **{"layer2.thickness": 0.6}), load="csPbI3-CBTS-wfITO44.def"),
    "ST_d08": S(dict(STACK, **{"layer2.thickness": 0.8}), load="csPbI3-CBTS-wfITO44.def"),
    "ST_d10": S(dict(STACK, **{"layer2.thickness": 1.0}), load="csPbI3-CBTS-wfITO44.def"),
    "ST_d10_rs2": S(dict(STACK, **{"layer2.thickness": 1.0, "external.Rs": 2}),
                     load="csPbI3-CBTS-wfITO44.def"),
    "JBASE_JV": S(dict(NEW)),
}

# custom char scripts (qe/cv/eb at joint base), after characterize.build
def cbuild(kind, sets):
    c = ["clear actions", "load definitionfile csPbI3-CBTS-r7.def"]
    for k, v in sets.items():
        c.append(f"set {k} {v}")
    c += ["action workingpoint.temperature 300", "action intensity.T 100", "action light"]
    if kind == "qe":
        c += ["action qe.startlambda 300", "action qe.stoplambda 850",
              "action qe.points 56", "action qe.doqe",
              "action iv.startv 0", "action iv.stopv 1.6", "action iv.increment 0.05",
              "action iv.doiv", "calculate singleshot", "save results.qe save_qe.txt"]
    elif kind == "cv":
        c += ["action workingpoint.frequency 1000000",
              "action cv.startV 0", "action cv.stopV 1.0", "action cv.points 21",
              "action cv.docv", "calculate singleshot", "save results.cv save_cv.txt"]
    elif kind == "eb0":
        c += ["action workingpoint.voltage 0", "calculate singleshot",
              "save results.eb save_eb.txt"]
    return "set quitscript.quitSCAPS\nset errorhandling.overwritefile\n" + "\n".join(c) + "\n"


def read_table(path, marker, cols):
    import numpy as np
    lines = open(path, errors="ignore").readlines()
    si = next(i for i, l in enumerate(lines) if l.strip().startswith(marker))
    out = []
    for l in lines[si + 1:]:
        s = l.strip()
        if not s:
            break
        try:
            vals = [float(x) for x in s.split()]
        except ValueError:
            break
        if len(vals) < len(cols):
            continue
        out.append(vals[:len(cols)])
    a = np.array(out)
    return {c: a[:, j].tolist() for j, c in enumerate(cols)}


def cop(result_file):
    import os
    rdir = os.path.dirname(result_file)
    out = dict(op(None) if False else {})
    txt = open(result_file, errors="ignore").read()
    d = {}
    for k, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"),
                   ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                   ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"),
                   ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt)
        d[k] = float(m.group(1)) if m else None
    out["deduced"] = d
    for name, marker, cols in [
            ("save_qe.txt", "lambda(nm)", ["lambda", "QE", "E"]),
            ("save_cv.txt", "v(V)", ["V", "C", "G", "W", "Napp", "jtot", "jbulk", "jifr"]),
            ("save_eb.txt", "i", ["i", "x_um", "y", "Ec", "Fn", "Fp", "Ev", "n", "p",
                                  "rho_def", "Ndop", "rho", "E", "jn", "jp", "jnt",
                                  "jpt", "jtot", "gen", "rec", "cumG", "cumR_LR"])]:
        p = os.path.join(rdir, name)
        if os.path.exists(p):
            try:
                out[name] = read_table(p, marker, cols)
            except Exception as e:
                out[name + "_error"] = str(e)[:200]
    out["error"] = None if d["eta"] else "no-eta"
    return out


CIN = {f"JQE_{k}": cbuild(k, NEW) for k in ["qe", "cv", "eb0"]}


def main():
    res = {}
    r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
    r.sync_parameters()
    out = r.run_inputs(IN)
    for k, v in out.items():
        res[k] = {"d": v["d"], "e": v["e"], "set": IN[k]["set"]}
        print(k, v["d"], v["e"], flush=True)

    # baseline JV with full curve
    # run baseline via char-style: use run_inputs then re-parse curve from result file is
    # unavailable here (op drops path); instead rerun through parse below using results dir.
    # Simpler: dedicated runner whose op returns the curve.
    rc = SCAPSrunner(lambda p: from_param_dict(p), curveop, ncores=2)
    cout = rc.run_inputs({"BASE_JV": S({})})
    for k, v in cout.items():
        res[k] = {"d": v["d"], "e": v["e"], "set": {}}
        json.dump({"V": v.get("V"), "J": v.get("J"), "deduced": v["d"]},
                  open(BASE / "outputs" / "baseline_JV.json", "w"))
        print(k, v["d"], v["e"], "npts=", len(v.get("V") or []), flush=True)

    # joint char regen: write .scaps scripts and call runner with identity processor.
    r2 = SCAPSrunner(lambda p: p, cop, ncores=2)
    r2.sync_parameters()
    cout2 = r2.run_inputs(CIN)
    for k, v in cout2.items():
        res[k] = {"d": v.get("deduced"), "e": v.get("error"),
                  "set": dict(NEW), "tables": [t for t in v if t.startswith("save_")]}
        print(k, v.get("deduced"), v.get("error"), flush=True)

    p = BASE / "outputs" / "s24_stack.json"
    old = json.load(open(p)) if p.exists() else {}
    old.update(res)
    json.dump(old, open(p, "w"), indent=1)
    print("s24 done")


if __name__ == "__main__":
    main()
