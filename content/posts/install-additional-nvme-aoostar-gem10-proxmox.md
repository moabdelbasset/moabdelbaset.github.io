+++
title = 'Install an Additional NVMe SSD in the AOOSTAR GEM10'
date = 2026-08-03T19:45:00+02:00
draft = false
description = 'Install and verify a second NVMe SSD in an AOOSTAR GEM10 running Proxmox VE, then configure it as fast local VM storage.'
summary = 'A practical hardware-to-Proxmox guide for adding a 2 TB Lexar NM790 NVMe SSD to the AOOSTAR GEM10 home-lab server.'
tags = ["AOOSTAR", "Proxmox", "NVMe", "Homelab", "Hardware"]
keywords = ["AOOSTAR GEM10 NVMe", "AOOSTAR GEM10 SSD upgrade", "Proxmox NVMe storage", "Lexar NM790", "Proxmox LVM-Thin"]
+++

My AOOSTAR GEM10 started with a 512 GB NVMe drive for Proxmox VE. As the number of VMs and lab environments grew, I added a **2 TB Lexar NM790 PCIe Gen4 NVMe SSD** to provide a separate, fast storage pool for virtual-machine disks.

This guide covers the complete process: opening the GEM10, reaching the additional M.2 slot, installing the SSD, confirming that Linux sees the correct device, and optionally adding it to Proxmox as LVM-thin storage.

> **Important:** Opening the chassis and moving the motherboard can damage connectors or affect the warranty. Check the documentation for your exact GEM10 revision before continuing, use anti-static precautions, and never work on the computer while it is connected to power.

## Tested hardware

| Component | Value |
|---|---|
| Mini PC | AOOSTAR GEM10 |
| CPU | AMD Ryzen 7 6800H |
| Operating system | Proxmox VE |
| Existing SSD | 512 GB NVMe, used as the OS disk |
| New SSD | Lexar NM790 2 TB PCIe Gen4 NVMe |

AOOSTAR specifies three M.2 2280 NVMe slots for this GEM10 model. The original system disk occupies one slot; the other slots provide room to add fast local storage without replacing the Proxmox boot drive.

## What you need

- A Phillips screwdriver that fits the chassis screws.
- An M.2 2280 NVMe PCIe SSD.
- An anti-static wrist strap, or another suitable way to ground yourself.
- A clean, well-lit work surface and a container for the screws.
- An optional M.2 thermal pad of the correct thickness.

Before changing the hardware, make sure important VMs, containers, and Proxmox configuration are backed up somewhere other than this machine.

## 1. Shut down and disconnect the GEM10

Shut down Proxmox cleanly from the web interface or console. Wait until the system is fully off, then disconnect:

- The power adapter.
- Ethernet.
- USB devices.
- HDMI or DisplayPort cables.

Press the power button once after unplugging the adapter to help discharge any residual power. Move the device to the prepared work surface.

## 2. Remove the bottom cover

Turn the GEM10 upside down and remove the four bottom screws. Keep track of their positions in case the screws are not all the same length.

Lift the bottom cover slowly. The cover contains a cooling fan connected to the motherboard, so do not pull it away from the chassis or put tension on the cable. Rest the cover next to the computer while keeping the cable relaxed, or disconnect the fan by holding the connector rather than pulling on its wires.

<!-- Photo to add when reattached: bottom cover removed, showing the fan and internal layout. -->

## 3. Access the additional M.2 slots

On my unit, the additional NVMe slots were on the opposite side of the motherboard. Reaching them required carefully lifting and turning the board.

1. Take a photo of the cable routing and connector positions before disconnecting anything.
2. Remove the motherboard mounting screws.
3. Disconnect only the fan or ribbon cables that prevent the board from moving safely.
4. Lift the motherboard by its edges and turn it over without scraping it against the chassis.

The internal layout may differ between revisions. Do not force the board if it does not lift freely; stop and look for a missed screw, cable, or connector.

<!-- Photo to add when reattached: motherboard lifted to expose the additional M.2 slots. -->

