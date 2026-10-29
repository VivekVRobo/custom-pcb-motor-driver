# Component source and package verification

**Review date:** 2026-10-29  
**Scope:** BOM source traceability and package-selection blockers for preliminary Rev A.  
**Related issue:** [#10 — Add a component-source and package-verification table](https://github.com/VivekVRobo/custom-pcb-motor-driver/issues/10).

## Important current state

This table records manufacturer-published component identity and package information where found. It does **not** certify the PCB footprint mapping or the electrical design.

The current files `hardware/cad/custom_pcb_motor_driver.kicad_sch` and `hardware/cad/custom_pcb_motor_driver.kicad_pcb` are capture scaffolds: the schematic has explanatory text rather than placed symbols/wires, and the PCB has a board outline/nets but no assigned footprints or routed layout. Therefore, **all KiCad footprint mappings are currently unassigned and unverified**. A package body name in this table is not a selected KiCad footprint or proof that the pad geometry matches.

## BOM component source table

| Reference | BOM manufacturer part number | Manufacturer / authoritative source | Published package or dimensional identity | Verification status / action |
|---|---|---|---|---|
| U1 | `DRV8848PWPR` | [Texas Instruments — part details](https://www.ti.com/product/DRV8848/part-details/DRV8848PWPR) | HTSSOP-16, TI PWP package | **Identity verified.** Select the exact KiCad land pattern against the current TI recommended land pattern; verify every symbol pin-to-net mapping before ERC. |
| R_SENSE_A, R_SENSE_B | `WSL2512R5600FEA` | [Vishay — WSL family datasheet](https://www.vishay.com/doc?49581=) | WSL2512 body, nominal 2512 (6.35 × 3.18 mm) size class | **BOM blocker.** The published standard WSL2512 range is 0.007–0.5 Ω and its stated power rating is 1.0 W. The BOM calls for 0.56 Ω / 2 W, so the listed series/value/rating combination is not supported by that datasheet. Verify the exact order code or select a documented suitable part; do not release this BOM row as verified. |
| C_VM_HF | `GRM21BR71H104KA01L` | [Murata — part lookup](https://www.murata.com/en-global/products/productdetail?partno=GRM21BR71H104KA01L) | 0.1 µF, 50 V, X7R, 0805 / 2012 metric class | **Identity consistent with BOM.** Confirm recommended land pattern against the current Murata package drawing. |
| C_VM_LOCAL | `GRM32ER71E226KE15L` | [Murata — part lookup](https://www.murata.com/en-global/products/productdetail?partno=GRM32ER71E226KE15L) | 22 µF, 25 V, X7R, 1210 / 3225 metric class | **Nominal identity consistent.** Verify effective capacitance at the actual DC bias, temperature, and tolerance; 22 µF is the nominal part value, not a guaranteed in-circuit value at 12.6 V. |
| C_VINT | `GRM21BR71C225KA12L` | [Murata — part lookup](https://www.murata.com/en-global/products/productdetail?partno=GRM21BR71C225KA12L) | 2.2 µF, 16 V, X7R, 0805 / 2012 metric class | **Identity consistent; net review required.** The current schematic scaffold text equates VINT and VREF. Treat that as an unresolved annotation, not valid connectivity: verify the TI pin functions and keep the internal-regulator output and current-reference input distinct as required by the datasheet. |
| R_NFAULT | `RC0805JR-0710KL` | [Yageo — exact part specification](https://www.yageogroup.com/component-documentation/download/specsheet/RC0805JR-0710KL) | 10 kΩ, 5%, 0.125 W, 0805 / 2012 metric class | **Identity consistent.** Select the footprint from the exact resistor dimensions and land-pattern guidance. |
| J1, J2, J3 | `1935161` | [Phoenix Contact — PT 1,5/2-5,0-H](https://www.phoenixcontact.com/en-in/products/printed-circuit-board-terminal-pt-15-2-50-h-1935161) | Two-position through-hole PCB terminal block, **5.00 mm pitch** | **BOM description mismatch.** The manufacturer lists 5 mm pitch and 17.5 A nominal current; rated voltage depends on the applicable category/standard. The BOM currently says 5.08 mm and 16 A / 300 V. Correct the BOM description from the exact datasheet and verify the solder-pin/land geometry, clearance, and applicable rating before design release. |
| J4 | `61300911121` | [Würth Elektronik — WR-PHD 2.54 mm header family](https://www.we-online.com/en/components/products/em/connectors/board-to-board_connectors/wr-phd_pin_header_socket_header/wr-phd_pin_header_socket_header_2_54mm) | Straight, through-hole, 1×9 pin header, 2.54 mm pitch; catalog data lists 3 A | **Identity consistent with the BOM description.** Confirm the exact manufacturer's drawing and select/verify a matching KiCad footprint. |
| F1 | `0451003.MRL` | [Littelfuse — 451 / 453 Nano² fuse datasheet](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1) | Nano² SMD fuse family; BOM identifies 2410 package | **Part-specific review required.** Confirm the exact suffix, fuse curve, interrupt rating, derating, and recommended pads for `0451003.MRL`; family-level similarity alone is not sufficient. |
| D_TVS | `SMAJ15A` | [Bourns — SMAJ series](https://bourns.com/products/diodes/product-detail/tvs-diodes/smaj-series) · [Bourns short-form TVS guide](https://www.bourns.com/docs/technical-documents/technical-library/chip-diodes/publications/bourns_tvs_diode_short_form.pdf) | SMA / DO-214AC package class; SMAJ family is listed as 400 W TVS | **Family package identity found.** Confirm the exact 15 V part's working standoff, breakdown, clamp voltage, polarity, and pulse assumptions against the full part-specific datasheet and the actual supply/transient envelope. |
| Q_RPOL | `SI2301CDS-T1-GE3` | [Vishay — SI2301CDS datasheet](https://www.vishay.com/docs/68741/si2301cd.pdf) | P-channel MOSFET, SOT-23 / TO-236 | **Identity consistent, current claim needs context.** The −3.1 A figure is case-temperature dependent; it must not be presented as an unconditional PCB/ambient current rating. Check thermal dissipation, RDS(on), SOA, polarity, and the actual PCB copper before approving the reverse-polarity path. |
| C_BULK | `EEH-ZA1E221P` | [Panasonic — hybrid aluminum capacitor product information](https://industrial.panasonic.com/ww/products/pt/hybrid-aluminum/models/EEHZA1E221P) | 220 µF, 25 V, surface-mount hybrid capacitor; nominal case 8 × 10.2 mm | **Nominal identity consistent.** Verify the latest case drawing, land pattern, ripple-current conditions, ESR, life/temperature conditions, and placement constraints. |

## Required closure before CAD-ready review

- [ ] Resolve the sense-resistor mismatch. The present WSL2512 line does not substantiate a 0.56 Ω, 2 W component; choose a manufacturer-confirmed orderable component or update the design target with engineering justification.
- [ ] Correct the connector BOM pitch/rating description for Phoenix Contact `1935161`; use the manufacturer's exact drawing for land geometry.
- [ ] Resolve the VINT/VREF annotation against the TI DRV8848 datasheet and a real, wired schematic.
- [ ] Place actual KiCad symbols, wire the design from the authoritative net specification, and verify all pin functions and power connections.
- [ ] Assign KiCad footprints only after comparing each exact manufacturer's recommended land pattern/dimensional drawing with the library footprint. Record the library identifier and any deviation; do not infer it only from package shorthand.
- [ ] Run and archive KiCad ERC and PCB DRC results, review schematic-to-PCB pin/pad mapping, and resolve all release-blocking findings.

Until these items are resolved and recorded, this component table is a **traceability aid**, not BOM approval, CAD-ready evidence, fabrication approval, or hardware-validation evidence. The existing release gates should remain unchanged.
