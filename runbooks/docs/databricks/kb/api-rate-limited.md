---
title: Workspace API rate limited (429)
service: databricks
owner: data-platform-engineering
last_reviewed: 2026-11-13
---

# Workspace API rate limited (429)

## Symptom

Job runs or automation fail with HTTP 429. Error text includes "rate limit" or "too many requests".

## Pre-checks

Check audit logs for the calling principal with the highest request count in the last 15 minutes.

## Cause

A single service principal or automation loop is making too many API calls. Workspace limits are shared across all callers.

## Resolution

1. Identify the top caller from the pre-check.
2. If it is a runaway automation, pause it (Prefect deployment or cron).
3. Ask the owner to add backoff and batching. Do not raise the limit as a first fix.

## Verification

429 count drops to zero on the dashboard within 5 minutes.

## Escalation

Data platform on-call secondary.

## Related

- [service README](../README.md)
