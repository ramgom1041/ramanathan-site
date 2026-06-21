# Camera Technology & Imaging Systems — Professional Course Curriculum

**Subtitle:** From Photons to Production — Understanding Camera Technology and Selecting the Right Imaging System for Real-World Engineering.

**Audience:** Machine-vision, robotics, computer-vision, automation & imaging-system engineers; technical product developers; engineering students.

**Orientation:** Industrial / machine-vision, engineering decision-making and system selection — *not* photography hobbyism.

**Format:** 7 sections · 22 modules · each module = live interactive simulation + theory + exercises + quiz.

**Author:** Dr. S. Ramanathan — Team Lead, Machine Vision.

---

# SECTION 1 — Foundations of Imaging

## Module 1 — How a Camera Works (Photon → Pixel)
- **Learning objectives:** Trace the full imaging pipeline; name each stage and what it does; identify where information/quality is lost.
- **Overview:** A camera is a measurement instrument. Light from the scene is focused by the lens onto a sensor, converted to charge, amplified, digitized, then processed into an image.
- **Core concepts:** Lens → aperture → sensor (photodiode → charge) → readout/amplifier → ADC → ISP (demosaic, white balance, gamma, compression) → image/stream.
- **Engineering explanations:** Each block has noise, bandwidth and latency; the weakest stage caps system performance; "image quality" is a chain, not one number.
- **Key equations:** Photons→electrons: `N_e = QE · N_photons`; signal `DN = gain · N_e + offset`.
- **Interactive sim ideas:** Animated pipeline — toggle each stage on/off and watch a sample image degrade (no demosaic → green mosaic; no ISP → raw; clipped ADC → posterized).
- **Diagrams:** Block diagram of the pipeline; cross-section of a pixel.
- **Practical exercises:** Label a real camera datasheet's spec against each pipeline stage.
- **Try This:** Disable the ISP stage and observe raw vs processed.
- **Common mistakes:** Thinking "megapixels = quality"; ignoring QE and the lens; assuming the ISP is lossless.
- **Knowledge check:** (1) Order the pipeline stages. (2) Where is demosaicing done? (3) What does the ADC limit?
- **Further reading:** Janesick, *Photon Transfer*; sensor vendor (Sony/onsemi) pixel app-notes.

## Module 2 — Light & the Electromagnetic Spectrum
- **Learning objectives:** Match each waveband to what it reveals and the sensor/lens technology required.
- **Overview:** Different wavelengths "see" different physics — pick the band that makes your feature visible.
- **Core concepts / bands:** **UV** (200–400 nm): surface defects, fluorescence. **Visible** (400–700 nm): general inspection, color. **NIR** (700–1000 nm): silicon-friendly, sees through some inks/skin, veins. **SWIR** (1–2.5 µm): moisture/water content, silicon vs InGaAs, sees through some plastics/silicon. **MWIR** (3–5 µm) & **LWIR** (8–14 µm): thermal/emissive imaging, no illumination needed. **X-ray:** internal/density inspection (BGA voids, castings).
- **Engineering explanations:** Silicon sensors respond ~350–1050 nm; SWIR needs InGaAs; thermal needs microbolometer/cooled detectors and special optics (Ge, not glass). Illumination & lens glass must match the band.
- **Key equations:** Photon energy `E = hc/λ`; blackbody peak `λ_max = 2898/T(K)` µm (Wien).
- **Interactive sim ideas:** Spectrum slider → shows example image + recommended sensor/lens/illumination + typical applications for the selected band.
- **Diagrams:** EM spectrum band chart with sensor materials & applications overlaid.
- **Practical exercises:** Given 4 inspection problems, choose the waveband and justify.
- **Try This:** Slide into SWIR — note silicon sensors no longer work (need InGaAs).
- **Common mistakes:** Using visible light when the feature is only visible in UV/NIR/thermal; using glass optics in thermal.
- **Knowledge check:** (1) Which band for water content? (2) Which detector for LWIR? (3) Wien's law for a 300 K object.
- **Further reading:** Edmund Optics "Imaging beyond visible"; FLIR thermal primers.

