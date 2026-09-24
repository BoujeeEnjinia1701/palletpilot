# PalletPilot

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Mobility and Logistics · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $1,200 USD · **Difficulty:** 4 of 5

Retrofit kit that turns a manual pallet jack into a powered, walk-behind unit with a UWB follow-me mode and bumper-based stopping.

## Problem

Small warehouses move pallets by hand, and powered pallet trucks with follow-me modes cost more than they can justify.

## Concept

Retrofit kit that turns a manual pallet jack into a powered, walk-behind unit with a UWB follow-me mode and bumper-based stopping.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Hub motor drive wheel module
- UWB anchor and tag pair
- Motor controller
- 24 V LiFePO4 pack
- Contact bumper strips
- Emergency stop
- Microcontroller

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Moving machinery near people. The design must use hardwired emergency stops, a speed limit at walking pace and a bumper that stops the unit on contact. Contains a lithium battery pack. Use a BMS with cell-level protection, fuse the pack, and charge on a non-combustible surface.

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
