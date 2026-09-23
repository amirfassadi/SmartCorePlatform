# SmartCore Platform — Capability Landscape, Product Vision, and Architectural Analysis

**Status:** Analysis / Discussion Draft  
**Normative:** No  
**Purpose:** Consolidate the current SmartCore product vision, capability landscape, existing project evidence, and architectural implications before any taxonomy or repository-boundary changes are approved.  
**Date:** 2026-09-23

---

## 1. Purpose

SmartCore is not intended to be a single application such as a booking system, accounting product, IoT dashboard, smart-home controller, trading bot, or marketplace.

The emerging vision is a reusable, composable platform that provides shared semantic, technical, business, financial, physical-world, and automation capabilities from which many products and industry solutions can be assembled.

The practical design goal is:

> Build a capability once, establish a stable contract for it, and compose it into many products without duplicating the underlying source of truth.

This document captures the current analysis derived from the SmartCore platform documentation and the following active or historical project lines:

- SmartCorePlatform
- SmartCoreIdentity
- SmartCoreServiceBusiness
- SmartCoreIOT
- GroupExpenseBot
- telegram_expense_bot
- ICT-Trading-System

This document does not supersede the canonical Platform Taxonomy, SFMM, ADRs, or platform specifications. Where this analysis implies a change to an existing architectural boundary, the change must be handled through the normal governance process.

---

## 2. Why SmartCore Is a Platform

The defining property of SmartCore is composition.

A product should not need to implement identity, organization, payment, reservation, IoT access control, finance, workflow, communication, trading, or analytics from scratch.

Instead, complete products should be composed from reusable capabilities.

Example:

Smart Parking = Identity + Asset + Resource + Reservation + Pricing + Finance + Access + IoT

Smart Home Rental = Identity + Asset + Marketplace + Reservation + Payment + Access + IoT

Service Business = Identity + Business + Service Catalog + Scheduling + Reservation + Resource + Finance + Communication

Mechanic Business = Service Business + Commerce + Inventory + Finance + Resource

Real Estate Platform = Business + Asset + Listing + Brokerage + Marketplace + Finance + Identity Verification

Crypto Trading Platform = Identity + Finance + Trading + Portfolio + Risk + Automation + Blockchain + DEX Integration + Copy Trading

The result is a platform that spans both the digital world and the physical world while preserving clear ownership boundaries.

---

## 3. Core Architectural Principles

### 3.1 Semantic first

SmartCore begins from stable semantic concepts and explicit boundaries rather than implementation technologies.

### 3.2 Composition over rigid classification

A Business should not be forced into exactly one fixed type such as Service, Commerce, or Financial.

A Business may activate several business capabilities simultaneously.

Example:

A mechanic shop may provide repair services, sell spare parts, manage inventory, reserve staff/equipment time, accept payments, and operate IoT devices.

Therefore:

Business != one fixed BusinessType

Business = Core Business Identity + Relationships + Enabled Capabilities + Domain-Specific Semantics

### 3.3 Platform capability != product

Identity, Finance, Reservation, IoT, Resource, Trading, Communication, and Workflow are reusable platform capabilities.

A finished customer-facing system is a solution/product composition.

### 3.4 Domain != capability

"Real Estate", "Automotive", "Healthcare", "Beauty", and "Hospitality" are domains or industries.

"Reservation", "Asset", "Finance", "Service", "Commerce", "IoT", and "Workflow" are reusable capabilities.

### 3.5 Asset != Resource != Device

These concepts must remain distinct.

Example:

- Car = Asset
- Car rental availability/usage right = Resource or Offering
- GPS/lock/immobilizer controller = Device

Example:

- Printer = Asset
- 100-page printing usage = Resource/Usage Offering
- Relay/sensor/controller = Device

### 3.6 Identity verification != ownership verification

Knowing who a person is does not prove that the person owns or controls a given property, vehicle, parking space, machine, or other asset.

