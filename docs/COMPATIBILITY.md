# Hardware compatibility

| Board | Platform | Status |
| --- | --- | --- |
| MIR63A0-00-P1 / PCA#500240 RevP21 | APQ8016 / MSM8916 | One unit recovered; original kernel 3.10.49-perf-gf46dad5260f |
| Other revisions, including i.MX8 | Different or unverified | No flash profile |

Confirm the printed board label before selecting a profile. An Android product
string or Qualcomm USB ID cannot identify the PCB revision. `--board` records
your confirmation; it does not electronically verify the label.

The software runs on the original board. Physical access to internal USB or the
PCB volume buttons can still be necessary. The tested board has no microSD slot.
Its LCD covers roughly the upper two-thirds of the upright mirror; the rest is
reflection only. Do not expect touch controls.

The original signed boot image/kernel remain essential to the display and board
drivers. A newer Android release needs a separate compatibility project. Android
7.x is an investigation target, not a supported upgrade or an established ceiling.
