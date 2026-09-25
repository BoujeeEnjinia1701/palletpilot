---
doc_id: PLP-PRB-001
title: PalletPilot problem statement
project: PalletPilot
doc_type: Problem statement
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
  change: Populate to TRL 2 (problem, users, context, constraints, out of scope, prior work with sources)
---

# PalletPilot problem statement

Small warehouses, shops and workshops move pallets with manual pallet jacks, and a loaded jack takes more force to start and keep rolling than ergonomic limits allow for repeated shifts. Powered walkie pallet jacks now cost from about $1,640, but trucks that follow the operator hands-free are forklift-class products well beyond a small business. PalletPilot is an open retrofit kit that adds powered drive, a follow-me mode and layered stopping to the manual jack the site already owns.

## The problem

A manual pallet jack is the most common load mover in small facilities. A typical unit has 685 x 1220 mm (27 x 48 in) forks, a 2,500 kg (5,500 lb) rating, a 75 mm (3 in) lowered height and a mass of about 64 kg (140 lb), and costs about $396 new ([Global Industrial](https://www.globalindustrial.com/p/global-industrial-153-standard-duty-pallet-jack-truck-5500-lb-capacity-27-x-48-forks)).

Moving it loaded is hard work:

- **Force.** With a 1,000 kg pallet, the rolling force is about 130 N (13 kgf) and the force to start moving is about 270 N (28 kgf), assuming 1.2 % rolling resistance and 2.5 % breakaway resistance for polyurethane wheels on smooth concrete (estimates; to be measured). The widely used Liberty Mutual tables give maximum acceptable initial push forces of about 9 to 22 kg for 90 % of female workers, and sustained forces of about 4 to 14 kg, depending on handle height, distance and frequency ([Ciriello and Snook 1991, summarized by MHI](https://og.mhi.org/media/members/14023/130258038292642021.pdf)). A heavy pallet on a manual jack is at or past those limits every time it starts.
- **Walking time.** Order picking and staging are mostly walking. The operator pulls the jack, stops, walks back to pick, and pulls again. A truck that follows the operator removes the repeated grab, pull and release.

Three kinds of product exist, and none fits a small site well:

1. **Powered walkie pallet jacks.** A basic lithium walkie with 1,500 kg (3,300 lb) capacity now sells for about $1,640 ([Home Depot, Tory Carrier A-1034](https://www.homedepot.com/p/3300-lbs-24V-20AH-Lithium-Battery-Electric-Pallet-Jack-Walkie-Truck-w-48-in-x-27-in-Fork-Size-3-1-in-Fork-Lowered-A-1034/326396102)). This solves the force problem but not the walking problem, and the site's existing manual jacks sit idle.
2. **Bolt-on power kits.** The PowerHandling PowerPallet 2000 converts a manual jack to powered drive in 10 to 20 minutes, with a 1,590 kg (3,500 lb) rating and a top speed of 1.65 m/s (3.7 mph), for about $2,084 to $2,294 ([HoF Equipment](https://hofequipment.com/PowerHandling-Power-Pallet-2000-p1957.html); [F.E. Bennett](https://febennett.com/product/powerhandling-power-drive-retrofit-kit-for-pallet-jacks/)). It proves the retrofit idea works but costs more than a new walkie and has no follow mode.
3. **Follow-me trucks.** Jungheinrich's easyPILOT Follow, shown at LogiMAT 2018, lets a low-level order picker follow an operator who carries a UWB control unit, with laser scanners for obstacle detection ([Jungheinrich](https://www.jungheinrich.com/en/press-events/press-releases/easypilot-follow-faster-order-picking-with-the-new-semi-automatic-control-unit-158956)). It is an option on a full order-picking truck, not something a small business can add to a manual jack.

So a retrofit kit only earns its place if it does something a cheap walkie does not: follow-me operation, reuse of existing jacks and open, repairable parts. The kit's cost has to stay well below a new walkie plus a follow-me system.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Small warehouse or 3PL operator | Move 20 to 100 pallets a shift without a forklift or a second worker | Single shift, one to five staff, concrete floor, some ramps |
| Retail backroom and grocery receiving | Stage deliveries and restock aisles, often one person working alone | Tight aisles, customers nearby, early-morning deliveries |
| Workshop, maker space or small manufacturer | Move raw stock and finished goods between machines | Mixed traffic, cables and debris on the floor |
| Order picker | Pick cartons onto a pallet while walking an aisle, without pulling the jack at every stop | Stop-start, short moves of 2 to 10 m |
| Maintenance person | Fit, inspect and repair the kit with ordinary tools and parts | No dealer service contract |

### Operating environment

- **Floors:** sealed or bare concrete, level, with expansion joints, dock plates and short ramps up to about 2 % grade. Dust, stretch-wrap scraps and small debris are common.
- **Loads:** pallets of 200 to 1,500 kg on 1,200 x 1,000 mm (48 x 40 in) stringer or block pallets.
- **Traffic:** people on foot, other jacks, occasionally a forklift; customers in retail backrooms.
- **Climate:** indoor, 0 to 40 °C; unheated storage and loading bays in winter.
- **Power:** ordinary 120 V or 230 V outlets for overnight charging.

## Constraints

- Garage-buildable prototype, about $1,200 USD for the kit. The donor manual jack is not included.
- Bolt-on to a common 27 x 48 in manual jack with no welding, cutting or drilling of the jack's load-bearing structure, and removable to restore the jack.
- Keep the jack's 75 mm lowered height, fork length and its ability to enter a standard pallet.
- Walking pace only, with hardwired emergency stops and a stop on bumper contact, as the pitch states.
- Low-voltage (24 V class) DC system with a lithium iron phosphate pack.
- Legal and workplace rules: in the United States a motorized pallet jack is a powered industrial truck, so every operator needs formal training and evaluation under 29 CFR 1910.178(l) ([OSHA 1910.178](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.178); [summary](https://www.safetyvideos.com/OSHA-Regulations-for-Pallet-Jack-Use)). The same standard does not allow users to make modifications that affect capacity and safe operation without the manufacturer's prior written approval (1910.178(a)(4)). A retrofit on a jack in a workplace therefore needs the jack maker's approval or a different legal route. This is a central open question.
- A truck that moves with no one at the tiller comes close to the scope of ISO 3691-4 for driverless industrial trucks, which calls for personnel detection that stops the truck before it contacts a person ([ISO 3691-4](https://www.iso.org/standard/70660.html); [overview](https://www.fabrico.io/blog/iso-3691-4-driverless-industrial-trucks/)). How a follow-me mode is classified must be settled before any trial with people.

## Out of scope

- Powered lifting. The donor jack's hand pump stays.
- Autonomous navigation, mapping or fleet management.
- Ride-on platforms or speeds above walking pace.
- Outdoor use, rough ground and steep ramps.
- Use in hazardous (explosive) atmospheres, cold stores below 0 °C and food-grade washdown areas.
- A commercial product. The first builds are research and demonstration prototypes.

## Prior work

- **Manual pallet jacks.** Commodity 2,500 kg jacks at about $396 set the donor platform and its dimensions ([Global Industrial](https://www.globalindustrial.com/p/global-industrial-153-standard-duty-pallet-jack-truck-5500-lb-capacity-27-x-48-forks)).
- **Low-cost lithium walkies.** About $1,640 for a 1,500 kg, 24 V, 20 Ah walkie ([Home Depot](https://www.homedepot.com/p/3300-lbs-24V-20AH-Lithium-Battery-Electric-Pallet-Jack-Walkie-Truck-w-48-in-x-27-in-Fork-Size-3-1-in-Fork-Lowered-A-1034/326396102)). This is the price ceiling that a retrofit kit has to beat.
- **Retrofit power kits.** The PowerPallet 2000 shows a clamp-on drive unit with a quick-change lithium pack and a truck mode at 0.67 m/s (1.5 mph) ([HoF Equipment](https://hofequipment.com/PowerHandling-Power-Pallet-2000-p1957.html)).
- **Follow-me order pickers.** easyPILOT Follow pairs UWB operator tracking with laser scanners ([Jungheinrich](https://www.jungheinrich.com/en/press-events/press-releases/easypilot-follow-faster-order-picking-with-the-new-semi-automatic-control-unit-158956)). The laser scanners matter: UWB tells the truck where the operator is, not where anyone else is.
- **UWB ranging modules.** Qorvo's DWM3000 module ranges to about 10 cm precision on UWB channels 5 and 9 ([Qorvo](https://www.qorvo.com/products/p/DWM3000)), which makes a low-cost operator tag practical.
- **Ergonomic push limits.** Ciriello and Snook's tables set the target for how much the kit must take off the operator ([MHI summary](https://og.mhi.org/media/members/14023/130258038292642021.pdf)).

## Open questions

- Legal route for a workplace retrofit under 1910.178(a)(4): partner with a jack maker, sell or document it for a specific donor model with written approval, or limit it to non-workplace and research use. Proposed, awaiting Amish.
- Classification of follow-me mode (ISO 3691-4 or not) and the safety functions it then needs.
- Which donor jack models and steering yokes to support first.
- Are small sites willing to wear a UWB tag and to train every operator as a powered truck operator?
- Typical pallet mass and move distance per shift at real sites, to replace the assumed 60 moves of 40 m.

## User research and co-design

This design is for workplaces the author does not work in, so requirements come from the people who will use it.

- [ ] Identify two or three small warehouses, backrooms or workshops willing to host interviews and observation
- [ ] Observe a full shift: pallet masses, distances, floor condition, ramps, traffic and how often the operator walks back to the jack
- [ ] Talk to a safety professional and a jack maker about training and modification approval
- [ ] Revise requirements (REQ) from findings before freezing the design
