# Beauty Salon Solution — Incremental Delivery Roadmap and MVP Decomposition

**Status:** Planning / Discussion Draft  
**Normative:** No  
**Repository:** SmartCorePlatform  
**Date:** 2026-09-23  
**Purpose:** Define an incremental delivery roadmap for building a reusable beauty-salon solution on top of SmartCore capabilities, before writing detailed MVP specifications for each capability.

---

## 1. Goal

The immediate product goal is to launch a usable beauty-salon website and service flow that supports:

- customer registration and login
- salon/business setup
- service definition
- pricing
- staff/service assignment
- staff availability
- appointment booking
- payment
- confirmations and reminders
- customer and admin views
- reporting
- later commission/accounting and commerce extensions

The implementation should be incremental. Each step should produce a coherent capability or product slice that can be validated before the next layer is added.

The solution should also remain reusable for other service businesses such as:

- barbershops
- clinics
- repair centers
- consulting businesses
- training/education services
- massage/wellness centers
- home-service providers

---

## 2. Delivery Principle

The salon product should be built by composing SmartCore capabilities rather than implementing all concerns inside one application.

Working dependency direction:

SmartCoreIdentity
-> SmartCoreBusiness
-> SmartCoreServiceBusiness
-> SmartCoreResource / Scheduling
-> SmartCoreReservation
-> SmartCoreFinance
-> SmartCoreCommunication

The exact repository boundaries remain subject to architecture decisions.

The practical delivery rule is:

> Build the smallest usable slice, validate it, then add the next dependent capability.

---

# 3. Phase 1 — Identity / Registration

## Goal

Allow users to register, verify their identity contact method, log in, and establish the minimum identity context required for later business and customer flows.

## Initial MVP Scope

- registration with phone or email
- OTP or equivalent verification
- login
- logout
- session management
- basic profile
- initial role/context support needed by the product

Expected core outputs may include:

- Person
- Organization
- Membership
- Session

The final role/authorization model must follow the SmartCore Identity and Authorization boundaries rather than using a single global user role.

## Exit Condition

A user can register, verify, authenticate, and receive a valid application identity context.

---

# 4. Phase 2 — Business Setup

## Goal

Represent the beauty salon as a Business.

## Initial MVP Scope

- create salon/business
- business name
- address/location reference
- contact information
- opening hours
- timezone
- currency
- active/inactive status
- basic Business Profile
- owner/business relationship

## Exit Condition

An authenticated owner can create and manage one salon/business profile.

---

# 5. Phase 3 — Service Catalog

## Goal

Allow the salon to define the services it sells.

## Initial MVP Scope

- Service Category
- Service
- service name
- description
- duration
- base price
- active/inactive state
- category assignment

Example categories:

- Hair
- Nail
- Facial
- Makeup
- Skin Care

Example services:

- Haircut
- Hair Coloring
- Blow Dry
- Manicure
- Facial

## Important Boundary

The service catalog is a business offering model. It should not automatically be treated as the same thing as a generic Resource.

## Exit Condition

The salon can publish a structured list of active services with price and duration.

---

# 6. Phase 4 — Staff / Service Provider

## Goal

Define who can perform which services.

## Initial MVP Scope

- Staff relationship
- link Staff to Person
- link Staff to Business
- Staff -> Service assignment
- active/inactive staff state
- optional staff-specific duration override
- optional staff-specific price override

## Important Boundary

Identity owns the Person.

ServiceBusiness owns the business relationship and service-provider semantics.

## Exit Condition

Each bookable service can be associated with one or more eligible staff members.

---

# 7. Phase 5 — Availability / Working Schedule

## Goal

Determine when a provider can accept appointments.

## Initial MVP Scope

- working days
- start/end time
- recurring weekly schedule
- breaks
- days off
- simple exceptions
- timezone handling
- conflict-safe availability generation

## Exit Condition

The system can calculate the available times for a staff member and service.

---

# 8. Phase 6 — Reservation / Appointment

## Goal

Provide the core customer booking flow.

## Customer Flow

Customer
-> Select Service
-> Select Staff or Any Staff
-> Select Date
-> View Available Slots
-> Select Slot
-> Create Appointment

