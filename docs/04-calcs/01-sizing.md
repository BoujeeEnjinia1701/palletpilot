---
doc_id: PLP-CAL-001
title: PalletPilot sizing calculations
project: PalletPilot
doc_type: Calculation
version: "0.3"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (mass, axle loads, traction, torque, steering, layered stopping, UWB error budget, energy, geometry, cost, requirement status)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($1,550 to $1,610, PLP-DDR-002); script rerun; R17 not met to met
---

# PalletPilot sizing calculations

On paper, PalletPilot meets eleven of its eighteen requirement lines, misses two, has two at risk, and three cannot be verified at TRL 3. The drive, ramp, bumper, energy, charging, parking, handle clearance, length and hand-push targets are met. The misses are follow-mode bearing accuracy (R5, about ±16° against ±10°) and kit mass (R15, 42.0 kg against 40 kg). Cost (R17) is met with no margin: $1,610 against the $1,610 budget Amish approved on 2026-09-26 (it was $1,550 in v0.2). Version 0.2 applies Amish's 2026-09-25 decisions in PLP-DDR-002: the bumper-only speed is limited to 0.15 m/s (R8 now met), a second main contactor is added to the stop chain (+$30, +0.3 kg), and the mass and cost overruns are accepted for now with no budget change. Version 0.3 applies only the budget change to $1,610 (PLP-DDR-002); no design number changed. The approved lidar layer stops the loaded truck from 0.6 m/s in 0.42 to 0.76 m, inside a 0.86 m protective field that stays clear of the operator it follows. That is the core of the layered-stopping case, but the sensor is not safety-rated, so R7 stays at risk. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [F3], is the line of the script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept of moving machinery that carries up to 1.6 t near people's feet, with a 512 Wh lithium pack. They do not replace brake, stop-chain, detection or electrical tests, and they give no basis for ISO 3691-4 or ISO 13849-1 claims. Nothing may be built or run on the strength of this note. See PLP-PRC-001, Safety.

## Scope and method