These are separate processes and separate evidence models.

### 3.7 Stable core, replaceable adapters

External providers and protocols must remain behind stable contracts.

Examples:

- Payment provider adapters
- SMS/email providers
- Exchange adapters
- DEX adapters
- Blockchain RPC providers
- MQTT/device transports

Business/domain logic must not depend directly on one provider.

---

## 4. Architectural View of the Platform

A useful working model is:

### Foundation
- Semantic Foundation / SFMM
- Vocabulary and semantic rules
- Architecture governance
- Platform taxonomy
- Modeling standards
- Composition rules
- Blueprint standards
- Validation
- AI-assisted generation standards

### Reusable Platform Capabilities
- Identity
- Organization/Tenancy
- Authorization
- Business
- Asset
- Resource
- Scheduling
- Reservation
- Finance
- Accounting
- Commerce
- Marketplace
- IoT
- Access
- Communication
- Notification
- Workflow
- Automation
- Analytics
- AI
- Trading
- Blockchain/Web3
- Search
- Media
- Audit
- Configuration
- Localization

### Domain Capabilities
- Service Business
- Real Estate
- Automotive
- Hospitality
- Healthcare
- Retail
- Manufacturing
- Asset Rental
- Smart Building
- Smart Home
- Smart Parking
- Trading Strategy Models

### Solutions / Products
- Salon/clinic/repair applications
- Parking marketplace
- Home rental platform
- Vehicle rental platform
- Equipment/printer rental
- Smart building application
- Business ERP-like products
- Group expense product
- DEX trading platform
- Trading robot platform
- Copy-trading platform

---

# 5. Capability Landscape

## 5.1 Identity and Authentication

Responsibilities and future capabilities include:

- Person
- Credential
- Registration
- Login / Logout
- Session
- Password management
- Email verification
- Phone verification
- MFA / OTP
- identity events
- preferred locale
- identity recovery
- external identity providers
- KYC / identity verification
- future Device Identity
- future Service Identity
- future AI Agent Identity

Identity answers "who is this actor?"

It must not own business authorization rules, booking semantics, trading strategy, asset ownership, or financial-domain policy.

---

## 5.2 Organization, Tenancy, and Membership

Capabilities:

- Organization
- Personal Organization
- Membership
- membership lifecycle
- organization lifecycle
- tenant isolation
- owner context
- member context
- multiple organizations per person
- organization context switching
- organization-scoped relationships

A Person may participate in several Organizations with different relationships.

No global user role should be used to describe all contexts.

---

## 5.3 Authorization and Security

Capabilities:

- Role
- Permission
- policy
- resource-scoped authorization
- organization-scoped authorization
- business-scoped authorization
- contextual authorization
- temporary access
- time-based authorization
- revocation
- audit trail
- future policy/attribute-based authorization

Authentication determines identity.

Authorization determines what the identified actor may do in a particular context.

---

## 5.4 Business Foundation

SmartCoreBusiness should represent the common concept of a Business without assuming one industry.

Candidate responsibilities:

- Business
- Business Profile
- Business Locations
- general Business Policy
- business lifecycle
- organization/business relationship
- ownership/reference context
- industry classification
- enabled business capabilities
- legal/organizational presentation metadata

A Business may simultaneously participate in several capability models.

Examples:

Beauty Center = Service + Reservation + Resource + Finance + optional Commerce

Mechanic = Service + Commerce + Inventory + Resource + Reservation + Finance

Consulting Company = Service + Subscription + Finance

Trading Company = Trading + Finance + Automation + Business

The final ownership boundary between Organization and Business still requires explicit canonical definition.

---

## 5.5 Service Business

Service Business should own service-business meaning, not generic platform capabilities.

Candidate concepts:

- Service
- Service Category
- Service Catalog
- service-specific policy
- customer relationship
- staff/provider relationship
- Appointment business state
- Booking Intent
- service execution
- provider/service assignment
- service commission policy
- service duration
- business-facing availability rules

