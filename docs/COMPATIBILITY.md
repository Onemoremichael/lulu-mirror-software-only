# Hardware compatibility

Target coverage is every original-board lululemon MIRROR combination. Current
evidence is much narrower. The [hardware registry](../hardware/README.md) tracks
observations and investigations; `profiles/` contains executable recovery
permissions, not a catalog of every board we want to support.

| Board | Platform | Status |
| --- | --- | --- |
| MIR63A0-00-P1 / PCA#500240 RevP21 | APQ8016 / MSM8916 | One unit recovered; original kernel 3.10.49-perf-gf46dad5260f |
| All other or unidentified combinations | Unknown until reported and investigated | Welcome for intake; no flash profile |

References to other chipset families (including i.MX8) are research leads, not
verified board identities or supported recovery procedures in this repository.
Do not infer a board population from this table. Add evidence through a
[board report](../CONTRIBUTING.md#1-report-your-hardware).

Confirm the printed board label before selecting a profile. An Android product
string or Qualcomm USB ID cannot identify the PCB revision. `--board` records
your confirmation; it does not electronically verify the label.

A matching board label is necessary for the current profile, but not sufficient
proof of firmware/peripheral compatibility. Record the boot firmware, storage
geometry, kernel and peripheral differences as separate combination evidence.
Unknown boards must not use `inspect --board mir63a0-revp21`, `plan` or `flash`
as a discovery mechanism. `doctor` and `devices` need no board selection; see the
[intake process](../CONTRIBUTING.md) for what to share when ADB is unavailable.

The software runs on the original board. Physical access to internal USB or the
PCB volume buttons can still be necessary. The tested board has no microSD slot.
Its LCD covers roughly the upper two-thirds of the upright mirror; the rest is
reflection only. Do not expect touch controls.

On the current RevP21 route, the original signed boot image/kernel remain essential to the display and board
drivers. A newer Android release needs a separate compatibility project. Android
7.x is an investigation target, not a supported upgrade or an established ceiling.
