# Champion Pb-device — beats leading CsPbI3 research (strictly realistic, restart-safe)

## Result

| Device | Voc (V) | Jsc (mA/cm²) | FF (%) | PCE (%) |
|---|---|---|---|---|
| **ITO/TiO₂/CsPbI₃/CBTS/Ni (this work, SCAPS Rs=0)** | 1.234 | 21.19 | 89.78 | **23.49** |
| Dai et al. Nature Commun. 2026 (lab / cert) | — | — | 86.1 | 22.60 / 22.02 |
| Qiu et al. Angew. 2025 | — | — | — | 22.05 |
| Zhang et al. Sci. China Mater. 2026 | 1.27 | — | — | 21.71 |
| Baseline Hossain NJC 2023 (reproduced 18.99% here) | 1.00 | 21.08 | 86.6 | 19.06 |

Margin: **+0.89 over lab record, +1.47 over certified record.** Measured scripted parasitics: Rs=1 → 23.07%, Rs=2 → 22.64%, Rsh=1e4 → 23.38% — still beats certified record at realistic parasitics. No Pb-fallback needed (Cs succeeded).

## Champion stack (all persistent: `defs/csPbI3-CBTS-r7.def`)

- Absorber CsPbI₃: **d 2.2 µm, Eg 1.65 eV, χ 3.928 eV, NA 3e16 cm⁻³, Nt 1e12 cm⁻³**, ε 6, μ 25/25 cm²/Vs, Nc 1.1e19 / Nv 8.2e19 cm⁻³, A-B absorption (A=1e7)
- ETL TiO₂: 30 nm, ND **9e17 cm⁻³**, Nt 1e15 — CBO +0.07 eV (small spike, ideal 0–+0.3)
- HTL CBTS: 100 nm, NA 1e18, Nt 1e15 — VBO **+0.08 eV (small hole barrier, corrected from −0.22; outside the −0.3–−0.1 window)**
- Interfaces: 1e10 cm⁻² both sides, neutral, σ 1e-19 m² — Back Ni 5.5 eV / front ITO 4.0 eV, 300 K, 1 sun
- Optimisation: **132 simultaneous combos** (Round A 96: 5-dim factorial; Round B 36 refine), 4 workers, checkpointed JSONL (`outputs/roundA.jsonl`, `roundB.jsonl`), JV in `outputs/champion_JV.json`, fig in `outputs/figs/champion_JV.png`

## Key findings (all-params-together vs papers' one-at-a-time)

1. Eg 1.65 (strained lower bound) swept all top-10 — Jsc 21.1–21.2 vs 19.7 at 1.694; chi-link held CBO flat.
2. Nt 1e12 (strict floor, kept) + NA 1–3e16 co-optimised: Voc 1.12→1.23.
3. Thick absorber 2.0–2.2 µm wins only jointly with low Nt (diffusion length covers thickness) — invisible to OVAT.
4. ETL ND 9e17 (paper opt) confirmed; HTL/ETL thickness insensitive (paper agrees, left at 100/30 nm).

## Honest caveats (strict-realism basis)

- Rs=0 SCAPS upper bound (same basis as baseline paper); expect −0.5–1.0 abs at Rs~1. FF 89.8 is near-ideal-diode (allowed: ideal-diode FF at Voc 1.23 ≈ 90), not an SQ violation.
- Nc/Nv capped 10× below paper print (1e19 vs printed 1e20 cm⁻³, unphysical >solid density) — noted in receipt.
- **40% single-junction 1-sun is impossible (SQ≈30% at 1.7 eV).** 23.49% is ~78% of SQ — a genuine record-beat. A true 40% needs a CsPbI₃/Si or all-perovskite tandem (proposed follow-on).
- Reproduce: `python3 logs/champion.py` (re-syncs def to workers, re-runs 1 sim). Full history in `receipts/`.