## 4. Install the new NVMe SSD

Locate an empty M.2 2280 NVMe slot and its retaining screw.

1. Remove the retaining screw.
2. Align the notch in the Lexar NM790 with the key in the M.2 socket.
3. Insert the drive at roughly a 30-degree angle.
4. Push it fully into the connector without forcing it.
5. Lower the free end of the SSD onto the standoff.
6. Reinstall the retaining screw until it is snug.

The SSD should sit flat and should not bow. The retaining screw only needs to hold the drive in place; overtightening it can damage the board or standoff.

<!-- Photo to add when reattached: Lexar NM790 secured in the empty M.2 slot. -->

## 5. Add the thermal pad

If the correct spare thermal pad is available, place it on the newly installed SSD so that it makes contact with the intended heatsink or chassis surface after reassembly. Remove any protective film first.

Do not stack pads or use one that is too thick. Excessive pressure can bend the SSD or motherboard. If there is no matching contact surface, leave the pad out and monitor the drive temperature after booting.

## 6. Reassemble the system

Work back through the disassembly steps:

1. Return the motherboard to its original position.
2. Reconnect every cable that was disconnected.
3. Reinstall the motherboard screws in their original locations.
4. Confirm that the bottom-cover fan is connected.
5. Position the bottom cover without pinching any wires.
6. Reinstall and gently tighten the four case screws.

Before closing the cover, compare the system with the photo taken during disassembly. This is a quick way to catch a missed cable.

## 7. Boot and identify the new disk

Reconnect the network and display if needed, then connect power and start the GEM10. Confirm that Proxmox boots normally before making any storage changes.

From the Proxmox shell, list only physical block devices and include identifying information:

```bash
lsblk -d -o NAME,SIZE,MODEL,SERIAL,TYPE
```

My result showed the two NVMe namespaces:

```text
NAME      SIZE MODEL             SERIAL       TYPE
nvme0n1   1.9T Lexar SSD NM790   <new-serial> disk
nvme1n1 476.9G <existing-model>   <os-serial>  disk
```

In this example, `nvme1n1` is the existing Proxmox system disk and `nvme0n1` is the new 2 TB Lexar drive. **Do not assume those names will be the same on another machine—or even after a future boot.** Match the capacity, model, and serial number before running a destructive command.

The persistent device links are also useful:

```bash
ls -l /dev/disk/by-id/ | grep -i nvme
```

If the `nvme` command is not installed, add the Debian package used by Proxmox:

```bash
apt update
apt install nvme-cli
```

Then display the detected NVMe devices:

```bash
nvme list
```

Example:

```text
Node             SN            Model
/dev/nvme0n1     <new-serial>  Lexar SSD NM790 2TB
/dev/nvme1n1     <os-serial>   <existing OS SSD>
```

Check the health information for the new drive's controller:

```bash
nvme smart-log /dev/nvme0
```

Review at least:

- `critical_warning` — it should be `0` on a healthy new disk.
- `temperature` — check it again under sustained I/O.
- `available_spare`.
- `percentage_used`.
- `media_errors` and error log entries.
- Data units read and written.

Use the controller that corresponds to the Lexar namespace shown by `nvme list`; it may not be `/dev/nvme0` on another system.

## 8. Optionally add the disk to Proxmox

> **Destructive operation:** Initializing, wiping, partitioning, or creating LVM storage erases data on the selected disk. Confirm the Lexar model, serial number, and 2 TB capacity again. Never select the existing Proxmox OS disk.

In the Proxmox web interface:

1. Select the Proxmox **node** in the left tree.
2. Open **Disks → Disks**.
3. Select the new Lexar SSD and verify its model, serial number, and size.
4. If required for the chosen storage workflow, use **Initialize Disk with GPT**.

Proxmox can use the disk in several ways:

