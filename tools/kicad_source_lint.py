#!/usr/bin/env python3
"""Conservative checks for generated KiCad capture scaffolds.

This is NOT a substitute for KiCad ERC/DRC. It catches malformed/truncated
S-expressions, missing expected board nets, accidental fabrication claims,
documentation/source maturity drift, and use of KiCad's own generator
identifiers by third-party generated files.
"""
from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CAD = ROOT / "hardware" / "cad"
SCH = CAD / "custom_pcb_motor_driver.kicad_sch"
PCB = CAD / "custom_pcb_motor_driver.kicad_pcb"
PRO = CAD / "custom_pcb_motor_driver.kicad_pro"
ORDERING = CAD / "ORDERING_GUIDE.md"
FAB_SPEC = CAD / "FABRICATION_SPEC.md"
DESIGN = ROOT / "hardware" / "design_values.yaml"

EXPECTED_BOARD_NETS = {
    "GND", "VM", "VINT", "VLOGIC", "AIN1", "AIN2", "BIN1", "BIN2",
    "nSLEEP", "nFAULT", "AISEN", "BISEN", "AOUT1", "AOUT2", "BOUT1", "BOUT2",
}
FABRICATION_FIELDS = (
    "schematic_complete",
    "footprint_verified",
    "erc_passed",
    "pcb_layout_complete",
    "drc_passed",
    "gerbers_reviewed",
)


def balanced_sexpr(text: str) -> bool:
    depth = 0
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0 and not in_string


def field_is_true(text: str, field: str) -> bool:
    return bool(re.search(rf"^\s*{re.escape(field)}:\s*true\s*$", text, flags=re.MULTILINE))


def main() -> None:
    errors: list[str] = []
    for path, root_token in ((SCH, "(kicad_sch"), (PCB, "(kicad_pcb")):
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.lstrip().startswith(root_token):
            errors.append(f"{path.name}: wrong KiCad root token")
        if not balanced_sexpr(text):
            errors.append(f"{path.name}: unbalanced S-expression")
        if "(generator eeschema)" in text or "(generator pcbnew)" in text:
            errors.append(f"{path.name}: third-party source must not impersonate KiCad generator")
        if "UNVALIDATED" not in text:
            errors.append(f"{path.name}: generated draft must preserve visible UNVALIDATED status")

    if PRO.exists():
        try:
            json.loads(PRO.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{PRO.name}: invalid JSON: {exc}")
    else:
        errors.append(f"missing {PRO.relative_to(ROOT)}")

    if PCB.exists():
        pcb_text = PCB.read_text(encoding="utf-8")
        found_nets = set(re.findall(r'\(net\s+\d+\s+"([^"]*)"\)', pcb_text))
        missing = EXPECTED_BOARD_NETS - found_nets
        if missing:
            errors.append("PCB scaffold missing nets: " + ", ".join(sorted(missing)))
        if "DO NOT FABRICATE" not in pcb_text:
            errors.append("PCB scaffold must remain visibly blocked from fabrication")

    # Never allow this lightweight linter to be mistaken for actual EDA validation.
    design_text = DESIGN.read_text(encoding="utf-8")
    for field in FABRICATION_FIELDS:
        if field_is_true(design_text, field):
            errors.append(f"{field}=true requires real KiCad/manual evidence, not scaffold lint")

    # While fabrication maturity is intentionally blocked, the human-facing CAD
    # docs must be equally explicit. This prevents a future documentation edit
    # from telling readers to order placeholder Gerbers while source/gates still
    # say the board is unrouted or unvalidated.
    fabrication_blocked = not all(field_is_true(design_text, field) for field in FABRICATION_FIELDS)
    if fabrication_blocked:
        if not ORDERING.exists():
            errors.append("missing hardware/cad/ORDERING_GUIDE.md")
        else:
            ordering_text = ORDERING.read_text(encoding="utf-8")
            required_ordering_markers = (
                "DO NOT ORDER / DO NOT FABRICATE",
                "not approved fabrication outputs",
                "45 mm × 35 mm",
            )
            for marker in required_ordering_markers:
                if marker not in ordering_text:
                    errors.append(f"ORDERING_GUIDE.md must preserve blocked-fabrication marker: {marker}")
            for forbidden in ("Checkout & Order.", "Upload Gerber: Select"):
                if forbidden in ordering_text:
                    errors.append(f"ORDERING_GUIDE.md contains premature ordering instruction: {forbidden}")

        if not FAB_SPEC.exists():
            errors.append("missing hardware/cad/FABRICATION_SPEC.md")
        else:
            fab_text = FAB_SPEC.read_text(encoding="utf-8")
            for marker in ("NOT RELEASED FOR FABRICATION", "45 mm × 35 mm"):
                if marker not in fab_text:
                    errors.append(f"FABRICATION_SPEC.md must preserve draft/source-truth marker: {marker}")

    if errors:
        print("KiCad scaffold checks failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("KiCad capture scaffold checks passed (not ERC/DRC validation)")


if __name__ == "__main__":
    main()