## Initial MVP Scope

- Appointment creation
- reservation/slot hold as needed
- double-booking prevention
- confirmation
- cancellation
- reschedule
- basic appointment lifecycle

Candidate statuses:

- Pending
- Confirmed
- Completed
- Cancelled
- NoShow

## Important Boundary

Appointment and Booking are business-semantic concepts.

Reservation is the generic allocation of time/resource capacity.

These concepts may be related but should not be collapsed automatically.

## Exit Condition

A customer can reserve an available slot without creating scheduling conflicts.

---

# 9. Phase 7 — Pricing

## Goal

Calculate the amount associated with the selected service/appointment.

## Initial MVP Scope

- base service price
- optional staff-specific price
- manual discount if needed
- total amount
- currency

## Future Extensions

- packages
- coupon
- membership pricing
- peak/off-peak pricing
- dynamic pricing
- promotional rules

## Exit Condition

Every payable appointment has a deterministic calculated amount.

---

# 10. Phase 8 — Payment

## Goal

Allow the customer to pay for an appointment.

## Initial MVP Scope

- Payment Intent
- appointment/payment relationship
- amount
- currency
- payment status
- Paid
- Failed
- Refunded
- idempotent payment handling
- provider abstraction

A mock provider may be used before introducing a real payment gateway.

## Exit Condition

The product can determine whether an appointment payment has succeeded or failed without treating the payment provider as the source of business truth.

---

# 11. Phase 9 — Deposit

## Goal

Support salons that require an advance payment before final appointment confirmation.

## Initial MVP Scope

- deposit required flag/policy
- fixed deposit
- percentage deposit
- payment-before-confirmation rule
- remaining balance tracking

## Exit Condition

The salon can require and verify a deposit before confirming an appointment.

---

# 12. Phase 10 — Customer Profile

## Goal

Provide a useful customer-facing history and business relationship view.

## Initial MVP Scope

- appointment history
- upcoming appointments
- prior services
- payment history
- basic customer notes where appropriate

## Future Extensions

- favorite staff
- preferences
- loyalty
- treatment/service notes
- customer segmentation

Sensitive or health-related information must have an explicitly approved domain/security model before being introduced.

## Exit Condition

The customer can review their current and historical relationship with the salon.

---

# 13. Phase 11 — Notifications

## Goal

Communicate important appointment events.

## Initial MVP Scope

- booking confirmation
- cancellation confirmation
- appointment reminder
- payment confirmation if required

Suggested first delivery channel:

- SMS

Future channels:

- Email
- Push
- Telegram
- WhatsApp where supported

## Exit Condition

Important appointment lifecycle events reliably create a delivery request through the communication/notification capability.

---

# 14. Phase 12 — Customer Website

## Goal

Deliver the complete customer booking experience.

## Initial MVP Scope

- salon public page
- business information
- service list
- service details and price
- staff selection
- date/time selection
- booking
- payment
- booking confirmation
- login/profile
- view appointments
- cancel/reschedule where allowed

## Exit Condition

A customer can complete the primary salon journey without staff intervention.

---

# 15. Phase 13 — Admin Panel

## Goal

Allow salon operators to manage the business.

## Initial MVP Scope

- Dashboard
- Business Profile
- Services
- Categories
- Staff
- Staff-Service assignment
- Working schedules
- Appointments
- Customers
- Payments

## Exit Condition

A salon owner/manager can operate the MVP product through one administrative interface.

---

# 16. Phase 14 — Reports

## Goal

Provide basic operational and financial insight.

## Initial MVP Scope

- appointment count
- daily revenue
- monthly revenue
- revenue by service
- revenue by staff
- cancellation count
- no-show count if available

## Future Extensions

- utilization
- retention
- repeat customers
- customer lifetime value
- staff productivity
- margin analysis

## Exit Condition

The business can answer basic operational and revenue questions from system data.

---

# 17. Phase 15 — Staff Commission and Business Finance

## Goal

Support compensation and internal settlement models used by salons.

Potential models:

- fixed monthly salary
- service commission
- product-sales commission
- chair/space rental
- partner/profit share

