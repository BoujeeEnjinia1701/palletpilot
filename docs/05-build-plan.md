---
doc_id: PLP-BLD-001
title: PalletPilot prototype build plan
project: PalletPilot
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan; design made constructable (PLP-DDR-003)
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Steering range stated in section 3.2 (about 40° each way, turning radius roughly 1.5 m about the load wheels); aisle turn added to the first checks
---

# PalletPilot prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component of the kit, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. The 17 components of the kit, pulled apart and numbered in build order. The donor jack is not shown.*

The prototype is the PalletPilot kit fitted to one ordinary 27 x 48 in manual pallet jack. Everything hangs off the jack's steering yoke, behind its pump: a steel subframe clamped to the yoke plate, two hub motors on sprung drive arms, a release lever that lifts the motors clear for pushing by hand, a low aluminium box holding the battery and electronics, a bumper hoop with a safety edge, a lidar and two radio anchors on the hoop, and a new control head on the jack's handle. Figure 1 shows the 17 components in the order you make or fit them. Eleven are made in a small fabrication shop: the subframe, lower jaw, drive arms, pivot pin, cam shaft, spring saddles and straps, lever, link, enclosure, bumper hoop and lidar bracket. The rest are bought: the hub motors, springs, steering stops, battery, motor driver, contactors, controller, safety edge, lidar, anchors and tiller head. The work is cutting and drilling steel plate, MIG welding, bending strip, folding aluminium sheet, riveting, and wiring bought modules at 25.6 V. The parts cost about $1,690 from the bill of materials. Nothing is drilled, cut or welded on the jack itself.

> **Safety:** The finished kit is moving machinery that can push a 1,000 kg load, and it carries a 512 Wh lithium iron phosphate battery that can deliver very high currents. Keep the battery fuse out and the disconnect off until section 6 says otherwise, keep the drive wheels lifted (lever up) and the jack chocked for every powered check, and never ride on the jack. Welding, grinding and cutting steel need eye, hand and fire precautions. The kit is a research prototype for a closed area and is not a certified industrial truck.

## 2. What changed to make it buildable

The concept showed what the kit does; several of its parts could not be made or fixed as drawn. Each change below keeps what the kit does, and all of them are recorded in decision record PLP-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Yoke clamp | A thick slab with a block that did not reach the yoke and a loose tongue under it | A 6 mm top plate on the yoke plate with a notch round the pump, a lower jaw underneath, and four M12 bolts behind the yoke's edge (Figure 6) | Grips the yoke plate without drilling the jack |
| Drive wheel mounts | Side cheeks welded solid to the plate, and springs floating beside it | Two drive arms on a pivot pin behind the wheels, each pushed down by a spring at its front end (Figures 7 and 12) | The wheels can follow the floor and carry the 1.5 kN preload |
| Hub motors | Wheels with no shaft into their mounts | Each motor's shaft passes through its arm with a spacer and a nut (Figure 7) | How a single-sided hub motor is mounted |
| Manual release | A lever along the box with no pivot and no link to the springs | A cam shaft with two cams, a crank, a link and a 400 mm lever; raising the lever lifts the wheels 10 mm (Figures 15 and 16) | One lever lifts both wheels with about 58 N of effort |
| Bumper | One solid block, mounted from the moving cheeks | A tube hoop bolted to brackets on the subframe, with the safety edge riveted on (Figure 21) | The bumper face no longer moves with the wheels |
| Lidar and anchors | Brackets in space the arms now need, and anchors with no fixing | A bent bracket and two corner plates screwed to the top of the hoop (Figure 23) | Scan height and anchor spacing unchanged |
| Enclosure | No fixing | Four riveted angle feet, one M8 bolt each (Figure 18) | The box floor stays whole |
| Steering | Nothing stopped the drive end swinging into the jack's frame | Corners of the top plate cut back and two rubber steering stops that meet the frame at 40° (Figure 3) | Steel parts of the kit never strike the jack |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Front" is the end of the kit nearest the jack's forks; "back" is the handle end. "Left" and "right" are as seen standing at the handle end, facing the forks; the release lever is on the left. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4. Before cutting anything, measure the donor jack's yoke plate (thickness, rear edge, width) and the distance from its steering axis to the back of its frame; the plan assumes a 15 mm yoke plate whose rear edge is 50 mm behind the steering axis and a frame 100 mm ahead of it.

### 3.1 Subframe (top plate with welded hangers and brackets)

