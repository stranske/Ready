# Brief R7: Trip-Planning Core — Transportation, Lodging, Constraints

**Question.** The owner rates nuts-and-bolts trip planning (transport discovery, lodging, timing, cost comparison, company travel policy) as the weakest area of the trip-planner fleet. What external data sources are realistically accessible on a near-zero budget, how should options and constraints be modeled, and what phased path moves from reliable option discovery to approval-ready business plans?

**Confidence.** High that **fixture-first ingestion + one flight sandbox + GTFS/Routes for ground** is the correct near-term stack. Medium that Duffel live search stays affordable at personal query volumes. Low that any major OTA (Booking Demand, Expedia Rapid, Skyscanner Travel API, Kiwi Tequila) approves a hobbyist builder without a commercial travel product.

---

## 1. Repo reality (what already exists)

**FACTS:** `trip-planner` ships authenticated trips, workspace APIs, deterministic business ranking (`trip_planner/ranking/business.py`), and a `SourceAdapter` boundary (`trip_planner/sources/adapters/base.py`) — but **no concrete adapters**; all inventory loads from static JSON under `trip_planner/resources/` (`clones/trip-planner/dossier-out/DOSSIER.md`). The adapter contract requires `RawSnapshot` with explicit `AdapterIssue` degradation (`trip_planner/sources/adapters/base.py`, `docs/contracts/source-adapters.md`). Normalized `TransportOption`, `LodgingOption`, and `InventoryBundle` contracts are specified in epic `#519` (`docs/normalized-inventory-contracts-epic.md`); ingestion epic `#525` sequences adapters → resolution → candidate generation without coupling to ranking (`docs/source-ingestion-epic.md`). Business ranking already penalizes missing comparables, booking links, and hard-blocks disallowed inventory (`trip_planner/ranking/business.py` lines 47–58, 550–561). `Travel-Plan-Permission` (TPP) owns authoritative policy evaluation; `trip-planner` exports `TripPlanProposal` and consumes `PolicyEvaluationResult` (`docs/contracts/trip-plan-proposal.md`). TPP exposes planner HTTP routes with golden fixtures for policy snapshot, proposal submission, and evaluation outcomes (`tests/python/test_planner_integration_contract.py`, `tests/fixtures/planner_integration/`). TPP's approved-provider registry is YAML-driven (`config/providers.yaml`). README explicitly defers live TPP execution and external policy transport (`clones/trip-planner/README.md` lines 10–21).

**JUDGMENT:** The architecture is **ahead of the data layer**. The highest-leverage work is not another ranking rewrite — it is **one vertical slice**: adapter → normalized option → existing ranker → TPP handoff, proven on fixture trips with known-good outputs before any live API spend.

---

## 2. External API landscape

### 2.1 Flights