## Module 3 — Exposure Fundamentals
- **Learning objectives:** Control image brightness in machine-vision terms (exposure time, gain, aperture) and understand the trade-offs.
- **Overview:** Exposure = how many electrons fill the well. In MV we fix it deterministically (not "auto").
- **Core concepts:** Aperture (f-number) ↔ light & DoF; exposure time ↔ motion blur; gain (dB)/ISO ↔ brightness & noise.
- **Engineering explanations:** Prefer more light + low gain over high gain; exposure time bounded by object motion; flicker-free/strobed lighting synced to trigger.
- **Key equations:** `EV = log2(N²/t)`; brightness `∝ t·gain/N²`; max exposure for blur < 1 px: `t < pixel_pitch·M / v_object`.
- **Interactive sim ideas:** Aperture/shutter/gain sliders → brightness preview + DoF/blur/noise indicators (already built).
- **Diagrams:** Exposure-triangle chart adapted to MV (gain in dB).
- **Practical exercises:** Compute max exposure time for a part moving at 0.5 m/s imaged at 20 µm/px.
- **Try This:** Raise gain to brighten — watch noise appear instead of using light.
- **Common mistakes:** Fixing brightness with gain instead of lighting; exposure too long for line-rate/motion.
- **Knowledge check:** (1) What causes motion blur? (2) Gain vs light for SNR? (3) Compute EV.
- **Further reading:** Basler "exposure & gain" app notes.

---

# SECTION 2 — Optics & Lenses

## Module 4 — Field of View & Focal Length
- **Objectives:** Compute focal length needed to cover a target at a working distance on a given sensor.
- **Core concepts:** FOV, working distance (WD), sensor size, magnification, "pixels on target."
- **Equations:** `FOV = 2·atan(d_sensor/2f)`; `FOV_width = WD·d_sensor/f`; `f ≈ d_sensor·WD/FOV_width`; spatial res = FOV_width/pixels.
- **Sim ideas:** Lens calculator — enter sensor, WD, target size → required focal length + FOV angle + mm/px (built).
- **Diagrams:** Camera/lens/FOV wedge to target plane.
- **Exercises:** Pick a lens to inspect a 200 mm part at 600 mm WD on a 2/3″ sensor.
- **Try This:** Halve focal length → FOV doubles, detail halves.
- **Common mistakes:** Ignoring sensor size; confusing FOV with resolution; not checking lens image-circle covers the sensor.
- **Quiz:** (1) f for given FOV/WD. (2) Effect of larger sensor. (3) mm/px definition.
- **Reading:** Edmund Optics lens-selection guide.

## Module 5 — Depth of Field
- **Objectives:** Predict and engineer the in-focus zone for inspection.
- **Core concepts:** Circle of confusion (CoC), hyperfocal distance, near/far limits, diffraction limit at small apertures.
- **Equations:** `H = f²/(N·c)+f`; `D_n = s(H−f)/(H+s−2f)`; `D_f = s(H−f)/(H−s)`.
- **Sim ideas:** Aperture/focal/distance sliders → shaded in-focus band (built); add diffraction warning at high f.
- **Diagrams:** Side-view scene with focus band.
- **Exercises:** Find aperture for ±5 mm DoF on a part.
- **Try This:** Stop down for more DoF — note diffraction softening past f/11–f/16.
- **Common mistakes:** Forgetting diffraction; assuming telecentric lenses follow normal DoF rules.
- **Quiz:** (1) DoF vs aperture. (2) Hyperfocal meaning. (3) When far limit = ∞.
- **Reading:** CoC & diffraction primers.

