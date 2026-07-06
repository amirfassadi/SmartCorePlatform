# SmartCore Capability Model

Version: 1.0

Status: Core Semantic Standard

---

# 1. Purpose

This document defines the semantic meaning of Capability within SmartCore.

A Capability represents the potential ability of a semantic construct to perform, support or enable one or more actions.

Capability is neither an Event nor a State.

It represents potential, not execution.

This specification is technology-independent.

---

# 2. Definition

A Capability is an intrinsic or acquired semantic ability possessed by a Thing.

Capabilities describe what a Thing can do.

They do not describe what the Thing is currently doing.

Examples

Person

- Drive
- Approve Expense
- Operate CNC Machine

Machine

- Drill
- Mill
- Weld

Door

- Lock
- Unlock
- Open

Organization

- Manufacture Products
- Issue Invoices
- Employ People

---

# 3. Core Principle

Capability represents possibility.

Events represent execution.

State represents condition.

---

# 4. Capability Ownership

Every Capability belongs to exactly one Thing.

Capabilities never exist independently.

Examples

Robot

Capability

Pick Object

Vehicle

Capability

Transport Cargo

Printer

Capability

Print Document

---

# 5. Capability vs Event

Capability

Can print.

Event

Printed Document #123.

Capability exists before execution.

Events realize Capabilities.

---

# 6. Capability vs State

Capability

Can open door.

State

Door is open.

A Capability may exist even when never exercised.

---

# 7. Capability vs Rule

Rules govern Capabilities.

Example

Capability

Approve Purchase

Rule

Only Managers may exercise this Capability.

Rules constrain usage.

They do not create Capability.

---

# 8. Capability Acquisition

Capabilities may be:

Intrinsic

Examples

Human can breathe.

Motor can rotate.

Acquired

Examples

Employee receives approval rights.

Robot receives new software module.

Machine receives new tooling.

---

# 9. Capability Removal

Capabilities may be removed.

Examples

License revoked.

Permission removed.

Hardware detached.

Software module uninstalled.

Removing a Capability does not necessarily affect Identity.

---

# 10. Capability Composition

Complex Capabilities may be composed of simpler Capabilities.

Example

Manufacture Product

↓

Cut Material

↓

Mill Component

↓

Inspect Part

↓

Assemble Product

Composition does not create new core semantic constructs.

---

# 11. Capability Dependencies

A Capability may depend on:

Other Capabilities

Specific States

Relations

Rules

Resources

Example

Capability

Start Machine

Requires

Machine = Ready

Operator Authorized

Power Available

---

# 12. Capability Enablement

Possessing a Capability does not imply that it is currently enabled.

Example

A vehicle may be capable of autonomous driving but disabled by policy.

Capability and availability are distinct concepts.

---

# 13. Capability Granularity

Capabilities may exist at multiple levels.

Examples

Generic

Communicate

Specialized

Send Email

Send SMS

Publish MQTT Message

The Core defines no mandatory hierarchy.

---

# 14. Capability Discovery

Capabilities should be discoverable through semantic inspection.

Consumers should be able to ask:

"What can this Thing do?"

without understanding implementation details.

---

# 15. Capability Evolution

Capabilities may evolve over time.

Examples

Software update introduces new functions.

Machine retrofit enables new operations.

Organization expands into new services.

Identity remains unchanged.

Capabilities evolve.

---

# 16. Capability Representation

Capability names belong to the Vocabulary Layer.

Examples

Print

Scan

Reserve

Approve

Unlock

Charge

The Core defines the structure.

Domains define the vocabulary.

---

# 17. Capability Validation

Before using a Capability, systems may evaluate:

Rules

Current State

Relations

Available Resources

Time Constraints

Capability itself remains unchanged.

---

# 18. Capability vs Permission

Capability answers:

"Can this Thing perform this type of action?"

Permission answers:

"Is this Thing currently allowed to perform this action?"

Capability is potential.

Permission is authorization.

---

# 19. Capability vs Resource

Resources enable Capabilities.

Capabilities consume or utilize Resources.

Example

Capability

Print

Requires

Paper

Ink

Printer

Electricity

Capability is not the Resource.

---

# 20. Architectural Principles

Capabilities belong to the Semantic Layer.

They are:

Owned by Things

Independent of implementation

Governed by Rules

Realized through Events

Observable through behavior

---

# 21. Validation Checklist

Before introducing a Capability ask:

Does it represent potential rather than execution?

Can it exist without being exercised?

Is it owned by a Thing?

Is it constrained by Rules rather than replacing them?

If yes,

it belongs in the Capability Model.

---

# 22. Final Principle

Capabilities define what Things are able to do.

Events record what Things actually did.

States describe the current condition of Things.

Rules determine when Capabilities may be exercised.

Together they provide a complete semantic description of behavior.

---

## END OF DOCUMENT