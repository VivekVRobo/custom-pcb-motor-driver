import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "tools"))

from corner_sweep import load_yaml, sweep

ROOT = Path(__file__).parents[1]


def test_reference_corner_sweep_passes_and_covers_expected_matrix():
    design = load_yaml(ROOT / "hardware/design_values.yaml")
    profile = load_yaml(ROOT / "hardware/reference_profiles/drv8848.yaml")
    report = sweep(design, profile)
    assert report["case_count"] == 24
    assert report["all_screening_checks_pass"] is True
    assert report["hardware_evidence"] is False
    assert report["cad_validation"] is False


def test_worst_current_corner_matches_vint_max_and_resistor_min():
    design = load_yaml(ROOT / "hardware/design_values.yaml")
    profile = load_yaml(ROOT / "hardware/reference_profiles/drv8848.yaml")
    report = sweep(design, profile)
    worst = report["extrema"]["max_regulated_current"]
    assert worst["corner"]["vint_corner"] == "max"
    assert worst["corner"]["sense_resistor_corner"] == "min"
    assert 0.94 < worst["metrics"]["regulated_current_a"] < 0.96


def test_worst_screening_corner_stays_below_limits():
    design = load_yaml(ROOT / "hardware/design_values.yaml")
    profile = load_yaml(ROOT / "hardware/reference_profiles/drv8848.yaml")
    report = sweep(design, profile)
    junction = report["extrema"]["max_rough_junction"]["metrics"]["rough_junction_c"]
    utilization = report["extrema"]["max_sense_resistor_utilization"]["metrics"][
        "sense_resistor_rating_utilization"
    ]
    assert junction < 150.0
    assert utilization < 0.50
