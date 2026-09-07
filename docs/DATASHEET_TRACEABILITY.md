# DRV8848 Datasheet Traceability

This document records the authoritative source assumptions used by the Rev-A analytical screening. It is **not hardware evidence** and must not be used to claim fabricated-board performance.

## Authoritative source

- Manufacturer: Texas Instruments
- Device: `DRV8848PWPR`
- Product page: <https://www.ti.com/product/DRV8848>
- Datasheet: <https://www.ti.com/lit/gpn/DRV8848>
- Datasheet revision recorded by the repository: `SLLSEL7B`, April 2024
- Source rechecked: 2026-09-07

The repository reference profile mirrors the design-relevant values used by the calculation tools. If TI publishes a newer datasheet, re-check the profile before fabrication.

## Current-regulation equation

The DRV8848 full-scale chopping current is modeled from the datasheet relationship:

```text
I_FS = V_REF / (6.6 × R_ISENSE)
```

For the Rev-A nominal values:

```text
V_REF = 3.30 V
R_ISENSE = 0.56 ohm
I_FS = 3.30 / (6.6 × 0.56)
     ≈ 0.8929 A
```

Because Rev-A ties VREF to VINT, a useful analytical corner must include the recorded VINT range and the resistor tolerance rather than reporting only the nominal value.

With:

```text
VINT_min = 3.13 V
VINT_max = 3.47 V
R = 0.56 ohm ±1%
```

the screening range is:

```text
I_min = 3.13 / (6.6 × 0.56 × 1.01) ≈ 0.8385 A
I_max = 3.47 / (6.6 × 0.56 × 0.99) ≈ 0.9483 A
```

These are calculated tolerance corners, not measurements.

## Sense-resistor power corner

At the analytical maximum current:

```text
P = I²R
  = 0.9483² × 0.56
  ≈ 0.504 W
```

A 1 W resistor would therefore sit slightly above a 50% screening utilization at this corner. Rev-A now targets a **>=1.5 W, 1%, low-inductance, pulse-capable** sense resistor so this simple screening utilization falls to roughly 34%.

Final selection still requires the selected resistor manufacturer's pulse, ambient-temperature and PCB-land-pattern derating curves.

## H-bridge conduction-loss screen

The reference profile records typical combined high-side + low-side path resistance of:

```text
25 C: 0.55 + 0.35 = 0.90 ohm
85 C: 0.66 + 0.42 = 1.08 ohm
```

For two simultaneously active bridges at the analytical maximum current:

```text
P_85C ≈ 2 × 0.9483² × 1.08 ≈ 1.94 W
```

Using the recorded JEDEC/package `theta_JA = 40.3 C/W` and a 50 C ambient produces a rough screening junction estimate near 128 C.

This calculation is deliberately conservative in some ways and incomplete in others. `theta_JA` is highly board/layout dependent and is **not** a substitute for a PowerPAD layout review, copper/thermal-via design, thermal simulation, or bench thermography.

## Supply and bypass checks

The Rev-A application maximum is 12.6 V, below the recorded 18 V recommended operating maximum and 20 V absolute maximum. The local nominal VM ceramic target is 22 uF plus 0.1 uF high-frequency bypass, exceeding the datasheet's nominal 10 uF minimum plus 0.1 uF recommendation.

Effective MLCC capacitance under DC bias must be verified after a real capacitor MPN/package is selected; nominal capacitance alone is not enough for fabrication release.

## Evidence boundary

The following claims are supported by this document and the repository calculation tools:

- the formulas were applied consistently to recorded datasheet values;
- the current-limit tolerance corner is explicitly modeled;
- the sense-resistor power target includes more margin than the earlier 1 W reference;
- rough loss/thermal screening is traceable to the reference profile.

The following remain unsupported until real CAD/part/hardware evidence exists:

- KiCad ERC/DRC pass;
- footprint/package correctness;
- PowerPAD thermal performance;
- capacitor effective capacitance;
- fabricated-board temperature;
- actual current-regulation accuracy;
- motor transient/EMI behavior;
- stall/fault behavior.
