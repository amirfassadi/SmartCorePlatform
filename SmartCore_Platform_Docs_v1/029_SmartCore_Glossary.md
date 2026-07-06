# 029_SmartCore_Glossary.md

# SmartCore Platform
## Glossary
Version: 1.0

---

# Purpose

This document defines the official vocabulary of SmartCore.

Every architectural document,
domain model,
API,
database schema,
and source code should use these definitions consistently.

Whenever ambiguity exists,
this glossary is the single source of truth.

---

# Thing

Anything that exists and has an identity.

Examples

- Person
- Organization
- Device
- Door
- Wallet
- Contract
- Invoice

A Thing may participate in Relations,
may own Properties,
and may participate in Events.

---

# Continuant

A Thing that exists through time.

Examples

- Person
- Building
- Device
- Vehicle
- Wallet

A Continuant may change its state without changing its identity.

---

# Occurrent

A Thing that represents something that happened.

Examples

- Payment
- Birth
- Login
- Temperature Reading
- Door Opened
- Reservation Started

An Occurrent has:

- timestamp
- participants
- facts

An Occurrent never changes after completion.

---

# Relation

A semantic connection between Things.

Examples

owns(Person, Wallet)

worksFor(Person, Organization)

locatedIn(Device, Building)

assignedTo(Task, Employee)

---

# Predicate

The semantic meaning of a Relation.

Examples

owns

uses

contains

controls

reportsTo

installedIn

---

# Property

A descriptive attribute of a Thing.

Examples

name

temperature

color

status

batteryLevel

serialNumber

---

# Property Assignment

Assignment of a Property to a Thing.

Examples

Battery = 82%

Temperature = 25°C

Status = Online

Properties may change over time.

---

# Rule

A business constraint.

Rules define what is allowed,
required,
or prohibited.

Examples

Maximum reservation duration

Employee must belong to one organization

Wallet balance cannot become negative

---

# Constraint

A Rule that limits valid states.

Examples

Age >= 18

Capacity > 0

Unique Email

---

# Policy

A configurable collection of Rules.

Examples

Refund Policy

Pricing Policy

Attendance Policy

Security Policy

---

# Capability

Something a Thing can potentially perform.

Examples

Door can open

Wallet can receive payment

Sensor can measure temperature

Person can approve invoices

---

# Role

A temporary responsibility that a Thing plays.

Examples

Employee

Manager

Tenant

Landlord

Customer

Administrator

A Thing may play multiple Roles simultaneously.

---

# State

Current condition of a Thing.

Examples

Draft

Active

Completed

Cancelled

Locked

Online

---

# Lifecycle

Allowed sequence of States.

Example

Draft

↓

Pending

↓

Approved

↓

Completed

↓

Archived

---

# Event

A change that occurred in the system.

Every Event creates immutable history.

Examples

Payment Completed

Reservation Created

Employee Hired

Door Opened

---

# Action

An Event initiated intentionally by an Agent.

Examples

Approve Invoice

Unlock Door

Create Contract

---

# Agent

A Thing capable of performing Actions.

Examples

Person

Organization

Software Agent

Automation Engine

---

# Resource

A Thing that may provide value.

Examples

Money

Building

Parking Space

Machine

Meeting Room

Vehicle

---

# Asset

A Resource recognized as having measurable value.

Examples

Cash

Machine

Building

Inventory

License

---

# Value

A measurable quantity associated with a Thing.

Examples

Money

Points

Energy

Time Credit

Carbon Credit

---

# Ownership

Relation indicating control over an Asset.

Examples

Person owns Vehicle

Organization owns Machine

---

# Contract

A Thing representing formal commitments between Parties.

A Contract defines

- obligations

- permissions

- responsibilities

- validity period

---

# Commitment

A future obligation.

Examples

Salary Payment

Future Delivery

Scheduled Maintenance

Loan Repayment

---

# Obligation

Something that must happen.

Examples

Pay Rent

Deliver Goods

Complete Inspection

---

# Permission

Authorization granted by Rules.

Examples

Can Enter

Can Edit

Can Approve

Can Withdraw

---

# Reservation

Temporary exclusive allocation of a Resource.

Examples

Room Booking

Parking Reservation

Machine Reservation

---

# Session

A temporary interaction.

Examples

Login Session

Parking Session

Charging Session

Meeting Session

---

# Ledger

Immutable record of economic Events.

Ledger records facts only.

Never intentions.

Never calculations.

---

# Transaction

A completed economic Event recorded in the Ledger.

Examples

Payment

Refund

Transfer

Salary Payment

---

# Wallet

A container holding balances.

Balances are projections.

Ledger remains the source of truth.

---

# Balance

Current calculated value derived from the Ledger.

Never stored as authoritative data.

---

# Projection

A computed view generated from Events.

Examples

Wallet Balance

Inventory Count

Employee Attendance

Monthly Revenue

---

# Evidence

Information proving an Event.

Examples

Receipt

Photo

Log Entry

GPS Position

Signature

---

# Identity

Stable identifier of a Thing.

Identity never changes.

Properties may change.

Relations may change.

Identity remains.

---

# Vocabulary

The domain-specific names used inside SmartCore.

Examples

Employee

Invoice

Machine

Building

Reservation

Salary

Invoice Number

These are not core semantic constructs.

They are vocabulary built upon the SmartCore Meta Model.

---

# Core Semantic Construct Concepts

The SmartCore Foundational Meta Model consists of the following core semantic constructs.

Content

- Thing
- Relation
- Rule

Dimensions

- Time

Everything else is composed from these semantic constructs.

---

# Canonical Principle

If a concept can be fully expressed using existing semantic constructs and composition rules,

it is **not** a new core semantic construct.

Instead,

it becomes vocabulary,
a derived concept,
or a domain pattern.

This principle protects SmartCore from uncontrolled growth.

---

# End of Document