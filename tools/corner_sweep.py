#!/usr/bin/env python3
"""Sweep deterministic DRV8848 design corners using recorded datasheet values.

This is analytical screening evidence only. It does not replace KiCad ERC/DRC,
board-specific thermal analysis, fabrication, or bench measurements.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from design_model import (
    conduction_loss_w,
    hbridge_path_resistance,
    regulated_current_a,
    resistor_dissipation_w,
    sense_resistor_derating_ratio,
    thermal_estimate,
)


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def sweep(design: dict, profile: dict) -> dict:
    app = design["application"]
    cs = design["current_sense"]
    regulation = profile["current_regulation"]
    resistance = profile["resistance"]
    thermal = profile["thermal"]
    motor = profile["motor"]

    r_nom = float(cs["resistor_ohm"])
    r_tol = float(cs["tolerance_percent"]) / 100.0
    r_values = {
        "min": r_nom * (1.0 - r_tol),
        "max": r_nom * (1.0 + r_tol),
    }
    vint_values = {
        "min": float(regulation["vint_min_v"]),
        "typ": float(regulation["vint_typ_v"]),
        "max": float(regulation["vint_max_v"]),
    }
    path_values = {
        "25c": hbridge_path_resistance(
            float(resistance["high_side_typ_25c_ohm"]),
            float(resistance["low_side_typ_25c_ohm"]),
        ),
        "85c": hbridge_path_resistance(
            float(resistance["high_side_typ_85c_ohm"]),
            float(resistance["low_side_typ_85c_ohm"]),
        ),
    }
    ambient_values = [25.0, float(app["ambient_design_max_c"])]
    gain = float(regulation["sense_gain"])
    active = int(app["simultaneous_channels"])
    resistor_rating = float(cs["resistor_power_rating_w"])
    rms_rating = float(motor["rms_current_per_bridge_a"])
    junction_limit = float(thermal["junction_max_operating_c"])
    theta_ja = float(thermal["theta_ja_c_per_w"])

    cases: list[dict] = []
    for ambient_c in ambient_values:
        for path_label, path_ohm in path_values.items():
            for vint_label, vint_v in vint_values.items():
                for resistor_label, resistor_ohm in r_values.items():
                    current_a = regulated_current_a(vint_v, resistor_ohm, gain)
                    conduction_w = conduction_loss_w(current_a, path_ohm, active)
                    thermal_case = thermal_estimate(conduction_w, ambient_c, theta_ja)
                    sense_power_w = resistor_dissipation_w(current_a, resistor_ohm)
                    utilization = sense_resistor_derating_ratio(sense_power_w, resistor_rating)
                    checks = {
                        "current_within_1a_rms_reference": current_a <= rms_rating,
                        "rough_junction_below_operating_limit": thermal_case.junction_c < junction_limit,
                        "sense_resistor_at_or_below_50pct_rating": utilization <= 0.50,
                    }
                    cases.append(
                        {
                            "corner": {
                                "ambient_c": ambient_c,
                                "bridge_resistance_model": path_label,
                                "vint_corner": vint_label,
                                "sense_resistor_corner": resistor_label,
                            },
                            "inputs": {
                                "vint_v": vint_v,
                                "sense_resistor_ohm": resistor_ohm,
                                "hbridge_path_resistance_ohm": path_ohm,
                                "active_bridges": active,
                            },
                            "metrics": {
                                "regulated_current_a": current_a,
                                "total_bridge_conduction_loss_w": conduction_w,
                                "rough_junction_c": thermal_case.junction_c,
                                "sense_resistor_power_w_each": sense_power_w,
                                "sense_resistor_rating_utilization": utilization,
                            },
                            "checks": checks,
                            "passed": all(checks.values()),
                        }
                    )

    def max_case(metric: str) -> dict:
        return max(cases, key=lambda item: float(item["metrics"][metric]))

    worst_current = max_case("regulated_current_a")
    worst_junction = max_case("rough_junction_c")
    worst_sense = max_case("sense_resistor_rating_utilization")

    return {
        "schema_version": 1,
        "evidence_type": "datasheet_deterministic_corner_sweep",
        "hardware_evidence": False,
        "cad_validation": False,
        "design_revision": design["design_revision"],
        "reference_profile": profile["profile"],
        "datasheet_revision": profile["source"]["datasheet_revision"],
        "case_count": len(cases),
        "all_screening_checks_pass": all(case["passed"] for case in cases),
        "extrema": {
            "max_regulated_current": worst_current,
            "max_rough_junction": worst_junction,
            "max_sense_resistor_utilization": worst_sense,
        },
        "cases": cases,
        "claim_boundary": (
            "Uses recorded DRV8848 datasheet/reference-profile values and deterministic tolerance corners. "
            "Theta-JA is a JEDEC screening metric, not board-specific thermal proof."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, default=Path("hardware/design_values.yaml"))
    parser.add_argument(
        "--profile", type=Path, default=Path("hardware/reference_profiles/drv8848.yaml")
    )
    parser.add_argument("--output", type=Path, default=Path("artifacts/corner-sweep.json"))
    args = parser.parse_args()

    report = sweep(load_yaml(args.design), load_yaml(args.profile))
    text = json.dumps(report, indent=2, sort_keys=True)
    print(text)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text + "\n", encoding="utf-8")
    return 0 if report["all_screening_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
