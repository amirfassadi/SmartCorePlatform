# Future Capability Note — Business Costing / Cost of Goods and Services

**Status:** Future Architecture Note / Non-Normative  
**Repository:** SmartCorePlatform

## Purpose

Record an explicit future SmartCore requirement:

> SmartCore must support calculating the real cost of goods and/or services for Businesses.

This capability is intentionally recorded now so it is not lost while the Kimia MVP is being implemented.

It is **not** part of the current Kimia Release 1 implementation scope.

## Business Need

A Business should eventually be able to determine the cost basis behind what it sells or delivers.

Depending on the domain, this may include concepts such as:

- direct material cost
- labor cost
- consumed inventory cost
- service delivery cost
- equipment/resource usage cost
- overhead allocation
- purchase cost
- wastage/loss
- discounts or adjustments that affect cost basis
- cost per Product
- cost per Service
- cost per Appointment/Job/Order
- cost by period
- gross margin / profitability derived from cost and revenue

Exact terminology and accounting semantics must be defined later.

## Example — Beauty Salon

A future Kimia example may require calculating the cost of a service from inputs such as:

```text
Hair Coloring Service
├── material consumption
│   ├── color
│   ├── oxidant
│   └── consumables
├── provider labor/commission
├── equipment/resource cost
└── allocated overhead
        ↓
Total Service Cost
        ↓
Service Revenue
        ↓
Gross Margin
```

This example is illustrative only and does not freeze the final costing model.

## Example — Commerce

For a sold Product:

```text
Purchase / Acquisition Cost
+ landed/related cost if applicable
+ inventory cost basis
→ Cost of Product Sold
```

This may later contribute to gross-margin reporting.

## Cross-Capability Relationships

Business costing may eventually consume data from several SmartCore capabilities:

```text
SmartCoreInventory
→ material / stock consumption and cost basis

SmartCoreBusinessCapability.Service
→ Service context

SmartCoreBusinessCapability.Commerce
→ Product / Order / Sale context

SmartCoreFinance
→ monetary truth and financial references

KimiaBeauty or other solutions
→ business-specific operational context
```

Potential future integrations may also include Resource, Workforce/Compensation, Manufacturing, Supply Chain, and Accounting capabilities.

## Ownership Is Deliberately Unresolved

This note does **not** decide whether costing ultimately belongs in:

- SmartCoreFinance
- a future SmartCoreAccounting capability
- a future SmartCoreCosting capability
- Business capability-specific modules
- Analytics
- or a composed model across several modules

That decision should be made after the required invariants, accounting depth, and cross-domain reuse are understood.

## Important Distinction

Cost, price, payment, and revenue are different concepts.

```text
Cost
= what the Business consumed/spent economically to deliver or sell something

Price
= what the Business asks the customer to pay

Payment
= monetary transaction state

Revenue
= recognized/business income concept
```

These concepts should not be collapsed into one field or one state model.

## Future Questions to Resolve

Before implementation, determine:

1. What exactly is the authoritative definition of "cost" in SmartCore?
2. Is costing operational, managerial-accounting, financial-accounting, or all three?
3. How are direct and indirect costs separated?
4. How is inventory valuation handled?
5. How are labor/commission costs attributed?
6. How are overheads allocated?
7. Is cost calculated per Service, Product, Appointment, Order, Job, or all of them?
8. Are historical cost snapshots required?
9. How are corrections/revaluations handled?
10. Which module owns cost calculation versus source cost data?
11. How does costing feed profitability and reporting?
12. Does the platform need COGS, cost of service, contribution margin, and gross margin as separate concepts?

## Current Action

For now:

- keep this capability on the SmartCorePlatform architecture backlog;
- do not expand Kimia Release 1 scope;
- preserve source data in current modules so future costing can consume it;
- revisit this topic before advanced reporting/accounting/profitability work.

---

> Record the cost inputs now. Decide the costing engine only when the business rules are mature enough.
