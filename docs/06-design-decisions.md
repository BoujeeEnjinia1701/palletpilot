---
doc_id: PLP-DEC-001
title: PalletPilot design decisions register
project: PalletPilot
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; open decisions from PLP-DDR-001 to 003 and the review note; budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Amish accepted the recommendation of open item 1 (steering range, option a, with a TRL 4 aisle test as a go or no-go gate; PLP-DDR-003 A1); moved to decisions made; open items renumbered 1 to 5
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for all five open decisions; moved to decisions made; To confirm item 1 and the value engineering note updated"
---

# PalletPilot design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The donor jack's yoke plate thickness, rear edge position and width, the pump diameter, and the distance from the steering axis to the frame head, for each of the three jacks in the donor survey decided on 2026-10-02 (a Crown PTH 50 series class model, a distributor's standard model such as Uline's, the Harbor Freight Pittsburgh 5,500 lb jack) | They set the packing bar, the clamp holes, the notch and the steering stop angle | PLP-DDR-003; R1 |
| 2 | The hub motor's 24 V winding, peak torque (30 N·m or more), brake holding torque (20 N·m or more), mass and its shaft's diameter and flats | They set the drive arm's axle hole and the mass and stopping figures | PLP-DDR-002; PLP-CAL-001 |
| 3 | The preload spring: about 34 mm outside diameter, about 65 mm free length, about 100 N/mm | It sets the 750 N per wheel preload and the 10 mm wheel lift | PLP-DDR-003; PLP-CAL-001 [G4] |
| 4 | The safety edge profile's travel (40 mm or more at the front), its evaluation unit's category and response time | R8's 0.15 m/s limit rests on 40 mm of travel and a 100 ms chain | PLP-DDR-002; R8 |
| 5 | The tiller head fits the donor handle tube and carries the beacon, stop and anchor | The head clamps on the handle; the grip width is still open in the appearance model | REVIEW (2026-09-26) |
| 6 | The lidar's mounting holes and scan plane height above its base | The bracket shelf is drilled to suit and sets the 200 mm scan plane | PLP-DDR-003 |

## Value engineering

Value-engineering target: USD 1,610 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 1,690 (USD 80 over the target). Main cost drivers and savings worth trying:

- The largest lines are the two hub motors (USD 400), the battery (USD 180), the motor driver (USD 150), the drive module (USD 130) and the contact bumper (USD 110); together they are about 57 % of the kit.
- Making the design constructable added USD 80: the drive module with its clamp, arms and pivot (USD 90 to USD 130), the release mechanism with its cams, link, springs and straps (USD 20 to USD 45), the enclosure feet (USD 5) and the steering stops (USD 10).
- Savings worth trying: a motor sold with its driver as a pair (the class prices run from USD 165 to USD 249 per motor), batching the laser-cut plate parts into one order, and a tube lever and hollow pivot pin, which also save mass (with the 5 mm top plate, about 1.5 kg; to be carried into the TRL 4 drawings, decided 2026-10-02).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D9: layered stopping with a low-cost lidar layer, budget, dual hub motors on a sprung yoke module, 24 V LiFePO4, everything on the yoke, speeds, kit rating, legal route, partner types | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | PLP-DDR-001 |
| 2026-09-25 | Bumper-only speed limited to 0.15 m/s (O4); mass and cost overruns accepted for now, R5 fixes evaluated at TRL 4 (O5); a second main contactor in series (O6) | Amish: "i accept all your recommendations, go with them across all repos." | PLP-DDR-002 |
| 2026-09-26 | Budget set to USD 1,610 to cover the priced BOM | Amish: "i approve all the budget items." | PLP-DDR-002 v0.2 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; outstanding decisions go in this register, not in the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | PLP-DDR-003 (Draft, open for review) |
| 2026-10-01 | The budget is a value-engineering target, reported as over or under, never as a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | This register; PLP-CAL-001 v0.4 |
| 2026-10-01 | Steering range (open item 1 in register v0.1): option (a). Accept about 40° each way with the kit fitted for the prototype (a bare jack turns about 90°), turning radius roughly 1.5 m about the load wheels; set the rubber stops from the donor survey; the precis, README and requirements no longer say the kit steers like the bare jack. **Go or no-go gate:** the TRL 4 aisle test must show the kit can make a right-angle turn into a standard pallet bay; if it cannot, the drive layout changes before TRL 5 (option c, for example one centre drive wheel under the yoke, which reopens D3) | Amish: "i accept your recommendations for PalletPilot" | PLP-DDR-003, A1 |
| 2026-10-02 | Kit mass of 44.4 kg accepted for the prototype (option a); R15's prototype limit restated as 45 kg, rechecked at the motor quote, and the 1.5 kg of savings of option (b) (5 mm top plate, tube lever, hollow pivot pin) carried into the TRL 4 drawings (open item 1) | Amish: "i approve your recommendations for all 555 open decisions." | PLP-DDR-003, A2 |
| 2026-10-02 | Drive wheel lift of 10 mm accepted for smooth indoor floors (option a); the build plan states that the release is for indoor floors only (open item 2) | Amish: "i approve your recommendations for all 555 open decisions." | PLP-DDR-003, A3 |
| 2026-10-02 | Follow mode is treated as a driverless truck function under ISO 3691-4, with personnel detection and stopping functions to that standard; it is reclassified as an operator-controlled assist mode only if a standards body or a notified body confirms that the walking follower counts as the operator (open item 3) | Amish: "i approve your recommendations for all 555 open decisions." | PLP-DDR-001, O2 |
| 2026-10-02 | Donor jacks to support first: a survey of three widely sold 27 x 48 in, 2,500 kg hand pallet jacks with published dimensioned drawings, a professional model such as the Crown PTH 50 series, a distributor's standard model such as Uline's, and the low-cost Harbor Freight Pittsburgh 5,500 lb jack (open item 4) | Amish: "i approve your recommendations for all 555 open decisions." | PLP-DDR-001, O3 |
| 2026-10-02 | Partners near Irving: Dallas Makerspace as the first candidate maker space, and a small food bank or charity warehouse in the Dallas and Fort Worth area as the first candidate warehouse, which trials only after the jack maker's written approval under D8 (open item 5) | Amish: "i approve your recommendations for all 555 open decisions." | PLP-DDR-001, O1 |
