# Fabrication / Ordering Guide — BLOCKED UNTIL CAD VALIDATION

**Board:** TI DRV8848 Dual Motor Driver (Rev-A design study)  
**Current CAD maturity:** capture scaffold only  
**Fabrication status:** **DO NOT ORDER / DO NOT FABRICATE**

> The files in this directory are not a released manufacturing package. The committed KiCad PCB is explicitly marked `UNROUTED / UNVALIDATED — DO NOT FABRICATE`, and the repository's CAD/fabrication gates remain false. The existing `gerbers_drv8848_revA.zip` and `gerbers_revA/` files are retained only as historical/placeholder artifacts; they are **not approved fabrication outputs** and must not be uploaded to a board house for production.

## Why ordering is blocked

The current `custom_pcb_motor_driver.kicad_pcb` contains an initial **45 mm × 35 mm** board outline and named nets, but it does not contain the completed component placement, routing, PowerPAD thermal-via implementation, mounting-hole implementation, copper pours, or verified fabrication geometry described by earlier planning documents.

Earlier draft documents referenced a **48 mm × 36 mm** target and fabrication details such as four M3 holes and nine PowerPAD thermal vias. Those values are design targets/history, **not evidence of what is implemented in the current KiCad PCB**.

## Required release gate before any order

Do not create or place a fabrication order until all of the following are complete and reviewed on the exact release commit:

- [ ] DRV8848 and all supporting components are captured in the KiCad schematic.
- [ ] Manufacturer pin mappings and every footprint are independently verified.
- [ ] KiCad ERC passes, or every waiver is documented and reviewed.
- [ ] PCB is updated from the reviewed schematic.
- [ ] Final board outline and mounting-hole dimensions are measured from the PCB source and documented.
- [ ] Component placement is complete.
- [ ] Power/current paths are routed for the intended electrical envelope.
- [ ] DRV8848 exposed-pad copper and thermal-via strategy is implemented and reviewed.
- [ ] Ground planes/pours, clearances, connector orientation, polarity and test access are reviewed.
- [ ] KiCad DRC passes, or every waiver is documented and reviewed.
- [ ] Solder-mask, paste, silkscreen, drill and edge geometry are visually inspected.
- [ ] Final Gerber/drill outputs are regenerated **from the validated KiCad source**.
- [ ] Gerbers are CAM-reviewed and their SHA-256 hashes are recorded.
- [ ] `hardware/design_values.yaml` fabrication gates are advanced only after the evidence above exists.
- [ ] The exact manufacturing archive is tagged/released so the ordered files can be traced back to source.

## Board-house parameters

Parameters such as material, copper weight, surface finish, minimum trace/spacing, drill sizes and stencil details must be selected from the **validated final layout and electrical/thermal review**, not copied blindly from this draft repository.

A future fabrication-ready revision should publish an immutable manufacturing package containing the items defined in [`docs/MANUFACTURING_RELEASE.md`](../../docs/MANUFACTURING_RELEASE.md), including the final board dimensions, stack-up, Gerbers/drills, ERC/DRC evidence, BOM, fabrication/assembly notes and checksums.

## Component sourcing

`hardware/BOM.csv` is the repository's sourcing reference. Distributor stock, lifecycle status, exact orderable part numbers and substitutions are time-sensitive and must be re-verified immediately before procurement. A sourcing list is not proof that the PCB itself is fabrication-ready.

## Evidence boundary

This guide intentionally contains **no “upload this ZIP and order” instruction** while the CAD release gate is false. When a real validated manufacturing package exists, this document can be promoted from a blocked checklist into a board-house-specific ordering procedure using values measured from that exact released package.