External capabilities it should consume:

- Identity
- Organization/Tenancy
- Authorization
- Scheduling
- Reservation
- Resource
- Finance/Payment
- Communication/Notification
- Audit
- Media

This implies that generic Business, generic Reservation, Payment, Resource, and Identity should not be duplicated as local sources of truth.

---

## 5.6 Commerce

Candidate capabilities:

- Product
- Product Category
- Catalog
- Offer
- Cart
- Order
- Sale
- Purchase
- Supplier
- Pricing
- Discount
- Promotion
- Return
- Refund integration
- invoice integration
- physical/digital product support

Commerce may coexist with Service Business.

A mechanic can repair a vehicle and also sell parts.

A clinic may sell products in addition to services.

A company can provide both services and goods.

---

## 5.7 Asset Management

Asset becomes a major platform concept when SmartCore is used to unlock revenue from idle physical assets.

Candidate capabilities:

- Asset
- Asset Type
- Asset lifecycle
- Asset status
- Ownership
- Custody
- ownership evidence
- Ownership Verification
- asset documents
- asset metadata
- Asset Location
- transfer of ownership
- shared ownership
- asset activation/deactivation

Examples:

- Apartment
- Parking space
- Vehicle
- Printer
- Machine
- Equipment
- Building
- Land
- Tool

A physical asset can exist without being reservable or monetized.

---

## 5.8 Resource Management

Resource describes something usable, allocatable, reservable, accessible, or consumable.

Candidate capabilities:

- Resource
- Resource Category
- Space Resource
- Equipment Resource
- Vehicle Resource
- Service Resource
- Access Resource
- status
- capacity
- Resource Assignment
- Resource Availability reference
- Resource Usage
- Resource Session
- Usage Meter
- Resource-Device relationship

Usage can be metered by:

- time
- quantity
- cycles
- pages
- energy
- distance
- capacity

The existing SmartCoreIOT line historically placed Resource at the center of a physical-world system. In the future architecture, Resource is likely a reusable platform boundary consumed by IoT and marketplace/rental products rather than owned by the IoT implementation itself.

---

## 5.9 Scheduling and Availability

Capabilities:

- Calendar
- Schedule
- Availability
- recurring availability
- blackout periods
- timezone rules
- capacity
- timeslots
- staff availability
- resource availability
- conflict detection

Scheduling describes possible time allocation.

Reservation owns an actual allocation/hold/commitment.

---

## 5.10 Reservation

Candidate capabilities:

- Reservation
- hold
- confirmation
- cancellation
- expiration
- conflict prevention
- recurring reservation
- resource reservation
- reservation lifecycle
- reservation-generated access windows

Important distinction:

Booking/Appointment = business semantics

Reservation = generic allocation of time/capacity/resource

---

## 5.11 Marketplace and Listings

Candidate capabilities:

- Listing
- provider/seller
- buyer/consumer
- discovery
- search integration
- offers
- availability projection
- price projection
- commission
- reputation/review extension
- marketplace transaction orchestration

The marketplace can support:

- services
- products
- parking
- homes
- vehicles
- equipment
- printers
- other rentable assets

Marketplace is not the source of truth for Identity, Asset, Reservation, or Finance.

---

# 6. Physical World and IoT

## 6.1 SmartCoreIOT Vision

The current IoT product path starts with smart parking-door control and grows toward whole-home automation.

The longer-term economic vision is broader:

1. Make physical access programmable.
2. Know who may use a resource.
3. Know when that access is valid.
4. Connect access rights to reservation and payment.
5. Monetize previously idle assets.

The platform may therefore support:

- smart parking
- smart homes
- home rental
- parking rental
- car rental
- printer/equipment rental
- controlled machine usage
- access-managed workspaces

SmartCoreIOT itself should remain focused on the technology boundary of connected devices.

