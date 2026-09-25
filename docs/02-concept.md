---
doc_id: PLP-PRC-001
title: PalletPilot design precis
project: PalletPilot
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, stopping analysis, safety, media)
---

# PalletPilot design precis

PalletPilot clamps a drive module with two 24 V hub motors to the steering yoke of an ordinary manual pallet jack, powers it from a 25.6 V LiFePO4 pack in an enclosure on the same yoke, and adds a walkie-style tiller head, a UWB follow-me mode, hardwired emergency stops and a contact bumper. First-order numbers suggest the kit can move a 1,000 kg pallet at walking pace for a full shift of 60 moves on one overnight charge. They also show two problems that shape the next step. First, a contact bumper cannot stop a loaded jack from follow-mode speed before it strikes a person, so follow mode needs non-contact sensing or a much lower speed. Second, the kit costs about $1,425 in parts, about 19 % over the $1,200 budget.

![Hero render](../media/hero.png)

*Figure 1. PalletPilot fitted to a 27 x 48 in manual jack under a 1,000 kg pallet, with a 1.75 m person for scale. Kit parts are colored; the donor jack is grey.*

## How it works

1. **Drive.** A steel subframe clamps to the jack's steering yoke behind the steer wheels. Two 200 mm hub motors sit on it side by side, pressed onto the floor by springs with about 1.1 kN of preload. They turn with the yoke, so the kit steers with the handle like the bare jack.
2. **Walk mode.** The operator holds the tiller as usual and sets speed with a thumbwheel. As on a factory walkie, drive is enabled only with the handle between about 20° and 70° from vertical, a belly-reverse paddle pushes the truck away if it pins the operator, and releasing the handle to upright brakes the truck. The two motors run at equal torque so the handle steers freely.
3. **Follow mode.** With the key switch set to follow and the handle latched upright by a gas spring, the operator walks ahead wearing a UWB tag. Two anchors on the bumper corners and one on the tiller head measure range to the tag. The controller turns the two motors at different speeds, and this differential drive rotates the yoke about its pivot to steer toward the tag. It holds a 1.5 m gap, stops when the operator stops, and stops if the tag is lost, the operator presses the tag's stop button or the gap exceeds 3 m.
4. **Stop.** The two emergency stops, the tag stop and the bumper all open a safety relay that drops the main contactor. The hub motor brakes are spring-applied and close when power is removed. The bumper is the last layer, not the main one (see "Stopping").
5. **Charge.** A certified 29.2 V, 5 A charger fills the pack from a wall outlet in about 4.5 h overnight.
6. **Push by hand.** A release lever lifts the drive wheels off the floor and releases the brakes so the jack can be pushed as a manual jack if the pack is flat or the kit fails.

![Energy flow](../media/flow.png)

*Figure 2. Energy per 8 h shift of 60 pallet moves, in Wh. All values are estimates.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

