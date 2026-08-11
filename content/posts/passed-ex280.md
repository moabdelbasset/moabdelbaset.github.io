+++
title = 'I Passed EX280: Red Hat OpenShift Administrator'
date = 2026-08-11T08:20:00+02:00
draft = false
description = 'I passed the Red Hat EX280 exam and became a Red Hat Certified System Administrator in OpenShift. Here is what helped me prepare.'
summary = 'A personal reflection on passing EX280 through official Red Hat training, objective-driven study, documentation, and hands-on OpenShift practice in my home lab.'
tags = ["OpenShift", "Kubernetes", "Red Hat", "Certifications", "Homelab"]
keywords = ["EX280", "Red Hat Certified System Administrator in OpenShift", "OpenShift certification", "EX280 preparation", "OpenShift homelab"]
+++

It is official: I **passed the Red Hat Certified System Administrator in OpenShift exam (EX280)**.

This is an important milestone in my OpenShift journey. The result represents many hours of official training, reading documentation, rebuilding lab environments, troubleshooting mistakes, and repeating tasks until the workflow became familiar.

In my earlier post, [Road to EX280: Preparing for OpenShift Administration](/posts/preparing-for-ex280/), I described the plan I was following. Passing the exam confirms that the combination of structured learning and consistent hands-on practice worked for me.

This post contains no exam questions, tasks, or confidential details. I am only sharing the preparation methods and lessons that helped me.

## The preparation approach that worked for me

My preparation was built around four main areas:

1. Official Red Hat training.
2. The published EX280 objectives and Red Hat documentation.
3. A repeatable OpenShift home lab.
4. Personal notes and continuous review.

Each part supported the others. The training provided structure, the objectives defined the destination, the home lab turned theory into practical experience, and writing notes exposed the areas I did not yet understand well enough.

## Starting with official Red Hat training

I took the official training from **Red Hat**. It gave me a clear path through OpenShift administration instead of approaching the platform as a collection of unrelated commands.

The training helped me connect topics such as application deployment, authentication, authorization, routes, services, network policies, resource controls, Operators, and application security. More importantly, it showed how these resources interact inside a real OpenShift cluster.

Completing the training was not the end of the preparation. EX280 is a performance-based exam, so understanding a concept is only useful if I can configure it, verify it, and troubleshoot it under time pressure.

## Treating the official objectives as a checklist

I followed the [official EX280 exam objectives](https://www.redhat.com/en/services/training/red-hat-certified-openshift-administrator-exam) rather than relying on a random collection of tutorials.

For every objective, I tried to answer five questions:

1. What does this resource or feature do?
2. Can I configure it from the command line?
3. Can I inspect and verify the resulting state?
4. Can I recognize and fix a broken configuration?
5. Can I repeat the task without copying a prepared command?

This approach kept the study plan focused. It also changed the goal from memorizing syntax to proving that the required result was actually working.

## Building an OpenShift lab with kcli

The most valuable part of my preparation was hands-on practice. I used **kcli** in my Proxmox home lab to deploy OpenShift environments for testing and study.

A repeatable lab allowed me to:

- Start with a clean cluster.
- Practise the same objective several times.
- Break configurations intentionally.
- Diagnose problems using events, logs, YAML, and resource status.
- Delete the environment and rebuild it when necessary.

Automating the infrastructure removed much of the fear of making mistakes. If an experiment went badly, the cluster was disposable. That made it easier to explore, troubleshoot, and learn how OpenShift behaves beyond the happy path.

I documented the foundation of this home-lab workflow in [Install kcli on macOS and Manage Proxmox VMs](/posts/install-kcli-macos-proxmox/).

## Writing and reviewing my notes

I kept my EX280 study notes in a public GitHub repository:

**[moabdelbasset/ex280-v414](https://github.com/moabdelbasset/ex280-v414)**

Writing notes was more useful than saving commands in shell history. It forced me to explain what a command changed, why it worked, and how I could verify the outcome.

The repository also gave me a practical revision tool. Before the exam, I could return to a topic, compare it with the official objectives, and identify areas that needed another lab session.

The notes began around OpenShift 4.14, while exam versions and product behavior continue to evolve. I therefore treated the objectives and documentation for my booked exam as authoritative and retested older notes where necessary.

## What passing EX280 reinforced

The biggest lesson from this experience is that **hands-on repetition matters more than passive reading**.

Reading documentation helped me understand the available resources and options. Repeated lab work helped me use that information quickly, recognize incorrect states, and recover from mistakes.

A few habits made a real difference:

- Read the required outcome carefully before making changes.
- Use the documentation as a working tool instead of trying to memorize everything.
- Verify resources with YAML, conditions, events, logs, and connectivity tests.
- Practise troubleshooting, not only successful deployments.
- Make sure configurations are persistent and survive the conditions required by the task.
- Build command-line fluency with `oc`, resource discovery, `oc explain`, selectors, and structured output.

The exam result is valuable, but the deeper benefit is the confidence gained from operating OpenShift repeatedly in a real environment.

## What comes next

Passing EX280 is not the end of the OpenShift journey. I plan to keep using the home lab, improve the GitHub notes, and apply these administration skills to more complex Kubernetes and OpenShift scenarios.

I also want to spend more time on automation, advanced troubleshooting, platform reliability, and the operational practices needed to run OpenShift beyond individual exam objectives.

For now, I am happy to celebrate this milestone:

**EX280 passed — Red Hat Certified System Administrator in OpenShift achieved.**

## Resources

- [Official EX280 exam page and objectives](https://www.redhat.com/en/services/training/red-hat-certified-openshift-administrator-exam)
- [My EX280 preparation post](/posts/preparing-for-ex280/)
- [My EX280 notes on GitHub](https://github.com/moabdelbasset/ex280-v414)
- [Install kcli on macOS and Manage Proxmox VMs](/posts/install-kcli-macos-proxmox/)