---

## 6.2 Device Management

Candidate IoT responsibilities:

- Device
- Device Capability
- Device Channel
- Sensor
- Actuator
- Device provisioning
- device lifecycle
- health
- heartbeat
- connectivity
- telemetry
- command
- execution
- firmware
- OTA
- MQTT
- WebSocket/HTTP transport where applicable
- edge behavior
- offline behavior

IoT should not own Person, Reservation, Pricing, Payment, Asset Ownership, Business, or Marketplace.

---

## 6.3 Device Twin

Existing SmartCoreIOT work includes a relatively mature Device Twin model.

Relevant capabilities:

- Desired State
- Reported State
- Delta
- reconciliation
- sync state
- versioning
- retry
- stale command rejection
- field-level state synchronization
- command acknowledgement

The desired architectural relationship is:

Business/Access Decision -> IoT Command Intent -> Device Twin -> Transport -> Device -> Reported State

The IoT subsystem executes the physical action. It should not own the business decision that grants the right to execute it.

---

## 6.4 Physical Access Control

Capabilities:

- Access Credential
- RFID
- PIN
- QR
- mobile token
- Access Policy
- Access Point
- temporary access
- reservation-driven access
- scheduled access
- revocation
- access event audit

Example:

A customer reserves a parking space for one night.

Identity confirms the person.

Reservation confirms the right and time window.

Finance confirms the required payment/deposit.

Authorization/Access creates a temporary access grant.

IoT executes the physical gate opening.

---

# 7. Idle Asset Economy

A core SmartCore product direction is to unlock economic value from underused assets.

Canonical conceptual flow:

Owner
-> Identity Verification
-> Asset Registration
-> Ownership Verification
-> Asset Activation
-> Resource/Offering Creation
-> Availability
-> Pricing
-> Listing
-> Customer Discovery
-> Reservation
-> Payment
-> Temporary Access Grant
-> IoT/Physical Execution where applicable
-> Usage Session
-> Settlement
-> Owner Revenue
-> Platform Commission

This flow should work for both individual owners and organizations.

Examples:

- A residential parking space rented overnight.
- An apartment rented for a defined period.
- A verified vehicle made available for rental.
- A printer sold by time/page/usage.
- Industrial equipment monetized by cycle/hour.
- Access to a room or workspace sold for a scheduled interval.

The key platform proposition is not merely device control. It is controlled, verified, monetizable access to assets and resources.

---

# 8. Finance, Accounting, and Economic Capabilities

## 8.1 Finance Core

Finance should provide reusable financial primitives and financial truth.

Candidate capabilities:

- Money
- Currency
- exchange-rate references
- Account
- Wallet
- Balance
- Ledger
- Ledger Entry
- Transaction
- Debit/Credit
- Transfer
- Payment
- Refund
- Settlement
- Deposit
- Fee
- Commission
- Revenue Share
- multi-currency
- reconciliation
- idempotent financial operations

Finance is consumed by Service Business, Commerce, Marketplace, Asset Rental, IoT monetization, and Trading.

---

## 8.2 Accounting and Financial Management

Historical GroupExpenseBot and telegram_expense_bot work demonstrates a separate financial-management domain.

Candidate capabilities:

- Expense
- Income
- Business Cost
- personal expense
- group expense
- shared expense
- cost allocation
- budget
- category
- cost center
- accounts payable/receivable extensions
- cash-flow reporting
- P&L reporting
- financial reports

Important distinction:

Expense/Cost = business/accounting meaning

Payment = movement/execution of money

Ledger Entry = financial/accounting record

Settlement = resolution of obligations

These must not collapse into one entity.

---

## 8.3 Shared and Group Finance

Candidate capabilities:

- Group
- Group Membership
- shared expenses
- payer
- participants
- split calculation
- multi-currency group accounting
- group balance
- debt simplification
- settlement
- payment confirmation

