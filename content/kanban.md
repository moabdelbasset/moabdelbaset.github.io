+++
title = 'Project Board'
date = '2026-05-17'
draft = false
hidemeta = true
disableShare = true
ShowReadingTime = false
ShowBreadCrumbs = false
ShowPostNavLinks = false
+++

# Project Board

A public roadmap for this site. Work is planned in the open and shipped iteratively — features land via PRs, bugs get triaged, ideas brew in the backlog. Built with help from Claude.

**Legend:**
<span class="kanban-tag feature">Feature</span>
<span class="kanban-tag bug">Bug</span>
<span class="kanban-tag pr">PR</span>
<span class="kanban-tag idea">Idea</span>
<span class="kanban-tag chore">Chore</span>

<div class="kanban-board">

<div class="kanban-column">
<div class="kanban-column-header">
<h3 class="kanban-column-title">Backlog</h3>
<span class="kanban-column-count">11</span>
</div>

<div class="kanban-card">
<span class="kanban-tag feature">Feature</span>
<div class="kanban-card-title">Daily writing habit</div>
<div class="kanban-card-desc">Ship at least one post or TIL every day. Even a short note counts. Streak tracked publicly via post dates.</div>
<div class="kanban-card-meta">area: workflow</div>
</div>

<div class="kanban-card">
<span class="kanban-tag feature">Feature</span>
<div class="kanban-card-title">Write-up: Solaris LDOM storage migration</div>
<div class="kanban-card-desc">Migrating Solaris LDOMs from VMAX to XtremIO — planning, online cutover, gotchas.</div>
<div class="kanban-card-meta">area: posts · category: side project</div>
</div>

<div class="kanban-card">
<span class="kanban-tag feature">Feature</span>
<div class="kanban-card-title">Write-up: vCloud Director automation with Terraform</div>
<div class="kanban-card-desc">Provisioning infrastructure on vCloud Director using Terraform — provider quirks, module layout, state strategy.</div>
<div class="kanban-card-meta">area: posts · category: side project</div>
</div>

<div class="kanban-card">
<span class="kanban-tag feature">Feature</span>
<div class="kanban-card-title">Write-up: PCI hardening automation</div>
<div class="kanban-card-desc">Automating Linux server hardening to meet PCI DSS requirements — Ansible roles, compliance scanning, drift detection.</div>
<div class="kanban-card-meta">area: posts · category: side project</div>
</div>

<div class="kanban-card">
<span class="kanban-tag feature">Feature</span>
<div class="kanban-card-title">Write-up: AWS monitoring with Datadog</div>
<div class="kanban-card-desc">Setting up Datadog monitoring for AWS infrastructure — agent rollout, dashboards, alerting strategy.</div>
<div class="kanban-card-meta">area: posts · category: side project</div>
</div>

<div class="kanban-card">
<span class="kanban-tag feature">Feature</span>
<div class="kanban-card-title">Blog: home lab hardware tour</div>
<div class="kanban-card-desc">What's in the rack, why I picked it, what I'd change.</div>
<div class="kanban-card-meta">area: posts · series: home lab</div>
</div>

<div class="kanban-card">
<span class="kanban-tag feature">Feature</span>
<div class="kanban-card-title">Blog: Proxmox home lab build</div>
<div class="kanban-card-desc">Installing and configuring Proxmox as the hypervisor for the home lab.</div>
<div class="kanban-card-meta">area: posts · series: home lab</div>
</div>

<div class="kanban-card">
<span class="kanban-tag feature">Feature</span>
<div class="kanban-card-title">Blog: Ansible Automation Platform on the home lab</div>
<div class="kanban-card-desc">Installing AAP on the home lab — controller, execution environments, first playbook run.</div>
<div class="kanban-card-meta">area: posts · series: home lab</div>
</div>

<div class="kanban-card">
<span class="kanban-tag feature">Feature</span>
<div class="kanban-card-title">Blog: book summaries series</div>
<div class="kanban-card-desc">A recurring series — short summaries and takeaways from books I read.</div>
<div class="kanban-card-meta">area: posts · series: books</div>
</div>

