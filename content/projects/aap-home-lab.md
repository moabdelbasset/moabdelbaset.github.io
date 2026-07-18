+++
title = 'Containerized AAP 2.6 Home Lab'
date = 2026-04-20T09:00:00+02:00
draft = false
weight = 20
kicker = 'Automation lab'
year = '2026'
summary = 'A working Ansible Automation Platform 2.6 environment for building execution environments and practising controller workflows.'
description = 'Building a containerized AAP 2.6 lab for execution environments, Automation Controller, Git workflows, and Ansible development.'
stack = ['AAP 2.6', 'Ansible', 'Proxmox', 'Execution Environments', 'Git']
tags = ['Ansible', 'Automation', 'Platform Engineering']
+++

## Why I built it

Reading about modern Ansible workflows is useful, but the platform only becomes intuitive when every component has to work together. I built an all-in-one, containerized **Ansible Automation Platform 2.6** environment on a Proxmox-based home lab as a permanent place to develop, break, and repair automation.

## What the lab covers

- AAP subscription manifest and registry service-account configuration.
- Automation Controller projects, inventories, credentials, job templates, surveys, and workflows.
- Custom execution environments built with `ansible-builder`.
- Git-based content workflows and project synchronization.
- Playbook execution and debugging through `ansible-navigator`.

## What it taught me

Building the platform from the ground up exposed the boundaries between the controller, source control, credentials, and execution environments. That context made troubleshooting much faster: instead of treating a failed job as a controller problem, I could reason about the whole execution path.

The environment became the foundation for my EX374 preparation and remains a useful sandbox for testing reusable automation content.

## Related field notes

- [Road to EX374: Developing Automation with Ansible](/posts/preparing-for-ex374/)
- [I Passed EX374: What to Focus On](/posts/passed-ex374/)
