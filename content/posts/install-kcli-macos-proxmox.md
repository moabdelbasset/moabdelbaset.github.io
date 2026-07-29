+++
title = 'Install kcli on macOS and Manage Proxmox VMs'
date = 2026-07-29T10:00:00+02:00
draft = false
description = 'Install kcli on macOS, connect it securely to a Proxmox VE home lab, and provision a cloud-image VM from the command line.'
summary = 'A practical guide to running kcli on a Mac, configuring Proxmox API and SSH access, and creating the first VM from a cloud image.'
tags = ["kcli", "Proxmox", "Homelab", "Automation", "macOS"]
keywords = ["kcli macOS", "kcli Proxmox", "Proxmox automation", "Proxmox API token", "homelab VM provisioning"]
+++

I wanted a repeatable way to create VMs in my Proxmox home lab without clicking through the web interface every time. **kcli** provides one command-line workflow across several infrastructure providers, including Proxmox, and can build VMs directly from cloud images.

This guide covers the complete path I used:

1. Run kcli on macOS.
2. Create a Proxmox API token.
3. Configure passwordless SSH.
4. Prepare Proxmox storage.
5. Store the kcli configuration and token separately.
6. Verify the connection and create the first VM.

I have replaced my own host address and token with placeholders. Do not publish real credentials in a blog post or commit them to Git.

## How kcli communicates with Proxmox

The Proxmox provider uses two separate paths:

- The **Proxmox API on port 8006** is used to manage VM resources.
- **SSH** is used to run host-side image staging commands and upload cloud-init or Ignition files.

This distinction matters. A working API token is not enough to download an image and build a usable cloud-init VM; the Mac running kcli must also be able to reach the Proxmox host over SSH without a password prompt.

## Prerequisites

Before starting, make sure you have:

- A Mac with `zsh`.
- [Homebrew](https://brew.sh/) installed.
- Docker Desktop or Podman available and running.
- A Proxmox VE host reachable from the Mac on ports `22` and `8006`.
- Administrative access to the Proxmox web interface.
- An SSH key on the Mac.

You can test basic network access with:

```bash
ssh root@<PVE_HOST_OR_IP>
curl -k https://<PVE_HOST_OR_IP>:8006/api2/json/version
```

The `-k` option is useful when the home lab uses Proxmox's default self-signed certificate. It should not be necessary when the certificate is signed by a CA trusted by the Mac.

## Install kcli on macOS

kcli's official installer uses a container when it cannot use an RPM or Debian package manager. This is a good fit for macOS because the container contains the dependencies for all providers, including `proxmoxer`.

The example below uses Podman:

```bash
brew install podman
podman machine init
podman machine start
```

If a Podman machine already exists, skip `podman machine init` and start the existing machine.

Download the installer so you can inspect it before running it:

```bash
curl -fsSL \
  https://raw.githubusercontent.com/karmab/kcli/main/install.sh \
  -o /tmp/kcli-install.sh

less /tmp/kcli-install.sh
bash /tmp/kcli-install.sh
```

On macOS I run the script as my normal user because it adds the `kcli` alias to my shell configuration and creates files below my home directory.

Open a new terminal, or reload the zsh configuration:

```bash
source ~/.zshrc
kcli version
```

The generated container alias mounts `~/.kcli` and `~/.ssh` into the kcli container. That allows it to read the provider configuration and use the same SSH key as the Mac.

> If both Docker and Podman are installed, the current installer prefers Podman. Make sure its virtual machine is running before calling `kcli`.

## Create a Proxmox API token

In the Proxmox web interface, open:

**Datacenter → Permissions → API Tokens → Add**

Use these values for an initial home-lab setup:

| Field | Value |
|---|---|
| User | `root@pam` |
| Token ID | `kcli` |
| Privilege Separation | Unchecked |

Proxmox displays the token secret only once. Copy it immediately and store it securely.

Disabling privilege separation lets the token inherit the user's permissions, which is convenient for proving the setup but gives the token broad access. For a long-lived or shared environment, enable privilege separation and assign a dedicated role and ACL with only the permissions kcli needs.

## Configure passwordless SSH

Create an SSH key if the Mac does not already have one:

```bash
ssh-keygen -t ed25519
```

Copy the public key to the Proxmox host:

```bash
ssh-copy-id root@<PVE_HOST_OR_IP>
```

Then verify that SSH no longer prompts for a password:

```bash
ssh root@<PVE_HOST_OR_IP> hostname
```

The command must return the Proxmox node name without asking for a password. This is mandatory because kcli runs image staging commands and transfers cloud-init files over SSH rather than through the API.

## Enable the required storage content types

In the Proxmox web interface, open:

**Datacenter → Storage → local → Edit → Content**

Enable:

- **ISO image**
- **Import**
- **Snippets**

`Snippets` is especially important for cloud-init user data. Without it, a VM can start successfully while missing its injected SSH key, hostname, and other initialization settings.

In this guide:

- `local-lvm` stores VM disks.
- `local` provides kcli's temporary import staging path and stores snippets.
- `<PVE_IMAGE_STORAGE>` stores the reusable cloud-image template.

Change those names if your Proxmox storage is configured differently.

The target image storage must support the Proxmox `images` content type and appear in:

```bash
kcli list pool
```

A storage can exist in `pvesm status` but remain invisible to kcli when it does not support VM images.

## Configure the Proxmox provider

kcli reads its configuration from `~/.kcli`. Create the directory:

```bash
mkdir -p ~/.kcli
```

Create `~/.kcli/config.yml`:

```yaml
default:
  client: homelab
  pool: local-lvm
  numcpus: 2
  memory: 2048

homelab:
  type: proxmox
  host: <PVE_HOST_OR_IP>
  user: root@pam
  auth_token_name: kcli
  auth_token_secret: ?secret
  pool: local-lvm
  imagepool: <PVE_IMAGE_STORAGE>
  node: <PVE_NODE_NAME>
  filtertag: kcli
  verify_ssl: false
```

Use only the Proxmox hostname or IP in `host`. kcli constructs the API URL, so do not enter `https://`, port `8006`, or `/api2/json`.

Create `~/.kcli/secrets.yml` with the real token:

```yaml
homelab:
  auth_token_secret: <PVE_TOKEN_SECRET>
```

Restrict access to the secrets file:

```bash
chmod 600 ~/.kcli/secrets.yml
```

The `?secret` value tells kcli to look up the real value from the matching YAML path in `secrets.yml`. This keeps the token out of the main configuration file, which is much easier to copy or accidentally commit.

### Proxmox provider settings

| Parameter | Purpose |
|---|---|
| `host` | Proxmox hostname or IP, without a URL or port |
| `user` | Proxmox user and realm, such as `root@pam` |
| `auth_token_name` | Token ID only, such as `kcli` |
| `auth_token_secret` | Token secret, resolved from `secrets.yml` here |
| `pool` | Proxmox storage used for VM disks |
| `imagepool` | Storage used for cloud images and ISOs |
| `node` | Target node in a Proxmox cluster |
| `filtertag` | Limits normal kcli VM discovery to resources with this tag |
| `verify_ssl` | Enables or disables TLS certificate verification |

If a credential is written elsewhere as `root@pam!kcli`, split it across the two kcli fields:

```yaml
user: root@pam
auth_token_name: kcli
```

Passing the entire `root@pam!kcli` value as `auth_token_name` results in an authentication failure.

For a lab with the default self-signed Proxmox certificate, `verify_ssl: false` is practical. A better long-term setup is to install a trusted certificate and change it to `true`.

## Keep kcli away from existing VMs

I set:

```yaml
filtertag: kcli
```

With this filter, normal kcli VM listing and management is scoped to VMs carrying the `kcli` tag. Existing workloads that were not created and tagged by kcli stay out of its default view.

This is a useful safety boundary, but it does not replace careful review of destructive commands. Always confirm names and the selected provider before deleting a VM or plan.

## Verify the connection

Run:

```bash
kcli list vm
```

A VM table confirms that API authentication works. If `filtertag` is configured and no kcli-managed VMs exist yet, an empty table is the expected result.

You can explicitly select the provider:

```bash
kcli -C homelab list vm
```

## Download a cloud image

List the images kcli knows how to download:

```bash
kcli list available-images
```

Download a CentOS Stream 9 cloud image:

```bash
kcli download image centos9stream
```

With the current Proxmox provider, kcli opens an SSH session and runs the image download on the Proxmox host. It stages the file under `local`, imports it into `imagepool`, and then removes the staging file. If this step fails after `kcli list vm` succeeded, investigate SSH access, free space on `local`, and the target storage's `images` capability first.

## Create the first VM

Create a VM using the CPU and memory defaults from `config.yml`:

```bash
kcli create vm -i centos9stream testvm
```

kcli injects the local SSH public key through cloud-init.

To override the defaults:

```bash
kcli create vm -i centos9stream \
  -P memory=4096 \
  -P numcpus=4 \
  -P 'disks=[30]' \
  -P 'nets=[vmbr0]' \
  testvm
```

The quotes around list parameters prevent zsh from treating the square brackets as filename patterns.

Inspect the VM and connect:

```bash
kcli info vm testvm
kcli ssh testvm
```

kcli infers the default SSH user from the cloud-image name. Use a recognizable image name such as `centos9stream` so the provider can choose the expected user.

## Useful VM commands

| Task | Command |
|---|---|
| List VMs | `kcli list vm` |
| Show VM details | `kcli info vm testvm` |
| Start a VM | `kcli start vm testvm` |
| Stop a VM | `kcli stop vm testvm` |
| Connect over SSH | `kcli ssh testvm` |
| Add a 5 GB disk | `kcli create vm-disk -s 5 testvm` |
| Change memory | `kcli update vm -P memory=4096 testvm` |
| Clone a VM | `kcli clone -b testvm testvm2` |
| Create a snapshot | `kcli create snapshot vm -n testvm snap1` |
| Delete a VM | `kcli delete vm testvm` |

Most commands also accept `-C homelab` when you want to make the target provider explicit.

## Create a reusable profile

Profiles collect image and hardware settings so they do not have to be repeated on every command. Create `~/.kcli/profiles.yml`:

```yaml
mycentos:
  image: centos9stream
  numcpus: 4
  memory: 4096
  disks:
    - size: 30
  nets:
    - vmbr0
  cmds:
    - dnf -y install vim git
```

Create a VM from the profile:

```bash
kcli create vm -p mycentos myvm
```

## Define multiple VMs in a plan

A plan declares multiple VMs in one YAML file. For example, create `myplan.yml`:

```yaml
parameters:
  image: centos9stream
  memory: 4096

web01:
  image: "{{ image }}"
  memory: "{{ memory }}"
  numcpus: 2
  cmds:
    - dnf -y install httpd
    - systemctl enable --now httpd

db01:
  image: "{{ image }}"
  memory: "{{ memory }}"
  numcpus: 4
  disks:
    - size: 50
```

Create the plan:

```bash
kcli create plan -f myplan.yml myplan
```

Override a parameter at runtime:

```bash
kcli create plan -f myplan.yml -P memory=8192 myplan
```

Delete the plan and its managed resources when they are no longer needed:

```bash
kcli delete plan myplan
```

Review the plan and target provider carefully before running the delete command.

## Troubleshooting

### `401 Unauthorized: Authentication failed!`

Check these items in order:

1. `auth_token_name` contains only the Token ID, not `root@pam!kcli`.
2. The token exists under the same Proxmox user shown in `config.yml`.
3. Privilege separation is disabled, or the token has an explicit ACL.
4. The token secret is under the matching client and key in `secrets.yml`.

Test the token directly:

```bash
curl -k \
  -H "Authorization: PVEAPIToken=root@pam!kcli=<PVE_TOKEN_SECRET>" \
  "https://<PVE_HOST_OR_IP>:8006/api2/json/cluster/resources?type=vm"
```

JSON output means the token works and the likely issue is in the kcli YAML. Another `401` points back to the token or its permissions.

Be careful with shell history when testing a real secret on the command line. Remove the command from history afterward, or load the secret from a protected file instead.

### `kcli list vm` works but image download fails

- Verify passwordless SSH from the Mac to the Proxmox host.
- Confirm that the kcli container can read the expected key from `~/.ssh`.
- Confirm that `imagepool` exactly matches the Proxmox storage name.
- Confirm that `imagepool` appears in `kcli list pool` and supports `images`.
- Confirm that `local` has enough free space for the temporary download.

### The VM starts but SSH is refused

This usually means cloud-init did not apply:

- Confirm that **Snippets** is enabled on the selected storage.
- Use a genuine cloud image rather than a normal installation ISO.
- Inspect the VM's cloud-init drive and settings in Proxmox.
- Confirm that the public key mounted into the kcli container is the one you expect.

### kcli reports a missing Python module

The official kcli container includes provider dependencies. If a locally installed Python version reports a missing module, install the Proxmox extra or inject `proxmoxer` and `requests` into that same Python environment. Do not install them into a different interpreter and expect kcli to find them.

### Podman cannot connect

Confirm that its macOS virtual machine is running:

```bash
podman machine list
podman machine start
```

## Final result

At this point the workflow is:

```bash
kcli download image centos9stream
kcli create vm -i centos9stream testvm
kcli ssh testvm
```

That turns my Mac into a lightweight control point for the Proxmox home lab. I can keep reusable profiles and plans in Git while the API token stays protected in `~/.kcli/secrets.yml`.

The next step is [deploying a single-node k3s Kubernetes cluster with kcli](/posts/deploy-single-node-k3s-proxmox-kcli/).

## References

- [kcli documentation](https://kcli.readthedocs.io/en/latest/)
- [kcli source and installer](https://github.com/karmab/kcli)
- [kcli plan samples](https://github.com/karmab/kcli-plan-samples)
- [Complete kcli parameter sample](https://github.com/karmab/kcli/blob/main/samples/all_parameters.yml)
- [Proxmox VE user and token management](https://pve.proxmox.com/pve-docs/pveum.1.html)
