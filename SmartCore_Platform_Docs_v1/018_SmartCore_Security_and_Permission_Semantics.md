# SmartCore Platform
## Document 018 — Security & Permission Semantics

Version: 1.0
Status: Core Architecture Spec

---

## 1. Purpose

این سند تعریف می‌کند:

- Identity چیست
- Permission چگونه مدل می‌شود
- Access Control چگونه در SmartCore اعمال می‌شود
- چرا Security نباید وارد Core Semantic شود، اما باید از آن مشتق شود

---

## 2. Core Principle

> Security is not a standalone system — it is a semantic constraint over Relations.

یعنی:

- Security = Rule applied on Relation
- نه یک subsystem مستقل
- نه یک layer جدا از معنا

---

## 3. Identity Model

Identity در SmartCore یک Semantic Construct مستقل نیست.

### تعریف:
Identity := stable reference over Continuant or Occurrent

ویژگی‌ها:

- تغییر نمی‌کند
- قابل resolve شدن است
- می‌تواند چند Representation داشته باشد

مثال:

- PersonID
- DeviceID
- EventID

---

## 4. Actor Model

Actor = هر چیزی که بتواند در یک Event مشارکت کند
Actor ∈ {Continuant ∪ Occurrent Reference}

انواع Actor:

- Human Actor (Person)
- System Actor (Service)
- Organizational Actor (Organization)
- Derived Actor (Token / API Key / Session)

---

## 5. Permission Model

Permission یک Semantic Construct مستقل نیست.

Permission = Rule over Relation
Permission := Rule(Actor, Action, Target)

مثال:

- Ali can "pay" Invoice #123
- System can "read" SensorStream
- Employee can "approve" Expense

---

## 6. Authorization Semantics

Authorization همیشه در لحظه‌ی اجرای Event بررسی می‌شود.
EventExecution:
if Rule(Actor, Action, Target) == true
→ allow Event
else
→ emit AuthorizationFailureEvent

---

## 7. Access Control is Event-Based

هیچ Access Control static نیست.

هر تصمیم امنیتی خودش یک Event است:

- AccessGrantedEvent
- AccessDeniedEvent
- PermissionRevokedEvent

---

## 8. Role Model (Derived Concept)

Role مستقل نیست.

Role = Contextual Permission Set over Relation
Role := set of Permissions bound to Actor in Context

مثال:

- Employee Role → permission set over Organization relations
- Customer Role → permission set over Purchase relations

---

## 9. Ownership Semantics

Ownership = Special Relation with enforced permissions
owns(A, B) ⇒ A has full permission over B (unless Rule restricts)

Ownership همیشه قابل override توسط Rule است.

---

## 10. Security Inheritance Rule

Permissions do NOT propagate by inheritance.

They propagate by Relation:

- Person → Organization
- Organization → Contract
- Contract → Resource

Security flows along semantic graph.

---

## 11. Multi-Tenant Isolation

Tenant is a top-level security boundary:
∀ Event:
Event.tenant_id must match Actor.tenant_id

No cross-tenant implicit access allowed.

---

## 12. Authentication vs Authorization

### Authentication:
> Who are you? (Identity resolution)

### Authorization:
> What are you allowed to do? (Rule evaluation)

SmartCore separates them strictly.

---

## 13. Capability Model (Derived from Permissions)

Capability = Permission + Context + Time
Capability := (Permission, ValidTime, Context)

Capabilities are temporary and dynamic.

---

## 14. Security as Derived System

Security is NOT a subsystem.

It is derived from:

- Relation graph
- Rules
- Identity mapping

---

## 15. Failure in Security

Security failures are Events:

- UnauthorizedAccessAttempt
- PermissionViolationEvent
- TokenForgeryDetectedEvent

No silent rejection.

---

## 16. Key Insight

> Security is not about protecting data.
> It is about constraining semantic execution paths.

---

## 17. Relationship to Previous Documents

- 015 Runtime → executes events
- 016 Deployment → distributes execution
- 017 Failure → handles breakdown
- 018 Security → constrains execution

---

## End of Document 018