import json
import dashboard.utils as u
p=u.bundled_asset_timeseries_path()
i=u.bundled_sample_index_path()
print(json.dumps({'module':u.__file__,'asset_sample':str(p),'asset_exists':p.exists(),'index_sample':str(i),'index_exists':i.exists()},indent=2))
assert not p.exists() and i.exists()
