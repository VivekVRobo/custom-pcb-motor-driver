# v0.1.0 Release Readiness

This checklist defines the minimum bar for the first tagged release of `custom-pcb-motor-driver`.

The first release is an **engineering-reference release**. It may publish the design intent, calculations, KiCad sources, BOM traceability, preliminary manufacturing outputs and automated checks, but it must not imply that the board is fabrication-ready or hardware-validated unless those gates have actually passed.

## Required before tagging

- [ ] Engineering checks are green on the exact release commit.
- [ ] Unit-tested electrical calculations complete successfully.
- [ ] BOM/netlist/KiCad source checks pass.
- [ ] README release truth table matches the exact repository state.
- [ ] Preliminary Gerber/drill outputs remain clearly labelled as candidate/review artifacts unless `fab-ready` passes.
- [ ] `hardware_evidence: false` / equivalent truth boundaries remain intact in analytical artifacts.
- [ ] Datasheet traceability documents remain linked and current.
- [ ] `LICENSE` is present and accurate.
- [ ] Release notes state whether ERC/DRC, fabrication and bench validation are still pending.

## Allowed v0.1.0 claims

The first release may claim:

- a DRV8848-based dual brushed-DC motor-driver reference design;
- documented electrical sizing and tolerance-aware calculations;
- current-limit, conduction-loss and thermal screening models;
- KiCad project/schematic/PCB source files;
- BOM and datasheet traceability;
- PCB layout/manufacturing guidance;
- preliminary Rev-A manufacturing outputs for review;
- automated engineering checks;
- a documented first-article bring-up protocol.

## Claims that remain blocked until their gates pass

Do not claim:

- `cad-ready` unless the required native CAD/ERC/DRC review has passed;
- `fab-ready` unless the manufacturing-release gate and final human review have passed;
- fabricated hardware unless a physical board exists;
- measured current-limit, thermal, stall or load performance without bench evidence;
- safety certification or production qualification.

## Promotion rule

Tag `v0.1.0` only from a clean commit satisfying this checklist. Later releases may promote `cad-ready`, `fab-ready` or `hardware-validated` status only when the corresponding repository gates and evidence exist.