"""Regenerate 4 figures per visual-judge Round 1: JV scale, T dual-axis, CV fonts, audit 23.49."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = '/home/touhid/Documents/leadpaper'
FIG = BASE + '/outputs/figs/'
plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'xtick.labelsize': 10,
                     'ytick.labelsize': 10, 'legend.fontsize': 10})

# 1. champion JV: physical window, conventional +J
d = json.load(open(BASE + '/outputs/champion_JV.json'))
V = np.array(d['V']); J = -np.array(d['J'])
m = (V >= 0) & (V <= 1.32) & (J >= 0) & (J <= 23)
plt.figure(figsize=(6.4, 4.6))
plt.plot(V[m], J[m], lw=2)
plt.xlabel('Voltage (V)'); plt.ylabel('Current density (mA/cm2)')
plt.title('Champion JV: 23.49% (Voc 1.234 V, Jsc 21.19 mA/cm2, FF 89.78%)')
plt.grid(True); plt.xlim(0, 1.35); plt.ylim(0, 23)
plt.savefig(FIG + 'champion_JV.png', dpi=110)

# 2. T dual-axis
T = [275, 300, 350, 400, 475]
ch = {json.loads(l)['id']: json.loads(l) for l in
      open(BASE + '/outputs/char.jsonl') if l.strip()}
fig, ax1 = plt.subplots(figsize=(6.4, 4.4))
ax1.set_xlabel('Temperature (K)')
ax1.set_ylabel('PCE (%)', color='tab:blue')
ax1.plot(T, [ch[f'T{t}']['data']['deduced']['eta'] for t in T], 'o-', color='tab:blue', label='PCE')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax2 = ax1.twinx()
ax2.set_ylabel('Voc (V)', color='tab:red')
ax2.plot(T, [ch[f'T{t}']['data']['deduced']['Voc'] for t in T], 's-', color='tab:red', label='Voc')
ax2.tick_params(axis='y', labelcolor='tab:red')
plt.title('Temperature dependence (champion, 1 sun)')
fig.tight_layout(); plt.savefig(FIG + 'fig_T.png', dpi=110)

# 3. CV stacked, big fonts
fig, ax = plt.subplots(2, 1, figsize=(6.4, 6), sharex=True)
for k, lab in [('cv_base', 'baseline'), ('cv_champ', 'champion')]:
    dd = ch[k]['data']['table']
    Vv = np.array(dd['V']); Cc = np.array(dd['C'])
    ax[0].plot(Vv, Cc, 'o-', ms=4, label=lab)
    ax[1].plot(Vv, 1 / Cc ** 2, 'o-', ms=4, label=lab)
ax[1].set_xlabel('Bias voltage (V)')
ax[0].set_ylabel('C (nF/cm2)'); ax[1].set_ylabel('1/C2 (cm4/nF2)')
for a in ax: a.legend(); a.grid(True)
fig.suptitle('C-V (1 MHz) and Mott-Schottky')
fig.tight_layout(); plt.savefig(FIG + 'fig_CV_MS.png', dpi=110)

# 4. audit with unified 23.49 champ
pairs = [('th1.5', 23.40, 24.87), ('th2.0', 23.47, 24.73), ('champ', 23.49, 25.16)]
X = np.arange(len(pairs))
plt.figure(figsize=(6.4, 4.4))
plt.bar(X - 0.2, [p[1] for p in pairs], 0.4, label='interfaces ON (strict)')
plt.bar(X + 0.2, [p[2] for p in pairs], 0.4, label='interfaces OFF (literature-style)')
plt.xticks(X, [p[0] for p in pairs]); plt.ylabel('PCE (%)'); plt.legend(); plt.grid(True, axis='y')
plt.title('Guardrail audit: same cells, interfaces on/off')
plt.tight_layout(); plt.savefig(FIG + 'fig_audit.png', dpi=110)

# 5. analysis.json: archive honest 80/20 test split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
rows = []
for f in ['roundA.jsonl', 'roundB.jsonl']:
    for l in open(BASE + '/outputs/' + f):
        r = json.loads(l)
        if r.get('deduced') and r['deduced'].get('eta') is not None:
            p = r['params']
            rows.append([[p['layer2.thickness'], np.log10(p['layer2.NA']),
                          np.log10(p['layer2.defect1.Ntotal']),
                          np.log10(p.get('layer3.ND', 9e17)), p['layer2.Eg']],
                         r['deduced']['eta']])
Xa = np.array([r[0] for r in rows]); y = np.array([r[1] for r in rows])
Xtr, Xte, ytr, yte = train_test_split(Xa, y, test_size=0.2, random_state=0)
rf = RandomForestRegressor(n_estimators=300, random_state=0).fit(Xtr, ytr)
an = json.load(open(BASE + '/outputs/analysis.json'))
an['ML'] = {'n': len(rows), 'protocol': '80/20 split, seed 0',
            'R2_test': round(float(rf.score(Xte, yte)), 4),
            'R2_train': round(float(rf.score(Xtr, ytr)), 4),
            'importance': dict(zip(['thickness', 'logNA', 'logNt', 'logND_ETL', 'Eg'],
                               [round(float(v), 4) for v in rf.feature_importances_]))}
json.dump(an, open(BASE + '/outputs/analysis.json', 'w'), indent=1)
print('ML:', an['ML'])
print('figs done')
