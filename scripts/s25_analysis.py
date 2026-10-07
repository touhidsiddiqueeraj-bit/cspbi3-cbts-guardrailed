"""S25 analysis: seed-21 trajectory rebuild, signed EEs (n=8, s13-style),
mu*/sigma, per-decade conversions, paired Nif-Nt + 20000 bootstrap CI.
Writes outputs/s25_analysis.json."""
import json
import numpy as np

BASE = "/home/touhid/Documents/leadpaper-polish-r8"
SEED = 21
p, r, k = 4, 8, 6
DELTA = p / (2 * (p - 1))
NAMES = ["d", "logNA", "logNt", "logND", "Eg", "logNif"]
SPAN = {"d": 1.8, "logNA": 1.5, "logNt": 3.0, "logND": 3.0,
        "Eg": 0.1, "logNif": 2.0}


def main():
    rng = np.random.default_rng(SEED)
    seqs, paths = [], []
    for _ in range(r):
        a = rng.integers(0, p, size=k) / (p - 1)
        o = rng.permutation(k)
        s = rng.choice([-1.0, 1.0], size=k)
        xx = a.copy(); pts = [xx.copy()]; seq = []
        for j in o:
            st = s[j] * DELTA
            if not (0 <= xx[j] + st <= 1):
                st = -st
            xx = xx.copy(); xx[j] += st
            pts.append(xx.copy()); seq.append((int(j), float(st)))
        paths.append(pts); seqs.append(seq)
    rows = [json.loads(l) for l in open(BASE + "/outputs/s25_morris.jsonl")]
    fx = {n: [] for n in NAMES}
    pair_diff = []
    etas_all = []
    for t in range(r):
        etas = []
        for u in paths[t]:
            m = next(x for x in rows if x["traj"] == t and np.allclose(x["u"], u))
            etas.append(m["deduced"]["eta"])
        etas_all.extend(etas)
        for s, (j, step) in enumerate(seqs[t]):
            fx[NAMES[j]].append((etas[s + 1] - etas[s]) / step)
        dnif = [((etas[s + 1] - etas[s]) / st) for s, (j, st) in enumerate(seqs[t])
                if NAMES[j] == "logNif"][0]
        dnt = [((etas[s + 1] - etas[s]) / st) for s, (j, st) in enumerate(seqs[t])
               if NAMES[j] == "logNt"][0]
        pair_diff.append(abs(dnif) - abs(dnt))
    pair_diff = np.array(pair_diff)
    OUT = {"mu_star": {}, "per_unit": {}, "span": [round(float(min(etas_all)), 2),
                                                   round(float(max(etas_all)), 2)]}
    for n in NAMES:
        v = np.array(fx[n])
        mu = float(np.mean(np.abs(v))); sg = float(np.std(v))
        per = mu / SPAN[n]
        unit = "per eV" if n == "Eg" else ("per um" if n == "d" else "per decade")
        OUT["mu_star"][n] = {"mu": round(mu, 3), "sigma": round(sg, 3), "n": len(v),
                             "per": round(per, 3), "per_unit": unit}
    # marginal CIs (20000 resamples of signed EE magnitudes)
    rng2 = np.random.default_rng(SEED)
    OUT["ci95"] = {}
    for n in NAMES:
        v = np.abs(np.array(fx[n])) / SPAN[n]
        bs = np.array([np.mean(rng2.choice(v, len(v), replace=True)) for _ in range(20000)])
        OUT["ci95"][n] = [round(float(np.quantile(bs, 0.025)), 3),
                          round(float(np.quantile(bs, 0.975)), 3)]
    bs = np.array([np.mean(rng2.choice(pair_diff, r, replace=True)) for _ in range(20000)])
    OUT["paired"] = {"mean": round(float(np.mean(pair_diff)), 3),
                     "ci95": [round(float(np.quantile(bs, 0.025)), 3),
                              round(float(np.quantile(bs, 0.975)), 3)],
                     "frac_positive": round(float(np.mean(pair_diff > 0)), 3)}
    json.dump(OUT, open(BASE + "/outputs/s25_analysis.json", "w"), indent=1)
    print(json.dumps(OUT, indent=1))


if __name__ == "__main__":
    main()
