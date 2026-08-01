---
layout: post
title: "PeakForce Tapping AFM"
date: 2026-07-28
tags: [protocols, AFM]
mathjax: true
comments: true
---
 
## Tip Selection

- The spring constant \($k$\) should be close to or greater than the "stiffness" corresponding to the sample modulus, so that the tip can deform the sample surface.
    - For biological samples, typically choose 0.01–0.5 N/m <sup class="ref-badge" title="Dufrene & Muller, Nat. Methods (2013)">ref</sup>
    - For biological samples with unknown modulus, start with ~0.1 N/m <sup class="ref-badge" title="Alice Pyne & Muller, Nat. Protoc (2014)">ref</sup>
- The resonance frequency in liquid \($f$\) (typically ~1/3 of that in air) must be significantly higher than the operating frequency of the PeakForce tapping (PFT) mode (1–2 kHz) <sup class="ref-badge" title="Dufrene & Muller, Nat. Methods (2013)">ref</sup>, to avoid excitation of the cantilever near its resonance during operation, which would cause inertia effects and hydrodynamic drag that degrade imaging quality.
    - Since $Q \sim f/\Delta f$, a low Q-factor means $\Delta f$ is large, so the cantilever can still be excited even at frequencies far from resonance.
    - For high-speed imaging, cantilevers with $f$ > 100 kHz are required.
- Force sensitivity should be as high as possible, but there is a tradeoff: high force sensitivity typically corresponds to a high Q-factor, and a high Q-factor is unfavorable for fast imaging <sup class="ref-badge" title="Dufrene & Muller, Nat. Methods (2013)">ref</sup>.
- Tips with a metal coating may exhibit larger drift, affecting the accuracy of force control.
- **Blunt tips typically do not become sharper, but sharp tips gradually become sharper** <sup class="ref-badge" title="Muller, Nat. Protoc (2014)">ref</sup>.
    - In any case, achieving high-resolution FD-based AFM topographs and images takes patience. The operator **needs to wait for the stylus to get sufficiently sharp** to contour structural details of the proteins. <sup class="ref-badge" title="Muller, Nat. Protoc (2014)">ref</sup>
- Tips from the same batch may share the same contamination profile. If one encounters a poor tip, try a different batch.

## Tip Calibration

- Before and after scanning, or after changing the laser alignment, calibrate the deflection sensitivity using a hard substrate (e.g., mica, glass).

<div class="callout callout-tip" markdown="1" style="background: #eff6ff; border-left: 4px solid #2563eb; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
<p style="margin: 0 0 8px 0; font-weight: 600; color: #2563eb;">💡 Measuring Sensitivity</p>
The so-called deflection sensitivity is also referred to as z scan sensitivity.
- For z scan sensitivity: use Ramp mode, set trigger mode to "relative" and trig threshold to &lt;0.5 V.
- For PeakForce QNM, also calibrate the Drive3 Amplitude Sensitivity (see Bruker AFM manual for the calibration procedure).
- If Drive3 is set correctly, the amplitude of the height sensor in high-speed capture should match the set PeakForce amplitude.
</div>

<div class="callout callout-note" markdown="1" style="background: #fffbeb; border-left: 4px solid #d97706; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
<p style="margin: 0 0 8px 0; font-weight: 600; color: #d97706;">🔎 Tip Deflection Sensitivity Changes During Scanning</p>
Possible causes:
- Thermal drift shifting the laser spot position.
- Changes in tip reflectivity caused by contamination or coating delamination.
**A 5–8% change in deflection sensitivity over several hours of scanning is acceptable.**
<sup class="ref-badge" title="Muller, Nat. Protoc (2014)">ref</sup>
</div>

- To measure $k$, the tip must be retracted at least 100 μm from the substrate.
    - Measured $k$ can differ substantially from the nominal value (potentially by a factor of 2).

## Imaging Parameters

#### Engaging

