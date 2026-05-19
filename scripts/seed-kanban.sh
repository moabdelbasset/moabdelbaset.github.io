#!/usr/bin/env bash
# Seeds GitHub Issues + labels to match the /kanban page on the site.
#
# Prereqs:
#   brew install gh
#   gh auth login
#
# Usage:
#   ./scripts/seed-kanban.sh
#
# After running, create a GitHub Project (Projects -> New project -> Board)
# in the repo and bulk-add the issues. Labels are pre-coloured to match
# the kanban page.

set -euo pipefail

REPO="moabdelbasset/moabdelbaset.github.io"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found. Install with: brew install gh" >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "gh is not authenticated. Run: gh auth login" >&2
  exit 1
fi

echo "== Seeding labels =="
# label|color|description
LABELS=(
  "feature|1e6aff|A new capability on the site"
  "bug|ff4d4d|Something broken"
  "idea|ffb300|Needs decision before scoping"
  "chore|888888|Maintenance, tooling, housekeeping"
  "cv|ff7a00|Touches the CV page"
  "blog|00b3a4|Blog post or series"
  "side-project|a566ff|Past work to write up as a portfolio piece"
  "ai|e0429d|AI-related work"
  "home-lab|2bbf6f|Home lab series"
)

for entry in "${LABELS[@]}"; do
  IFS='|' read -r name color desc <<< "$entry"
  if gh label list --repo "$REPO" --search "$name" --json name -q '.[].name' | grep -qx "$name"; then
    gh label edit "$name" --color "$color" --description "$desc" --repo "$REPO" >/dev/null
    echo "  updated: $name"
  else
    gh label create "$name" --color "$color" --description "$desc" --repo "$REPO" >/dev/null
    echo "  created: $name"
  fi
done

echo "== Seeding issues =="
# title|labels|body
ISSUES=(
  "Collapse promoted roles in CV|feature,cv|Merge multiple entries at the same company (Atlassian, Vodafone Egypt) into a single entry per company with the final title and a short note on internal moves. Goal: avoid the job-hopper look."
  "Tighten CV claims to actual strengths|feature,cv|Trim aspirational phrasing. Lead with what I actually do day-to-day: Linux, Terraform, Ansible, Kubernetes, escalation engineering. No exaggeration."
  "Daily writing habit|feature|Ship at least one post or TIL every day. Set up post template, drafts folder, and a daily reminder. Even short notes count."
  "Write-up: Solaris LDOM storage migration|side-project,blog|Migrating Solaris LDOMs from VMAX to XtremIO — planning, online cutover, gotchas, rollback plan."
  "Write-up: vCloud Director automation with Terraform|side-project,blog|Provisioning infrastructure on vCloud Director with Terraform — provider quirks, module layout, state strategy."
  "Write-up: PCI hardening automation|side-project,blog|Automating Linux server hardening to meet PCI-DSS — Ansible roles, compliance scanning, drift detection."
  "Write-up: AWS monitoring with Datadog|side-project,blog|End-to-end Datadog observability on AWS — agent rollout, integrations, dashboards, alert hygiene."
  "Blog: home lab hardware tour|blog,home-lab|What's in the rack, why I picked it, what I'd change."
  "Blog: Proxmox home lab build|blog,home-lab|Installing and configuring Proxmox as the hypervisor for the home lab."
  "Blog: Ansible Automation Platform on the home lab|blog,home-lab|Installing AAP — controller, execution environments, first playbook run."
  "Blog series: book summaries|blog|Recurring series of short summaries and takeaways from books I read."
  "Blog series: learning to program in public|blog|Log the programming journey — what I'm learning, what's hard, what clicked."
  "AI feature on the site — pick a direction|idea,ai|Three feasible options on a static GH Pages site: (1) build-time AI via GitHub Action generating per-post TL;DRs/tags, (2) 'Ask my CV' chat via Cloudflare Worker proxying Claude API, (3) AI-assisted drafting CLI that turns daily notes into draft posts. Decide once the blog has a few posts."
)

for entry in "${ISSUES[@]}"; do
  IFS='|' read -r title labels body <<< "$entry"
  if gh issue list --repo "$REPO" --state all --search "in:title \"$title\"" --json title -q '.[].title' | grep -Fxq "$title"; then
    echo "  exists: $title"
  else
    gh issue create --repo "$REPO" --title "$title" --body "$body" --label "$labels" >/dev/null
    echo "  created: $title"
  fi
done

echo
echo "Done. Next: create a Project board in GitHub UI (Projects -> New project -> Board)"
echo "and add these issues. Three columns: Backlog / In Progress / Done."
