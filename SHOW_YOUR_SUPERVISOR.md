# Show your supervisor: the 24.95% CsPbI3 cell in SCAPS

File: `defs/champion24p95.scaps`
(same champion cell as `defs/csPbI3-CBTS-champion24p95.def`, renamed to the extension you asked for — SCAPS loads it identically, verified at 24.9441%. Drop a copy in the SCAPS `def/` folder wherever SCAPS is installed)

## The 60-second demo

1. Open SCAPS-1D, **Load** this definition file.
2. Check the stack reads ITO / TiO2 / **2.2 µm CsPbI3** / CBTS / Ni.
3. Press **Calculate → Single shot** (AM1.5G, 300 K, Rs = 0 defaults).
4. Read the IV panel: **eta ≈ 24.94%**, Voc ≈ 1.321 V, Jsc ≈ 21.20 mA/cm²,
   FF ≈ 89.1%.

## What is baked in (nothing hidden in scripts)

| Parameter | Value | Source |
|---|---|---|
| Absorber thickness | 2.2 µm | Round-B optimum |
| Absorber NA | 3×10¹⁶ cm⁻³ | box ceiling |
| Absorber Nt | 10¹² cm⁻³ | box floor (τ ≈ 100 µs) |
| ETL ND | 9×10¹⁷ cm⁻³ | surveyed optimum |
| Eg / χ absorber | 1.65 / 3.928 eV | χ linked to Eg |
| χ CBTS / χ TiO2 | 3.9 / 3.7 eV | joint-optimum map (Table 5) |
| Interfaces, both sides | N = 10¹⁰ cm⁻², σ = 10⁻¹⁹ m² | guardrail floor |
| Contacts | ITO 4.0 eV / Ni 5.5 eV | surveyed |

## The honest footnote (read this if asked)

The batch receipt for this exact cell (`outputs/s22_jointIF.json`,
`J_if1e10_explicit`) is **24.9464%**. Loading the same numbers from a
definition file instead of script `set` commands gives **24.9441%**.
The 0.002-point gap is a file-parse vs script-set path difference inside
SCAPS, stable across repeated runs, and 7× smaller than the paper's own
0.017-point IV-step significance threshold — so both round consistently
with everything the paper claims. We report it here rather than round it
away.
