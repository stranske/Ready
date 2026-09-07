# PAEM audit scope
Unit: D-audit-Portable-Alpha-Extension-Model--2026-09-07T04-47-31Z
Started: 2026-09-07T05:13:54.121796+00:00
Base: main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc
Scope from dossier and owner notes: first-party pa_core, dashboard, web, packaging scripts, tests and repo-owned CI. Synced Workflows infrastructure is upstream-owned. Research and staged issue bodies only; no issue filing or code changes. Eight dimensions planned with explicit coverage limits. Native work Python available; WASM unknown. Synthetic inputs only.
Orientation: pa_core 165 files/24768 lines; dashboard 21/6343; tests 198/32527; scripts 60/26044. Hotspots cli.py 2106, config.py 1280, sleeve_suggestor.py 1160. Remote current-head CI 34015303572 success. Untracked dossier-out/ pre-exists. System Python numeric ABI errors; isolated uv runtime being installed. Load 24.28,30.37,32.90; no stale ownership established, no unrelated processes killed.
