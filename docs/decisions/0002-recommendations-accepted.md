---
doc_id: PLP-DDR-002
title: PalletPilot recommendations accepted
project: PalletPilot
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of the TRL 3 review recommendations and what changed in the repo
- version: "0.2"
  date: '2026-09-26'
  author: Amish Chadha
  change: "Budget set to $1,610 to cover the priced BOM: decided by Amish, 2026-09-26; R17 met"
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted for items O4 to O6, and for the budget on 2026-09-26; items O1 to O3 remain proposed

## Context

The TRL 3 review note (`docs/REVIEW.md`, session 2026-09-25, TRL 3) and PLP-DDR-001 left six items as "Proposed, awaiting Amish". Three of them (O4, O5, O6) carried a recommendation; three (O1, O2, O3) did not. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is therefore decided in favor of it, and where the recommendation named one of several options, that option is the decision. Items with no recommendation stay open. TRL 4 remains on hold by Amish's instruction, so any recommendation that needs building, testing or purchasing is recorded as decided but on hold.

## Options considered

The options for each item are those in `docs/REVIEW.md` (TRL 3 session), PLP-DDR-001 Table 2 and PLP-CAL-001 v0.1.

## Decision

*Table 1. Items decided on 2026-09-25.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| O4 | Bumper-only stopping (R8): (a) limit bumper-only speed to 0.15 m/s, or (b) an edge with 65 mm or more of travel | Decided by Amish, 2026-09-25: go with recommendation. Option (a): any operation that relies on the bumper alone is limited to 0.15 m/s. Because the lidar layer is untested, follow mode also runs at 0.15 m/s or less until that layer is built and tested (was 0.2 m/s) | R8 target restated from 0.2 to 0.15 m/s and now met on paper (38 mm stop within 40 mm of travel); R4 interim follow limit 0.2 to 0.15 m/s; PLP-CAL-001 stop table and [S3] line; safety sections in PLP-PRC-001 and README; note on PLP-DWG-001 |
| O5 | Mass (1.7 kg) and cost ($30) overruns, and the R5 bearing gap | Decided by Amish, 2026-09-25: go with recommendation. Accept both overruns for now and recheck them at a motor quote, with no budget change. For R5, evaluate angle-of-arrival UWB and lidar leg tracking at TRL 4; decided but on hold, since TRL 4 is on hold | `budget_usd` stays at 1550. R15 mass and R17 are still reported as not met, marked "accepted for now". No R5 design change. The cost part is superseded by the 2026-09-26 budget decision below |
| O6 | Stop chain for PL d (R9): a second contactor or a driver with rated safe torque off | Decided by Amish, 2026-09-25: go with recommendation. Add a second main contactor in series, one per safety relay channel | BOM line 6 from $45 to $75; model part 6 now shows two contactors; kit mass 41.7 to 42.0 kg; BOM total $1,580 to $1,610; R9 target text restated; PLP-DWG-001 to Rev P2; PLP-CAL-001 to v0.2. R9 stays at risk until the PL is calculated |

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Named site and co-design partners (partner types were decided in PLP-DDR-001 D9) | Proposed, awaiting Amish; partners are picked per area later |
| O2 | Classification of follow mode under ISO 3691-4 and the safety functions it then needs | Proposed, awaiting Amish; no recommendation made |
| O3 | Which donor jack models and steering yokes to support first | Proposed, awaiting Amish; no recommendation made |

### Budget, 2026-09-26

On 2026-09-26 Amish wrote: "i approve all the budget items." Budget set to $1,610 to cover the priced BOM: decided by Amish, 2026-09-26. The priced BOM is $1,610 over 18 lines (`bom/bom.csv`), so `budget_usd` in `project.yaml` moves from 1550 to 1610 and R17 moves from not met (accepted for now) to met, with no margin. The motor quote is still the next paper check, since any rise in the motor price would take R17 over again. `docs/04-calcs/sizing.py` now checks against $1,610 and was rerun; PLP-CAL-001 v0.3, PLP-REQ-001 v0.5, PLP-PRC-001 v0.5, PLP-PRB-001 v0.4, `README.md` and `bom/bom-notes.md` were updated. The concept blueprint quotes the kit cost, not the budget, so `media/` was not regenerated. Requirement status is now 11 met, 2 not met (R5, R15 mass), 2 at risk and 3 not verifiable.

## Consequences

- Requirement status (PLP-CAL-001 v0.2): 10 met, 3 not met (R5, R15 mass, R17), 2 at risk (R7, R9), 3 not verifiable at TRL 3 (R1, R6, R16). Before these decisions it was 9 met, 3 not met, 3 at risk and 3 not verifiable.
- Numbers that moved: kit mass 41.7 to 42.0 kg; BOM total $1,580 to $1,610 (3.9 % over $1,550); energy from the pack 292 to 293 Wh per shift; unpowered push force rise 3.9 % to 4.0 %; bumper-only speed limit 0.2 to 0.15 m/s.
- Documents revised: PLP-REQ-001 and PLP-PRC-001 to v0.4, PLP-CAL-001 to v0.2, PLP-DDR-001 to v0.2, PLP-DWG-001 to Rev P2. `cad/src/model.py` re-exported to STEP and STL; concept media regenerated. `project.yaml` is unchanged apart from listing this record as evidence; the pitch, problem and budget are unchanged.
- Cross-repo actions: none. PalletPilot uses its own 24 V pack and shares no interface with another repo.
- On hold (TRL 4): the R5 evaluation of angle-of-arrival UWB and lidar leg tracking, which needs bench measurement. The motor quote that rechecks the overruns and the PL calculation of the stop chain are paper work at TRL 3 and are listed as the next step; no part is to be bought.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building, testing or buying.
