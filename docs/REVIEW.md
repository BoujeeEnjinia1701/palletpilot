# Review note: PalletPilot

## Session 2026-09-25: /populate to a strong TRL 2

Overnight batch run; no questions were asked. Every choice that is Amish's to make is listed below as proposed.

### What was done

- `docs/01-problem.md` (PLP-PRB-001 v0.2): problem with ergonomic push-force data, users and context, operating environment, constraints (including OSHA 1910.178 training and modification approval, and ISO 3691-4), out of scope, prior work with inline sources, open questions; co-design checklist added in the portfolio's standard form.
- `docs/03-requirements.md` (PLP-REQ-001 v0.2): 17 measurable requirements (R1 to R17) with targets, verification and a status column, a design load case and design duty, and a list of requirements not met.
- `docs/02-concept.md` (PLP-PRC-001 v0.2): how it works, components table numbered to the BOM and exploded view, first-order numbers (forces, traction, stopping, UWB bearing error, energy, mass and cost) with assumptions, key design choices, safety section, open questions.
- `cad/src/concept_media.py`: massing model of a 27 x 48 in donor jack (grey) and 13 numbered kit parts, with a 48 x 40 in pallet and cartons as hero context.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `model.glb` and `viewer.html`, `exploded.png` with BOM callouts, `cutaway.png`, `flow.png` (energy per shift, estimates marked).
- `bom/bom.csv`: 17 lines with indicative USD prices, rows 1 to 13 numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image, links line, updated problem, concept, components and safety.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged. The pitch and problem are still accurate (see decision 1 on the pitch wording).

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Rolling and breakaway force, 1,100 kg total | about 130 N and 270 N | Motivates the kit |
| Available traction (1.1 kN preload, friction 0.5) | about 550 N | R2 met; R3 (2 % ramp) at risk |
| Stop from 1.2 m/s, walk mode | about 1.56 m | Normal walkie practice |
| Stop from 0.6 m/s, follow mode | about 0.42 m, against about 40 mm bumper travel | R7 **not met** |
| Bumper-only safe speed | about 0.2 m/s | R8 met at that speed |
| UWB bearing error, two anchors 450 mm apart | about ±18° raw | R5 (±10°) **not met** on paper |
| Energy per shift, 60 moves | about 281 Wh of 410 Wh usable | R12 met |
| Charge time | about 4.5 h | R13 met |
| Kit mass | about 37 kg | R15 mass met |
| Added length at floor level | about 330 mm | R15 length (300 mm) **not met** |
| Kit parts cost | about $1,425 | R17 ($1,200) **not met**, about 19 % over |
| Walk-only variant | about $1,075 | Within budget |

Requirements not met or at risk: R7 (non-contact stop in follow mode), R5 (bearing accuracy), R15 (added length, by about 30 mm), R17 (cost) and R3 (2 % ramp, traction margin). R1, R6, R9, R10, R14 and R16 are unverified.

Market context found: a complete 1,500 kg lithium walkie now costs about $1,640 and the PowerPallet 2000 retrofit about $2,084. A walk-only kit plus a new donor jack costs about the same as a new walkie, so PalletPilot's case rests on follow mode and on reusing existing jacks.

### Proposed, awaiting Amish

