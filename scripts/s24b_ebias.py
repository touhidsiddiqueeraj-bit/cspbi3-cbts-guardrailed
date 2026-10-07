"""S24b: biased band diagrams (MPP/Voc Ni-contact budget) + NREL-spectrum
champion IV (Jsc-gap diagnostic). Custom raw scripts, identity processor.
Merges into outputs/s24_stack.json under JEB_v115, JEB_v130, J_NREL.
"""
import sys, json, os, re, shutil, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
NEW = {"layer2.thickness": 2.2, "layer2.NA": 3e16,
       "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
       "layer2.Eg": 1.65, "layer2.chi": 3.928,
       "layer1.chi": 3.9, "layer3.chi": 3.7}
SPE_SRC = "/home/touhid/.wine/drive_c/Program Files (x86)/Scaps3309/spectrum/AM1_5G 1 sun.spe"


def eb_at(v):
    c = ["clear actions", "load definitionfile csPbI3-CBTS-r7.def"]
    for k, val in NEW.items():
        c.append(f"set {k} {val}")
    c += ["action workingpoint.temperature 300", "action intensity.T 100", "action light",
          f"action workingpoint.voltage {v}", "calculate singleshot",
          "save results.eb save_eb.txt"]
    return "set quitscript.quitSCAPS\nset errorhandling.overwritefile\n" + "\n".join(c) + "\n"


def iv_nrel():
    c = ["clear actions", "load definitionfile csPbI3-CBTS-r7.def"]
    for k, val in NEW.items():
        c.append(f"set {k} {val}")
    c += ["load spectrumfile NREL_AM15G.spe",
          "action workingpoint.temperature 300", "action intensity.T 100", "action light",
          "action iv.startv 0", "action iv.stopv 1.6", "action iv.increment 0.02",
          "action iv.doiv", "calculate singleshot"]
    return "set quitscript.quitSCAPS\nset errorhandling.overwritefile\n" + "\n".join(c) + "\n"


def read_table(path, marker, cols):
    import numpy as np
    lines = open(path, errors="ignore").readlines()
    si = next(i for i, l in enumerate(lines) if l.strip().startswith(marker))
    out = []
    for l in lines[si + 1:]:
        s = l.strip()
        if not s:
            continue
        try:
            vals = [float(x) for x in s.split()]
        except ValueError:
            break
        if len(vals) < len(cols):
            continue
        out.append(vals[:len(cols)])
        if len(out) > 5000:
            break
    a = np.array(out)
    return {c: a[:, j].tolist() for j, c in enumerate(cols)}


def cop(result_file):
    rdir = os.path.dirname(result_file)
    txt = open(result_file, errors="ignore").read()
    d = {}
    for k, pat in [("Voc", r"Voc\s*=\s*([0-9.\-eE+]+)"),
                   ("Jsc", r"Jsc\s*=\s*([0-9.\-eE+]+)"),
                   ("FF", r"FF\s*=\s*([0-9.\-eE+]+)"),
                   ("eta", r"eta\s*=\s*([0-9.\-eE+]+)")]:
        m = re.search(pat, txt)
        d[k] = float(m.group(1)) if m else None
    out = {"deduced": d, "error": None if d["eta"] else "no-eta"}
    p = os.path.join(rdir, "save_eb.txt")
    if os.path.exists(p):
        try:
            out["save_eb.txt"] = read_table(p, "i", ["i", "x_um", "y", "Ec", "Fn", "Fp", "Ev",
                                                     "n", "p", "rho_def", "Ndop", "rho", "E",
                                                     "jn", "jp", "jnt", "jpt", "jtot", "gen",
                                                     "rec", "cumG", "cumR_LR"])
        except Exception as e:
            out["save_eb_error"] = str(e)[:200]
    return out


def main():
    dst = os.path.join(os.path.dirname(SPE_SRC), "NREL_AM15G.spe")
    if not os.path.exists(dst):
        shutil.copy(SPE_SRC, dst)
    IN = {"JEB_v115": eb_at(1.15), "JEB_v130": eb_at(1.30), "J_NREL": iv_nrel()}
    r = SCAPSrunner(lambda q: q, cop, ncores=4)
    r.sync_parameters()
    out = r.run_inputs(IN)
    p = BASE / "outputs" / "s24_stack.json"
    res = json.load(open(p))
    for k, v in out.items():
        entry = {"d": v.get("deduced"), "e": v.get("error"), "set": dict(NEW)}
        if "save_eb.txt" in v:
            entry["tables"] = {"save_eb.txt": v["save_eb.txt"]}
        res[k] = entry
        print(k, v.get("deduced"), v.get("error"), flush=True)
    json.dump(res, open(p, "w"), indent=1)
    print("s24b done")


if __name__ == "__main__":
    main()
