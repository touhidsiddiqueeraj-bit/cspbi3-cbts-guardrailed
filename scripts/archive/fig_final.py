import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FIG = '/home/touhid/Documents/leadpaper/outputs/figs/'
plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'xtick.labelsize': 10,
                     'ytick.labelsize': 10, 'legend.fontsize': 10})

# timeline: aggressive stagger, leader lines
exp = [(2016, 10.8, 'Swarnkar'), (2017, 17.0, 'Frolova'), (2018, 15.1, 'Wang'),
       (2019, 18.4, 'Wang'), (2025, 22.05, 'Qiu'), (2026, 21.71, 'Zhang'),
       (2026.2, 22.60, 'Dai lab'), (2026.35, 21.43, 'Hu cert.')]
sim = [(2021, 15.6, 'Jayan'), (2022, 17.9, 'Hossain'), (2023, 19.06, 'Hossain'),
       (2023.15, 24.24, 'Oyedele*'), (2025, 24.17, 'Nazli*'), (2026, 23.1, 'Ristiansyah'),
       (2026.5, 23.49, 'This work')]
plt.figure(figsize=(7.4, 4.8))
plt.scatter([e[0] for e in exp], [e[1] for e in exp], s=70, marker='s', color='black', label='Experiment')
plt.scatter([s[0] for s in sim], [s[1] for s in sim], s=70, facecolors='none', edgecolors='tab:blue', label='SCAPS-1D')
offs = {'Swarnkar': (6, 8), 'Frolova': (6, -16), 'Wang': (6, 8), 'Qiu': (-40, 10), 'Zhang': (-36, 10),
        'Dai lab': (6, 10), 'Hu cert.': (10, -24), 'Jayan': (6, 8), 'Hossain': (6, -16),
        'Oyedele*': (6, 10), 'Nazli*': (-46, -16), 'Ristiansyah': (-52, 8), 'This work': (6, 8)}
for x, y, lab in exp + sim:
    plt.annotate(lab, (x, y), textcoords='offset points', xytext=offs[lab], fontsize=8,
                 arrowprops=dict(arrowstyle='-', lw=0.6, color='gray'))
plt.axhline(22.02, ls='--', color='gray', label='22.02% certified record')
plt.xlabel('Year'); plt.ylabel('PCE (%)'); plt.legend(loc='upper left')
plt.xlim(2015.5, 2029.0); plt.ylim(8, 26.5)
plt.title('CsPbI3 record race (* = no interface layers)')
plt.tight_layout(); plt.savefig(FIG + 'fig_timeline.png', dpi=110)

# align: names on top (already), keep
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
ax.text(1.0, -3.68, 'CBO +0.07', ha='center', fontsize=10)
ax.set_xlim(-0.6, 4.6); ax.set_ylim(-8.2, -1.2)
ax.set_xticks([]); ax.set_ylabel('Energy (eV, vacuum = 0)')
ax.set_title('Champion band alignment (CBO +0.07 eV, VBO -0.22 eV)')
plt.tight_layout(); plt.savefig(FIG + 'fig_align.png', dpi=110)

# audit: legend below axes
pairs = [('th1.5', 23.40, 24.87), ('th2.0', 23.47, 24.73), ('champ', 23.49, 25.16)]
X = list(range(len(pairs)))
plt.figure(figsize=(6.6, 4.8))
plt.bar([x - 0.2 for x in X], [p[1] for p in pairs], 0.4, label='interfaces ON (strict)')
plt.bar([x + 0.2 for x in X], [p[2] for p in pairs], 0.4, label='interfaces OFF (literature-style)')
plt.xticks(X, [p[0] for p in pairs]); plt.ylabel('PCE (%)')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.14), ncol=2)
plt.grid(True, axis='y')
plt.title('Guardrail audit: same cells, interfaces on/off')
plt.tight_layout(); plt.savefig(FIG + 'fig_audit.png', dpi=110)
print('figs final done')
