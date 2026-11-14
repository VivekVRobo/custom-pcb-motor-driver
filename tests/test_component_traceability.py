import csv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BOM_PATH = REPO_ROOT / "hardware" / "BOM.csv"
TRACEABILITY_PATH = REPO_ROOT / "docs" / "COMPONENT_TRACEABILITY.md"


def _bom_by_reference():
    with BOM_PATH.open(newline="", encoding="utf-8") as handle:
        return {row["Reference"]: row for row in csv.DictReader(handle)}


def _traceability_rows():
    rows = []
    for line in TRACEABILITY_PATH.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and cells[0] and cells[0] != "Ref":
            rows.append(cells)
    return rows


def _expand_references(reference):
    if reference == "J1/J2/J3":
        return ["J1", "J2", "J3"]
    return [reference]


def _normalize_markdown_cell(value):
    return value.strip().strip(`).strip()


def test_traceability_references_match_bom():
    bom = _bom_by_reference()
    traceability = _traceability_rows()


    assert traceability, "traceability table must contain at least one component row"


    for row in traceability:
        reference, _, manufacturer, mpn, *_ = row
        for ref in _expand_references(reference):
            assert ref in bom, f"{reference} is missing from hardware/BOM.csv"
            assert bom[ref]["Manufacturer"] == manufacturer, (
                f"{ref}: manufacturer differs between traceability and BOM"
            )
            assert bom[ref]["MPN"] == _normalize_markdown_cell(mpn), (
                f"{ref}: MPN differs between traceability and BOM"
            )
