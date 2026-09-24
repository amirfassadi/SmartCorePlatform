# Kimia Beauty — End-to-End Architecture Review Before Implementation

**Status:** Architecture Review / Non-Normative  
**Scope:** Kimia Releases 1–5

## 1. Executive Summary

The current Kimia architecture is structurally coherent.

Authoritative ownership is now separated as follows:

~~~text
Identity          → SmartCoreIdentity
Business          → SmartCoreBusiness
Service/Commerce  → SmartCoreBusinessCapability
Scheduling        → SmartCoreScheduling
Reservation       → SmartCoreReservation
Finance           → SmartCoreFinance
Communication     → SmartCoreCommunication
Inventory         → SmartCoreInventory
Product Workflow  → KimiaBeauty
~~~

The release plan is also coherent:

~~~text
Release 1 → Public presence + Identity + Service Catalog
Release 2 → Provider + Scheduling + Booking
Release 3 → Payment + Deposit + Communication
Release 4 → Customer Operations + Reports + Commission
Release 5 → Commerce + Inventory
~~~

No additional repository is required for Releases 1–3.

The remaining risk is not missing modules. It is unresolved cross-module contracts.

---

# 2. Architecture Already Clear Enough

## Identity

SmartCoreIdentity owns Person, Organization, Membership, Credential, and Session.

Registration preserves:

~~~text
Person
+
Personal Organization
+
Membership(Owner)
~~~

Business authorization remains outside Identity.

## Business vs Business Capability

A Business is not a mutually exclusive SERVICE/COMMERCE type.

It has stable identity plus enabled capabilities.

Kimia may therefore become:

~~~text
SERVICE
+
COMMERCE
~~~

without changing Business identity.

## Staff / Provider

~~~text
Person
→ SmartCoreIdentity

Person is Staff of Kimia
→ SmartCoreBusiness.BusinessPersonRelationship

Staff can perform Service
→ SmartCoreBusinessCapability.ServiceProviderAssignment

Staff is available at a time
→ SmartCoreScheduling

Staff time is committed
→ SmartCoreReservation
~~~

This boundary is strong and reusable.

## Scheduling / Reservation / Appointment

~~~text
Scheduling = possibility
Reservation = commitment
Appointment = business meaning
~~~

Appointment staying in KimiaBeauty is appropriate until real cross-product reuse is proven.

## Finance

Business/product policy determines why money is required.

SmartCoreFinance owns monetary truth.

Appointment state and Payment state remain separate.

## Commerce / Inventory

~~~text
Commerce = Product / Order / Sale
Inventory = Stock / StockMovement
~~~

This is the correct boundary.

---

# 3. Release 1 Blockers

## GAP-01 — Business multilingual profile is incomplete

Service depends on:

~~~text
Business.defaultLocale
Business.supportedLocales[]
~~~

but the Business MVP does not consistently define supportedLocales[] and its public profile fields are currently single-value fields such as displayName and shortDescription.

### Recommended resolution

Add:

~~~text
Business
- defaultLocale
- supportedLocales[]
~~~

and:

~~~text
BusinessProfile
- businessId
- phone
- email
- locale-independent fields

BusinessProfileTranslation
- businessId
- locale
- displayName
- shortDescription
- publicAddressText?
~~~

This is a **Release 1 blocker**.

---

## GAP-02 — Money representation must be unified

Service and Product currently refer to basePrice while Finance requires explicit currency.

### Recommended resolution

Use a common Money representation from the beginning:

~~~text
Money
- amountMinor
- currency
~~~

or the canonical SmartCore equivalent.

Use it consistently for:

- Service base price
- Product base price
- Appointment price snapshot
- Order totals
- PaymentIntent
- Commission accrual

This is a **Release 1 blocker**.

---

## GAP-03 — Release 1 authorization matrix is not frozen

### Recommended MVP rule

~~~text
Public visitor
→ read active Business profile and Service catalog

Authenticated Person
→ manage own Identity profile

Kimia Owner
→ full Business + Service administration
~~~

Do not add Manager/Employee permission systems yet.

A STAFF relationship must not automatically imply admin rights.

This is a **Release 1 blocker**.

---

# 4. Release 2 Blockers

## GAP-04 — Staff onboarding flow

Staff currently requires an existing Person, but Identity MVP has no invitation/admin-created Person flow.

### Recommended MVP rule

~~~text
Staff member registers first
→ Owner selects existing Person
→ Owner creates STAFF relationship
~~~

Do not expand Identity just for this release.

---

## GAP-05 — Scheduling subject identifier

For Kimia MVP, schedule the Business relationship, not raw Person identity.

Recommended:

~~~text
providerRelationshipId
=
BusinessPersonRelationship.id
~~~

or the equivalent typed subject reference.

---

## GAP-06 — Reservation succeeds but Appointment creation fails

Current flow:

~~~text
Scheduling
→ Reservation
→ Appointment
~~~

needs compensation.

### Recommended MVP workflow

~~~text
1. Validate Service + Provider
2. Create/confirm Reservation
3. Create Appointment
4. If Appointment creation fails:
   cancel Reservation
~~~

Use a shared booking operation/correlation id.

---

# 5. Release 3 Blockers

## GAP-07 — Appointment price snapshot

If Service price changes after booking, historical Appointment meaning must not change.

### Recommended resolution

Store a booking-time snapshot:

