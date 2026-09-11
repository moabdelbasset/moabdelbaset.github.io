+++
title = 'GitOps Delivery for a Flask Portfolio on OpenShift'
date = 2026-09-11T00:00:00+03:00
draft = false
weight = 12
kicker = 'Application delivery'
year = '2026'
summary = 'A tested Flask container delivered through GitHub Actions, Quay, and Argo CD, with a verified development release and automatic drift correction.'
description = 'Building and testing a Flask portfolio image, deploying it to OpenShift through GitOps, and demonstrating a digest-based release and Argo CD self-healing.'
stack = ['OpenShift', 'Argo CD', 'GitHub Actions', 'Quay', 'Flask', 'Kustomize']
tags = ['GitOps', 'OpenShift', 'CI/CD', 'Flask', 'Homelab']
+++

## Why I built it

After [building my OpenShift lab on Hetzner](/projects/openshift-hetzner-lab/), I wanted to demonstrate how an application moves from source code to a running deployment. I built a small Flask portfolio and a delivery workflow that tests its container, publishes it to Quay, and deploys a reviewed image digest through Argo CD.

The application is deliberately small: its content lives in `content.json`, and Flask renders a template and stylesheet. There is no database or persistent volume. This let me focus on image compatibility, deployment configuration, networking, and reconciliation.

## Delivery architecture

```text
Application repository → GitHub Actions → Tested image in Quay
                                                |
                                    Manually copy image digest
                                                |
GitOps repository ← Reviewed digest-update PR and merge
        |
        v
Argo CD → OpenShift Deployment → Service → HTTPS Route
```

The [application repository](https://github.com/moabdelbasset/portolio-flask) contains Flask code, seven automated tests, the Dockerfile, and CI. The [GitOps repository](https://github.com/moabdelbasset/portolio-flask-gitops) contains a shared Kustomize base, a development overlay, and the Argo CD Application definition.

Publishing an image does not deploy it. I select its digest in a GitOps pull request, review the change, and merge it. Argo CD watches that repository and applies the desired configuration. CI does not need cluster credentials.

## Building an OpenShift-compatible image

The container runs Gunicorn on port 8080 and defaults to a non-root user. CI tests it with an arbitrary UID and a read-only root filesystem, with writable temporary storage mounted at `/tmp`.

Seven tests cover portfolio rendering and links, HTML escaping, CSS delivery, the health response, health independence from the content file, missing routes, and rejected POST requests. CI then builds the container and checks both `/healthz` and `/` before publishing the same tested image to Quay on pushes to `main`.

The Deployment adds resource requests and limits, startup/readiness/liveness probes, dropped Linux capabilities, and disabled service-account token mounting. Readiness checks `/` so the application must render before it receives traffic; liveness checks `/healthz`.

## Deploying development

The recorded environment ran OpenShift **4.22.11** on three ready `amd64` VMs sharing one Hetzner dedicated server. I installed OpenShift GitOps **1.21.4** through the web console and configured Argo CD to read `overlays/development`.

The overlay selects the `portfolio-development` namespace, image digest, and Route hostname. I created and labeled the namespace for Argo CD management, registered the Application, and performed the first synchronization manually. Once the application was healthy, I enabled automatic synchronization and self-healing, leaving automatic pruning disabled.

An access issue exposed an important network dependency: the cluster worked through local hosts-file overrides but failed through proxied Cloudflare records. Changing the cluster DNS records to **DNS only** restored access without those overrides. The OpenShift router handles HTTPS for the application Route.

## Demonstrations and results

| Demonstration | Recorded result |
| --- | --- |
| Initial deployment | Argo CD reported `Synced / Healthy`; the portfolio loaded through its HTTPS Route |
| Configuration drift | After manually scaling to two replicas, Argo CD restored the Git-defined count of one |
| Application release | A change to `content.json` produced a new image; merging its digest-update PR changed the running website |

The replica watch captured desired counts of **1 → 2 → 1**. Kubernetes maintains the live Deployment's requested count; Argo CD corrected that requested count to match Git. The watch output had no timestamps, so it does not establish a recovery duration.

The release demonstrated on September 11, 2026 used application commit `4f2c57a9aab9c272dd5ccc77b4c6f0608c67a1ed` and this image:

```text
quay.io/moabdelbasset/portolio-flask@sha256:85e7a1936b2a3d90cb2b681f0cfa916d9e47458509b7705d92ba6b9a70bf0f26
```

## What remains

The development delivery flow works. Staging promotion, recovery through a Git revert, automatic creation of digest-update PRs, and measured delivery/recovery timings are the next milestones. They have not yet been demonstrated.

This is a lab deployment on a single physical host, with one application replica. It is not a demonstration of production availability or disaster recovery.

## Code and walkthrough

- [Application source and CI](https://github.com/moabdelbasset/portolio-flask)
- [Kustomize manifests and Argo CD Application](https://github.com/moabdelbasset/portolio-flask-gitops)
- [Download the step-by-step wiki guide](/guides/GitOps-Application-Delivery-on-OpenShift.md)
- [Underlying Hetzner lab case study](/projects/openshift-hetzner-lab/)
