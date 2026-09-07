"""Synthetic coverage calibration; writes no repository files."""
import json
from statistics import NormalDist
import numpy as np
from pa_core.sim.metrics import cvar_confidence_interval
rng=np.random.default_rng(20260907)
n=2000
reps=1000
normal=NormalDist()
p=0.05
z=normal.inv_cdf(p)
truth=-np.exp(-z*z/2)/np.sqrt(2*np.pi)/p
hits=0
control=0
width=[]
for _ in range(reps):
    sample=rng.normal(0,1,n)
    lo,hi=cvar_confidence_interval(sample)
    hits+=lo<=truth<=hi
    width.append(hi-lo)
    se=np.std(sample,ddof=1)/np.sqrt(n)
    control+=abs(np.mean(sample))<=normal.inv_cdf(.975)*se
print(json.dumps({'repetitions':reps,'draws_each':n,'seed':20260907,'normal_true_lower_5pct_CVaR':float(truth),'nominal_coverage':.95,'observed_CVaR_coverage':hits/reps,'mean_interval_control_coverage':control/reps,'mean_width':float(np.mean(width))},indent=2))
