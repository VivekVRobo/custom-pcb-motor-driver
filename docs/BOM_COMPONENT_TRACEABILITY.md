# BOM component-source and package traceability

This table ties the current reference BOM to the manufacturer part number already recorded in hardware/BOM.csv. It is a traceability aid, not a fabrication-release approval.

| Ref | MPN | Manufacturer | Current repository package / footprint description | Authoritative source | Verification state |
| --- | --- | --- | --- | --- | --- |
| U1 | DRV8848PWPR | Texas Instruments | HTSSOP-16 / PWP | https://www.ti.com/product/DRV8848 | **Verified family + package** |
| R_SENSE_A | WSL2512R5600FEA | Vishay Dale | 2512, 2 W, 1% low-inductance metal-strip | https://www.vishay.com/en/landingpage/sampleboard/smd/index.html | **Family verified; exact MPN/2 W mapping needs datasheet check** |
| R_SENSE_B | WSL2512R5600FEA | Vishay Dale | 2512, 2 W, 1% low-inductance metal-strip | https://www.vishay.com/en/landingpage/sampleboard/smd/index.html | **Family verified; exact MPN/2 W mapping needs datasheet check** |
| C_VM_HF | GRM21BR71H104KA01L | Murata | 0805, X7R, 0.1 uF, 50 V | https://www.murata.com/ | **MPN/spec source located; lifecycle/package status should be rechecked before release** |
| C_VM_LOCAL | GRM32ER71E226KE15L | Murata | 1210, X7R, 22 uF, 25 V | https://www.murata.com/ | **MPN/spec source located; exact manufacturer page not independently resolved in this run** |
| C_VINT | GRM21BR71C225KA12L | Murata | 0805, X7R, 2.2 uF, 16 V | https://www.murata.com/ | **MPN/spec source located; exact manufacturer page not independently resolved in this run** |
| R_NFAULT | RC0805JR-0710KL | Yageo | 0805, 10 kOhm, 5%, 0.125 W | https://www.yageo.com/ | **MPN/spec source located; exact manufacturer page not independently resolved in this run** |
| J1 | 1935161 | Phoenix Contact | 2-position, 5.08 mm pitch PCB terminal | https://www.phoenixcontact.com/en-gb/products/printed-circuit-board-terminal-pt-15-2-50-h-1935161 | **Verified** |
| J2 | 1935161 | Phoenix Contact | 2-position, 5.08 mm pitch PCB terminal | https://www.phoenixcontact.com/en-gb/products/printed-circuit-board-terminal-pt-15-2-50-h-1935161 | **Verified** |
| J3 | 1935161 | Phoenix Contact | 2-position, 5.08 mm pitch PCB terminal | https://www.phoenixcontact.com/en-gb/products/printed-circuit-board-terminal-pt-15-2-50-h-1935161 | **Verified** |
| J4 | 61300911121 | Würth Elektronik | 1x9, 2.54 mm straight male header | https://www.we-online.com/ | **MPN retained; exact manufacturer page not independently resolved in this run** |
| F1 | 0451003.MRL | Littelfuse | Nano2 451, 3 A, SMD fuse | https://www.littelfuse.com/ | **MPN/spec source located; exact manufacturer page not independently resolved in this run** |
| D_TVS | SMAJ15A | Bourns | SMA / DO-214AC, 15 V TVS | https://www.bourns.com/ | **MPN retained; exact manufacturer page not independently resolved in this run** |
| Q_RPOL | SI2301CDS-T1-GE3 | Vishay Siliconix | SOT-23 P-channel MOSFET | https://www.vishay.com/en/applications/telecommunications/xdsl_modemrouter/peripheral_circuits/wlanmodule/ | **Family/package verified; exact suffix mapping needs datasheet check** |
| C_BULK | EEH-ZA1E221P | Panasonic | SMD hybrid polymer, 220 uF, 25 V, 8 x 10.2 mm | https://na.industrial.panasonic.com/products/capacitors/polymer-capacitors/series/79/model/82 | **Verified** |

## Important discrepancies and release blockers

### Phoenix Contact J1/J2/J3

The repository BOM currently describes MPN 1935161 as 16 A / 300 V. The current Phoenix Contact product page identifies 1935161 as a 2-position, 5 mm-pitch PCB terminal with 17.5 A nominal current and 400 V rated voltage (III/2). The repository should not silently retain the older 16 A / 300 V description; reconcile the BOM wording against the manufacturer documentation before a fabrication release.

### Murata C_VM_HF

The exact GRM21BR71H104KA01L MPN is present in the repository BOM. Current distributor data identifies this exact part as obsolete, while the repository still treats it as a selected component. This is a sourcing/lifecycle review item, not evidence that the electrical design is invalid. Do not substitute a different capacitor without checking dielectric, voltage, package, DC-bias behavior, and the actual KiCad footprint.

### Package/footprint verification boundary

This document does not mark the design CAD-ready or fab-ready. Exact symbol/footprint mapping must still be checked against the native KiCad schematic/PCB, manufacturer package drawings, and the repository's CAD lint/release gates.

Where an exact manufacturer page could not be independently resolved during this contribution, the row is explicitly marked rather than presenting a guessed link or claiming verification.

## Review workflow

Before advancing the board to CAD-ready or fab-ready:

1. Verify every exact MPN against the current manufacturer source.
2. Verify package/case and land pattern against the native KiCad footprint.
3. Reconcile any BOM description that differs from the manufacturer source.
4. Re-run the repository BOM, netlist, KiCad-source, and release-gate checks.
5. Keep fabricated and hardware-validated gates blocked until physical evidence exists.