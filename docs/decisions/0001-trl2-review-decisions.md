---
doc_id: PLP-DDR-001
title: PalletPilot TRL 2 review decisions
project: PalletPilot
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D9; items O4 to O6 decided on 2026-09-25 in PLP-DDR-002; items O1 to O3 remain proposed

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", each with a recommendation. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." For PalletPilot the instruction added that the approved safety recommendation is the low-cost lidar or time-of-flight stop layer (option 1A), that the approved budget is about $1,550, and that the pitch changes to "layered stopping". Every item with a recommendation is therefore decided in favor of it. Items without a recommendation stay open.

The same instruction approved portfolio-wide SwapCell interface changes (a wake method for hosts without CAN, a charge-while-discharging mode, a latch vibration rating) and pricing shared SwapCell packs once. They do not apply to PalletPilot, which uses its own 24 V pack (D4). It also confirmed that co-design partners are picked per area later.

## Options considered

The options for each item are those in `docs/REVIEW.md` (TRL 2 session) and in PLP-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Decided items.*

| # | Item | Decision |
| --- | --- | --- |
| D1 | Follow-mode stopping and the pitch | Option A: a low-cost 2D lidar or time-of-flight sensor is the main stopping layer in follow mode, the contact bumper is the last layer, follow mode runs at 0.6 m/s or less, and trials are for research in a closed area. A safety-rated laser scanner (option B) is named as the route to workplace use. The pitch changes from "bumper-based stopping" to "layered stopping". Decided by Amish, 2026-09-25: go with recommendation. |
| D2 | Budget | Raise `budget_usd` from $1,200 to $1,550 (the figure given with option 1A). The donor jack stays excluded. Decided by Amish, 2026-09-25: go with recommendation. |
| D3 | Drive layout | Two hub motors on a sprung module on the steering yoke, steering by differential drive in follow mode. Decided by Amish, 2026-09-25: go with recommendation. |
| D4 | Power system | 24 V (25.6 V nominal) LiFePO4, 20 Ah, not a SwapCell pack. Decided by Amish, 2026-09-25: go with recommendation. |
| D5 | Mounting | Pack and electronics on the steering yoke, not the forks, checked at TRL 3 for handle clearance and bearing load. Decided by Amish, 2026-09-25: go with recommendation. |
| D6 | Speeds | Walk 1.2 m/s handle-end first, 0.8 m/s forks first, creep 0.3 m/s, follow 0.6 m/s. Follow mode stays at 0.2 m/s or less until the lidar layer is built and tested. Decided by Amish, 2026-09-25: go with recommendation. |
| D7 | Kit rating | 1,000 kg design load; 1,500 kg maximum at 0.8 m/s or less, below the donor's 2,500 kg. Decided by Amish, 2026-09-25: go with recommendation. |
| D8 | Legal route for workplace use | Document the kit for research use now, and approach a jack maker for written approval under 29 CFR 1910.178(a)(4) before any workplace trial. Decided by Amish, 2026-09-25: go with recommendation. |
| D9 | First site partner types | One small warehouse and one maker space. Decided by Amish, 2026-09-25: go with recommendation. The named partners remain open (O1). |

*Table 2. Items left open at v0.1 (no recommendation was made, or raised at TRL 3). O4 to O6 are now decided in PLP-DDR-002.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Named site and co-design partners | Proposed, awaiting Amish; partners are picked per area later |
| O2 | Classification of follow mode under ISO 3691-4 and the safety functions it then needs | Proposed, awaiting Amish; no recommendation made |
| O3 | Which donor jack models and steering yokes to support first | Proposed, awaiting Amish; no recommendation made |
| O4 | Bumper-only speed or bumper travel (R8): 0.15 m/s limit or an edge with 65 mm or more of travel | Decided by Amish, 2026-09-25: go with recommendation (0.15 m/s limit); see PLP-DDR-002 |
| O5 | Closing the mass (1.7 kg) and cost ($30) overruns, and the R5 bearing gap | Decided by Amish, 2026-09-25: go with recommendation (accept for now, recheck at the motor quote, no budget change; R5 fixes evaluated at TRL 4, on hold); see PLP-DDR-002 |
| O6 | A second contactor or rated safe torque off for PL d (R9) | Decided by Amish, 2026-09-25: go with recommendation (second contactor); see PLP-DDR-002 |

## Consequences

- `project.yaml`: `budget_usd` is 1550 and the pitch reads "layered stopping". The problem line is unchanged, since no rewording was recommended.
- PLP-PRB-001, PLP-PRC-001 and PLP-REQ-001 are revised to v0.3. R7 is redefined as the lidar layer's stop, R17 carries the $1,550 target, R2 and R8 carry the decided rating and speeds, and the design choices are no longer "proposed".
- The model, drawing PLP-DWG-001, calculation note PLP-CAL-001 and the BOM (new line 18, obstacle lidar) use the decided configuration.
- Workplace use stays excluded until D8's approval route and O2 are settled.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
