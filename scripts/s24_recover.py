"""Recover s24 char tables from on-disk SCAPS save files (import-safe)."""
import json
import numpy as np

BASE = "/home/touhid/Documents/leadpaper-polish-r8"
P = "/home/touhid/.scaps-runner"


def read_table(path, marker, cols):
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


def main():
    qe = read_table(P + "/proc0/drive_c/Program Files (x86)/Scaps3309/results/save_qe.txt",
                    "lambda(nm)", ["lambda", "QE", "E"])
    cv = read_table(P + "/proc0/drive_c/Program Files (x86)/Scaps3309/results/save_cv.txt",
                    "v(V)", ["V", "C", "G", "W", "Napp", "jtot", "jbulk", "jifr"])
    eb = read_table(P + "/proc1/drive_c/Program Files (x86)/Scaps3309/results/save_eb.txt",
                    "i", ["i", "x_um", "y", "Ec", "Fn", "Fp", "Ev", "n", "p",
                          "rho_def", "Ndop", "rho", "E", "jn", "jp", "jnt",
                          "jpt", "jtot", "gen", "rec", "cumG", "cumR_LR"])
    print("qe rows:", len(qe["lambda"]), "edge:", qe["lambda"][0], "->", qe["lambda"][-1],
          "maxQE:", round(max(qe["QE"]), 2))
    print("cv rows:", len(cv["V"]), "eb rows:", len(eb["x_um"]),
          "x-range:", round(min(eb["x_um"]), 3), round(max(eb["x_um"]), 3))
    p = BASE + "/outputs/s24_stack.json"
    d = json.load(open(p))
    d["JQE_qe"]["tables"] = {"save_qe.txt": qe}
    d["JQE_cv"]["tables"] = {"save_cv.txt": cv}
    d["JQE_eb0"]["tables"] = {"save_eb.txt": eb}
    for k in ["JQE_qe", "JQE_cv", "JQE_eb0"]:
        d[k]["e"] = None
    json.dump(d, open(p, "w"), indent=1)
    print("merged")


if __name__ == "__main__":
    main()
