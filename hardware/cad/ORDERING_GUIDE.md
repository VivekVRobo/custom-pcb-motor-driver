# Fab House Ordering Guide — JLCPCB & PCBWay

**Board:** TI DRV8848 Dual Motor Driver (Rev-A)  
**Gerber Package:** [`hardware/cad/gerbers_drv8848_revA.zip`](file:///c:/Users/vivek/Desktop/portfolio%20website/repos/custom-pcb-motor-driver/hardware/cad/gerbers_drv8848_revA.zip)  

---

## 1. Fast Ordering on JLCPCB

1. **Navigate to:** `https://cart.jlcpcb.com/quote`
2. **Upload Gerber:** Select `hardware/cad/gerbers_drv8848_revA.zip`.
3. **Detected Dimensions:** $48.0\text{ mm} \times 36.0\text{ mm}$.
4. **Configure Parameters:**
   - **Base Material:** FR-4
   - **Layers:** 2
   - **PCB Quantity:** 5 or 10 pcs
   - **Different Design:** 1
   - **Delivery Format:** Single PCB
   - **PCB Thickness:** 1.6 mm
   - **PCB Color:** Matte Black (or Green)
   - **Silkscreen:** White
   - **Surface Finish:** **LeadFree HASL** (or ENIG for enhanced coplanarity)
   - **Outer Copper Weight:** **2 oz** (Select 2 oz for dual 1.0A motor thermal stability)
   - **Via Covering:** Tented
   - **Flying Probe Test:** Fully Tested
   - **Gold Fingers:** No
   - **Castellated Holes:** No
5. **Review Gerber in Online Viewer:**
   - Verify outline on Edge.Cuts ($48\text{mm} \times 36\text{mm}$).
   - Verify 4 corner mounting holes (3.2mm M3).
   - Verify 9 thermal vias under IC U1 pad.
6. **Checkout & Order.**

---

## 2. Fast Ordering on PCBWay

1. **Navigate to:** `https://www.pcbway.com/orderonline.aspx`
2. **PCB Specification:**
   - **Size:** $48\text{ mm} \times 36\text{ mm}$
   - **Quantity:** 5 or 10 pcs
   - **Layers:** 2 layers
   - **Material:** FR-4 (Tg 140–150°C)
   - **Thickness:** 1.6 mm
   - **Min Track/Spacing:** 8/8 mil
   - **Min Hole Size:** 0.3 mm
   - **Solder Mask:** Matte Black
   - **Silkscreen:** White
   - **Surface Finish:** Lead-Free HASL / Immersion Gold (ENIG)
   - **Finished Copper:** 2 oz
3. **Upload Gerber Archive:** Upload `gerbers_drv8848_revA.zip`.

---

## 3. Component Procurement (DigiKey / Mouser / LCSC Quick-Cart)

All components are standard, active lifecycle items in stock across major distributors:

| Designator | MPN | Package | DigiKey Part Number |
| :--- | :--- | :--- | :--- |
| **U1** | `DRV8848PWPR` | HTSSOP-16 PowerPAD | 296-36862-1-ND |
| **R_SENSE_A, B** | `WSL2512R5600FEA` | SMD 2512 (0.56Ω 2W 1%) | WSL-.56-1.0%-ND |
| **C_VM_LOCAL** | `GRM32ER71E226KE15L` | SMD 1210 (22µF 25V X7R) | 490-6523-1-ND |
| **C_VM_HF** | `GRM21BR71H104KA01L` | SMD 0805 (0.1µF 50V X7R) | 490-1636-1-ND |
| **C_VINT** | `GRM21BR71C225KA12L` | SMD 0805 (2.2µF 16V X7R) | 490-5321-1-ND |
| **R_NFAULT** | `RC0805JR-0710KL` | SMD 0805 (10kΩ 0.125W) | 311-10KARCT-ND |
| **J1, J2, J3** | `1935161` | 5.08mm 2P Screw Terminal | 277-1667-ND |
| **J4** | `61300911121` | 2.54mm 1x9 Male Pin Header | 732-5328-ND |
| **F1** | `0451003.MRL` | SMD 2410 (3A Fast Nano2) | F2318TR-ND |
| **D_TVS** | `SMAJ15A` | SMA / DO-214AC (15V 400W) | SMAJ15ALFCT-ND |
| **Q_RPOL** | `SI2301CDS-T1-GE3` | SOT-23 (-20V -3.1A P-FET) | SI2301CDS-T1-GE3CT-ND |
| **C_BULK** | `EEH-ZA1E221P` | SMD 8x10.2mm (220µF 25V) | PCE5024CT-ND |
