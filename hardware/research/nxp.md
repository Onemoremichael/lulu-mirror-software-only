# NXP i.MX8M Mini research lead

Status: **researched external reports; no executable profile and no independently
validated software-only entry point here**. Claims **n01–n05** and their source
access limitations are recorded in [catalog.json](catalog.json).

## What supports the lead

The [owner discussion](https://www.reddit.com/r/hardwarehacking/comments/17ii9bn/lululemon_studio_mirror/)
contains technical replies with a PCB-label transcription, shell output and boot
logs. Some replies were accessible through indexed thread excerpts but omitted
by the live reader; we have not upgraded that into our own label inspection.

The linked first-person [Making Lululemonade](https://failedattempts.neocities.org/)
writeup independently supplies its author's stated scope and describes a
hardware-assisted approach. It is a continuation of that owner's evidence trail,
not a second independent implementation. Its [JTAG page](https://failedattempts.neocities.org/jtag-to-adb)
was read directly over HTTPS. The opening [boot-log material](https://failedattempts.neocities.org/part3a.html)
was reviewed, not the entire large page or its embedded exploit implementation.
No commands from those pages were executed.

The software-branch string in a boot log must not be promoted into a confirmed
stock Android release or SDK. Exact fingerprint, RAM/eMMC capacities, panel,
camera/audio/radio parts, wiring and signing policy remain unresolved here.
There is also no demonstrated identity equivalence to the community's Rev08
designation; don't fill that gap from assumptions about which model came later.

## Implications for the project

This family warrants its own access/build investigation. Our Qualcomm ISP shim,
kernel modules, binary patches, userdata geometry and signing observations do
not transfer. Shared concepts—artifact provenance, owner authorization, precise
write boundaries and non-touch UI—still do.

[NXP's component documentation](https://www.nxp.com/products/i.MX8MMINI) can help
interpret capabilities, but it is not a MIRROR board schematic. A development-kit
image or generic i.MX port is not a replacement image for this unit.

Highest-value next evidence: direct dated comment/photo confirmation of the PCB
label, same-unit chip identity, allowlisted stock OS identity and lawful
board-specific build inputs. A software-only bootstrap must be demonstrated
separately; soldered debug access is not relabeled to satisfy that goal.
