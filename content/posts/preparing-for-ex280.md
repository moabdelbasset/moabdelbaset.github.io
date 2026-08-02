+++
title = 'Road to EX280: Preparing for OpenShift Administration'
date = 2026-08-02T11:30:00+02:00
draft = false
description = 'How I am preparing for EX280 with official Red Hat training, objective-driven study, a kcli-powered OpenShift home lab, and public GitHub notes.'
summary = 'My EX280 preparation plan combines official Red Hat training and documentation with repeatable OpenShift practice in my Proxmox home lab.'
tags = ["OpenShift", "Kubernetes", "Red Hat", "Certifications", "Homelab"]
keywords = ["EX280", "OpenShift Administration", "DO280", "Red Hat certification", "OpenShift homelab", "kcli"]
+++

I have started preparing for the **Red Hat Certified System Administrator in OpenShift exam (EX280)**. This is the next step in my OpenShift learning path and a chance to turn the Kubernetes and container fundamentals I have been building into practical cluster-administration skills.

This post is a record of how I am preparing. It contains no exam questions or confidential exam material—only public objectives, official documentation, and the lab work I am doing myself.

## Starting with official Red Hat training

I took the official training from **Red Hat**, which gave me a structured foundation instead of learning isolated commands without context. The course aligned with this certification path is [Red Hat OpenShift Administration II: Configuring a Production Cluster (DO280)](https://www.redhat.com/en/services/training/red-hat-openshift-administration-ii-configuring-a-production-cluster).

The training helped connect day-to-day administration topics such as:

- Managing applications from manifests and packaged content.
- Authentication, authorization, users, groups, and roles.
- Routes, services, TLS, and network policies.
- Resource quotas, limit ranges, and developer self-service.
- Operators and application security.
- Cluster health, troubleshooting, and updates.

Completing a course is only the beginning. EX280 is performance-based, so I need to be able to perform and verify the work on a real cluster—not simply recognize the correct option in a list.

## Following the official exam objectives

My source of truth is the [official EX280 exam page and objectives](https://www.redhat.com/en/services/training/red-hat-certified-openshift-administrator-exam).

I use the objectives as a checklist. For each study point, I want to be able to:

1. Explain what the resource or feature does.
2. Create or configure it with the `oc` command-line interface.
3. Inspect the resulting YAML and status.
4. Test that the configuration produces the intended outcome.
5. Troubleshoot a deliberately broken version.
6. Repeat the workflow without relying on copied commands.

The official objectives currently cover OpenShift management, resource manifests, application deployment, authentication and authorization, network security, developer self-service, Operators, and application security. Red Hat also makes an important point: configurations created during a performance-based exam must persist without manual intervention after a reboot.

I regularly check the objectives again rather than assuming they have stayed unchanged. The public EX280 page currently references **OpenShift Container Platform 4.18**, while my original notes repository was created around **OpenShift 4.14**. I therefore treat the booked exam version and its current official objectives as authoritative, then update or retest older notes where the platform behavior has changed.

## Building a repeatable OpenShift home lab

Reading documentation is useful, but OpenShift administration only becomes familiar through repetition. I use **kcli** in my Proxmox home lab to deploy OpenShift clusters for testing and study.

This gives me a lab that I can rebuild instead of being afraid to break:

- Provision a clean cluster.
- Practise an objective from scratch.
- Introduce a failure intentionally.
- Diagnose it using events, logs, resource status, and documentation.
- Delete the environment and repeat the exercise.

Automating the infrastructure setup lets me spend more time on OpenShift administration and less time manually creating VMs. It also makes destructive practice safer because the cluster is disposable and separate from workloads I care about.

I documented the foundation of this setup in two earlier posts:

- [Install kcli on macOS and Manage Proxmox VMs](/posts/install-kcli-macos-proxmox/)
- [Deploy a Single-Node k3s Kubernetes Cluster on Proxmox with kcli](/posts/deploy-single-node-k3s-proxmox-kcli/)

The k3s deployment was a quick validation of the kcli and Proxmox pipeline. OpenShift exercises additional paths and has a much larger resource footprint, but the same repeatable-lab principle applies.

## Keeping my study notes on GitHub

I created a public repository for the commands, explanations, and examples I collect while studying:

**[moabdelbasset/ex280-v414](https://github.com/moabdelbasset/ex280-v414)**

The repository currently includes notes on areas such as:

- Using the web console and `oc` CLI.
- Querying, formatting, importing, and exporting resources.
- Images, projects, logs, cluster health, and troubleshooting.
- Deployments, manifests, Kustomize, Helm, jobs, services, labels, and selectors.
- Secrets and application configuration.

Writing the notes forces me to explain why a command works, not just save it in shell history. Keeping them in Git also gives me a visible checklist, change history, and a place to improve examples whenever I learn a better approach.

These are personal study notes rather than a replacement for Red Hat documentation. Anyone using them should confirm the OpenShift and exam version first.

## My preparation loop

My study sessions follow a simple cycle:

```text
Official objective → Red Hat documentation → home-lab practice
        ↑                                      ↓
        └──────── verify, troubleshoot, and document ────────┘
```

For every topic, the final question is not “Did the command run?” but “Can I prove the required state is correct?” That means checking resource YAML, conditions, events, logs, permissions, connectivity, and application behavior as appropriate.

I am also building speed with the tools available in the environment: `oc explain`, API resource discovery, JSONPath and custom-column output, label selectors, server-side dry runs, and the official product documentation. The goal is not to memorize every command. It is to know how to find the right information quickly and apply it correctly.

## What comes next

The plan from here is straightforward:

1. Complete a first pass through every official objective.
2. Fill the remaining gaps in the GitHub notes.
3. Rebuild the OpenShift lab regularly with kcli.
4. Practise mixed scenarios that combine security, networking, storage, and application management.
5. Recheck the official exam version and objectives before booking.

I will keep updating the repository as the preparation progresses, and I will share the lessons that come out of the lab work here.

## References

- [Official EX280 exam page and objectives](https://www.redhat.com/en/services/training/red-hat-certified-openshift-administrator-exam)
- [Red Hat OpenShift Administration II (DO280)](https://www.redhat.com/en/services/training/red-hat-openshift-administration-ii-configuring-a-production-cluster)
- [OpenShift Container Platform documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18)
- [My EX280 study notes on GitHub](https://github.com/moabdelbasset/ex280-v414)
