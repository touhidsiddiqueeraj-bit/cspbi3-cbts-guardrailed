"""Deck figure pack: 6 new publication graphs from archived receipts, serif + warm neutrals."""
import json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = pathlib.Path("/home/touhid/Documents/leadpaper")
OUT = pathlib.Path("/home/touhid/Documents/leadpaper/opendesign/mockups/record-race-deck/pptx_figs")
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.size": 13})
ACC, ACC2, INK = "#b3541e", "#2e6e5e", "#1c1a16"

# 1. affinity heatmap (Grid A + peak extension)
s11 = json.load(open(BASE / "outputs/s11_joint_chi.json"))
s16 = json.load(open(BASE / "outputs/s16.json"))
chih = [3.5, 3.55, 3.6, 3.65, 3.7, 3.75, 3.8, 3.85, 3.9, 3.95, 4.0, 4.05, 4.1]
chie = [3.6, 3.7, 3.8, 3.9, 4.0]
grid = np.full((len(chih), len(chie)), np.nan)
for k, v in list(s11.items()) + list(s16.items()):
    if not (v["d"] and v["d"].get("eta")):
        continue
    s = v.get("set", {})
    h, e = round(s.get("layer1.chi", -1), 2), round(s.get("layer3.chi", -1), 1)
    if h in chih and e in chie:
        grid[chih.index(h), chie.index(e)] = v["d"]["eta"]
fig, ax = plt.subplots(figsize=(9, 6.5))
im = ax.imshow(grid, origin="lower", aspect="auto", cmap="YlOrBr", vmin=21, vmax=25)
ax.set_xticks(range(len(chie)), [f"{e:.1f}" for e in chie])
ax.set_yticks(range(len(chih)), [f"{h:.2f}" for h in chih])
ax.set_xlabel("χ TiO2 (eV)"); ax.set_ylabel("χ CBTS (eV)")
ax.set_title("Joint affinity map: PCE (%) at guardrailed interfaces")
for i in range(len(chih)):
    for j in range(len(chie)):
        if not np.isnan(grid[i, j]):
            ax.text(j, i, f"{grid[i, j]:.1f}", ha="center", va="center", fontsize=8,
                    color="white" if grid[i, j] > 23.5 else "black")
fig.colorbar(im, label="PCE (%)")
fig.tight_layout(); fig.savefig(OUT / "affinity_heatmap.png", dpi=300)

# 2. Rs derate: computed vs analytic
eta0, J, FF0, V = 24.9464, 21.19740913, 0.891083, 1.320708
rs = np.array([0, 0.5, 1.0, 2.0])
comp = np.array([24.9464, 24.7311, 24.5160, 24.0866])
ana = eta0 / (1 + J * rs / (1e3 * FF0 * V))
fig, ax = plt.subplots(figsize=(8, 5.2))
ax.plot(rs, comp, "o-", color="black", ms=8, label="computed (SCAPS)")
xx = np.linspace(0, 2.2, 50)
ax.plot(xx, eta0 / (1 + J * xx / (1e3 * FF0 * V)), "--", color=ACC, label="analytic derate")
ax.set_xlabel("Rs (Ωcm²)"); ax.set_ylabel("PCE (%)")
ax.set_title("Series resistance: scripted sweep vs analytic (max Δ 0.011 pts)")
ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(OUT / "rs_derate.png", dpi=300)

# 3. thickness x Nt factorial
s21 = json.load(open(BASE / "outputs/s21_thNt.json"))
ths = [0.5, 0.8, 1.0, 1.5]
g14 = [s21[f"th{t:g}_nt1e+14"]["d"]["eta"] if s21.get(f"th{t:g}_nt1e+14", {}).get("d") else np.nan for t in ths]
g15 = [s21[f"th{t:g}_nt1e+15"]["d"]["eta"] for t in ths]
x = np.arange(len(ths)); w = 0.35
fig, ax = plt.subplots(figsize=(8, 5.2))
ax.bar(x - w / 2, g14, w, label="Nt = 10¹⁴ cm⁻³", color=ACC2)
ax.bar(x + w / 2, g15, w, label="Nt = 10¹⁵ cm⁻³ (routine)", color=ACC)
ax.set_xticks(x, [f"{t:g}" for t in ths]); ax.set_xlabel("thickness (µm)")
ax.set_ylabel("PCE (%)"); ax.set_title("Optimum shifts with defects: 1.5 µm → 1.0 µm")
ax.legend(); ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig(OUT / "thickness_nt.png", dpi=300)

# 4. loss budget: PCE bars ours vs records
names = ["This work\n(bound)", "AP 22.16", "QD 22.15", "Dual-IF 21.71", "Carbon 20.72", "Cert. record"]
vals = [24.95, 22.16, 22.15, 21.71, 20.72, 22.02]
cols = [INK, ACC2, ACC2, ACC2, ACC2, "0.55"]
fig, ax = plt.subplots(figsize=(9, 5.2))
ax.bar(names, vals, color=cols)
ax.axhline(22.02, ls=":", color="0.4")
ax.set_ylabel("PCE (%)"); ax.set_title("Loss budget: simulation bound vs measured records")
fig.tight_layout(); fig.savefig(OUT / "loss_budget.png", dpi=300)

# 5. optimizer scatter: eta vs Nif
s13 = json.load(open(BASE / "outputs/s13_opt.json"))
nif, eta, grd = [], [], []
for v in s13.values():
    if v["d"] and v["d"].get("eta"):
        n = v["set"]["interface1.IFdefect1.Ntotal"]
        nif.append(n); eta.append(v["d"]["eta"]); grd.append(n >= 1e10)
nif, eta, grd = map(np.array, (nif, eta, grd))
fig, ax = plt.subplots(figsize=(8, 5.2))
ax.semilogx(nif[~grd], eta[~grd], "o", color="0.7", label="below floor (audit only)")
ax.semilogx(nif[grd], eta[grd], "o", color=ACC, label="guardrail-satisfying")
ax.axvline(1e10, ls=":", color="0.4"); ax.axhline(24.9464, ls="--", color=INK, label="grid champion 24.95")
ax.set_xlabel("Nif (cm⁻²)"); ax.set_ylabel("PCE (%)")
ax.set_title("104-run exploratory search: nothing guardrailed beats the grid")
ax.legend(fontsize=10); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(OUT / "optimizer.png", dpi=300)

# 6. gap-step waterfall
steps = ["1.65\n23.84", "1.68\n22.70", "1.70\n22.51", "1.72\n21.59"]
vals = [23.8365, 22.7025, 22.5141, 21.5882]
fig, ax = plt.subplots(figsize=(8, 5.2))
ax.plot(steps, vals, "o-", color="black", ms=9)
for i, v in enumerate(vals):
    ax.annotate("", xy=(i + 0.97, vals[i + 1]), xytext=(i + 0.97, v),
                arrowprops=dict(arrowstyle="<->", color=ACC, lw=1.6)) if i < 3 else None
ax.set_ylabel("PCE (%)"); ax.set_title("Attainable gaps: non-monotonic steps map the Ea landscape")
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(OUT / "gap_steps.png", dpi=300)
print("deck figs done:", sorted(p.name for p in OUT.glob("*.png")))