![Figure 2. Making sketch of the subframe](../cad/drawings/PLP-DWG-101.png)

*Figure 2. Subframe making sketch (PLP-DWG-101).*

**What it is and what it is made from.** The plate everything hangs from. It sits on the jack's yoke plate, carries the enclosure on top and, underneath, the hangers for the cam shaft and the drive arms and the brackets for the bumper. Steel plate, S275 or A36 class: 6 mm for the top plate, front hangers, bumper brackets and lever bracket; 10 mm for the rear hangers.

**How to make it.**

1. Have the top plate laser or plasma cut: 295 x 400, front corners cut off at 45° for 50 along each edge, and a half-round notch of 62 radius in the front edge, centred on the centre line 15 in front of the edge, so it reaches 47 into the plate.
2. Drill the top plate, measuring back from the front edge and sideways from the centre line: four 13 mm clamp bolt holes 49 back, at 35 and 80 each side; four 9 mm enclosure foot holes at 80 and 270 back, 162 each side.
3. Cut the two front hangers (6 mm, 24 x 59) and drill a 16 mm hole in each, 37 from the top edge, centred. Cut the two rear hangers (10 mm, 28 x 94) and drill a 20 mm hole in each, 74 from the top edge, centred.
4. Cut the two bumper brackets (6 mm, 40 x 119) and drill two 9 mm holes in each, 109 from the top edge, 10 and 30 from the back edge.
5. Cut the lever bracket (6 mm, 60 x 60) and drill a 12 mm pivot hole 35 above its bottom edge, 40 from its front end. Cut the stop tab (15 x 21 x 12).
6. Tack the parts under the top plate, square to it: front hangers with their inner faces 174 from the centre line, centred 75 back; rear hangers with inner faces 180 out, centred 275 back; bumper brackets flush with the side edges, 215 to 255 back. Slide a 16 mm bar through both front hangers and a 20 mm bar through both rear hangers before welding, so the holes stay in line.
7. Tack the lever bracket on top of the plate at the left edge, inner face 194 from the centre line, 250 to 310 back (it overhangs the back edge by 15), and the stop tab on its outer face, 13 above the plate, 255 to 270 back.
8. Weld everything with short alternating runs to limit distortion, then check the plate is flat within 1 mm. Deburr, and paint or powder coat.

**How it fits the parts next to it.** The front of the plate rests on the yoke plate's rear margin with the pump in the notch, 7 clear all round; the lower jaw grips the yoke plate from below (Figure 6). The drive arms hang from the rear hangers (Figure 10), the cam shaft runs in the front hangers (Figure 4), the bumper hoop bolts to the brackets (Figure 21) and the enclosure feet bolt through the top (Figure 18).

**Check before moving on.** The 16 mm and 20 mm bars slide through each pair of hangers by hand; the hangers are square to the plate; the plate is flat within 1 mm.

### 3.2 Steering stops (bought, make 2)

**What it is and what it is made from.** A hard rubber block (about 80 Shore A), 40 x 40 x 20, under each front corner of the top plate. The stops set how far the jack steers with the kit fitted: about 40° each way, against about 90° for a bare jack, for a turning radius of roughly 1.5 m about the load wheels.

**How to make it.**

1. Buy two blocks with a bonded steel backing plate, or cut them from hard rubber sheet.
2. Mark the block's position from Figure 3: its outer face must lie flat on the back of the jack's frame when the handle is turned 40° to that side, and nothing else may touch the frame first.
3. Drill two 9 mm holes through the top plate and the block and fit two M8 bolts with large washers and nyloc nuts.

**How it fits the parts next to it.**

