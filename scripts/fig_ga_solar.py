"""Graphical abstract for Solar Energy submission (>=531x1328 px).

Left: headline result blocks (short lines only -- nothing may cross the
panel boundary). Right: scripted Rs sweep from real receipts
(outputs/s36_rs.json) bounding the fill-factor gap.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

Rs = [0, 1, 2, 3, 4, 5]
J_FF = [89.11, 87.57, 86.03, 84.50, 82.97, 81.45]
R_FF = [87.42, 85.70, 84.00, 82.32, 80.65, 78.99]

fig = plt.figure(figsize=(13.28, 5.31), dpi=100)
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.0], wspace=0.30,
                      left=0.05, right=0.97, top=0.88, bottom=0.13)

ax0 = fig.add_subplot(gs[0, 0])
ax0.set_xlim(0, 1)
ax0.set_ylim(0, 1)
ax0.axis("off")
X = 0.02
ax0.text(X, 0.96, "Modeling electrical losses", fontsize=15,
         fontweight="bold", va="top", ha="left")
ax0.text(X, 0.86, "in CsPbI3 solar cells", fontsize=15,
         fontweight="bold", va="top", ha="left")
ax0.text(X, 0.72, "Permissive-box ceiling", fontsize=17,
         fontweight="bold", va="top", ha="left", color="#1a5c1a")
ax0.text(X, 0.60, "24.95%", fontsize=26,
         fontweight="bold", va="top", ha="left", color="#1a5c1a")
ax0.text(X, 0.50, "2.2 \u03bcm, Nt 1e12 cm\u207b\u00b3,", fontsize=11,
         va="top", ha="left")
ax0.text(X, 0.43, "joint affinities", fontsize=11, va="top", ha="left")
ax0.text(X, 0.32, "Routine-quality envelope", fontsize=17,
         fontweight="bold", va="top", ha="left", color="#8a4b00")
ax0.text(X, 0.20, "18.0%  [15.6\u201320.0%]", fontsize=24,
         fontweight="bold", va="top", ha="left", color="#8a4b00")
ax0.text(X, 0.10, "96-run LHS prior volume", fontsize=11,
         va="top", ha="left")
ax0.text(X, 0.03, "records fall above it", fontsize=11,
         va="top", ha="left")

ax1 = fig.add_subplot(gs[0, 1])
ax1.plot(Rs, J_FF, "o-", label="Ceiling base FF")
ax1.plot(Rs, R_FF, "s--", label="Routine base FF")
ax1.axhspan(82, 84, color="0.85", label="Measured FF ~83%")
ax1.set_xlabel("Series resistance (\u03a9 cm\u00b2)", fontsize=12)
ax1.set_ylabel("Fill factor (%)", fontsize=12)
ax1.set_xticks(Rs)
ax1.set_title("Rs to 5 \u03a9cm\u00b2 closes ~half the FF gap",
              fontsize=13)
ax1.tick_params(labelsize=11)
ax1.legend(fontsize=10, loc="lower left")
ax1.grid(True, alpha=0.3)

fig.savefig("submission/solar-energy/graphical-abstract.png")
fig.savefig("submission/solar-energy/graphical-abstract.pdf")
print("saved")
