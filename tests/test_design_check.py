import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "tools"))
from design_check import load_yaml, evaluate

ROOT = Path(__file__).parents[1]


def test_reference_design_passes_screening_checks():
    d = load_yaml(ROOT / "hardware/design_values.yaml")
    p = load_yaml(ROOT / "hardware/reference_profiles/drv8848.yaml")
    report = evaluate(d, p)
    assert report["passed"] is True
    assert report["evidence_type"] == "datasheet_based_engineering_screening"
    assert report["hardware_evidence"] is False
    assert 0.89 < report["metrics"]["configured_current_limit_a"] < 0.90
    assert 0.94 < report["metrics"]["worst_case_current_limit_max_a"] < 0.96
    assert report["metrics"]["sense_resistor_power_worst_case_limit_w_each"] > 0.50
    assert report["metrics"]["sense_resistor_worst_case_rating_utilization"] < 0.50
