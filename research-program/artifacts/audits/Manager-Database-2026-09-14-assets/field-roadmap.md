# Field comparison, opportunities, and tooling

Research checked 2026-09-14; proposals are distinct from verified implementation defects.

## Public-field benchmark

- SEC Form 13F distinguishes restatements from amendments adding holdings. Portfolio history should preserve that distinction; a generic latest-filing rule alone is not a sufficient domain contract. Verify adapter/filing provenance before any additional implementation proposal. Source: https://www.sec.gov/pdf/form13f.pdf
- Streamlit-Authenticator documents nested per-user credential mappings and current login/session APIs. This audit independently reproduced the pinned 0.4.2 mismatch; changing only one Hasher call would leave the other old interfaces unverified. Source: https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/README.md
- Native Streamlit OIDC is a possible enterprise integration, but authentication does not supply application authorization. It is a later hosting option, not required to fix the existing password gate. Source: https://docs.streamlit.io/develop/concepts/connections/authentication
- AWS documents the v2 installer for supported Linux distributions. The failed Ubuntu job should install and verify a supported CLI explicitly, then execute the dry-run contract without production credentials. Source: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
- pgvector already offers exact and approximate search. This repo already uses pgvector-compatible queries; adding a new vector database is not an evidenced gap. Measure recall on manager-filtered questions before changing search infrastructure. Source: https://github.com/pgvector/pgvector
- OCRmyPDF can add searchable text layers and sidecars to scanned PDFs. This is a candidate local preprocessor, not a recommendation to expose work documents to a hosted provider. Source: https://ocrmypdf.readthedocs.io/en/latest/cookbook.html

## Near-term proposals

1. A parameterized manager-key fixture matrix (id and manager_id) across dashboard, daily report, and RAG consumers. Matched synthetic fixtures here expose defects masked by the existing manager_id-only demo. Reuse adapters.base.resolve_manager_id_column; no new ORM needed. Evidence: dialect-results.json.
2. Exercise configured-login with the actual locked authentication dependency in CI, in addition to fake-auth tests. This catches third-party API incompatibility without an identity-provider account. Evidence: auth-repro.json and rendered auth.png.
3. Restore the existing backup job before adding observability infrastructure. Installation and dry-run gates are enough to catch today's failure; an isolated restore drill is the next evidence increment. No live backup/restore was performed by this audit.

## Larger product roadmap (deferred, not falsely filed as present breakage)

- Scanned-document coverage: utils/extract.py:20-30 calls the baseline text provider and rejects empty output. Owner guidance confirms scans occur in the real work library and requires OCR fallback. Design a local OCR tier preserving content hash, source pages, extraction method, and failure reasons; validate against a mixed text/scanned corpus before promotion. Reuse the shared extraction contract rather than building a fourth parallel parser. Dependency/IT case: local OCR binaries and installation approval on work endpoints; no database/host necessary for this goal.
- Shared evidence identity and a static linked manager-review packet: bridge existing document/filing IDs to the program's agreed identity contract, with per-fact source pointers and explicit missing coverage. A local script plus static HTML fits known work capabilities. Browser WASM remains unverified on the actual work endpoint.
- Shared multi-user editing, scheduling, and central access control would require a managed internal host, Postgres storage, internal URL/port, backup storage and service account. A local-file packet cannot guarantee concurrent authoritative writes. Request those accommodations only when that goal is selected; no new hosting is necessary for the bounded fixes in this audit.

## Automation observations

Current-SHA CI is successful, but the 2026-09-14 Database Snapshot run fails at client installation. These are different acceptance surfaces. Fresh issue inventory has 2 implementation candidates, 2 informational dashboards, and no open PRs at capture. Existing open #1653 owns similarity-table Postgres bootstrap. Research-only output stages bodies and therefore does not refill GitHub issue supply until an authorized publication lane acts. Local opener, closer, and research automation configurations were inventoried in local-automations.json; no schedule changed. Shared agents-* workflows remain Workflows-owned; the database-snapshot workflow is repo-specific.
