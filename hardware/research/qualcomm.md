# Qualcomm research cluster

All claims here are **researched**, not newly verified hardware. Full locators,
source revisions, limits and validation tasks are in [catalog.json](catalog.json).
This cluster is not one interchangeable board model.

## Firmware and access

Claims **q01–q03** describe the external
[stock-firmware profile](https://github.com/TimStewartJ/lululemon-mirror-repurpose/blob/2f2f31c3446c80f58af29254c20945f7f01792e3/docs/supported-devices.md)
and its [machine-readable identity checks](https://github.com/TimStewartJ/lululemon-mirror-repurpose/blob/2f2f31c3446c80f58af29254c20945f7f01792e3/tools/device-profiles/ifc6309-mirror-329.json).
Its app-level reuse approach preserves the installed OS and requires an
authorized connection. That is a potentially less invasive route for the exact
documented starting state, not evidence that every stock unit authorizes ADB.
The [OS investigation](https://github.com/TimStewartJ/lululemon-mirror-repurpose/blob/2f2f31c3446c80f58af29254c20945f7f01792e3/docs/os-replacement.md)
records signing barriers. Neither external result validates our rebuilt image.

Our [RevP21 record](../boards/mir63a0-revp21.md) describes a separate system
reconstruction. Do not confuse a reconstructed build fingerprint with a stock
fingerprint, or assume this external firmware profile identifies a PCB revision.

## Component leads

Claims **q04–q07** capture the [MDME teardown author's identifications](https://mdthats.me/projects/lululemon-smart-mirror-p1/).
The component map provides candidates for camera, radio, audio and power research,
but its PCB revision is not established here. Its memory-package interpretation
is explicitly a guess; we did not turn that marking into a RAM/storage capacity.
Claims **p04/r03** preserve the panel association and amplifier-rating caveat.

Claim **q08** records a [separate owner's UART log](https://github.com/olm3ca/mirror/issues/11#issuecomment-2089160907).
The boot/display strings are useful cross-checks, not permission to adopt another
unit's firmware, switches, serial pinout or write geometry.

## Source/build leads, not ready-made upgrades

Claims **q09/q10** distinguish the silicon specification from the Inforce
[reference-platform Nougat announcement](https://ir.penguinsolutions.com/news/news-details/2018/Android-Nougat-7-for-Inforce-Snapdragon-410-Based-Platforms/default.aspx).
A BSP release existing does not prove its availability, licensing, MIRROR device
tree coverage or acceptance by the OEM signer. Do not replace signed boot
components to find out. The documented first-path reproduction gaps remain in
[BUILD.md](../../docs/BUILD.md).

## Missing joins that would materially help

One independent, redacted report tying together PCB/PCA revision, visible SoC,
stock fingerprint, memory/storage observations, panel, camera and audio boards
would be more valuable than several additional reposts of a chipset name.
We have not proved that the external stock-firmware unit, MDME teardown, UART
owner and our RevP21 unit share an identical BOM. Keep those observations separate.
