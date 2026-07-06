# SmartCore Platform

## Document 021 — Value & Economic Semantics

Version: 1.0
Status: Core Architecture Spec

---

# 1. Purpose

این سند تعریف می‌کند:

- Value چیست
- Money چگونه در مدل SmartCore معنا پیدا می‌کند
- Ownership چه معنایی دارد
- Ledger چگونه Value را تبدیل به Event می‌کند

هدف:

> ساخت یک اقتصاد semantic-first، نه account-based

---

# 2. Core Principle

> Value is not stored. Value is inferred from Events.

---

# 3. Value Definition

Value یک Semantic Construct مستقل نیست.

Value = semantic interpretation of change in state over time

```
Value := Δ(State over Time)
``` id="v1"

---

# 4. Value is Derived, not a Core Semantic Construct

Value از هیچ‌کدام از این‌ها مستقل نیست:

- Thing
- Relation
- Event
- Rule

Value فقط نتیجه‌ی تعامل آن‌هاست.

---

# 5. Economic Event

Economic Event یک Occurrent است که:

- باعث تغییر Ownership می‌شود
- یا Value را منتقل می‌کند
- یا Commitment را settle می‌کند

```
EconomicEvent ⊂ Occurrent
``` id="v2"

---

# 6. Ownership Model

Ownership یک Relation است، نه Property.

```
owns(A, B) := Relation(A, B, Rule)
``` id="v3"

ویژگی‌ها:

- قابل انتقال است
- قابل تقسیم است
- قابل محدودسازی توسط Rule است

---

# 7. Value Transfer

Value همیشه از طریق Event منتقل می‌شود:

```
Event:
    Transfer(Value, from: A, to: B)
``` id="v4"

هیچ انتقال Value بدون Event وجود ندارد.

---

# 8. Money Definition

Money یک Entity نیست.

Money = standardized representation of Value

```
Money := Tokenized Value Unit
``` id="v5"

---

# 9. Ledger Model

Ledger فقط یک projection از Event stream است.

Ledger ≠ source of truth

Ledger = derived state

```
Ledger = Fold(EconomicEvents)
``` id="v6"

---

# 10. Account Model Rejection

SmartCore does NOT use accounts as core semantic constructs.

Instead:

- Accounts = derived views over Ownership relations
- Balances = computed projections

---

# 11. Pricing Model

Price is not stored.

Price is a Rule applied to Value exchange:

```
Price = Rule(Context, Time, Relation)
``` id="v7"

---

# 12. Transaction Model

A Transaction is a bounded set of Events:

- initiation Event
- validation Event
- settlement Event

Transaction is not a single object.

---

# 13. Commitment Model

Commitment is a future Economic Event expectation.

```
Commitment := Deferred EconomicEvent
``` id="v8"

---

# 14. Settlement Model

Settlement is the point where:

- Commitment becomes Economic Event
- Value transfer becomes final

---

# 15. Reversibility

Economic Events are NOT deleted.

They are reversed:

```
ReversalEvent cancels EconomicEvent
``` id="v9"

---

# 16. Multi-Party Value Flow

Value transfer is not binary.

It may involve:

- multiple parties
- splits
- chained distributions

Represented as Event graph.

---

# 17. Temporal Dependency

All Value has Time dependency:

- when value is created
- when value is recognized
- when value is settled

No Value exists outside Time Model (020).

---

# 18. Security Dependency

Economic operations depend on:

- Identity (019)
- Permission (018)
- Event ordering (020)

Not on static account rules.

---

# 19. Key Insight

> Value is not a thing.
> Value is a relationship over time between state transitions.

---

# 20. Relationship to Previous Documents

- 019 Identity → who participates in Value flow
- 020 Time → when Value is realized
- 017 Failure → how economic events are recovered
- 018 Security → who can trigger Value changes

---

End of Document 021