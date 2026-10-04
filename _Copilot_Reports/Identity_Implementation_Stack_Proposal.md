# Identity implementation stack proposal

Status: engineering recommendation only; not adopted, and not permission to implement.

Recommend ASP.NET Core on .NET 10 LTS and PostgreSQL on a supported major version frozen with the deployment plan. .NET's typed contracts and async services fit the explicit Command/Query/service boundaries. PostgreSQL provides transactional updates and uniqueness for ownership and workflow races. Serializable isolation can require retries; it does not replace uniqueness constraints, idempotency or crash-recovery design.

Primary references: [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core), [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html). .NET 10 is listed as LTS with support through November 2028; verify supported database major and hosting compatibility when freezing versions.

TypeScript with a supported Node.js runtime is a viable alternative if team experience favors it. It requires the same database concurrency design and explicit runtime contract validation; TypeScript types alone do not validate network messages. Team skill and operational hosting should decide between these options rather than schema-check counts.

Prepare a repeatable local database environment, injectable clock, code-delivery test adapter, operation-specific JSON Schema validation and real-database tests for uniqueness, compare-and-set, retry and recovery. Preserve separate ownership and Credential transaction boundaries even if a development environment cohosts them; deployment topology remains an architectural decision. Initial test adapters can support approved contracts without selecting a production SMS provider, KMS or transport broker. A broker/Redis choice must follow the adopted T16/SESSION requirements.

Before implementation, close the applicable 064/065 gates, select policy/security parameters and record stack acceptance. Then build the registration delivery phase against the accepted single MVP Blueprint and versioned contracts. No runtime scaffold was created by this proposal.
