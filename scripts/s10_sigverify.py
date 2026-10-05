"""R1: sigma set-field unit diagnosis + determinism/reproducibility floor.

Champion geometry (surveyed chi_TiO2=4.0 unless noted; step 0.02 so the
values are comparable with s1/s4/s6 reference receipts).

Decisive comparisons:
  set both interfaces sigma=1e-14  -> 22.2108 means set-units are cm^2 (x10)
  set both interfaces sigma=1e-15  -> 23.5041 means set-units are cm^2 (x1)
  set both interfaces sigma=1e-18  -> 25.15   means set-units are cm^2 (/1000)
  (the old s1/s6 "structural trap" run passed 1e-18.)
A raw script also saves the definition file after set commands so the stored
field can be read back (``get`` output is not captured by the runner).

Writes outputs/s10_sigverify.json and outputs/s10_checkdef.json.
"""
import sys, json, re, shutil, pathlib, glob, os
sys.path.insert(0, "/home/touhid/scaps-runner/src")
from scaps_runner import SCAPSrunner
from scaps_runner.script_gen import from_param_dict

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
BASEDEF = BASE / "defs" / "csPbI3-CBTS-r7.def"
SCADIR = pathlib.Path("/home/touhid/.scaps-runner/scaps_dat/def")


def def_variant(name, subs):
    t = BASEDEF.read_text()
    for a, b in subs:
        assert a in t, a
        t = t.replace(a, b)
    p = BASE / "defs" / name
    p.write_text(t)
    shutil.copy(p, SCADIR / name)
    return name


SIG4 = ["sigma_nleft : 1.000e-19 [m^2]", "sigma_nright : 1.000e-19 [m^2]",
        "sigma_pleft : 1.000e-19 [m^2]", "sigma_pright : 1.000e-19 [m^2]"]


def sig_both(name, new):
    return def_variant(name, [(s, s.replace("1.000e-19", new)) for s in SIG4])


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


IF1 = {"interface1.IFdefect1.capture_cross_section.electron": 1e-14,
       "interface1.IFdefect1.capture_cross_section.hole": 1e-14}
IF2 = {"interface2.IFdefect1.capture_cross_section.electron": 1e-14,
       "interface2.IFdefect1.capture_cross_section.hole": 1e-14}
BOTH = dict(IF1, **IF2)


def set_sig(v):
    return {k: v for k in BOTH}


IN = {
    # determinism / reproducibility floor (same config repeated in one batch)
    "base_c4": S({}),
    "base_c4_r2": S({}),
    "base_c4_r3": S({}),
    "base_c38": S({"layer3.chi": 3.8}),
    "base_c38_r2": S({"layer3.chi": 3.8}),
    "base_c38_r3": S({"layer3.chi": 3.8}),
    # set-route sigma values (the decisive unit test)
    "sig_set_1e18_both": S(set_sig(1e-18)),
    "sig_set_1e15_both": S(set_sig(1e-15)),
    "sig_set_1e14_both": S(set_sig(1e-14)),
    "sig_set_1e14_if1": S(IF1),
    "sig_set_1e14_if2": S(IF2),
    # def-copy controls (file units, m^2)
    "sig_def_x10_both": dict(CH, load=sig_both("csPbI3-CBTS-sigX10new.def", "1.000e-18")),
    "sig_def_div1000_both": dict(CH, load=sig_both("csPbI3-CBTS-sigdiv1000.def", "1.000e-22")),
}

RAW_CHECK = {
    "raw_script": (
        "clear actions\n"
        "load definitionfile csPbI3-CBTS-r7.def\n"
        "set layer2.NA 1e16\n"
        "set interface1.IFdefect1.capture_cross_section.electron 1e-14\n"
        "set interface1.IFdefect1.capture_cross_section.hole 1e-14\n"
        "save settings definitionfile R1_checkdef.def\n"
    ),
}


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


def proc(p):
    if "raw" in p:
        return p["raw"]
    return from_param_dict(p)


r = SCAPSrunner(proc, op, ncores=4)
r.sync_parameters()
out = r.run_inputs(IN)
res = {k: {"d": v["d"], "e": v["e"], "load": IN[k]["load"]} for k, v in out.items()}
open(BASE / "outputs" / "s10_sigverify.json", "w").write(json.dumps(res, indent=1))
print(json.dumps({k: (v["d"], v["e"]) for k, v in res.items()}, indent=1))

# --- saved-definition readback (separate single run; failure is diagnostic) ---
raw_out = r.run_inputs(RAW_CHECK)
hits = glob.glob(os.path.expanduser("~/.scaps-runner/proc*/**/R1_checkdef.def"), recursive=True)
hits.sort(key=os.path.getmtime, reverse=True)
readback = {"raw_out": raw_out.get("raw_script"), "found": hits[:3], "fields": None}
if hits:
    t = open(hits[0], errors="ignore").read().splitlines()
    keep = []
    for i, ln in enumerate(t):
        if "sigma_nleft" in ln or "sigma_pleft" in ln or "sigma_nright" in ln or "sigma_pright" in ln:
            keep.append(ln.strip())
        if ln.strip().startswith("Nleft") or ln.strip().startswith("Nright"):
            keep.append(ln.strip())
        if "NA" in ln and "[/m^3]" in ln and "layer" not in ln:
            keep.append(ln.strip())
    readback["fields"] = keep
open(BASE / "outputs" / "s10_checkdef.json", "w").write(json.dumps(readback, indent=1))
print(json.dumps(readback, indent=1))