A "Group" in an expense-sharing product should not automatically be treated as the same concept as an Organization tenant.

---

# 9. Trading and Digital Asset Economy

## 9.1 Trading Is Not the Same as Finance

Trading and Finance interact but have different ownership.

Finance owns financial truth such as money movement, fees, settlement, balances, and ledgers.

Trading owns market behavior such as orders, positions, strategy, execution, and portfolio exposure.

Candidate SmartCoreTrading concepts:

- Market
- Instrument
- Symbol
- Market Data
- Exchange/Venue
- Trading Account
- Order
- Trade
- Position
- Portfolio
- Execution
- PnL
- trading fees
- risk state
- order lifecycle

---

## 9.2 Market Intelligence and Analysis

Candidate capabilities:

- OHLCV
- technical indicators
- swing detection
- liquidity models
- market structure
- FVG
- displacement
- signal generation
- ICT models
- custom analytical models

The ICT-Trading-System project currently belongs here and in the Strategy layer.

Its current deterministic sequence is:

Liquidity Sweep
-> Displacement
-> Market Structure Shift
-> Fair Value Gap
-> Retracement
-> Micro MSS
-> Signal

The current project is a research detector, not yet a complete live-trading engine.

---

## 9.3 Strategy Engine

Candidate capabilities:

- Strategy Definition
- Strategy Parameters
- Strategy State
- Signal
- Entry Conditions
- Exit Conditions
- invalidation
- stop-loss/take-profit policies
- strategy lifecycle
- execution intent

Potential strategy plugins:

- ICT
- Grid
- DCA
- Arbitrage
- indicator-based strategies
- AI-assisted strategies

ICT should be a strategy model/plugin, not the core definition of SmartCoreTrading.

---

## 9.4 Backtesting and Research

Candidate capabilities:

- historical replay
- deterministic strategy execution
- commission model
- slippage model
- fill model
- parameter experiments
- out-of-sample validation
- walk-forward validation
- research reports
- reproducibility

Research and production execution should share strategy specifications while using different execution adapters.

---

## 9.5 Risk Management

Candidate capabilities:

- max position size
- max portfolio exposure
- per-trade risk
- leverage constraints
- drawdown limits
- stop loss
- take profit
- asset exposure
- market exposure
- strategy-level limits
- copy-trading risk limits

No strategy should bypass risk controls when operating automatically.

---

## 9.6 Portfolio Management

Candidate capabilities:

- Portfolio
- Asset Balance
- Position
- Allocation
- Exposure
- realized/unrealized PnL
- strategy allocation
- performance
- future rebalancing

---

## 9.7 Robot Trading

Candidate capabilities:

- bot instance
- strategy scheduling
- strategy state
- signal -> trade intent
- risk validation
- order creation
- execution
- retry/recovery
- monitoring
- multiple accounts
- multiple venues
- multiple portfolios

Robot Trading should compose Strategy + Risk + Portfolio + Execution + Finance rather than reimplementing them.

---

## 9.8 Copy Trading

Candidate capabilities:

- Leader
- Follower
- Strategy Provider
- Copy Relationship
- allocation percentage
- fixed allocation
- risk scaling
- max exposure
- allowed markets
- pause/stop copy
- performance records
- follower execution policy

Copy trading must produce follower-specific execution intents after applying follower-specific risk rules.

---

# 10. Exchange, Blockchain, and DEX Integration

## 10.1 CEX Connectivity

Historical telegram_expense_bot branches show exploration of exchange integrations such as Bybit, MEXC, and Hyperliquid-related support.

The future platform should normalize external exchange connectivity behind contracts.

Capabilities:

- account connectivity
- balances
- orders
- trades
- positions
- market data
- deposit/withdraw integration where appropriate
- venue-specific adapter

---

## 10.2 Blockchain / Web3

Candidate capabilities:

