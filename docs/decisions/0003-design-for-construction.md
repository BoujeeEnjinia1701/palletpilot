---
doc_id: PLP-DDR-003
title: PalletPilot design for construction
project: PalletPilot
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. The changes in Table 1 were made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 change what the kit does or how it is pitched, so they are Proposed, awaiting Amish, and are listed in the design decisions register (PLP-DEC-001).

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of PalletPilot showed what the kit does, but it was a massing model: several parts had no fixing, floated in space, overlapped other parts, or could not do the job the concept gives them. Checking the model with build123d found the problems in Table 1.

The changes keep what the kit does: the same drive layout (two 200 mm hub motors on a 260 mm track, 180 mm behind the steering axis, 1.5 kN spring preload), the same enclosure under the handle sweep, the same bumper face, lidar scan plane and anchor baseline, the same electrical parts and the same stop chain. The added length (290 mm), handle clearance (40 mm at 70°, 14 mm lowered flat), stopping, traction, energy and tracking figures are unchanged. Every change is in `cad/src/model.py`, which now runs constructability checks (`python cad/src/model.py --check`): 46 pairs of parts that must touch do touch, no two of the 36 components share volume, nothing collides with the release lever raised, and the steering sweep is checked against the jack's frame. All pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The subframe was a 20 mm slab with a clamp block 10 mm short of the yoke and a tongue under it, held by nothing. It could not grip the yoke. | A 6 mm top plate rests on the yoke plate's rear margin with a 62 mm radius notch round the pump. A 10 mm lower jaw goes under the margin, with a packing bar behind the yoke's edge, and four M12 bolts behind the edge pull the jaw and the top plate together, gripping the yoke plate between them. | R1 forbids drilling the jack. The bolts pass behind the yoke's edge, not through it; the pump in the notch stops the plate sliding back, and the packing bar stops it sliding forward. |
| P2 | The trailing cheeks were welded solid to the plate, so the wheels could not move, and the two spring towers floated outside the plate touching nothing. The 1.5 kN preload had nothing to act on. | Each hub motor is carried by its own drive arm (10 mm plate) that pivots on a 20 mm pin in two rear hangers behind the wheels. The arm's front end carries a spring tab; a 100 N/mm spring between the tab and a saddle under a cam pushes the arm, and so the wheel, down. The arm ratio of 1.77 gives 750 N per wheel from 423 N per spring. | A pivoted arm is the simplest sprung mount. The pivot behind the wheel leaves the space ahead of the wheel for the spring and the release, and keeps every part between the steer wheels and the bumper. The stiff spring lets the empty jack's steer wheels lift only about 1.2 mm, as PLP-CAL-001 [C3] asks. |
| P3 | The hub motors sat 5 mm from the cheeks with no shaft between them. | Each motor's fixed shaft passes through the arm's axle hole with a 5 mm spacer inside and a nut outside. | This is how a single-sided hub servo motor is mounted; the shaft size is confirmed when a motor is chosen. |
| P4 | The release lever was a bar along the enclosure side with no pivot and no link to the springs, so it could not lift anything. | A 16 mm cam shaft runs across under the top plate in two front hangers, with a 22 mm eccentric cam above each spring saddle and a crank on its left end. A link joins the crank to an up-arm on a 400 mm lever pivoted on a bracket on the top plate, making a parallelogram. Raising the lever a quarter turn lifts the saddles 22 mm; slotted straps then lift the arms, and the drive wheels clear the floor by 10 mm. With the wheels down the lever lies forward on a stop, over centre. | One lever lifts both wheels (R14) with a peak effort of about 58 N, half the 117 N the concept estimated [G4]. Every moving part was checked in both lever positions. |
| P5 | The bumper was a single solid block, and its mounts ran from the cheeks (which now move with the wheels) to the hoop's sides, which reached forward to 70 mm behind the steering axis. | A U hoop of 40 x 20 x 2 mm tube, its side legs bolted with two M8 bolts each into rivet nuts on brackets welded under the top plate. The safety edge is riveted to the front (50 mm deep, 40 mm travel) and to both sides (20 mm). The side legs start 120 mm behind the steering axis. | The hoop is fixed to the parts that do not spring, so the bumper face stays put. The bumper face, width (480 mm) and edge travel are unchanged, so R8 stands. Edge length is now about 0.9 m, not 1.3 m. |
| P6 | The lidar bracket hung from the subframe in the space the arm pivot now needs. | A bent steel strap screwed to the top of the hoop's front bar carries the lidar shelf. | Scan plane (200 mm) and the lidar's position 10 mm behind the bumper face are unchanged. |
| P7 | The two bumper anchors floated above the bumper with no fixing. | Each anchor sits on a small corner plate on top of the hoop's front corners, its top 180 mm above the floor, below the scan plane. | Baseline (450 mm) unchanged, so the tracking budget [U1] to [U4] stands. |
| P8 | The enclosure had no fixing; the rear emergency stop and the disconnect overlapped its walls. | Four aluminium angle feet riveted to the box sides, each bolted through the top plate with an M8 bolt; holes in the walls for the stop (22 mm) and the disconnect (40 mm). | The box floor stays whole, so nothing inside sits on a bolt head. The box is 89 mm deep plus a 6 mm lid, 95 mm as before. |
| P9 | With the kit on, the yoke cannot turn as far as a bare jack: the drive end reaches the jack's frame head. On the reference donor the top plate's corners met it at 34° and the cams, link and wheels at 44° to 48°. | The top plate's front corners are cut off at 45° (50 mm), and two rubber steering stops under them meet the frame head flat at 40° each way, 4° before any other kit part. | Without stops, steel parts of the kit would strike the jack's frame. The stop angle is set by the donor survey (R1). The range itself is a change to what the kit does: see Table 3, A1. |
| P10 | The donor reference geometry overlapped itself: the steer wheels ran through the yoke plate and the frame head, and the pump through the yoke. | Reference donor corrected: yoke plate 204 to 219 mm above the floor over 180 mm steer wheels, frame head's rear face 100 mm ahead of the steering axis, yoke side legs added. | Reference geometry only; still a survey item (R1, O3). |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Kit 44.4 kg (was 42.0 kg) [B1]: drive module 10.6 kg (was 9.8), release mechanism 3.3 kg (was 0.8), bumper 2.3 kg (was 3.3), steering stops 0.1 kg. R15 mass is now 4.4 kg over its 40 kg target (2.0 kg was accepted for now in PLP-DDR-002). | Made parts are now weighed from their modelled volumes. |
| Cost | BOM lines 1 ($90 to $130), 3 ($45 to $50) and 13 ($20 to $45) repriced and line 19 (steering stops, $10) added: $1,690. Value-engineering target: USD 1,610 (`budget_usd`, unchanged). Estimated cost of the constructable design: USD 1,690 (USD 80 over the target) [K1]. | Parts added for construction. |
| Calculations | PLP-CAL-001 v0.4: mass, loads and forces rerun (design total 1,108 kg; worst motor torque 25.6 N·m of 30; ramp margin 1.53; bumper-only stop 39 mm of 40 mm; 28 % of usable energy left); lever effort [G4] 58 N; steering range [G5]. No requirement changed status. | Follows the model. |
| Drawings | PLP-DWG-001 Rev P4; making sketches PLP-DWG-101 to 111 added; concept blueprint PLP-DWG-010 Rev P2. | Follows the model. |
| Documents | PLP-REQ-001 v0.6 and PLP-PRC-001 v0.6: mass, cost, release and steering figures. | Follows the model. |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Steering range. With the kit fitted the jack steers about 40° each way, against about 90° bare, on the reference donor. The concept says the kit "steers with the handle like the bare jack"; it does not. A wider turn needs more room in aisles. | (a) Accept for the prototype, set the stops from the donor survey and measure the turning circle at TRL 4; (b) narrow the drive end (hoop sides inboard, release moved) for perhaps 48°, at the cost of a narrower anchor baseline and a worse R5; (c) a different drive layout, for example one centre drive wheel under the yoke, which reopens D3. | (a), and state the steering range in the precis and README. |
| A2 | Mass. The kit is 44.4 kg against R15's 40 kg; Amish accepted 2.0 kg over for now. | (a) Accept for the prototype and recheck at the motor quote; (b) lighten now: 5 mm top plate, tube lever, hollow pivot pin (about 1.5 kg). | (a), keeping (b) as savings to try in the TRL 4 drawings. |
| A3 | Wheel lift. The lever lifts the drive wheels 10 mm clear. A larger lift needs a larger cam, which the top plate's height does not leave room for. | (a) Accept 10 mm for smooth indoor floors; (b) lower the cam shaft and raise the hangers for about 15 mm. | (a). |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan PLP-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); open decisions are in PLP-DEC-001.
- Requirement status is unchanged: 10 met, 2 not met (R5, R15 mass), 2 at risk (R7, R9), 3 not verifiable at TRL 3 (R1, R6, R16); R17 is reported against the value-engineering target, USD 80 over.
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept subframe, cheeks, springs and release lever; they need updating on Amish's Mac, where Blender is.
- The donor survey (R1, O3) now sets four numbers in the build: the yoke plate's thickness (packing bar), its rear edge and the pump's position (notch and clamp), and the frame head's position (steering stop angle).
