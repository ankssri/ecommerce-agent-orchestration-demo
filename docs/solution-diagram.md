# E-Commerce Support Agent Solution Diagram

```mermaid
flowchart LR
    customer[Customer / Agent User]
    ui[Web Demo UI<br/>Chat + Dashboard]
    api[Flask App / API Layer]
    orchestrator[Orchestrator Agent<br/>Intent + Routing + Guardrails]

    faq[FAQ / Cache Path<br/>Static policy answers]
    shipping[Shipping Status Path<br/>Read-only workflow]
    returns[Return / Refund Path<br/>End-to-end task workflow]

    llm[BytePlus LLM<br/>dola-seed-2-1-turbo-260628<br/>thinking=disabled]
    policy[Policy Engine<br/>Rules + confidence gate]
    human[Human Approval Gate]
    audit[Audit + Workflow Store<br/>steps, retries, idempotency, resume]

    customerMcp[Customer MCP]
    orderMcp[Order MCP]
    productMcp[Product MCP]
    shippingMcp[Shipping MCP]
    paymentMcp[Payment MCP]
    policyMcp[Policy MCP]

    customerSys[(Customer System)]
    orderSys[(Order System)]
    productSys[(Product System)]
    shippingSys[(Shipping System)]
    paymentSys[(Payment System)]
    policySys[(Policy Docs / FAQ)]

    customer --> ui
    ui --> api
    api --> orchestrator

    orchestrator --> llm
    orchestrator --> faq
    orchestrator --> shipping
    orchestrator --> returns
    orchestrator --> audit

    faq --> policy
    faq --> audit

    shipping --> policy
    shipping --> customerMcp
    shipping --> orderMcp
    shipping --> shippingMcp
    shipping --> audit

    returns --> policy
    returns --> customerMcp
    returns --> orderMcp
    returns --> productMcp
    returns --> shippingMcp
    returns --> paymentMcp
    returns --> policyMcp
    returns --> human
    returns --> audit

    customerMcp --> customerSys
    orderMcp --> orderSys
    productMcp --> productSys
    shippingMcp --> shippingSys
    paymentMcp --> paymentSys
    policyMcp --> policySys

    policy --> human
    policy --> audit
    human --> returns
    human --> audit

    audit --> ui
```

## Reading Guide

- `Customer -> UI -> API -> Orchestrator` is the main request path.
- The orchestrator uses the `BytePlus LLM` only for intent understanding and response wording.
- `FAQ / Cache Path` handles simple static questions without hitting backend systems when possible.
- `Shipping Status Path` is a reversible, read-only workflow.
- `Return / Refund Path` is the full task workflow with policy checks, MCP lookups, approval gating, and irreversible actions.
- `Policy Engine` applies confidence thresholds, policy checks, retry ceilings, and safe fallback logic.
- `Human Approval Gate` is used before risky irreversible actions when policy or confidence requires it.
- `Audit + Workflow Store` records workflow IDs, step IDs, retries, idempotency keys, and supports resume after failure.
- Each business domain is isolated behind its own `MCP`, which then connects to its own backend system.
