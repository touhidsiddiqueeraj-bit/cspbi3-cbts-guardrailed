"""Morris bars from s25 (guardrail-clean)."""
import json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
    s = json.load(open(BASE / "outputs" / "s25_analysis.json"))["mu_star"]
    order = ["logNif", "logNt", "Eg", "d", "logND", "logNA"]
    labels = {"logNif": "log $N_{if}$ (both IF)", "logNt": "log $N_t$ (absorber)",
              "Eg": "$E_g$ (+$\\chi$ link)", "d": "thickness",
              "logND": "log $N_D$ (ETL)", "logNA": "log $N_A$ (absorber)"}
    plt.rcParams.update({'font.family': 'serif', 'font.size': 13,
                         'axes.labelsize': 14, 'xtick.labelsize': 14,
                         'ytick.labelsize': 14, 'legend.fontsize': 13})
    fig, ax = plt.subplots(figsize=(10.8, 5.4))
    y = list(range(len(order)))
    mu = [s[k]["mu"] for k in order]
    sd = [s[k]["sigma"] for k in order]
    ax.barh(y, mu, xerr=sd, capsize=3, color="0.35")
    ax.errorbar([-1], [-1], xerr=[0.1], fmt='none', ecolor='0.35', capsize=3,
                label=r'whiskers: $\mu \pm \sigma$')
    ax.legend(loc='lower right')
    ax.set_xlim(left=0)
    ax.set_yticks(y); ax.set_yticklabels([labels[k] for k in order])
    ax.set_xlabel(r"Morris $\mu^*$ (per normalised unit input, $r=8$, $p=4$, seed 21)")
    ax.set_title("Sensitivity inside the guardrailed box ($N_{if}$ $10^{10}$--$10^{12}$)", pad=10)
    fig.tight_layout()
    fig.savefig(BASE / "outputs" / "figs" / "fig_morris.png", dpi=300)
    fig.savefig(BASE / "manuscript" / "figs" / "fig_morris.png", dpi=300)
    print("morris fig done")


if __name__ == "__main__":
    main()
