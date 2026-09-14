## Why

Current break: setting the documented UI credentials raises TypeError before any login form. `ui/__init__.py:40` uses the removed Hasher constructor; the credential mapping and login call at `ui/__init__.py:42` and `ui/__init__.py:52` also use older interfaces. `requirements.lock:583` pins authenticator 0.4.2. Existing fake objects in `tests/test_ui_auth.py:28` reproduce the obsolete interface and cannot detect the mismatch. The documented private deployment relies on this gate.

## Scope

Configured username/password login and authenticated-session logout in the existing UI.

## Non-Goals

Do not introduce OIDC, remove the login gate, or change credential ownership. Scaffold-only completion does NOT count: swapping one Hasher call while the configured login and session/logout path still fails is a failure of this issue.

## Tasks

- [ ] Replace the old hashing, credential mapping, and login and session handling in `ui/__init__.py` with the installed authenticator API while preserving local no-credentials mode.
- [ ] Keep authentication state and logout control consistent on every rerun in `ui/__init__.py` so a cached auth flag cannot hide the logout action.
- [ ] Add actual-dependency AppTest coverage to `tests/test_ui_auth.py` for initial form render, valid and invalid credentials, authenticated rerun, and logout.

## Acceptance Criteria

- [ ] pytest tests/test_ui_auth.py tests/test_ui_auth_dev_mode.py must pass; the new configured-login test must render a form with no exception using authenticator 0.4.2 and Streamlit 1.60.0. Valid login grants access, invalid login does not, and logout clears access on the next rerun.
- [ ] Deliberate-break gate: Restore the old Hasher constructor in `ui/__init__.py`; the new configured-login test in `tests/test_ui_auth.py` must fail before form rendering; revert the break and rerun.

## Implementation Notes

Verified at 4523cf50dac3f3fe2ba338b8243e630940c54fd0. Actual dependency reproduction and browser both raised Hasher.__init__ TypeError. No real credentials used. Existing local blank-credential behavior remains intentional. Upstream API reference: https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/README.md
