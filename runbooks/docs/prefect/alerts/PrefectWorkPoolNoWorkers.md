---
title: PrefectWorkPoolNoWorkers
service: prefect
owner: data-platform-engineering
last_reviewed: 2026-11-13
---

# PrefectWorkPoolNoWorkers

## Overview

A work pool has had zero online workers for 5 minutes. Nothing in that pool will run. Flows start going Late.

## Services

Prefect workers. See [service README](../README.md).

## Metrics

Count of workers with heartbeat in the last 60 seconds per work pool. Threshold: 0 for 5 minutes.

## Alert behavior

Fires once per pool. Stays firing until a worker heartbeats. Can be silenced during planned worker redeploys.

## Severity

S2. S1 if the pool runs tier 1 flows.

## Verification

1. Open Work Pools in the Prefect UI. Confirm the pool shows no workers.
2. Check the worker deployment:

```bash
kubectl -n prefect get deploy prefect-worker-<pool> -o wide
```

## Recent changes

Recent rollouts of the worker deployment. Kubernetes node events. Prefect server upgrades.

## Troubleshooting

1. Pods CrashLoopBackOff: read pod logs. Usually a bad API URL or expired API key.
2. Pods Running but no heartbeat: the worker cannot reach the server. Check network policy and server health.
3. Deployment scaled to 0: someone scaled it down. Check the rollout history.

## Possible resolutions

1. Bad config: fix the secret or config map, restart the deployment.
2. Scaled to 0: scale back to the previous replica count.
3. Server down: fix the server first, workers reconnect on their own.

## Dependencies

Kubernetes, Prefect server, identity provider.

## Escalation

1. Data platform on-call secondary.
2. Platform Kubernetes team if the cluster itself is unhealthy.

## Definitions

- Alert source: TODO link
- Dashboard: TODO link