- Start from a low engage setpoint and increase by ~10 pN increments until the minimum reliable engage setpoint is found.
- The gain during engagement should not be too high, otherwise the tip is easily damaged. Recommended value: 10 <sup class="ref-badge" title="Alice Pyne, Chromosome Architecture (2022)">ref</sup>.
- Increasing the engage setpoint or raising the gain can both speed up the engagement process.
- If ScanAsyst Auto Setpoint is not used, the system sets the engage setpoint as the peak force setpoint after engagement.

#### Sync Distance

- Set the sync distance <font color="#FCD092">immediately</font> after engagement; otherwise, the tip is easily damaged.
    - Autoconfig can be used to set this value, but when using a small peak force (where the peak force is barely discernible above the noise), manual adjustment is required.

<div class="callout callout-note" markdown="1" style="background: #fffbeb; border-left: 4px solid #d97706; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
<p style="margin: 0 0 8px 0; font-weight: 600; color: #d97706;">🔎 Note</p>
- In the Bruker Multimode 8 Force Monitor, the blue trace is approach and the red trace is retract.
- Another use of autoconfig: to analyze and eliminate parasitic deflection (i.e., ringing at the pull-off point, typically including free oscillation of the tip after detachment from the surface, piezo cycle-induced tip deformation, and viscoelastic effects).
</div>

<div class="callout callout-tip" markdown="1" style="background: #eff6ff; border-left: 4px solid #2563eb; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
<p style="margin: 0 0 8px 0; font-weight: 600; color: #2563eb;">💡 Auto Config for Small Peak Force Setpoint (&lt; ~20 mV)</p>
Using autoconfig at a very small setpoint may cause the tip to completely lose contact with the surface. Therefore, first set a larger setpoint, run autoconfig, and then reduce the setpoint back down.
</div>

- Sync Distance QNM is obtained by calibrating on a hard sample (and should not be modified since calibration), whereas Sync Distance New is used for feedback and needs to be tuned during scanning.
- Alice Pyne's approach <sup class="ref-badge" title="Alice Pyne, Chromosome Architecture (2022)">ref</sup>: First optimize Sync Distance New so that the small circle lies at the peak force on the Force–Time curve; then set Sync Distance QNM to the same value as Sync Distance New, and check whether the Force–Z curve is symmetric about the small circle. <font color="#787878">(This can also serve as a check for correct Sync Distance New tuning: if setting Sync Distance QNM equal to Sync Distance New makes the Force–Z curve symmetric about the small circle, then the setting is correct.)</font>
- When the PeakForce frequency changes, the Sync Distance must be adjusted accordingly. Generally, when the frequency doubles, the Sync Distance should be reduced to 1/3 <sup class="ref-badge" title="Alice Pyne, Chromosome Architecture (2022)">ref</sup>.
    - <u>Personal note: This recommendation may apply to Sync Distance in units of μs rather than the percentage-based Sync Distance used on the MM8.</u>

#### Amplitude

**Small amplitudes keep the tip in the short-range force regime, achieving high topographic contrast while also reducing fluid drag. However, the amplitude must not be too small to avoid sample damage.**

- Large oscillation amplitudes (~10–100 nm) are desirable for measuring long-range interactions (e.g., **electrostatic and hydrophobic**), whereas small oscillation amplitudes (3 nm) are suitable for sensing short-range interactions (e.g., **Pauli repulsion and van der Waals**) <sup class="ref-badge" title="Dufrene & Muller, Nat. Methods (2013)">ref</sup>.
- The amplitude can be adjusted to roughly the height of the protein protrusions (for membrane proteins: 4–15 nm) <sup class="ref-badge" title="Muller, Nat. Protoc (2014)">ref</sup>, or 1–2 times the protrusion height <sup class="ref-badge" title="Alice Pyne, Chromosome Architecture (2022)">ref</sup>.
- At too-high amplitudes, the force feedback may be impaired and the biological sample may be damaged <sup class="ref-badge" title="Muller, Nat. Protoc (2014)">ref</sup>.

#### Lift Height

