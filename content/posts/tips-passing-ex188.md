+++
title = 'Tips for Passing the EX188: Red Hat Certified Specialist in Containers'
date = 2026-07-04T10:00:00+02:00
draft = false
tags = ["Containers", "Podman", "Red Hat", "Certifications", "EX188"]
+++

I want to share the study habits and small tactical choices that worked for me while preparing for the **Red Hat Certified Specialist in Containers (EX188)** exam. This is a hands-on, performance-based exam focused on running, building, and managing containers on Red Hat Enterprise Linux with **Podman** — no OpenShift, no Kubernetes, just the container runtime fundamentals.

**Note:** this post contains no exam content — no questions, no tasks, no specifics of what came up on the day. Everything referenced here is publicly available from Red Hat's exam page.

## Take the Official Objectives Literally

Before doing anything else, read Red Hat's published objectives and treat them as the source of truth:

* [Official EX188 exam page](https://www.redhat.com/en/services/training/red-hat-certified-specialist-containers-exam)

The scope is genuinely tight: image lifecycle, running and managing containers, storage, basic networking, and systemd integration. If a topic isn't listed, don't chase it. It's easy to fall down orchestrator rabbit holes when this exam deliberately isn't about that.

## Build a Lab You Actually Live In

The single biggest thing that helped me was **a RHEL 9 VM I used every day**, not a scratch environment I only opened during study sessions.

* Spin up a RHEL 9 VM in your home lab — Proxmox, KVM, VirtualBox, whatever you already run.
* Register it with a free [Red Hat Developer subscription](https://developers.redhat.com/products/rhel/download) so `dnf` behaves normally.
* Use it as your everyday sandbox. When you need to test *anything* container-adjacent — for work, for a blog post, for curiosity — do it there.

Familiarity with the environment is quiet but powerful. On exam day you don't want to be surprised by anything about how the OS feels.

## Rootless and Rootful Aren't the Same Podman

Rootless Podman behaves differently from rootful — user namespaces, storage locations, port ranges, and networking all shift. Practise both, but spend real time on rootless. That's where the interesting quirks live, and it's the direction Red Hat is steering people toward.

If you can't explain, off the top of your head, *why* a rootless container can't bind to port 80 by default, spend an evening on that before booking the exam.

## Build Podman Muscle Memory

The exam is time-boxed and hands-on. Grepping through `man` pages for basic flags will burn time you don't have.

Practise until these are automatic, no thinking required:

* Pulling, tagging, inspecting, and removing images.
* Running containers with the right combination of volume mounts, port publishing, environment variables, and restart policy.
* Writing a Containerfile and understanding what each instruction does at build time.
* Reading and following container logs.

You don't need to memorise every flag. You do need the common workflows to feel like typing your own name.

## Read the Docs, Don't Memorise the Tutorial

It's tempting to memorise "the command that mounts a volume" without understanding what actually happens on disk. That approach holds up until a scenario shifts one step off the tutorial path — and then it collapses.

Slow down and read the primary sources:

* [Podman documentation](https://docs.podman.io/)
* [Building, running, and managing containers (RHEL 9)](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/building_running_and_managing_containers/index)

The RHEL 9 container guide is excellent and free. The more time you spend there, the less any exam scenario feels unfamiliar.

## Invest Extra Time in systemd Integration

Running containers as systemd units is one of the more nuanced parts of the Podman story, and it maps directly to how you'd actually deploy things in the real world.

* Practise generating unit files with `podman generate systemd` and read every section of the output.
* Learn **Quadlet** as well — it's the modern path and where Red Hat is heading.
* Get comfortable with `systemctl --user` for rootless services, and know where user unit files live.

## Exam-Day Habits That Saved Me Time

* **Read every task fully before starting.** No skimming. A missed constraint at the top costs you five minutes at the bottom.
* **Move on when stuck.** If a task isn't clicking after a few minutes, skip it and come back. Points are additive, not sequential.
* **Verify what you built.** The exam grades outcomes, not typing. Start the container, hit the port, confirm the unit is enabled and running — a clean-exit command isn't proof.
* **Keep an eye on the clock but don't panic.** The time budget is generous if you aren't fighting the CLI.

## Resources That Actually Helped

* Red Hat's **Container, Kubernetes and OpenShift Fundamentals (DO188)** course — the training paired with EX188.
* [Building, running, and managing containers (RHEL 9)](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/building_running_and_managing_containers/index) — the best free resource, full stop.
* [Podman documentation](https://docs.podman.io/).
* [Red Hat Developer subscription](https://developers.redhat.com/products/rhel/download) — free RHEL for your lab.

## Closing Thought

Treat EX188 as a **fundamentals** exam, not a hard one. Red Hat is deliberately setting up a shared container base before you specialise into OpenShift or Kubernetes. Get the fundamentals fully automatic here and every downstream exam gets easier.

Next stop for me: doubling down on the OpenShift specialist track. More posts to come.
