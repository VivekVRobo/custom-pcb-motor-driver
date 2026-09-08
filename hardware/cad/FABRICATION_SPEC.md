# Fabrication Specification — TI DRV8848 Motor Driver Rev-A

**Document ID:** `FAB-SPEC-DRV8848-REVA`  
**Board Name:** `custom_pcb_motor_driver`  
**Revision:** `Rev-A`  
**Target Fabricators:** JLCPCB, PCBWay, OSH Park  
**Classification:** IPC-A-600 Class 2  

---

## 1. Board Mechanical & Physical Parameters

| Parameter | Specification | Tolerance / Notes |
| :--- | :--- | :--- |
| **Dimensions** | 48.0 mm × 36.0 mm | ±0.15 mm (routed outline) |
| **Layer Count** | 2 Layers | Top (F.Cu) and Bottom (B.Cu) |
| **Board Thickness** | 1.6 mm | Standard FR-4 core |
| **Material Base** | FR-4 Standard | Glass transition temp $T_g \ge 140^\circ\text{C}$ |
| **Dielectric Constant ($\epsilon_r$)** | 4.5 @ 1 MHz | Standard FR-4 |
| **Outer Finished Copper** | **2.0 oz (70 µm)** | **Mandatory:** Sized for thermal dissipation & dual 1.0A continuous motor current |
| **Surface Finish** | **Lead-Free HASL** (or ENIG) | RoHS compliant; flat pad coplanarity for 0.65mm HTSSOP |
| **Solder Mask Color** | Matte Black (or Dark Green) | High-contrast against white silkscreen |
| **Silkscreen Color** | White | Epoxied, legibility $\ge 0.8\text{mm}$ text height |
| **Minimum Trace / Clearance** | 8 mil / 8 mil (0.203 mm / 0.203 mm) | Standard fab house capability |
| **Minimum Drill Size** | 0.3 mm (12 mil) | Thermal vias under IC |
| **Mounting Holes** | 4× 3.2 mm (M3 clear) | Non-plated, 6.0 mm clearance diameter at corners |

---

## 2. Layer Stackup & Impedance

```text
┌─────────────────────────────────────────────────────────────┐
│ Top Silkscreen (White Epoxy)                                │
├─────────────────────────────────────────────────────────────┤
│ Top Solder Mask (Matte Black LPI, 15-20 µm)                 │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: Top Copper (F.Cu) — 2.0 oz (70 µm finished)        │
│   - High-current motor buses: VM, AOUT1, AOUT2, BOUT1, BOUT2│
│   - PowerPAD top thermal spreading pour                     │
├─────────────────────────────────────────────────────────────┤
│ FR-4 Dielectric Core — 1.45 mm thickness                    │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: Bottom Copper (B.Cu) — 2.0 oz (70 µm finished)     │
│   - Solid continuous Ground Plane pour (GND)                │
│   - Thermal via heat dissipation sink                       │
├─────────────────────────────────────────────────────────────┤
│ Bottom Solder Mask (Matte Black LPI, 15-20 µm)              │
├─────────────────────────────────────────────────────────────┤
│ Bottom Silkscreen (White Epoxy)                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. High-Current & Thermal Layout Rules

1. **DRV8848 PowerPAD Thermal Vias:**
   - 9× thermal vias (3 × 3 matrix) positioned directly within the exposed center pad area ($3.4\text{ mm} \times 2.0\text{ mm}$).
   - Drill diameter: $0.30\text{ mm}$ finished hole.
   - Annular ring: $0.15\text{ mm}$ minimum ($0.60\text{ mm}$ pad diameter).
   - Bottom solder mask: Solder mask aperture kept open on bottom copper to allow auxiliary heatsink attachment or reflow coupling.
2. **Current Trace Ampacity:**
   - VM power rail, AOUT1/2, BOUT1/2 traces routed with $\ge 1.50\text{ mm}$ (60 mil) track width.
   - Temperature rise calculation under 2 oz copper: $\Delta T < 8^\circ\text{C}$ at $1.5\text{A}$ continuous load.
3. **Current Sense Kelvin Return:**
   - $R_{\text{SENSE\_A}}$ and $R_{\text{SENSE\_B}}$ (Vishay WSL2512 $0.56\,\Omega$) returned directly into local ground plane via multiple stitching vias adjacent to driver GND pin 13.

---

## 4. Stencil & Assembly Specification

- **Stencil Thickness:** $100\,\mu\text{m}$ ($0.10\text{ mm}$) stainless steel, laser-cut, electropolished.
- **PowerPAD Aperture:** 4-pane windowpane aperture pattern (80% area reduction) to prevent solder paste excess and thermal pad float.
- **Component Packaging:** SMT components 0805, 1210, 2512, HTSSOP-16, SOT-23, and SMA diodes.