## Module 6 — Lens Technologies
- **Objectives:** Select the right lens *type* for an application.
- **Core concepts:** Prime vs zoom; wide / normal / telephoto; macro (>1:1); **telecentric** (constant magnification, no perspective error — key for metrology); fixed-focal MV lenses, image circle, mount (C/CS/F/M12).
- **Engineering explanations:** Telecentric removes parallax → accurate gauging; macro for tiny parts; resolution (lp/mm) must match sensor; avoid consumer zooms in MV (focus/zoom drift).
- **Equations:** Telecentric: magnification independent of WD; lateral magnification `M = f/(WD−f)` (entocentric).
- **Sim ideas:** Lens-type selector → shows perspective vs telecentric projection of a stepped part; magnification calculator.
- **Diagrams:** Ray diagrams: entocentric vs telecentric.
- **Exercises:** Choose lens for measuring a 10 mm part to ±10 µm.
- **Try This:** Compare entocentric vs telecentric on a 3D step — watch parallax error vanish.
- **Common mistakes:** Using entocentric lenses for metrology; telecentric on objects larger than its diameter.
- **Quiz:** (1) Why telecentric for gauging? (2) Macro definition. (3) Image-circle/mount checks.
- **Reading:** Opto-Engineering telecentric handbook.

## Module 7 — Lens Distortion & Calibration
- **Objectives:** Quantify distortion and calibrate for accurate measurement.
- **Core concepts:** Radial (barrel/pincushion), tangential, perspective distortion; pinhole model + intrinsics/extrinsics; reprojection error.
- **Equations:** Brown–Conrady `r_d = r(1+k₁r²+k₂r⁴+k₃r⁶)`; intrinsics `K = [[fx,0,cx],[0,fy,cy],[0,0,1]]`.
- **Sim ideas:** k₁ slider warps a grid (built); add checkerboard "calibration" demo showing undistort.
- **Diagrams:** Distorted vs undistorted grid; checkerboard calibration setup.
- **Exercises:** Run OpenCV `calibrateCamera` on a checkerboard set (offline lab).
- **Try This:** Switch k₁ sign → barrel vs pincushion.
- **Common mistakes:** Skipping calibration before measuring; too few/poorly-spread calibration views.
- **Quiz:** (1) Barrel vs pincushion sign. (2) What K holds. (3) Why calibrate for metrology.
- **Reading:** Zhang's calibration paper; OpenCV calib docs.

---

# SECTION 3 — Image Sensors

## Module 8 — Sensor Formats & Pixel Size
- **Objectives:** Read sensor specs; trade resolution vs sensitivity.
- **Core concepts:** Optical formats (1/4″…full-frame), crop factor, pixel pitch, fill factor, microlenses, resolution vs sensitivity trade-off.
- **Equations:** crop factor `= 43.27/diag_mm`; pixel pitch `= sensor_w/h_px`; well capacity ∝ pixel area.
- **Sim ideas:** Overlay sensor rectangles to compare sizes; MP + format → pixel pitch, crop factor (built).
- **Diagrams:** Scaled sensor-size comparison chart.
- **Exercises:** Compare 5 MP on 1/2″ vs 2/3″ — which has bigger pixels/better low light?
- **Try This:** Increase MP at fixed sensor size → smaller pixels → less light/pixel.
- **Common mistakes:** Chasing MP at the cost of pixel size & SNR; lens not covering the format.
- **Quiz:** (1) Crop factor of 1″ sensor. (2) Pixel pitch from MP. (3) Bigger pixels → ?
- **Reading:** Sony Pregius/Starvis briefs.

## Module 9 — CCD vs CMOS
- **Objectives:** Choose sensor architecture by application.
- **Core concepts:** CCD charge-transfer to one amp (uniform, high full-well, slow, blooming/smear) vs CMOS per-column ADC (fast, low-power, ROI, cheap, modern low-noise).
- **Engineering explanations:** CMOS dominates MV; CCD niche (scientific/uniformity); BSI, global-shutter CMOS (Sony Pregius).
- **Sim ideas:** Architecture diagram toggle CCD/CMOS readout path (built).
- **Diagrams:** Readout-path schematics.
- **Exercises:** Pick sensor tech for a high-speed line-scan vs low-light astronomy.
- **Try This:** Toggle architectures, compare readout.
- **Common mistakes:** Assuming CCD always lower-noise; ignoring shutter type.
- **Quiz:** (1) Why CMOS faster? (2) CCD smear cause. (3) ROI readout benefit.
- **Reading:** Teledyne CCD-vs-CMOS white paper.

