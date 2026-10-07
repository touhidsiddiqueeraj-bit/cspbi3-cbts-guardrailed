"""R8 figure polish: regenerate flagged figs with print-size fonts,
higher-contrast fills, and grayscale-safe linestyles. Data identical.
Writes outputs/figs/ (caller copies to manuscript/figs/)."""
import json, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
FIG = BASE / "outputs" / "figs"
plt.rcParams.update({'font.family': 'serif', 'font.size': 11,
                     'axes.labelsize': 12, 'xtick.labelsize': 10,
                     'ytick.labelsize': 10, 'legend.fontsize': 10})

# ---- 1. timeline (was: 8.5pt labels, dpi 150) ----
exp = [(2016, 10.8), (2017, 17.0), (2018, 15.1), (2019, 18.4),
       (2025, 22.05), (2026, 21.71), (2026.2, 22.60), (2026.35, 21.43)]
sim = [(2022, 17.9), (2023, 19.06), (2023.15, 24.24),
       (2025, 24.17), (2026, 23.10), (2026.5, 23.49)]
fig, ax = plt.subplots(figsize=(9.6, 5.6))
ax.scatter([e[0] for e in exp], [e[1] for e in exp], s=70, marker='s',
           color='black', label='Experiment', zorder=3)
ax.scatter([s[0] for s in sim], [s[1] for s in sim], s=70, facecolors='none',
           edgecolors='black', linewidths=1.6, label='SCAPS-1D', zorder=3)
AR = dict(arrowstyle='-', color='0.5', lw=0.8, shrinkB=4)
for txt, xy, txy in [
        ('Swarnkar 10.8', (2016, 10.8), (12, 4)),
        ('Frolova 17.0', (2017, 17.0), (12, 4)),
        ('Wang 18.4', (2019, 18.4), (12, 4))]:
    ax.annotate(txt, xy, textcoords='offset points', xytext=txy,
                fontsize=10.5, arrowprops=AR)
for txt, xy, txy in [
        ('Oyedele* 24.24', (2023.15, 24.24), (2020.9, 25.4)),
        ('Qiu 22.05', (2025, 22.05), (2023.1, 23.4)),
        ('Zhang 21.71', (2026, 21.71), (2023.9, 19.9)),
        ('Dai lab 22.60', (2026.2, 22.60), (2027.2, 20.6)),
        ('Hu 21.43', (2026.35, 21.43), (2027.2, 22.4)),
        ('This work 23.49', (2026.5, 23.49), (2027.2, 24.0))]:
    ax.annotate(txt, xy, xytext=txy, fontsize=10.5, arrowprops=AR)
ax.axhline(22.02, ls='--', color='0.45', lw=1.2)
ax.text(2015.8, 22.25, '22.02% certified', va='bottom', fontsize=10.5, color='0.3')
ax.set_xlabel('Year'); ax.set_ylabel('PCE (%)')
ax.set_xlim(2015.5, 2029.5); ax.set_ylim(8, 26.5)
ax.set_title('CsPbI3 record race (* = no interface layers)', pad=10)
ax.legend(loc='upper left', borderpad=0.6)
fig.tight_layout(); fig.savefig(FIG / 'fig_timeline.png', dpi=300)

# ---- 2. alignment (was: pastel alpha 0.25, 8.5-9pt) ----
fig, ax = plt.subplots(figsize=(12.0, 6.9))
blocks = [("ITO\n(front)", -4.00, -7.50), ("TiO2\nETL", -3.70, -6.90),
          ("CsPbI3\nabsorber", -3.928, -5.578), ("CBTS\nHTL", -3.90, -5.80)]
for i, (lab, cb, vb) in enumerate(blocks):
    ax.fill_between([i - 0.3, i + 0.3], [cb, cb], [vb, vb],
                    color="0.55", alpha=0.45, zorder=1)
    ax.hlines(cb, i - 0.3, i + 0.3, colors="black", lw=3, zorder=3)
    ax.hlines(vb, i - 0.3, i + 0.3, colors="black", lw=3, ls="--", zorder=3)
    ax.text(i, cb + 0.12, f"{cb:.2f}", ha="center", fontsize=12, color="black")
    ax.text(i, vb - 0.15, f"{vb:.2f}", ha="center", fontsize=12, color="black")
    ax.text(i, -8.35, lab, ha="center", fontsize=12)
ax.hlines(-5.5, 3.7, 4.3, colors="black", lw=3)
ax.text(4.0, -5.35, "Ni 5.5 eV", ha="center", fontsize=12)
ax.annotate("", xy=(1.28, -3.70), xytext=(1.72, -3.93),
            arrowprops=dict(arrowstyle="<->", lw=1.4))
ax.text(1.5, -4.05, "spike +0.23 eV (raises $E_a$)", ha="center", fontsize=11.5)
ax.annotate("", xy=(2.28, -5.58), xytext=(2.72, -5.80),
            arrowprops=dict(arrowstyle="<->", lw=1.4))