## Initial MVP Direction

This phase should not reuse one generic Role entity for salary, partnership, investment, customer, and authorization.

Instead, employment, staff compensation, partnership, and financial settlement should be modeled as distinct business relationships/policies.

## Exit Condition

The salon can calculate a defined staff compensation/commission model from completed business activity.

---

# 18. Phase 16 — Commerce and Inventory

## Goal

Allow the salon to sell products in addition to services.

Examples:

- shampoo
- hair care
- skin care
- nail products
- cosmetics

## Candidate Capabilities

- Product
- Product Category
- Catalog
- Inventory
- Stock
- Sale
- Order
- Payment integration
- supplier/purchase extensions

## Exit Condition

The same Business can operate Service and Commerce capabilities without becoming two unrelated systems.

---

# 19. Recommended MVP Delivery Sequence

The recommended sequence is:

## Phase A — Foundation

1. Identity / Registration
2. Business Setup

## Phase B — Service Model

3. Service Catalog
4. Staff / Service Provider

## Phase C — Scheduling

5. Availability
6. Appointment / Reservation

## Phase D — Money

7. Pricing
8. Payment
9. Deposit

## Phase E — Product Experience

10. Customer Profile
11. Notifications
12. Customer Website
13. Admin Panel

## Phase F — Business Operations

14. Reports
15. Staff Commission / Finance

## Phase G — Expansion

16. Commerce / Inventory

---

# 20. Minimum Usable Salon Product

The smallest meaningful production-oriented product flow is:

Register / Login
-> Salon
-> Services
-> Staff
-> Availability
-> Appointment
-> Pricing
-> Payment
-> Confirmation

This flow gives a real customer the ability to:

1. create an account
2. discover the salon
3. choose a service
4. choose a provider/time
5. reserve the appointment
6. pay
7. receive confirmation

Everything beyond this should extend that flow rather than redesign it.

---

# 21. SmartCore Reuse Goal

The salon solution must be designed so that the reusable platform capabilities can later support other service businesses.

For example:

Beauty Salon
-> Service + Staff + Appointment

Clinic
-> Service + Provider + Appointment

Mechanic
-> Service + Technician + Appointment + Resource + Commerce + Inventory

Consulting
-> Service + Consultant + Appointment + Finance

Home Services
-> Service + Provider + Scheduling + Location + Payment

Therefore business-specific semantics should stay in ServiceBusiness/domain layers while reusable scheduling, reservation, finance, identity, communication, and resource capabilities remain platform-level.

---

# 22. Detailed MVP Specification Process

After this roadmap is accepted, each phase should receive a separate MVP specification containing at least:

- Objective
- In Scope
- Out of Scope
- Actors
- Entities / Value Objects
- Aggregate boundaries
- Commands
- Queries
- Events
- APIs
- authorization rules
- validation rules
- data ownership
- external dependencies
- failure scenarios
- acceptance criteria
- test scenarios
- migration/compatibility notes where applicable

Implementation should follow the approved MVP specification rather than allowing API/database design to define the architecture implicitly.

---

# 23. Open Architecture Questions

Before or during detailed MVP work, the following boundaries require confirmation:

1. Exact ownership of generic Business between SmartCoreBusiness and SmartCoreServiceBusiness.
2. Formal relationship between Appointment and Reservation.
3. Whether Scheduling is its own platform capability.
4. Exact ownership of Staff business relationships.
5. Service pricing ownership versus generic Pricing capability.
6. Customer relationship ownership in ServiceBusiness.
7. Payment versus Finance versus Billing boundaries.
8. Whether deposit is a Payment policy, Booking policy, or both through explicit contracts.
9. Resource requirements for salon services, chairs, rooms, equipment, and staff.
10. Notification event ownership and communication delivery contracts.

These should be settled incrementally as each MVP is specified.

---

## 24. Status

This roadmap is intentionally non-normative.

It is a delivery and architecture-planning document intended to guide the detailed MVP specifications for the first SmartCoreServiceBusiness-based beauty salon solution.

Any change to canonical platform ownership, taxonomy, or architecture must follow SmartCore governance and ADR requirements.