## Module 10 — Global vs Rolling Shutter
- **Objectives:** Select shutter type for moving scenes.
- **Core concepts:** Rolling (row-by-row, skew/jello/partial-exposure) vs global (all pixels at once); flash/strobe with rolling shutter.
- **Equations:** skew shift `Δx = v·T_read`; safe with strobe if `t_strobe ≪ T_read`.
- **Sim ideas:** Object speed + readout time → skewed parallelogram vs rectangle (built).
- **Diagrams:** Row-exposure timing chart.
- **Exercises:** Decide shutter for a conveyor at 1 m/s line-scan vs area-scan.
- **Try This:** Increase speed/readout → shear grows.
- **Common mistakes:** Rolling shutter for fast motion; expecting strobe to fix rolling without global reset.
- **Quiz:** (1) Cause of skew. (2) When global is mandatory. (3) Strobe + rolling caveat.
- **Reading:** Vendor global-shutter app notes.

## Module 11 — Dynamic Range & Noise
- **Objectives:** Compute DR/SNR; identify the dominant noise source.
- **Core concepts:** Shot noise (√S), read noise (floor), dark current (thermal), fixed-pattern noise, full-well capacity, quantization.
- **Equations:** `DR_dB = 20·log10(N_full/σ_read)`; `DR_stops = log2(N_full/σ_read)`; `SNR(S) = S/√(S+σ_read²+σ_dark²)`.
- **Sim ideas:** Full-well/read-noise/bit-depth sliders → SNR curve + DR readout (built).
- **Diagrams:** Photon-transfer curve (noise vs signal, log-log).
- **Exercises:** Compute DR for 20 ke⁻ well, 4 e⁻ read noise.
- **Try This:** Lower read noise → shadows clean up, DR widens.
- **Common mistakes:** Over-specifying bit depth beyond DR; cooling ignored for long exposures.
- **Quiz:** (1) DR formula. (2) Shot vs read-noise regimes. (3) Why √S.
- **Reading:** EMVA 1288 standard; Photon Transfer (Janesick).

---

# SECTION 4 — Image Science

## Module 12 — Bayer Pattern & Color Imaging
- **Objectives:** Understand color capture and when to use mono.
- **Core concepts:** CFA (RGGB), demosaicing, color reproduction, white balance, color spaces (sRGB), 3-CCD/prism, **monochrome advantages** for MV (resolution, sensitivity, no false color).
- **Equations:** white balance gains `(R,G,B)·(g_r,1,g_b)`; luminance `Y=0.299R+0.587G+0.114B`.
- **Sim ideas:** Toggle raw mosaic ↔ demosaiced; white-balance gain sliders (mosaic built).
- **Diagrams:** Bayer tile; demosaic interpolation.
- **Exercises:** Decide color vs mono for a steel-surface scratch inspection.
- **Try This:** Toggle demosaic; see resolution/false-color trade-off.
- **Common mistakes:** Using color when mono is better; ignoring white balance/illuminant.
- **Quiz:** (1) Why 2× green. (2) Mono benefits. (3) What demosaicing estimates.
- **Reading:** Demosaicing survey; EMVA color notes.

## Module 13 — Resolution, MTF & Nyquist
- **Objectives:** Specify true resolving power, not just MP.
- **Core concepts:** Optical vs sensor resolution, sampling theory, Nyquist, aliasing/moiré, OLPF, system MTF = lens × sensor.
- **Equations:** `f_Nyq = 1/(2p)` lp/mm; sensor MTF `= |sinc(f·p)|`; `MTF_sys = ∏ MTF_i`.
- **Sim ideas:** Pixel pitch + lens MTF50 → system MTF curve with Nyquist marker (built).
- **Diagrams:** MTF curves; aliasing of a fine grating.
- **Exercises:** Match a lens to a 3.45 µm pixel sensor (need ~145 lp/mm).
- **Try This:** Shrink pixels — Nyquist rises only if lens keeps up.
- **Common mistakes:** Buying MP a lens can't resolve; ignoring aliasing.
- **Quiz:** (1) Nyquist from pitch. (2) System MTF rule. (3) Aliasing cause.
- **Reading:** MTF tutorials (Edmund); EMVA 1288.

