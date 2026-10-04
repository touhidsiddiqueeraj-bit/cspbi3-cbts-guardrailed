import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FIG = '/home/touhid/Documents/leadpaper/outputs/figs/'
plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'xtick.labelsize': 10,
                     'ytick.labelsize': 10, 'legend.fontsize': 10})

# 1. record timeline: experimental (black squares) + simulation (open circles)
exp = [(2016, 10.8, 'Swarnkar'), (2017, 17.0, 'Frolova'), (2018, 15.1, 'Wang'), (2019, 18.4, 'Wang'),
       (2025, 22.05, 'Qiu'), (2026, 21.71, 'Zhang'), (2026.2, 22.60, 'Dai lab'), (2026.3, 21.43, 'Hu cert.')]
sim = [(2021, 15.6, 'Jayan'), (2022, 17.9, 'Hossain'), (2023, 19.06, 'Hossain'), (2023, 24.24, 'Oyedele*'),
       (2025, 24.17, 'Nazli*'), (2026, 23.1, 'Ristiansyah'), (2026.5, 23.49, 'This work')]
plt.figure(figsize=(7, 4.6))
plt.scatter([e[0] for e in exp], [e[1] for e in exp], s=70, marker='s', color='black', label='Experiment')
plt.scatter([s[0] for s in sim], [s[1] for s in sim], s=70, facecolors='none', edgecolors='tab:blue', label='SCAPS-1D')
for x, y, lab in exp + sim:
    plt.annotate(lab, (x, y), textcoords='offset points', xytext=(4, 6), fontsize=8)
plt.axhline(22.02, ls='--', color='gray', label='22.02% certified record')
plt.xlabel('Year'); plt.ylabel('PCE (%)'); plt.legend(loc='upper left')
plt.title('CsPbI3 record race (* = no interface layers)')
plt.tight_layout(); plt.savefig(FIG + 'fig_timeline.png', dpi=110)

# 2. band alignment schematic from champion parameters
layers = [('ITO\n(front)', 4.0, 3.5), ('TiO2\nETL', 4.0, 3.2), ('CsPbI3\nabsorber', 3.928, 1.65),
          ('CBTS\nHTL', 3.6, 1.9), ('Ni\n(back)', None, None)]
plt.figure(figsize=(7, 4.6))
ax = plt.gca()
xpos = [0, 1, 2, 3, 4]
for i, (name, chi, eg) in enumerate(layers):
    if chi is None:
        wf = 5.5
        ax.plot([i - 0.4, i + 0.4], [-wf, -wf], color='black', lw=3)
        ax.text(i, -wf + 0.08, 'Ni 5.5 eV', ha='center', fontsize=10)
    else:
        cb, vb = -chi, -(chi + eg)
        ax.fill_between([i - 0.4, i + 0.4], [cb, cb], [vb, vb], alpha=0.25)
        ax.plot([i - 0.4, i + 0.4], [cb, cb], color='tab:blue', lw=2.5)
        ax.plot([i - 0.4, i + 0.4], [vb, vb], color='tab:red', lw=2.5)
        ax.text(i, cb + 0.1, f'{cb:.2f}', ha='center', fontsize=9, color='tab:blue')
        ax.text(i, vb - 0.18, f'{vb:.2f}', ha='center', fontsize=9, color='tab:red')
    ax.text(i, -7.9, name, ha='center', fontsize=10)
ax.annotate('', xy=(1.35, -4.0), xytext=(1.65, -3.95), arrowprops=dict(arrowstyle='<->'))
ax.text(1.5, -3.75, 'CBO +0.07', ha='center', fontsize=10)
ax.set_xlim(-0.6, 4.6); ax.set_ylim(-8.2, -1.5)
ax.set_xticks([]); ax.set_ylabel('Energy (eV, vacuum = 0)')
ax.set_title('Champion band alignment (CBO +0.07 eV, VBO -0.22 eV)')
plt.tight_layout(); plt.savefig(FIG + 'fig_align.png', dpi=110)
print('new figs done')
