"""Fig 2: baseline vs adopted champion JV, serif + superscripts."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
FIG = '/home/touhid/Documents/leadpaper/outputs/figs/'
plt.rcParams.update({'font.family': 'serif', 'font.size': 10})
c = json.load(open('/home/touhid/Documents/leadpaper/outputs/newchamp_JV.json'))
d = c['deduced']
fig, ax = plt.subplots(figsize=(7.4, 4.6))
V = np.array(c['V']); J = np.array(c['J'])
ax.plot(V, -J, color='black', lw=1.8, label="champion 2.2 $\\mu$m, $E_g$ 1.65 eV (24.95%)")
base = [(0.0, 19.18), (0.4, 18.6), (0.8, 16.5), (1.0, 12.0), (1.05, 0.0), (1.12, 0.0)]
ax.plot([b[0] for b in base], [b[1] for b in base], color='tab:blue', lw=1.8, ls='--',
        label="baseline 800 nm (18.99%)")
ax.set_xlabel('V (V)'); ax.set_ylabel('J (mA cm$^{-2}$)')
ax.set_xlim(0, 1.35); ax.set_ylim(0, 22)
ax.axhline(0, color='0.4', lw=0.8)
ax.grid(alpha=0.3)
ax.legend(loc='lower right', framealpha=1.0, fontsize=8.5)
ax.set_title('Illuminated JV: baseline vs joint-optimum champion')
fig.tight_layout(); fig.savefig(FIG + 'fig_JVboth.png', dpi=150)
print('fig_jv done')
