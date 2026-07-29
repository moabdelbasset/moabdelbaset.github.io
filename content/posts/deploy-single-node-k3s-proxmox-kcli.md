+++
title = 'Deploy a Single-Node k3s Kubernetes Cluster on Proxmox with kcli'
date = 2026-07-29T18:00:00+02:00
draft = false
description = 'Deploy a single-node k3s Kubernetes cluster on Proxmox with kcli, including storage selection, troubleshooting, kubeconfig setup, and validation.'
summary = 'A tested kcli workflow for deploying k3s on Proxmox, with the storage and kubeconfig problems I hit along the way.'
tags = ["Kubernetes", "k3s", "kcli", "Proxmox", "Homelab"]
keywords = ["k3s Proxmox", "kcli Kubernetes", "single-node Kubernetes", "Proxmox Kubernetes cluster", "k3s homelab"]
+++

After connecting kcli to my Proxmox home lab, I wanted to test more than basic VM creation. Deploying a small Kubernetes cluster exercises the complete automation path: API authentication, cloud-image import, cloud-init, bridge networking, SSH, cluster installation, and kubeconfig generation.

This post continues from [Install kcli on macOS and Manage Proxmox VMs](/posts/install-kcli-macos-proxmox/). That guide covers the API token, passwordless SSH, provider configuration, and first VM.

The result here was a working **single-node k3s cluster running Kubernetes v1.36.2**, provisioned in roughly **70 seconds** on a Proxmox VM with 2 vCPUs, 4 GB of memory, and a 20 GB disk.

All private IP addresses and credentials have been replaced with placeholders.

## Why start with k3s?

My longer-term goal is to test more demanding Kubernetes and OpenShift deployments. Starting with k3s gave me a fast way to validate the Proxmox pipeline before spending significantly more CPU, memory, storage, and time.

| Area | Single-node k3s | OpenShift SNO |
|---|---|---|
| Node provisioning | Cloud-init on a normal cloud image | Ignition on RHCOS |
| Pull secret | Not required | Required |
| Temporary bootstrap VM | No | Yes for the installer workflow |
| Lab footprint used here | 2 vCPU, 4 GB RAM, 20 GB disk | Much larger |
| Deployment time observed | About 70 seconds | Usually much longer |

A successful k3s deployment does not prove that every OpenShift-specific path will work. It does prove most of the shared Proxmox plumbing at a much lower troubleshooting cost.

## Prerequisites

Before continuing, verify that:

- kcli is configured with a working Proxmox provider.
- Passwordless SSH works from the kcli environment to the Proxmox host.
- The Mac can reach the Proxmox API and VM network.
- `kubectl` is installed on the Mac.
- A DHCP lease is available on the Proxmox bridge, or static networking is prepared.
- The Proxmox storage layout has enough room for a cloud image and VM disk.

Check the provider and existing VMs:

```bash
kcli -C homelab list vm
```

## Inspect the k3s defaults

kcli exposes the parameters accepted by each cluster type:

```bash
kcli info cluster k3s
```

The defaults relevant to this deployment were:

```text
api_ip: None
cluster: myk3s
ctlplanes: 1
disk_size: 10
domain: karmalabs.corp
image: ubuntu2004
memory: 1024
network: default
numcpus: 2
pool: None
sdn: flannel
token: supersecret
workers: 0
```

`ctlplanes: 1` and `workers: 0` already describe a single-node cluster. I changed the remaining values to fit the home lab:

| Default | Reason to change it | Value used |
|---|---|---|
| `image: ubuntu2004` | I wanted a current image already used in the lab | `centos9stream` |
| `memory: 1024` | Too tight once workloads are added | `4096` |
| `disk_size: 10` | Limited room for container images | `20` |
| `network: default` | This is normally a Libvirt network | `vmbr0` |
| `pool: None` | Proxmox disk storage should be explicit | `local-lvm` |
| `token: supersecret` | A published default is not a secret | A generated token |
| `domain: karmalabs.corp` | Not my lab domain | `lab.example.com` |

An `api_ip` is not required for one control-plane node. kcli requires one for a non-cloud, multi-control-plane deployment where a stable API endpoint is needed.

## Diagnose Proxmox storage before deploying

My first image download failed with:

```text
Image centos9stream not Added because storage local not found on pve.
```

The message suggested that `local` did not exist, but Proxmox showed it as active:

```bash
ssh root@<PVE_HOST_OR_IP> pvesm status
```

I then inspected the storage configuration:

```bash
ssh root@<PVE_HOST_OR_IP> "cat /etc/pve/storage.cfg"
```

Finally, I compared it with kcli's view:

```bash
kcli list pool
```

The useful diagnostic sequence is:

1. `pvesm status` — does the storage exist and is it active?
2. `/etc/pve/storage.cfg` — which content types does it support?
3. `kcli list pool` — which storage can kcli actually use?
4. Compare the last two results.

