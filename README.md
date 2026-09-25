# PalletPilot

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Mobility and Logistics · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $1,200 USD · **Difficulty:** 4 of 5

Retrofit kit that turns a manual pallet jack into a powered, walk-behind unit with a UWB follow-me mode and bumper-based stopping.

![PalletPilot concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Small warehouses move pallets by hand, and powered pallet trucks with follow-me modes cost more than they can justify. Starting a 1,000 kg pallet on a manual jack takes about 270 N (estimate), at or past common ergonomic push limits. Basic lithium walkies now cost about $1,640, but follow-me trucks are forklift-class products. Full problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

Retrofit kit that turns a manual pallet jack into a powered, walk-behind unit with a UWB follow-me mode and bumper-based stopping.

A sprung module with two 24 V hub motors clamps to the jack's steering yoke, with a 25.6 V 20 Ah LiFePO4 pack and the electronics in an enclosure above it. In walk mode the operator steers with the handle and a walkie-style tiller head. In follow mode the operator wears a UWB tag and the motors steer by differential drive to hold a 1.5 m gap. First-order estimates: a full shift of 60 pallet moves on one charge, about 37 kg added, about $1,425 in parts (over the $1,200 budget). The concept study found that a bumper alone cannot stop a loaded jack in time at follow-mode speed, so non-contact sensing is proposed (awaiting Amish). Requirements not met are listed in [docs/03-requirements.md](docs/03-requirements.md).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Drive module with two 24 V, 200 mm hub motors and spring-applied brakes
- Dual-channel motor driver
- 25.6 V 20 Ah LiFePO4 pack with BMS
- Tiller control head with throttle, belly-reverse paddle and mode key
- Two hardwired emergency stops and a safety relay
- Contact bumper (safety edge)
- Three UWB anchors and an operator tag
- ESP32-S3 class controller

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Moving machinery near people. The design must use hardwired emergency stops, a speed limit at walking pace and a bumper that stops the unit on contact. A bumper alone cannot stop a loaded jack before contact above about 0.2 m/s, so follow mode stays at creep speed in a closed area until non-contact sensing is fitted. Contains a lithium battery pack. Use a BMS with cell-level protection, fuse the pack, and charge on a non-combustible surface. In the United States a powered pallet jack needs trained operators and the jack maker's approval for modifications (29 CFR 1910.178). Builds are research prototypes, not certified industrial trucks. See [docs/02-concept.md](docs/02-concept.md#safety).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
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

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
