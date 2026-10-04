"""Fig 1 redraw: leader lines on every labelled point, no crossings, adopted value."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
FIG = '/home/touhid/Documents/leadpaper/outputs/figs/'
plt.rcParams.update({'font.family': 'serif', 'font.size': 10})

exp = [(2016, 10.8), (2017, 17.0), (2018, 15.1), (2019, 18.4),
       (2025, 22.05), (2026, 21.71), (2026.2, 22.60), (2026.35, 21.43)]
sim = [(2022, 17.9), (2023, 19.06), (2023.15, 24.24),
       (2025, 24.17), (2026, 23.10), (2026.5, 23.84)]
fig, ax = plt.subplots(figsize=(8.4, 5.0))
ax.scatter([e[0] for e in exp], [e[1] for e in exp], s=60, marker='s',
           color='black', label='Experiment', zorder=4)
ax.scatter([s[0] for s in sim], [s[1] for s in sim], s=60, facecolors='none',
           edgecolors='tab:blue', linewidths=1.4, label='SCAPS-1D', zorder=4)

# label, text position (data coords), for non-crossing placement
ann = {
 (2016, 10.8):  "Swarnkar 10.8", (2017, 17.0): "Frolova 17.0",
 (2019, 18.4):  "Wang 18.4",     (2025, 22.05): "Qiu 22.05",
 (2026, 21.71): "Zhang 21.71",   (2026.2, 22.60): "Dai lab 22.60",
 (2026.35, 21.43): "Hu 21.43",   (2023.15, 24.24): "Oyedele* 24.24",
 (2026.5, 23.84): "This work 23.84",
}
pos = {  # strictly separated rows, no leader crossings
 (2016, 10.8):  (2016.35, 11.6),  (2017, 17.0): (2017.35, 17.8),
 (2019, 18.4):  (2019.35, 19.2),  (2025, 22.05): (2023.05, 23.55),
 (2026, 21.71): (2023.75, 19.75),  (2026.2, 22.60): (2027.35, 20.45),
 (2026.35, 21.43): (2027.35, 22.35), (2023.15, 24.24): (2020.85, 25.45),
 (2026.5, 23.84): (2027.35, 23.95),
}
for (x, y), lab in ann.items():
    ax.annotate(lab, (x, y), xytext=pos[(x, y)], fontsize=8.5, zorder=5,
                arrowprops=dict(arrowstyle='-', color='0.55', lw=0.7, shrinkB=5),
                bbox=dict(fc='white', ec='none', pad=0.8))
ax.axhline(22.02, ls='--', color='0.45', lw=1, zorder=2)
ax.text(2015.7, 22.3, '22.02% certified', va='bottom', fontsize=8.5, color='0.3', zorder=5,
        bbox=dict(fc='white', ec='none', pad=0.8))
ax.set_xlabel('Year'); ax.set_ylabel('PCE (%)')
ax.set_xlim(2015.5, 2029.5); ax.set_ylim(8, 26.8)
ax.set_title('CsPbI3 record race (* = no interface layers)', pad=10)
ax.legend(loc='upper left', borderpad=0.6, framealpha=1.0)
fig.tight_layout(); fig.savefig(FIG + 'fig_timeline.png', dpi=150)
print('timeline v5 done')
