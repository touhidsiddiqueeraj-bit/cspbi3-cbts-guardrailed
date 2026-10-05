"""Revision figures: corrected alignment, interface dose-response, Morris bars."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
FIG = '/home/touhid/Documents/leadpaper/outputs/figs/'
plt.rcParams.update({'font.family': 'serif', 'font.size': 10})

# --- joint-optimum band alignment (spike +0.23, VBO +0.22 barrier side) ---
fig, ax = plt.subplots(figsize=(12.0, 6.9))
blocks = [("ITO\n(front)", -4.00, -7.50, "C0"), ("TiO2\nETL", -3.70, -6.90, "C1"),
          ("CsPbI3\nabsorber", -3.928, -5.578, "C2"), ("CBTS\nHTL", -3.90, -5.80, "C3")]
for i, (lab, cb, vb, c) in enumerate(blocks):
    ax.bar(i, vb - cb if False else 0, bottom=0)
    ax.fill_between([i - 0.3, i + 0.3], [cb, cb], [vb, vb],
                    color="C%d" % i, alpha=0.25)
    ax.hlines(cb, i - 0.3, i + 0.3, colors="C%d" % i, lw=2.5)
    ax.hlines(vb, i - 0.3, i + 0.3, colors="red", lw=2.5)
    ax.text(i, cb + 0.12, f"{cb:.2f}", ha="center", fontsize=9, color="C%d" % i)
    ax.text(i, vb - 0.15, f"{vb:.2f}", ha="center", fontsize=9, color="red")
    ax.text(i, -8.35, lab, ha="center", fontsize=9)
ax.hlines(-5.5, 3.7, 4.3, colors="black", lw=2.5)
ax.text(4.0, -5.35, "Ni 5.5 eV", ha="center", fontsize=9)
ax.annotate("", xy=(1.28, -3.70), xytext=(1.72, -3.93),
            arrowprops=dict(arrowstyle="<->", lw=1.2))
ax.text(1.5, -4.05, "spike +0.23 eV (raises $E_a$)", ha="center", fontsize=8.5)
ax.annotate("", xy=(2.28, -5.58), xytext=(2.72, -5.80),
            arrowprops=dict(arrowstyle="<->", lw=1.2, color="red"))
ax.text(2.5, -6.15, "VBO +0.22 (barrier side: yet best)", ha="center", fontsize=9, color="red")
ax.set_xlim(-0.6, 4.6); ax.set_ylim(-8.6, -3.1)
ax.set_ylabel("Energy (eV, vacuum = 0)")
ax.set_xticks([])
ax.set_title("Joint-optimum alignment\n(absorber CB 0.23 eV below ETL: spike; absorber VB 0.22 eV below HTL)", pad=10)
fig.tight_layout(); fig.savefig(FIG + "fig_align.png", dpi=300)

# --- interface dose-response ---
fig, ax = plt.subplots(figsize=(11.4, 6.6))
nif = np.array([8, 9, 10, 11, 12]); eta = np.array([25.11, 24.77, 23.84, 22.62, 21.20])
ax.axvline(10, ls=":", color="0.5", zorder=1)
ax.plot(nif, eta, "o-", color="black", label="both interfaces (own cell)", zorder=3)
ax.text(10.06, 20.9, "guardrail $10^{10}$", fontsize=8.5, color="0.35", zorder=5,
        bbox=dict(fc="white", ec="none", pad=0.8))
ax.scatter([12.7], [25.16], s=60, facecolors="none", edgecolors="black", zorder=3, label="interfaces removed (above radiative Voc)")
ax.text(12.25, 24.82, "noIF 25.16 (unphysical)", fontsize=8.5, zorder=5,
        bbox=dict(fc="white", ec="none", pad=0.8))
ax.set_xlabel(r"Interface defect density (log$_{10}$ cm$^{-2}$, both sides)")
ax.set_ylabel("PCE (%)")
ax.set_xlim(7.7, 13.2); ax.set_ylim(20.5, 25.7)
ax.legend(loc="upper left", framealpha=1.0, fontsize=8)
ax.set_title("Interface dose-response (own cell): 23.84% at the guardrail", pad=10)
fig.tight_layout(); fig.savefig(FIG + "fig_audit.png", dpi=300)

# --- Morris mu* bars ---
import json
s = json.load(open("/home/touhid/Documents/leadpaper/outputs/s5_morris_summary.json"))["summary"]
order = ["logNif", "logNt", "Eg", "d", "logND", "logNA"]
labels = {"logNif": "log $N_{if}$ (both IF)", "logNt": "log $N_t$ (absorber)",
          "Eg": "$E_g$ (+$\\chi$ link)", "d": "thickness",
          "logND": "log $N_D$ (ETL)", "logNA": "log $N_A$ (absorber)"}
fig, ax = plt.subplots(figsize=(10.8, 5.4))
y = np.arange(len(order))
mu = [s[k]["mu_star"] for k in order]; sd = [s[k]["sigma"] for k in order]
ax.barh(y, mu, xerr=sd, capsize=3, color="0.35")
ax.set_yticks(y); ax.set_yticklabels([labels[k] for k in order])
ax.set_xlabel(r"Morris $\mu^*$ (PCE pts per unit input, $r=8$, $p=4$)")
ax.set_title("Sensitivity at the defect floor: interfaces lead (with interaction, see $\\sigma$)", pad=10)
fig.tight_layout(); fig.savefig(FIG + "fig_morris.png", dpi=300)
print("rev1 figs done")
