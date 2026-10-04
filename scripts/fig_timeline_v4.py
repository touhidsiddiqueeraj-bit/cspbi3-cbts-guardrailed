import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# v4: hand-placed data-coordinate labels; serif to match Times body
FIG = '/home/touhid/Documents/leadpaper/outputs/figs/'
plt.rcParams.update({'font.family': 'serif', 'font.size': 10,
                     'axes.labelsize': 11, 'xtick.labelsize': 9,
                     'ytick.labelsize': 9, 'legend.fontsize': 9})
exp = [(2016, 10.8), (2017, 17.0), (2018, 15.1), (2019, 18.4),
       (2025, 22.05), (2026, 21.71), (2026.2, 22.60), (2026.35, 21.43)]
sim = [(2022, 17.9), (2023, 19.06), (2023.15, 24.24),
       (2025, 24.17), (2026, 23.10), (2026.5, 23.49)]
fig, ax = plt.subplots(figsize=(8.2, 4.8))
ax.scatter([e[0] for e in exp], [e[1] for e in exp], s=60, marker='s',
           color='black', label='Experiment', zorder=3)
ax.scatter([s[0] for s in sim], [s[1] for s in sim], s=60, facecolors='none',
           edgecolors='tab:blue', linewidths=1.4, label='SCAPS-1D', zorder=3)
AR = dict(arrowstyle='-', color='0.5', lw=0.6, shrinkB=4)
ax.annotate('Swarnkar 10.8', (2016, 10.8), textcoords='offset points',
            xytext=(12, 4), fontsize=8.5, arrowprops=AR)
ax.annotate('Frolova 17.0', (2017, 17.0), textcoords='offset points',
            xytext=(12, 4), fontsize=8.5, arrowprops=AR)
ax.annotate('Wang 18.4', (2019, 18.4), textcoords='offset points',
            xytext=(12, 4), fontsize=8.5, arrowprops=AR)
ax.annotate('Oyedele* 24.24', (2023.15, 24.24), xytext=(2020.9, 25.4),
            fontsize=8.5, arrowprops=AR)
ax.annotate('Qiu 22.05', (2025, 22.05), xytext=(2023.1, 23.4),
            fontsize=8.5, arrowprops=AR)
ax.annotate('Zhang 21.71', (2026, 21.71), xytext=(2023.9, 19.9),
            fontsize=8.5, arrowprops=AR)
ax.annotate('Dai lab 22.60', (2026.2, 22.60), xytext=(2027.2, 20.6),
            fontsize=8.5, arrowprops=AR)
ax.annotate('Hu 21.43', (2026.35, 21.43), xytext=(2027.2, 22.4),
            fontsize=8.5, arrowprops=AR)
ax.annotate('This work 23.49', (2026.5, 23.49), xytext=(2027.2, 24.0),
            fontsize=8.5, arrowprops=AR)
ax.axhline(22.02, ls='--', color='0.45', lw=1)
ax.text(2015.8, 22.25, '22.02% certified', va='bottom', fontsize=8.5, color='0.3')
ax.set_xlabel('Year'); ax.set_ylabel('PCE (%)')
ax.set_xlim(2015.5, 2029.5); ax.set_ylim(8, 26.5)
ax.set_title('CsPbI3 record race (* = no interface layers)', pad=10)
ax.legend(loc='upper left', borderpad=0.6)
fig.tight_layout(); fig.savefig(FIG + 'fig_timeline.png', dpi=150)
print('timeline v4 done')
