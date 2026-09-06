#!/usr/bin/env python3
"""Validate the EDA-independent connectivity contract before/after CAD capture."""
from __future__ import annotations
import argparse
from pathlib import Path
import yaml

REQUIRED_NETS = {
    "VM", "GND", "VINT", "VLOGIC", "AIN1", "AIN2", "BIN1", "BIN2", "nSLEEP", "nFAULT",
    "AOUT1", "AOUT2", "BOUT1", "BOUT2", "AISEN", "BISEN"
}
REQUIRED_ENDPOINTS = {
    "U1.VM", "U1.GND", "U1.PPAD", "U1.VINT", "U1.VREF",
    "U1.AIN1", "U1.AIN2", "U1.BIN1", "U1.BIN2", "U1.nSLEEP", "U1.nFAULT",
    "U1.AISEN", "U1.BISEN", "U1.AOUT1", "U1.AOUT2", "U1.BOUT1", "U1.BOUT2",
}


def lint(path: Path) -> list[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["contract root must be a mapping"]

    nets = data.get("nets", {})
    if not isinstance(nets, dict):
        return ["nets must be a mapping"]

    missing = REQUIRED_NETS - set(nets)
    if missing:
        errors.append("missing nets: " + ", ".join(sorted(missing)))

    endpoint_owner: dict[str, str] = {}
    all_endpoints: set[str] = set()
    for net, cfg in nets.items():
        endpoints = cfg.get("endpoints", []) if isinstance(cfg, dict) else []
        if not isinstance(endpoints, list):
            errors.append(f"{net}: endpoints must be a list")
            continue
        if len(endpoints) < 2:
            errors.append(f"{net}: expected >=2 endpoints")
        if len(endpoints) != len(set(endpoints)):
            errors.append(f"{net}: duplicate endpoint inside net")
        for endpoint in endpoints:
            if not isinstance(endpoint, str) or "." not in endpoint:
                errors.append(f"{net}: invalid endpoint {endpoint!r}")
                continue
            previous = endpoint_owner.get(endpoint)
            if previous is not None and previous != net:
                errors.append(f"{endpoint}: assigned to both {previous} and {net}")
            else:
                endpoint_owner[endpoint] = net
            all_endpoints.add(endpoint)

    missing_endpoints = REQUIRED_ENDPOINTS - all_endpoints
    if missing_endpoints:
        errors.append("missing driver endpoints: " + ", ".join(sorted(missing_endpoints)))

    # Reference profile deliberately ties VREF to the VINT rail.
    vint = set(nets.get("VINT", {}).get("endpoints", []))
    required_vint = {"U1.VINT", "U1.VREF", "C_VINT.1", "J4.VREF"}
    if not required_vint.issubset(vint):
        errors.append("VINT: expected U1.VINT, U1.VREF, C_VINT.1 and J4.VREF on one physical net")

    return errors


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("path", nargs="?", type=Path, default=Path("hardware/cad/netlist_spec.yaml"))
    args = p.parse_args()
    errors = lint(args.path)
    if errors:
        for e in errors:
            print(e)
        raise SystemExit(1)
    print("netlist contract passed")


if __name__ == "__main__":
    main()
