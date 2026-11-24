import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parents[1] / "tools"))
from netlist_lint import lint


ROOT = Path(__file__).parents[1]


def test_connectivity_contract():
    assert lint(ROOT / "hardware/cad/netlist_spec.yaml") == []


def test_rejects_endpoint_for_undeclared_component(tmp_path):
    contract = {
        "components": {"U1": "DRV8848PWPR"},
        "nets": {
            "VM": {"endpoints": ["U1.VM", "J99.VM"]},
        },
    }
    path = tmp_path / "netlist.yaml"
    path.write_text(yaml.safe_dump(contract), encoding="utf-8")

    errors = lint(path)

    assert "VM: endpoint 'J99.VM' references undeclared component 'J99'" in errors


def test_rejects_empty_component_or_pin_name(tmp_path):
    contract = {
        "components": {"U1": "DRV8848PWPR"},
        "nets": {
            "VM": {"endpoints": ["U1.VM", ".VM", "U1."]},
        },
    }
    path = tmp_path / "netlist.yaml"
    path.write_text(yaml.safe_dump(contract), encoding="utf-8")

    errors = lint(path)

    assert "VM: invalid endpoint '.VM'" in errors
    assert "VM: invalid endpoint 'U1.'" in errors
