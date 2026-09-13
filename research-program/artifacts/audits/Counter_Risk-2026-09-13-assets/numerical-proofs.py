"""Standalone regression proofs for the Counter_Risk numerical audit.

Run from the target clone:
PYTHONPATH="$PWD/src" .venv/bin/python \
  [LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/numerical-proofs.py
"""

from __future__ import annotations

from datetime import date

from counter_risk.compute.limits import check_limits, find_missing_limit_entities
from counter_risk.compute.rollups import compute_concentration_metrics
from counter_risk.normalize import resolve_counterparty
from counter_risk.parsers.exposure_maturity_schedule import _parse_block_rows


def _records(table: object) -> list[dict[str, object]]:
    if hasattr(table, "to_dict"):
        return table.to_dict(orient="records")  # type: ignore[union-attr,no-any-return]
    return [dict(row) for row in table]  # type: ignore[union-attr]


class _Cell:
    def __init__(self, value: object) -> None:
        self.value = value


class _Worksheet:
    max_row = 4

    def __init__(self) -> None:
        self._values = {
            (1, 1): date(2026, 1, 1),
            (1, 2): "not-a-number",
            (2, 1): "Total",
        }

    def cell(self, *, row: int, column: int) -> _Cell:
        return _Cell(self._values.get((row, column)))


def proof_duplicate_counterparty_concentration() -> None:
    rows = [
        {"variant": "all", "segment": "total", "counterparty": "Alpha", "notional": 60.0},
        {"variant": "all", "segment": "total", "counterparty": "Alpha", "notional": 60.0},
        *[
            {"variant": "all", "segment": "total", "counterparty": f"Beta-{n}", "notional": 10.0}
            for n in range(10)
        ],
    ]
    actual = _records(compute_concentration_metrics(rows))[0]
    expected_hhi = (120.0 / 220.0) ** 2 + 10 * (10.0 / 220.0) ** 2
    print("duplicate-counterparty concentration")
    print(" actual:", actual)
    print(" expected after counterparty aggregation:", {"top5_share": 1.0, "hhi": expected_hhi})
    assert actual["top5_share"] != 1.0
    assert actual["hhi"] != expected_hhi


def proof_limit_registry_bypass() -> None:
    exposures = [{"counterparty": "Bank of America, NA", "notional": 200.0}]
    config = {
        "schema_version": 1,
        "limits": [
            {
                "entity_type": "counterparty",
                "entity_name": "bank_of_america",
                "limit_kind": "absolute_notional",
                "limit_value": 100.0,
            }
        ],
    }
    resolution = resolve_counterparty("Bank of America, NA")
    missing = find_missing_limit_entities(exposures, config)
    breaches = _records(check_limits(exposures, config))
    print("limit-registry bypass")
    print(" registry canonical key:", resolution.canonical_key)
    print(" missing entities:", missing)
    print(" breaches:", breaches)
    assert resolution.canonical_key == "bank_of_america"
    assert missing == [{"entity_type": "counterparty", "entity_name": "bank_of_america"}]
    assert breaches == []


def proof_invalid_maturity_total_becomes_zero() -> None:
    rows = _parse_block_rows(worksheet=_Worksheet(), date_col=1, total_col=2, start_row=1)
    print("invalid-maturity-total")
    print(" parsed rows:", rows)
    assert len(rows) == 1
    assert rows[0].total == 0.0


if __name__ == "__main__":
    proof_duplicate_counterparty_concentration()
    proof_limit_registry_bypass()
    proof_invalid_maturity_total_becomes_zero()
    print("all current-code proofs reproduced")