![Figure 3. Joint 10: a steering stop meeting the jack's frame at full turn](05-build-plan/joint-10.png)

*Figure 3. At 40° of turn the rubber stop meets the jack's frame head flat; the hub motors, the hoop and the plate are still clear.*

**Check before moving on.** After step 6, turn the handle fully each way: the stop must touch the frame before any steel part of the kit, with about 4° to spare. If your jack's frame sits further from the steering axis than 100 mm, the stops can be moved out to allow more turn.

### 3.3 Cam shaft, cams and crank

![Figure 4. Making sketch of the cam shaft](../cad/drawings/PLP-DWG-105.png)

*Figure 4. Cam shaft making sketch (PLP-DWG-105).*

**What it is and what it is made from.** The shaft that the release lever turns. Its two cams press the spring saddles down when the wheels are down and let them rise 22 when the lever is raised. 16 mm bright steel bar; cams from 12 mm steel plate; crank from 24 x 10 flat bar with a 10 mm pin.

**How to make it.**

1. Cut the shaft 419 long and chamfer both ends.
2. Have two cams cut: discs 72 across with a 16 mm bore whose centre is 22 from the disc's centre. Ream the bores to a sliding fit on the shaft.
3. Make the crank: 74 long, ends rounded, a 16 mm bore at one end and a 10 mm pin, 18 long, welded into a hole at the other, 50 between centres.
4. The shaft, cams and crank are assembled in the subframe's front hangers (step 2), because the cams sit outside the hangers.
5. With the shaft in the hangers, slide a cam on each end with its outer face 198 from the centre line, and the crank on the long (left) end with its outer face 221 out. Turn the cams so their thick side points straight down and the crank pin straight up, then drill a 5 mm hole through each hub and the shaft and drive in a roll pin.

**How it fits the parts next to it.** The shaft turns in the front hangers (grease it). Each cam bears on the top of a spring saddle (Figure 12). The crank pin carries the link (Figure 15).

**Check before moving on.** The shaft turns freely by hand; cams and crank do not move on it.

### 3.4 Lower jaw and packing bar

![Figure 5. Making sketch of the lower jaw](../cad/drawings/PLP-DWG-102.png)

*Figure 5. Lower jaw making sketch (PLP-DWG-102).*

**What it is and what it is made from.** The plate that grips the jack's yoke plate from below. 10 mm steel plate for the jaw; a flat bar 34 wide for the packing bar, as thick as your yoke plate less 1 mm.

**How to make it.**

1. Cut the jaw 71 x 190.
2. Cut the packing bar 190 long and weld it on top of the jaw along its back edge, ends flush.
3. Clamp the jaw under the top plate, packing bar between them, back edges flush, and drill the four 13 mm holes through both from the top plate's holes.

**How it fits the parts next to it.**

![Figure 6. Joint 1: the clamp on the jack's yoke, cut through the right-hand bolts](05-build-plan/joint-01.png)

*Figure 6. The yoke plate is gripped between the top plate and the jaw; the packing bar sits 2 behind the yoke's edge; the bolts pass behind the edge, so the jack is not drilled.*

The jaw's front part lies under the yoke plate's rear margin, 35 deep. Four M12 bolts go up from below, through the jaw, the packing bar and the top plate, with nuts on top. Because the packing bar is 1 mm thinner than the yoke plate, tightening the bolts squeezes the yoke plate. The pump in the notch stops the subframe sliding back; the packing bar against the yoke's edge stops it sliding forward.

**Check before moving on.** With the bolts snug, the jaw sits flat under the yoke plate along its whole width.

### 3.5 Hub motors (bought, make up 2 with their arms)

**What it is.** Two 24 V brushless hub servo motors, 200 mm, 30 N·m peak or more, with spring-applied brakes and a single fixed shaft on one side (bill of materials line 2). Each is fitted to its drive arm on the bench (step 5).

**How it fits the parts next to it.**

![Figure 7. Joint 3: hub motor shaft in the drive arm](05-build-plan/joint-03.png)

*Figure 7. The motor's shaft passes through the arm's axle hole, with a 5 mm spacer between the motor and the arm and a nut outside.*

**Check before moving on.** The shaft's flats (if it has them) seat in the arm without play; the motor's cable leaves on the side away from the floor.

### 3.6 Drive arms (make 2, a left and a right)

![Figure 8. Making sketch of the drive arm](../cad/drawings/PLP-DWG-103.png)

*Figure 8. Drive arm making sketch (PLP-DWG-103).*

**What it is and what it is made from.** The arm that carries one hub motor and pivots behind it, so the spring at its front end can push the wheel onto the floor. 10 mm steel plate, with a 10 mm spring tab welded on.

**How to make it.**

1. Have the two arms cut as a mirror pair from the profile: a 20 mm pivot hole at the back end; a 20 mm axle hole 110 ahead of it and 45 lower; the front end's centre 195 ahead of the pivot and 95 lower. Ends rounded to 18 radius, 36 wide between.
2. Check the axle hole against the hub motor's shaft and opt for a flatted hole if the shaft has flats.
3. Cut two spring tabs 44 x 44 from 10 mm plate. Weld one to the outer face of each arm at the front end, square to the arm, its top face 90 below the pivot hole centre, reaching 34 out from the arm.
4. Drill and tap an M6 hole into the middle of each tab's front and back edges, 5 below its top face (for the lift straps).

**How it fits the parts next to it.** The pivot pin passes through the back hole (Figure 10), the motor shaft through the axle hole (Figure 7), and the spring stands on the tab (Figure 12).

**Check before moving on.** Laid back to back, the two arms' holes line up.

### 3.7 Pivot pin, spacers and nuts

![Figure 9. Making sketch of the pivot pin](../cad/drawings/PLP-DWG-104.png)

*Figure 9. Pivot pin making sketch (PLP-DWG-104).*

**What it is and what it is made from.** The pin the two arms turn on. 20 mm bright steel bar; two spacers from 30 x 5 tube; two M20 nyloc nuts.

**How to make it.**

1. Cut the pin 392 long and thread both ends M20 for 25.
2. Cut two spacers 5 long from 30 mm tube with a 20 mm bore; deburr.

**How it fits the parts next to it.**

![Figure 10. Joint 2: drive arm on its pivot pin](05-build-plan/joint-02.png)

*Figure 10. Each arm turns on the pin between a spacer and the open middle; the nut clamps the hanger, not the arm.*

**Check before moving on.** Each arm swings freely by hand on the greased pin.

### 3.8 Springs, spring saddles and lift straps

![Figure 11. Making sketch of the saddle and straps](../cad/drawings/PLP-DWG-106.png)

*Figure 11. Spring saddle and lift straps making sketch (PLP-DWG-106).*

**What it is and what it is made from.** Each drive arm's spring stands on the arm's tab; a steel saddle sits on top of it, under the cam. Two slotted straps join each saddle to its tab, so that raising the saddle lifts the arm. Springs are bought: compression springs about 34 outside diameter, about 65 free length, about 100 N/mm. Saddles from 8 mm steel; straps from 12 x 4 strip.

**How to make it.**

1. Cut two saddles 44 x 34. Turn or mill a ring groove 2 deep and 34 across in the underside to locate the spring. Drill and tap M6 into the middle of its front and back edges (the 34 long ones).
2. Cut four straps 79 long. Drill a 6.5 mm hole 5 from one end; at the other end cut a slot 6.5 wide and 12 long, ending 4 from the end.

**How it fits the parts next to it.**

![Figure 12. Joint 4: spring, saddle and cam](05-build-plan/joint-04.png)

*Figure 12. The cam presses the saddle down onto the spring, and the spring presses the arm, and so the wheel, onto the floor.*

Each spring is squashed about 4 by the cam when the wheels are down, which puts about 420 N on each arm's tab and 750 N on each wheel. Each strap is bolted M6 to the tab through its hole and to the saddle through its slot, with the saddle bolt 4 below the top of the slot when the wheels are down. A bump can squash the spring further; when the lever is raised, the saddle rises, the slot's top catches the bolt, and the straps lift the arm.

**Check before moving on.** The saddle slides up and down in the slots without binding.

### 3.9 Release lever and link

![Figure 13. Making sketch of the release lever](../cad/drawings/PLP-DWG-107.png)

*Figure 13. Release lever making sketch (PLP-DWG-107).*

![Figure 14. Making sketch of the release link](../cad/drawings/PLP-DWG-108.png)

*Figure 14. Release link making sketch (PLP-DWG-108).*

**What it is and what it is made from.** The lever on the left of the enclosure that lifts the drive wheels for pushing by hand, and the link that joins it to the cam shaft's crank. 20 x 10 flat bar with a 28 mm tube grip; link from 20 x 8 flat bar.

**How to make it.**

1. Lever: cut the main bar 410 long and drill a 12 mm pivot hole 10 from one end. Cut the up-arm from the same bar, round its ends, drill a 10 mm hole 50 from the pivot hole centre, and weld it at the pivot end, square to the main bar. Weld a 30 long piece of 28 mm tube across the far end as a grip, standing out to the left.
2. Link: measure the distance from the cam shaft's centre to the lever bracket's pivot hole on your subframe (228.7 on the drawing). Cut the link and drill its two 10 mm holes exactly that distance apart, within 0.5.
3. Make the pivot pin (12 mm, 27 long, with a split pin hole) and an 11 long spacer of 20 mm tube.

**How it fits the parts next to it.**

![Figure 15. Joint 5: lever, link and crank, wheels down](05-build-plan/joint-05.png)

*Figure 15. The crank and the lever's up-arm stay parallel through the link; with the wheels down the lever lies forward on its stop.*

![Figure 16. Joint 6: the release with the lever raised](05-build-plan/joint-06.png)

*Figure 16. Raising the lever a quarter turn turns the cams, lifts the saddles 22 and, through the straps, lifts both drive wheels about 10 clear of the floor.*

The lever turns on its pin in the bracket with the spacer between them. The link sits outboard of the crank and the up-arm, on their 10 mm pins, with a washer and split pin at each end. With the wheels down, the cams are just past their lowest point and the springs hold the lever down on its stop, so it cannot creep up. The peak effort to raise it is about 58 N at the grip.

**Check before moving on.** The lever swings a quarter turn without touching the enclosure or the hoop.

### 3.10 Enclosure, lid and feet

![Figure 17. Making sketch of the enclosure](../cad/drawings/PLP-DWG-109.png)

*Figure 17. Enclosure, lid and feet making sketch (PLP-DWG-109).*

**What it is and what it is made from.** The low box that holds the battery and electronics, under the jack's handle. 2 mm aluminium sheet, 5052 class; feet from 25 x 20 x 3 aluminium angle.

**How to make it.**

1. Have the box folded from 2 mm sheet to 270 long, 300 wide and 89 tall, open at the top with an inward flange for the lid gasket; rivet or weld the corners.
2. Fold the lid to 270 x 300 with a 6 mm down-turned edge. Fit six M5 rivet nuts in the box flange and drill the lid to match.
3. Cut holes: 40 mm on the right side for the disconnect, 180 from the front end and 45 up; 22 mm in the back face for the emergency stop, 80 left of centre and 45 up; and glands for the cables as the wiring needs. Never put a hole in the lid.
4. Cut four feet 24 long from the angle and drill a 9 mm hole in each flat leg, 12 from the upright leg. Rivet each upright leg to the box side with two 4.8 mm rivets, 20 and 210 from the front end, bottoms flush with the box bottom.

**How it fits the parts next to it.**

![Figure 18. Joint 8: enclosure foot on the top plate](05-build-plan/joint-08.png)

*Figure 18. Each foot is riveted to the box side and held to the top plate by one M8 bolt, nut below.*

**Check before moving on.** The lid seals on its gasket all round; with the box on the top plate, the lid top is 320 or less above the floor, so the lowered handle clears it by 14.

#### 3.10.1 Electrical parts and wiring

![Figure 19. Block-level power and stop-chain wiring](05-build-plan/wiring.png)

*Figure 19. Block-level wiring. No circuit board is laid out at this stage; bought modules are wired together.*

*Table 2. Electrical modules (bill of materials lines 4 to 7, 9, 11, 14, 16 to 18).*

| Module | What to buy |
| --- | --- |
| Battery | 8S LiFePO4, 25.6 V, 20 Ah, about 270 x 115 x 85, with a BMS rated 50 A continuous and a charge temperature cut-off below 0 °C |
| Main fuse and disconnect | 80 A fuse at the battery terminal; lockable battery disconnect for panel mounting |
| Contactors | Two 24 V main contactors rated 80 A or more, with a pre-charge resistor for the driver's input capacitors |
| Motor driver | Dual-channel 24 V brushless servo driver, 2 x 15 A continuous, 30 A peak, CAN, brake outputs, matched to the motors' encoders |
| Controller and safety relay | ESP32-S3 class controller with a CAN transceiver; dual-channel safety relay with manual reset |
| Stop devices | Two 22 mm emergency stops with two normally closed contacts each; the safety edge's evaluation unit |
| Sensors | 2D lidar (RPLIDAR C1 class); three UWB anchor modules (DWM3000 class); Hall angle sensor on the handle pivot |

Wire it as Figure 19 shows. All main power is 5.3 mm² (10 AWG) with crimped lugs; stop-chain and coil wiring 0.75 mm²; signals in twisted pairs. Both emergency stops and the safety edge feed the safety relay's two channels; each channel opens one contactor. The controller can only ask the relay for a stop; it can never close the chain. The motor brakes close when power is removed.

**Check before moving on.** With the battery fuse out: every wire continues end to end and is labelled; pressing either emergency stop or the edge opens both relay channels (meter on each coil circuit).

### 3.11 Bumper hoop

![Figure 20. Making sketch of the bumper hoop](../cad/drawings/PLP-DWG-110.png)

*Figure 20. Bumper hoop making sketch (PLP-DWG-110).*

**What it is and what it is made from.** A U of steel tube round the drive end that carries the safety edge. 40 x 20 x 2 rectangular tube, standing 40 tall.

**How to make it.**

1. Cut the front bar 440 long and two side legs 210 long, outside lengths, with 45° mitres at the corners. Weld all round and grind the corners smooth.
2. In the inner face of each leg drill two 11 mm holes, 120 and 140 from the leg's open end, centred on the tube's height, and set an M8 rivet nut in each.
3. In the top of the front bar, on the centre line, drill and set two M5 rivet nuts for the lidar bracket, and two at each front corner for the anchor plates.
4. Paint safety yellow.

**How it fits the parts next to it.**

![Figure 21. Joint 7: the hoop on the subframe bracket, seen from inside](05-build-plan/joint-07.png)

*Figure 21. Each leg's inner face bears on the subframe's bumper bracket; two M8 bolts go through the bracket into the rivet nuts.*

The tube's underside is 90 above the floor and the front bar is 30 behind the drive wheels' treads. The safety edge's rail is riveted to the front face (the 50 deep front edge, 40 travel) and to the outer faces of both legs (20 deep).

**Check before moving on.** The legs are parallel and 400 apart inside, within 1.

### 3.12 Lidar bracket

![Figure 22. Making sketch of the lidar bracket](../cad/drawings/PLP-DWG-111.png)

*Figure 22. Lidar bracket making sketch (PLP-DWG-111).*

**What it is and what it is made from.** A small bent bracket that holds the lidar just behind the bumper face. 40 x 4 steel strip and a 6 mm plate shelf.

**How to make it.**

1. Bend the strip to an L: foot 20 long, upright 44 tall.
2. Weld the shelf (60 x 50) to the top of the upright, reaching forward, and drill it for the lidar's own mounting holes.
3. Drill two 5.5 mm holes in the foot to match the rivet nuts in the hoop.

**How it fits the parts next to it.**

![Figure 23. Joint 9: lidar and anchor on the hoop](05-build-plan/joint-09.png)

*Figure 23. The lidar's scan plane is 200 above the floor and its front 10 behind the bumper face; each anchor sits on a corner plate below the scan plane.*

**Check before moving on.** The shelf is level within 1° both ways.

### 3.13 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Hub motors (line 2).** As section 3.5; confirm the 24 V winding, the brake's holding torque (20 N·m or more) and the shaft's size and flats before the arms are cut.
- **Springs (line 13).** Two compression springs, about 34 outside diameter, 65 free length, 100 N/mm, closed and ground ends.
- **Steering stops (line 19).** As section 3.2.
- **Battery, driver, contactors, controller, relay and stops (lines 4 to 7 and 9).** As Table 2.
- **Tiller head (line 8).** A clamp-on walkie head that fits the jack's handle tube, with a thumbwheel throttle, belly-reverse paddle, mode key, horn and a beacon mount; carries the beacon (line 12), the second emergency stop and the third UWB anchor.
- **Safety edge (line 10).** Pressure-sensitive edge with its evaluation unit and an aluminium mounting rail: front length 480 with 40 or more of travel, two side lengths of about 210.
- **UWB anchors (line 11) and lidar (line 18).** As Table 2; each anchor in a small box on a corner plate screwed to the hoop.
- **Handle sensor and gas spring (line 16), charger (line 14), operator tag (line 15).** As the bill of materials; the charger and tag are not fitted to the jack.
- **Fixings (line 17).** Four M12 x 50 bolts (8.8) with nuts and hardened washers; M8 bolts, nyloc nuts and rivet nuts; M6 and M5 screws; M5 rivet nuts; 4.8 mm rivets; 5 mm roll pins; split pins; 5.3 mm² cable, lugs, spiral wrap and labels.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in. Steps 1, 2 and 5 are done on the bench; the jack is then chocked on a level floor with its forks lowered.

### Step 1: steering stops under the top plate

![Step 1](05-build-plan/step-01.png)

With the subframe upside down on the bench, bolt each stop under a front corner on two M8 bolts.

### Step 2: cam shaft through the front hangers

![Step 2](05-build-plan/step-02.png)

Slide the shaft in from the left through both front hangers, then fit the cams and the crank and drive in the roll pins as section 3.3.

### Step 3: subframe onto the jack's yoke

![Step 3](05-build-plan/step-03.png)

Remove nothing from the jack. Slide the subframe forward over the yoke plate until the pump sits in the notch and the plate lies flat on the yoke plate.

### Step 4: lower jaw under the yoke plate

![Step 4](05-build-plan/step-04.png)

Offer the jaw up under the yoke plate with the packing bar behind the yoke's edge. Fit the four M12 bolts from below, nuts and hardened washers on top, and tighten evenly in a cross pattern to 80 N·m. **Hold point:** the jaw is flat under the yoke plate and the handle still steers and pumps freely.

### Step 5: hub motors into the drive arms

![Step 5](05-build-plan/step-05.png)

On the bench, pass each motor's shaft through its arm's axle hole with the 5 mm spacer between motor and arm, and fit the nut outside to the motor maker's torque.

### Step 6: arms and motors onto the pivot pin

![Step 6](05-build-plan/step-06.png)

With a helper, lift both arms with their motors under the subframe so the back holes line up with the rear hangers. Push the greased pin through the left hanger, a spacer, the left arm, the right arm, a spacer and the right hanger, and fit the nuts. The wheels rest on the floor.

### Step 7: springs, saddles and lift straps

![Step 7](05-build-plan/step-07.png)

Turn the crank toward the back of the kit with a spanner, so the cams point their thick side forward and are high. Stand each spring on its tab, put the saddle on top, and bolt the straps to the tab and, through their slots, to the saddle. Turn the crank back upright: the cams press the saddles down and squash the springs about 4.

### Step 8: release lever and link

![Step 8](05-build-plan/step-08.png)

Fit the lever on its pin in the bracket with the spacer between them. Fit the link over the crank pin and the up-arm's pin, outboard of both, with washers and split pins. **Hold point:** raising the lever lifts both wheels clear of the floor, and lowering it puts them back down with the lever resting on its stop.

### Step 9: enclosure onto the top plate

![Step 9](05-build-plan/step-09.png)

Stand the box on the top plate and fit one M8 bolt through each foot and the plate, nyloc nut below.

### Step 10: battery, driver, contactors and controller into the enclosure

![Step 10](05-build-plan/step-10.png)

Fit each module on its own bracket or pads and wire as Figure 19, with the disconnect off and the battery fuse out. Run the motor, safety edge and lidar cables through glands. **Hold point:** the wiring checks of section 3.10.1 pass.

### Step 11: close the lid

![Step 11](05-build-plan/step-11.png)

Check the gasket is clean and no wire lies across it; fit the six M5 screws evenly.

### Step 12: bumper hoop onto the brackets

![Step 12](05-build-plan/step-12.png)

Slide the hoop forward over the bumper brackets from behind and fit two M8 bolts each side into the rivet nuts.

### Step 13: safety edge onto the hoop

![Step 13](05-build-plan/step-13.png)

Rivet the edge's rail to the front and side faces of the hoop and run its lead to the evaluation unit in the enclosure.

### Step 14: lidar and corner anchors onto the hoop

![Step 14](05-build-plan/step-14.png)

Screw the lidar bracket and the two anchor plates to the hoop with M5 screws, fit the lidar and anchors, and check the lidar's scan plane is 200 above the floor.

### Step 15: tiller head onto the handle

![Step 15](05-build-plan/step-15.png)

Remove the jack's grip and clamp the tiller head on the handle tube. Run its cable down the handle in spiral wrap to a gland on the enclosure, leaving slack for the full handle swing and full steering turn. Fit the handle angle sensor at the pivot and the gas spring, as their makers describe. **Hold point:** safety stop S4 in section 6.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of PLP-REQ-001.

*Table 3. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Clamp and fit | R1 | Time the fitting and removal; look for any drilled or damaged part of the jack | No change to the jack; fitted in 2 h or less, removed in 1 h or less |
| Steering stops | R1, R15 | Turn the handle fully each way, power off | The rubber stops touch the frame first; record the angle (40° expected) |
| Aisle turn | R15 | Walk mode at creep speed with the design load: turn from an aisle into a standard pallet bay; measure the turning radius about the load wheels | The kit makes the right-angle turn into the bay; radius recorded (roughly 1.5 m expected) |
| Handle clearance | R11 | Lower the handle to horizontal over the enclosure | 14 or more of clearance; none of the kit touched |
| Release | R14 | Raise the lever with a spring balance at the grip; time it | Both wheels clear the floor by about 10; effort under 120 N; under 10 s |
| Hand push | R14 | Spring balance on the handle, lever up, jack empty and loaded | Push force within 10 % of the bare jack's |
| Stop chain | R8, R9 | Wheels lifted, power on, wheels turning slowly: press each stop and the edge | Both contactors open and the brakes close within 100 ms (scope on the coils) |
| Brake hold | R10 | Power off, wheels down, on a 2 % slope with the design load | The truck does not move |
| Speed limits | R4 | Wheels lifted; command each mode; measure wheel speed | 1.2, 0.8, 0.3 and 0.15 m/s equivalents, not exceeded |
| Kit mass | R15 | Weigh each subassembly before fitting | About 44 kg in all; recorded against the 40 kg target |
| Added length | R15 | Measure from the steer wheels' back to the bumper face | 290 or less |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the battery comes into the workshop.** Pack voltage about 24 to 28 V; no swelling, dents or leaks; the maker's datasheet and BMS limits in hand. A charging spot ready on a non-combustible surface, away from stored goods, with a fire extinguisher for electrical fires within reach.
- **S2. Before the battery fuse goes in.** Wiring checks of section 3.10.1 pass. Polarity checked with a meter at the driver input. Disconnect off. Insulated tools only; no rings or watches.
- **S3. Before the first power-up.** Jack chocked on a level floor, drive wheels lifted with the lever, nobody within reach of the wheels. The safety relay needs its manual reset before anything moves.
- **S4. Before the motors turn.** Both emergency stops and the edge open both contactors (section 5, stop chain). Driver current limits set to the motors' ratings; speed limited to the creep setting.
- **S5. Before the wheels go down on the floor under power.** A cordoned, level, dry area with no other people in it; the operator wears safety footwear; walk mode only, with the handle-angle drive band and belly-reverse paddle checked with the wheels lifted. No load on the forks.
- **S6. Before any load goes on the forks.** All checks of section 5 pass empty. Start with a light pallet and work up; no ramps.
- **S7. Follow mode.** Not run until the lidar layer is built and tested, and then only at 0.15 m/s or less in a cordoned area with no other people present, the operator wearing the tag with its stop button.
- **S8. Charging.** Only with the certified charger, on the charging spot, never below 0 °C and never a damaged or swollen pack; never left unattended on a first charge.

## 7. Tools, skills and workspace

**Tools.** Access to a laser or plasma cutting service for the plates and cams; bandsaw or hacksaw; bench drill with drills to 20 mm and a 13 mm drill; M5, M6 and M20 taps and dies; MIG welder; angle grinder with cutting and flap discs; sheet metal folder for 2 mm aluminium (or a sheet metal shop); rivet gun for 4.8 mm rivets and a rivet nut tool for M5 and M8; files, deburring tool, engineer's square, steel rule, calipers, digital angle finder; torque wrench to 100 N·m; spring balance to 200 N; crimp tool for 5.3 mm² lugs and ferrules; wire strippers; multimeter; two-channel oscilloscope or a timing meter for the stop chain; wheel chocks and two axle stands; a scale to 50 kg.

**Skills.** MIG welding of 6 and 10 mm structural steel to a sound standard; marking out and drilling; sheet metal riveting; crimping and wiring of 25.6 V, 80 A circuits; safe handling of lithium iron phosphate packs. The welds on the subframe hangers and the bumper hoop carry the drive and spring loads, so a competent welder should make or check them. No mains wiring is part of the build: the charger is a certified, self-contained unit.

**Workspace.** A fabrication area with fire-safe welding screens, away from the battery and electronics; a clean bench for wiring; a level concrete floor about 3 x 4 m for fitting and first checks, which can be cordoned off; the charging spot of S1. Two people for lifting the motors (about 7 kg each) and fitting the arms.

**Personal protective equipment.** Welding helmet, gloves and flame-resistant clothing for welding; safety glasses and hearing protection for cutting and grinding; safety footwear throughout; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`): overlaps, contacts, the release lever's raised state and the steering sweep; STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/PLP-DWG-101` to `PLP-DWG-111`.
- General arrangement: `cad/drawings/PLP-DWG-001.pdf`, Rev P4.
- Calculations: `docs/04-calcs/01-sizing.md` (PLP-CAL-001 v0.5) and `docs/04-calcs/sizing.py`; mass [B0], [B1], loads [C1] to [C3], torque [F4], stopping [S2], [S3], release [G4], steering [G5].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (PLP-DDR-003), with PLP-DDR-001 and PLP-DDR-002; open decisions in `docs/06-design-decisions.md` (PLP-DEC-001).
- Requirements: `docs/03-requirements.md` (PLP-REQ-001 v0.7).
