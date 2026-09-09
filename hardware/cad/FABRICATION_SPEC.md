# Fabrication Specification — TI DRV8848 Motor Driver Rev-A

**Document ID:** `FAB-SPEC-DRV8848-REVA`  
**Board Name:** `custom_pcb_motor_driver`  
**Revision:** Rev-A design study  
**Status:** **TARGET REQUIREMENTS ONLY — NOT RELEASED FOR FABRICATION**

> This document records intended manufacturing constraints for a future validated Rev-A board. It is **not** a description of a fabrication-ready PCB. The committed KiCad PCB is still an unrouted/unvalidated capture scaffold, and the repository intentionally keeps CAD/fabrication gates false.

---

## 1. Current source-of-truth status

The current `custom_pcb_motor_driver.kicad_pcb` implements only an initial **45 mm × 35 mm** rectangular outline plus named nets and draft silkscreen. It does **not** yet implement or prove the complete placement, routing, mounting holes, PowerPAD thermal-via array, copper pours, clearances or production stack-up described as targets below.

An earlier planning revision used a **48 mm × 36 mm** target. That value must not be treated as the current board dimension or entered into a fabrication order. Final mechanical dimensions must be measured from the validated KiCad release immediately before manufacturing outputs are generated.

---

## 2. Target manufacturing constraints

These are design requirements to verify during final CAD review; they are not completed-layout evidence.

| Parameter | Target / design intent | Release requirement |
| :--- | :--- | :--- |
| **Layer count** | 2 layers | Confirm from final PCB and CAM output |
| **Board thickness** | 1.6 mm FR-4 | Confirm with selected fabricator stack-up |
| **Material** | FR-4, Tg appropriate for assembly/use | Confirm exact laminate option before order |
| **Outer copper** | 2 oz target | Re-validate against final current/thermal geometry and fab capability |
| **Surface finish** | Lead-free HASL or ENIG | Choose for final assembly requirements |
| **Trace / clearance** | 8/8 mil planning floor | Must be enforced and passed by final DRC/fab rules |
| **Minimum drill** | 0.30 mm planning floor | Verify final drill table and fab capability |
| **Mounting holes** | Four M3-clear holes were an earlier target | Must exist in final PCB source and be dimensionally reviewed |
| **Board dimensions** | **Not frozen** | Measure from final `Edge.Cuts`; current scaffold is 45 × 35 mm |

No target in this table may be promoted into a fabrication claim until it is present in the source and independently verified.

---

## 3. Power and thermal layout requirements

The future routed design should be reviewed against the following engineering intent:

1. **DRV8848 PowerPAD**
   - implement exposed-pad copper according to the manufacturer package/layout guidance;
   - add an appropriate thermal-via array only after pad geometry, drill rules and assembly process are reviewed;
   - verify solder-mask/paste treatment in KiCad and CAM outputs.
2. **Motor-current paths**
   - size VM and motor-output copper from the actual current envelope, copper weight, temperature-rise target and final geometry;
   - do not use an unverified width or temperature-rise number as a performance claim.
3. **Current-sense routing**
   - preserve low-impedance, noise-conscious current-sense returns and verify their relationship to the driver ground/current path in the final placement and routing.
4. **Grounding and protection**
   - review the final ground plane/pours, return paths, fuse/reverse-polarity/TVS implementation and connector placement before release.

---

## 4. Assembly targets

Potential assembly choices such as stencil thickness, exposed-pad aperture reduction, component package compatibility and solder process remain **targets to verify**, not released specifications. The final release package must derive them from the completed footprints, paste layers and assembly-house requirements.

---

## 5. Fabrication release checklist

A document may be called a fabrication specification only after the exact release commit demonstrates:

- [ ] schematic complete and reviewed;
- [ ] footprints verified against manufacturer drawings;
- [ ] ERC passed or waivers reviewed;
- [ ] placement and routing complete;
- [ ] PowerPAD / thermal implementation complete;
- [ ] board outline and mounting geometry frozen;
- [ ] DRC passed or waivers reviewed;
- [ ] Gerbers/drills regenerated from that exact validated source;
- [ ] CAM review completed;
- [ ] BOM and assembly outputs reviewed;
- [ ] checksums recorded;
- [ ] manufacturing archive tied to an immutable Git tag/release.

Until then, use this file only as an engineering design target. See [`ORDERING_GUIDE.md`](ORDERING_GUIDE.md) for the explicit no-order gate and [`../../docs/MANUFACTURING_RELEASE.md`](../../docs/MANUFACTURING_RELEASE.md) for the required release package.
