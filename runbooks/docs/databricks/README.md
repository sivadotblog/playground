---
title: Databricks
service: databricks
owner: data-platform-engineering
last_reviewed: 2026-11-13
---

# Databricks

## Summary

Shared lakehouse platform for data engineering and analytics teams. Runs scheduled jobs, interactive notebooks, and SQL warehouses. Hundreds of engineering teams depend on it for daily pipelines.

## Architecture

- Control plane managed by Databricks.
- Data plane runs in our cloud subscription: job clusters, all-purpose clusters, SQL warehouses.
- Unity Catalog for governance.
- Upstream: cloud storage, identity provider, Prefect (triggers jobs).
- Downstream: Snowflake loads, BI tools, data quality checks in Bigeye.

## Performance

Job latency depends on cluster start time (typically 3 to 6 minutes for a cold cluster). Pools reduce this. Known bottleneck: driver node for jobs with many small tasks.

## Scalability

Autoscaling clusters. Workspace limits on concurrent jobs and API rate. See kb/api-rate-limited.md.

## Availability

Target 99.9% for job scheduling. Vendor status page covers control plane. No cross-region failover.

## Durability

Data lives in cloud storage, not in the cluster. Notebooks are in Repos (git) or workspace storage backed up nightly.

## Security / Compliance

SSO via identity provider. Secrets in the secret scope backed by the key vault. Unity Catalog enforces table access. Audit logs forwarded to the SIEM.

## Monitoring / Alerting

- Dashboard: TODO link
- Logs: cluster event logs, driver logs, audit logs in log analytics
- Alerts:
  - [DatabricksJobRunFailed](alerts/DatabricksJobRunFailed.md)

## Known issues

- [cluster-stuck-pending](kb/cluster-stuck-pending.md): cluster never leaves Pending state

## Links to further documentation

- Vendor docs: https://docs.databricks.com
- Team channel: #data-platform-oncall
