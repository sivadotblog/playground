# Runbooks

Operational knowledge base for support and operations engineers. Modeled on the GitLab SRE runbooks repo (runbooks.gitlab.com). This file is the spec. It is written so an LLM can read it and produce or maintain content that fits the structure.

## Core concepts

1. **The service catalog is the root.** Every top-level directory under `docs/` must match a `name` in `service-catalog.yml`. Nothing else is allowed at that level. Anything that does not belong to one service goes under `docs/uncategorized/`.
2. **One directory per service.** `docs/<service>/` holds everything an on-call engineer needs for that service.
3. **One README per service.** `docs/<service>/README.md` follows `templates/service-readme.md`. It is background, not procedure. It is the only place general service information lives. Runbooks link to it instead of repeating it.
4. **One file per issue.** Each known problem gets its own file under `docs/<service>/kb/`. It follows `templates/kb-article.md`. The structure is symptom, cause, solution.
5. **One playbook per alert.** Each alert that pages someone gets its own file under `docs/<service>/alerts/`, named exactly after the alert name. It follows `templates/alert-playbook.md`. The alert definition links to it. If you add an alert you must add its playbook in the same change.
6. **Ownership.** Each service in the catalog has an owner team. That team owns the README, the kb, and the alert playbooks for that service.

## Layout

```
runbooks/
  README.md                  this file
  service-catalog.yml        source of truth for service names and owners
  templates/
    service-readme.md
    kb-article.md
    alert-playbook.md
  docs/
    <service>/
      README.md              from templates/service-readme.md
      alerts/
        <AlertName>.md       from templates/alert-playbook.md
      kb/
        <short-slug>.md      from templates/kb-article.md
    uncategorized/
      <short-slug>.md
```

## Rules for writing

- Write for a tired on-call engineer with standard access, not a senior expert.
- Short and concise. No fluff. Lead with the action.
- Every runbook must be complete enough to execute without further research. If a step needs a command, put the exact command in a code block.
- Do not duplicate. Link to the service README or another article instead of copying.
- Name the alert exactly as it appears in the monitoring system. File names are case sensitive.
- Each article has frontmatter: `title`, `service`, `owner`, `last_reviewed`. Review at least quarterly.
- Prefer decision points over prose when the fix depends on a condition ("If X, do A. Otherwise do B.").
- Say what to do when the runbook does not work: who to escalate to and where.

## Naming

- Service directories: kebab-case, matching the catalog exactly (`databricks`, `prefect`).
- Alert playbooks: the alert name as is (`DatabricksJobRunFailed.md`).
- KB articles: short kebab-case slug describing the symptom (`cluster-stuck-pending.md`).

## How to add content

- New service: add it to `service-catalog.yml`, create `docs/<service>/README.md` from the template, create empty `alerts/` and `kb/` directories.
- New known issue: copy `templates/kb-article.md` to `docs/<service>/kb/<slug>.md` and fill it in.
- New alert: copy `templates/alert-playbook.md` to `docs/<service>/alerts/<AlertName>.md`, fill it in, and add the file link to the alert definition.

## Instructions for an LLM

When asked to create or update content here:

1. Read `service-catalog.yml` first. If the service is not listed, stop and ask whether to add it.
2. Pick the template that matches the request: a service overview, a known issue, or an alert.
3. Copy the template exactly. Keep every heading. Leave a heading in place with "N/A" rather than deleting it.
4. Fill in only what you know. Do not invent commands, dashboard URLs, or owner names. Use `TODO:` where the author must fill in.
5. Link to existing articles when they cover a step. Do not restate them.
6. Set `last_reviewed` to today's date.
