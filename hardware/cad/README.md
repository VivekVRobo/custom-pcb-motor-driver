# CAD Handoff

This directory now contains a **KiCad-native capture scaffold** for the Rev-A reference design:

```text
custom_pcb_motor_driver.kicad_pro
custom_pcb_motor_driver.kicad_sch
custom_pcb_motor_driver.kicad_pcb
netlist_spec.yaml
```

The important distinction is that **CAD source exists, but CAD validation has not been claimed**.

## Current status

- `netlist_spec.yaml` is the machine-readable electrical connectivity contract.
- The VREF reference is intentionally tied to the DRV8848 `VINT` rail, so `U1.VINT`, `U1.VREF`, `C_VINT.1`, and `J4.VREF` belong to one physical net.
- The PCB scaffold contains the named electrical nets and an initial board outline only.
- The schematic scaffold is intentionally marked `UNVALIDATED` and is the handoff point for verified symbol placement/wiring in KiCad.
- Application-specific fuse, reverse-polarity, TVS, optional bulk-capacitor selections are still blockers for a complete release schematic.
- No fabrication-ready routing, Gerbers, ERC result, DRC result, or footprint-verification claim exists yet.

## Why the validation flags remain false

Creating `.kicad_sch` or `.kicad_pcb` files is **not** proof that symbols, footprints, pin mapping, clearances, thermal layout, ERC, or DRC are correct. Therefore `hardware/design_values.yaml` intentionally keeps these gates false:

```yaml
schematic_complete: false
footprint_verified: false
erc_passed: false
pcb_layout_complete: false
drc_passed: false
gerbers_reviewed: false
```

`tools/kicad_source_lint.py` performs only conservative repository checks such as S-expression balance, expected net names and protection against accidental fabrication claims. It explicitly does **not** replace KiCad ERC/DRC.

## Required KiCad validation sequence

1. Open `custom_pcb_motor_driver.kicad_pro` in a current KiCad release.
2. Capture/verify the DRV8848PWPR symbol using the datasheet pinout and exposed PowerPAD grounding requirement.
3. Place every BOM component and resolve the application-specific protection components.
4. Wire the schematic to match `netlist_spec.yaml` exactly.
5. Run KiCad ERC and review every warning/error rather than suppressing it blindly.
6. Verify each footprint against its manufacturer package drawing and intended assembly process.
7. Update PCB from schematic, place components, implement the PowerPAD copper/thermal-via strategy and power-current paths.
8. Route the board and add ground copper/planes.
9. Run DRC, inspect clearances/current paths/thermal layout, and perform schematic-to-PCB parity review.
10. Generate and inspect Gerbers/drill files before advancing the fabrication gate.

Only after the corresponding evidence exists should the validation fields be changed to `true`.

The release gate deliberately continues to fail `cad-ready` and `fab-ready` today. That is intentional: the repository cannot silently turn a generated scaffold into a fake validation claim.
