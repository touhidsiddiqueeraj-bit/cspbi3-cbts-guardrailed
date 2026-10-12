import json, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
FIG = BASE / "outputs" / "figs"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({'font.family': 'serif', 'font.size': 11,
                     'axes.labelsize': 12, 'xtick.labelsize': 10,
                     'ytick.labelsize': 10, 'legend.fontsize': 10})

# ---- fig_align: enlarged canvas, spike label moved clear of the arrow ----
fig, ax = plt.subplots(figsize=(13.2, 7.6))
blocks = [("ITO\n(front)", -4.00, -7.50), ("TiO2\nETL", -3.70, -6.90),
          ("CsPbI3\nabsorber", -3.928, -5.578), ("CBTS\nHTL", -3.90, -5.80)]
for i, (lab, cb, vb) in enumerate(blocks):
    ax.fill_between([i - 0.3, i + 0.3], [cb, cb], [vb, vb],
                    color="0.55", alpha=0.45, zorder=1)
    ax.hlines(cb, i - 0.3, i + 0.3, colors="black", lw=3, zorder=3)
    ax.hlines(vb, i - 0.3, i + 0.3, colors="black", lw=3, ls="--", zorder=3)
    ax.text(i, cb + 0.30, f"{cb:.2f}", ha="center", fontsize=14, color="black")
    ax.text(i, vb - 0.38, f"{vb:.2f}", ha="center", fontsize=14, color="black")
    ax.text(i, -8.35, lab, ha="center", fontsize=14)
ax.hlines(-5.5, 3.7, 4.3, colors="black", lw=3)
ax.text(4.0, -5.35, "Ni 5.5 eV", ha="center", fontsize=14)
ax.annotate("", xy=(1.28, -3.70), xytext=(1.72, -3.93),
            arrowprops=dict(arrowstyle="<->", lw=1.4))
ax.text(1.66, -3.16, "spike +0.23 eV (raises $E_a$)", ha="center", fontsize=15,
        bbox=dict(fc="white", ec="none", pad=0.8))
ax.annotate("", xy=(2.28, -5.58), xytext=(2.72, -5.80),
            arrowprops=dict(arrowstyle="<->", lw=1.4))
ax.text(2.5, -6.15, "VBO +0.22 (barrier side: yet best)", ha="center", fontsize=15)
ax.set_xlim(-0.6, 4.6); ax.set_ylim(-8.6, -2.95)
ax.set_ylabel("Energy (eV, vacuum = 0)")
ax.set_xticks([])
ax.set_title("Joint-optimum alignment (absorber CB 0.23 eV below ETL: spike; absorber VB 0.22 eV below HTL)", pad=10)
fig.tight_layout(); fig.savefig(FIG / "fig_align.png", dpi=300)
fig.savefig(BASE / "manuscript" / "figs" / "fig_align.png", dpi=300)

# ---- fig_JVboth: x-axis Voltage (V) ----
c = json.load(open(BASE / 'outputs' / 'newchamp_JV.json'))
b = json.load(open(BASE / 'outputs' / 'baseline_JV.json'))
fig, ax = plt.subplots(figsize=(7.4, 4.6))
ax.plot(np.array(c['V']), -np.array(c['J']), color='black', lw=1.8,
        label=r"champion 2.2 $\mu$m, $E_g$ 1.65 eV (24.95%)")
ax.plot(np.array(b['V']), -np.array(b['J']), color='0.5', lw=1.8, ls='--',
        label="baseline 800 nm (18.99%)")
ax.set_xlabel('Voltage (V)'); ax.set_ylabel('J (mA cm$^{-2}$)')
ax.set_xlim(0, 1.35); ax.set_ylim(0, 25.5)
ax.axhline(0, color='0.4', lw=0.8)
ax.grid(alpha=0.3)
ax.legend(loc='upper center', framealpha=1.0, fontsize=10, ncol=2)
ax.set_title('Illuminated JV: baseline vs joint-optimum champion')
fig.tight_layout(); fig.savefig(FIG / 'fig_JVboth.png', dpi=300)
print('r15 figs done')
