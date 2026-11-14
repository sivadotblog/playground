---
title: Prefect
service: prefect
owner: data-platform-engineering
last_reviewed: 2026-11-13
---

# Prefect

## Summary

Workflow orchestration for data pipelines. Teams deploy flows that run on schedules and trigger Databricks jobs, Snowflake loads, and quality checks.

## Architecture

- Prefect server (API, UI, scheduler) running in Kubernetes.
- Postgres backing database.
- Work pools with worker deployments per team.
- Upstream: Kubernetes, Postgres, identity provider.
- Downstream: Databricks, Snowflake, Bigeye.

## Performance

Scheduler handles thousands of runs per hour. Slowdowns usually come from Postgres connection exhaustion.

## Scalability

Workers scale horizontally per work pool. Server is a single deployment with replicas.

## Availability

Target 99.5%. If the server is down, scheduled runs are missed, not queued.

## Durability

All state in Postgres. Nightly backup plus point in time recovery.

## Security / Compliance

SSO via identity provider. Blocks store secrets, backed by the key vault.

## Monitoring / Alerting

- Dashboard: TODO link
- Logs: server pod logs, worker pod logs
- Alerts:
  - [PrefectWorkPoolNoWorkers](alerts/PrefectWorkPoolNoWorkers.md)

## Known issues

- [flow-runs-stuck-late](kb/flow-runs-stuck-late.md): runs pile up in Late state

## Links to further documentation

- Vendor docs: https://docs.prefect.io
- Team channel: #data-platform-oncall
