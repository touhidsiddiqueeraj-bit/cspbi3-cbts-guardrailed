"""Fig 4 redraw: no label/rule collisions, labels offset clear of band edges."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
FIG = '/home/touhid/Documents/leadpaper/outputs/figs/'
plt.rcParams.update({'font.family': 'serif', 'font.size': 10})

fig, ax = plt.subplots(figsize=(8.4, 4.9))
blocks = [("ITO\n(front)", -4.00, -7.50, "C0"), ("TiO2\nETL", -3.80, -7.00, "C1"),
          ("CsPbI3\nabsorber", -3.928, -5.578, "C2"), ("CBTS\nHTL", -3.60, -5.50, "C3")]
for i, (lab, cb, vb, c) in enumerate(blocks):
    ax.fill_between([i - 0.3, i + 0.3], [cb, cb], [vb, vb], color=c, alpha=0.18, zorder=1)
    ax.plot([i - 0.3, i + 0.3], [cb, cb], color=c, lw=2.5, zorder=3)
    ax.plot([i - 0.3, i + 0.3], [vb, vb], color="red", lw=2.5, zorder=3)
    # value labels: CB above its line, VB below its line (clear of the rule)
    ax.text(i - 0.34, cb + 0.06, f"{cb:.2f}", ha="left", va="bottom", fontsize=8.5,
            color=c, zorder=4, bbox=dict(fc="white", ec="none", pad=0.6))
    ax.text(i - 0.34, vb - 0.06, f"{vb:.2f}", ha="left", va="top", fontsize=8.5,
            color="red", zorder=4, bbox=dict(fc="white", ec="none", pad=0.6))
    ax.text(i, -8.15, lab, ha="center", va="top", fontsize=9)

ax.plot([3.72, 4.28], [-5.5, -5.5], color="black", lw=2.5, zorder=3)
ax.text(4.0, -5.42, "Ni 5.5 eV", ha="center", va="bottom", fontsize=8.5, zorder=4,
        bbox=dict(fc="white", ec="none", pad=0.6))

# spike annotation drawn INSIDE the frame, between the two band tops
ax.annotate("", xy=(1.30, -3.80), xytext=(1.70, -3.928),
            arrowprops=dict(arrowstyle="<->", lw=1.2, color="black"), zorder=5)
ax.text(1.5, -3.62, "spike 0.13\n(raises $E_a$)", ha="center", va="bottom", fontsize=8.5, zorder=5,
        bbox=dict(fc="white", ec="0.7", pad=1.4, boxstyle="round,pad=0.25"))
ax.annotate("", xy=(2.30, -5.578), xytext=(2.70, -5.50),
            arrowprops=dict(arrowstyle="<->", lw=1.2, color="red"), zorder=5)
ax.text(2.5, -6.10, "offset 0.08\n(shallow, favourable)", ha="center", va="top", fontsize=8.5,
        color="red", zorder=5, bbox=dict(fc="white", ec="none", pad=0.6))

ax.set_xlim(-0.6, 4.6); ax.set_ylim(-8.7, -3.05)
ax.set_ylabel("Energy (eV, vacuum = 0)")
ax.set_xticks([])
ax.set_title("Adopted alignment: absorber CB 0.13 eV below ETL (spike),\n"
             "absorber VB 0.08 eV below HTL (shallow favourable offset)", pad=8)
fig.tight_layout(); fig.savefig(FIG + "fig_align.png", dpi=150)
print("fig_align v3 done")