- Blockchain Network
- Token
- Wallet Address
- chain transaction
- signing integration
- smart-contract interaction
- gas/fee estimation
- transaction confirmation
- RPC provider adapter
- wallet connection
- non-custodial architecture
- custodial architecture if ever explicitly adopted

Custody must be treated as an explicit architectural and security decision.

---

## 10.3 DEX Integration

The intended product direction includes a platform similar in user experience to advanced trading-automation products while executing through decentralized exchange infrastructure.

Candidate capabilities:

- DEX Adapter
- Quote
- Swap
- Route
- Slippage policy
- Liquidity
- Pool reference
- transaction submission
- confirmation tracking
- multi-DEX routing
- aggregation
- protocol abstraction

Desired dependency direction:

Trading Domain
-> Stable Execution Contract
-> DEX Adapter
-> External Protocol / Blockchain

Trading-domain logic must not depend on a specific DEX implementation.

---

# 11. Automation and Workflow

## 11.1 Automation

Capabilities:

- event trigger
- schedule trigger
- condition
- action
- IF/THEN rule
- retry
- timeout
- device automation
- business automation
- finance automation
- trading automation
- alert automation

Automation is a reusable engine.

Specific business rules remain owned by the domain that defines their meaning.

---

## 11.2 Workflow

Capabilities:

- multi-step process
- state transition
- human task
- automated task
- approval
- compensation
- retries
- orchestration
- cross-capability workflow

Workflow should coordinate capabilities through contracts/events rather than absorb their domain ownership.

---

# 12. Communication and Notifications

## 12.1 Communication

Capabilities:

- Email
- SMS
- Push
- Telegram
- Webhook
- in-app messaging
- templates
- channels
- provider abstraction

## 12.2 Notification

Capabilities:

- notification intent
- event-driven notification
- recipient preferences
- localization
- template resolution
- delivery
- retry
- delivery status

The domain emits the need to communicate.

Communication/Notification owns the delivery mechanics.

---

# 13. Configuration, Localization, Media, Search, Audit, Observability

## Configuration
- platform configuration
- organization configuration
- business configuration
- feature flags
- policies
- defaults

## Localization
- system locale
- person preferred locale
- business default locale
- translated business content
- RTL support
- timezone
- currency formatting
- fallback rules

## Media
- images
- documents
- logos
- attachments
- upload/storage abstraction
- access-controlled media references

## Search and Discovery
- business search
- service search
- product search
- resource search
- asset listing search
- location-based search
- filtering/ranking

## Audit
- actor
- action
- time
- context
- before/after
- administrative audit
- security audit
- financial audit
- access audit

## Observability
- logging
- metrics
- tracing
- service health
- device health
- execution monitoring
- financial reconciliation monitoring
- trading execution monitoring

---

# 14. Analytics and AI

## Analytics

Potential analytical areas:

- business performance
- financial analytics
- resource utilization
- occupancy
- IoT telemetry
- asset utilization
- marketplace conversion
- revenue
- customer behavior
- trading performance
- strategy performance

## AI

Potential platform uses:

- assistants
- anomaly detection
- prediction
- recommendation
- demand forecasting
- pricing assistance
- trading research
- strategy research
- device anomaly detection
- business insight generation
- code/document generation
- future AI Agent identity

AI should consume governed platform data and contracts rather than silently become a new source of truth for existing domains.

---

# 15. Pricing, Subscription, Promotion, and Economic Models

## Pricing

The platform should support different units of monetization:

- fixed
- hourly
- daily
- per unit
- per cycle
- per page
- per kWh
- per distance
- capacity-based
- hybrid
- future dynamic pricing

## Subscription and Billing

Capabilities:

- Plan
- Subscription
- recurring billing
- usage billing
- entitlement
- invoice
- renewal
- cancellation
- limits/quotas

## Referral, Loyalty, and Promotion

Capabilities:

- referral
- invitation
- referral commission/reward
- loyalty points
- promotion
- coupon
- campaign