| Storage type | Good fit | Main consideration |
|---|---|---|
| LVM-thin | Local VM and container disks | Thin provisioning, snapshots, and clones; not shared between nodes |
| ZFS | Data-integrity features and ZFS workflows | Plan memory use, topology, and redundancy before creating the pool |
| Directory | ISOs, backups, snippets, or file-based VM images | Simple and flexible, with behavior dependent on the filesystem and image format |
| LVM | Local block storage | Does not provide the efficient snapshot and clone support of LVM-thin |

For this single-node home lab, I chose **LVM-thin** for VM disks. It is a straightforward match for fast local storage and supports thin provisioning, snapshots, and clones.

To create it, open **Node → Disks → LVM-Thin** and choose **Create: Thinpool**. Select only the new drive or the volume group created for it, use a clear name such as `fastnvme`, and enable **Add Storage** if the interface offers that option. Review the final selection before confirming; the exact fields can differ slightly between Proxmox VE releases and according to the disk's current state.

After creation, verify that the storage is active:

```bash
pvesm status
```

The result should contain an enabled entry named `fastnvme`. It can now be selected when creating a VM or when moving an existing VM disk.

LVM-thin is thin-provisioned, so allocated virtual sizes can exceed currently used physical blocks. Monitor actual pool usage and keep backups; thin provisioning is not extra physical capacity and does not provide redundancy.

## Verification checklist

- [ ] The SSD is fully inserted and secured.
- [ ] The motherboard and bottom cover are reinstalled correctly.
- [ ] The fan and any ribbon cables are reconnected.
- [ ] Proxmox boots successfully.
- [ ] `lsblk` shows the expected 2 TB model and serial number.
- [ ] `nvme list` identifies the Lexar NM790.
- [ ] The NVMe SMART log has no critical warning or media errors.
- [ ] The new disk—not the OS disk—was selected in Proxmox.
- [ ] `pvesm status` shows `fastnvme` as active, if storage was created.
- [ ] Backups remain on a different physical device or system.

## Troubleshooting

### The SSD is not detected

- Shut down, disconnect power, and reseat the SSD.
- Confirm that the drive is M.2 2280 **NVMe PCIe**, not M.2 SATA.
- Inspect the socket and retaining screw, and try another available NVMe slot if appropriate.
- Check whether the drive appears in the firmware setup.
- Review the kernel messages:

  ```bash
  dmesg -T | grep -i nvme
  ```

### The system does not boot

- Disconnect power and recheck the fan and ribbon cables.
- Confirm that the motherboard is seated correctly and no cable is trapped below it.
- Check for a missed or misplaced mounting screw.
- Temporarily remove the new SSD and test the original configuration.

### The disk appears in firmware but not in Linux

Check both the NVMe tool and PCI device list:

```bash
nvme list
lspci -nn | grep -i 'non-volatile'
dmesg -T | grep -i nvme
```

If the controller appears in `lspci` but no namespace is available, inspect the NVMe and kernel messages before attempting to initialize anything.

### The SSD runs hot

Confirm that the cooling pad has made proper contact and that the bottom fan is connected and unobstructed. Compare idle and load temperatures with `nvme smart-log`; a single reading immediately after boot does not show sustained-workload behavior.

## Final result

The GEM10 now has its original 512 GB Proxmox system disk plus a dedicated 2 TB Lexar NM790 for VM and container storage. Keeping the OS and lab workloads on separate devices gives the home lab more capacity and makes storage placement easier to reason about.

This new pool also gives my [kcli-based Proxmox workflow](/posts/install-kcli-macos-proxmox/) more room for repeatable Kubernetes and OpenShift test environments.

## References

- [AOOSTAR GEM10 product specifications](https://aoostar.com/eo/products/aoostar-gem10-amd-ryzen-7-7735hs-mini-pc-with-win-11-pro-3-nvme-oculink-2-2-5g-lan)
- [Proxmox VE Administration Guide](https://pve.proxmox.com/pve-docs/pve-admin-guide.html)
- [Proxmox VE Storage Manager documentation](https://pve.proxmox.com/pve-docs/pvesm.1.html)
- [nvme-cli documentation](https://github.com/linux-nvme/nvme-cli)
