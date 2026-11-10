+++
title = 'I Passed EX380: Preparing with a Single-Node Homelab and a Three-Node OpenShift Cluster'
date = 2026-11-10T09:00:00+01:00
draft = false
description = 'How I used a single-node OpenShift homelab and a three-node cluster on Hetzner to prepare for EX380 through practical, objective-driven study.'
summary = 'Passing EX380 with hands-on OpenShift practice: a single-node homelab for focused experiments, a three-node Hetzner cluster for broader scenarios, and verification beyond successful commands.'
tags = ["OpenShift", "Kubernetes", "Red Hat", "Certifications", "Homelab", "GitOps"]
keywords = ["EX380", "OpenShift exam preparation", "single-node OpenShift", "SNO", "Hetzner", "OpenShift homelab"]
+++

I **passed EX380**! After [passing EX280](/posts/passed-ex280/), this was another milestone in my OpenShift journey—and another reminder of how much I learn by running the platform myself.

The most useful part of my preparation was turning exam objectives into things I could test. Reading gave me the concepts. My lab gave me somewhere to apply them, inspect the results, and work through the gaps in my understanding.

I used two environments: **a single-node OpenShift (SNO) setup in my homelab** and **a three-node OpenShift cluster on Hetzner**. Having both let me approach preparation from different angles without expecting one small environment to reproduce every scenario.

## Starting with the objectives

[Red Hat currently lists EX380 as the Red Hat Certified Advanced System Administrator in OpenShift exam](https://www.redhat.com/en/services/training/ex380-red-hat-certified-advanced-system-administrator-in-openshift-exam). It is a practical exam, so my preparation needed to go beyond recognizing configuration examples.

I treated the objectives as prompts for lab work. For each topic, the useful questions were:

- What working result am I trying to produce?
- Which resources and dependencies make it possible?
- How can I prove the result works?
- What would I inspect if it stopped working?

That last question matters. A command can complete successfully while the application or integration is still unusable. I wanted to understand the path from configuration to observable behavior.

Red Hat offers multiple exam versions, so check the objectives for your booked version through the [official exam page](https://www.redhat.com/en/services/training/ex380-red-hat-certified-advanced-system-administrator-in-openshift-exam). The examples here describe my preparation approach and lab projects.

## Two clusters with different purposes

My home environment ran **single-node OpenShift**. Having the control plane and workloads on one node made it a useful place for focused experiments. I could work on resources, inspect their state, and revisit a configuration without needing a larger cluster for every session.

SNO also has clear limits. One node cannot demonstrate placement across several nodes or workload continuity when another node becomes unavailable. Restarting the only node affects the whole environment. Those limits shaped which experiments belonged there.

The Hetzner environment gave me a different topology: **three OpenShift VMs running on one dedicated server**, with each node carrying control-plane and worker roles. I documented the installation in [OpenShift Lab on a Hetzner Dedicated Server](/projects/openshift-hetzner-lab/).

| Environment | Where it helped | Constraint to keep in mind |
| --- | --- | --- |
| Single-node homelab | Focused configuration experiments and application-level practice | No placement across multiple nodes |
| Three-node Hetzner cluster | Multi-node behavior and a larger environment for integrated projects | All three VMs share one physical server |

The Hetzner cluster gave me multiple nodes to work with, but the dedicated server remained a shared failure domain. That distinction is useful when learning about availability: multiple VMs and independent infrastructure failures are different things to test.

## Turning an objective into a lab exercise

The public objectives include identity integration, application recovery, workload placement, GitOps, monitoring, and logging. [Red Hat's objective list](https://www.redhat.com/en/services/training/ex380-red-hat-certified-advanced-system-administrator-in-openshift-exam) provides the scope; the next step is defining evidence for each exercise.

These are examples of how to translate those areas into practical checks, rather than a claim that one lab project covers the entire exam:

| Area | Exercise to reproduce | Evidence to look for |
| --- | --- | --- |
| Identity and access | Connect an identity provider and assign group permissions | A test user can perform the intended action and is denied an unauthorized one |
| Application recovery | Back up a disposable application with persistent data, then restore it | The restored application serves the original data |
| Workload placement | Combine labels, selectors, taints, and tolerations | Pods land on eligible nodes; an incompatible configuration produces an explainable pending state |
| GitOps | Deploy from Git and introduce a manual change | Reconciliation returns the managed resource to its declared state |
| Monitoring | Create a controlled application problem | Metrics and alerts expose the condition and clear after recovery |
| Logging | Generate a known application message | The message can be found through the configured logging path |

Some exercises need extra infrastructure. Recovery practice needs suitable storage and a backup destination; identity integration needs an identity service. A healthy OpenShift installation is the starting point, and the dependencies are part of planning the experiment.

## GitOps made the learning concrete

One project that brought several skills together was [delivering my Flask portfolio through GitOps](/projects/gitops-flask-openshift/). I built and tested a container, published it to Quay, and deployed it to the Hetzner cluster using Argo CD and Kustomize.

The workflow made the relationship between repositories, images, and cluster state visible. Publishing an image alone did not release the application. I selected its digest in the GitOps repository, then Argo CD applied the updated configuration.

For a drift experiment, I manually scaled the Deployment from one replica to two. Argo CD's self-healing restored the Git-defined count of one. Watching **1 → 2 → 1** made reconciliation much easier to explain than simply reading about it.

It also gave me a useful troubleshooting question: **which system owns the desired state?** If I changed a managed resource directly, I needed to understand why that change might disappear.

## The infrastructure taught me too

Building the lab exposed dependencies that are easy to overlook in a ready-made environment. API access, application routes, DNS, and ingress all had to fit together before I could concentrate on higher-level tasks.

For example, my Hetzner setup initially relied on local hosts-file entries. During the GitOps project, switching the cluster's Cloudflare records to DNS only restored access without those overrides. The application configuration was only one part of the path to a working URL.

That experience reinforced a habit I carried into preparation: trace the complete path. When something fails, inspect the relevant resource status, events, logs, permissions, and network dependencies instead of repeatedly applying the same manifest.

## What I would recommend to someone preparing

Start with the objectives for your exam version and build a small exercise around each one. Give every exercise an observable success condition. Then change something deliberately, explain the failure, and recover.

Use the environment you have thoughtfully. SNO is useful for many focused tasks. Multiple nodes become necessary when the behavior you want to understand depends on placement or disruption across nodes. Choose the topology around the experiment.

Keep notes that explain the result as well as the commands. A short record of what changed, how you verified it, and why a failed attempt failed is more useful on the next session than a page of unexplained YAML.

Passing EX380 is a milestone I am happy to celebrate. The lasting benefit is the experience behind it: building environments, testing assumptions, and getting better at explaining what OpenShift is doing when the first attempt does not work.
