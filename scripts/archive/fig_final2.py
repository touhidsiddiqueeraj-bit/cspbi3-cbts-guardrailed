import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FIG = '/home/touhid/Documents/leadpaper/outputs/figs/'
plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'xtick.labelsize': 10,
                     'ytick.labelsize': 10, 'legend.fontsize': 9})

exp = [(2016, 10.8, 'Swarnkar'), (2017, 17.0, 'Frolova'), (2018, 15.1, 'Wang'),
       (2019, 18.4, 'Wang'), (2025, 22.05, 'Qiu'), (2026, 21.71, 'Zhang'),
       (2026.2, 22.60, 'Dai lab'), (2026.35, 21.43, 'Hu cert.')]
sim = [(2021, 15.6, 'Jayan'), (2022, 17.9, 'Hossain'), (2023, 19.06, 'Hossain'),
       (2023.15, 24.24, 'Oyedele*'), (2025, 24.17, 'Nazli*'), (2026, 23.1, 'Ristiansyah'),
       (2026.5, 23.49, 'This work')]
fig, ax = plt.subplots(figsize=(7.4, 4.8))
ax.scatter([e[0] for e in exp], [e[1] for e in exp], s=70, marker='s', color='black', label='Experiment')
ax.scatter([s[0] for s in sim], [s[1] for s in sim], s=70, facecolors='none', edgecolors='tab:blue', label='SCAPS-1D')
main_lab = {'Swarnkar': (6, 8), 'Frolova': (6, 8), 'Wang': (6, 8), 'Qiu': (6, 8),
            'Dai lab': (6, 8), 'Jayan': (6, 8), 'Hossain': (6, -16), 'This work': (6, 8)}
for x, y, lab in exp + sim:
    if lab in main_lab:
        ax.annotate(lab, (x, y), textcoords='offset points', xytext=main_lab[lab], fontsize=9)
ax.axhline(22.02, ls='--', color='gray')
ax.set_xlabel('Year'); ax.set_ylabel('PCE (%)')
ax.set_xlim(2015.5, 2029.0); ax.set_ylim(8, 26.5)
ax.set_title('CsPbI3 record race (* = no interface layers)')

ins = fig.add_axes((0.52, 0.52, 0.43, 0.40))
ins.scatter([e[0] for e in exp if e[0] >= 2024.5], [e[1] for e in exp if e[0] >= 2024.5],
            s=45, marker='s', color='black')
ins.scatter([s[0] for s in sim if s[0] >= 2024.5], [s[1] for s in sim if s[0] >= 2024.5],
            s=45, facecolors='none', edgecolors='tab:blue')
in_offs = {'Qiu': (-30, 6), 'Zhang': (-36, -14), 'Dai lab': (6, 6), 'Hu cert.': (8, -14),
           'Nazli*': (-40, 4), 'Ristiansyah': (6, -14), 'This work': (6, 6)}
for x, y, lab in exp + sim:
    if x >= 2024.5 and lab in in_offs:
        ins.annotate(lab, (x, y), textcoords='offset points', xytext=in_offs[lab], fontsize=8,
                     arrowprops=dict(arrowstyle='-', lw=0.6, color='gray'))
ins.axhline(22.02, ls='--', color='gray', lw=0.8)
ins.set_xlim(2024.4, 2026.9); ins.set_ylim(20.8, 25.0)
ins.set_title('2025-2026 cluster', fontsize=9)
fig.legend(loc='upper left', bbox_to_anchor=(0.08, 0.94),
           labels=['Experiment', 'SCAPS-1D', '22.02% certified record'])
fig.tight_layout(); plt.savefig(FIG + 'fig_timeline.png', dpi=110)

# align: CBO callout above arrow
layers = [('ITO\n(front)', 4.0, 3.5), ('TiO2\nETL', 4.0, 3.2), ('CsPbI3\nabsorber', 3.928, 1.65),
          ('CBTS\nHTL', 3.6, 1.9)]
plt.figure(figsize=(7.2, 4.8))
ax = plt.gca()
for i, (name, chi, eg) in enumerate(layers):
    cb, vb = -chi, -(chi + eg)
    ax.fill_between([i - 0.4, i + 0.4], [cb, cb], [vb, vb], alpha=0.25)
    ax.plot([i - 0.4, i + 0.4], [cb, cb], color='tab:blue', lw=2.5)
    ax.plot([i - 0.4, i + 0.4], [vb, vb], color='tab:red', lw=2.5)
    ax.text(i, cb + 0.12, f'{cb:.2f}', ha='center', fontsize=10, color='tab:blue')
    ax.text(i, vb - 0.22, f'{vb:.2f}', ha='center', fontsize=10, color='tab:red')
    ax.text(i, -1.75, name, ha='center', fontsize=11)
ax.plot([3.6, 4.4], [-5.5, -5.5], color='black', lw=3)
ax.text(4.0, -5.3, 'Ni 5.5 eV', ha='center', fontsize=10)
ax.annotate('', xy=(0.82, -4.0), xytext=(1.18, -3.93), arrowprops=dict(arrowstyle='<->'))
ax.text(1.0, -3.45, 'CBO +0.07', ha='center', fontsize=11,
        bbox=dict(facecolor='white', edgecolor='none', pad=1))
ax.set_xlim(-0.6, 4.6); ax.set_ylim(-8.2, -1.2)
ax.set_xticks([]); ax.set_ylabel('Energy (eV, vacuum = 0)')
ax.set_title('Champion band alignment (CBO +0.07 eV, VBO -0.22 eV)')
plt.tight_layout(); plt.savefig(FIG + 'fig_align.png', dpi=110)
print('figs v2 done')