- Defined as the height at which the tip no longer interacts with the sample, corresponding to the point on the force curve where the signal flattens. This is the lift height used during autoconfig.
- Lift height is coupled with autoconfig: clicking the autoconfig button automatically calculates the lift height and performs autoconfig at that height; manually changing the lift height triggers autoconfig at the specified height.
- If set manually, observe the force curve and set the lift height at the point where the force curve begins to flatten (should be higher than the protrusion height of the molecules of interest).
- Even at small amplitudes and small forces, adjusting the lift height can help flatten the baseline <sup class="ref-badge" title="Alice Pyne, Chromosome Architecture (2022)">ref</sup>.

#### Setpoint

- A very small force may result in a noisy force curve. In this case, increasing the force can improve the signal-to-noise ratio.
- **After starting the scan, the approach setpoint must be adjusted to be less than the imaging setpoint**, because changes to the peak force amplitude, lift height, sync distance, or running autoconfig will all trigger re-engagement.

#### Gain

**Goal: to find the optimal ratio between I gain and P gain for the system.**

- Gain tuning procedure <sup class="ref-badge" title="Atomic Force Microscopy for Life Sciences by Bruker">ref</sup>:
    1. Increase I gain until the signal begins to oscillate, then reduce slightly.
    2. Increase P gain until the signal begins to oscillate, then reduce slightly.
    3. Repeat steps 1 and 2 until no oscillation occurs after a slight increase in gain.
- Generally, first minimize the force, then optimize the feedback gain and scan rate.
- Optimal gain: the gain value just before the signal starts oscillating or just before noise noticeably increases in the topography image.

#### Lowpass Filter
(This parameter appears distinct from the parameter controlled by "LP Deflection BW" ?)
<div class="callout callout-note" markdown="1" style="background: #fffbeb; border-left: 4px solid #d97706; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
<p style="margin: 0 0 8px 0; font-weight: 600; color: #d97706;">🔎 "LP Deflection BW"</p>
This parameter invokes a user-programmable low-pass filter to remove high-frequency noise from the real-time data. The filter operates on the collected data regardless of scan direction. The cutoff frequency can be set from 1–65 kHz.
In contrast, the lowpass deflection bandwidth parameter in PeakForce (not available on the MM8) can only be set from 0–65.56 kHz.
</div>

**Purpose: To reduce baseline ringing occurring at the pull-off point.**

- Typically set to ~20 times the peak force frequency (&lt;65 kHz) <sup class="ref-badge" title="Alice Pyne's doctoral thesis (2015)">ref</sup>.
- However, if set too low, it will distort the force curve and introduce errors when analyzing mechanical properties.



#### Scanning Strategy

- Recommended operations after engagement <sup class="ref-badge" title="Alice Pyne, Chromosome Architecture (2022)">ref</sup>:
    1. Set the force setpoint slightly above the noise floor (~70 pN).
    2. Adjust Sync Distance New and QNM.
    3. Set Lift Height (a worse approach: Auto Config).
    4. Scan at a large scale; tune gain (and possibly increase setpoint + re-tune gain).
    5. Zoom in to a small area, increase pixel count to achieve a resolution of $\le$ ~0.5 nm.
    6. Reduce the setpoint (and re-tune gain).
- From large to small scan ranges:
    - Large range: scan rate 1–2 Hz, PeakForce amplitude 40–60 nm (to compensate for large obstacles and the tilt of the support).
        - The scan angle can also be adjusted to compensate for the tilt of the support.
    - Small range: zoom in from the large range, adjust the amplitude for optimal topographic contrast. PeakForce amplitude: membrane proteins 4–15 nm; protein fibrils 10–25 nm <sup class="ref-badge" title="Muller, Nat. Protoc (2014)">ref</sup>.
        - When switching to a small scan range, it may be necessary to reduce the setpoint accordingly.
        - The scan rate should be increased appropriately to prevent sample damage from acquiring too many force curves per pixel.
        - If "smearing" or "creep" is observed at the small range, a faster scan rate or a more stable instrument setup is needed.

## Other Aspects

#### Instrument Stability and Equilibration

**Standard: the tip should exert force with an accuracy of a few pN.**

