# 058_SmartCore_Foundation_MVP.md

Version: 1.0

Status: **Normative**

---

# 1. Purpose

This document defines the **Minimum Viable Platform (MVP)** for SmartCore.

The objective of the MVP is **not** to implement every planned platform.

Its objective is to establish a stable technical foundation upon which every future SmartCore Platform can be built.

The MVP shall validate the architecture through the implementation of a real IoT scenario.

---

# 2. Goals

The MVP SHALL:

* Validate the SmartCore Foundation.
* Validate the Organization-centric ownership model.
* Validate authentication and identity.
* Validate the application architecture.
* Validate the API architecture.
* Validate device management.
* Validate real communication with IoT devices.

The MVP SHALL remain intentionally small.

---

# 3. Scope

The MVP includes only the components required to support a functional IoT system.

Included:

* Identity Foundation
* Organization Foundation
* Membership Foundation
* Authentication
* Session Management
* Device Foundation
* API Foundation
* Event Recording
* Basic Audit Logging

Excluded:

* Finance
* Manufacturing
* Reservation
* CRM
* ERP
* Marketplace
* Notification Engine
* Workflow Engine
* Rule Engine
* Billing
* Payment
* Reporting

---

# 4. MVP Architecture

The implementation follows the SmartCore architecture.

```text
SFMM

↓

Platform Architecture

↓

Foundation MVP

↓

IoT Platform Validation
```

The MVP validates the architecture rather than the business domains.

---

# 5. Foundation Components

The MVP consists of the following foundational modules.

## Identity Foundation

Responsible for:

* Person registration
* Authentication
* Session management
* Identity retrieval

This module does not include advanced identity providers.

---

## Organization Foundation

Responsible for:

* Organization creation
* Personal Organization creation
* Organization retrieval

Every registered Person receives a Personal Organization automatically.

---

## Membership Foundation

Responsible for:

* Connecting Persons to Organizations.
* Defining organizational participation.

Version 1.0 supports only one role:

* Owner

Future roles are outside MVP scope.

---

## Device Foundation

Responsible for:

* Device registration
* Device ownership
* Device status
* Device connectivity

The MVP validates communication with physical IoT devices.

---

## API Foundation

Responsible for:

* Public REST API
* Authentication endpoints
* Device endpoints
* Organization endpoints

The API is independent from presentation technologies.

---

# 6. Registration Flow

Registration SHALL execute as one atomic transaction.

```text
Register Request

↓

Create Person

↓

Create Personal Organization

↓

Create Owner Membership

↓

Commit

↓

Return Authentication Result
```

Partial registration is prohibited.

---

# 7. Authentication

Version 1.0 supports only:

* Email
* Mobile Number
* Password

Future versions may introduce:

* Google
* Apple
* Telegram
* Microsoft
* OAuth
* SAML
* Enterprise SSO

Authentication providers SHALL NOT change the domain model.

---

# 8. Authorization

Authorization is intentionally minimal.

The MVP recognizes only one organizational role:

* Owner

Complex authorization policies are deferred.

The future Rule Engine will replace this simplified implementation without changing the data model.

---

# 9. Database Strategy

The database SHALL be designed for long-term extensibility.

Entity schemas may contain fields that are not immediately exposed by the API.

Example:

The Person entity may support:

* Full Name
* Birth Date
* National Identifier
* Avatar
* Language
* Time Zone
* Address
* Emergency Contact

while the registration API initially requires only:

* Name
* Email
* Mobile Number
* Password

This minimizes future schema changes while keeping the user experience simple.

---

# 10. IoT Validation Scenario

The MVP is considered successful when the following scenario is completed.

1. Register a new Person.
2. Automatically create a Personal Organization.
3. Automatically create the Owner Membership.
4. Authenticate successfully.
5. Register an ESP32 device.
6. Connect the device.
7. Send a command to the device.
8. Turn a relay ON.
9. Turn a relay OFF.
10. Record the operation as an event.

Successful completion validates the SmartCore foundation.

---

# 11. Deferred Features

The following capabilities are intentionally postponed.

* Multiple organizations
* Multiple memberships
* Invitation system
* Team collaboration
* Fine-grained permissions
* Rule Engine
* Workflow Engine
* Finance
* Reservation
* Manufacturing
* Messaging
* Notification
* Billing
* Payment
* Analytics

These features SHALL build upon the MVP foundation without requiring architectural redesign.

---

# 12. Exit Criteria

The Foundation MVP is complete when all of the following conditions are satisfied.

✓ Person registration works.

✓ Authentication works.

✓ Personal Organization is created automatically.

✓ Membership is created automatically.

✓ Device registration works.

✓ Device authentication works.

✓ REST API functions correctly.

✓ ESP32 successfully communicates with the platform.

✓ Relay control succeeds.

✓ Events are recorded.

No additional functionality is required before beginning the IoT Platform.

---

# 13. Relationship to Future Platforms

This MVP establishes the common infrastructure for:

* SmartCore IoT
* SmartCore Finance
* SmartCore Manufacturing
* SmartCore Business
* SmartCore Communication
* SmartCore Resource
* SmartCore Reservation

Future platforms SHALL extend this foundation rather than replacing it.

---

# 14. Final Statement

The SmartCore Foundation MVP is the first executable implementation of the SmartCore architecture.

Its purpose is to validate the architectural principles through a focused IoT implementation while preserving a stable foundation for future platform expansion.

---

**END OF DOCUMENT**