<div class="kanban-card">
<span class="kanban-tag feature">Feature</span>
<div class="kanban-card-title">Blog: learning to program in public</div>
<div class="kanban-card-desc">Log my programming journey — what I'm learning, what's hard, what clicked.</div>
<div class="kanban-card-meta">area: posts · series: learning</div>
</div>

<div class="kanban-card">
<span class="kanban-tag idea">Idea</span>
<div class="kanban-card-title">AI feature on the site — pick a direction</div>
<div class="kanban-card-desc">Three feasible options for a static GH Pages site:<br>
<strong>1. Build-time AI:</strong> GitHub Action calls Claude on each push to generate per-post TL;DRs, tags, or related-post links. No runtime cost, no key exposure.<br>
<strong>2. "Ask my CV" chat:</strong> small widget where visitors ask about my experience. Needs a Cloudflare Worker or Vercel function to proxy the API key. Free tier works.<br>
<strong>3. AI-assisted drafting:</strong> a workflow script that turns daily notes into draft posts I review before publishing — lives off-site.</div>
<div class="kanban-card-meta">area: site · needs: decision</div>
</div>

</div>

<div class="kanban-column">
<div class="kanban-column-header">
<h3 class="kanban-column-title">In Progress</h3>
<span class="kanban-column-count">0</span>
</div>

<div class="kanban-card" style="border-style: dashed; opacity: 0.6;">
<div class="kanban-card-desc">Nothing in flight. Drag something over from the Backlog.</div>
</div>

</div>

<div class="kanban-column">
<div class="kanban-column-header">
<h3 class="kanban-column-title">Done</h3>
<span class="kanban-column-count">6</span>
</div>

<div class="kanban-card">
<span class="kanban-tag pr">PR</span>
<div class="kanban-card-title">Collapse promoted roles in CV</div>
<div class="kanban-card-desc">Atlassian and Vodafone Egypt entries merged into one each, with final title and a "Promoted from..." note. Timeline reads as four employers instead of seven.</div>
<div class="kanban-card-meta">commit: this PR</div>
</div>

<div class="kanban-card">
<span class="kanban-tag pr">PR</span>
<div class="kanban-card-title">Tighten CV claims to actual strengths</div>
<div class="kanban-card-desc">Profile rewritten to lead with Linux, Ansible, Terraform, and senior support engineering — the actual day-to-day. Dropped aspirational phrasing about architecting K8s platforms.</div>
<div class="kanban-card-meta">commit: this PR</div>
</div>

<div class="kanban-card">
<span class="kanban-tag pr">PR</span>
<div class="kanban-card-title">Ship public project board</div>
<div class="kanban-card-desc">Add /kanban page, kanban CSS, menu item, and profile button. Goldmark unsafe HTML enabled for card markup.</div>
<div class="kanban-card-meta">commit: 9d28ec1</div>
</div>

<div class="kanban-card">
<span class="kanban-tag pr">PR</span>
<div class="kanban-card-title">Rewrite CV with DevOps positioning</div>
<div class="kanban-card-desc">Lead with DevOps Engineer identity, group skills/certs by domain, refresh through current IBM role.</div>
<div class="kanban-card-meta">commit: 09195d9</div>
</div>

<div class="kanban-card">
<span class="kanban-tag pr">PR</span>
<div class="kanban-card-title">Fix CV 404 — backdate page</div>
<div class="kanban-card-desc">Page date was in the future relative to UTC build, so Hugo excluded it. Backdated and unblocked deploy.</div>
<div class="kanban-card-meta">commit: bcdc555</div>
</div>

<div class="kanban-card">
<span class="kanban-tag pr">PR</span>
<div class="kanban-card-title">Add /cv page and real social links</div>
<div class="kanban-card-desc">First pass CV from LinkedIn export. Replaced placeholder GitHub and LinkedIn URLs.</div>
<div class="kanban-card-meta">commit: 86135b8</div>
</div>

</div>

</div>
