---
title: Cluster stuck in Pending
service: databricks
owner: data-platform-engineering
last_reviewed: 2026-11-13
---

# Cluster stuck in Pending

## Symptom

A cluster shows state Pending for more than 10 minutes. Jobs on it never start. Cluster event log shows no Running event.

## Pre-checks

1. Open the cluster event log. Look for the last event.
2. Run against the Clusters API:

```bash
databricks clusters get --cluster-id <id> | jq '.state, .state_message'
```

## Cause

Almost always one of three things: cloud quota exhausted for the instance type, instance type unavailable in the zone, or a bad init script that never returns.

## Resolution

1. If `state_message` mentions quota: request a quota increase or switch the cluster to an instance type with headroom. Then restart.
2. If `state_message` mentions capacity or availability: change the instance type or let the pool fall back. Then restart.
3. If the event log shows Init Scripts Started with no Init Scripts Finished: terminate the cluster, disable the init script, start again. File a ticket for the script owner.

## Verification

Cluster state is Running and a trivial notebook cell executes.

## Escalation

Data platform on-call secondary, then Databricks support if the message is unclear.

## Related

- [DatabricksJobRunFailed](../alerts/DatabricksJobRunFailed.md)
- [service README](../README.md)
