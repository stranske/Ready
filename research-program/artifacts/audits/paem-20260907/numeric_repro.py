"""Executable, read-only numerical audit probes for PAEM main 59cb12b.

Run exactly as:
PYTHONPATH=/Users/teacher/.codex/automations/research-program/clones/Portable-Alpha-Extension-Model \
  /tmp/paem-audit-20260907-venv/bin/python numeric_repro.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from pa_core.agents.registry import build_from_config
from pa_core.config import ModelConfig, SweepConfig, SweepParameter
from pa_core.facade import RunOptions, run_single, run_sweep
from pa_core.fees import FeeSchedule
from pa_core.simulations import simulate_agents
from pa_core.sleeve_suggestor import _StreamCache, _evaluate_allocation


INDEX = pd.Series([0.0] * 12, dtype=float)


def cfg(**changes: object) -> ModelConfig:
    data: dict[str, object] = {
        "N_SIMULATIONS": 128,
        "N_MONTHS": 12,
        "return_unit": "monthly",
        "financing_mode": "per_path",
        "total_fund_capital": 1000.0,
        "external_pa_capital": 200.0,
        "active_ext_capital": 200.0,
        "internal_pa_capital": 100.0,
        "w_beta_H": 1.0,
        "w_alpha_H": 0.0,
        "reference_sigma": 0.0,
        "theta_extpa": 0.5,
        "active_share": 0.5,
        "mu_H": 0.0,
        "sigma_H": 0.0,
        "mu_E": 0.10,
        "sigma_E": 0.0,
        "mu_M": 0.10,
        "sigma_M": 0.0,
        "internal_pa_financing_mean_month": 0.0,
        "internal_pa_financing_sigma_month": 0.0,
        "ext_pa_financing_mean_month": 0.0,
        "ext_pa_financing_sigma_month": 0.0,
        "act_ext_financing_mean_month": 0.0,
        "act_ext_financing_sigma_month": 0.0,
    }
    data.update(changes)
    return ModelConfig.model_validate(data)


def row(df: pd.DataFrame, agent: str, metric: str) -> float:
    return float(df.loc[df["Agent"] == agent, metric].iloc[0])


def revalidated(base: ModelConfig, **changes: object) -> ModelConfig:
    dumped = base.model_dump()
    dumped.update(changes)
    return ModelConfig.model_validate(dumped)


def probe_sweep_convenience_drift() -> None:
    base = cfg(
        analysis_mode="alpha_shares",
        external_pa_alpha_min_pct=0.0,
        external_pa_alpha_max_pct=100.0,
        external_pa_alpha_step_pct=100.0,
        active_share_min_pct=0.0,
        active_share_max_pct=0.0,
        active_share_step_pct=100.0,
    )
    swept = run_sweep(base, INDEX, options=RunOptions(seed=7)).summary
    sweep_ext = swept[swept["Agent"] == "ExternalPA"].sort_values("theta_extpa")
    actual_delta = float(sweep_ext["terminal_AnnReturn"].iloc[-1] - sweep_ext["terminal_AnnReturn"].iloc[0])

    control_zero = run_single(revalidated(base, theta_extpa=0.0), INDEX, RunOptions(seed=7))
    control_one = run_single(revalidated(base, theta_extpa=1.0), INDEX, RunOptions(seed=7))
    expected_delta = row(control_one.summary, "ExternalPA", "terminal_AnnReturn") - row(
        control_zero.summary, "ExternalPA", "terminal_AnnReturn"
    )
    print("SWEEP_CONVENIENCE_DRIFT", f"actual_delta={actual_delta:.12f}", f"control_delta={expected_delta:.12f}")


def probe_sweep_fee_omission() -> None:
    sweep = SweepConfig(method="grid", parameters={"theta_extpa": SweepParameter(values=[0.5])})
    gross_cfg = cfg(sweep=sweep)
    net_cfg = revalidated(
        gross_cfg,
        fee_schedule={"InternalPA": FeeSchedule(mgmt_fee_bps=120.0)},
    )
    gross_sweep = run_sweep(gross_cfg, INDEX, options=RunOptions(seed=9)).summary
    net_sweep = run_sweep(net_cfg, INDEX, options=RunOptions(seed=9)).summary
    gross_single = run_single(gross_cfg, INDEX, RunOptions(seed=9)).summary
    net_single = run_single(net_cfg, INDEX, RunOptions(seed=9)).summary
    print(
        "SWEEP_FEE_OMISSION",
        f"sweep_drag={row(gross_sweep, 'InternalPA', 'terminal_AnnReturn') - row(net_sweep, 'InternalPA', 'terminal_AnnReturn'):.12f}",
        f"single_drag={row(gross_single, 'InternalPA', 'terminal_AnnReturn') - row(net_single, 'InternalPA', 'terminal_AnnReturn'):.12f}",
    )


def probe_internal_pa_cost_scaling() -> None:
    small = cfg(internal_pa_capital=100.0, external_pa_capital=0.0, active_ext_capital=0.0,
                internal_pa_financing_mean_month=0.01)
    full = revalidated(small, internal_pa_capital=1000.0)
    small_out = run_single(small, INDEX, RunOptions(seed=4)).raw_returns["InternalPA"].to_numpy()
    full_out = run_single(full, INDEX, RunOptions(seed=4)).raw_returns["InternalPA"].to_numpy()
    print(
        "INTERNAL_PA_COST_SCALING",
        f"small_sleeve_return={float(small_out.mean()):.12f}",
        f"full_sleeve_return={float(full_out.mean()):.12f}",
        "expected_small=-0.001000000000",
    )


def probe_internal_pa_common_random_numbers() -> None:
    sweep = SweepConfig(method="grid", parameters={"theta_extpa": SweepParameter(values=[0.2, 0.8])})
    static = cfg(sweep=sweep, internal_pa_financing_sigma_month=0.0)
    stochastic = cfg(sweep=sweep, internal_pa_financing_sigma_month=0.01)
    static_rows = run_sweep(static, INDEX, options=RunOptions(seed=21)).summary
    stochastic_rows = run_sweep(stochastic, INDEX, options=RunOptions(seed=21)).summary
    static_int = static_rows[static_rows["Agent"] == "InternalPA"].sort_values("theta_extpa")
    stochastic_int = stochastic_rows[stochastic_rows["Agent"] == "InternalPA"].sort_values("theta_extpa")
    static_delta = float(static_int["terminal_AnnReturn"].iloc[1] - static_int["terminal_AnnReturn"].iloc[0])
    stochastic_delta = float(stochastic_int["terminal_AnnReturn"].iloc[1] - stochastic_int["terminal_AnnReturn"].iloc[0])
    print("INTERNAL_PA_CRN", f"sigma0_delta={static_delta:.12f}", f"sigma1pct_delta={stochastic_delta:.12f}")


def probe_suggestor_convenience_drift() -> None:
    base = cfg()
    cache = _StreamCache(base, INDEX, seed=31)
    low = _evaluate_allocation(
        base, INDEX, ext_cap=0.0, act_cap=0.0, int_cap=1000.0,
        max_te=10.0, max_breach=1.0, max_cvar=1.0, max_shortfall=1.0,
        constraint_scope="total", seed=31, stream_cache=cache, include_returns=True,
    )
    high = _evaluate_allocation(
        base, INDEX, ext_cap=1000.0, act_cap=0.0, int_cap=0.0,
        max_te=10.0, max_breach=1.0, max_cvar=1.0, max_shortfall=1.0,
        constraint_scope="total", seed=31, stream_cache=cache, include_returns=True,
    )
    assert low is not None and high is not None
    low_return = low[0]["Total_terminal_AnnReturn"]
    high_return = high[0]["Total_terminal_AnnReturn"]

    # Matched control: revalidation recompiles agent shares before simulation.
    low_cfg = revalidated(base, external_pa_capital=0.0, active_ext_capital=0.0, internal_pa_capital=1000.0)
    high_cfg = revalidated(base, external_pa_capital=1000.0, active_ext_capital=0.0, internal_pa_capital=0.0)
    low_control = row(run_single(low_cfg, INDEX, RunOptions(seed=31)).summary, "Total", "terminal_AnnReturn")
    high_control = row(run_single(high_cfg, INDEX, RunOptions(seed=31)).summary, "Total", "terminal_AnnReturn")
    print(
        "SUGGESTOR_CONVENIENCE_DRIFT",
        f"actual_delta={high_return - low_return:.12f}",
        f"control_delta={high_control - low_control:.12f}",
    )


if __name__ == "__main__":
    probe_sweep_convenience_drift()
    probe_sweep_fee_omission()
    probe_internal_pa_cost_scaling()
    probe_internal_pa_common_random_numbers()
    probe_suggestor_convenience_drift()
