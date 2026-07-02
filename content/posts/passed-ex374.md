+++
title = 'I Passed EX374: What to Focus On for the Ansible Automation Platform Exam'
date = 2026-07-02T21:00:00+02:00
draft = false
tags = ["Ansible", "Red Hat", "Automation", "Certifications", "AAP", "EX374"]
+++

It's official — I **passed the EX374 exam**, the Red Hat Certified Specialist in Developing Automation with Ansible Automation Platform. This one is the natural next step after my earlier [Road to EX374](/posts/preparing-for-ex374/) post, and getting there took a lot of hands-on lab time rather than reading alone.

I won't share any exam questions or specifics — that's against the Red Hat exam agreement, and it wouldn't help you anyway. What I *can* do is point at the areas that rewarded real practice, so you spend your prep time where it counts.

## Live entirely inside `ansible-navigator`
If you're still reaching for `ansible-playbook`, retrain that muscle now. Get comfortable running, inspecting, and debugging automation through `ansible-navigator` — stdout mode, interactive mode, `:doc` for module lookups, and reviewing playbook artifacts. It should feel like second nature well before exam day.

## Know Execution Environments cold
Execution environments are central to the modern platform, so don't treat them as an afterthought. Practice building them with `ansible-builder`, understand the definition file, pin your collections and Python dependencies deliberately, and be able to reason about *why* a playbook behaves differently inside one EE versus another. Being able to build, tag, and actually use an EE end-to-end matters more than memorizing flags.

## Get fluent with Automation Controller
Spend real time in the Automation Controller UI and its objects: projects, inventories, credentials, job templates, and workflows. Know how a project syncs content from Git, how credentials are injected, and how surveys and variables flow through. Clicking through it a few times isn't enough — build the muscle memory of wiring these pieces together from scratch.

## Treat Git as a first-class skill
Your automation content lives in version control, so the Git workflow isn't a side topic — it's part of the job. Be smooth with branching, committing, and pushing, and understand how the controller pulls from a branch. If Git ever slows you down, that's friction you don't want under time pressure.

## Write content the "professional" way
The exam is about *developing* automation, not just running it. Practice writing modular, reusable playbooks and roles, using variables and templates cleanly, and structuring content so it's maintainable. Sloppy-but-working isn't the target — think about how you'd hand this off to a teammate.

## General exam-day habits
- **Read every task fully before touching anything.** Understand what "done" looks like first.
- **Make your work persistent.** Verify that what you build actually survives and behaves as required, not just that it ran once.
- **Watch the clock, but don't rush the setup.** A correct execution environment or controller object early saves you from cascading failures later.
- **Lab, lab, lab.** Nothing here is theoretical — every objective rewards having done it with your own hands.

## My setup
I did all of my prep in a containerized **AAP 2.6** deployment on a Proxmox-based home lab. Building that environment myself — subscription manifest, registry service account, the works — turned out to be some of the best preparation, because it forced me to understand how the platform fits together rather than just how to click through it.

On to the next one. If you're on this path, keep your hands on the keyboard and your content in Git.
