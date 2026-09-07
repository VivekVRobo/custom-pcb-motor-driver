# Deterministic Electrical Corner Sweep

Before fabrication, the Rev-A reference design can still be checked against the recorded DRV8848 datasheet limits and tolerance corners.

Run:

```bash
python tools/corner_sweep.py
```

The tool evaluates a deterministic matrix across:

- VINT minimum / typical / maximum;
- sense-resistor minimum / maximum from the configured tolerance;
- 25 °C and 85 °C bridge-resistance models from the recorded reference profile;
- 25 °C and the configured maximum design ambient;
- simultaneous operation of the configured number of bridges.

For each case it computes:

- regulated current;
- total bridge conduction-loss screening estimate;
- rough junction temperature using the recorded JEDEC θJA value;
- sense-resistor dissipation;
- sense-resistor power-rating utilization;
- pass/fail screening checks against the documented reference limits.

Output:

```text
artifacts/corner-sweep.json
```

## Evidence boundary

This is useful **analytical design evidence**, but it is not physical validation.

The sweep does not replace:

- KiCad ERC;
- footprint verification;
- PCB DRC;
- copper-current or field-solver analysis;
- board-specific thermal simulation;
- fabrication inspection;
- bench current/voltage measurements;
- stall or thermal tests.

The generated JSON therefore explicitly carries:

```text
hardware_evidence: false
cad_validation: false
```

Only actual KiCad and hardware evidence may advance those release gates.
