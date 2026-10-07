# Frozen priors for the s29 prior-predictive UQ (do not edit after runs start)

Frozen: 2026-10-07 (pre-registration for `scripts/s29_lhs.py`, seed 11).Held-fixed base: surveyed affinities (r7 def: χCBTS 3.6 / χTiO2 4.0),
Eg 1.70 eV with linked χ = 3.953 eV, NA 3e16 cm⁻³, ND_ETL 9e17 cm⁻³,
Et 0.6 eV mid-gap, σ = 1e-19 m² all defects, T 300 K, 1 sun.

| # | Factor | Prior | Source / rationale |
|---|---|---|---|
| 1 | log₁₀ Nt (cm⁻³) | U(13, 16) | routine films ~1e15; intrinsic point defects ~1e14 (Chem. Mater. 2025); floor 1e12 excluded here (priced separately), ceiling avoids degenerate doping |
| 2 | log₁₀ Nif (cm⁻²) | U(10, 13) | guardrail floor 1e10; extends to 1e13 where dose flattens at routine Nt (own s1/s6 data); both heterojunctions tied |
| 3 | log₁₀ Cr (cm³/s) | U(−11, −9) | literature bracket; top end pessimistic (no photon recycling); krad = 0 run separately as labelled sensitivity (8 runs), not in the interval |
| 4 | mobility scale | U(0.2, 1) × 25/25 | DFT range 5–10 e⁻ / 1–5 h cm²/Vs (Motta et al., Sci. Rep. 5, 12746); applied to absorber μn/μp |
| 5 | Rs (Ω·cm²) | U(0.5, 3) | above optimistic 0–2; ITO sheet resistance typically higher (own §9) |
| 6 | ITO WF (eV) | {4.0, 4.2, 4.4} categorical | archived def variants (r7, wfITO42, wfITO44); 4.7 excluded (collapse regime, priced separately) |
| 7 | Ni WF (eV) | {5.0, 5.2, 5.5} categorical | archived def variants (wfNi50, wfNi52, r7); joint-base cliff priced separately |
| 8 | absorber d (µm) | U(0.4, 1.5) | experimental film window (typical CsPbI3 0.5–0.7 µm); 2.2 µm excluded (upper-bound geometry) |

Design: N = 96 LHS (scipy.qmc.LatinHypercube, seed 11) + 8-run Cr = 0
sensitivity subset (seed 12). Report: median + 5–95% interval (asymmetric),
20k-bootstrap CIs on both percentiles, per-run Voc (≤1.418 V at 1.70 eV)
and Green-FF screens with flagged count, optical ±1.2 mA propagated
post-hoc (PCE ∝ Jsc) and labeled electrical-only otherwise. Crashes retried
(solo), never silently excluded. This is a prior-predictive interval under
stated priors, not a confidence interval on real devices.

## Amendment A (frozen 2026-10-07, pre-registration for `scripts/s32_lhs_dos.py`, seeds 13/14)

Adds factor 9: log₁₀ Nv (cm⁻³) ~ U(18.6, 19.9), i.e. hole mass m* 0.2–2.2
(Nv = 2.51e19 × m*^1.5); Nc fixed at 1.1e19. s29's eight factors and all
held-fixed settings unchanged. Interval reported both ways (with/without
the DOS dimension via post-stratification on the s29 archive and directly
from s32). Rationale: headline sensitivity to the DOS cap (26.50% at
physical DOS) makes DOS-conditional reporting mandatory.