~~~text
AppointmentPriceSnapshot
- amount
- currency
- pricingSource/reference
- capturedAt
~~~

For MVP this can live inside Appointment/KimiaBeauty.

---

## GAP-08 — Deposit / payment policy owner

Finance must not decide deposit policy.

### Recommended MVP ownership

Keep booking payment policy in Kimia product/domain:

~~~text
ServiceBookingPolicy
- serviceId
- paymentRequirementType
- depositType?
- depositValue?
~~~

If reusable later, move it into Service capability.

---

## GAP-09 — Stable communication locale

Communication needs a locale before Release 4 Customer Profile necessarily exists.

### Recommended resolution

Capture:

~~~text
notificationLocale
~~~

on Appointment/booking context.

Resolution:

~~~text
current Kimia UI locale
→ if supported
→ else Business.defaultLocale
~~~

---

## GAP-10 — Cross-module idempotency/correlation standard

Use:

~~~text
operationId / correlationId
idempotencyKey
~~~

for at least:

- booking creation
- Reservation
- PaymentIntent
- payment callback
- refund
- Communication request

---

# 6. Release 4 Gaps

## GAP-11 — Reporting definitions

Before Release 4 implementation, define:

- whether revenue uses payment date or Appointment date;
- whether refunded money is excluded;
- whether deposits count immediately;
- which timezone defines day/month boundaries.

Recommended:

~~~text
Appointment metrics
→ Appointment scheduled/completed dates

Revenue metrics
→ successful Finance payments minus successful refunds

Timezone
→ Business timezone
~~~

## GAP-12 — Commission basis

Recommended MVP basis:

~~~text
Completed Appointment
+
net successfully paid amount attributable to it
→ commission basis
~~~

Exact Kimia rule still needs configuration.

---

# 7. Release 5 Critical Gap

## GAP-13 — Online payment vs stock race

Current flow can produce:

~~~text
Customer A pays
Customer B pays
Only one physical unit exists
~~~

if stock is not allocated before payment.

### Recommended resolution

Before production online product checkout:

~~~text
Create Order
→ Allocate stock
→ Payment
→ Confirm stock issue on payment success
→ Release allocation on payment failure/expiry
~~~

A minimal Inventory concept may be:

~~~text
StockAllocation
- inventoryItemId
- locationId
- quantity
- contextType = ORDER
- contextId
- status
- expiresAt?
~~~

This is a blocker for online Release 5 sales, but not for Release 5A product catalog.

---

# 8. Non-Blocking Product Gaps

## GAP-14 — Media

Kimia will likely need service images, product images, salon gallery, and staff photos.

Do not create SmartCoreMedia yet.

For MVP, keep Kimia-specific media references/configuration in KimiaBeauty and revisit only if reusable media management is proven.

## GAP-15 — Localized SEO slugs

Not a blocker.

Use stable IDs/canonical slugs first. Translated names must not become authoritative identifiers.

---

# 9. Deployment Architecture

## GAP-16 — Repository boundary must not imply microservice boundary

Separate repositories define ownership.

They do not require independently deployed network services.

Freeze:

~~~text
Repository boundary
≠
Deployment boundary
~~~

For Kimia MVP, use the simplest deployment/composition model that preserves module contracts.

Independent service deployment should happen only when operational requirements justify it.

This decision should be closed before implementation topology is chosen.

---

# 10. Shared Technical Baseline

Freeze once across all modules:

## Identifiers
One ID strategy.

## Time
- IANA timezone names
- offset-aware/UTC instants
- local wall-clock values for recurring schedules

## Money
- precise amount representation
- explicit ISO currency

## Locale
- stable locale keys
- Business.defaultLocale
- Business.supportedLocales[]

## Idempotency
Stable keys for retriable mutations.

## Correlation
Cross-module operation/correlation id.

## Errors
Stable domain error codes, separate from provider/transport errors.

## Audit
At minimum createdAt / updatedAt and actor/correlation data where operationally important.

---

# 11. Implementation Gate

Before Release 1 coding:

~~~text
[ ] Business multilingual profile
[ ] supportedLocales[] ownership
[ ] common Money representation
[ ] Release 1 authorization matrix
[ ] repository vs deployment boundary
[ ] IDs/time/locale/error conventions
~~~

Before Release 2:

~~~text
[ ] staff onboarding rule
[ ] Scheduling subject reference
[ ] Reservation/Appointment compensation workflow
~~~

Before Release 3:

~~~text
[ ] Appointment price snapshot
[ ] deposit/payment policy owner
[ ] notificationLocale
[ ] cross-module idempotency/correlation
~~~

Before Release 5 online checkout:

~~~text
[ ] Inventory stock allocation
~~~

---

# 12. Recommended Immediate Next Pass

Close only the Release 1 blockers now:

~~~text
1. Multilingual Business/Profile model
2. Common Money model
3. Kimia Release 1 authorization matrix
4. Shared technical conventions
5. Initial deployment/composition model
6. Freeze Release 1 contracts
7. Begin implementation
~~~

Release 2–5 gaps are now documented and do not need to delay Release 1.

---

# 13. Overall Assessment

The module map is sufficient.

No major new repository is required before starting Kimia Release 1.

The next architectural work should standardize the seams between modules, then implementation can begin incrementally.

> Design the boundaries once. Ship the product slice by slice.
