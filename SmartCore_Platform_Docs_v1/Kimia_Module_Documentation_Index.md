# SmartCore — Kimia Module Documentation Index

**Status:** Working Architecture / Delivery Index  
**Product:** KimiaBeauty

This document tracks the SmartCore repositories currently used to deliver Kimia Beauty and the architecture/MVP documents that define their boundaries.

## Active Kimia Module Set

### SmartCoreIdentity

Purpose:
- identity
- authentication
- organization/membership context
- session

Documents:
- `README.md`
- `docs/IDENTITY_VISION.md`
- `docs/KIMIA_IDENTITY_MVP.md`

Kimia target:
- Release 1

### SmartCoreBusiness

Purpose:
- Business identity/profile
- locale/timezone/currency context
- capability activation

Documents:
- `README.md`
- `docs/BUSINESS_VISION.md`
- `docs/KIMIA_BUSINESS_MVP.md`

Kimia target:
- Release 1

### SmartCoreBusinessCapability

Purpose:
- composable operational/economic Business capabilities
- initial capability: Service

Documents:
- `README.md`
- `docs/SERVICE_CAPABILITY_VISION.md`
- `docs/KIMIA_SERVICE_MVP.md`

Kimia target:
- Release 1

### SmartCoreScheduling

Purpose:
- working schedules
- exceptions
- availability calculation
- candidate slot generation

Documents:
- `README.md`
- `docs/SCHEDULING_VISION.md`
- `docs/KIMIA_SCHEDULING_MVP.md`

Kimia target:
- Release 2

### SmartCoreReservation

Purpose:
- hold/confirm/cancel/reschedule
- conflict prevention
- committed time/capacity allocation

Documents:
- `README.md`
- `docs/RESERVATION_VISION.md`
- `docs/KIMIA_RESERVATION_MVP.md`

Kimia target:
- Release 2

### SmartCoreFinance

Purpose:
- Money
- PaymentIntent
- Payment
- deposit/refund growth path
- future ledger/settlement

Documents:
- `README.md`
- `docs/FINANCE_VISION.md`
- `docs/KIMIA_FINANCE_MVP.md`

Kimia target:
- Release 3

### SmartCoreCommunication

Purpose:
- communication delivery
- provider abstraction
- multilingual message templates
- initial SMS channel

Documents:
- `README.md`
- `docs/COMMUNICATION_VISION.md`
- `docs/KIMIA_COMMUNICATION_MVP.md`

Kimia target:
- Release 3

### KimiaBeauty

Purpose:
- product composition
- branding
- UI/UX
- product orchestration
- release delivery

Documents:
- `README.md`
- `docs/PRODUCT_VISION.md`
- `docs/MVP_RELEASE_PLAN.md`

## Delivery Sequence

```text
Release 1
SmartCoreIdentity
→ SmartCoreBusiness
→ SmartCoreBusinessCapability.Service
→ KimiaBeauty public website

Release 2
Provider/Staff relationship
→ SmartCoreScheduling
→ SmartCoreReservation
→ Appointment flow

Release 3
SmartCoreFinance
→ SmartCoreCommunication
→ payment/deposit + confirmation/reminder
```

## Multilingual Baseline

Multilingual support is a cross-cutting requirement from the first production release.

Principles:

- Business has `defaultLocale` and `supportedLocales`.
- translatable domain content uses translation records, not language-specific columns;
- scheduling/reservation/finance domain values remain locale-independent;
- presentation localizes dates, weekdays, time, numbers, currency, and status labels;
- Communication templates are locale-aware;
- adding a new locale should not require schema redesign.

## Repositories Not Required by Current Kimia MVP

### SmartCoreIOT

Important SmartCore platform capability for physical devices and future physical-world automation.

Not required for the initial Kimia releases unless Kimia later integrates:
- smart access
- physical equipment
- sensors
- device automation

It requires its own architecture/governance track and should not be pulled into Kimia prematurely.

### SmartCoreServiceBusiness

Existing historical/service-business repository.

The current architecture is moving generic concerns toward:
- SmartCoreBusiness
- SmartCoreBusinessCapability
- Scheduling
- Reservation
- Finance
- Communication
- product composition

SmartCoreServiceBusiness should not be used as the source of truth for new Kimia implementation until its migration/retirement/composition role is explicitly decided.

### SmartCorePlatform

Architecture/governance repository.

It defines and governs platform architecture; it is not a deployable Kimia business module.

## Future Repositories / Capabilities

Not required to launch the first Kimia releases:

- SmartCoreResource
- SmartCoreAsset
- SmartCoreAccess
- SmartCoreCommerce
- SmartCoreInventory
- SmartCoreMarketplace
- SmartCoreTrading
- SmartCoreBlockchain
- SmartCoreAutomation / Workflow as separately governed

They should receive Vision + product-specific MVP documents when a real product requirement activates them.

## Documentation Rule

For each active SmartCore module:

```text
README.md
    = repository boundary and orientation

docs/*_VISION.md
    = long-term target scope and growth path

docs/KIMIA_*_MVP.md
    = minimum implementation needed by Kimia
```

The MVP may be small, but it must be compatible with the module's documented growth direction.

---

> Design for the destination. Implement only the next useful product slice.
