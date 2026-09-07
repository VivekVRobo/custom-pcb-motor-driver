# CAD Validation Checklist — Rev A

Use this checklist only against the actual KiCad project. A checked item means the corresponding evidence has been inspected and retained; it is not a planning checkbox.

## Schematic capture

- [ ] DRV8848 symbol pin numbers verified against current TI datasheet
- [ ] Exposed PowerPAD electrical/thermal intent documented
- [ ] `VINT` / `VREF` connectivity matches `netlist_spec.yaml`
- [ ] A/B current-sense networks match reference design values
- [ ] VM decoupling and local bypass parts are present and correctly rated
- [ ] `nSLEEP` and `nFAULT` nets are correctly connected and exposed as intended
- [ ] Motor outputs, logic inputs, power input, and ground connector pinouts are verified
- [ ] Application-specific protection choices are resolved or explicitly blocked
- [ ] Schematic annotations/reference designators are final for Rev A

## Footprints

For every critical component record manufacturer part number, package drawing, KiCad footprint, and reviewer initials/notes.

| Ref | Manufacturer part | Package | KiCad footprint | Verified |
|---|---|---|---|---|
| U1 | DRV8848PWPR | HTSSOP / PowerPAD | | |
| R sense A | | | | |
| R sense B | | | | |
| VM bulk | | | | |
| VINT cap | | | | |
| Connectors | | | | |

- [ ] Pad numbering matches datasheet pin numbering
- [ ] PowerPAD dimensions and solder-mask/paste intent reviewed
- [ ] Connector orientation/polarity physically unambiguous
- [ ] Courtyard/clearance requirements reviewed

## ERC evidence

- KiCad version:
- Project commit SHA:
- ERC report path:
- ERC date:

- [ ] ERC completed
- [ ] Zero unexplained errors
- [ ] Every warning reviewed individually
- [ ] Any intentional suppression documented with rationale

## PCB placement

- [ ] Board outline verified against intended mechanical envelope
- [ ] Driver placed to support short high-current paths
- [ ] Sense resistors placed according to current/ground-return intent
- [ ] Decoupling placed close to relevant pins
- [ ] PowerPAD copper strategy implemented
- [ ] Thermal vias implemented and reviewed
- [ ] Logic routing separated sensibly from noisy motor-current paths
- [ ] Test points accessible after assembly
- [ ] Connector placement/orientation reviewed mechanically

## Routing / copper

- [ ] VM and motor-current trace widths reviewed against actual copper stack/current target
- [ ] Ground return paths reviewed
- [ ] Ground plane continuity reviewed
- [ ] Sense paths do not share avoidable high-current drops
- [ ] Thermal copper around U1 reviewed
- [ ] No avoidable neck-downs on motor-current paths

## DRC evidence

- DRC report path:
- DRC date:

- [ ] DRC completed
- [ ] Zero unexplained violations
- [ ] Every exception documented

## Fabrication outputs

- [ ] Gerbers generated from reviewed board revision
- [ ] Drill files generated
- [ ] Gerber viewer inspection completed
- [ ] Copper layers inspected
- [ ] Mask layers inspected
- [ ] Silkscreen polarity / connector labels inspected
- [ ] Drill alignment inspected
- [ ] Board outline inspected
- [ ] BOM reviewed for orderability
- [ ] Position file reviewed if assembly is planned

## Gate decision

### CAD-ready

May be marked true only when schematic capture, footprint review, and ERC evidence above are complete.

- [ ] `schematic_complete`
- [ ] `footprint_verified`
- [ ] `erc_passed`

### Fab-ready

May be marked true only after actual layout/routing, DRC, and fabrication-output review.

- [ ] `pcb_layout_complete`
- [ ] `drc_passed`
- [ ] `gerbers_reviewed`

### Still blocked after fab-ready

The following require physical evidence and must remain false until a real board exists:

- fabricated
- bring-up passed
- load tested
- thermal validated
- stall/fault behavior validated

## Reviewer note

A reviewer should be able to trace:

`datasheet/BOM -> schematic -> footprints -> ERC -> PCB -> DRC -> Gerbers -> fabrication -> bench evidence`