---

# 16. Developer Platform and Integration Surface

Candidate capabilities:

- REST APIs
- WebSocket
- Webhooks
- event contracts
- OpenAPI
- generated SDK/client
- API versioning
- integration adapters
- sandbox
- provider mocks
- test harnesses
- Blueprint
- Blueprint Validator
- generators
- extension contracts
- AI-assisted implementation workflows

The platform should make correct composition easier than local reinvention.

---

# 17. Product Composition Examples

## 17.1 Smart Parking Rental

Identity
+ Asset
+ Ownership Verification
+ Resource
+ Availability
+ Pricing
+ Marketplace
+ Reservation
+ Finance
+ Access
+ IoT

## 17.2 Smart Home Rental

Identity
+ Property Asset
+ Ownership Verification
+ Marketplace
+ Reservation
+ Payment
+ Smart Access
+ IoT
+ Communication

## 17.3 Vehicle Rental

Identity
+ KYC
+ Vehicle Asset
+ Ownership Verification
+ Marketplace
+ Reservation
+ Deposit
+ Finance
+ Access
+ IoT/GPS
+ Usage
+ Settlement

## 17.4 Printer / Equipment Monetization

Asset
+ Resource
+ Metering
+ Availability
+ Pricing
+ Reservation or On-Demand Access
+ Payment
+ IoT
+ Usage Settlement

## 17.5 Mechanic Business

Business
+ Service Business
+ Commerce
+ Inventory
+ Resource
+ Scheduling
+ Reservation
+ Finance
+ Communication

## 17.6 Real Estate Brokerage

Business
+ Asset
+ Listing
+ Brokerage semantics
+ Marketplace
+ Identity
+ Finance
+ Communication

A real-estate business cannot be modeled accurately as only "Service" or only "Commerce". It is a domain composition.

## 17.7 DEX Trading Automation Platform

Identity
+ Trading
+ Market Data
+ Strategy Engine
+ Risk
+ Portfolio
+ Automation
+ Blockchain
+ DEX Adapters
+ Finance
+ Communication
+ Analytics

## 17.8 Copy Trading

Identity
+ Trading
+ Strategy
+ Leader/Follower Relationships
+ Risk
+ Portfolio
+ Execution
+ Finance
+ Analytics

---

# 18. Implications for Existing Repositories

## SmartCoreServiceBusiness

Current ServiceBusiness work contains generic Business concepts together with Service concepts.

If SmartCoreBusiness becomes the canonical owner of generic Business identity/profile/location/policy, ServiceBusiness may need to consume those concepts rather than own them.

This requires an explicit architecture decision before refactoring.

## SmartCoreIOT

The current/historical IoT model contains concepts beyond IoT, including Identity, Resource, Reservation, Wallet, Transaction, Notification, and Automation.

The next architecture should separate reusable cross-platform ownership from IoT-specific ownership.

SmartCoreIOT should likely concentrate on Device, Twin, Telemetry, Commands, Connectivity, Firmware, Provisioning, and execution of physical actions.

## GroupExpenseBot / telegram_expense_bot

These projects contain useful financial and business concepts but combine Identity, Groups, Business, Expense, Payment, Ledger, Settlement, and product UI concerns.

Their value for the platform is primarily domain discovery and implementation experience.

Concepts should be extracted into appropriate capability boundaries rather than ported as one monolith.

## ICT-Trading-System

This project is currently a deterministic research/signal detector.

It should be treated as a Strategy/Market Analysis implementation or plugin, not as the definition of the entire Trading platform.

---

# 19. Candidate Top-Level Capability Families

The following is a working landscape, not a frozen taxonomy.

### Foundation and Governance
- SFMM / Semantic Foundation
- Platform Taxonomy
- Modeling Standards
- Composition Rules
- Governance / ADR
- Blueprint / Validation / Generation