### Why `local` was missing from kcli

The relevant storage capabilities in my lab looked like this:

| Storage | Backing device | Relevant content | Visible to kcli |
|---|---|---|---|
| `local` | Internal NVMe directory | `import`, `snippets`, `iso` | No |
| `local-lvm` | Internal NVMe LVM-thin | `images`, `rootdir` | Yes |
| `external4tb` | External LVM-thin | `images`, `rootdir` | Yes |
| `external1tb` | External directory | `images`, `iso`, `snippets` | Yes |

kcli's Proxmox provider filters its pool list to active storage with the **`images` content type**. The `local` storage existed, but it did not support `images`, so it was deliberately absent from `kcli list pool`.

This distinction explains the misleading "storage not found" error: it means "not available as a VM-image storage to this provider," not necessarily "missing from Proxmox."

## Choose storage based on workload

I initially considered placing everything on the external drives. That would have saved NVMe capacity, but Kubernetes control-plane storage is latency-sensitive. VM disks belong on the lowest-latency reliable device available.

The split I used was:

```yaml
pool: local-lvm
imagepool: external1tb
```

- **`pool: local-lvm`** keeps the running VM disk on internal NVMe.
- **`imagepool: external1tb`** stores the reusable cloud-image template on capacity-oriented storage.

The current kcli Proxmox provider also uses the conventional `local` directory for two internal tasks:

- It stages image downloads under `/var/lib/vz/images/0` before importing them into `imagepool`.
- It uploads cloud-init metadata and user data to `/var/lib/vz/snippets` and references `local:snippets/...`.

That means `local` still needs enough temporary free space and the `snippets` content type, even when it does not appear in `kcli list pool`.

> Storage names and hardware differ between labs. The rule is more important than my specific names: place the running control-plane disk on reliable low-latency storage, select an `images`-capable `imagepool`, and keep kcli's `local` staging and snippets paths available.

## Confirm the provider configuration

The relevant parts of my `~/.kcli/config.yml` were:

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
  auth_token_name: <TOKEN_ID>
  auth_token_secret: ?secret
  pool: local-lvm
  imagepool: external1tb
  node: pve
  filtertag: kcli
  verify_ssl: false
```

The actual token remains in `~/.kcli/secrets.yml`, not in this file.

## Create the k3s parameter file

Generate a strong cluster token:

```bash
openssl rand -hex 32
```

Create `k3s-single.yml`:

```yaml
cluster: k3slab
domain: lab.example.com
ctlplanes: 1
workers: 0
image: centos9stream
numcpus: 2
memory: 4096
disk_size: 20
network: vmbr0
pool: local-lvm
token: <GENERATED_CLUSTER_TOKEN>
sdn: flannel

# Optional: pin the exact version used in this walkthrough.
install_k3s_version: v1.36.2+k3s1
```

Do not commit a real cluster token to Git. Store a private parameter file outside the repository or inject the value securely in a repeatable automation workflow.

Leaving out `install_k3s_version` follows the k3s stable channel instead. That is convenient for experiments but makes future runs less reproducible.

## Download the cloud image

Download CentOS Stream 9:

```bash
kcli download image centos9stream
```

The successful run downloaded roughly 1.5 GB in about 15 seconds.

The download speed surprised me until I checked the provider implementation and command output. kcli opens an SSH session and runs `curl` on the **Proxmox host**. It does not carry the entire image through the Mac. The host downloads to the temporary `local` staging path, Proxmox imports it into `imagepool`, and kcli removes the temporary file.

The practical consequences are:

- Download speed depends on the Proxmox host's internet connection.
- The Mac's Wi-Fi is not carrying the image payload.
- `local` needs enough free space for the temporary file.
- The target `imagepool` must appear in `kcli list pool`.

## Deploy the cluster

Run:

```bash
kcli create cluster k3s \
  --paramfile k3s-single.yml \
  k3slab
