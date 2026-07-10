# SmartCore Core Vocabulary
Version: 1.0

Status: Draft

---

# Purpose

This document defines the first version of the SmartCore Core Vocabulary.

Unlike the Semantic Grammar (Continuant, Occurrent, Relation, Rule, Time),
this document does NOT define core semantic constructs.

Instead, it defines the first reusable concepts that every SmartCore
application may use.

These concepts are intentionally technology-independent,
domain-independent whenever possible,
and validated against the SmartCore Semantic Grammar.

---

# Vocabulary Layers

The vocabulary is divided into four levels.

Level 0
Semantic Grammar

Level 1
Universal Concepts

Level 2
Cross-domain Concepts

Level 3
Domain Concepts

Only Level 1 and Level 2 belong in this document.

---

# Level 0 (Reference)

Continuant

Occurrent

Relation

Rule

Time

These are defined in:

001_SmartCore_Foundational_Principles.md

002_SmartCore_Meta_Model.md


---

# Level 1 — Universal Concepts

These concepts are expected to exist in almost every software system.

---

## Person

Category

Continuant

Description

Represents a natural human being.

Examples

Customer

Employee

Citizen

Tenant

Driver

Student

Owner

Derived From

Continuant

---

## Organization

Category

Continuant

Description

Represents a legal or logical collective of persons.

Examples

Company

Government

School

Hospital

Club

Association

Derived From

Continuant

Rule

Relation

---

## Device

Category

Continuant

Examples

Sensor

Camera

Door Lock

Gateway

Printer

POS

Router

Machine

Derived From

Continuant

---

## Asset

Category

Continuant

Description

Anything that may be owned,
managed,
reserved,
tracked,
or monetized.

Examples

House

Vehicle

Machine

Room

Parking Space

Money

Inventory

Subscription

Derived From

Continuant

Relation

---

## Location

Category

Continuant

Examples

Country

City

Building

Floor

Room

Zone

GPS Point

Derived From

Continuant

---

## Document

Category

Continuant

Description

Represents persistent information.

Examples

Invoice

Contract PDF

Receipt

Certificate

Report

Drawing

Image

Derived From

Continuant

Relation

---

## Event

Category

Occurrent

Examples

Payment

Login

Purchase

Door Open

Temperature Change

Birth

Death

Reservation Started

Derived From

Occurrent

---

## Action

Category

Occurrent

Description

Event intentionally initiated by an Agent.

Examples

Approve

Reject

Pay

Reserve

Transfer

Derived From

Occurrent

Rule

---

## Measurement

Category

Occurrent

Description

Observation produced by a device or actor.

Examples

Temperature Reading

Humidity Reading

Voltage Reading

GPS Reading

Derived From

Occurrent

Relation

---

# Level 2 — Cross Domain Concepts

These concepts appear in many domains but are still composed from Level 0 semantic constructs.

---

## Contract

Composition

Relation

Rule

Time

Examples

Employment

Rental

Subscription

Insurance

Warranty

Supplier Agreement

---

## Membership

Composition

Relation

Rule

Time

Examples

Gym Membership

Association Membership

Club Member

VIP Membership

---

## Reservation

Composition

Relation

Rule

Time

Examples

Room Reservation

Machine Reservation

Parking Reservation

Court Reservation

---

## Ownership

Composition

Relation

Time

Examples

Own Vehicle

Own Building

Own Wallet

Own Device

---

## Assignment

Composition

Relation

Time

Examples

Assign Employee

Assign Machine

Assign Ticket

Assign Role

---

## Permission

Composition

Rule

Relation

Examples

Door Access

API Permission

Admin Rights

Edit Permission

---

## Identity

Composition

Continuant

Rule

Examples

Passport

National ID

Employee Number

Customer Number

Device Serial

---

## Wallet

Composition

Continuant

Relation

Rule

Examples

Cash Wallet

Reward Wallet

Crypto Wallet

Gift Wallet

---

## Ledger

Composition

Continuant

Relation

Rule

Examples

Accounting Ledger

Inventory Ledger

Carbon Ledger

Reward Ledger

---

## Schedule

Composition

Rule

Time

Examples

Working Hours

Opening Hours

Production Calendar

Maintenance Plan

---

## Workflow

Composition

Rule

Occurrent

Time

Examples

Purchase Flow

Approval Flow

Manufacturing Flow

Complaint Flow

---

## Notification

Composition

Occurrent

Relation

Examples

Email

SMS

Push

Telegram

Webhook

---

## Attachment

Composition

Relation

Document

Examples

Invoice Attachment

Image

Drawing

CAD File

PDF

---

## Tag

Composition

Relation

Examples

Urgent

VIP

Finance

Production

Maintenance

---

## Comment

Composition

Relation

Document

Examples

Internal Note

Customer Note

Audit Comment

---

## Audit Record

Composition

Occurrent

Document

Time

Examples

Created

Updated

Deleted

Approved

Rejected

---

# Vocabulary Evolution Rules

A concept may be added only if:

- it appears in multiple independent domains

- it cannot be reduced without losing meaning

- it survives the Validation Matrix

- it remains technology independent

Otherwise it belongs to Domain Vocabulary.

---

# Examples of Domain Vocabulary

Finance

Invoice

Payment

Refund

Debt

Credit

Interest

ERP

Work Order

Purchase Order

Production Order

Material Request

CRM

Lead

Opportunity

Campaign

Referral

IoT

Sensor

Alarm

Automation

Rule Engine

Smart Device

Healthcare

Patient

Prescription

Diagnosis

Treatment

---

# Vocabulary Review Checklist

Every new concept must answer:

Is it reusable?

Can it be composed?

Does it introduce a new core semantic construct?

Is it technology independent?

Does it belong in Core?

Can Biology use it?

Can Finance use it?

Can IoT use it?

If not,

it belongs in a higher layer.

---

# Goal

The purpose of the Core Vocabulary is not to describe every business concept.

Its purpose is to provide a stable language that every SmartCore domain can extend without modifying the semantic foundation.

This document is expected to evolve slowly and remain stable over the lifetime of the platform.

---

## END OF DOCUMENT