### Identity and Trust
- Identity
- Organization/Tenancy
- Membership
- Authorization
- Verification
- Audit

### Business and Commerce
- Business
- Service Business
- Commerce
- Marketplace
- Subscription
- Promotion / Loyalty / Referral

### Asset and Physical Economy
- Asset
- Resource
- Scheduling
- Reservation
- Usage / Metering
- Location
- Access
- IoT
- Building/Home extensions

### Finance
- Finance Core
- Payment
- Settlement
- Accounting / Expense Management
- Billing

### Trading and Digital Assets
- Market Data
- Trading
- Strategy
- Backtesting/Research
- Risk
- Portfolio
- Robot Trading
- Copy Trading
- CEX Connectivity
- Blockchain
- DEX Connectivity

### Platform Operations
- Workflow
- Automation
- Communication
- Notification
- Configuration
- Localization
- Media
- Search
- Analytics
- AI
- Observability

### Product / Solution Composition
- Service businesses
- Commerce businesses
- Real Estate
- Smart Parking
- Smart Home
- Smart Building
- Rental marketplace
- Vehicle rental
- Equipment monetization
- Trading automation
- Copy trading
- future industry solutions

---

# 20. Architectural Questions That Must Be Resolved Before Freezing the Next Taxonomy

1. What is the exact relationship between Organization and Business?
2. Does generic Business ownership move out of ServiceBusiness into SmartCoreBusiness?
3. Is Asset a first-class platform capability?
4. What is the formal distinction between Asset and Resource?
5. Is Access a separate platform capability, a Physical capability, or part of another platform?
6. Should Scheduling be independent from Reservation?
7. What is the formal boundary between Booking/Appointment and Reservation?
8. What belongs to Finance Core versus Accounting versus Billing/Payment?
9. Is Trading a first-class platform capability?
10. Should Blockchain/Web3 be a platform capability or an infrastructure/integration family?
11. What is the formal boundary between Automation and Workflow?
12. Which responsibilities remain in SmartCoreIOT after generic Resource, Reservation, Finance, Identity, and Automation are externalized?
13. How should ownership verification be modeled?
14. How are individual asset owners supported without forcing every scenario into a commercial Business?
15. Which of the proposed capabilities deserve independent repositories, and which should remain modules inside a larger platform?
16. What is the canonical dependency direction among Business, Asset, Resource, Reservation, Finance, IoT, and Marketplace?
17. Which capabilities are Phase 1 requirements versus future architecture placeholders?

These questions should be answered through architecture review and ADRs where required.

---

# 21. Proposed Strategic Definition

A working definition of SmartCorePlatform is:

> SmartCorePlatform is a modular, composable platform for modeling identities, organizations, businesses, assets, resources, value, markets, workflows, and the physical world, so that reusable capabilities can be assembled into interoperable digital products, business systems, financial systems, trading systems, IoT systems, and asset-economy solutions without duplicating their core sources of truth.

A shorter product principle is:

> Build capabilities once. Compose them into many products.

---

# 22. Next Recommended Architecture Step

Before refactoring SmartCoreServiceBusiness, SmartCoreIOT, or the financial/trading projects, SmartCore should produce an approved capability map with four explicit levels:

1. Foundation
2. Platform Capability
3. Domain Capability
4. Solution / Product

For every candidate platform capability, the map should specify:

- Owns
- Consumes
- Must Not Own
- Public Contracts
- Events
- Upstream dependencies
- Downstream consumers
- Whether it deserves its own repository
- MVP requirement
- governance status

The result should become the basis for a formal "SmartCore Repository Map" and the next revision of the Platform Taxonomy.

---

## 23. Status of This Document

This document is intentionally non-normative.

It records the current consolidated vision and analysis so that the next architecture discussion can operate from one shared reference.

Any change to canonical ownership, platform taxonomy, lifecycle, or frozen semantic definitions must be performed through the appropriate SmartCore governance process.