## Module 14 — Image Quality Metrics
- **Objectives:** Quantify "good image" with engineering metrics.
- **Core concepts:** Sharpness (MTF50/acutance), contrast, SNR, dynamic range, color accuracy (ΔE), uniformity, defect-pixel metrics.
- **Equations:** `SNR_dB = 20log10(μ/σ)`; `ΔE` color difference; contrast `=(I_max−I_min)/(I_max+I_min)`.
- **Sim ideas:** Adjust noise/contrast/blur on a test chart → live metric readouts.
- **Diagrams:** Slanted-edge MTF; test charts (Siemens star, ΔE chart).
- **Exercises:** Measure SNR from a flat-field image (offline).
- **Try This:** Add noise → watch SNR & MTF50 drop.
- **Common mistakes:** Judging by eye instead of metrics; one metric only.
- **Quiz:** (1) SNR in dB. (2) What MTF50 means. (3) ΔE for color.
- **Reading:** EMVA 1288; ISO 12233.

---

# SECTION 5 — 3D & Advanced Imaging

## Module 15 — Stereo Vision
- **Objectives:** Recover depth from two views; budget the error.
- **Core concepts:** Disparity, triangulation, epipolar geometry, rectification, baseline vs range trade-off.
- **Equations:** `Z = f·B/d`; depth error `ΔZ ≈ Z²·Δd/(f·B)`.
- **Sim ideas:** Baseline/focal/disparity sliders → depth + top-view triangulation (built); add error vs range.
- **Diagrams:** Two-camera epipolar geometry.
- **Exercises:** Size a baseline for ±1 mm at 2 m.
- **Try This:** Widen baseline → better far-range precision, smaller overlap.
- **Common mistakes:** Ignoring Z² error growth; textureless surfaces (no correspondences).
- **Quiz:** (1) Z = ? (2) Error scaling. (3) Why texture needed.
- **Reading:** Hartley & Zisserman, *Multiple View Geometry*.

## Module 16 — 3D Imaging Technologies
- **Objectives:** Choose a 3D method per application.
- **Core concepts:** Passive stereo; **structured light** (projected patterns); **Time-of-Flight** (phase/pulse); **laser triangulation** (line profilometry); **LiDAR**; trade-offs in range, accuracy, speed, cost, ambient-light robustness.
- **Equations:** ToF `Z = c·Δt/2` (pulse) or `Z = c·φ/(4πf_mod)` (CW); laser-tri depth from displaced line position.
- **Sim ideas:** Method selector → accuracy/range/speed radar chart + best-fit applications.
- **Diagrams:** Each modality's geometry.
- **Exercises:** Pick a 3D method for bin-picking shiny parts vs room mapping.
- **Try This:** Compare structured light vs ToF accuracy at 1 m vs 5 m.
- **Common mistakes:** ToF for sub-mm metrology; structured light in bright ambient.
- **Quiz:** (1) ToF equation. (2) Best for sub-mm? (3) LiDAR use case.
- **Reading:** Structured-light & ToF reviews.

## Module 17 — Multispectral & Hyperspectral Imaging
- **Objectives:** Use spectral signatures for material discrimination.
- **Core concepts:** Multispectral (few bands) vs hyperspectral (hundreds, contiguous); spectral cube (x,y,λ); push-broom vs snapshot; spectral signatures.
- **Equations:** reflectance `R(λ)=I_sample/I_reference`; NDVI `=(NIR−Red)/(NIR+Red)`.
- **Sim ideas:** Pick bands → "see" hidden features (bruised fruit, vegetation health, coatings).
- **Diagrams:** Spectral cube; example signatures.
- **Exercises:** Choose bands to detect surface moisture vs vegetation stress.
- **Try This:** Toggle NIR band to reveal a bruise invisible in RGB.
- **Common mistakes:** Hyperspectral when 2–3 bands suffice (cost/data); ignoring calibration/illuminant.
- **Quiz:** (1) NDVI formula. (2) Multi vs hyper. (3) Push-broom meaning.
- **Reading:** Remote-sensing & food-sorting hyperspectral case studies.

