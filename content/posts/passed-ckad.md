+++
title = 'I Passed the CKAD Exam: What Helped Me Succeed'
date = 2026-08-23T10:00:00+02:00
draft = false
description = 'I passed the Certified Kubernetes Application Developer exam. Here are the hands-on study methods, Kubernetes skills, and exam habits that helped me succeed.'
summary = 'A personal reflection on passing CKAD through repeated kubectl practice, objective-driven study, documentation, and hands-on Kubernetes labs.'
tags = ["Kubernetes", "CKAD", "CNCF", "Certifications", "Homelab"]
keywords = ["CKAD", "Certified Kubernetes Application Developer", "CKAD preparation", "Kubernetes certification", "kubectl practice"]
+++

It is official: I **passed the Certified Kubernetes Application Developer (CKAD) exam**.

This is another important milestone in my cloud-native journey. CKAD is a practical certification: instead of selecting answers from a list, candidates work directly with Kubernetes resources from the command line. Passing it required more than knowing what a Pod, Deployment, or Service does. I needed to create, modify, troubleshoot, and verify application configurations efficiently.

This post contains no exam questions, tasks, or confidential details. I am only sharing the preparation approach and general habits that helped me.

## Why I chose CKAD

After working with Kubernetes and OpenShift in my home lab—and recently [passing the EX280 OpenShift administration exam](/posts/passed-ex280/)—I wanted to strengthen the vendor-neutral Kubernetes application skills underneath that experience.

CKAD was a good fit because it focuses on the application layer: designing workloads, managing configuration, exposing applications, applying security settings, observing behavior, and troubleshooting problems. These are useful skills whether a cluster runs upstream Kubernetes, k3s, a managed cloud service, or OpenShift.

The certification gave me a clear goal and a reason to practise the details that are easy to overlook during normal project work.

## Understanding the current exam

