---
doc_id: PLP-REQ-001
title: PalletPilot requirements
project: PalletPilot
doc_type: Requirements
version: "0.6"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record decisions PLP-DDR-001 (R7 redefined for the lidar layer, R17 to $1,550, 1,500 kg on level floors); status from PLP-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: "Constructable design (PLP-DDR-003): mass, release and cost figures; R17 reported against the value-engineering target"
---

# PalletPilot requirements

These requirements are checked by calculation in PLP-CAL-001. Ten of eighteen requirement lines are met on paper, two are not met (R5 bearing accuracy, R15 kit mass), two are at risk (R7, R9), three cannot be verified at TRL 3 (R1, R6, R16), and R17 is reported against its value-engineering target. Targets are still to be validated with users after site visits (see PLP-PRB-001). Decisions recorded in PLP-DDR-001 on 2026-09-25 changed R2, R4, R7 and R17; decisions in PLP-DDR-002 on the same date restated R4 and R8 (bumper-only and untested follow mode at 0.15 m/s) and R9 (two contactors in series). On 2026-09-26 Amish approved the budget of $1,610 (PLP-DDR-002); on 2026-10-01 he set budgets as value-engineering targets, not limits, so R17 is reported as over or under the target. On 2026-10-01 the design was made constructable (PLP-DDR-003, Draft): the kit mass and cost rose and the release lever was resized; no requirement changed status.

The **design load case** is a 1,000 kg pallet on a 64 kg donor jack with a kit of about 44.4 kg, about 1,108 kg in total, on a level, dry, sealed concrete floor.

The **design duty** is one 8 h shift of 60 pallet moves, each 40 m loaded and 40 m empty, with four starts in each direction.

Table 1. Requirements.

