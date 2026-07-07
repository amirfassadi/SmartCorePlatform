Version: 1.0

Status: Draft

---

# 1. Purpose

This document defines the responsibilities and architectural boundaries of SmartCore Core Engines.

---

# 2. Definition

A Core Engine is a reusable platform service that provides generic behavior to Capability Platforms.

Core Engines SHALL NOT contain business knowledge.

---
# 3. Core Engines

The SmartCore Platform defines the following foundational Core Engines.

| Engine | Responsibility |
|---------|----------------|
| Policy Engine | Evaluate configurable platform policies. |
| Rule Engine | Execute generic rule evaluation independent of domain semantics. |
| Event Engine | Publish, route, and consume platform events. SHALL NOT interpret business meaning or execute domain logic. |
| Workflow Engine | Coordinate long-running workflows and process execution. |
| Scheduler | Execute time-based operations. |
| Messaging Engine | Deliver asynchronous platform messages. |

Additional Core Engines MAY be introduced in future platform versions provided they satisfy the requirements defined in this document.

Every Core Engine SHALL satisfy all of the following characteristics:

- domain independent
- reusable by multiple Capability Platforms
- stable and technology-agnostic
- replaceable without changing business semantics
- free of capability-specific knowledge
---

# 4. Boundary Rules

Core Engines SHALL:

- remain domain independent
- expose stable contracts
- be reusable
- never depend on Capability Platforms

---

# 5. Capability Platform Composition

Capability Platforms compose Core Engines in order to implement business capabilities.

Core Engines provide generic technical behavior.

Capability Platforms provide domain semantics.

Application Services SHALL orchestrate execution.

Domain Services SHALL enforce intrinsic domain rules.

Policy Engines SHALL evaluate configurable policies.

Rule Engines SHALL execute reusable rule-processing logic that remains independent of any specific business domain.

The responsibilities SHALL therefore remain clearly separated.

| Component | Responsibility |
|-----------|----------------|
| Application Service | Orchestrate workflows and coordinate execution |
| Domain Service | Enforce intrinsic domain rules and cross-aggregate business invariants |
| Policy Engine | Evaluate configurable policies |
| Rule Engine | Execute reusable generic rule-processing logic independent of business semantics |
| Core Engine | Provide reusable platform infrastructure |

Application Services MAY invoke one or more Core Engines.

Domain Services SHALL NOT invoke Core Engines directly.

Core Engines SHALL NOT contain business semantics.

A typical execution flow is illustrated below.

```
Command
      ↓
Application Service
      ↓
Load Aggregates
      ↓
Policy Engine (optional)
      ↓
Domain Service
      ↓
Aggregate
      ↓
Domain Events
      ↓
Event Engine
      ↓
Workflow Engine (optional)
      ↓
Messaging Engine / Scheduler (optional)
```

This sequence illustrates responsibility boundaries rather than a mandatory execution order.

Not every use case requires every Core Engine.

Application Services remain responsible for orchestration throughout the execution lifecycle.
---

# 6. Policy Engine and Rule Engine

The Policy Engine evaluates configurable policies.

Policies represent behavior that administrators, tenants, or configuration MAY change without modifying application source code.

Typical examples include:

- authorization policies
- configurable approval rules
- configurable access restrictions
- configurable operational limits

The Rule Engine executes reusable generic rule-processing mechanisms.

It provides reusable evaluation algorithms that remain independent of any business domain.

Typical examples include:

- expression evaluation
- rule execution pipelines
- decision evaluation frameworks
- reusable rule-processing infrastructure

The Rule Engine SHALL NOT contain business-specific decision logic.

Neither engine SHALL own domain state.

Neither engine SHALL enforce intrinsic domain invariants.

Intrinsic business rules belong exclusively to Domain Services.

The following practical test SHALL be applied.

If changing a rule requires modifying application source code, the rule belongs to the domain model.

If changing a rule SHOULD be possible through configuration, the rule belongs to the Policy Engine.

This distinction SHALL be applied consistently across all Capability Platforms.
---
# 7. Engine Selection Principles

Capability Platforms SHALL select Core Engines according to the architectural responsibility of the problem being solved, rather than implementation convenience.

Choosing an incorrect Core Engine introduces architectural drift, reduces consistency across Capability Platforms, and weakens platform interoperability.

The following decision guide SHALL be used.

| Question | Correct Component |
|-----------|-------------------|
| Does the behavior represent an intrinsic business invariant that is part of the domain model? | Domain Service |
| Should the behavior be configurable without changing application source code? | Policy Engine |
| Is the behavior reusable generic logic independent of business concepts? | Rule Engine |
| Does the behavior coordinate application workflows or use-case execution? | Application Service |
| Does the behavior orchestrate long-running processes? | Workflow Engine |
| Does the behavior publish, route, or consume events? | Event Engine |
| Does the behavior execute according to time or schedule? | Scheduler |
| Does the behavior deliver asynchronous communication? | Messaging Engine |

The following principles SHALL always apply.

- Business invariants SHALL remain inside Domain Services.
- Configurable behavior SHALL be evaluated by the Policy Engine.
- Generic reusable rule execution SHALL be delegated to the Rule Engine.
- Application Services SHALL orchestrate execution but SHALL NOT contain business rules.
- Core Engines SHALL remain domain independent.

The following practical decision rule SHOULD be applied during design.

- If modifying the behavior requires changing application source code, it represents domain logic and SHALL remain within the Capability Platform.
- If modifying the behavior SHOULD be possible through configuration, the behavior SHALL be implemented as a policy.
- If the behavior is reusable across multiple Capability Platforms without knowledge of domain concepts, it MAY be implemented by a Core Engine.

The architecture SHALL favor clear responsibility boundaries over implementation convenience.
----

# 8. Engine Interaction Principles

Core Engines MAY collaborate with one another where required by platform infrastructure.

Capability Platforms SHALL orchestrate such collaboration through their Application Services.

Core Engines SHALL remain unaware of business workflows and SHALL NOT coordinate domain processes.

Examples of valid collaboration include:

- Scheduler → Event Engine
- Workflow Engine → Messaging Engine
- Workflow Engine → Event Engine
- Messaging Engine → Event Engine

Such collaboration SHALL remain purely technical.

Business decisions SHALL always remain within Capability Platforms.

Core Engines SHALL communicate only through their published contracts.

No Core Engine SHALL depend upon capability-specific knowledge or domain semantics.
----

# 9. Dependency Rule

```
Capability

↓

Core Engine

↓

Shared
```

Reverse dependencies are forbidden.

---

# 10. Examples

Allowed

```
Identity Platform

↓

Policy Engine
```

Forbidden

```
Policy Engine

↓

Identity Platform
```

---

# 11. Final Principles

Core Engines exist to provide reusable platform capabilities.

Business semantics SHALL remain inside Capability Platforms.

Application Services orchestrate execution.

Domain Services enforce intrinsic business rules.

Policy Engines evaluate configurable policies.

Rule Engines execute reusable generic rule-processing logic.

Event Engines transport events but SHALL NOT interpret business meaning.

Core Engines SHALL remain completely independent of business concepts.

Capability Platforms SHALL depend on Core Engines.

Core Engines SHALL NEVER depend on Capability Platforms.

The architecture SHALL preserve this dependency direction throughout the platform lifecycle.

Correct engine selection is an architectural responsibility and SHALL take precedence over implementation convenience.
---

END OF DOCUMENT