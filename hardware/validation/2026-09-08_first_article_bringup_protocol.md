# Hardware Validation Protocol — Rev A First-Article Bring-Up

**Document ID:** `VAL-PROTO-DRV8848-001`  
**Date:** September 8, 2026  
**Board Revision:** `Rev-A` (`custom_pcb_motor_driver`)  
**Target Device:** TI DRV8848PWP (HTSSOP-16 Dual H-Bridge Motor Driver)  
**Order Reference:** `hardware/cad/gerbers_drv8848_revA.zip`  
**Applicable Runbook:** [`PCB_PHYSICAL_VALIDATION_RUNBOOK.md`](file:///c:/Users/vivek/Desktop/All%20in%20one%20place/TECHNICAL_ACTIVATIONS/PCB_PHYSICAL_VALIDATION_RUNBOOK.md)  

---

## 1. Test Equipment & Instrumentation Required

| Instrument | Model / Specification | Purpose |
| :--- | :--- | :--- |
| **Bench Power Supply** | 0–30V, 0–5A adjustable with current limiting | Staged, current-limited power delivery |
| **Digital Multimeter (DMM 1)** | 4.5 digit (True RMS) | Voltage test point measurements ($V_{INT}$, $V_{CP}$, $V_{M}$) |
| **Digital Multimeter (DMM 2)** | mA / $\mu\text{A}$ precision range | Quiescent current measurement |
| **Digital Storage Oscilloscope** | 2-channel $\ge 100\text{ MHz}$, 1 GSa/s | PWM switching edge timing & dead-time verification |
| **Thermocouple / IR Thermometer** | Type-K probe or Fluke IR sensor | DRV8848 package case temperature logging |
| **Test Loads** | 24Ω 10W & 12Ω 25W ceramic power resistors; N20 / TT DC gear motor | Progressive load verification |

---

## 2. Stage 1: Bare-Board Unpopulated Inspection (Continuity Check)

*Before soldering any components onto the fabricated PCBs:*

| Test Node Pair | Expected Reading | Observed Result | Status |
| :--- | :--- | :--- | :---: |
| **VM to GND** | OPEN ($\infty\,\Omega$) | | [ ] |
| **VINT to GND** | OPEN ($\infty\,\Omega$) | | [ ] |
| **AOUT1 to AOUT2** | OPEN ($\infty\,\Omega$) | | [ ] |
| **BOUT1 to BOUT2** | OPEN ($\infty\,\Omega$) | | [ ] |
| **AISEN / BISEN to GND** | Continuous to ground plane via sense pads | | [ ] |
| **Mounting Holes to GND** | Isolated (Non-plated) | | [ ] |

---

## 3. Stage 2: SMT Assembly & Solder Inspection

*Inspect board under 10x–20x stereo microscope or inspection camera:*

- [ ] **DRV8848PWPR PowerPAD:** Solder reflowed completely into bottom thermal vias without solder balls or voids.
- [ ] **0.65mm Pitch Leads:** Zero solder bridges across pins 1–16.
- [ ] **Decoupling Capacitors:** 0.1µF ($C_{\text{VM\_HF}}$) and 22µF ($C_{\text{VM\_LOCAL}}$) seated flat within 2.0mm of driver pins.
- [ ] **Sense Resistors:** Vishay WSL2512 $0.56\,\Omega$ resistors flat against pads with clean solder fillets on both terminals.

---

## 4. Stage 3: Progressive Low-Voltage Quiescent Bring-Up

### Step 3.1: Sleep State Verification ($nSLEEP = \text{LOW}$)
1. Set bench power supply to **$V_{IN} = 6.0\text{ V}$, Current Limit = $50\text{ mA}$**.
2. Connect power supply leads to terminal $J1$ ($V_M$ and GND).
3. Keep $nSLEEP$ pin tied to GND ($0\text{ V}$).
4. Turn on bench supply.
5. **Criterion:** Quiescent current draw must be **$< 5.0\,\mu\text{A}$** (Datasheet spec: typ $1.5\,\mu\text{A}$, max $5\,\mu\text{A}$).

### Step 3.2: Active Idle State Verification ($nSLEEP = \text{HIGH}$)
1. Pull $nSLEEP$ HIGH (connect to 3.3V or 5V logic rail).
2. Measure supply current: Must read **$1.5\text{ mA} – 3.0\text{ mA}$**.
3. Measure $V_{INT}$ test point ($TP_{\text{VINT}}$):
   - **Target:** **$3.30\text{ V} \pm 5\%$** ($3.13\text{ V} – 3.47\text{ V}$).
4. Measure Charge Pump test point ($TP_{\text{VCP}}$):
   - **Target:** **$V_M + 5\text{ V} \approx 11.0\text{ V}$** (confirms internal charge pump oscillator is operating).

---

## 5. Stage 4: Dynamic PWM Switching & Gate Drive Verification

1. Connect function generator or MCU GPIO to `AIN1`, `AIN2`, `BIN1`, `BIN2`.
2. Connect oscilloscope Channel 1 to `AOUT1` and Channel 2 to `AOUT2`.
3. Set PWM frequency to **$20.0\text{ kHz}$**, 50% duty cycle on `AIN1`, `AIN2 = LOW`:
   - Verify clean square wave output toggling from $0\text{ V}$ to $V_M$.
   - Measure 10%–90% rise time: Target **$< 100\text{ ns}$**.
   - Measure 90%–10% fall time: Target **$< 100\text{ ns}$**.
   - Verify internal dead-time insertion: Zero shoot-through spikes on supply rail.

---

## 6. Stage 5: Progressive Load & Thermal Validation Matrix

| Test Tier | Operating Conditions | Load Type | Expected Current | Thermal Limit ($T_{\text{case}}$) | Gate Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Tier 1** | $V_M = 12.0\text{V}$, limit $500\text{mA}$ | No-load TT DC motor | $60\text{mA} – 120\text{mA}$ | Ambient $+ 5^\circ\text{C}$ | [ ] PASS |
| **Tier 2** | $V_M = 12.0\text{V}$, limit $1.0\text{A}$ | $24\,\Omega$ 10W power resistor | $0.50\text{ A}$ continuous | $< 45^\circ\text{C}$ after 5 min | [ ] PASS |
| **Tier 3** | $V_M = 12.0\text{V}$, limit $1.5\text{A}$ | $12\,\Omega$ 25W power resistor | $0.89\text{ A} – 0.95\text{ A}$ (chopping) | $< 65^\circ\text{C}$ after 10 min | [ ] PASS |
| **Tier 4** | $V_M = 12.0\text{V}$, overload trip | Low impedance ($< 4\,\Omega$) | Current limit trip / $nFAULT$ LOW | Output clamps safely | [ ] PASS |

---

## 7. Sign-Off & Release Approval

- **Fabrication Package:** `hardware/cad/gerbers_drv8848_revA.zip` (SHA-256 verified)
- **BOM Order Status:** 100% Selected with active manufacturer part numbers
- **Next Milestone:** Submit Gerber package to JLCPCB/PCBWay for 5-piece prototype run.