---

# SECTION 6 — Industrial Camera Systems

## Module 18 — Camera Interfaces & Data Rates
- **Objectives:** Choose the interface that carries your data rate at the required cable length.
- **Core concepts:** USB3 Vision, GigE Vision (+PoE), 10GigE, Camera Link (Base/Full), CoaXPress (CXP-6/12), MIPI CSI-2 (embedded); cable length, bandwidth, CPU load, multi-camera.
- **Equations:** data rate `= W·H·bitdepth·fps` bits/s; e.g. 5 MP×8 bit×60 fps ≈ 2.4 Gb/s ≈ 300 MB/s.
- **Sim ideas:** Resolution/fps/bit-depth → required MB/s → smallest interface that fits, with max cable length (built).
- **Diagrams:** Interface bandwidth-vs-distance chart.
- **Exercises:** Pick interface for 12 MP @ 30 fps at 20 m.
- **Try This:** Push fps until GigE saturates → step up to 10GigE/CXP.
- **Common mistakes:** Ignoring cable length; forgetting host bandwidth/CPU; sustained vs burst.
- **Quiz:** (1) Bandwidth formula. (2) GigE limit. (3) Longest-reach interface.
- **Reading:** AIA/EMVA interface standards.

## Module 19 — Illumination Systems
- **Objectives:** Design lighting that makes the feature pop (often the highest-leverage decision in MV).
- **Core concepts:** Geometry — backlight (silhouette), bright field, **dark field** (scratches/edges), diffuse/dome (specular parts), coaxial, **structured/line**; **polarized** (glare removal); wavelength selection & filters; strobing/over-driving.
- **Engineering explanations:** "Good lighting > more pixels"; maximize contrast of the defect; control ambient light.
- **Equations:** inverse-square `E ∝ 1/d²`; contrast goal `C=(I_feat−I_bg)/(I_feat+I_bg)` maximized.
- **Sim ideas:** Lighting-geometry selector → simulated appearance of a scratch/edge/specular part under each.
- **Diagrams:** Each lighting geometry vs sample.
- **Exercises:** Choose lighting to reveal an engraved code on shiny metal.
- **Try This:** Switch bright→dark field → scratches invert from invisible to bright.
- **Common mistakes:** Solving with software what lighting should solve; uncontrolled ambient; specular hotspots.
- **Quiz:** (1) Dark field reveals? (2) Polarizer use. (3) Backlight for?
- **Reading:** CCS/Smart Vision Lights lighting guides.

## Module 20 — Machine Vision System Design
- **Objectives:** Integrate camera + lens + lighting + trigger + processing into a working system.
- **Core concepts:** Triggering (hardware/software, encoder for line-scan), synchronization, exposure/strobe timing, processing (edge/PC/GPU), latency & throughput budget, environment (vibration, heat, IP rating).
- **Equations:** throughput `= parts/s`; cycle time budget = acquisition + transfer + processing; line-scan line rate `= v/Δy`.
- **Sim ideas:** Timing diagram — trigger → strobe → exposure → readout → process; adjust and find bottleneck.
- **Diagrams:** Full system block + timing chart.
- **Exercises:** Build a timing budget for 30 parts/s on a conveyor.
- **Try This:** Increase processing time past cycle time → see missed parts.
- **Common mistakes:** No hardware trigger; ignoring transfer/processing latency; under-spec'd PC.
- **Quiz:** (1) Why encoder trigger for line-scan. (2) Cycle-time terms. (3) Strobe-exposure sync.
- **Reading:** Cognex/Keyence integration guides.