- Use a mechanical vibration analyzer to assess the instrument's mechanical vibrations; electromagnetic noise can be analyzed via the AFM's input and output signals. A more practical approach is to monitor the tip oscillation far from and close to the substrate to judge instrument stability.
- Avoid introducing air bubbles when preparing the substrate.
- Prevent cables from picking up mechanical or acoustic noise.
- Turn on the instrument and related equipment several hours before scanning to minimize drift. After sample loading, reaching full equilibration may take ~2 h, which can be judged by monitoring the deflection channel or the diode signals ("VERT", "HORI").
- For tips with a low spring constant, thermal noise is usually the dominant noise source.
- Cantilever drift typically manifests as a slow, continuous bending of the cantilever.

<div class="callout callout-tip" markdown="1" style="background: #eff6ff; border-left: 4px solid #2563eb; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
<p style="margin: 0 0 8px 0; font-weight: 600; color: #2563eb;">💡 If the Instrument Cannot Be Stabilized, Diagnose as Follows:</p>
- If unstable in both liquid and air, the issue is likely ambient thermal effects or a problem with the instrument itself.
- If unstable only in liquid, the problem is more likely with the probe.
*(Source: Muller, Nat. Protoc (2014))*
</div>

<div class="callout callout-note" markdown="1" style="background: #fffbeb; border-left: 4px solid #d97706; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
<p style="margin: 0 0 8px 0; font-weight: 600; color: #d97706;">🔎 Possible Causes of a Large Hysteresis Between Trace and Retrace:</p>
- The tip is not properly clamped.
- The substrate is unstable (air bubbles, unadhered glue, or partially cleaved mica that did not fully detach and fell back onto the substrate).
- Feedback gain is too low.
*(Source: Muller, Nat. Protoc (2014))*
</div>

#### Sample Cleanliness

**Standard: scan bare mica and observe no contamination.**

- Use nanopure, double-distilled, or ultrapure water instead of deionized water to avoid residual ions or organic matter in the water.
- Clean the substrate or fluid cell sequentially with dishwashing detergent and filtered nanopure water.
- Dry with a N<sub>2</sub> gun fitted with a filter, not with compressed air.
- Use buffer within one week.
- Rinse containers for samples or buffer with nanopure water before use.

#### Miscellaneous

- Substrate assembly:
    - Place a 0.5–1 cm diameter mica disc on a 1.5–2 cm diameter Teflon foil, then fix onto a metal disc <sup class="ref-badge" title="Muller, Nat. Protoc (2014)">ref</sup>.
- **A trick to prevent tip sticking**: add glycerol to the buffer (&lt; 30% (v/v)).
- Time management tip:
    - While preparing the sample, prepare a clean mica substrate with clean buffer as a dummy sample, mount the probe, turn on the laser, and let the entire system equilibrate and stabilize.
- Some opinions on high-resolution imaging:
    - "Proteins and fibrils that protrude by more than 3 nm from the mica surface may be imaged at a resolution **approaching 2 nm**, because such 'large' protrusions are likely to be structurally flexible and their protruding height prevents the proper contouring of the sample surface by the AFM stylus." <sup class="ref-badge" title="Muller, Nat. Protoc (2014)">ref</sup>
    - "There are a number of complications that currently prevent AFM from achieving atomic resolutions on biomolecules. These include: The binding of the biomolecule to an appropriate substrate, mobility of the molecule, the presence of contamination, the effect of forces exerted by the tip on the sample, and the difficulties in following the contours of a more complex and highly corrugated molecule using a feedback system, whilst accurately controlling the tip sample interaction and therefore the imaging force." <sup class="ref-badge" title="Alice Pyne's doctoral thesis (2015)">ref</sup>
- Reference parameters <sup class="ref-badge" title="Alice Pyne's doctoral thesis (2015) & Alice Pyne, Chromosome Architecture (2022)">ref</sup>:
    - ![AlicePyne_doctoral_thesis_Table3.1.png](/assets/img/protocols/peakforce-tapping/AlicePyne_doctoral_thesis_Table3.1.png)
    - ![AlicePyne_Chromosome_Architecture(2022).png](/assets/img/protocols/peakforce-tapping/AlicePyne_Chromosome_Architecture(2022).png)
