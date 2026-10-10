# Identity backend execution directive — 2026-10-09

Owner: Amir (@amirfassadi), project and technical owner. Attribution: direct conversation instruction on 2026-10-09, Asia/Tehran. This is not a GPG/SSH signature or an independent security review.

## Owner instruction

> «میخوام این برنامه رو شروع کنیم به نوشتنش ... باید اول بک اند رو آماده کنیم و همه ی دیتابیس و ... رو پیاده سازی کنیم ... بعدش میریم سراغ فرانت اند ... توی قدم اول یه ثبت نام انجام بدیم ... مهمترینش پیاده سازیه بک اند هستش ... داکیومنتها رو دیگه همه رو نهایی کن که میخوایم بریم جلو»

The owner explicitly authorizes backend/database implementation, registration first, frontend afterward, and documentation updates supporting delivery. Unlike earlier 'continue' instructions, this is an express implementation request. Historical pre-implementation holds do not justify stopping all work after this instruction. The authorization does not manufacture individual ADR signatures, a full four-gate validation PASS, completed runtime evidence or production safety.

Reviewed input commits: Platform `240151e25c5d9f67a58a6f4eea729a667934cc2b`; Identity `f0781c1415b3a784788c326b93c2cd45bd5206cd`. Work is isolated on `implementation/registration-backend` in both repositories; no main merge is implied.

## Engineering disposition for the first executable delivery

1. Implement .NET 10 / PostgreSQL 17 verified-contact registration under the existing separate ownership/Credential/Ready acknowledgment protocol. Preserve one Identity MVP Blueprint and staged delivery. This is an engineering stack choice under the broad execution direction, not a falsely signed historical stack acceptance.
2. Preserve atomic Person/Personal Organization/Owner Membership, absolute OTP expiry/attempt cap, bound lost-response replay, immutable initial winner, protected material transfer/disposal, distinct Ready/ownership timestamps, and transactional Outbox facts.
3. Keep deployment co-hosting distinct from accepting the unresolved shared single-transaction co-location alternative. The first executable adapter retains separate durable commits. No cross-service authentication proof is claimed by an in-process adapter.
4. Keep T16 publication and Session/BFF policy out of this phase's exposed surface; no event is marked published and registration issues no Session tokens. Do not choose between conflicting P04/P05 drafts by silently marking one accepted.
5. Finalize the **internal registration phase's** executable contract/policy/run guide. Preserve older full-MVP review documents as history and explicitly disclose remaining capabilities/gates. Do not mark all 00–16 Blueprint content final while reset, recovery, Session and transport contracts are still incomplete.
6. Retain minimal password reset inside the Identity MVP, delivered and accepted before public registration. Internal test accounts are disposable test data. A public-open gate must require reset, actual delivery, usable authentication and verified recovery/security/operations.

## Responsibility

Amir remains the accountable project/technical owner. Implementer prepares code, tests and concrete choices. The latest broad instruction permits continued implementation and routine engineering choices; any material new product/security decision must be presented concretely, without repeated requests for permission already given. No additional person's review or operations ownership is invented.

## Implemented evidence and next work

Identity implementation commit: `770486d` on local branch `implementation/registration-backend`. Local evidence: zero build warnings/errors, 21 PGlite integration checks, HTTP smoke with OpenAPI response checks, and 12 domain-event schema checks passed. GitHub push was blocked by automatic approval review pending explicit destination authorization. Native PostgreSQL CI is configured but has not run.

The Identity branch contains the phase baseline at `docs/implementation/BASELINE.md`, migration, API, durable provisioning worker, tests, development Compose and CI. Actual verification is recorded in `docs/implementation/VERIFICATION.md`; a test plan or CI file is not itself test success.

Next deliveries: formal setup/recovery, login/self/Session/BFF and password lifecycle, real delivery adapters, ordered/event transport disposition and conformance, least-privilege/keys/audit/restore/runbooks. Full 064/065/066 readiness remains an explicit evidence obligation. The host rejects Production startup until these release prerequisites are completed; no public deployment or main merge was performed by this directive.
