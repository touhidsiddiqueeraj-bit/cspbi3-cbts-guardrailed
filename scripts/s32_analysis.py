"""S29 analysis: prior-predictive median + 5-95% interval, 20k-bootstrap
CIs on both percentiles, per-run Voc (<=1.418 at Eg 1.70) + Green-FF
screens with flagged count, optical +/-1.2 mA post-propagation,
rank-correlation importances. Writes outputs/s32_analysis.json."""
import json
import numpy as np

BASE = "/home/touhid/Documents/leadpaper-polish-r8"
VT = 0.025692


def green_ff(v):
    return (v - VT * np.log(v / VT + 1)) / (v + VT) * 100


def main():
    rows = [json.loads(l) for l in open(BASE + "/outputs/s32_lhs_dos.jsonl")]
    main_rows = [r for r in rows if not r["id"].startswith("Q0_")]
    sens_rows = [r for r in rows if r["id"].startswith("Q0_")]
    etas = np.array([r["d"]["eta"] for r in main_rows])
    OUT = {"n_main": len(main_rows), "n_sens": len(sens_rows),
           "converged": int(np.sum([r["d"]["eta"] is not None for r in rows]))}
    med = float(np.median(etas))
    p5, p95 = float(np.quantile(etas, 0.05)), float(np.quantile(etas, 0.95))
    OUT["interval"] = {"median": round(med, 2), "p5": round(p5, 2), "p95": round(p95, 2)}
    rng = np.random.default_rng(13)
    for q, name in [(0.05, "p5"), (0.5, "median"), (0.95, "p95")]:
        bs = np.array([np.quantile(rng.choice(etas, len(etas), replace=True), q)
                       for _ in range(20000)])
        OUT[f"ci_{name}"] = [round(float(np.quantile(bs, 0.025)), 2),
                             round(float(np.quantile(bs, 0.975)), 2)]
    # per-run screens
    flags = []
    for r in main_rows:
        d = r["d"]
        gff = green_ff(d["Voc"])
        hit = []
        if d["Voc"] > 1.418:
            hit.append("Voc-bound")
        if d["FF"] > gff:
            hit.append("Green-FF")
        if hit:
            flags.append((r["id"], hit))
    OUT["screen_flags"] = {"n_flagged": len(flags), "flags": flags}
    # optical post-propagation: dPCE ~= PCE * 1.2 / Jsc
    jsc = np.array([r["d"]["Jsc"] for r in main_rows])
    opt = etas * 1.2 / jsc
    OUT["optical_scale"] = {"mean_pts": round(float(opt.mean()), 2),
                            "note": "electrical-only interval otherwise"}
    # rank importances (Spearman of eta vs each factor)
    from scipy.stats import spearmanr
    keys = ["logNt", "logNif", "Cr", "mu", "Rs", "ITO", "Ni", "d", "logNv"]
    imp = {}
    for k in keys:
        v = np.array([r["meta"][k] if k != "Cr" else np.log10(max(r["meta"][k], 1e-12))
                      for r in main_rows])
        imp[k] = round(float(spearmanr(v, etas).statistic), 3)
    OUT["spearman"] = imp
    # Cr=0 sensitivity
    if sens_rows:
        se = np.array([r["d"]["eta"] for r in sens_rows if r["d"]["eta"]])
        if len(se):
            OUT["Cr0_sensitivity"] = {"median": round(float(np.median(se)), 2),
                                      "n": len(se)}
    json.dump(OUT, open(BASE + "/outputs/s32_analysis.json", "w"), indent=1)
    print(json.dumps(OUT, indent=1))


if __name__ == "__main__":
    main()