---

# SECTION 7 — Camera Selection Masterclass

## Module 21 — Camera Selection Workflow
- **Objectives:** Turn application requirements into a complete camera+lens+light+interface spec.
- **Core concepts / workflow:**
  1. **Required resolution** = object size / smallest feature × (pixels per feature, ≥2–3).
  2. **Sensor & pixel size** from resolution + sensitivity/SNR needs.
  3. **Lens** from FOV, WD, and required spatial resolution (Modules 4–6); check MTF & format.
  4. **Frame/line rate** from part speed/throughput.
  5. **Shutter** (global if moving), **mono/color**, **waveband**.
  6. **Interface** from data rate + cable length (Module 18).
  7. **Illumination** to maximize feature contrast (Module 19).
  8. Validate **DR/SNR**, environment, budget.
- **Equations:** `sensor_px = (FOV/feature_size)·px_per_feature`; `mm/px = FOV/px`; data rate (Module 18); blur limit (Module 3).
- **Sim ideas:** **Interactive selection wizard** — enter object size, smallest defect, accuracy, WD, speed, environment → outputs recommended resolution, pixel size, lens focal length, frame rate, shutter, interface, lighting.
- **Diagrams:** Decision-flow flowchart.
- **Exercises:** Spec a full system for a stated inspection task.
- **Try This:** Tighten accuracy 2× → watch required resolution & cost rise.
- **Common mistakes:** Spec'ing camera before defining the smallest feature & accuracy; forgetting lighting/interface.
- **Quiz:** (1) Resolution from feature size. (2) When global shutter. (3) First step in the workflow.
- **Reading:** Vendor MV selection calculators; this course's modules 4/13/18.

## Module 22 — Engineering Case Studies
For each: requirement → chosen sensor/resolution/pixel/shutter/waveband → lens → lighting → interface → rationale & pitfalls.
- **PCB inspection** — high-res area/line-scan, coaxial/dome lighting, telecentric for measurement, mono.
- **Semiconductor inspection** — sub-µm, telecentric + high-MTF, UV/DUV, vibration isolation.
- **Traffic ANPR** — global shutter (motion), NIR + NIR illumination + IR-pass filter, wide DR for headlights, GigE.
- **Drone imaging** — small/light, global shutter, multispectral for crops, rolling-shutter pitfalls.
- **Fruit sorting** — color + NIR/hyperspectral (bruises, sugar), high line rate, diffuse lighting.
- **Warehouse robotics** — 3D (stereo/ToF), wide FOV, robust to ambient, GigE/USB3.
- **Bin picking** — structured-light/ToF 3D, handling shiny parts, accuracy vs cycle time.
- **Medical imaging** — high DR & color accuracy, low noise, regulatory; sometimes cooled sensors.
- **Thermal inspection** — LWIR microbolometer, Ge optics, emissivity calibration, no visible light.
- **Try This / Exercise:** Re-derive each spec from the Module 21 workflow.
- **Common mistakes:** Copying a spec without re-checking feature size, motion, and lighting for the new case.
- **Quiz:** Match each application to its critical camera decision.
- **Reading:** Vendor application notes per industry.

---

## Implementation notes (for the interactive platform)
- **Reuse existing sims** (built): exposure, DoF, FOV, distortion, rolling shutter, stereo, sensor formats, lens selector, interfaces, CCD/CMOS, Bayer, MTF, DR/SNR — they map onto Modules 3,5,4,7,10,15,8,6,18,9,12,13,11.
- **New sims to build:** pipeline animation (M1), spectrum explorer (M2), telecentric vs entocentric (M6), 3D-method comparison (M16), spectral-band explorer (M17), lighting-geometry explorer (M19), system timing diagram (M20), **selection wizard (M21)**, case-study cards (M22), image-quality metrics (M14).
- **Per module:** add Learning Objectives, Try-This, Common Mistakes, a 3-question quiz, and Further Reading blocks.
- **Navigation:** group the 22 modules under the 7 collapsible sections; add a progress/contents sidebar.
