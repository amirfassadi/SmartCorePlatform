# SFMM-08 — Validation Matrix (Core Concept Test System)

## 1. Purpose

This document defines the validation system for the SmartCore semantic architecture.

Its goal is to ensure that:
- No concept is incorrectly promoted to a higher semantic status than the core layer
- All domain concepts are constructible from the core semantic model
- Semantic consistency is preserved across domains

---

## 2. Core Grammar (Frozen Set)

All validation must use only these semantic constructs:

### Semantic Layer
- Thing → entity that persists over time
- Event → occurrence that happens over time
- Relation → connection between constructs
- Rule → constraint or obligation

### Dimensional Layer
- Time → temporal overlay applied to semantic constructs

---

## 3. Key Distinction Rules

### 3.1 Thing vs Event
- Thing = continues through time
- Event = occurs at a time or interval

### 3.2 Relation Types
- evidentiary → describes an Event
- constitutive → creates or defines a relation-based fact

### 3.3 Reification Rule
An Event or Relation may be referenced through a reified form.

Important:
- Type does not change
- Only the reference layer is reified

---

## 4. Constructibility Test

A concept is valid if it can be expressed using:

> Thing + Event + Relation + Rule + Time

If not, it should be treated as vocabulary or a derived concept rather than a new core construct.

---

## 5. Validation Matrix Template

Each concept must be evaluated using the following structure:

| Concept | Type | Construction | Relation Kind | Breaks Core? | Notes |
|--------|------|--------------|---------------|--------------|------|

---

## 6. Design Principle

> The core semantic model must remain stable across all domains.
> Only composition rules, domain vocabulary, and execution adapters may evolve.
