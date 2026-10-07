"""S27: QE illumination-mode test. Joint-base QE under explicit
`set numerical qe constant_photonflux` vs constant_photonpower.
If the QE curve (and its integral) moves with the flux mode, the 5%
QE-vs-IV gap is a flux-normalisation mechanism, not a data error.
Merges tables into outputs/s24_stack.json as JQE_flux/JQE_power."""
import sys, json, os, re, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
NEW = {"layer2.thickness": 2.2, "layer2.NA": 3e16,
       "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
       "layer2.Eg": 1.65, "layer2.chi": 3.928,
       "layer1.chi": 3.9, "layer3.chi": 3.7}


def qe_script(mode):
    c = ["clear actions", "load definitionfile csPbI3-CBTS-r7.def"]
    for k, val in NEW.items():
        c.append(f"set {k} {val}")
    c += [f"set numerical qe {mode}",
          "action workingpoint.temperature 300", "action intensity.T 100", "action light",
          "action qe.startlambda 300", "action qe.stoplambda 850",
          "action qe.points 56", "action qe.doqe",
          "action iv.startv 0", "action iv.stopv 1.6", "action iv.increment 0.05",
          "action iv.doiv", "calculate singleshot", "save results.qe save_qe.txt"]
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
    return {"deduced": d, "mode": None, "tables": {}}


def main():
    IN = {"JQE_flux": qe_script("constant_photonflux"),
          "JQE_power": qe_script("constant_photonpower")}
    r = SCAPSrunner(lambda q: q, cop, ncores=2)
    r.sync_parameters()
    out = r.run_inputs(IN)
    print({k: v["deduced"] for k, v in out.items()}, flush=True)
    print("s27 done (tables recovered post-hoc like s24)")


if __name__ == "__main__":
    main()