ax.text(2.5, -6.15, "VBO +0.22 (barrier side: yet best)", ha="center", fontsize=12)
ax.set_xlim(-0.6, 4.6); ax.set_ylim(-8.6, -3.1)
ax.set_ylabel("Energy (eV, vacuum = 0)")
ax.set_xticks([])
ax.set_title("Joint-optimum alignment (absorber CB 0.23 eV below ETL: spike; absorber VB 0.22 eV below HTL)", pad=10)
fig.tight_layout(); fig.savefig(FIG / "fig_align.png", dpi=300)

# ---- 3. audit dose-response (was: 8pt legend/annotations) ----
fig, ax = plt.subplots(figsize=(11.4, 6.6))
nif = np.array([8, 9, 10, 11, 12]); eta = np.array([25.11, 24.77, 23.84, 22.62, 21.20])
ax.axvline(10, ls=":", color="0.5", zorder=1)
ax.plot(nif, eta, "o-", color="black", label="both interfaces (own cell)", zorder=3)
ax.text(10.06, 20.9, "guardrail $10^{10}$", fontsize=10.5, color="0.35", zorder=5,
        bbox=dict(fc="white", ec="none", pad=0.8))
ax.scatter([12.7], [25.16], s=70, facecolors="none", edgecolors="black", zorder=3,
           label="interfaces removed (above radiative Voc)")
ax.text(12.25, 24.82, "noIF 25.16 (unphysical)", fontsize=10.5, zorder=5,
        bbox=dict(fc="white", ec="none", pad=0.8))
ax.set_xlabel(r"Interface defect density (log$_{10}$ cm$^{-2}$, both sides)")
ax.set_ylabel("PCE (%)")
ax.set_xlim(7.7, 13.2); ax.set_ylim(20.5, 25.7)
ax.legend(loc="upper left", framealpha=1.0, fontsize=10)
ax.set_title("Interface dose-response (own cell): 23.84% at the guardrail", pad=10)
fig.tight_layout(); fig.savefig(FIG / "fig_audit.png", dpi=300)

# ---- 4-7. QE/CV/EB/GR grayscale-safe (was: default C0/C1 pairs) ----
char = {json.loads(l)["id"]: json.loads(l) for l in
        (BASE / "outputs" / "char.jsonl").read_text().splitlines() if l.strip()}
plt.figure()
for k, lab, st in [("qe_base", "baseline 800 nm", {"color": "0.5", "ls": "--"}),
                   ("qe_champ", r"champion 2.2 $\mu$m / $E_g$ 1.65", {"color": "black", "ls": "-"})]:
    d = char[k]["data"]["table"]
    plt.plot(d["lambda"], d["QE"], label=lab, lw=1.8, **st)
plt.xlabel("Wavelength (nm)"); plt.ylabel("QE (%)"); plt.legend(); plt.grid(True)
plt.title("Quantum efficiency: baseline vs champion")
plt.savefig(FIG / "fig_QE.png", dpi=300)

fig, ax = plt.subplots(2, 1, figsize=(7.4, 7.0), sharex=True)
for k, lab, st in [("cv_base", "baseline", {"color": "0.5", "ls": "--"}),
                   ("cv_champ", "champion", {"color": "black", "ls": "-"})]:
    d = char[k]["data"]["table"]
    V = np.array(d["V"]); C = np.array(d["C"])
    ax[0].plot(V, C, label=lab, lw=1.8, **st)
    ax[1].plot(V, 1 / np.array(C) ** 2, label=lab, lw=1.8, **st)
ax[0].set(xlabel="V (V)", ylabel="C (nF/cm$^2$)"); ax[1].set(xlabel="V (V)", ylabel="1/$C^2$ (cm$^4$/nF$^2$)")
for a in ax: a.legend(); a.grid(True)
fig.suptitle("C-V (1 MHz) and Mott-Schottky"); fig.savefig(FIG / "fig_CV_MS.png", dpi=300)

d = char["eb0_champ"]["data"]["table"]
x = np.array(d["x_um"])
plt.figure()
for c, st in [("Ec", {"color": "black", "ls": "-"}), ("Ev", {"color": "black", "ls": "--"}),
              ("Fn", {"color": "0.5", "ls": "-"}), ("Fp", {"color": "0.5", "ls": "--"})]:
    plt.plot(x, d[c], label=c, lw=1.8, **st)
plt.xlabel("x ($\mu$m, 0 = back/CBTS)"); plt.ylabel("Energy (eV)")
plt.legend(); plt.grid(True); plt.title("Champion band diagram @0V illuminated")
plt.savefig(FIG / "fig_EB.png", dpi=300)
plt.figure()
plt.semilogy(x, d["gen"], label="generation", color="black", lw=1.8)
plt.semilogy(x, d["rec"], label="recombination", color="black", ls="--", lw=1.8)
plt.xlabel("x ($\mu$m)"); plt.ylabel("rate (cm$^{-3}$ s$^{-1}$)"); plt.legend(); plt.grid(True)
plt.title("Generation / recombination profiles @0V")
plt.savefig(FIG / "fig_GR.png", dpi=300)
print("r8 figs done")
