# SmartCore Property Model
Version: 1.0

Status: Core Semantic Standard

---

# 1. Purpose

This document defines the semantic meaning of Properties within SmartCore.

Properties describe characteristics of Things, Relations and Events.

Properties are NOT core semantic constructs.

They are semantic descriptors attached to existing semantic constructs.

This specification is technology-independent.

---

# 2. Definition

A Property represents a characteristic, quality, measurement or attribute of another semantic construct.

A Property cannot exist independently.

It always belongs to:

- Thing
- Relation
- Event

Examples

Person

- Name
- Birth Date
- Nationality

Device

- Serial Number
- Firmware Version

Employment

- Salary
- Department
- Job Title

PaymentCompleted

- Amount
- Currency
- Payment Method

---

# 3. Core Principle

A Property describes.

It never exists by itself.

---

# 4. Property Ownership

Every Property has exactly one semantic owner.

Possible owners are:

Thing

Relation

Event

Example

Thing

Car

Properties

VIN

Color

Weight

---

Relation

Employment

Properties

Salary

Department

Working Hours

---

Event

TemperatureMeasured

Properties

Temperature

Humidity

Battery Level

---

# 5. Property Structure

Conceptually:

Property

Name

Value

Value Type

Owner

Optional Unit

Optional Constraints

Optional Metadata

Example

Temperature

Name

Temperature

Value

23.4

Type

Decimal

Unit

°C

Owner

SensorReading Event

---

# 6. Property Types

Common semantic property categories include:

Identifier

Text

Boolean

Number

Enumeration

Date

Time

Duration

Money

Quantity

Reference

Collection

Complex Object

The Core does not restrict property types.

---

# 7. Property vs Thing

Thing exists independently.

Property does not.

Example

Thing

Machine

Property

Power Rating

Deleting the Property does not delete the Thing.

Deleting the Thing removes semantic meaning of the Property.

---

# 8. Property vs Relation

Relations connect Things.

Properties describe Relations.

Example

Employment

Relation

Organization ↔ Person

Properties

Salary

Position

Start Date

---

# 9. Property vs Event

Events represent occurrences.

Properties describe occurrences.

Example

PaymentCompleted

Properties

Amount

Currency

Gateway

Reference Number

---

# 10. Property vs State

Property

Battery Capacity = 5000 mAh

State

Battery Level = 82%

Capacity is an intrinsic Property.

Level is a current State.

State changes frequently.

Property usually changes rarely.

---

# 11. Property vs Rule

Rules validate Properties.

Example

Rule

Salary must be positive.

Property

Salary = 5000

Rules constrain values.

Properties store values.

---

# 12. Property Mutability

Properties may be:

Immutable

Example

VIN

Birth Date

Mutable

Example

Phone Number

Firmware Version

Display Name

Mutability is domain-defined.

---

# 13. Property Cardinality

Properties may be:

Single-valued

Name

Multi-valued

Phone Numbers

Email Addresses

Tags

Languages

Core imposes no limitation.

---

# 14. Property Constraints

Properties may define:

Minimum

Maximum

Length

Precision

Pattern

Allowed Values

Constraints are interpreted through Rules.

---

# 15. Property Units

Properties may include units.

Examples

Length

mm

cm

m

Weight

g

kg

Temperature

°C

°F

Money

USD

EUR

TRY

The Core recognizes units but does not define conversion logic.

---

# 16. Property History

Property history is not stored directly.

History is reconstructed through Events.

Example

Price

100

↓

PriceChanged Event

↓

120

↓

PriceChanged Event

↓

150

Current Property

150

History

100 → 120 → 150

---

# 17. Derived Properties

Some Properties are calculated.

Example

Invoice Total

=

Sum(Line Totals)

Example

Inventory Balance

=

Incoming

-

Outgoing

Derived Properties are semantic results.

They are not independent data.

---

# 18. Unknown Values

A Property may be:

Known

Unknown

Not Applicable

Unavailable

Estimated

These meanings are semantically distinct.

---

# 19. Property Identity

Properties do not require global identity.

Their identity is determined by:

Owner

+

Property Name

Example

Machine #25

Firmware Version

---

# 20. Property Lifecycle

Properties may evolve.

Example

Phone Number

Changed

Address

Updated

Firmware

Upgraded

The Property remains the same semantic concept.

Only its Value changes.

---

# 21. Property Validation

Validation belongs to Rules.

Examples

Email format

Positive Salary

Temperature Range

Properties never validate themselves.

---

# 22. Architectural Principles

Properties are descriptive.

Properties never:

Create behavior

Create relationships

Create events

Create identity

They only describe existing semantic constructs.

---

# 23. Validation Checklist

Before introducing a new Property ask:

Is it describing an existing semantic construct?

Can it exist independently?

Does it represent a characteristic rather than a relationship?

If yes,

it belongs to the Property Model.

---

# 24. Final Principle

Properties are semantic descriptors attached to Things, Relations and Events.

They enrich meaning without introducing new semantic identity.

Properties are derived constructs built upon the core semantic constructs of SmartCore.

---

## END OF DOCUMENT