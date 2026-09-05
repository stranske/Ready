# Trend browser smoke: native crash diagnosis

During the Astra delivery unblock, the Trend browser smoke repeatedly lost its connection after Select All. CPython 3.14.3, Streamlit 1.58.0, Arrow 25.0.0, NumPy 2.5.0 and pandas 3.0.3 reproduced the failure locally. The server exited with SIGSEGV. PYTHONFAULTHANDLER placed the native fault in libarrow `mi_thread_init`, reached through `MimallocAllocator::AllocateAligned` during a pandas-to-Arrow conversion. The app's in-process AppTest completed 20 -> 0 -> 20 with no exceptions, separating selection logic from the native server crash.

Setting ARROW_DEFAULT_MEMORY_POOL=system before launching the smoke process produced a complete 20 -> 0 -> 20 browser run and clean shutdown on Python 3.14.3. GitHub browser run 33938311896 also passed on repair head e38d75790934b5a38e7f320ff10599467461108d.

The smoke process now defaults to the system pool while preserving an explicit caller override. This is a bounded test-runtime workaround; production launchers still use their configured allocator. No claim is made that an upstream Arrow defect is fixed or that all Python/platform combinations were tested. Raw diagnostic logs containing host network addresses were retained only in temporary local files.

Reference: [Arrow allocator environment variable](https://arrow.apache.org/docs/cpp/env_vars.html#arrow-default-memory-pool).
