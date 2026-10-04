# SCAPS-1D 3.3.10 unit map — MEASURED on csPbI3-CBTS-r7.def (2026-10-04)
Diag: `set layer2.NA 1e15` reproduces file baseline exactly (19.00%); file stores 1e21 /m³.
Conclusion: **`set` uses practical units, file stores SI.** Skill's blanket "`set` uses /m³" is wrong for this build.

| Param | `set` unit (use this) | File unit | Example: paper → set value |
|---|---|---|---|
| layer.thickness | µm | m | 1500 nm → `1.5` |
| layer.NA / layer.ND | cm⁻³ | /m³ | abs NA 1e16 cm⁻³ → `1e16`; ETL ND 9e17 → `9e17`; HTL NA 1e18 → `1e18` |
| layer.defect1.Ntotal | cm⁻³ | /m³ | abs Nt 1e12 cm⁻³ → `1e12` |
| interface.IFdefect.Ntotal (when blocks exist) | cm⁻² (to verify) | /m² | 1e10 cm⁻² → `1e10` |
| layer.mun / mup | cm²/Vs (assumed, verify before sweeping) | m²/Vs | 25 → `25` (DO NOT sweep until verified) |
| layer.Nc / Nv | cm⁻³ (assumed, verify) | /m³ | 1e19 → `1e19` (DO NOT sweep until verified) |
| layer.Eg / chi | eV | eV | Eg 1.694 |
| workingpoint.temperature | K | — | 300 |
| illumination | % of 100mW/cm² (100 = 1 sun) | — | 100 |

Artefact rule: NA ≥1e21 cm⁻³ or Nt ≤1e11 cm⁻³ → degenerate/unphysical (Voc>Eg/q, FF>88%) → reject.
Strict-realism sweep windows (set units): abs d 0.4–2.2; NA 1e15–1e17; Nt 1e12–1e15;
ETL ND 1e16–1e19, d 0.02–0.09; HTL NA 1e17–1e19, d 0.05–0.2; Eg 1.65–1.75 + chi link.
