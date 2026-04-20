+++
title = 'Road to EX374: Developing Automation with Ansible'
date = 2026-04-20T22:45:00+02:00
draft = false
tags = ["Ansible", "Red Hat", "Automation", "Certifications", "AAP"]
+++

I have officially started my preparation for the **Red Hat Certified Specialist in Developing Automation with Ansible Automation Platform (EX374)** exam. This exam is a deep dive into the modern Ansible ecosystem, focusing on execution environments, automation controller, and professional content development.

## Official Exam Objectives
To keep my study focused, I am following the official Red Hat objectives closely:
* [Official EX374 Exam Objectives](https://www.redhat.com/en/services/training/red-hat-certified-specialist-developing-automation-ansible-automation-platform-exam)

## My Lab Setup & Installation
For my lab environment, I am using a containerized installation of **Ansible Automation Platform (AAP) 2.6**. Setting this up correctly is the first hurdle, and I found an excellent guide that covers the "All-In-One" containerized deployment.

* **Key Resource:** [Installing AAP 2.6 via Containerized Version](https://www.youtube.com/watch?v=9KeofmpeHmw) by Waldirio Pinheiro.
* **Note:** This video was instrumental in getting my Proxmox-based lab up and running, especially the parts about configuring the subscription manifest and setting up the service account for the registry.

## Study & Practice Sessions
I am also following a dedicated series of practice sessions that walk through each objective. It’s one thing to read the documentation, but seeing the "GitOps" workflow and branch management in action is much more effective.

* **Study Playlist:** [Red Hat EX374 Practice Sessions](https://www.youtube.com/watch?v=kQyDWocyqHw&list=PLgYy5YCbiYbFLDLZN5XzgM40_neATEhd1) by Eddie Jennings.
* I am starting with the "Understand and use Git" section to ensure my automation content is version-controlled and ready for CI/CD pipelines.

## Current Progress
Currently working through:
* **Developing Content:** Writing modular and reusable playbooks.
* **Execution Environments:** Building and managing containerized environments for automation.
* **Ansible Navigator:** Moving away from `ansible-playbook` to the modern `ansible-navigator` CLI.

Stay tuned for more deep dives into my lab challenges!
