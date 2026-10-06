# v0.1.0 Release Notes Draft

`custom-pcb-motor-driver` v0.1.0 is intended as the first **engineering-reference** release.

## Included

- DRV8848 dual brushed-DC motor-driver reference design;
- tolerance-aware current-limit and electrical calculations;
- thermal/conduction-loss screening;
- KiCad project, schematic and PCB sources;
- BOM and datasheet traceability;
- layout/manufacturing guidance;
- preliminary Rev-A manufacturing outputs for review;
- automated engineering checks;
- first-article bring-up protocol.

## Evidence boundary

This release does **not** claim that the board is fabrication-ready or hardware-validated unless the corresponding repository gates have passed on the release commit.

If native ERC/DRC review, final manufacturing review, fabrication or bench measurements are still pending, the release notes must state that explicitly.

## Before publication

Publish only after the exact tag commit satisfies `docs/RELEASE_READINESS.md` and the repository's required checks are green.