Table 1. Main components.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Drive module subframe | 6 mm steel plate clamp to the yoke, side cheeks, two preload springs (about 1.1 kN) | Clamp pattern per donor model |
| 2 | Hub motors | Two 24 V brushless hub servo motors, 200 mm, about 250 W rated, with spring-applied brakes | AGV parts class; torque and brake data to confirm |
| 3 | Enclosure | Steel or aluminium box on the subframe, IP54 | Turns with the yoke; never on the forks |
| 4 | Battery | 8S LiFePO4, 25.6 V, 20 Ah (512 Wh), BMS with charge temperature cut-off | About 5 kg |
| 5 | Motor driver | Dual-channel 24 V servo driver, 2 x 15 A, CAN or RS-485 | Differential control for follow mode |
| 6 | Contactor, fuse and disconnect | 80 A fuse, main contactor with pre-charge, lockable disconnect | Opened by the safety relay |
| 7 | Controller and safety relay | ESP32-S3 class controller; dual-channel safety relay | Software never closes the stop chain alone |
| 8 | Tiller control head | Thumbwheel throttle, belly-reverse paddle, mode key, horn | Replaces the jack's grip |
| 9 | Emergency stops | Two red mushroom buttons, tiller head and enclosure lid | Hardwired |
| 10 | Contact bumper | Pressure-sensitive safety edge on a U hoop around the drive end | Last-resort stop |
| 11 | UWB anchors | Three DWM3000 class modules: two on the bumper corners (450 mm baseline), one on the tiller head | Range about 10 cm precision ([Qorvo](https://www.qorvo.com/products/p/DWM3000)) |
| 12 | Status beacon and buzzer | Amber in walk mode, blue in follow mode | Warns people nearby |
| 13 | Manual release lever | Over-center lever lifts the drive wheels and frees the brakes | For pushing by hand |
| 14 to 17 | Charger, operator tag, handle sensor and gas spring, wiring | See `bom/bom.csv` | Not modelled |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM. The donor jack is grey and stays in place.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section through the center of the kit, showing the pack (yellow), motor driver (orange) and controller (green) in the enclosure above the drive module.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. The design load case is 1,100 kg in total (1,000 kg pallet, 64 kg jack, about 37 kg kit) on level, dry, sealed concrete, with the assumptions listed in PLP-REQ-001.

### Forces, torque and traction

Table 2. Drive forces for the design load case.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Rolling force, level | about 130 N | 1,100 kg x 9.81 m/s² x 1.2 % | |
| Breakaway force, level | about 270 N | 2.5 % breakaway resistance | R2 |
| Grade force, 2 % | about 216 N extra, about 346 N in total | 1,100 kg x 9.81 x 0.02 | R3 |
| Wheel torque, 2 % grade | about 35 N·m total, about 17 N·m per motor | 346 N x 0.1 m wheel radius | Datasheet check |
| Power at the wheels, 1.2 m/s level | about 156 W | 130 N x 1.2 m/s | Two 250 W motors |
| Available traction | about 550 N | 1.1 kN preload x friction 0.5 | |
| Acceleration limit, level | about 0.38 m/s²; set 0.3 m/s² | (550 − 130) N / 1,100 kg | R2 met |
| Acceleration limit, 2 % grade | about 0.19 m/s² | (550 − 346) N / 1,100 kg | R3 at risk |
| At 1,500 kg pallet | about 0.23 m/s² level | Rolling about 188 N | Reduced speed needed |

Traction, not motor power, limits the concept. The springs press only the kit onto the floor; the pallet's weight stays on the steer and load wheels. More preload lifts the steer wheels and adds load to the yoke bearing, so the preload value is a trade-off to settle at TRL 3.

### Stopping

A loaded jack has a lot of momentum and poor braking because only the drive wheels brake. Assuming 550 N of braking traction and a 0.1 s delay from detection to full braking:

Table 3. Stopping distances for the design load case, level floor unless stated.

| Speed | Stopping distance | Kinetic energy |
| --- | --- | --- |
| 1.2 m/s (walk mode, full speed) | about 1.56 m | about 790 J |
| 1.2 m/s on a 2 % downgrade | about 2.5 m | about 790 J |
| 0.6 m/s (follow mode) | about 0.42 m | about 200 J |
| 0.2 m/s (creep) | about 0.06 m | about 22 J |

A pressure-sensitive safety edge compresses about 40 mm before it bottoms out. Stopping within that travel from 0.6 m/s would need about 4.5 m/s², nine times the braking available. In follow mode the truck would therefore still be moving when it reached a person's legs after the bumper tripped. **A bumper can only be the sole stopping layer at about 0.2 m/s.**

In walk mode this is acceptable practice, since the operator at the tiller watches the path, as on any walkie. In follow mode no one watches the path ahead of the truck except the operator it is following, who faces away. Commercial follow-me trucks use laser scanners for exactly this reason ([Jungheinrich](https://www.jungheinrich.com/en/press-events/press-releases/easypilot-follow-faster-order-picking-with-the-new-semi-automatic-control-unit-158956)), and ISO 3691-4 expects driverless trucks to stop before contact with a person ([overview](https://www.fabrico.io/blog/iso-3691-4-driverless-industrial-trucks/)). Options are in "Key design choices".

### Follow-me tracking

Two range-only anchors 450 mm apart find the tag's bearing from the difference in range. With about 10 cm range precision per anchor, the raw bearing error is about ±18° at any distance (about 1.4 x 0.1 m / 0.45 m). This does not meet R5 (±10°). Filtering over several samples at 10 Hz or more, a third anchor on the tiller head, or modules that measure angle of arrival directly could close the gap; the choice is a TRL 3 task. The gap measurement itself (about ±0.1 m) meets R5.

### Energy per shift

Assumptions: the design duty (60 moves of 40 m loaded and 40 m empty, four starts each way, to 1.2 m/s), no regenerative braking, 70 % motor and driver efficiency, 8 W for controls, UWB and lights over 8 h, 95 % cell efficiency and an 88 % efficient charger.

Table 4. Energy per shift.

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Work at the wheels | about 152 Wh (about 2.5 Wh per move) | |
| Motor driver input | about 217 Wh | |
| Controls, UWB and lights | about 64 Wh | |
| Energy from the pack | about 281 Wh | |
| Usable pack energy | about 410 Wh (512 Wh x 80 %) | R12 met, 31 % left |
| Energy from the wall | about 336 Wh | |
| Charge time at 5 A | about 4.5 h | R13 met |

### Mass, size and cost

Table 5. Mass, size and cost.

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Kit mass | about 37 kg (motors 11 kg, subframe 8 kg, pack 5 kg, bumper 3 kg, enclosure 3 kg, the rest 7 kg) | R15 met |
| Added length at floor level | about 330 mm | R15 target 300 mm, not met |
| Kit parts cost | about $1,425 | R17 ($1,200) not met, about 19 % over |
| Walk-only variant | about $1,075 | Within budget |
| Donor jack (not in kit) | about $396 new | |

For comparison, a complete 1,500 kg lithium walkie costs about $1,640 ([Home Depot](https://www.homedepot.com/p/3300-lbs-24V-20AH-Lithium-Battery-Electric-Pallet-Jack-Walkie-Truck-w-48-in-x-27-in-Fork-Size-3-1-in-Fork-Lowered-A-1034/326396102)) and the PowerPallet 2000 retrofit about $2,084 ([HoF Equipment](https://hofequipment.com/PowerHandling-Power-Pallet-2000-p1957.html)). A walk-only PalletPilot plus a new donor jack would cost about the same as a new walkie, so the kit's case rests on follow mode and on reusing jacks a site already owns.

## Key design choices

Every choice below is **Proposed, awaiting Amish**.

- **Follow-mode stopping.** The pitch says bumper-based stopping, and the numbers show a bumper alone is not enough in follow mode.
  - Option A: add a low-cost 2D lidar or time-of-flight sensor (about $70 to $150) that slows and stops the truck when anything is in the path, keep the bumper as the last layer, and limit follow mode to 0.6 m/s. Not safety-rated, so it cannot claim ISO 3691-4 compliance; suitable for research trials in a closed area.
  - Option B: a safety-rated laser scanner. Meets the intent of ISO 3691-4, but costs well over $1,000 on its own and breaks the budget.
  - Option C: bumper only, with follow mode limited to 0.2 m/s. Cheap and matches the pitch, but that speed is too slow for walking pickers (about a third of walking pace).
  - Option D: drop follow mode and ship walk mode only (about $1,075). Meets the budget but loses the main reason to prefer the kit over a new walkie.
  - Recommendation: Option A for the prototype, run only in a closed test area, with Option B named as the route to workplace use. This changes the pitch wording from "bumper-based stopping" to "layered stopping", which is Amish's call.
- **Drive layout.** Two hub motors on a sprung module on the yoke, steering by differential drive in follow mode. Alternatives: one hub motor plus a steering motor on the yoke (simpler drive, but a second actuator and gear on the yoke), or replacing the steer wheels with load-rated drive wheels (best traction, but the motors must carry up to about 800 kg, which rules out low-cost hub motors). Recommendation: dual hub motors on a sprung module.
- **24 V LiFePO4, 20 Ah.** Matches the scaffold and the class of low-cost walkies. A SwapCell 48 V pack is not proposed: the kit needs no more than 24 V, stays on the jack all shift and would take on the SwapCell interface work for little gain. Recommendation: 24 V LiFePO4.
- **Everything on the yoke.** Mounting the pack and electronics on the steering yoke keeps the forks clear and avoids slip rings, at the cost of more mass for the steering bearing to carry and less room when the handle is lowered. Recommendation: yoke mounting, checked at TRL 3 for handle clearance and bearing load.
- **Speeds.** Walk mode 1.2 m/s handle-end first, 0.8 m/s forks first, creep 0.3 m/s; follow mode 0.6 m/s. These sit below the PowerPallet's 1.65 m/s. Recommendation: as listed.
- **Kit rating.** 1,000 kg design load and 1,500 kg maximum at 0.8 m/s or less, well below the donor's 2,500 kg, because traction limits braking. Recommendation: as listed.
- **Budget.** The kit is about $225 over. Options are in `docs/REVIEW.md`. The `project.yaml` budget is unchanged.

## Safety

> **Safety:** PalletPilot is moving machinery that carries up to 1.5 t close to people's feet and legs, and it contains a lithium battery. Every build is a research prototype for a closed test area, not a certified industrial truck. Do not use it in a workplace until the questions below are answered.

- **Crushing and collision.** A loaded jack at 1.2 m/s carries about 790 J and needs about 1.6 m to stop. Foot injuries under the drive end and pinning against racking or walls are the classic walkie hazards. Use the belly-reverse paddle, handle-angle braking, walking-pace speed limits, safety footwear and a bumper hoop that shields the wheels. Never ride on the jack.
- **Follow mode.** The truck moves with no hand on the tiller. Until non-contact sensing is fitted and tested, follow mode must run only at creep speed (0.2 m/s or less) in a cordoned area with no other people present. Loss of the tag, a tag stop press, a gap over 3 m or any fault must stop the truck with brakes applied.
- **Emergency stop.** The emergency stops and bumper act through a hardwired safety relay and contactor, never only through software. The spring-applied brakes close on loss of power.
- **Runaway on slopes.** Braking falls by about 40 % on a 2 % downgrade. Do not use on ramps steeper than 2 % or on dock plates with a loaded pallet until traction is measured.
- **Lithium pack.** LiFePO4 is more stable than other lithium-ion chemistries but still stores 512 Wh and can deliver very high currents. Use a BMS with cell-level protection and a charge temperature cut-off, fuse the pack at the terminal, provide a lockable disconnect, charge on a non-combustible surface away from stored goods, and do not charge below 0 °C or a pack that is damaged or swollen.
- **Legal and training.** In the United States a motorized pallet jack is a powered industrial truck, so operators need formal training and evaluation under 29 CFR 1910.178(l), and modifications affecting capacity or safe operation need the jack maker's written approval under 1910.178(a)(4) ([OSHA 1910.178](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.178)). Other countries have similar rules. The kit must not be fitted to a jack used at work without resolving this.
- **Donor jack condition.** Do not convert a jack with a cracked frame, a leaking pump or a worn steering bearing. The added yoke mass and drive forces load the steering bearing more than hand use.

## Open questions for TRL 3

- Decide the follow-mode stopping option and the resulting pitch wording (Amish).
- Measure rolling and breakaway resistance, and tread friction, on a real jack on typical floors; revisit preload and the 2 % ramp (R3).
- Survey three common donor jacks for yoke geometry, steering bearing rating and handle clearance.
- Choose hub motors with published peak torque (17 N·m or more each) and brake holding torque (about 11 N·m or more each).
- Build the UWB error budget and choose between filtering, a third ranging anchor and angle-of-arrival modules (R5).
- Write the stop chain and estimate its performance level under ISO 13849-1 (R9).
- Settle the legal route for workplace use (1910.178(a)(4) and ISO 3691-4).
- Close the $225 cost gap or propose a budget change.
- Shorten the drive module and bumper by about 30 mm (R15).

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
