import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FIG = '/home/touhid/Documents/leadpaper/outputs/figs/'
plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'xtick.labelsize': 10,
                     'ytick.labelsize': 10, 'legend.fontsize': 9})

# NO inset: sparse labels only, everything else lives in Table 1
exp = [(2016, 10.8, 'Swarnkar'), (2017, 17.0, 'Frolova'), (2019, 18.4, 'Wang 18.4'),
       (2025, 22.05, 'Qiu 22.05'), (2026.2, 22.60, 'Dai lab 22.60')]
sim = [(2021, 15.6, None), (2022, 17.9, None), (2023, 19.06, None),
       (2023.15, 24.24, 'Oyedele* 24.24'), (2025, 24.17, None), (2026, 23.1, None),
       (2026.5, 23.49, 'This work 23.49')]
exp2 = [(2018, 15.1, None), (2026, 21.71, 'Zhang 21.71'), (2026.35, 21.43, 'Hu 21.43')]
plt.figure(figsize=(7.4, 4.6))
ax = plt.gca()
ax.scatter([e[0] for e in exp + exp2], [e[1] for e in exp + exp2], s=70, marker='s',
           color='black', label='Experiment', zorder=3)
ax.scatter([s[0] for s in sim], [s[1] for s in sim], s=70, facecolors='none',
           edgecolors='tab:blue', label='SCAPS-1D', zorder=3)
offs = {'Swarnkar': (6, 8), 'Frolova': (6, 8), 'Wang 18.4': (6, 8), 'Qiu 22.05': (-64, -18),
        'Dai lab 22.60': (8, -18), 'Zhang 21.71': (-70, 4), 'Hu 21.43': (8, -18),
        'Oyedele* 24.24': (8, 6), 'This work 23.49': (8, 6)}
for x, y, lab in exp + exp2 + sim:
    if lab is None:
        continue
    ax.annotate(lab, (x, y), textcoords='offset points', xytext=offs[lab], fontsize=9)
ax.axhline(22.02, ls='--', color='gray')
ax.text(2028.3, 22.02, '22.02% certified', va='center', fontsize=9, color='gray')
ax.set_xlabel('Year'); ax.set_ylabel('PCE (%)')
ax.set_xlim(2015.5, 2029.5); ax.set_ylim(8, 26.5)
ax.set_title('CsPbI3 record race (* = no interface layers)', pad=10)
ax.legend(loc='upper left', borderpad=0.6)
plt.tight_layout(); plt.savefig(FIG + 'fig_timeline.png', dpi=110)
print('timeline clean done')
