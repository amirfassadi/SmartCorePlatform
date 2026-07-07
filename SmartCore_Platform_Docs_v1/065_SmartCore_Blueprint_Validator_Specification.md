# 064 — SmartCore Blueprint Validator Specification

Version: 1.1

Status: NORMATIVE

Depends on:

- 046 Reference Architecture
- 047 Architecture & Taxonomy Layer Model
- 050 Governance
- 063 Blueprint Standard

---

# 1. Purpose

This document defines the Blueprint Validator.

The Blueprint Validator verifies that every Capability Blueprint is:

- structurally complete
- semantically consistent
- architecturally compliant
- machine-readable
- ready for AI generation

The Validator SHALL execute automatically as part of the SmartCore Developer Platform.

---

# 2. Scope

The Blueprint Validator validates:

- Blueprint package structure
- Narrative documentation
- Machine specification (YAML)
- Cross-reference consistency
- Architecture compliance
- Governance compliance
- Dependency correctness

It SHALL NOT generate code.

It SHALL NOT modify Blueprints.

---

# 3. Responsibilities

The Blueprint Validator SHALL verify:

- completeness
- consistency
- correctness
- synchronization
- readiness

It SHALL produce deterministic validation results.

---

# 4. Validation Categories

Validation is divided into seven categories.

1. Structural Validation
2. Semantic Validation
3. Contract Validation
4. Dependency Validation
5. Machine Specification Validation
6. MVP Validation
7. Quality Gate Validation

---

# 5. Structural Validation

The Validator SHALL verify:

✓ Required files exist

✓ Required sections exist

✓ Required headings exist

✓ Required references exist

✓ Version information exists

✓ Status exists

✓ Package structure matches Blueprint Standard

Missing required elements SHALL produce FAIL.

---

# 6. Semantic Validation

The Validator SHALL verify that:

Commands described in narrative
match

Commands declared in YAML

Queries described in narrative
match

Queries declared in YAML

Events described in narrative
match

Events declared in YAML

Aggregates match.

Repositories match.

Policies match.

Any mismatch SHALL produce FAIL.

---

# 7. Contract Validation

Every public capability SHALL expose a contract.

The Validator SHALL verify:

REST

Messaging

Integration Events

OpenAPI

Contract naming

Contract versioning

Missing public contracts SHALL produce FAIL.

---

# 8. Dependency Validation

Dependency direction SHALL follow:

Capability Platform

↓

Core Engines

↓

Shared Kernel

Forbidden:

Shared Kernel → Capability

Core Engine → Capability

Capability → Capability implementation

Circular references

Violations SHALL produce FAIL.

---

# 9. Machine Specification Validation

The machine specification SHALL be validated.

Checks include:

YAML syntax

Required fields

Unique identifiers

Aggregate names

Repository names

Command names

Query names

Events

Contracts

Version

Invalid YAML SHALL produce FAIL.

---

# 10. MVP Validation

The Validator SHALL verify that:

every MVP feature

is fully documented.

The MVP SHALL include:

Aggregate

Repository

Commands

Queries

Events

Contracts

Persistence

Tests

Configuration

Missing required MVP elements SHALL produce FAIL.

---

# 11. Validation Rules

The Validator SHALL enforce the following rules.

### Rule V-001

Every Aggregate SHALL define exactly one Repository interface.

Severity:

FAIL

---

### Rule V-002

Every Command SHALL define at least one resulting Event.

Severity:

FAIL

---

### Rule V-003

Every Query SHALL reference exactly one Aggregate.

Severity:

FAIL

---

### Rule V-004

Every public Command SHALL expose a Contract.

Severity:

FAIL

---

### Rule V-005

Every Event SHALL declare its owning Capability Platform.

Severity:

FAIL

---

### Rule V-006

Machine Specification SHALL match Narrative.

Severity:

FAIL

---

### Rule V-007

Repository interfaces SHALL belong to their Aggregate.

Severity:

FAIL

---

### Rule V-008

No unresolved TODO SHALL exist inside MVP scope.

Severity:

FAIL

---

### Rule V-009

Examples SHALL compile conceptually with the documented model.

Severity:

WARNING

---

### Rule V-010

Optional configuration SHOULD be documented.

Severity:

WARNING

---

### Rule V-011

External references SHOULD resolve.

Severity:

WARNING

---

### Rule V-012

Naming SHOULD follow SmartCore conventions.

Severity:

WARNING

---

# 12. Validation Severity

The Validator SHALL classify findings.

## PASS

Requirement satisfied.

Implementation may continue.

---

## WARNING

Non-blocking issue.

Blueprint remains valid.

Generation MAY continue.

Human review recommended.

---

## FAIL

Blocking issue.

Blueprint SHALL NOT enter AI Generation.

Quality Gates SHALL fail.

---

# 13. Quality Gate Evaluation

The Validator SHALL evaluate:

Gate 1

Architecture Complete

Gate 2

Blueprint Complete

Gate 3

Governance Approved

Gate 4

Validation Passed

Gate 5

Ready For Generation

If any mandatory Gate fails,

overall validation SHALL fail.

---

# 14. Validation Report

Example:

```text
Blueprint:

Identity

--------------------------------

Structural

PASS

Semantic

PASS

Contracts

PASS

Dependencies

PASS

Machine Spec

PASS

MVP

PASS

Quality Gates

PASS

Overall

PASS
```

---

# 15. Continuous Integration

The Validator SHALL execute:

before Pull Request

before Merge

before Release

before AI Generation

CI SHALL reject FAIL results.

---

# 16. Governance Integration

Validation results SHALL be attached to Governance Review.

Governance MAY reject a Blueprint despite a PASS result.

Architecture authority remains defined by:

SFMM

↓

Reference Architecture

↓

Platform Taxonomy

↓

Blueprint

Validation is an implementation gate,

not an architectural authority.

---

# 17. Extensibility

New validation rules MAY be added.

Existing FAIL rules SHALL NOT change semantics
without Governance approval.

Rule identifiers SHALL remain stable.

---

# 18. Tooling

The Blueprint Validator is a Developer Platform tool.

Possible implementation:

CLI

VSCode Extension

GitHub Action

GitLab Pipeline

Azure DevOps Task

Pre-Commit Hook

---

# 19. Output Formats

The Validator SHOULD support:

Console

JSON

HTML

Markdown

SARIF

Machine-readable output SHALL be deterministic.

---

# 20. Final Statement

The Blueprint Validator is the mandatory quality gate between Blueprint authoring and AI code generation.

Its purpose is to ensure that every Blueprint is complete, internally consistent, architecturally compliant, and ready for deterministic implementation.

Blueprint validation protects SmartCore from architectural drift and guarantees that generated implementations faithfully reflect the approved architecture.

---

END OF DOCUMENT