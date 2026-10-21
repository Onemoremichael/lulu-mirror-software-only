# Hardware registry and investigation map

This is the community's entry point for **every original-board lululemon MIRROR**,
including locked and unidentified units. We aim to find software-only paths for
all combinations. An entry is an evidence record, not firmware compatibility or
permission to flash. No unsupported board is expected to use the first board's
images as an experiment.

## What is a combination?

Track more than the SoC: printed PCB/PCA revision, boot firmware/security state,
storage type and geometry, stock kernel/OS, panel/interface, Wi-Fi/Bluetooth,
audio codec/amplifier/microphones and camera sensor/ISP. Some are unknown at
intake. Different firmware or peripherals on the same labeled PCB may need a
separate variant; matching SoC does not merge records automatically.

Use one stable board ID and document observed variants under it until evidence
justifies a split. Record **observed**, **owner-reported**, **inferred** and
**unknown** separately. IDs do not encode unverified chipset guesses. Research
records live here; executable write permissions live separately in `profiles/`.

## Current records

| Record | Evidence level | Recovery profile | Important boundary |
| --- | --- | --- | --- |
| [MIR63A0-00-P1 / PCA#500240 RevP21](boards/mir63a0-revp21.md) | Research-unit recovered | `mir63a0-revp21` | One original research unit; extracted image not hardware-accepted; not a turnkey release |
| Other or unidentified combinations | Awaiting owner evidence | None | Submit a board report; no verified population/count is implied |

[`registry.json`](registry.json) is the machine-readable index. It deliberately
contains only evidenced board records; an unknown row above is an invitation,
not an invented board. Each record links its investigations, evidence and known
gaps. A board can advance in one subsystem and remain blocked in another.

## Evidence levels

1. **Reported:** an actual owner reports labels/state; identification incomplete.
2. **Identified:** board/combination evidence reviewed, important unknowns listed.
3. **Investigating:** active access/build work with reproducible attempt logs.
4. **Research-unit recovered:** a documented software-only route ran useful
   Android on at least one exact combination; regressions and provenance gaps
   remain visible. This is our current first-board level.
5. **Repeatable recovery:** a second independent owner completed the published
   process using attributable inputs and an exact identified artifact, including
   [physical acceptance](../docs/ACCEPTANCE.md) and disclosed limitations.

These are evidence descriptions, not elapsed-time milestones. A regression can
lower a level. Public artifact release is a separate provenance/licensing and
owner-key gate, not an automatic consequence of the fifth level. For each
subsystem also record pass/fail/partial/not-tested and which artifact was tested;
do not flatten a camera failure into an overall green badge.

## Join or start work

[Contribute a report](../CONTRIBUTING.md) → locate or create an investigation issue
→ add a [board record](TEMPLATE.md) → test a scoped hypothesis → contribute a
shared finding with applicability conditions → seek reviewed profile support.
No coding or destructive test is required to join. See
[how the first board's lessons transfer](../docs/PORTING.md).
