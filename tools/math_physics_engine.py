#!/usr/bin/env python3
"""First-Principles Mathematical Physics & Analytical Validation Engine for DRV8848 PCB.

This module computes complete electrical, thermal, switching, capacitive,
and conductor physics from foundational equations (Ohm's law, Fourier heat conduction,
IPC-2152, MOSFET charge dynamics, and LC impedance networks).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass(frozen=True)
class CurrentRegulationResult:
    vint_nom_v: float
    vint_min_v: float
    vint_max_v: float
    r_sense_nom_ohm: float
    r_sense_min_ohm: float
    r_sense_max_ohm: float
    gain: float
    i_chop_nom_a: float
    i_chop_min_a: float
    i_chop_max_a: float
    ocp_typ_a: float
    ocp_min_a: float
    ocp_headroom_percent: float
    rms_headroom_percent: float
    p_sense_nom_w: float
    p_sense_max_w: float
    r_sense_power_rating_w: float
    sense_derating_utilization_percent: float


@dataclass(frozen=True)
class PowerLossResult:
    v_m_v: float
    i_motor_a: float
    active_bridges: int
    r_ds_hs_25c_ohm: float
    r_ds_ls_25c_ohm: float
    r_path_25c_ohm: float
    r_path_85c_ohm: float
    r_path_125c_ohm: float
    p_cond_25c_w: float
    p_cond_85c_w: float
    p_cond_max_corner_w: float
    f_pwm_hz: float
    t_rise_s: float
    t_fall_s: float
    p_sw_w: float
    t_dead_s: float
    v_diode_f_v: float
    p_dead_w: float
    p_quiescent_w: float
    p_total_nom_85c_w: float
    p_total_worst_corner_w: float


@dataclass(frozen=True)
class ThermalPhysicsResult:
    theta_jc_bot_c_per_w: float
    theta_ja_jedec_c_per_w: float
    via_count: int
    via_drill_m: float
    via_plating_thickness_m: float
    board_thickness_m: float
    k_copper_w_per_mk: float
    r_th_single_via_c_per_w: float
    r_th_via_array_c_per_w: float
    board_length_m: float
    board_width_m: float
    copper_area_effective_m2: float
    h_heat_transfer_w_per_m2k: float
    r_th_board_to_amb_c_per_w: float
    theta_ja_effective_c_per_w: float
    t_amb_lab_c: float
    t_j_lab_nominal_c: float
    t_j_lab_effective_c: float
    t_amb_enclosed_c: float
    t_j_enclosed_effective_c: float
    t_amb_industrial_c: float
    t_j_industrial_worst_corner_c: float
    t_tsd_c: float
    thermal_margin_lab_c: float
    thermal_margin_industrial_c: float


@dataclass(frozen=True)
class CapacitiveFilterResult:
    c_local_f: float
    c_bulk_f: float
    delta_i_step_a: float
    delta_t_step_s: float
    esr_local_ohm: float
    voltage_droop_v: float
    voltage_droop_percent: float
    f_pwm_hz: float
    duty_cycle: float
    i_rms_bulk_a: float
    i_bulk_rating_a: float
    bulk_ripple_utilization_percent: float


@dataclass(frozen=True)
class ConductorTraceResult:
    trace_width_mil: float
    copper_weight_oz: float
    copper_thickness_um: float
    copper_thickness_mil: float
    cross_section_mil2: float
    current_a: float
    delta_t_ipc2152_c: float
    fault_current_a: float
    delta_t_fault_ipc2152_c: float
    trace_length_mm: float
    trace_dc_resistance_mohm: float
    trace_voltage_drop_mv: float
    trace_power_loss_mw: float


@dataclass(frozen=True)
class ProtectionPhysicsResult:
    motor_inductance_h: float
    peak_current_a: float
    stored_inductive_energy_mj: float
    tvs_standoff_v: float
    tvs_breakdown_min_v: float
    tvs_clamping_max_v: float
    drv8848_abs_max_v: float
    pfet_rds_on_mohm: float
    pfet_conduction_loss_mw: float


class MathematicalPhysicsEngine:
    """Rigorous analytical calculator implementing exact circuit and physics formulas."""

    def __init__(
        self,
        v_m_nom: float = 12.0,
        v_m_max: float = 12.6,
        r_sense_nom: float = 0.560,
        r_sense_tol_pct: float = 1.0,
        r_sense_rating_w: float = 2.0,
        vint_nom: float = 3.30,
        vint_min: float = 3.13,
        vint_max: float = 3.47,
        gain: float = 6.6,
        f_pwm: float = 20000.0,
        motor_inductance_h: float = 0.0025,
    ):
        self.v_m_nom = v_m_nom
        self.v_m_max = v_m_max
        self.r_sense_nom = r_sense_nom
        self.r_sense_tol_pct = r_sense_tol_pct
        self.r_sense_rating_w = r_sense_rating_w
        self.vint_nom = vint_nom
        self.vint_min = vint_min
        self.vint_max = vint_max
        self.gain = gain
        self.f_pwm = f_pwm
        self.motor_inductance_h = motor_inductance_h

    def compute_current_regulation(self) -> CurrentRegulationResult:
        r_tol = self.r_sense_tol_pct / 100.0
        r_min = self.r_sense_nom * (1.0 - r_tol)
        r_max = self.r_sense_nom * (1.0 + r_tol)

        # I_CHOP = V_INT / (GAIN * R_ISEN)
        i_nom = self.vint_nom / (self.gain * self.r_sense_nom)
        i_min = self.vint_min / (self.gain * r_max)
        i_max = self.vint_max / (self.gain * r_min)

        ocp_typ = 3.0
        ocp_min = 2.0
        ocp_headroom = ((ocp_min - i_max) / ocp_min) * 100.0
        rms_headroom = ((1.0 - i_max) / 1.0) * 100.0

        p_sense_nom = (i_nom**2) * self.r_sense_nom
        p_sense_max = (i_max**2) * r_max
        utilization = (p_sense_max / self.r_sense_rating_w) * 100.0

        return CurrentRegulationResult(
            vint_nom_v=round(self.vint_nom, 4),
            vint_min_v=round(self.vint_min, 4),
            vint_max_v=round(self.vint_max, 4),
            r_sense_nom_ohm=round(self.r_sense_nom, 4),
            r_sense_min_ohm=round(r_min, 4),
            r_sense_max_ohm=round(r_max, 4),
            gain=self.gain,
            i_chop_nom_a=round(i_nom, 6),
            i_chop_min_a=round(i_min, 6),
            i_chop_max_a=round(i_max, 6),
            ocp_typ_a=ocp_typ,
            ocp_min_a=ocp_min,
            ocp_headroom_percent=round(ocp_headroom, 2),
            rms_headroom_percent=round(rms_headroom, 2),
            p_sense_nom_w=round(p_sense_nom, 4),
            p_sense_max_w=round(p_sense_max, 4),
            r_sense_power_rating_w=self.r_sense_rating_w,
            sense_derating_utilization_percent=round(utilization, 2),
        )

    def compute_power_losses(
        self, active_bridges: int = 2, i_load: float | None = None
    ) -> PowerLossResult:
        i_active = i_load if i_load is not None else (self.vint_nom / (self.gain * self.r_sense_nom))
        r_tol = self.r_sense_tol_pct / 100.0
        r_min = self.r_sense_nom * (1.0 - r_tol)
        i_worst_corner = self.vint_max / (self.gain * r_min)

        r_hs_25 = 0.45
        r_ls_25 = 0.45
        r_path_25 = r_hs_25 + r_ls_25
        r_path_85 = 1.08  # Datasheet recorded typical at 85 C
        r_path_125 = r_path_25 * (1.0 + 0.004 * (125 - 25))  # alpha = +0.4%/C

        p_cond_25 = active_bridges * (i_active**2) * r_path_25
        p_cond_85 = active_bridges * (i_active**2) * r_path_85
        p_cond_max = active_bridges * (i_worst_corner**2) * r_path_85

        t_rise = 50e-9
        t_fall = 50e-9
        # P_sw = N * 0.5 * V_M * I_load * (t_rise + t_fall) * f_pwm
        p_sw = active_bridges * 0.5 * self.v_m_nom * i_active * (t_rise + t_fall) * self.f_pwm

        # Dead time conduction loss (body diode) during dead time t_dead
        t_dead = 400e-9
        v_diode_f = 0.8
        p_dead = active_bridges * 2 * v_diode_f * i_active * t_dead * self.f_pwm

        # Quiescent operating power
        i_q_active = 2.5e-3
        p_quiescent = self.v_m_nom * i_q_active

        p_total_nom = p_cond_85 + p_sw + p_dead + p_quiescent
        p_total_worst = p_cond_max + p_sw + p_dead + p_quiescent

        return PowerLossResult(
            v_m_v=self.v_m_nom,
            i_motor_a=round(i_active, 4),
            active_bridges=active_bridges,
            r_ds_hs_25c_ohm=r_hs_25,
            r_ds_ls_25c_ohm=r_ls_25,
            r_path_25c_ohm=round(r_path_25, 4),
            r_path_85c_ohm=round(r_path_85, 4),
            r_path_125c_ohm=round(r_path_125, 4),
            p_cond_25c_w=round(p_cond_25, 4),
            p_cond_85c_w=round(p_cond_85, 4),
            p_cond_max_corner_w=round(p_cond_max, 4),
            f_pwm_hz=self.f_pwm,
            t_rise_s=t_rise,
            t_fall_s=t_fall,
            p_sw_w=round(p_sw, 5),
            t_dead_s=t_dead,
            v_diode_f_v=v_diode_f,
            p_dead_w=round(p_dead, 5),
            p_quiescent_w=round(p_quiescent, 4),
            p_total_nom_85c_w=round(p_total_nom, 4),
            p_total_worst_corner_w=round(p_total_worst, 4),
        )

    def compute_thermal_physics(self, p_loss_w: float) -> ThermalPhysicsResult:
        theta_jc_bot = 2.1
        theta_ja_jedec = 40.2

        via_count = 9
        via_drill_m = 0.30e-3
        via_plating_m = 25e-6
        board_h_m = 1.6e-3
        k_cu = 386.0  # W/(m*K)

        # Via barrel cross section: A = pi * d * t
        a_via = math.pi * via_drill_m * via_plating_m
        r_via_single = board_h_m / (k_cu * a_via)
        r_via_array = r_via_single / via_count

        # Board convection from 2 oz copper plane (48 mm x 36 mm)
        l_m = 0.048
        w_m = 0.036
        board_area_m2 = l_m * w_m
        effective_surface_m2 = 2 * board_area_m2  # Top and bottom faces
        h_eff = 15.0  # W/(m^2 * K) natural convection + radiation
        r_board_amb = 1.0 / (h_eff * effective_surface_m2)

        # Total board effective Theta_JA
        theta_ja_eff = theta_jc_bot + r_via_array + (r_board_amb * 0.70)

        t_amb_lab = 25.0
        t_j_lab_jedec = t_amb_lab + (p_loss_w * theta_ja_jedec)
        t_j_lab_eff = t_amb_lab + (p_loss_w * theta_ja_eff)

        t_amb_enc = 40.0
        t_j_enc_eff = t_amb_enc + (p_loss_w * theta_ja_eff)

        t_amb_ind = 50.0
        p_worst_case = 1.98
        t_j_ind_worst = t_amb_ind + (p_worst_case * theta_ja_eff)

        t_tsd = 160.0
        margin_lab = t_tsd - t_j_lab_eff
        margin_ind = t_tsd - t_j_ind_worst

        return ThermalPhysicsResult(
            theta_jc_bot_c_per_w=theta_jc_bot,
            theta_ja_jedec_c_per_w=theta_ja_jedec,
            via_count=via_count,
            via_drill_m=via_drill_m,
            via_plating_thickness_m=via_plating_m,
            board_thickness_m=board_h_m,
            k_copper_w_per_mk=k_cu,
            r_th_single_via_c_per_w=round(r_via_single, 2),
            r_th_via_array_c_per_w=round(r_via_array, 2),
            board_length_m=l_m,
            board_width_m=w_m,
            copper_area_effective_m2=round(effective_surface_m2, 6),
            h_heat_transfer_w_per_m2k=h_eff,
            r_th_board_to_amb_c_per_w=round(r_board_amb, 2),
            theta_ja_effective_c_per_w=round(theta_ja_eff, 2),
            t_amb_lab_c=t_amb_lab,
            t_j_lab_nominal_c=round(t_j_lab_jedec, 2),
            t_j_lab_effective_c=round(t_j_lab_eff, 2),
            t_amb_enclosed_c=t_amb_enc,
            t_j_enclosed_effective_c=round(t_j_enc_eff, 2),
            t_amb_industrial_c=t_amb_ind,
            t_j_industrial_worst_corner_c=round(t_j_ind_worst, 2),
            t_tsd_c=t_tsd,
            thermal_margin_lab_c=round(margin_lab, 2),
            thermal_margin_industrial_c=round(margin_ind, 2),
        )

    def compute_capacitive_filtering(self) -> CapacitiveFilterResult:
        c_local = 22e-6
        c_bulk = 220e-6
        delta_i = 1.0
        delta_t = 2.0e-6
        esr_local = 0.008

        # Delta V = (Delta I * Delta t) / C + Delta I * ESR
        v_droop = ((delta_i * delta_t) / c_local) + (delta_i * esr_local)
        v_droop_pct = (v_droop / self.v_m_nom) * 100.0

        d = 0.50
        i_rms_bulk = delta_i * math.sqrt(d * (1.0 - d))
        i_bulk_rating = 1.80
        utilization = (i_rms_bulk / i_bulk_rating) * 100.0

        return CapacitiveFilterResult(
            c_local_f=c_local,
            c_bulk_f=c_bulk,
            delta_i_step_a=delta_i,
            delta_t_step_s=delta_t,
            esr_local_ohm=esr_local,
            voltage_droop_v=round(v_droop, 5),
            voltage_droop_percent=round(v_droop_pct, 3),
            f_pwm_hz=self.f_pwm,
            duty_cycle=d,
            i_rms_bulk_a=round(i_rms_bulk, 3),
            i_bulk_rating_a=i_bulk_rating,
            bulk_ripple_utilization_percent=round(utilization, 2),
        )

    def compute_conductor_traces(self) -> ConductorTraceResult:
        w_mil = 60.0
        oz = 2.0
        t_um = 70.0
        t_mil = t_um / 25.4  # ~2.756 mil
        area_mil2 = w_mil * t_mil

        # IPC-2152 External Conductor equation:
        # I = k * (Delta_T)^b * A^c
        # k = 0.048, b = 0.44, c = 0.725
        # Delta_T = ( I / (k * A^c) )^(1/b)
        k = 0.048
        b = 0.44
        c = 0.725

        i_nom = 1.0
        delta_t = (i_nom / (k * (area_mil2**c))) ** (1.0 / b)

        i_fault = 3.0  # Fuse rating
        delta_t_fault = (i_fault / (k * (area_mil2**c))) ** (1.0 / b)

        length_mm = 25.0
        length_m = length_mm * 1e-3
        area_m2 = (w_mil * 25.4e-6) * (t_um * 1e-6)
        rho_copper = 1.72e-8  # ohm * m
        r_dc = rho_copper * length_m / area_m2
        v_drop_mv = i_nom * r_dc * 1000.0
        p_loss_mw = (i_nom**2) * r_dc * 1000.0

        return ConductorTraceResult(
            trace_width_mil=w_mil,
            copper_weight_oz=oz,
            copper_thickness_um=t_um,
            copper_thickness_mil=round(t_mil, 3),
            cross_section_mil2=round(area_mil2, 2),
            current_a=i_nom,
            delta_t_ipc2152_c=round(delta_t, 3),
            fault_current_a=i_fault,
            delta_t_fault_ipc2152_c=round(delta_t_fault, 3),
            trace_length_mm=length_mm,
            trace_dc_resistance_mohm=round(r_dc * 1000.0, 3),
            trace_voltage_drop_mv=round(v_drop_mv, 3),
            trace_power_loss_mw=round(p_loss_mw, 3),
        )

    def compute_protection_physics(self) -> ProtectionPhysicsResult:
        i_peak = 1.0
        e_ind = 0.5 * self.motor_inductance_h * (i_peak**2) * 1000.0  # mJ

        tvs_standoff = 15.0
        tvs_breakdown_min = 16.7
        tvs_clamping_max = 24.4
        abs_max = 20.0

        pfet_rds_on = 0.070  # ohm
        pfet_loss_mw = (i_peak**2) * pfet_rds_on * 1000.0

        return ProtectionPhysicsResult(
            motor_inductance_h=self.motor_inductance_h,
            peak_current_a=i_peak,
            stored_inductive_energy_mj=round(e_ind, 3),
            tvs_standoff_v=tvs_standoff,
            tvs_breakdown_min_v=tvs_breakdown_min,
            tvs_clamping_max_v=tvs_clamping_max,
            drv8848_abs_max_v=abs_max,
            pfet_rds_on_mohm=round(pfet_rds_on * 1000.0, 1),
            pfet_conduction_loss_mw=round(pfet_loss_mw, 2),
        )

    def generate_full_dossier(self) -> Dict[str, Any]:
        reg = self.compute_current_regulation()
        loss = self.compute_power_losses(active_bridges=2)
        therm = self.compute_thermal_physics(loss.p_total_nom_85c_w)
        cap = self.compute_capacitive_filtering()
        trace = self.compute_conductor_traces()
        prot = self.compute_protection_physics()

        return {
            "metadata": {
                "engine": "MathematicalPhysicsEngine",
                "target_device": "TI DRV8848PWPR",
                "revision": "Rev-A",
                "date": "2026-09-08",
                "status": "ANALYTICAL_MATHEMATICAL_VERIFICATION_COMPLETE",
            },
            "current_regulation": asdict(reg),
            "power_losses": asdict(loss),
            "thermal_physics": asdict(therm),
            "capacitive_filtering": asdict(cap),
            "conductor_traces": asdict(trace),
            "protection_physics": asdict(prot),
            "safety_margins_summary": {
                "i_chop_within_continuous_1a_rating": reg.i_chop_max_a < 1.0,
                "i_chop_margin_to_ocp_trip_percent": reg.ocp_headroom_percent,
                "sense_resistor_derating_safe": reg.sense_derating_utilization_percent < 50.0,
                "junction_temp_industrial_safe": therm.t_j_industrial_worst_corner_c < therm.t_tsd_c,
                "thermal_shutdown_headroom_c": therm.thermal_margin_industrial_c,
                "bus_voltage_droop_safe": cap.voltage_droop_percent < 2.0,
                "trace_temperature_rise_safe": trace.delta_t_ipc2152_c < 1.0,
            },
        }


if __name__ == "__main__":
    import json
    engine = MathematicalPhysicsEngine()
    dossier = engine.generate_full_dossier()
    print(json.dumps(dossier, indent=2))
