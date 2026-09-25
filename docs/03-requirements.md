---
doc_id: PLP-REQ-001
title: PalletPilot requirements
project: PalletPilot
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# PalletPilot requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3 and revised after site visits (see PLP-PRB-001). The status column compares each target with the first-order estimates in PLP-PRC-001; every status is an estimate until verified.

The **design load case** is a 1,000 kg pallet on a 64 kg donor jack with a kit of about 37 kg, about 1,100 kg in total, on a level, dry, sealed concrete floor.

The **design duty** is one 8 h shift of 60 pallet moves, each 40 m loaded and 40 m empty, with four starts in each direction.

Table 1. Requirements.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (estimate) |
| --- | --- | --- | --- | --- |
| R1 | Fit a common manual jack | Bolts to 27 x 48 in (685 x 1220 mm), 2,500 kg manual jacks with a common steering yoke; no welding, cutting or drilling of load-bearing parts; fitted in 2 h or less and removed in 1 h or less with hand tools | Survey of three donor models; fitting sequence review | Unverified; yoke patterns vary |
| R2 | Move the design load | Start and move 1,000 kg on a level floor; kit rating 1,500 kg at reduced speed (0.8 m/s or less), below the donor rating | Traction and torque calculation | Met on paper at 1,000 kg; traction margin thin at 1,500 kg |
| R3 | Handle short ramps | Start, climb and hold the design load on a 2 % grade | Traction, torque and brake calculation | **At risk**: needs about 350 N of 550 N available traction |
| R4 | Walking-pace speeds | Walk mode 1.2 m/s (4.3 km/h) or less handle-end first and 0.8 m/s or less forks first; creep 0.3 m/s or less with the handle near upright; follow mode 0.6 m/s or less | Controller limits; later timed runs | Met by design (software limits) |
| R5 | Follow the operator | In follow mode, hold a 1.5 m gap within ±0.3 m and a bearing within ±10° of the tag at walking pace | UWB error budget; later tracking trials | **Not met on paper**: raw bearing error about ±18° with a 450 mm anchor baseline; needs filtering or angle-of-arrival sensing |
| R6 | Stop if the operator is lost | Stop within 0.3 s of losing the tag link, a gap over 3 m, a tag stop press or the tag leaving a ±45° cone | Firmware design review; later bench test | Unverified |
| R7 | Stop before hitting a person in follow mode | Detect a person in the travel path and stop without contact from 0.6 m/s with the design load | Stopping calculation; later test with an ISO 3691-4 style test piece | **Not met**: a contact bumper alone cannot stop 1,100 kg from 0.6 m/s within its travel (about 0.42 m stop versus about 40 mm travel); needs non-contact sensing or a lower speed |
| R8 | Stop on bumper contact | Bumper contact removes drive power and applies the brakes within 100 ms; bumper-only stopping limited to 0.2 m/s or less | Stop chain design review | Met by design at 0.2 m/s (about 0.06 m stop) |
| R9 | Emergency stop | Two hardwired emergency stops (tiller head and enclosure) plus the tag stop; the hardwired stops cut drive power through a safety relay and contactor, independent of software; target performance level PL d under ISO 13849-1 | Stop chain review; PL calculation at TRL 3 | Unverified |
| R10 | Park safely | Brakes apply with power off and hold the design load on a 2 % grade | Brake torque check against datasheet | Unverified; needs about 22 N·m holding torque in total |
| R11 | Keep the operator in control | Walk mode drives only with the handle between about 20° and 70° from vertical; belly-reverse paddle on the tiller head reverses the truck when pressed | Design review | Met by design |
| R12 | Work a full shift | Complete the design duty on one charge with 20 % or more of usable energy left | Energy calculation | Met: about 281 Wh used of about 410 Wh usable (31 % left) |
| R13 | Charge overnight | Full charge in 5 h or less from a 120 V or 230 V outlet through a certified charger | Charger datasheet | Met: about 4.5 h at 5 A |
| R14 | Push by hand when unpowered | One lever lifts the drive wheels clear and releases the brakes in 10 s or less; unpowered push force no more than 10 % above the bare jack | Design review; later push-force test | Unverified |
| R15 | Keep the jack usable | Kit mass 40 kg or less; overall length increase 300 mm or less; lowered fork height and pallet entry unchanged | Mass estimate; model check | **Partly met**: about 37 kg, but about 330 mm longer at floor level with the bumper (about 100 mm beyond the upright handle) |
| R16 | Indoor environment | Operate at 0 to 40 °C; electronics and connectors IP54; no charging below 0 °C | Datasheets and design review | Unverified |
| R17 | Affordable | Kit parts cost $1,200 or less, donor jack excluded | Priced BOM (`bom/bom.csv`) | **Not met**: about $1,425, about 19 % over |

## Requirements not met or at risk

- **R7, non-contact stopping in follow mode, is not met.** This is the main finding of the concept. See PLP-PRC-001, "Stopping".
- **R5, follow bearing accuracy, is not met on paper** with two range-only anchors; it may be met with filtering or angle-of-arrival modules.
- **R17, cost, is not met** by about $225. A walk-only variant costs about $1,075.
- **R3, the 2 % ramp, is at risk** on traction margin.
- **R15 is partly met.** Mass is within target, but the drive module and bumper add about 330 mm at floor level, 30 mm over the target, which widens the turning circle in tight aisles.

## Assumptions

- Rolling resistance 1.2 % and breakaway resistance 2.5 % for polyurethane steer and load wheels on smooth concrete. These are assumptions to be measured on a real jack.
- Tread-to-floor friction coefficient 0.5 for the drive wheels on dusty concrete; lower on wet or polished floors.
- The drive wheels carry about 1.1 kN of spring preload and no share of the pallet load.
- Motor plus driver efficiency 70 %; controls, UWB and lights draw about 8 W in total.
- Operator reaction and stop-chain delay of 0.1 s in follow mode.
- The legal status of the retrofit (OSHA 1910.178(a)(4)) and of follow mode (ISO 3691-4) is open; targets R7 and R9 anticipate the stricter answer.