| Provider | Access model | Near-zero budget? | Booking-ready? |
|----------|--------------|-------------------|----------------|
| **Amadeus self-service** | Decommissioned 17 Jul 2026; enterprise-only portal remains ([developers.amadeus.com](https://developers.amadeus.com/), [traveltrade.today](https://traveltrade.today/gds-systems/amadeus-sa/amadeus-closes-self-service-apis-portal-for-developers/)) | **No** for new hobbyists | Yes (enterprise) |
| **Duffel** | Self-serve signup; free test mode; live pay-per-confirmed-order ($3/order + managed-content %, excess-search fee above 1500:1 ratio) ([duffel.com/pricing](https://duffel.com/pricing), [duffel.com/docs/api/overview/test-mode](https://duffel.com/docs/api/overview/test-mode)) | **Yes** for sandbox; live search cheap if not booking | Yes |
| **Kiwi Tequila** | Invitation-only B2B since May 2024 ([phptravels.com/blog/comprehensive-guide-to-flights-api-integration](https://phptravels.com/blog/comprehensive-guide-to-flights-api-integration)) | **No** for new applicants | Yes (virtual interlining) |
| **Skyscanner Travel API** | Partner application; >100k MAU, established business ([skyscannerpartnersupport.zendesk.com](https://skyscannerpartnersupport.zendesk.com/hc/en-us/articles/10881149122717-What-is-the-acceptance-criteria-for-the-Travel-API)) | **No** | Redirect/affiliate, not full booking |
| **Google Flights** | No public API; ITA QPX Express shut down ([scrapegraphai.com/blog/google-flights-api](https://scrapegraphai.com/blog/google-flights-api)) | Scraping wrappers exist (Apify, SerpApi) but are paid third parties | Display-only via scrapers |

**FACTS:** Google Flights has no sanctioned developer API ([dev.to/nikita_iakovlev_415524c19](https://dev.to/nikita_iakovlev_415524c19/google-flights-data-without-an-api-what-you-can-actually-get-in-2026-52c3)). Scraping publicly displayed fares is legally contested — CFAA claims against public scraping were narrowed ([whitecase.com](https://www.whitecase.com/insight-our-thinking/web-scraping-website-terms-and-cfaa-hiqs-preliminary-injunction-affirmed-again)), but ToS, copyright, and anti-bot measures remain risks for a product the owner may later use at work.

**JUDGMENT:** For home development, **Duffel test mode** is the only credible self-serve flight inventory path. Treat Google Flights scraping as **reject** for anything beyond personal one-off research. Amadeus is off the table unless the owner gains enterprise access through an employer travel program — do not plan around it.

### 2.2 Rail

| Provider | Access | Cost | Fit |
|----------|--------|------|-----|
| **Amtrak** | Static GTFS ZIP, no key ([content.amtrak.com/content/gtfs/GTFS.zip](https://content.amtrak.com/content/gtfs/GTFS.zip), [github.com/api-evangelist/amtrak](https://github.com/api-evangelist/amtrak)) | Free | Schedules, not live fares |
| **Trainline Global API** | B2B sales only; ~12-week integration ([tps.thetrainline.com](https://tps.thetrainline.com/our-products/global-api/)) | Commercial | Full EU/UK retail |
| **Rail Europe** | No public self-serve API found | N/A | — |

**JUDGMENT:** US Northeast Corridor business trips can get **schedule-level discovery** from GTFS + `gtfs-kit` parsing ([gtfs.org](https://gtfs.org/documentation/schedule/reference/)). Fares and European rail require either manual capture with provenance or a commercial partnership — not phase-1.

### 2.3 Ground / multi-modal

| Provider | Access | Cost | Fit |
|----------|--------|------|-----|
| **Google Routes API** | Self-serve; Essentials SKU ~10k free requests/month then ~$5/1k ([developers.google.com/maps/documentation/routes/usage-and-billing](https://developers.google.com/maps/documentation/routes/usage-and-billing)) | Low at planner volumes | Drive/transit timing, matrices |
| **Rome2Rio** | Partner API; basic tier up to 100k req/mo but **no live air or transit prices** ([apis.io/plans/rome2rio](https://apis.io/plans/rome2rio/rome2rio-plans-pricing/)) | Free tier if approved | Mode-sequence discovery |
| **trip-planner Google Maps** | JS adapter with bounded fallback already shipped (`README.md` line 21) | Maps Platform billing | Map display, not fare data |

**JUDGMENT:** **Google Routes** complements the existing map seam for leg timing and feasibility checks. Rome2Rio is useful for "how do I get there" narratives but not for price comparison — apply only if partner approval is easy; otherwise defer.

### 2.4 Lodging

| Provider | Access | Near-zero budget? |
|----------|--------|-------------------|
| **Booking.com Demand API** | Managed affiliate; targets established distributors ([stayapi.com/blog/booking-com-api](https://stayapi.com/blog/booking-com-api)) | **No** for side projects |
| **Expedia Rapid** | Partner application; booking-monetized, not data-only ([stayapi.com/blog/expedia-rapid-api](https://stayapi.com/blog/expedia-rapid-api)) | **No** |
| **Amadeus hotels** | Enterprise-only (same portal shutdown) | **No** |
| **Airbnb unofficial** | No sanctioned API; scraping violates ToS | **Reject** |

**JUDGMENT:** Live lodging search is **not realistic** on near-zero budget without affiliate approval. Phase-1 lodging should use **curated fixtures + owner-captured deep links** with full provenance (`provenance_summary.booking_links` already modeled in bundles — `trip_planner/resources/options/bundles/transport_lodging_bundle.json`). This matches the business ranker's need for booking-link evidence more than it needs live rate feeds.

---

## 3. Open-source planners and optimizers

**FACTS:** OpenTripPlanner is a mature open-source multi-modal router over GTFS/OSM ([github.com/opentripplanner/OpenTripPlanner](https://github.com/opentripplanner/OpenTripPlanner)). Orienteering / TOPTW formulations handle time-windowed itinerary selection ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S030505480900080X)). Google OR-Tools and PuLP support MILP routing under constraints ([developers.google.com/optimization/mip](https://developers.google.com/optimization/mip)). PADCS exposes a REST API for personalized TOPTW ([github.com/hm4uc/PADCS](https://github.com/hm4uc/PADCS)).

**JUDGMENT:** **Do not adopt** a standalone OSS trip planner as the product core — `trip-planner` already has ranking, policy packaging, and TPP contracts. Borrow **patterns** only: TOPTW for multi-city day allocation, OTP or GTFS-kit for rail leg timing, OR-Tools for small constraint-satisfaction tests in the eval harness. Running OTP is JVM ops overhead the owner cannot support from a no-terminal work PC.

---

## 4. LLM-agent travel planning — documented failure modes

**FACTS:** Tool-use hallucinations include wrong tool selection, malformed parameters, solvability errors (agent assumes task is doable), and tool-bypass (answers from training data) ([techrxiv.org/doi/pdf/10.36227/techrxiv.177219979.94060974](https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.177219979.94060974), [emergentmind.com/topics/tool-use-hallucinations](https://www.emergentmind.com/topics/tool-use-hallucinations)). Solvability hallucinations account for >40% of deep planning errors ([emergentmind.com](https://www.emergentmind.com/topics/tool-use-hallucinations)). Long-horizon travel agents suffer "constraint drift" as context grows ([arxiv.org/abs/2603.04750](https://doi.org/10.48550/arxiv.2603.04750)). DynamoTrip reports 92% constraint satisfaction using multi-agent verification loops ([zenodo.org/record/18316076](https://doi.org/10.5281/zenodo.18316076)).

**JUDGMENT:** LLMs belong **above** deterministic tools, not **instead of** them. Use agents for intent parsing and explanation generation; **never** for fare/policy numbers without tool grounding. The existing deterministic `business.py` ranker and TPP `PolicyEngine` are the correct authority chain. LangChain planner epic in trip-planner should remain deferred until fixture-backed adapters produce trustworthy option sets.

---

## 5. Recommendations

### 5.1 Realistic provider stack (near-zero budget)

| Layer | Phase-1 choice | Rationale |
|-------|----------------|-----------|
| Flights | **Duffel test adapter** → live only when booking | Only self-serve sandbox with real schema |
| US rail schedules | **Amtrak GTFS** adapter | Free, stable, schedule fidelity |
| Ground timing | **Google Routes** (Essentials) | Fits existing Maps work; low volume |
| Lodging | **Fixture + manual capture adapter** | Partnership APIs blocked |
| Policy | **TPP HTTP** (fixtures → staging) | Already contract-defined |
| Prices for comparison | Snapshot at search time + stored provenance | Avoid stale LLM quotes |

**JUDGMENT:** Total cash cost for development can stay under **$0/month** if live Duffel and Routes calls are gated behind explicit "refresh" actions and CI uses recorded snapshots only.

### 5.2 Data model (extend, do not reinvent)

Align with existing contracts:

1. **`SourceQuery`** → **`RawSnapshot`** → **`NormalizationHandoff`** (adapter layer).
2. **`TransportOption` / `LodgingOption`** with `feasibility`, `booking_terms`, `policy_summary`, `provenance` (normalized layer — epics `#521`–`#522`).
3. **`InventoryBundle`** assembled for ranking (`#524`).
4. **`TripPlanProposal`** with `comparable_reference_ids`, `booking_links`, `justifications` for TPP (`docs/contracts/trip-plan-proposal.md`).

Add one cross-cutting envelope for constraints:

```text
ConstraintEvaluation {
  constraint_id, source (policy|preference|schedule),
  severity (hard|soft), status (pass|fail|unknown),
  evidence_refs[], waiver_eligible
}
```

Attach to each option and bundle **before** ranking so `business.py` soft penalties map to explicit records rather than inferred text.

**JUDGMENT:** The model is already 80% specified in-repo. Missing piece is **constraint evaluation objects** wired from TPP `PolicyConstraintSet` imports — not a new options schema.

### 5.3 Evaluation harness

**FACTS:** Trip-planner has persona ranking tests over fixture options (`tests/ranking/test_persona_ranking_tradeoffs.py`). TPP has `washington_dc_business_trip.json` and planner-integration golden JSON (`tests/fixtures/`). Business ranking uses documented penalty amounts (`business.py` `_SOFT_PENALTY_AMOUNTS`).

**JUDGMENT:** Build a **cross-repo fixture trip suite**:

| Fixture trip | Tests | Known-good artifact |
|--------------|-------|---------------------|
| `dc-client-summit` (business) | Top-3 bundles, policy hard-block on premium cabin short-haul, comparables present | Golden `RankedResultSet` JSON + TPP `evaluation_result_compliant.json` |
| `northeast-amtrak` (business) | GTFS schedule feasibility, arrival buffer | Expected leg timings ±15 min |
| `leisure-multi-city` (leisure) | Persona reordering, no policy gate | Existing persona tests |
| `incomplete-trip` | `missing_destination` adapter issues | Workspace partial state |

Harness rules: (1) adapters never hit network in CI — use committed `RawSnapshot` recordings; (2) ranking golden files fail on score drift >0.01; (3) TPP round-trip asserts proposal JSON validates against `trip_plan.min.schema.json`; (4) every option cites `source_id` + URL per Workflows `evidence-object/v1` when promoting to approval packets.

### 5.4 Phased plan

| Phase | Goal | Deliverable | Effort |
|-------|------|-------------|--------|
| **0 — Recorded ingestion** | Prove adapter seam | `DuffelSnapshotAdapter` (test mode) + `GtfsAmtrakAdapter` reading committed ZIP; normalize to `TransportOption` | S |
| **1 — Discovery UX** | Reliable option sets | Workspace "refresh transport" action; show freshness, issues, booking deep links; leisure + business modes | M |
| **2 — Lodging capture** | Comparable lodging rows | Browser-assisted deep-link capture → `LodgingOption` with provenance; no live search | M |
| **3 — Policy loop** | Business compliance | Live TPP policy snapshot + proposal evaluate; reoptimization on `exception_required` (`integrations/tpp/reoptimization.py`) | M |
| **4 — Approval-ready** | Manager packet | `ApprovalReadyPackage` + TPP spreadsheet handoff (`/portal/handoff`) with one-click evidence | L |

**JUDGMENT:** Phases 0–2 deliver 80% of owner value. Phase 4 depends on work-side hosting (Backstop/SharePoint) left open by R4/R5 — keep synthetic data at home.

---

## 6. Ranked candidate list

| # | What | Why for owner | Effort | Prerequisite | Disposition |
|---|------|---------------|--------|--------------|-------------|
| 1 | **Duffel test-mode flight adapter** | Only self-serve flight API; feeds real transport options into existing ranker | S | Duffel developer account | `extend:trip-planner` |
| 2 | **Amtrak GTFS schedule adapter** | Free Northeast Corridor discovery for business trips | S | None | `extend:trip-planner` |
| 3 | **Cross-repo fixture eval harness** | Prevents regression in ranking + TPP compliance — owner's weakest trust area | M | Phase-0 adapters | `extend:trip-planner` (+ TPP fixtures) |
| 4 | **ConstraintEvaluation envelope on bundles** | Makes policy gates inspectable before TPP call | S | `#519` option contracts | `extend:trip-planner` |
| 5 | **Google Routes timing enrichment** | Ground leg feasibility without scraping | S | Maps Platform key (exists) | `extend:trip-planner` |
| 6 | **Lodging deep-link capture flow** | Booking links + comparables without OTA partnership | M | Provenance contracts | `extend:trip-planner` |
| 7 | **Live TPP policy execution wire-up** | Closes business approval loop | M | TPP service deploy | `extend:trip-planner` |
| 8 | **Rome2Rio partner adapter** | Multi-modal mode narratives | M | Partner approval | `extend:trip-planner` (defer) |
| 9 | **OpenTripPlanner sidecar** | EU/multi-city transit routing | L | JVM ops | `reject` (ops burden) |
| 10 | **Google Flights scraper integration** | Tempting price data | M | Apify/SerpApi paid | `reject` |
| 11 | **LLM-first planner replacing ranker** | Faster demos, worse trust | L | — | `reject` |
| 12 | **Booking/Expedia live lodging API** | Real rates | L | Commercial partnership | `reject` (near-term) |
| 13 | **Skyscanner/Kiwi flight APIs** | Broader inventory | M | Partner approval | `reject` (near-term) |

---

## 7. Open questions for the owner

1. **Primary travel corridors?** Default assumed: **US Northeast business (Amtrak + air)** plus occasional international leisure. European rail changes phase-1 adapter choice.
2. **Is live booking in scope or discovery + approval packet only?** Default: **discovery and approval-ready plans**; Duffel live mode only when owner explicitly books.
3. **Will employer provide Concur/Amex GBT API access?** Default: **no** — plan on public/synthetic data at home; managed-travel channels stay manual capture with provenance.
4. **Work-PC delivery for refreshed plans?** Default: **HTML bundle per R5** with embedded trip JSON; no live API calls from work browser.

---

## 8. Strongest objections (evaluator stance)

1. **Duffel alone under-covers legacy-airline corporate fares** that drive policy exceptions. Mitigation: comparables and "manual quote" provenance slots in `TripPlanProposal` — already anticipated by `comparables_missing` penalty in `business.py`.
2. **Fixture lodging will feel weak vs Kayak.** Correct — but OTA APIs won't approve this use case; captured links are honest about the gap.
3. **Amadeus shutdown (Jul 2026) invalidates older travel-API blog posts.** Any agent citing "free Amadeus tier" is wrong; verify against [developers.amadeus.com](https://developers.amadeus.com/).

**What would change my mind:** Employer-sponsored GDS/OTA credentials, or Rome2Rio/Trainline partner approval with written sandbox access.

---

STOP SIGNAL: NEW_CANDIDATES=13
