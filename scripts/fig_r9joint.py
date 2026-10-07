"""R9 figures: timeline star + defended value, real baseline JV,
joint-base QE/CV/EB/GR from s24 tables. Writes outputs/figs/."""
import json, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = pathlib.Path("/home/touhid/Documents/leadpaper-polish-r8")
FIG = BASE / "outputs" / "figs"
plt.rcParams.update({'font.family': 'serif', 'font.size': 11,
                     'axes.labelsize': 12, 'xtick.labelsize': 10,
                     'ytick.labelsize': 10, 'legend.fontsize': 10})


def main():
    # ---- timeline: own points starred/flagged, defended value shown ----
    exp = [(2016, 10.8), (2019, 18.4), (2024, 20.6),
           (2025, 22.05), (2026, 21.71), (2026.2, 22.60), (2026.35, 21.43)]
    sim = [(2022, 17.9), (2023, 19.06), (2023.15, 24.24),
           (2025, 24.17)]
    fig, ax = plt.subplots(figsize=(10.4, 5.6))
    import matplotlib.patches as mpatches
    ax.scatter([e[0] for e in exp], [e[1] for e in exp], s=70, marker='s',
               color='black', label='Experiment', zorder=3)
    ax.scatter([s[0] for s in sim], [s[1] for s in sim], s=70, facecolors='none',
               edgecolors='black', linewidths=1.6, label='SCAPS-1D', zorder=3)
    ax.scatter([2026.5], [24.95], s=140, marker='*', color='black', zorder=4)
    ax.fill_between([2026.3, 2026.7], [15.55, 15.55], [19.96, 19.96],
                    color='0.7', alpha=0.8, edgecolor='black', lw=1.0, zorder=2)
    AR = dict(arrowstyle='-', color='0.5', lw=0.8, shrinkB=4)
    for txt, xy, txy in [
            ('Swarnkar 10.8', (2016, 10.8), (12, 4)),
            ('Wang 18.4', (2019, 18.4), (12, 4)),
            ('Shah 20.6', (2024, 20.6), (12, 4))]:
        ax.annotate(txt, xy, textcoords='offset points', xytext=txy,
                    fontsize=10.5, arrowprops=AR)
    for txt, xy, txy in [
            ('Oyedele* 24.24', (2023.15, 24.24), (2019.7, 25.7)),
            ('Qiu 22.05', (2025, 22.05), (2021.4, 23.4)),
            ('Dai lab 22.60', (2026.2, 22.60), (2021.4, 22.4)),
            ('Zhang 21.71', (2026, 21.71), (2021.4, 21.5)),
            ('Hu 21.43', (2026.35, 21.43), (2021.4, 20.6))]:
        ax.annotate(txt, xy, xytext=txy, fontsize=11, arrowprops=AR)
    ax.annotate('This work: 24.95 box max', (2026.5, 24.95), xytext=(2021.4, 24.9),
                fontsize=11, weight='bold', arrowprops=AR)
    ax.annotate('15.6--20.0 routine-quality', (2026.5, 17.5), xytext=(2021.4, 17.0),
                fontsize=10, weight='bold', arrowprops=AR)
    ax.axhline(22.02, ls='--', color='0.45', lw=1.2)
    ax.text(2027.6, 22.25, '22.02% certified', va='bottom', fontsize=10.5, color='0.3')
    ax.set_xlabel('Year'); ax.set_ylabel('PCE (%)')
    ax.set_xlim(2015.5, 2030.5); ax.set_ylim(8, 26.5)
    import matplotlib.lines as mlines
    star = mlines.Line2D([], [], color='black', marker='*', ls='',
                         markersize=12, label='This work box max')
    band = mpatches.Patch(facecolor='0.7', alpha=0.8, edgecolor='black',
                           label='routine-quality 5--95%')
    h1, l1 = ax.get_legend_handles_labels()
    ax.legend(handles=list(h1) + [star, band], loc='upper left', borderpad=0.6)
    fig.tight_layout(); fig.savefig(FIG / 'fig_timeline.png', dpi=300)

    # ---- JV: real baseline curve + champion ----
    c = json.load(open(BASE / 'outputs' / 'newchamp_JV.json'))
    b = json.load(open(BASE / 'outputs' / 'baseline_JV.json'))
    d = c['deduced']
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    ax.plot(np.array(c['V']), -np.array(c['J']), color='black', lw=1.8,
            label=r"champion 2.2 $\mu$m, $E_g$ 1.65 eV (24.95%)")
    ax.plot(np.array(b['V']), -np.array(b['J']), color='0.5', lw=1.8, ls='--',
            label="baseline 800 nm (18.99%)")
    ax.set_xlabel('V (V)'); ax.set_ylabel('J (mA cm$^{-2}$)')
    ax.set_xlim(0, 1.35); ax.set_ylim(0, 25.5)
    ax.axhline(0, color='0.4', lw=0.8)
    ax.grid(alpha=0.3)
    ax.legend(loc='upper center', framealpha=1.0, fontsize=10, ncol=2)
    ax.set_title('Illuminated JV: baseline vs joint-optimum champion')
    fig.tight_layout(); fig.savefig(FIG / 'fig_JVboth.png', dpi=300)

    # ---- joint-base QE/CV/EB/GR from s24 ----
    s24 = json.load(open(BASE / 'outputs' / 's24_stack.json'))
    qe = s24['JQE_qe']['tables']['save_qe.txt']
    plt.figure()
    plt.plot(qe['lambda'], qe['QE'], color='black', lw=1.8, label='joint-optimum champion')
    # surveyed baseline QE for context (char.jsonl)
    char = {json.loads(l)['id']: json.loads(l) for l in
            open(BASE / 'outputs' / 'char.jsonl').read().splitlines() if l.strip()}
    qb = char['qe_base']['data']['table']
    plt.plot(qb['lambda'], qb['QE'], color='0.5', ls='--', lw=1.8, label='baseline 800 nm')
    plt.xlabel('Wavelength (nm)'); plt.ylabel('QE (%)'); plt.legend(); plt.grid(True)
    plt.title('Quantum efficiency: baseline vs joint-optimum champion')
    plt.savefig(FIG / 'fig_QE.png', dpi=300)

    cv = s24['JQE_cv']['tables']['save_cv.txt']
    V = np.array(cv['V']); Cc = np.array(cv['C'])
    cb = char['cv_base']['data']['table']
    Vb = np.array(cb['V']); Cb = np.array(cb['C'])
    fig, ax = plt.subplots(2, 1, figsize=(7.4, 7.0), sharex=True)
    ax[0].plot(V, Cc, color='black', lw=1.8, label='champion (joint base)')
    ax[0].plot(Vb, Cb, color='0.5', ls='--', lw=1.8, label='baseline')
    ax[1].plot(V, 1 / Cc ** 2, color='black', lw=1.8, label='champion (joint base)')
    ax[1].plot(Vb, 1 / Cb ** 2, color='0.5', ls='--', lw=1.8, label='baseline')
    ax[0].set(xlabel='V (V)', ylabel='C (nF/cm$^2$)')
    ax[1].set(xlabel='V (V)', ylabel='1/$C^2$ (cm$^4$/nF$^2$)')
    for a in ax: a.legend(); a.grid(True)
    fig.suptitle('C-V (1 MHz) and Mott-Schottky'); fig.savefig(FIG / 'fig_CV_MS.png', dpi=300)

    eb = s24['JQE_eb0']['tables']['save_eb.txt']
    x = np.array(eb['x_um'])
    plt.figure()
    for col, st in [('Ec', {'color': 'black', 'ls': '-'}),
                    ('Ev', {'color': 'black', 'ls': '--'}),
                    ('Fn', {'color': '0.5', 'ls': '-'}),
                    ('Fp', {'color': '0.5', 'ls': '--'})]:
        plt.plot(x, eb[col], label=col + ' (joint base)', lw=1.8, **st)
    plt.xlabel('x ($\\mu$m, 0 = back/CBTS)'); plt.ylabel('Energy (eV)')
    plt.legend(); plt.grid(True); plt.title('Champion band diagram @0V illuminated (joint affinities)')
    plt.savefig(FIG / 'fig_EB.png', dpi=300)
    plt.figure()
    plt.semilogy(x, eb['gen'], label='generation', color='black', lw=1.8)
    plt.semilogy(x, eb['rec'], label='recombination', color='black', ls='--', lw=1.8)
    plt.xlabel('x ($\\mu$m)'); plt.ylabel('rate (cm$^{-3}$ s$^{-1}$)'); plt.legend(); plt.grid(True)
    plt.title('Generation / recombination profiles @0V (joint base)')
    plt.savefig(FIG / 'fig_GR.png', dpi=300)
    print('r9 figs done')


if __name__ == '__main__':
    main()
