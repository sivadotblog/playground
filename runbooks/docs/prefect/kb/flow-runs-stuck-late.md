---
title: Flow runs stuck in Late
service: prefect
owner: data-platform-engineering
last_reviewed: 2026-11-13
---

# Flow runs stuck in Late

## Symptom

Many flow runs show state Late in the UI. Scheduled start time has passed but no worker picked them up.

## Pre-checks

1. Check which work pool the late runs belong to.
2. Confirm the pool has online workers. If not, see [PrefectWorkPoolNoWorkers](../alerts/PrefectWorkPoolNoWorkers.md).

## Cause

Either no workers in the pool, workers at concurrency limit, or a pool-level concurrency limit set too low.

## Resolution

1. No workers: follow the alert playbook above.
2. Workers at limit: scale the worker deployment up temporarily.
3. Pool concurrency limit: raise it in the UI under the work pool settings. Note the previous value.
4. After runs drain, return limits to their previous values and file a ticket for the pool owner.

## Verification

Late count on the dashboard returns to zero within 10 minutes.

## Escalation

Data platform on-call secondary.

## Related

- [service README](../README.md)
