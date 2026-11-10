# Component Source & Package Traceability — Rev A

This table is a review aid for the current engineering-reference BOM. It records the selected manufacturer part numbers, the package information explicitly verified from manufacturer sources in this review, and the current KiCad-footprint verification state.

**Scope:** documentation/traceability only. This file does not make the board CAD-ready, fab-ready, fabricated, or hardware-validated.

| Ref | Category | Manufacturer | MPN | Package / form | KiCad footprint | Source / verification |
|---|---|---|---|---|---|---|
| U1 | Motor driver | Texas Instruments | DRV8848PWPR | HTSSOP (PWP), 16-pin, 5.0 × 6.4 mm, exposed PowerPAD | **Unverified in KiCad** | [TI product page](https://www.ti.com/product/DRV8848) — exact MPN/package verified |
| R_SENSE_A | Current sense | Vishay Dale | WSL2512R5600FEA | 2512 SMD current-sense resistor | **Unverified in KiCad** | [Vishay Power Metal Strip family](https://www.vishay.com/en/product/30123/) — family/source verified; exact MPN/package drawing still requires direct part-level review |
| R_SENSE_B | Current sense | Vishay Dale | WSL2512R5600FEA | 2512 SMD current-sense resistor | **Unverified in KiCad** | Same source as R_SENSE_A |
| C_VM_HF | Decoupling | Murata | GRM21BR71H104KA01L | 0805 (2012M), X7R, 50 V | **Unverified in KiCad** | [Murata MLCC part-number list](https://www.murata.com/-/media/webrenewal/tool/library/common-pdf/dynamic-model/component-list-d-mlcc-2504.ashx?cvid=20250523010405000000&la=en) — matching GRM21BR71H104KA01 family/package verified |
| C_VM_LOCAL | Decoupling | Murata | GRM32ER71E226KE15L | 1210 family/package code L | **Unverified in KiCad** | [Murata product datasheet](https://www.murata.com/en-global/api/pdfdownloadapi?cate=luCeramicCapacitorsSMD&partno=GRM32ER71E226KE15%23) — exact part family/package-code source verified |
| C_VINT | Decoupling | Murata | GRM21BR71C225KA12L | 0805 SMD ceramic capacitor | **Unverified in KiCad** | Manufacturer source should be checked at part level before the footprint is marked verified |
| R_NFAULT | Logic | Yageo | RC0805JR-0710KL | 0805 SMD resistor | **Unverified in KiCad** | Manufacturer part-level source not independently verified in this review |
| J1 | Power connector | Phoenix Contact | 1935161 | 2-position PCB terminal block, 5.0 mm pitch, 17.5 A, wave-solder mount | **Unverified in KiCad** | [Phoenix Contact product page](https://www.phoenixcontact.com/en-us/products/pcb-terminal-block-pt-15-2-50-h-1935161) — exact MPN/form verified |
| J2 | Motor connector | Phoenix Contact | 1935161 | 2-position PCB terminal block, 5.0 mm pitch, 17.5 A, wave-solder mount | **Unverified in KiCad** | Same source as J1 |
| J3 | Motor connector | Phoenix Contact | 1935161 | 2-position PCB terminal block, 5.0 mm pitch, 17.5 A, wave-solder mount | **Unverified in KiCad** | Same source as J1 |
| J4 | Logic header | Würth Elektronik | 61300911121 | WR-PHD, 1×9, 2.54 mm, straight THT, 3 A, 22.86 mm | **Unverified in KiCad** | [Würth WR-PHD product family](https://www.we-online.com/en/components/products/BTB_WR_PHD_2_54_MM_PIN_HEADER_SINGLE) and [manufacturer datasheet](https://www.we-online.com/components/products/datasheet/61300911121.pdf) — exact MPN/form verified |
| F1 | Protection | Littelfuse | 0451003.MRL | Nano2 / 2410 SMD fuse | **Unverified in KiCad** | Manufacturer family source requires part-level confirmation before footprint verification |
| D_TVS | Protection | Bourns | SMAJ15A | SMA / DO-214AC, 400 W TVS | **Unverified in KiCad** | [Bourns TVS technical documentation](https://www.bourns.com/docs/technical-documents/technical-library/chip-diodes/publications/bourns_esd1710_tvs_diode_short_form_update_jp.pdf) — SMAJ15A/SMA family and 400 W rating verified |
| Q_RPOL | Protection | Vishay Siliconix | SI2301CDS-T1-GE3 | TO-236 / SOT-23, 3-pin P-channel MOSFET | **Unverified in KiCad** | [Vishay SI2301CDS datasheet](https://www.vishay.com/docs/68741/si2301cd.pdf) — exact ordering code and SOT-23 package verified |
| C_BULK | Input bulk | Panasonic | EEH-ZA1E221P | Surface-mount hybrid polymer aluminum capacitor, Ø8 × 10.2 mm, 25 V, 220 µF | **Unverified in KiCad** | [Panasonic product page](https://industrial.panasonic.com/tw/products/pt/hybrid-aluminum/models/EEHZA1E221P) — exact MPN, electrical rating and body dimensions verified |

## Verification rules

- **Verified source** means the manufacturer source explicitly identifies the part number or the exact product family/package used by the selected MPN.
- **Unverified in KiCad** means the manufacturer package information has not yet been reconciled against the actual KiCad footprint in the committed schematic/PCB. Do not fill this column from a generic library name.
- Where the exact manufacturer MPN could not be independently verified during this documentation pass, the row deliberately says so instead of guessing.
- A package match does **not** by itself prove pad numbering, courtyard clearance, paste/solder-mask treatment, exposed-pad geometry, or assembly suitability.
- The authoritative electrical/connectivity sources remain `hardware/reference_profiles/drv8848.yaml`, `hardware/design_values.yaml`, and `hardware/cad/netlist_spec.yaml`.

## Review status

This document satisfies the traceability/documentation portion of the component-source issue. It does **not** close the CAD verification gates.

The next verification step is to reconcile each selected MPN against the actual KiCad symbol/footprint and record the footprint library identifier plus reviewer evidence in `hardware/cad/CAD_VALIDATION_CHECKLIST.md`.
