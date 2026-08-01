---
layout: post
title: "Calcein-containing Liposome Leakage Assay"
date: 2026-07-28
tags: [protocols, liposome]
mathjax: true
comments: true
---

## Foreword

Several common [fluorescent combinations](https://www.thermofisher.cn/cn/zh/home/references/molecular-probes-the-handbook/technical-notes-and-product-highlights/assays-of-volume-change-membrane-fusion-and-membrane-permeability.html?utm_source=chatgpt.com) can be used for the liposome leakage assay:
- ANTS / DPX
- Tb<sup>3+</sup> / DPA
- Fluorescein derivatives (e.g., calcein, carboxyfluorescein) (can be used in combination with divalent metal ions)

## Calcein Basics

- Calcein = fluorescein + iminodiacetic acid (a key moiety of EDTA), so calcein exhibits both fluorescence and chelating properties <sup class="ref-badge" title="Hausig-Punke, F. et al. Tracking the Endosomal Escape. Macromolecular Bioscience 22, 2200167 (2022)">ref</sup>
![calcein_synthesis.png](/assets/img/protocols/calcein-leakage/calcein_synthesis.png)
- Its excitation and emission spectra are shown [below](https://assets.thermofisher.cn/TFS-Assets/LSG/manuals/MAN0019058_CalceinAM_UG.pdf): excitation at 495 nm, emission at 515 nm.
![calcein_spectrum.png](/assets/img/protocols/calcein-leakage/calcein_spectrum.png)
- Calcein AM is a non-fluorescent, membrane-permeable variant that enters cells and is hydrolyzed by intracellular esterases, producing calcein.

### Factors Affecting Calcein Fluorescence
<sup class="ref-badge" title="Hausig-Punke, F. et al. Tracking the Endosomal Escape. Macromolecular Bioscience 22, 2200167 (2022)">ref</sup>
![influencing_factor_of_calcein_fluorescence.png](/assets/img/protocols/calcein-leakage/influencing_factor_of_calcein_fluorescence.png)

#### Concentration
- It is generally accepted that calcein is completely self-quenched at concentrations above ~70 mM (though different conditions and sources may report varying values) <sup class="ref-badge" title="Hausig-Punke, F. et al. Tracking the Endosomal Escape. Macromolecular Bioscience 22, 2200167 (2022)">ref</sup>
![calcein_quenching_concentration_table.png](/assets/img/protocols/calcein-leakage/calcein_quenching_concentration_table.png)
- The change in fluorescence intensity with concentration is shown in the figure below ([A](https://www.nature.com/articles/s41598-023-43813-4), [B](http://dx.doi.org/10.1023/a:1016832027325), [C](https://linkinghub.elsevier.com/retrieve/pii/S0731708598002295))
![calcein_fluorescence-intensity_vs_concentration.png](/assets/img/protocols/calcein-leakage/calcein_fluorescence-intensity_vs_concentration.png)

#### pH
The degree of pH-dependent change in fluorescence intensity: 6-carboxyfluorescein > calcein > sulforhodamine B.
Calcein maintains high fluorescence intensity over pH 4.5–10.

#### Cations
- Alkaline earth metal ions (Mg<sup>2+</sup>, Ca<sup>2+</sup>, etc.) enhance calcein fluorescence at alkaline pH, whereas at neutral pH they only affect the absorption spectrum without altering fluorescence intensity.
- Transition metal ions (Co<sup>2+</sup>, Ni<sup>2+</sup>, etc.) quench calcein fluorescence at neutral pH ([image source: ThermoFisher](https://www.thermofisher.cn/cn/zh/home/references/molecular-probes-the-handbook/indicators-for-ca2-mg2-zn2-and-other-metal-ions/fluorescent-indicators-for-zn2-and-other-metal-ions.html))
![calcein_quenched_by_metal-ions.png](/assets/img/protocols/calcein-leakage/calcein_quenched_by_metal-ions.png)
- At high pH, Na<sup>+</sup> ions increase fluorescence intensity, whereas K<sup>+</sup> has almost no effect on calcein fluorescence.

## Protocol

Overview <sup class="ref-badge" title="Hausig-Punke, F. et al. Tracking the Endosomal Escape. Macromolecular Bioscience 22, 2200167 (2022)">ref</sup>:
![calcein-containing_liposome_preparation.png](/assets/img/protocols/calcein-leakage/calcein-containing_liposome_preparation.png)

1. Dry the desired lipid components into a film under vacuum.
2. Add a solution containing ~70 mM calcein or 1 mM calcein + 1 mM Co<sup>2+</sup>, and vortex thoroughly until the lipid is fully dissolved.

<div class="callout callout-tip" markdown="1" style="background: #fffbeb; border-left: 4px solid #d97706; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #d97706;">💡 Preparing Calcein Stock Solution</p>
  - Calcein is strongly acidic and has very low solubility under acidic conditions; therefore, NaOH is needed to adjust the pH and increase solubility. A pH meter should be used to continuously monitor the pH during adjustment.
- <u>In the absence of a buffering system, diluting the calcein stock will cause a significant drop in pH.</u> If a stable pH is required, an excess of buffer species (e.g., HEPES, Tris) must be present.
</div>

3. (Optional: after vortexing, perform more than 5 freeze-thaw cycles, which is reported to improve the calcein encapsulation efficiency.) Use an extruder to pass the solution >20 times, or sonicate.

<div class="callout callout-note" markdown="1" style="background: #eff6ff; border-left: 4px solid #2563eb; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #2563eb;">💡 Extrusion vs. Sonication</p>
  Extrusion is the most common method and provides the best control over liposome size. However, some [literature](https://doi.org/10.3390/ma6083294) points out that due to shape relaxation, the size of extruded liposomes decreases significantly over time (on the order of days), and lipid fluidity drops markedly after 3 days; sonication does not suffer from this issue. The drawback of sonication, however, is that liposome size distribution is more difficult to control.
</div>

4. Prepare the external phase solution, keeping the internal and external phases approximately isosmotic ([~70 mM calcein is roughly isosmotic with 10 mM NaCl](https://www.sciencedirect.com/science/article/pii/S0006349522006063)). For Co<sup>2+</sup>-calcein-encapsulated liposomes, the external phase should contain 1 mM EDTA.
5. Use SEC, centrifugation, or ultrafiltration with the external phase buffer to separate free calcein or Co<sup>2+</sup>-calcein from the dye-loaded liposomes.

<div class="callout callout-note" markdown="1" style="background: #eff6ff; border-left: 4px solid #2563eb; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #2563eb;">💡 Comparison of Separation Methods</p>
  [Literature](http://www.doi.org/10.26538/tjnpr/v6i9.6) indicates that SEC loses about 40% of liposomes, whereas 1 kDa ultrafiltration loses almost none; ultrafiltration slightly reduces the mean liposome size.
</div>

6. Pilot experiment to determine the appropriate liposome dilution factor: Dilute the liposomes with external phase buffer at various factors, transfer to a 96-well plate (black, low binding), and measure the fluorescence before and after adding 0.2% (v/v) Triton X-100 using a plate reader. A suitable sample condition is when the signal after Triton addition is 4–5 times that before. Typically, the liposome concentration is in the range of **1–100 µg/mL**.
7. Pilot experiment to assess the effect of the protein/molecule of interest on fluorescence: Set up four control groups (without liposomes): <u>external phase buffer</u>, <u>external phase buffer + protein/molecule</u>, <u>external phase buffer + calcein/Co<sup>2+</sup>-calcein</u>, <u>external phase buffer + calcein/Co<sup>2+</sup>-calcein + protein/molecule</u>. Add 0.2% (v/v) Triton X-100 to all groups at the end. If significant signal shifts by protein/molecule are observed, consider optimizing the concentration, reducing the effect, or switching to another dye.
8. Formal experiment: At least three control groups per condition: <u>external phase buffer</u>, <u>external phase buffer + liposomes</u>, <u>external phase buffer + liposomes + protein/molecule</u>. Add 0.2% (v/v) Triton X-100 to all groups at the end.
9. Data processing: Normalize the fluorescence intensity. The initial fluorescence should be measured before protein/molecule addition. In some cases, noticable leakage can be observed immediately after protein/molecule addition. The maximum fluorescence can be taken from the external buffer + liposomes + Triton X-100 group, or from the external buffer + liposomes + protein/molecule + Triton X-100 group.

Reference protocols from selected publications:

|                                Reference                               |                                          Internal Phase                                           |                                          External Phase                                         |                     Liposome Preparation                     |                                        Separation Method                                       |
| :----------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------: | :-----------------------------------------------------------: | :--------------------------------------------------------------------------------------------: |
|              [a](https://bio-protocol.org/e3690)                 |                                         103 mM calcein                                          |                                                    -                                                     |                         extrusion                         |                                       Sephadex G-50 SEC                                       |
|    [b](https://www.tjnpr.org/index.php/home/article/view/1254)     |                                    HEPES pH 7.4<br>107 mM calcein                                    |                                     HEPES pH 7.4                                     | 5 cycles freeze–60°C thaw<br>sonication 30 min<br>extrusion 200 nm |                        Sephadex G-25 SEC<br>or<br>1 kDa ultrafiltration 4000 rpm, 15 min (total dilution: 4096)                        |
|        [c](https://doi.org/10.1074/jbc.M200429200)                 |                                        HBS<br>90 mM calcein                                         |                                         HBS                                         |                    extrusion 50–600 nm                    |                            100,000×g centrifugation, 1 mL, 45 min × 2                            |
|       [d](https://doi.org/10.1016/0005-2736(95)80035-E)          | 150 mM H<sub>2</sub>BO<sub>3</sub><br>pH 9<br>5 mM EDTA<br>5 mM KOH<br>20 mM NaCl<br>80 mM calcein | 150 mM H<sub>2</sub>BO<sub>3</sub><br>pH 9<br>5 mM EDTA<br>5 mM KOH<br>140 mM NaCl |                     extrusion 100 nm                      |                                       Sephadex G-50 SEC                                       |
|    [e](https://www.nature.com/articles/s41598-023-43813-4)       |                                       pH 7.7<br>30 mM calcein                                       |                               borate buffer<br>pH 8.5                                |           sonication 2 min<br>extrusion 200 nm            |                           3000 rpm centrifugation, 1 h, 1 mL                             |
|        [f](https://doi.org/10.1073/pnas.0606129103)              |                                            60 mM calcein                                            |                        10 mM HEPES<br>pH 7.4<br>150 mM NaCl                         |                                         -                                         |                                       Sephadex G-50 SEC                                       |
| [g](https://www.embopress.org/doi/full/10.1038/s44318-024-00190-6) |                                       pH 7.0<br>80 mM calcein                                       |                  20 mM HEPES<br>pH 7.0<br>140 mM NaCl<br>1 mM EDTA                  |                         extrusion                         |                                       Sephadex G-50 SEC                                       |
|    [h](https://www.nature.com/articles/s41467-023-39726-5)       |             50 mM phosphate buffer<br>pH 7.0<br>1 mM CoCl<sub>2</sub><br>0.8 mM calcein             |                   35 mM phosphate buffer<br>pH 7.0<br>10 mM EDTA                    |            5 cycles freeze–thaw<br>extrusion 400 nm             |                       Sephadex G-75 SEC<br>444,000×g centrifugation, 25 min                    |
|    [i](https://doi.org/10.1021/acsbiomedchemau.5c00084)          |                                       pH 7.4<br>80 mM calcein                                       |                 50 mM HEPES<br>pH 7.4<br>100 mM NaCl<br>0.3 mM EDTA                 |         3 cycles freeze–thaw<br>extrusion 100 nm          |                                       Sephadex G-50 SEC                                       |

## Additional Notes

### About DMSO
In liposome leakage assays where DMSO is used as part of the external phase, **controls with no DMSO are essential**. Based on my experience, 4% DMSO renders GUVs of DOPC impermeable to FITC (MW: 389 Da). [Literature](https://doi.org/10.3389/fmicb.2021.669709) indicates that DMSO ≤ 5% does not affect the liposome leakage induced by the peptides they studied.

### Estimating the Released Calcein Concentration

Assume that the total lipid concentration in solution is $C_{\text{lipid}}$, the encapsulated calcein concentration inside the liposomes is $C_0$, the solution volume is $V$, the average area occupied per lipid molecule is $A$, the mean liposome radius is $R$, and the final calcein concentration after complete release is $C_f$. Then

$$
\begin{align}
C_f &= C_0 \cdot N_{\text{liposome}} \cdot \frac{4}{3}\pi R^3 / V \\
&= C_0 \cdot \frac{N_A \, C_{\text{lipid}} \, V}{2 \cdot 4\pi R^2 / A} \cdot \frac{\frac{4}{3}\pi R^3}{V} \\
&= C_0 \cdot \frac{1}{6} N_A \, C_{\text{lipid}} \, A \, R \tag{1}
\end{align}
$$

[It is reported](https://doi.org/10.1016/j.bbamem.2012.05.006) that $A \approx 0.6~\mathrm{nm}^2$. Let

$$
C_{\text{lipid}} = x~\mathrm{mM}, \quad C_0 = y~\mathrm{mM}, \quad R = r \times 10^2~\mathrm{nm}
$$

Substituting into equation (1):

$$
\begin{align}
C_f &= y~\mathrm{mM} \cdot \frac{1}{6} \cdot 6.02 \times 10^{23} \cdot x \times 10^{-3}~\mathrm{mol/L} \cdot 0.6 \times 10^{-16}~\mathrm{dm}^2 \cdot r \times 10^{-6}~\mathrm{dm} \\
&= 6.02 \times 10^{-3} \cdot x \cdot y \cdot r~\mathrm{mM}
\end{align}
$$
