"""S26: contact artifact (Ni 5.8/6.0 at joint base) + physical-DOS
sensitivity (champion + routine) + Cr 1e-11 bracket + IV-step convergence.
Merges into outputs/s26_diag.json."""
import sys, json, shutil, pathlib
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
BASEDEF = BASE / "defs" / "csPbI3-CBTS-r7.def"
SCADIR = pathlib.Path("/home/touhid/.scaps-runner/scaps_dat/def")
NEW = {"layer2.thickness": 2.2, "layer2.NA": 3e16,
       "layer2.defect1.Ntotal": 1e12, "layer3.ND": 9e17,
       "layer2.Eg": 1.65, "layer2.chi": 3.928,
       "layer1.chi": 3.9, "layer3.chi": 3.7}
ROUTINE = {"layer2.thickness": 1.0, "layer2.NA": 3e16,
           "layer2.defect1.Ntotal": 1e15, "layer3.ND": 9e17,
           "layer2.Eg": 1.65, "layer2.chi": 3.928}
WP = {"workingpoint": {"temperature": 300, "illumination": 100}}
IV = {"start": 0, "stop": 1.6, "step": 0.02}


def def_variant(name, back=None):
    t = BASEDEF.read_text()
    assert "Fi_m :   5.5000 [eV]" in t
    t = t.replace("Fi_m :   5.5000 [eV]", f"Fi_m :   {back:.4f} [eV]")
    p = BASE / "defs" / name
    p.write_text(t)
    shutil.copy(p, SCADIR / name)
    return name


def S(extra, load="csPbI3-CBTS-r7.def", iv=None):
    return dict({"load": load}, set=dict(extra), **WP, iv=dict(iv or IV))


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
    ni58 = def_variant("csPbI3-CBTS-ni58.def", back=5.8)
    ni60 = def_variant("csPbI3-CBTS-ni60.def", back=6.0)
    IN = {
        # contact artifact at joint base
        "J_ni58": S(dict(NEW), load=ni58),
        "J_ni60": S(dict(NEW), load=ni60),
        # DOS same-value checks (validate Nc/Nv set path + units)
        "J_doscheck": S(dict(NEW, **{"layer2.Nc": 1.1e19, "layer2.Nv": 8.2e19})),
        "R_doscheck": S(dict(ROUTINE, **{"layer2.Nc": 1.1e19, "layer2.Nv": 8.2e19})),
        # physical DOS (m* 0.3 -> 4.1e18; m* 0.5 -> 8.9e18), Nv only
        "J_dos03": S(dict(NEW, **{"layer2.Nv": 4.1e18})),
        "J_dos05": S(dict(NEW, **{"layer2.Nv": 8.9e18})),
        "R_dos03": S(dict(ROUTINE, **{"layer2.Nv": 4.1e18})),
        "R_dos05": S(dict(ROUTINE, **{"layer2.Nv": 8.9e18})),
        # Cr 1e-11 bracket
        "J_cr1em11": S(dict(NEW, **{"layer2.radiative": 1e-11})),
        "R_cr1em11": S(dict(ROUTINE, **{"layer2.radiative": 1e-11})),
        # IV-step convergence at champion
        "J_iv001": S(dict(NEW), iv={"start": 0, "stop": 1.6, "step": 0.01}),
        "J_iv0005": S(dict(NEW), iv={"start": 0, "stop": 1.6, "step": 0.005}),
    }
    r = SCAPSrunner(lambda p: from_param_dict(p), op, ncores=4)
    r.sync_parameters()
    out = r.run_inputs(IN)
    p = BASE / "outputs" / "s26_diag.json"
    res = json.load(open(p)) if p.exists() else {}
    for k, v in out.items():
        res[k] = {"d": v["d"], "e": v["e"], "set": IN[k]["set"]}
        print(k, v["d"], v["e"], flush=True)
    json.dump(res, open(p, "w"), indent=1)
    print("s26 done")


if __name__ == "__main__":
    main()
