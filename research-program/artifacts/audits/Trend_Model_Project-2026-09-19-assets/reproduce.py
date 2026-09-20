from copy import deepcopy
from pathlib import Path
import json
import math
import yaml
import pandas as pd
from trend_analysis.config import load_config
from trend_analysis.config.model import CostModelSettings, RiskSettings
from trend_analysis.metrics.turnover import linear_turnover_cost
from trend_analysis.risk import _scale_factors

base = yaml.safe_load(Path("config/demo.yml").read_text())
base["data"]["csv_path"] = "demo/demo_returns.csv"
results = {}
for field in ("per_trade_bps", "half_spread_bps"):
    for value in (float("inf"), float("nan")):
        mapping = deepcopy(base)
        mapping["portfolio"]["cost_model"] = {"per_trade_bps": 5, "half_spread_bps": 0}
        mapping["portfolio"]["cost_model"][field] = value
        cfg = load_config(mapping)
        strict = CostModelSettings.model_validate(mapping["portfolio"]["cost_model"])
        assert not math.isfinite(cfg.portfolio["cost_model"][field])
        assert not math.isfinite(getattr(strict, field))
        results[f"cost_{field}_{value}"] = "accepted by strict and mapping loaders"
for value in (float("inf"), float("nan")):
    mapping = deepcopy(base)
    mapping["vol_adjust"]["floor_vol"] = value
    cfg = load_config(mapping)
    strict = RiskSettings.model_validate(mapping["vol_adjust"])
    assert not math.isfinite(cfg.vol_adjust["floor_vol"])
    assert not math.isfinite(strict.floor_vol)
    results[f"floor_{value}"] = "accepted by strict and mapping loaders"
assert math.isinf(linear_turnover_cost(1.0, float("inf")))
assert math.isnan(linear_turnover_cost(1.0, float("nan")))
assert linear_turnover_cost(1.0, 5.0) == 0.0005
vol = pd.Series({"A": .2, "B": .1})
scales = _scale_factors(vol, .1, floor_vol=float("inf"))
assert scales.to_dict() == {"A": 0.0, "B": 0.0}
assert _scale_factors(vol, .1, floor_vol=.01).to_dict() == {"A": .5, "B": 1.0}
results["invalid_floor_scale_factors"] = scales.to_dict()
results["finite_controls"] = "pass"
print(json.dumps(results, indent=2))