The [official CKAD page](https://training.linuxfoundation.org/certification/certified-kubernetes-application-developer-ckad/) describes an online, proctored, performance-based exam completed from a Linux command line. Candidates currently have two hours, and the exam is aligned to Kubernetes v1.35.

At the time of writing, the published domains are:

| Domain | Weight |
|---|---:|
| Application Design and Build | 20% |
| Application Deployment | 20% |
| Application Observability and Maintenance | 15% |
| Application Environment, Configuration and Security | 25% |
| Services and Networking | 20% |

Kubernetes and the certification curriculum continue to evolve. I treated the official exam page and the [CNCF curriculum repository](https://github.com/cncf/curriculum) as the source of truth and recommend checking them again before scheduling an exam.

## My preparation approach

My study plan was based on a simple loop:

```text
Read the objective → practise the task → verify the result
        ↑                                      ↓
        └──── break it, troubleshoot it, and repeat ────┘
```

Reading documentation helped me understand the API and available options. Repetition turned that knowledge into command-line fluency. Troubleshooting showed whether I actually understood the resource or had only memorized a working example.

I focused on being able to do each workflow in several ways:

- Create a resource quickly with `kubectl`.
- Generate YAML and modify it safely.
- Read an existing manifest and identify the important fields.
- Inspect the live object and confirm the result.
- Diagnose a deliberately broken version.
- Find unfamiliar details quickly in the official documentation.

## Practising in my home lab

My Proxmox home lab gave me a place to practise without worrying about damaging an important environment. I could deploy disposable clusters, create workloads, introduce failures, and start again whenever necessary.

I previously documented how I [deployed a single-node k3s cluster on Proxmox with kcli](/posts/deploy-single-node-k3s-proxmox-kcli/). A small cluster like this is useful for daily Kubernetes exercises because it is quick to rebuild and provides a real API server, scheduler, networking layer, and container runtime.

The exact Kubernetes distribution mattered less than repeating the core workflows. I used the lab to work with:

- Pods and multi-container patterns.
- Deployments, updates, rollbacks, Jobs, and CronJobs.
- ConfigMaps, Secrets, environment variables, and volumes.
- Resource requests, limits, quotas, and security contexts.
- Services, Ingress resources, and NetworkPolicies.
- Health probes, logs, events, and application troubleshooting.
- Helm packages and Kustomize overlays.

The biggest benefit of a disposable lab was learning to recover from mistakes. A successful manifest proves only one path; a broken one teaches me how Kubernetes reports problems.

## Building `kubectl` fluency

CKAD rewards accuracy, but it also rewards efficient use of the command line. I practised common operations until they no longer required much thought.

Commands such as these became part of my normal workflow:

```bash
kubectl create deployment web --image=nginx --dry-run=client -o yaml
kubectl get pods -o wide
kubectl describe pod <pod-name>
kubectl logs <pod-name> --all-containers
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl explain deployment.spec.template.spec
```

The goal was not to memorize every flag. It was to know the common commands well and use `kubectl explain`, command help, and the Kubernetes documentation for everything else.

Generating a valid starting manifest with `--dry-run=client -o yaml` was especially useful, but I still needed to understand the YAML I was editing. Speed without understanding can create subtle errors that take longer to diagnose than writing the resource carefully in the first place.

## Verifying every result

One of the most useful habits was to stop treating a successful `kubectl apply` as proof that a task was complete.

After every change, I checked the resulting behavior. Depending on the resource, that meant:

- Confirming desired and available replicas.
- Inspecting Pod status, conditions, and events.
- Reading logs from the correct container.
- Testing a Service or Ingress endpoint.
- Verifying mounted configuration and environment variables.
- Checking that probes behaved as intended.
- Confirming selectors matched the expected Pods.
- Inspecting the live YAML instead of assuming the submitted manifest was accepted unchanged.

This verify-first mindset helped both in preparation and during the exam. Kubernetes often accepts a valid object even when it does not produce the outcome I intended.

## Using the documentation effectively

The Linux Foundation publishes the resources permitted during CKAD. At the time of writing, the Kubernetes documentation can be accessed through the browser inside the exam environment, subject to the current exam rules.

I therefore practised with the [official Kubernetes documentation](https://kubernetes.io/docs/) rather than building a large collection of personal shortcuts and copied snippets. I learned where to find common examples for probes, security contexts, volumes, Services, Ingress, NetworkPolicies, Jobs, and other curriculum topics.

Knowing the documentation structure was more valuable than trying to remember every YAML field. Before the exam, I also reviewed the current [Linux Foundation allowed-resources policy](https://docs.linuxfoundation.org/tc-docs/certification/certification-resources-allowed) and candidate instructions rather than relying on old blog posts about the exam environment.

## Exam-day habits that helped

A few general habits made the practical exam easier to manage:

- Read the complete requirement before changing anything.
- Confirm the current Kubernetes context and namespace for every task.
- Use imperative commands when they provide a clean starting point, then edit the generated YAML.
- Verify the requested outcome instead of stopping when a command exits successfully.
- Watch the remaining time and move on temporarily when a problem is taking too long.
- Use the official documentation deliberately; avoid searching for details already known.
- Leave the environment clean and avoid changing resources outside the task's scope.

I also practised inside a terminal setup close to the real exam workflow. Familiarity with Linux keyboard shortcuts, YAML editing, copy and paste, and navigating the documentation reduced unnecessary friction.

## What passing CKAD reinforced

Passing CKAD reinforced the same lesson I learned while preparing for EX280: **hands-on repetition is the most effective way to learn Kubernetes**.

The certification is valuable, but the lasting result is greater confidence. I am now faster at turning application requirements into Kubernetes resources, more systematic when verifying a deployment, and more comfortable troubleshooting workloads from events, status, and logs.

For now, I am happy to celebrate the milestone:

**CKAD passed — Certified Kubernetes Application Developer achieved.**

## Resources

- [Official CKAD certification page](https://training.linuxfoundation.org/certification/certified-kubernetes-application-developer-ckad/)
- [Current CNCF certification curricula](https://github.com/cncf/curriculum)
- [Kubernetes documentation](https://kubernetes.io/docs/)
- [Linux Foundation CKAD and CKA instructions](https://docs.linuxfoundation.org/tc-docs/certification/tips-cka-and-ckad)
- [Linux Foundation allowed-resources policy](https://docs.linuxfoundation.org/tc-docs/certification/certification-resources-allowed)
- [Deploy a Single-Node k3s Cluster on Proxmox with kcli](/posts/deploy-single-node-k3s-proxmox-kcli/)
