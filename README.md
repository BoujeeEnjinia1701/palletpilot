# PalletPilot

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Mobility and Logistics · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** $1,550 USD · **Difficulty:** 4 of 5

Retrofit kit that turns a manual pallet jack into a powered, walk-behind unit with a UWB follow-me mode and layered stopping.

![PalletPilot concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement PLP-DWG-001 (PDF)](cad/drawings/PLP-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Most small sites already own one or more manual pallet jacks, and the jack's forks, pump and load wheels already do the hard part: lifting and carrying the pallet. What the operator lacks is drive and, for picking, a way to stop walking back to the handle. A bolt-on drive module on the steering yoke adds both without touching the jack's load path, and it can be removed to restore the jack. The kit uses parts a small shop can buy or make: AGV hub motors, a 24 V LiFePO4 pack, folded sheet metal, a commodity 2D lidar and UWB modules.

Keeping the design open matters because the likely users have no dealer service contract. Published drawings, a priced bill of materials and the sizing script let a maintenance person repair it, adapt the clamp to another donor jack, and check the safety numbers for themselves. The kit is a research prototype, not a certified industrial truck.

## Burning platform

Moving loads by hand is one of the most common causes of work injury. In the United States, warehousing and storage recorded 4.8 injury and illness cases per 100 full-time workers in 2024 ([BLS, Warehousing and Storage](https://www.bls.gov/iag/tgs/iag493.htm)), about twice the private industry rate of 2.3 ([BLS, Employer-Reported Workplace Injuries and Illnesses](https://www.bls.gov/news.release/osh.nr0.htm)).

In the European Union, about three in five workers report musculoskeletal complaints, and 52 % of establishments name lifting or moving people or heavy loads as a risk factor ([EU-OSHA, Healthy Workplaces 2020 to 2022](https://healthy-workplaces.osha.europa.eu/en/previous-campaigns/musculoskeletal-disorders-2020-22/what-issue)). Powered trucks remove most of that effort, but small sites with a handful of staff are the ones least able to buy them.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Small warehousing and third-party logistics | Staging, put-away and loading without a forklift or a second worker |
| Grocery and retail backrooms | Receiving early-morning deliveries and restocking aisles, often by one person |
| Beverage and food distribution | Short, repeated moves of heavy pallets from dock to cooler or truck |
| Light manufacturing and workshops | Moving raw stock and finished goods between machines |
| Maker spaces and training centers | Shared material handling and teaching of safe powered-truck practice |
| Agricultural packhouses | Moving filled crates and bins from packing lines to cold rooms |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| United States | Warehousing injury rate about twice the private industry average ([BLS](https://www.bls.gov/iag/tgs/iag493.htm)); OSHA 1910.178 sets the training and modification-approval route |
| European Union | About three in five workers report musculoskeletal complaints ([EU-OSHA](https://healthy-workplaces.osha.europa.eu/en/previous-campaigns/musculoskeletal-disorders-2020-22/what-issue)); many small distributors and workshops share manual jacks |
| Japan | An ageing workforce in logistics makes reducing push force and walking a practical way to keep experienced staff working |
| India | Manual jacks are common at small distributors; a low-cost, locally repairable retrofit avoids importing a complete powered truck |
| Brazil | Small wholesalers and supermarkets that move pallets by hand and cannot justify a powered fleet |
| Kenya and East Africa | Distributors and packhouses where powered trucks are scarce and a kit built from commodity parts can be maintained locally |

## What sparked the idea

The starting point was Piaggio Fast Forward's gita, a personal cargo robot that went on sale on November 18, 2019 for $3,250. It pairs with its owner through on-board cameras and sensors and follows them at up to about 2.7 m/s (6 mph), carrying up to about 18 kg (40 lb) ([VentureBeat](https://venturebeat.com/business/gita-is-a-3250-personal-cargo-robot-that-follows-you-around)). At the other end of the scale, follow-me operation for pallets comes as an option on full order-picking trucks such as Jungheinrich's easyPILOT Follow. Nothing sat between them: a follow-me mode for a 1,000 kg pallet at a price a small site can pay. PalletPilot fills that gap by adding the follow-me mode, with layered stopping, to the manual jack the site already owns.

## Problem

Small warehouses move pallets by hand, and powered pallet trucks with follow-me modes cost more than they can justify. Starting a 1,000 kg pallet on a manual jack takes about 270 N (estimate, PLP-CAL-001), at or past common ergonomic push limits. Basic lithium walkies now cost about $1,640, but follow-me trucks are forklift-class products. Full problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

Retrofit kit that turns a manual pallet jack into a powered, walk-behind unit with a UWB follow-me mode and layered stopping.

A sprung module with two 24 V hub motors clamps to the jack's steering yoke, with a 25.6 V 20 Ah LiFePO4 pack and the electronics in a low enclosure under the handle's sweep. In walk mode the operator steers with the handle and a walkie-style tiller head. In follow mode the operator wears a UWB tag and the motors steer by differential drive to hold a 1.5 m gap. Stopping is layered: a 2D lidar watches a 0.86 m field ahead of the truck in follow mode, hardwired emergency stops act through a dual-channel safety relay and two contactors in series, and a contact bumper is the last layer.

The sizing note ([PLP-CAL-001](docs/04-calcs/01-sizing.md)) finds that the kit moves 1,000 kg, starts on a 2 % ramp, works a 60-move shift with 29 % of the pack left and stops from 0.6 m/s in 0.42 to 0.76 m. Three targets are missed on paper: follow bearing accuracy (about ±16° against ±10°), kit mass (42.0 kg against 40 kg) and cost ($1,610 against $1,550); Amish has accepted the mass and cost overruns for now, to be rechecked at a motor quote. Requirement status is in [docs/03-requirements.md](docs/03-requirements.md); decisions are in [PLP-DDR-001](docs/decisions/0001-trl2-review-decisions.md) and [PLP-DDR-002](docs/decisions/0002-recommendations-accepted.md).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Drive module with two 24 V, 200 mm hub motors and spring-applied brakes
- Dual-channel motor driver
- 25.6 V 20 Ah LiFePO4 pack with BMS
- Tiller control head with throttle, belly-reverse paddle and mode key
- Two hardwired emergency stops, a safety relay and two main contactors
- 2D lidar stop layer for follow mode
- Contact bumper (safety edge) as the last layer
- Three UWB anchors and an operator tag
- ESP32-S3 class controller

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Moving machinery near people. The design uses hardwired emergency stops, walking-pace speed limits, a lidar stop layer in follow mode and a bumper that stops the unit on contact. The lidar is not safety-rated, so follow mode stays at 0.15 m/s or less in a closed area until the layer is built and tested. Contains a lithium battery pack. Use a BMS with cell-level protection, fuse the pack, and charge on a non-combustible surface. In the United States a powered pallet jack needs trained operators and the jack maker's written approval for modifications (29 CFR 1910.178). Builds are research prototypes, not certified industrial trucks. See [docs/02-concept.md](docs/02-concept.md#safety).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | General arrangement PLP-DWG-001 (generated by `cad/src/sheets.py`) |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (PLP-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `PLP-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.
