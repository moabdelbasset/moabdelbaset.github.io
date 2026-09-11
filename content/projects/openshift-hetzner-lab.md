+++
title = 'OpenShift Lab on a Hetzner Dedicated Server'
date = 2026-09-07T09:00:00+03:00
draft = false
weight = 15
kicker = 'OpenShift infrastructure lab'
year = '2026'
summary = 'A three-node OpenShift lab on one Hetzner dedicated server, deployed with Ansible, KVM/libvirt, and the Assisted Installer.'
description = 'Deploying a compact OpenShift lab on a Hetzner dedicated server with Ansible automation, KVM/libvirt networking, and the Red Hat Assisted Installer.'
stack = ['OpenShift', 'Ansible', 'KVM/libvirt', 'Hetzner', 'Assisted Installer']
tags = ['OpenShift', 'Ansible', 'Infrastructure', 'Homelab']
+++

## Why I built it

I wanted a remote OpenShift environment for hands-on administration practice. A Hetzner dedicated server provided a single host for running a compact cluster while giving me practical experience with the virtualization, networking, and installation steps underneath it.

The project brought those pieces together into a working lab: three OpenShift nodes running as virtual machines, access to the web console, and CLI access from my laptop.

## Architecture

All three nodes run on the same physical server and carry the control-plane, master, and worker roles. KVM/libvirt provides the virtual machines and their NAT network, while the Red Hat Assisted Installer handles cluster discovery and installation.

| Component | Role in the lab |
| --- | --- |
| Hetzner dedicated server | Physical host for the virtualized cluster |
| KVM/libvirt | Virtual machines and an internal NAT network |
| Three OpenShift nodes | Compact cluster combining control-plane and worker roles |
| Host port forwarding | Sends TCP 6443 to the API VIP and TCP 443 to the ingress VIP |
| Ansible and Make targets | Prepare the host, configure networking, validate prerequisites, and deploy the lab VMs |
| Assisted Installer | Discovers the hosts from a boot ISO and installs OpenShift |

This is a learning environment with a shared physical failure domain. Three control-plane VMs do not provide resilience against the dedicated server failing.

## My implementation work

I followed and adapted [Amedeos's installation guide](https://amedeos.github.io/openshift/2026/06/29/Install-OpenShift-Assisted-Installer-lab-on-Hetzner.html) and used the upstream [ocp-assisted-in-the-jars automation](https://github.com/amedeos/ocp-assisted-in-the-jars). Credit for the original guide and automation belongs to that project; my work here was deploying the environment, configuring it for my lab, and documenting the process and results.

The deployment covered:

- Installing Ansible and the required collections on the server.
- Configuring secrets and encrypting the vault and Red Hat pull secret with Ansible Vault.
- Preparing the hypervisor, libvirt NAT network, IP forwarding, and API/ingress port forwarding.
- Running preflight checks for virtualization support, networking, available memory, disk space, and the base image.
- Generating an SSH key and an Assisted Installer discovery ISO, then placing the ISO at the path expected by the automation.
- Booting the control-plane VMs, configuring the API and ingress VIPs, and completing the cluster installation.
- Configuring local hostname resolution and validating access from my laptop.

## Practical details

The deployment required coordinating the automation with the Assisted Installer console. I created the cluster and discovery image in the console, then supplied that image to the VM deployment workflow. When the playbook prompted for the ISO, I copied it into the expected libvirt image location before continuing.

Access also depended on both hostname resolution and forwarding traffic to the correct internal VIP. For the documented deployment, I added local hosts-file entries for the API, console, and OAuth endpoints. During the later [Flask GitOps delivery project](/projects/gitops-flask-openshift/), I completed that follow-up: switching the cluster records in Cloudflare to DNS only restored access without local hosts-file overrides.

## Verified outcome

After installation, I accessed the OpenShift console and queried the cluster from my laptop using its downloaded kubeconfig. The documented `oc get nodes` output showed all three nodes reporting `Ready`, each with the control-plane, master, and worker roles.

That validates the initial deployment and client access. Storage integration, including the external Ceph/ODF setup mentioned in the installation notes, is outside the verified outcome of this case study.

## Installation notes and references

The wiki contains the step-by-step commands, installation screenshots, and validation output:

- [My OpenShift on Hetzner installation walkthrough](https://github.com/moabdelbasset/home-lab/wiki/Install-Openshift-Cluster-on-Hetzner-server)
- [Original installation guide by Amedeos](https://amedeos.github.io/openshift/2026/06/29/Install-OpenShift-Assisted-Installer-lab-on-Hetzner.html)
- [Upstream Ansible automation](https://github.com/amedeos/ocp-assisted-in-the-jars)
