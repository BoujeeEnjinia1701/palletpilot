---
doc_id: PLP-DEC-001
title: PalletPilot design decisions register
project: PalletPilot
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; open decisions from PLP-DDR-001 to 003 and the review note; budget treated as a value-engineering target
---

# PalletPilot design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Steering range with the kit fitted: about 40° each way on the reference donor, against about 90° bare; the concept said the kit steers like the bare jack | (a) Accept for the prototype, set the stops from the donor survey, measure the turning circle at TRL 4; (b) narrow the drive end for perhaps 48°, which narrows the anchor baseline and worsens R5; (c) a different drive layout, reopening D3 | (a), and state the range in the precis and README | Steering stop position (section 3.2); pitch wording | PLP-DDR-003, A1 |
| 2 | Kit mass of 44.4 kg against R15's 40 kg (2.0 kg over was accepted for now) | (a) Accept for the prototype and recheck at the motor quote; (b) lighten now (5 mm top plate, tube lever, hollow pivot pin, about 1.5 kg) | (a), keeping (b) for the TRL 4 drawings | Plate thickness, lever and pin stock | PLP-DDR-003, A2 |
| 3 | Drive wheel lift of 10 mm with the release lever raised | (a) Accept for smooth indoor floors; (b) lower the cam shaft and raise the hangers for about 15 mm | (a) | Cam throw, hanger height | PLP-DDR-003, A3 |
| 4 | Classification of follow mode under ISO 3691-4 and the safety functions it then needs | Classify as a driverless truck function, or as an operator-controlled truck with an assist mode | None yet | Not part of the TRL 3 build; sets the stop functions and sensor rating needed later | PLP-DDR-001, O2 |
| 5 | Donor jack models and steering yokes to support first | Survey three common 27 x 48 in, 2,500 kg jacks from published drawings | None yet | Packing bar thickness, clamp and notch, steering stop angle | PLP-DDR-001, O3 |
| 6 | Named site and co-design partners (types decided: one small warehouse, one maker space) | Picked per area later | None yet | None in the build | PLP-DDR-001, O1 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The donor jack's yoke plate thickness, rear edge position and width, the pump diameter, and the distance from the steering axis to the frame head | They set the packing bar, the clamp holes, the notch and the steering stop angle | PLP-DDR-003; R1 |
| 2 | The hub motor's 24 V winding, peak torque (30 N·m or more), brake holding torque (20 N·m or more), mass and its shaft's diameter and flats | They set the drive arm's axle hole and the mass and stopping figures | PLP-DDR-002; PLP-CAL-001 |
| 3 | The preload spring: about 34 mm outside diameter, about 65 mm free length, about 100 N/mm | It sets the 750 N per wheel preload and the 10 mm wheel lift | PLP-DDR-003; PLP-CAL-001 [G4] |
| 4 | The safety edge profile's travel (40 mm or more at the front), its evaluation unit's category and response time | R8's 0.15 m/s limit rests on 40 mm of travel and a 100 ms chain | PLP-DDR-002; R8 |
| 5 | The tiller head fits the donor handle tube and carries the beacon, stop and anchor | The head clamps on the handle; the grip width is still open in the appearance model | REVIEW (2026-09-26) |
| 6 | The lidar's mounting holes and scan plane height above its base | The bracket shelf is drilled to suit and sets the 200 mm scan plane | PLP-DDR-003 |

## Value engineering

Value-engineering target: USD 1,610 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 1,690 (USD 80 over the target). Main cost drivers and savings worth trying:

- The largest lines are the two hub motors (USD 400), the battery (USD 180), the motor driver (USD 150), the drive module (USD 130) and the contact bumper (USD 110); together they are about 57 % of the kit.
- Making the design constructable added USD 80: the drive module with its clamp, arms and pivot (USD 90 to USD 130), the release mechanism with its cams, link, springs and straps (USD 20 to USD 45), the enclosure feet (USD 5) and the steering stops (USD 10).
- Savings worth trying: a motor sold with its driver as a pair (the class prices run from USD 165 to USD 249 per motor), batching the laser-cut plate parts into one order, and a tube lever and hollow pivot pin, which also save mass.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D9: layered stopping with a low-cost lidar layer, budget, dual hub motors on a sprung yoke module, 24 V LiFePO4, everything on the yoke, speeds, kit rating, legal route, partner types | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | PLP-DDR-001 |
| 2026-09-25 | Bumper-only speed limited to 0.15 m/s (O4); mass and cost overruns accepted for now, R5 fixes evaluated at TRL 4 (O5); a second main contactor in series (O6) | Amish: "i accept all your recommendations, go with them across all repos." | PLP-DDR-002 |
| 2026-09-26 | Budget set to USD 1,610 to cover the priced BOM | Amish: "i approve all the budget items." | PLP-DDR-002 v0.2 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; outstanding decisions go in this register, not in the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | PLP-DDR-003 (Draft, open for review) |
| 2026-10-01 | The budget is a value-engineering target, reported as over or under, never as a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | This register; PLP-CAL-001 v0.4 |