| ID | Requirement | Target | Verification | Status (PLP-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Fit a common manual jack | Bolts to 27 x 48 in (685 x 1220 mm), 2,500 kg manual jacks with a common steering yoke; no welding, cutting or drilling of load-bearing parts; fitted in 2 h or less and removed in 1 h or less with hand tools | Survey of three donor models; fitting sequence review | Not verifiable at TRL 3; the model assumes one donor geometry |
| R2 | Move the design load | Start and move 1,000 kg on a level floor; kit rating 1,500 kg at 0.8 m/s or less on level floors, below the donor rating (decided, PLP-DDR-001 D7) | Traction and torque calculation | Met: 25.5 N·m per motor needed of 30 N·m specified; 750 N traction. A 1,500 kg ramp start is outside the rating |
| R3 | Handle short ramps | Start, climb and hold the design load on a 2 % grade | Traction, torque and brake calculation | Met: start needs 488 N of 750 N (margin 1.54, 1.23 at friction 0.4) |
| R4 | Walking-pace speeds | Walk mode 1.2 m/s (4.3 km/h) or less handle-end first and 0.8 m/s or less forks first; creep 0.3 m/s or less with the handle near upright; follow mode 0.6 m/s or less, and 0.15 m/s or less until the lidar layer is built and tested (decided, PLP-DDR-001 D6; interim limit lowered from 0.2 m/s to the bumper-only limit by PLP-DDR-002) | Controller limits; later timed runs | Met by design (software limits) |
| R5 | Follow the operator | In follow mode, hold a 1.5 m gap within ±0.3 m and a bearing within ±10° (2σ) of the tag at walking pace | UWB error budget; later tracking trials | **Not met**: gap ±0.06 m, but bearing about ±16° with a 450 mm anchor baseline and filtering |
| R6 | Stop if the operator is lost | Stop command within 0.3 s of losing the tag link, a gap over 3 m, a tag stop press or the tag leaving a ±45° cone | Firmware design review; later bench test | Not verifiable at TRL 3; timing budget 0.20 s |
| R7 | Stop before hitting a person in follow mode | The lidar layer detects a person in the travel path and the truck stops without contact from 0.6 m/s with the design load, with the bumper as the last layer (redefined for option 1A, D1) | Stopping calculation; later test with an ISO 3691-4 style test piece | **At risk**: stop 0.42 m level and 0.76 m worst case, inside a 0.86 m protective field; the sensor is not safety-rated and detection of dark clothing is unproven |
| R8 | Stop on bumper contact | Bumper contact removes drive power and applies the brakes within 100 ms; any operation that relies on the bumper alone limited to 0.15 m/s or less (decided, PLP-DDR-002; was 0.2 m/s) | Stop chain design review | Met on paper: 0.10 s chain; 0.15 m/s stops in 38 mm of the 40 mm edge travel |
| R9 | Emergency stop | Two hardwired emergency stops (tiller head and enclosure) plus the tag stop; the hardwired stops cut drive power through a dual-channel safety relay and two main contactors in series (decided, PLP-DDR-002), independent of software; target performance level PL d under ISO 13849-1 | Stop chain review; PL calculation | **At risk**: dual-channel relay and two contactors in series; PL not yet calculated |
| R10 | Park safely | Brakes apply with power off and hold the design load on a 2 % grade | Brake torque check against datasheet | Met on paper: 40 N·m specified against 21.7 N·m needed; datasheet to confirm |
| R11 | Keep the operator in control | Walk mode drives only with the handle between about 20° and 70° from vertical; belly-reverse paddle on the tiller head reverses the truck when pressed | Design review; model check | Met: the handle clears the enclosure by 40 mm at 70° and 14 mm when lowered flat |
| R12 | Work a full shift | Complete the design duty on one charge with 20 % or more of usable energy left | Energy calculation | Met: 293 Wh used of 410 Wh usable (28 % left) |
| R13 | Charge overnight | Full charge in 5 h or less from a 120 V or 230 V outlet through a certified charger | Charger datasheet | Met: 4.5 h at 5 A |
| R14 | Push by hand when unpowered | One lever lifts the drive wheels clear in 10 s or less (brakes need no release once the wheels are clear); unpowered push force no more than 10 % above the bare jack | Design review; later push-force test | Met on paper: +4.2 % push force; peak lever effort about 58 N; drive wheels lift about 10 mm (PLP-DDR-003) |
| R15 | Keep the jack usable | Kit mass 40 kg or less; overall length increase 300 mm or less at floor level; lowered fork height and pallet entry unchanged | Mass estimate; model check | **Partly met**: 290 mm added length (met); 44.4 kg (**not met**, 4.4 kg over; 2.0 kg over was accepted for now in PLP-DDR-002; the rest is open decision 2 in PLP-DEC-001) |
| R16 | Indoor environment | Operate at 0 to 40 °C; electronics and connectors IP54; no charging below 0 °C | Datasheets and design review | Not verifiable at TRL 3; set by the specification of bought parts |
| R17 | Affordable | Kit parts cost against the value-engineering target of $1,610, donor jack excluded (budget decided, D2; $1,610 approved by Amish, 2026-09-26, PLP-DDR-002; a target, not a limit, 2026-10-01) | Priced BOM (`bom/bom.csv`) | Value-engineering target: USD 1,610. Estimated cost of the constructable design: USD 1,690 (USD 80 over the target) |

## Requirements not met or at risk

- **R5, follow bearing accuracy, is not met.** Filtering brings the error to about ±16°; ±10° would need a 706 mm anchor baseline, wider than the jack. Amish decided to evaluate angle-of-arrival modules and lidar leg tracking at TRL 4, which is on hold (PLP-DDR-002).
- **R15 mass is not met** by 4.4 kg. The 30 N·m class hub motors weigh about 7 kg each; the second contactor adds 0.3 kg; the parts added to make the design constructable (clamp jaw, drive arms, pivot pin, cam shaft and lever) add 2.4 kg (PLP-DDR-003). Amish accepted 2.0 kg over for now, to be rechecked at the motor quote (PLP-DDR-002); the larger figure is open decision 2 in PLP-DEC-001.
- **R17, cost, is USD 80 over its value-engineering target**: USD 1,690 against USD 1,610. Savings worth trying are listed in PLP-DEC-001.
- **R7 is at risk.** The stopping distances fit the lidar field on paper, but the sensor is not safety-rated, so this cannot support an ISO 3691-4 claim.
- **R9 is at risk** until the stop chain, now with two contactors in series, has a PL calculation.

## Assumptions

- Rolling resistance 1.2 % and breakaway resistance 2.5 % for polyurethane steer and load wheels on smooth concrete. These are assumptions to be measured on a real jack.
- Tread-to-floor friction coefficient 0.5 for the drive wheels on dusty concrete, 0.4 as a low case; lower on wet or polished floors.
- The drive wheels carry 1.5 kN of spring preload and no share of the pallet load.
- Motor plus driver efficiency 70 %; controls, UWB, lidar and lights draw about 9.2 W in total.
- Stop delays of 0.25 s for the lidar layer and 0.10 s for the bumper and emergency stops.
- R8 is met by the 0.15 m/s speed limit, not by a longer-travel edge; a firmware or hardware fault that lets the truck exceed 0.15 m/s in a bumper-only mode would defeat it.
- The legal status of the retrofit (OSHA 1910.178(a)(4)) and of follow mode (ISO 3691-4) is open; targets R7 and R9 anticipate the stricter answer. The kit is documented for research use in a closed area (D8).