```

During my run, kcli:

1. Created and booted `k3slab-ctlplane-0`.
2. Applied hostname, network, SSH keys, and other cloud-init settings.
3. Acquired a DHCP lease on `vmbr0`.
4. Installed the guest and SELinux dependencies.
5. Installed and started k3s.
6. Waited for the node and generated a per-cluster kubeconfig.

The final output was:

```text
k3slab-ctlplane-0 deployed on homelab
K3s cluster k3slab deployed!!!
INFO export KUBECONFIG=$HOME/.kcli/clusters/k3slab/auth/kubeconfig
INFO export PATH=$PWD:$PATH
```

The complete deployment took approximately 70 seconds in this lab. Treat that as an observation, not a benchmark; image caching, storage, CPU, DNS, and internet speed all affect the result.

## Use the correct kubeconfig

My first `kubectl get nodes` failed with an authentication error mentioning a completely unrelated GKE plugin. The new cluster was healthy; `kubectl` had fallen back to my existing `~/.kube/config`, whose current context pointed to an old GKE cluster.

kcli writes a separate kubeconfig for each cluster and does not replace the default file. Export the path printed at the end of the deployment:

```bash
export KUBECONFIG="$HOME/.kcli/clusters/k3slab/auth/kubeconfig"
```

Then validate the cluster:

```bash
kubectl config current-context
kubectl cluster-info
kubectl get nodes -o wide
kubectl get pods -A
kubectl get storageclass
```

If `kubectl` reports an unexpected server address or authentication provider, check these before troubleshooting the cluster:

```bash
printf '%s\n' "$KUBECONFIG"
kubectl config current-context
kubectl config view --minify
```

### Add a small zsh helper

For repeated use, add this function to `~/.zshrc`:

```bash
kubeswitch() {
  export KUBECONFIG="$HOME/.kcli/clusters/$1/auth/kubeconfig"
  kubectl config current-context
}
```

Reload the shell and select a cluster by name:

```bash
source ~/.zshrc
kubeswitch k3slab
```

## What the single-node cluster includes

The default k3s installation provides:

- **Flannel** for pod networking.
- **Traefik** as the ingress controller.
- **Local Path Provisioner** for local persistent volumes.
- **SQLite** as the single-server datastore when no other datastore is configured.

Inspect the installed components:

```bash
kubectl get pods -A
kubectl get storageclass
```

SQLite is suitable for this simple single-server lab. Multi-server high availability requires embedded etcd or a supported external datastore.

## Troubleshooting notes

### Storage exists but kcli says it is not found

Check whether it supports `images` and appears in:

```bash
kcli list pool
```

Do not rely on `pvesm status` alone.

### The image download fails

Check:

- Passwordless SSH from the kcli environment to Proxmox.
- Free space under `local` for the staging file.
- The exact `imagepool` name.
- The `images` content type on the target storage.
- Proxmox host DNS and outbound internet access.

### The VM boots but cloud-init settings are missing

Check:

- The `snippets` content type on `local`.
- Files under `/var/lib/vz/snippets` on the Proxmox host.
- The VM's `cicustom` and cloud-init drive configuration.
- Whether `centos9stream` is a genuine cloud image.

### `kubectl` mentions the wrong cluster

Check `KUBECONFIG` and the current context before assuming the k3s deployment failed:

```bash
printf '%s\n' "$KUBECONFIG"
kubectl config current-context
```

### Benign messages observed during deployment

I also saw warnings about the QEMU guest-agent service being registered before its virtio port appeared, and host `iptables-save` tools not being present. The deployment completed because k3s provides its own iptables tooling. These messages are useful context if networking later behaves unexpectedly, but neither blocked this lab run.

## Clean up the cluster

When finished:

```bash
kcli delete kube k3slab
kcli list vm
```

The second command checks for an orphaned cluster VM. My provider uses `filtertag: kcli`, which keeps untagged pre-existing VMs outside kcli's normal view and acts as a useful guardrail. I still review the selected provider and resource names before every delete operation.

## What this deployment proved

This run validated:

- Proxmox API-token authentication.
- Image download and import.
- Cloud-init metadata and SSH-key injection.
- Bridge networking through `vmbr0`.
- DHCP for the cluster node.
- kcli's k3s installation and wait logic.
- Per-cluster kubeconfig generation.

It did not validate OpenShift-specific requirements such as RHCOS, Ignition, an installer bootstrap VM, a highly available API endpoint, or the larger control-plane storage footprint.

## Final lessons

1. kcli lists Proxmox pools that are active and support `images`.
2. `local` still handles temporary image staging and cloud-init snippets.
3. The Proxmox host downloads the cloud image; the Mac orchestrates the process.
4. Running control-plane disks belong on reliable, low-latency storage.
5. A one-node k3s cluster does not need a separate `api_ip`.
6. Always export the kubeconfig generated for the cluster.
7. k3s is a fast, practical validation step before attempting a larger Kubernetes or OpenShift deployment.

## References

- [kcli Kubernetes cluster documentation](https://kcli.readthedocs.io/en/latest/#deploying-kubernetes-openshift-clusters)
- [kcli Proxmox provider source](https://github.com/karmab/kcli/blob/main/kvirt/providers/proxmox/__init__.py)
- [kcli k3s defaults](https://github.com/karmab/kcli/blob/main/kvirt/cluster/k3s/kcli_default.yml)
- [k3s cluster datastore documentation](https://docs.k3s.io/datastore)
- [k3s networking documentation](https://docs.k3s.io/networking/basic-network-options)
- [k3s v1.36.2+k3s1 release](https://github.com/k3s-io/k3s/releases/tag/v1.36.2%2Bk3s1)
- [Proxmox VE storage documentation](https://pve.proxmox.com/pve-docs/pvesm.1.html)