1. **Follow-mode stopping and the pitch.** Options: (A) add a low-cost lidar or time-of-flight sensor as the main stopping layer, bumper as last resort, follow mode 0.6 m/s, research use in a closed area; (B) safety-rated laser scanner (over $1,000 on its own); (C) bumper only with follow mode at 0.2 m/s; (D) drop follow mode. Recommendation: A for the prototype, with B named as the route to workplace use. This would change "bumper-based stopping" in the pitch to "layered stopping"; `project.yaml` is unchanged until you decide.
2. **Budget.** Options: (a) raise `budget_usd` from $1,200 to about $1,450 (about $1,550 with option 1A); (b) keep $1,200 and cut to the walk-only variant (about $1,075); (c) keep $1,200 and cut elsewhere (for example a single hub motor plus a steering actuator, cheaper bumper). Recommendation: (a), since follow mode is the reason to build the kit. `project.yaml` is unchanged at $1,200.
3. **Drive layout:** two hub motors on a sprung module on the steering yoke, steering by differential drive in follow mode. Alternatives: one motor plus a steering motor, or load-rated drive wheels replacing the steer wheels. Recommendation: dual hub motors.
4. **Power system:** 24 V LiFePO4, 20 Ah. The SwapCell 48 V pack is not proposed because the kit needs only 24 V and stays on the jack all shift. Recommendation: 24 V LiFePO4.
5. **Mounting:** pack and electronics on the steering yoke, not the forks. Recommendation: yoke mounting, checked for handle clearance and bearing load at TRL 3.
6. **Speeds:** walk 1.2 m/s handle-end first and 0.8 m/s forks first, creep 0.3 m/s, follow 0.6 m/s (0.2 m/s until option 1 is built and tested).
7. **Kit rating:** 1,000 kg design load, 1,500 kg maximum at 0.8 m/s or less, below the donor's 2,500 kg.
8. **Legal route for workplace use** (OSHA 1910.178(a)(4) needs the jack maker's written approval for modifications affecting capacity and safe operation). Options: partner with a jack maker for one donor model; document the kit for research and non-workplace use only; or both. Recommendation: document for research use now, and approach a jack maker before any workplace trial.
9. **First site partners:** a small warehouse or 3PL, a grocery or retail backroom, or a maker space. Recommendation: one small warehouse and one maker space.

### Safety concerns

- A loaded jack in follow mode will strike a person before a bumper can stop it at any speed above about 0.2 m/s. This is the main safety finding and drives decision 1.
- Foot crush and pinning at the drive end are the classic walkie injuries; the belly-reverse paddle, handle-angle braking and bumper hoop address them but are unverified.
- Braking falls by about 40 % on a 2 % downgrade; ramps and dock plates need limits.
- The 512 Wh LiFePO4 pack needs a BMS, a terminal fuse, a lockable disconnect and safe charging practice.
- Workplace use raises OSHA training and modification-approval duties; the kit must be presented as a research prototype.

### Gaps against the brief

- The OSHA page could not be fetched during the session (the permission request timed out); the 1910.178 citations use the official regulation URL and a secondary summary for the training requirement. The wording of 1910.178(a)(4) should be checked against the source.
- Hub motor torque, brake holding torque and prices are for the part class, not a chosen supplier.

### Recommended next step

Review this note and the media, and decide items 1 and 2. If approved, run `/advance-trl3` to size traction, braking and the stop chain by calculation, choose the motors and the follow-mode sensor, build the UWB error budget, and produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

Amish's instruction for this session (2026-09-25): "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." For PalletPilot the approved safety recommendation is the low-cost lidar or time-of-flight stop layer (option 1A), the approved budget is about $1,550, and the pitch changes to "layered stopping". PalletPilot now claims TRL 3 (proof of concept on paper). TRL 4 is on hold by Amish's instruction.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (PLP-DDR-001 v0.1): nine TRL 2 items recorded as decided by Amish, 2026-09-25, going with the recommendation (D1 to D9), and six items that stay open (O1 to O6).
- `docs/04-calcs/01-sizing.md` (PLP-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: mass, axle and bearing loads, traction and preload, motor torque and power, steering by differential drive, layered stopping (lidar, bumper, emergency stop, tag loss, parking), protective field sizing, UWB error budget, energy and charging, handle clearance, length, release lever, cost, and a status line for every requirement. The script imports the model's `PARAMS` and the BOM, and prints every number the note quotes, tagged [B0] to [R0].
- `cad/src/model.py`: parametric build123d model (donor jack as reference; subframe with yoke clamp, hub motors, enclosure and lid, pack, driver, contactor, controller, tiller head, beacon, emergency stops, bumper hoop, UWB anchors, release lever, lidar and bracket) with `PARAMS` and `derived()`. Exports `cad/step/` and `cad/stl/`: `palletpilot-assembly`, `palletpilot-kit`, `drive-module`, `enclosure`, `bumper-and-sensors` and `tiller-head`.
- `cad/src/sheets.py` and `cad/drawings/PLP-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, scale 1:20, with length at floor level, added length, steer axis to drive axle, overall height, pivot height, width, bumper width, anchor baseline and drive track drawn from the model, an isometric view and a dimensions box. It carries "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet is PLP-DWG-010, so DWG-001 was free.
- `bom/bom.csv` and `bom/bom-notes.md`: all 18 lines priced with a supplier or supplier type; new line 18 (obstacle lidar); motor spec raised to 30 N·m peak; two lines checked against live listings.
- `cad/src/concept_media.py` now builds the media from `model.py`, with key figures and flow values from PLP-CAL-001. Every image in `media/` was regenerated and checked by eye (exploded callouts reordered by BOM number); the temporary `media/_views*` and `cad/drawings/_views` folders were deleted.
- PLP-PRB-001, PLP-PRC-001 and PLP-REQ-001 revised to v0.3; `README.md` updated (TRL 3, layered stopping, $1,550, links); `project.yaml` set to `trl: 3`, `trl_target: 3`, `budget_usd: 1550`, new pitch, evidence listed. PDFs are in `docs/pdf/`.

### Requirements (PLP-CAL-001, Table 5)

9 met, 3 not met, 3 at risk, 3 not verifiable at TRL 3 (R15 counted as two lines, mass and length).

| ID | Status | Value against target |
| --- | --- | --- |
| R5 | **Not met** | Bearing about ±16° (2σ) after filtering against ±10°; ±10° would need a 706 mm anchor baseline, wider than the 685 mm jack. Gap ±0.06 m is fine |
| R15 mass | **Not met** | 41.7 kg against 40 kg; the 30 N·m motors weigh about 7 kg each |
| R17 | **Not met** | $1,580 against $1,550 ($30, 1.9 %); within motor pricing uncertainty |
| R7 | At risk | Lidar stop 0.42 m level, 0.76 m worst case, inside a 0.86 m field that stays 0.19 m clear of the operator; sensor not safety-rated |
| R8 | At risk | Chain acts in 0.10 s, but 0.2 m/s needs 62 mm of edge travel against 40 mm; 0.15 m/s fits |
| R9 | At risk | Single contactor output; PL d not calculated |
| R1 | Not verifiable at TRL 3 | Needs a donor survey |
| R6 | Not verifiable at TRL 3 | Timing budget 0.20 s against 0.3 s; no firmware |
| R16 | Not verifiable at TRL 3 | Set by bought-part specifications |
| R2, R3, R4, R10, R11, R12, R13, R14, R15 length | Met | 25.5 of 30 N·m; ramp margin 1.54; brakes 40 against 21.7 N·m; handle clearance 40 mm at 70°; 292 of 410 Wh; 4.5 h charge; +3.9 % push force; 290 mm added length |

Other key numbers: traction 750 N at 1.5 kN preload; peak 554 W and 31 A; emergency stop from 1.2 m/s 1.62 m level and 2.66 m on a 2 % downgrade; wall energy 350 Wh per shift.

Design changes made while sizing, within the decided configuration: preload raised from 1.1 to 1.5 kN (R3 was at risk); motor spec raised to 30 N·m peak (the TRL 2 class was too weak); enclosure lowered below the handle pivot (the TRL 2 layout would have hit the handle at about 51°) with the beacon moved to the tiller head and the second emergency stop to the enclosure's rear; drive axle moved 40 mm closer and the track widened to 260 mm (R15 length now met); lidar placed inside the bumper face with its scan plane at 200 mm. Every TRL 2 number in the docs was checked against the script and corrected (PLP-CAL-001, Table 6). TRL 2 overstated the bumper-only safe speed (0.2 m/s; it is 0.15 m/s).

Other findings: the motors cannot swing the yoke at standstill (98 N·m available against 135 N·m of scrub), so follow mode must steer only while rolling, and standstill hand steering gets about 112 N heavier at the grip. The 1,500 kg rating holds on level floors only (a ramp start needs 35.4 N·m per motor).

### Decisions recorded (PLP-DDR-001)

Decided by Amish, 2026-09-25, going with the recommendation: D1 layered stopping with a low-cost lidar layer, bumper last, follow 0.6 m/s, research use in a closed area, safety-rated scanner named for workplace use, pitch "layered stopping"; D2 budget $1,550; D3 dual hub motors on a sprung yoke module; D4 24 V LiFePO4 20 Ah, not SwapCell; D5 everything on the yoke; D6 speeds 1.2, 0.8, 0.3 and 0.6 m/s (follow 0.2 m/s until the lidar layer is tested); D7 1,000 kg design load, 1,500 kg at 0.8 m/s or less; D8 research use now and a jack maker's written approval before any workplace trial; D9 partner types, one small warehouse and one maker space. `budget_usd` is now 1550 and the pitch is reworded in `project.yaml` and `README.md`; the problem line is unchanged (no rewording was recommended). The SwapCell interface decisions do not apply, since PalletPilot has its own pack.

### Proposed, awaiting Amish

1. Named site and co-design partners (O1); partners are picked per area later.
2. Follow-mode classification under ISO 3691-4 (O2). No recommendation.
3. Donor models to support first (O3). No recommendation.
4. Bumper-only stopping (O4, R8): (a) limit bumper-only speed to 0.15 m/s, or (b) an edge with 65 mm or more of travel (adds about 25 mm of length, to about 315 mm, over the 300 mm in R15). Recommendation: (a), since the lidar is the primary layer in follow mode.
5. Overruns (O5): cost $30 over and mass 1.7 kg over. Options: accept both as within estimate uncertainty and recheck when a motor is quoted; choose a lighter motor with published torque; or raise the budget to $1,600. Recommendation: accept for now and recheck at the motor quote, with no budget change. R5: angle-of-arrival UWB or lidar leg tracking; recommendation: evaluate both at TRL 4, when allowed.
6. Stop chain (O6, R9): add a second contactor or a driver with rated safe torque off (about $30). Recommendation: add the second contactor, which would push cost to about $1,610.

### Safety concerns

- The lidar layer is not safety-rated; its range on black targets falls to 6 m and detection of dark clothing at shin height is unproven. Follow mode stays at 0.2 m/s or less in a closed area with no bystanders until tested.
- A 40 mm safety edge stops the loaded truck only from 0.15 m/s or less.
- Emergency braking on a 2 % downgrade needs 2.7 m from 1.2 m/s; no 1,500 kg loads on ramps.
- The 512 Wh LiFePO4 pack needs its BMS, terminal fuse, lockable disconnect and safe charging practice.
- The drive adds up to 750 N of horizontal load at the donor's steering bearing; worn jacks must not be converted.
- Workplace use needs the jack maker's written approval under 29 CFR 1910.178(a)(4) and trained operators.

### Citations

The 1910.178(a)(4) and (l)(1)(i) wording was checked against the OSHA page in this session and now appears as a quotation in PLP-PRB-001. The motor and lidar prices were checked against the listings cited in `bom/bom-notes.md`. No unchecked citation flags remain.

### Gaps against the brief

- Hub motor mass, brake torque and 24 V availability are for the part class, not a quoted motor; R10 and the mass figure rest on the specified minimums.
- No TRL 4 material exists in the repo; `build-log/README.md` is the scaffold file only.

### Recommended next step

TRL 4 is on hold by Amish's instruction. Next, decide items 4 to 6 above, then run a paper follow-up at TRL 3: a donor survey from published jack drawings (yoke geometry, pivot height), a motor quote with brake data, and a PL estimate of the stop chain. For reference only, TRL 4 would need: a bench build of the drive module on one donor jack, measured rolling resistance, friction and stopping distances, lidar detection tests with dark clothing and a test piece, UWB bearing trials, a stop-chain test, a TST report with `environment: lab`, and build log entries.
