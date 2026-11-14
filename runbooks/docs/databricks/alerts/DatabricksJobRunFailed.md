---
title: DatabricksJobRunFailed
service: databricks
owner: data-platform-engineering
last_reviewed: 2026-11-13
---

# DatabricksJobRunFailed

## Overview

A scheduled job run ended in FAILED state. Downstream tables may be stale. Fires once per failed run for tier 1 jobs only.

## Services

Databricks jobs. See [service README](../README.md).

## Metrics

Job run state from the Jobs API polled every 5 minutes. Threshold: any run with `result_state = FAILED` and tag `tier=1`.

## Alert behavior

Fires per run, so a job on a 15 minute schedule can fire four times an hour. Can be silenced for up to 4 hours during a known vendor incident.

## Severity

S2 by default. S1 if the job feeds a regulatory report (see job tag `regulatory=true`).

## Verification

1. Open the run in the Jobs UI from the alert link.
2. Confirm `result_state` is FAILED and not CANCELED or SKIPPED.

## Recent changes

- Job definition history in the Jobs UI.
- Recent deploys to the job's repo.
- Vendor status page.

## Troubleshooting

1. Read the last 50 lines of the driver log. Most failures show the real error there.
2. Cluster never started: see [cluster-stuck-pending](../kb/cluster-stuck-pending.md).
3. Error mentions 429 or rate limit: see [api-rate-limited](../kb/api-rate-limited.md).
4. Error is in user code (Python traceback, SQL error): hand to the job owner. Do not fix user code on call.

## Possible resolutions

1. Infra cause fixed: re-run the job from the Jobs UI using Repair run.
2. User code cause: notify the job owner from the job's `owner` tag and leave the alert open.
3. Vendor incident: silence the alert, post in #data-platform-oncall, re-run when resolved.

## Dependencies

Cloud storage, identity provider, Prefect if the job is triggered externally.

## Escalation

1. Data platform on-call secondary.
2. Databricks vendor support (support portal, P2 or above).

## Definitions

- Alert source: TODO link
- Dashboard: TODO link
