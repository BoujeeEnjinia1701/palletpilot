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
