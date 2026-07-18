+++
title = 'Engineering Blog and Public Learning System'
date = 2026-04-15T09:00:00+02:00
draft = false
weight = 30
kicker = 'Technical communication'
year = '2026'
summary = 'A Hugo and GitHub Pages publishing workflow for turning hands-on learning into durable, searchable technical notes.'
description = 'A Hugo and GitHub Pages workflow for publishing practical DevOps notes, project case studies, and certification learning.'
stack = ['Hugo', 'GitHub Actions', 'GitHub Pages', 'Markdown']
tags = ['Technical Writing', 'Automation']
+++

## Goal

This site is more than a personal homepage. It is a lightweight publishing system for turning lab work, certification study, and architecture experience into notes that remain useful after the immediate task is finished.

## Design choices

- **Hugo** keeps the site static, fast, and easy to maintain.
- **Markdown** keeps writing portable and reviewable in Git.
- **GitHub Actions** builds the site consistently on every deployment.
- **GitHub Pages** provides a simple hosting path behind a custom domain.
- Structured metadata, RSS, tags, and search make the content easier to discover.

## Publishing workflow

Every article starts as a Markdown file, is reviewed as a normal source change, and is transformed into a production site by the deployment workflow. The source remains the system of record; generated output is deliberately kept out of version control.

That combination keeps the operational overhead low enough that the focus stays on publishing useful engineering work.
