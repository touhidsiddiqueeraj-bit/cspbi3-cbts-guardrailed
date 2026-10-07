"""S34: automated energetic screens over all sweep receipts.

For every run with Voc/FF in the archived JSON/JSONL receipts, checks:
- Voc <= Eg - 0.28 V (1.371 at 1.65 eV, 1.418 at 1.70 eV; Eg from run
  sets, defaulting to the base gap of each batch),
- FF <= Green ideal-diode FF at the run's Voc.
Writes outputs/s34_gates.json with per-batch flagged counts.
Analysis only (no SCAPS calls).
"""
import json, glob, math, pathlib

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
VT = 0.025692


def green_ff(v):
    return (v - VT * math.log(v / VT + 1)) / (v + VT) * 100


def eg_of(rec, default):
    try:
        return float(rec.get("set", {}).get("layer2.Eg", default))
    except (TypeError, ValueError):
        return default


BATCH_GAP = {"roundA": 1.65, "roundB": 1.65}


def iter_runs(path):
    import json as J
    txt = open(path).read()
    try:
        obj = J.loads(txt)
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, dict) and isinstance(v.get("d"), dict):
                    yield k, v
            return
    except Exception:
        pass
    for ln in txt.splitlines():
        if not ln.strip():
            continue
        try:
            r = J.loads(ln)
        except Exception:
            continue
        dd = r.get("d") or r.get("deduced")
        if isinstance(dd, dict):
            yield r.get("id", "?"), {"d": dd, "set": r.get("set", r.get("params", {}))}


def main():
    out = {"flagged": [], "batches": {}}
    seen = {}
    n = 0
    for f in sorted(glob.glob(str(BASE / "outputs" / "*.json")) +
                    glob.glob(str(BASE / "outputs" / "*.jsonl"))):
        name = pathlib.Path(f).stem
        default = 1.65
        for key, gap in (("roundA", 1.65), ("roundB", 1.65), ("char", 1.65),
                         ("s14", 1.65), ("s6_rev2", 1.65), ("s10", 1.65),
                         ("s16", 1.65), ("s17", 1.65), ("s13_opt", 1.65),
                         ("s28_calib", 1.70), ("s24_stack", 1.65), ("s26_diag", 1.65),
                         ("s31_small", 1.65), ("s35_phys", 1.65), ("s11_", 1.65),
                         ("s5_morris", 1.65), ("s25_morris", 1.65),
                         ("s18_analytic", None), ("s29", 1.70), ("s32", 1.70),
                         ("s13_analysis", None), ("s25_analysis", None),
                         ("s29_analysis", None), ("s32_analysis", None),
                         ("baseline", 1.694), ("newchamp", 1.65), ("noIF", 1.65),
                         ("s0_", 1.65), ("s1_", 1.65), ("s4", 1.65),
                         ("s9_", 1.65), ("s12_", 1.65), ("s21_", 1.65),
                         ("s22_", 1.65), ("diag_", 1.65), ("retry_", 1.65),
                         ("probe_", 1.65), ("analysis", None), ("sobol", None)):
            if key in name:
                default = gap
                break
        if default is None:
            continue
        nb, nf = 0, 0
        for rid, rec in iter_runs(f):
            d = rec["d"]
            if not isinstance(d, dict) or d.get("Voc") is None or d.get("FF") is None:
                continue
            nb += 1
            n += 1
            sig = (round(d["Voc"], 6), round(d["FF"], 4),
                   round(d["eta"], 4) if d.get("eta") is not None else None)
            seen[sig] = seen.get(sig, 0) + 1
            eg = eg_of(rec, default)
            hits = []
            if d["Voc"] > eg - 0.28:
                hits.append("Voc-bound(%.3f)" % (eg - 0.28))
            if d["FF"] > green_ff(d["Voc"]):
                hits.append("Green-FF(%.2f)" % green_ff(d["Voc"]))
            if hits:
                nf += 1
                out["flagged"].append({"file": name, "id": rid,
                                      "Voc": d["Voc"], "FF": d["FF"],
                                      "eta": d.get("eta"), "hits": hits})
        out["batches"][name] = {"checked": nb, "flagged": nf}
    out["total_checked"] = n
    out["unique_configurations"] = len(seen)
    out["note"] = ("entries include intentional cross-batch replications "
                   "(same parameters rerun as determinism checks); "
                   "unique value-configurations differ")
    json.dump(out, open(BASE / "outputs" / "s34_gates.json", "w"), indent=1)
    print("checked %d, flagged %d" % (n, len(out["flagged"])))
    for f in out["flagged"]:
        print(f["file"], f["id"], f["Voc"], f["FF"], f["hits"])
    print("s34 done")


if __name__ == "__main__":
    main()