The note checks every requirement in PLP-REQ-001 v0.4 against the design in PLP-PRC-001 v0.4, as decided in PLP-DDR-001 and PLP-DDR-002. The script imports `PARAMS` and `derived()` from `cad/src/model.py`, so the geometry here matches the STEP files and drawing PLP-DWG-001, and it reads the BOM total from `bom/bom.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Loads | 1,000 kg design pallet, 1,500 kg maximum; donor jack 64 kg; pallet center 615 mm from the frame head; 45 % of the jack's mass on the steer axle | PLP-REQ-001; 48 x 40 in pallet centered on 48 in forks |
| Floor | Rolling resistance 1.2 %, breakaway 2.5 %; drive tread friction 0.5 on dusty sealed concrete, 0.4 as a low case | Polyurethane wheels on concrete; to be measured |
| Drive | Two 200 mm hub motors; spring preload 1.5 kN on the pair (raised from 1.1 kN at TRL 2); specified minimums of 12 N·m continuous, 30 N·m peak and 20 N·m spring-brake torque per motor | Motor class data: 20/40 N·m ([UU Motor SVB8S](https://www.uumotor.com/high-torque-500w-robot-8-inch-servo-hub-motor.html)) and 40/80 N·m ([ZLTECH 8 in](https://zltech-hubmotor.en.made-in-china.com/product/NOgmzpqvCLhr/China-Zltech-8inch-24V-48V-200rpm-300kg-Load-Gearless-Electric-DC-Agv-Direct-Drive-Wheel-Hub-Servo-Motor-with-Encoder-for-Forklift.html)); brake torque to confirm |
| Acceleration | 0.3 m/s² level, 0.1 m/s² on the 2 % ramp, 0.2 m/s² at 1,500 kg | Controller settings |
| Stopping | Lidar layer: controlled stop by the motor driver, delay 0.25 s (two 10 Hz scans plus processing). Bumper and emergency stops: safety relay drops the two series contactors and the spring brakes act, delay 0.10 s. Tag loss: three missed frames at 20 Hz plus command, 0.20 s | [RPLIDAR C1](https://www.dfrobot.com/product-2803.html) scans at 8 to 12 Hz; relay and brake times typical of the part class |
| Follow geometry | Gap 1.5 m ± 0.3 m; tag worn at the front of the body, 0.15 m from the back of the legs | R5 |
| UWB | Range noise 0.10 m (1σ) per anchor; 20 Hz, averaged over 0.5 s (10 samples); correlated error 0.03 m per range from multipath and body shadowing; R5's ±10° read as a 2σ bound | [Qorvo DWM3000](https://www.qorvo.com/products/p/DWM3000) about 10 cm precision; correlated error is an assumption |
| Energy | 60 moves of 40 m loaded and 40 m empty, four starts each way to 1.2 m/s; no regeneration; motor and driver 70 %; controls, UWB, lidar and lights 9.2 W; 80 % usable depth; cell 95 %, charger 88 % | PLP-REQ-001 design duty |
| Mass | Hub motor 7.0 kg each (class range 3 to 8.5 kg); 6 mm steel subframe; 2 mm aluminium enclosure; 8S6P 26650 pack | Motor class data above; plate areas from the model |

## Mass and axle loads

The kit weighs about 42.0 kg on the truck [B1], 2.0 kg over R15; the second contactor adds 0.3 kg. The two hub motors (14 kg) and the subframe (9.8 kg) are nearly 60 % of it [B0]. The design total is 1,106 kg, and 1,606 kg with a 1,500 kg pallet [B2].

The steer axle carries 41.5 % of the pallet. The yoke's ground load is 4.77 kN at 1,000 kg and 6.81 kN at 1,500 kg [C1]. With 1.5 kN of spring preload on the drive wheels, the steer wheels keep 3.27 kN at the design load [C2]. With the jack empty, the yoke load (0.69 kN) is below the preload, so the steer wheels lift and the drive wheels carry the yoke; traction is then 0.33 g, which is ample [C3]. The spring travel stop must be set so the steer wheels lift only a few millimeters.

The kit hangs on the yoke, so it adds no vertical load to the jack's steering bearing, which carries 4.36 kN at 1,000 kg against 10.47 kN at the donor's rating. The bearing does take up to 750 N of horizontal drive force [C4], about 2.8 times the breakaway pull of a person, which makes bearing condition a donor survey item.

## Forces, traction and torque

*Table 2. Drive cases, design total unless stated [F1 to F4].*

| Case | Force | Torque per motor | Traction margin, friction 0.5 / 0.4 |
| --- | --- | --- | --- |
| Level start (breakaway) | 271 N | 13.6 N·m | 2.76 / 2.21 |
| Level, accelerate 0.3 m/s² | 462 N | 23.1 N·m | 1.62 / 1.30 |
| 2 % ramp start (breakaway plus grade) | 488 N | 24.4 N·m | 1.54 / 1.23 |
| 2 % ramp, accelerate 0.1 m/s² | 458 N | 22.9 N·m | 1.64 / 1.31 |
| 1,500 kg level, accelerate 0.2 m/s² | 510 N | 25.5 N·m | 1.47 / 1.18 |
| 1,500 kg, 2 % ramp start | 709 N | 35.4 N·m | 1.06 / 0.85 |

Raising the preload from 1.1 to 1.5 kN lifts the available traction from 550 to 750 N [F2], which turns R3 from at risk into met with a margin of 1.54. The worst case inside R2 and R3 needs 25.5 N·m per motor against the specified 30 N·m peak [F4]. A 1,500 kg ramp start needs 35.4 N·m and has almost no traction margin, so **the 1,500 kg rating applies to level floors only**. The TRL 2 motor class (about 16 N·m peak) is too weak; the BOM now calls for a 30 N·m peak class motor.

Cruising at 1.2 m/s loaded takes 6.5 N·m per motor against 12 N·m continuous, at 115 rpm [F5]. Peak wheel power is 554 W while accelerating, drawing about 31 A from the pack, about 15 A per driver channel [F6]. The 2 x 15 A continuous, 30 A peak driver and the 50 A BMS cover this.

**Steering finding.** The drive axle sits 180 mm from the steering axis, toward the handle end. The motors' differential push can produce about 98 N·m about the steering axis, but swinging the yoke at standstill scrubs the drive wheels sideways and needs about 135 N·m [F7]. The motors therefore cannot steer at standstill; follow mode must steer only while rolling, when the wheels follow arcs and the scrub disappears. With the drive end leading in follow mode, the yoke trails behind the drive axle, which is the stable arrangement. In walk mode, standstill steering by hand gets heavier by about 112 N at the grip [F8] until the truck rolls. No requirement covers steering effort; see REVIEW.md.

## Layered stopping

Braking force is limited by motor torque in a controlled stop (600 N) and by the spring brakes in an emergency stop (400 N) [S1]. Rolling resistance adds to both.

*Table 3. Stopping distances [S2].*

| Case | Deceleration | Stop | Kinetic energy |
| --- | --- | --- | --- |
| Walk 1.2 m/s, controlled, level | 0.66 m/s² | 1.21 m | 796 J |
| Walk 1.2 m/s, emergency stop, level | 0.48 m/s² | 1.62 m | 796 J |
| Walk 1.2 m/s, emergency stop, 2 % downgrade | 0.28 m/s² | 2.66 m | 796 J |
| Follow 0.6 m/s, lidar stop, level | 0.66 m/s² | 0.42 m | 199 J |
| Follow 0.6 m/s, lidar stop, 2 % downgrade | 0.46 m/s² | 0.54 m | 199 J |
| Follow 0.6 m/s, lidar stop, 1,500 kg, 2 % downgrade | 0.30 m/s² | 0.76 m | 289 J |
| Follow 0.6 m/s, bumper only, level | 0.48 m/s² | 0.44 m | 199 J |
| Creep 0.3 m/s, bumper only, level | 0.48 m/s² | 0.12 m | 50 J |
| 0.15 m/s bumper-only limit, level | 0.48 m/s² | 0.038 m | 12 J |
| 0.2 m/s, bumper only, level (v0.1 limit, for comparison) | 0.48 m/s² | 0.062 m | 22 J |

**Lidar layer (approved option 1A).** A 2D lidar sits just inside the bumper face with its scan plane 200 mm above the floor, above the bumper hoop and the UWB anchors [G3]. A protective field of 0.86 m ahead of the bumper face (the worst lidar stop plus 0.1 m) [S4] covers every follow case in Table 3. It is 885 mm wide, the jack width plus 100 mm each side [S5]. The operator's legs are at least 1.05 m from the bumper at the minimum gap, so the field stays clear of the person being followed by 0.19 m. A slow-down field beyond it should cut speed before a stop is needed. The distances fit on paper, but the sensor is not safety-rated, its range on black targets falls to 6 m, and its detection of dark or shiny clothing at shin height is unproven. **R7 is therefore at risk, not met**, and no ISO 3691-4 claim can be made.

**Bumper layer.** The chain acts in 0.10 s, which meets R8's 100 ms. The speed that stops within the edge's 40 mm travel is 0.15 m/s [S3]. Amish decided on 2026-09-25 to limit bumper-only operation to 0.15 m/s (PLP-DDR-002, O4) rather than fit a longer-travel edge. At that limit the truck travels 38 mm after contact, inside the 40 mm travel, so **R8 is met on paper**; at the former 0.2 m/s it would need 62 mm. Because the lidar layer is untested, follow mode also runs at 0.15 m/s or less until that layer is built and tested. The stop chain now drops two main contactors in series, one per safety relay channel (PLP-DDR-002, O6); the performance level is still to be calculated, so R9 stays at risk.

**Tag loss.** The stop command follows 0.20 s after the last good frame, inside R6's 0.3 s [S6]; the firmware does not exist, so R6 cannot be verified at TRL 3.

**Parking.** Holding the design load on 2 % needs 21.7 N·m in total; the specified brakes give 40 N·m, a margin of 1.84 [S7].

## Follow-me tracking: UWB error budget

Two anchors 450 mm apart give a raw bearing error of 18.0° (1σ) [U1]. Averaging 10 samples brings the random part to 5.7°, but the correlated part (5.4°) does not average out; the total is 7.8° (1σ), or about ±16° at 2σ against ±10° [U2]. Meeting R5 with this filter would need a 706 mm baseline, wider than the 685 mm jack [U3]. At the 1.5 m gap, ±16° is about 0.42 m of lateral error [U4]. The gap itself is held to about ±0.06 m, well within ±0.3 m. **R5 is not met on paper.** The routes are phase-difference angle-of-arrival UWB modules, fusing the lidar's track of the operator's legs with the UWB range, or accepting a wider bearing band; each needs a bench measurement, which is TRL 4 work.

## Energy and charging

*Table 4. Energy per shift [E1 to E4].*

| Quantity | Value |
| --- | --- |
| Work at the wheels | 153 Wh (2.56 Wh per move) |
| Motor driver input | 219 Wh |
| Controls, UWB, lidar and lights | 74 Wh |
| Energy from the pack | 293 Wh of 410 Wh usable (29 % left) |
| Energy from the wall | 350 Wh |
| Charge time at 5 A | 4.5 h |

R12 (20 % left) and R13 (5 h) are met. The lidar adds about 10 Wh per shift.

## Geometry

The TRL 2 enclosure sat above the handle pivot, so the lowered handle would have hit its lid at about 51° from vertical, inside the 20° to 70° walk band. The TRL 3 model lowers the enclosure top to 320 mm, below the 350 mm pivot, and moves the beacon to the tiller head and the second emergency stop to the enclosure's rear face. The handle now clears the enclosure by 40 mm at 70° and by 14 mm when fully lowered [G1]. The pivot height varies between jacks, so this is a donor survey item.

Moving the drive axle 40 mm closer to the steering axis and widening the drive track to 260 mm, so the drive wheels pass beside the steer wheels, brings the added length at floor level to 290 mm, within R15's 300 mm [G2]. The truck is 1,710 mm long at floor level against 1,420 mm bare.

The release lever (400 mm, over-center cam with a 25 mm throw) needs about 117 N, and with the drive wheels lifted the unpowered push force rises only 4.0 % [G4].

## Cost

The 18 BOM lines total $1,610, exactly the $1,610 budget Amish approved on 2026-09-26 [K1]; against the former $1,550 they were $60 (3.9 %) over. The overrun comes from the stronger hub motors ($200 each against $170 at TRL 2) and the second main contactor ($30); the lidar and its bracket add $80. Amish decided on 2026-09-25 to accept the mass and cost overruns for now and recheck them when a motor is quoted (PLP-DDR-002, O5), and on 2026-09-26 set the budget to $1,610 to cover the priced BOM. On the numbers **R17 is met**, with no margin; the motor price is the least certain line.

## Results against requirements

*Table 5. Requirement status. Values from the [R] lines of the script.*

| ID | Target | Value | Status |
| --- | --- | --- | --- |
| R1 | Bolts to common 27 x 48 in jacks; fit 2 h, remove 1 h | Clamp to the yoke, no drilling; donor geometry assumed | Not verifiable at TRL 3 |
| R2 | Move 1,000 kg; 1,500 kg at 0.8 m/s or less | 23.1 and 25.5 N·m per motor of 30 N·m; traction 750 N | Met (1,500 kg on level floors only) |
| R3 | Start, climb and hold 1,000 kg on 2 % | Start needs 488 N of 750 N (margin 1.54, 1.23 at friction 0.4); hold margin 1.84 | Met |
| R4 | Walk 1.2, forks first 0.8, creep 0.3, follow 0.6 m/s | Controller limits | Met |
| R5 | Gap ±0.3 m, bearing ±10° | Gap ±0.06 m; bearing ±16° (2σ) | **Not met** |
| R6 | Stop within 0.3 s of losing the tag | Timing budget 0.20 s; no firmware | Not verifiable at TRL 3 |
| R7 | Detect a person and stop without contact from 0.6 m/s | Stop 0.42 to 0.76 m inside a 0.86 m field; sensor not safety-rated | At risk |
| R8 | Bumper stop in 100 ms; bumper-only 0.15 m/s or less | 0.10 s; 0.15 m/s stops in 38 mm of 40 mm travel | Met |
| R9 | Hardwired stops through a relay and contactors; PL d | Dual-channel relay, two contactors in series; PL not calculated | At risk |
| R10 | Brakes hold 2 % with power off | 40 N·m specified against 21.7 N·m needed | Met (datasheet to confirm) |
| R11 | Walk drive only between 20° and 70°; belly reverse | Handle clears the enclosure by 40 mm at 70°, 14 mm at 90° | Met |
| R12 | Shift with 20 % or more left | 293 of 410 Wh; 29 % left | Met |
| R13 | Charge in 5 h or less | 4.5 h | Met |
| R14 | Release in 10 s; push force +10 % or less | +4.0 %; lever 117 N | Met |
| R15a | Kit mass 40 kg or less | 42.0 kg | **Not met** |
| R15b | Added length 300 mm or less | 290 mm | Met |
| R16 | 0 to 40 °C, IP54, no charging below 0 °C | By specification of bought parts | Not verifiable at TRL 3 |
| R17 | Kit parts $1,610 or less | $1,610 | Met (no margin; not met against $1,550 in v0.2) |

Totals: 11 met, 2 not met, 2 at risk, 3 not verifiable at TRL 3 [R0] (v0.2: 10 met, 3 not met).

## Checks against earlier figures

*Table 6. TRL 2 figures checked against this note.*

| TRL 2 figure (PLP-PRC-001 v0.2) | TRL 3 value | Change |
| --- | --- | --- |
| Kit mass about 37 kg | 42.0 kg | Stronger, heavier motors; lidar; second contactor (v0.2); R15 mass now not met |
| Available traction 550 N | 750 N | Preload raised to 1.5 kN |
| Wheel torque 17 N·m per motor | 25.5 N·m (30 N·m specified) | Acceleration and 1,500 kg cases added |
| Stop from 1.2 m/s about 1.56 m | 1.21 m controlled, 1.62 m emergency | Braking now split by stop type |
| Stop from 0.6 m/s about 0.42 m | 0.42 m level, up to 0.76 m worst case | Same level figure; worst cases added |
| Bumper-only safe at about 0.2 m/s | 0.15 m/s (now the decided limit) | TRL 2 compared the stop with no travel limit; 0.2 m/s needs 62 mm |
| Raw bearing error about ±18° | 18.0° (1σ); ±16° (2σ) filtered | Confirmed; filtering does not close the gap |
| Energy 281 Wh of 410 Wh | 293 Wh | Heavier kit and the lidar |
| Wall energy 336 Wh | 350 Wh | As above |
| Added length about 330 mm | 290 mm | Drive axle moved, track widened |
| Kit cost about $1,425 | $1,610 | Motors $60 more in total; lidar $80; second contactor $30 (v0.2); small price updates |

The docs PLP-PRC-001 and PLP-REQ-001 v0.4, PLP-PRB-001 v0.3, the README, the BOM notes and the concept media now use the TRL 3 values.
