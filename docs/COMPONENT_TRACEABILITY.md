# Component Source and Package Traceability

This table ties the selected Rev A reference BOM entries to the component identity already defined by `hardware/BOM.csv`. It is a documentation/traceability aid; it does **not** change the electrical design or advance any CAD/fabrication/validation gate.

| Ref | Function | Manufacturer | MPN | Package / footprint stated by repository | Authoritative source | Verification status |
| --- | --- | --- | --- | --- | --- | --- |
| U1 | Dual H-bridge motor driver | Texas Instruments | `DRV8848PWPR` | HTSSOP-16 / PWP | [TI DRV8848 product page](https://www.ti.com/product/DRV8848) | Verified against manufacturer product data |
| R_SENSE_A | Current sense | Vishay Dale | `WSL2512R5600FEA` | SMD 2512 | [Vishay Power Metal Strip family](https://www.vishay.com/en/product/30123/) | Family-level source verified; exact MPN/package mapping should be rechecked before release |
| R_SENSE_B | Current sense | Vishay Dale | `WSL2512R5600FEA` | SMD 2512 | [Vishay Power Metal Strip family](https://www.vishay.com/en/product/30123/) | Family-level source verified; exact MPN/package mapping should be rechecked before release |
| C_VM_HF | VM high-frequency bypass | Murata | `GRM21BR71H104KA01L` | SMD 0805 | — | Repository-selected part; exact manufacturer page not independently verified in this run |
| C_VM_LOCAL | VM local bulk ceramic | Murata | `GRM32ER71E226KE15L` | SMD 1210 | — | Repository-selected part; exact manufacturer page not independently verified in this run |
| C_VINT | VINT bypass | Murata | `GRM21BR71C225KA12L` | SMD 0805 | — | Repository-selected part; exact manufacturer page not independently verified in this run |
| R_NFAULT | nFAULT pull-up | Yageo | `RC0805JR-0710KL` | SMD 0805 | — | Repository-selected part; exact manufacturer page not independently verified in this run |
| J1/J2/J3 | 2-position PCB terminal | Phoenix Contact | `1935161` | 5.0 mm pitch, 2-position | [Phoenix Contact 1935161](https://www.phoenixcontact.com/en-us/products/pcb-terminal-block-pt-15-2-50-h-1935161) | Manufacturer product page verified; repository BOM description should be aligned to the manufacturer's current rating data |
| J4 | 1x9 logic header | Wurth Elektronik | `61300911121` | 2.54 mm pitch, 1x9 | — | Repository-selected part; exact manufacturer page not independently verified in this run |
| F1 | Input protection fuse | Littelfuse | `0451003.MRL` | SMD 2410 / Nano2 | — | Repository-selected part; exact manufacturer page not independently verified in this run |
| D_TVS | Input TVS | Bourns | `SMAJ15A` | SMA / DO-214AC | [Bourns TVS selection data](https://www.bourns.com/docs/technical-documents/technical-library/chip-diodes/publications/bourns_esd1710_tvs_diode_short_form_update_jp.pdf) | Manufacturer data verified for SMAJ15A family rating/package |
| Q_RPOL | Reverse-polarity MOSFET | Vishay Siliconix | `SI2301CDS-T1-GE3` | SOT-23 | [Vishay SI2301CDS family data](https://www.vishay.com/en/product/72604/) | Family-level source verified; exact suffix/package mapping should be rechecked before release |
| C_BULK | Input bulk capacitor | Panasonic | `EEH-ZA1E221P` | SMD hybrid aluminum, 8 x 10.2 mm | [Panasonic EEHZA1E221P](https://industrial.panasonic.com/ww/products/pt/hybrid-aluminum/models/EEHZA1E221P) | Manufacturer product page verified |

## Release-review rules

- The repository BOM remains the source of the selected MPNs; this document does not silently substitute parts.
- A **family-level** manufacturer page is not treated as proof of an exact MPN/suffix/package mapping.
- Rows marked as not independently verified must be checked against the manufacturer's current datasheet/product page before a CAD-ready or fab-ready gate is advanced.
- The table does not establish electrical, thermal, lifecycle, availability, or manufacturing suitability beyond the specific manufacturer data explicitly linked above.
- Any future part substitution must update the BOM and this traceability table together.

## Scope

This document satisfies the documentation portion of the component-traceability task while keeping the repository's existing evidence boundaries intact. It does not claim that the board is CAD-ready, fab-ready, fabricated, or hardware-validated.
