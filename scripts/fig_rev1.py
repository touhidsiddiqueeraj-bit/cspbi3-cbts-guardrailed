"""Revision figures: corrected alignment, interface dose-response, Morris bars."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
FIG = '/home/touhid/Documents/leadpaper/outputs/figs/'
plt.rcParams.update({'font.family': 'serif', 'font.size': 10})

# --- corrected band alignment (VBO +0.08 hole barrier, not -0.22) ---
fig, ax = plt.subplots(figsize=(8.0, 4.6))
blocks = [("ITO\n(front)", -4.00, -7.50, "C0"), ("TiO2\nETL", -3.80, -7.00, "C1"),
          ("CsPbI3\nabsorber", -3.928, -5.578, "C2"), ("CBTS\nHTL", -3.60, -5.50, "C3")]
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
ax.annotate("", xy=(1.28, -3.80), xytext=(1.72, -3.93),
            arrowprops=dict(arrowstyle="<->", lw=1.2))
ax.text(1.5, -3.30, "spike +0.13 (raises $E_a$)", ha="center", fontsize=9)
ax.annotate("", xy=(2.28, -5.58), xytext=(2.72, -5.50),
            arrowprops=dict(arrowstyle="<->", lw=1.2, color="red"))
ax.text(2.5, -5.95, "VBO +0.08 (shallow, favourable side)", ha="center", fontsize=9, color="red")
ax.set_xlim(-0.6, 4.6); ax.set_ylim(-8.6, -3.2)
ax.set_ylabel("Energy (eV, vacuum = 0)")
ax.set_xticks([])
ax.set_title("Adopted alignment\n(absorber CB 0.13 eV below ETL: spike; absorber VB 0.08 eV below HTL)", pad=10)
fig.tight_layout(); fig.savefig(FIG + "fig_align.png", dpi=150)

# --- interface dose-response ---
fig, ax = plt.subplots(figsize=(7.6, 4.4))
nif = np.array([8, 9, 10, 11, 12]); eta = np.array([25.11, 24.77, 23.84, 22.62, 21.20])
ax.plot(nif, eta, "o-", color="black", label="This work, both interfaces")
ax.axvline(10, ls=":", color="0.5"); ax.text(10.03, 20.9, "guardrail $10^{10}$", fontsize=8.5, color="0.35")
ax.axhspan(24.17, 24.24, color="C1", alpha=0.25)
ax.text(8.15, 23.55, "literature claims 24.17 / 24.24\n(scale reference only)", fontsize=7.5, color="C1")
ax.scatter([12.6], [25.16], s=60, facecolors="none", edgecolors="black")
ax.text(12.15, 25.25, "noIF 25.16", fontsize=8.5)
ax.set_xlabel(r"Interface defect density (log$_{10}$ cm$^{-2}$, both sides)")
ax.set_ylabel("PCE (%)")
ax.set_xlim(7.7, 13.0); ax.set_ylim(20.6, 25.6)
ax.set_title("Interface dose-response (own cell): 23.84% at the guardrail", pad=10)
fig.tight_layout(); fig.savefig(FIG + "fig_audit.png", dpi=150)

# --- Morris mu* bars ---
import json
s = json.load(open("/home/touhid/Documents/leadpaper/outputs/s5_morris_summary.json"))["summary"]
order = ["logNif", "logNt", "Eg", "d", "logND", "logNA"]
labels = {"logNif": "log $N_{if}$ (both IF)", "logNt": "log $N_t$ (absorber)",
          "Eg": "$E_g$ (+$\\chi$ link)", "d": "thickness",
          "logND": "log $N_D$ (ETL)", "logNA": "log $N_A$ (absorber)"}
fig, ax = plt.subplots(figsize=(7.2, 3.6))
y = np.arange(len(order))
mu = [s[k]["mu_star"] for k in order]; sd = [s[k]["sigma"] for k in order]
ax.barh(y, mu, xerr=sd, capsize=3, color="0.35")
ax.set_yticks(y); ax.set_yticklabels([labels[k] for k in order])
ax.set_xlabel(r"Morris $\mu^*$ (PCE pts per unit input, $r=8$, $p=4$)")
ax.set_title("Sensitivity: interfaces dominate (with interaction, see $\\sigma$)", pad=10)
fig.tight_layout(); fig.savefig(FIG + "fig_morris.png", dpi=150)
print("rev1 figs done")
