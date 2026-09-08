"""Unit tests for first-principles mathematical physics engine."""
import pytest
from tools.math_physics_engine import MathematicalPhysicsEngine


def test_current_regulation_physics():
    engine = MathematicalPhysicsEngine()
    reg = engine.compute_current_regulation()

    assert 0.890 < reg.i_chop_nom_a < 0.895
    assert reg.i_chop_min_a > 0.80
    assert reg.i_chop_max_a < 1.0
    assert reg.ocp_headroom_percent > 50.0
    assert reg.rms_headroom_percent > 4.0
    assert reg.sense_derating_utilization_percent < 30.0


def test_power_loss_and_switching_physics():
    engine = MathematicalPhysicsEngine()
    loss = engine.compute_power_losses(active_bridges=2)

    assert 1.40 < loss.p_cond_25c_w < 1.50
    assert 1.70 < loss.p_cond_85c_w < 1.75
    # Switching loss must be much smaller than conduction loss
    assert loss.p_sw_w < 0.05
    assert loss.p_total_nom_85c_w < 1.90
    assert loss.p_total_worst_corner_w < 2.10


def test_thermal_physics_safety():
    engine = MathematicalPhysicsEngine()
    loss = engine.compute_power_losses(active_bridges=2)
    therm = engine.compute_thermal_physics(loss.p_total_nom_85c_w)

    assert therm.r_th_via_array_c_per_w < 25.0
    assert therm.theta_ja_effective_c_per_w < therm.theta_ja_jedec_c_per_w
    assert therm.t_j_lab_effective_c < 100.0
    assert therm.t_j_industrial_worst_corner_c < therm.t_tsd_c
    assert therm.thermal_margin_industrial_c > 30.0


def test_capacitive_filter_physics():
    engine = MathematicalPhysicsEngine()
    cap = engine.compute_capacitive_filtering()

    assert cap.voltage_droop_percent < 1.0
    assert cap.bulk_ripple_utilization_percent < 35.0


def test_ipc2152_trace_ampacity():
    engine = MathematicalPhysicsEngine()
    trace = engine.compute_conductor_traces()

    # Temperature rise on 2 oz 60 mil trace at 1A should be well under 1 deg C
    assert trace.delta_t_ipc2152_c < 0.50
    assert trace.delta_t_fault_ipc2152_c < 5.0
    assert trace.trace_dc_resistance_mohm < 10.0
    assert trace.trace_voltage_drop_mv < 10.0


def test_full_dossier_summary_verifications():
    engine = MathematicalPhysicsEngine()
    dossier = engine.generate_full_dossier()
    summary = dossier["safety_margins_summary"]

    assert summary["i_chop_within_continuous_1a_rating"] is True
    assert summary["sense_resistor_derating_safe"] is True
    assert summary["junction_temp_industrial_safe"] is True
    assert summary["bus_voltage_droop_safe"] is True
    assert summary["trace_temperature_rise_safe"] is True
