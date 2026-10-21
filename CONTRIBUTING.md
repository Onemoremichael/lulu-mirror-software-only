# Contributing: one home for every MIRROR board

You do not need a recovered unit, firmware dump or developer background to
contribute. A clear board photo, a reproducible failure or an independently
verified success can move a hardware family forward. Our aim is software-only
reuse of every original-board combination; current support is listed in the
[hardware registry](hardware/README.md), not implied by that ambition.

No unit of your own? Contribute documentary research through
[the research catalog](hardware/research/README.md). Use its
[claim/evidence rules](hardware/research/EVIDENCE.md) and the investigation issue
form. Source-backed specifications can be recorded before implementation; they
must stay distinct from same-unit observation and hardware acceptance. Do not
invent an owner report or executable profile to add a researched lead.

## 1. Report your hardware

Search [existing issues](https://github.com/Onemoremichael/lulu-mirror-software-only/issues)
for the exact printed PCB/PCA label and revision. Use the **Board identification
and progress report** issue form for a new unit/combination. If a matching
investigation already exists, add a redacted independent-owner report there
rather than starting a competing recovery thread. Similar-looking units may
still be different combinations; say what is unknown instead of guessing.

Useful starting evidence:

- Exact printed mainboard/PCA revision; redacted front/back PCB photos if safely
  accessible. The product name on the outside alone is not enough.
- Legible SoC and storage markings if visible; report transcriptions as such.
  Do not remove shields, disconnect powered boards or probe pins just for intake.
- Current state: stock app, recovered Android, recovery, fastboot, inaccessible,
  or unknown. Describe how you observed it and whether you changed anything.
- Host OS, USB connection and tool versions; authorized/unauthorized/no ADB and
  fastboot detected/not detected. No serial number is needed in a public report.
- Public source/firmware references and their provenance, if known. A public
  download is not automatically permission to redistribute it.

`python3 mirror.py doctor` and `python3 mirror.py devices` are the no-profile
entry points. Review output before posting: device listings contain serials and
host tool paths can contain your username. Lack of ADB is useful evidence, not a
reason to flash, install a USB driver from an unknown source, or open more parts
of the hardware. Do not run the current profile's inspector on an unknown board
to make it appear supported. No automatic unknown-board collector exists yet.

## 2. Keep one evidence trail per investigation

Record attempts as dated updates in the combination's issue, linking focused
**Recovery investigation or shared finding** issues when work spans boards.
Use the [board record template](hardware/TEMPLATE.md) for a PR that adds or
updates a durable `hardware/boards/` record and `hardware/registry.json` entry.
An initial record can contain mostly `unknown`; it needs an actual owner report,
not a hypothetical chipset name. Maintainers reconcile duplicate reports and
assign a stable ID. Do not publish owner identities in the registry.

For every attempt include starting state, exact source revision and artifact
hash (if any), command with identifying data redacted, expected result, observed
result and resulting device state. Distinguish read-only observation, host build,
device write and physical test. Report failures and stop conditions too. A
failed generic programmer does not prove an entire SoC family is impossible;
a working transport does not prove arbitrary partitions can be written.

Progress belongs to the exact combination and artifact tested. Independent
owners should identify their reports as independent, without publishing serials.
Do not replace failure history with a final success summary; link both.

## 3. Promote shared learning, not assumed compatibility

Use the [porting strategy](docs/PORTING.md) to classify a finding as common host
tooling, SoC-family behavior, board-specific integration or firmware/peripheral
behavior. State the reuse hypothesis, its prerequisites, evidence and a test that
could disprove it. Link the original observation from each receiving board record.
Re-test rather than copying another board's image, partition sizes or key.

Adding a research record does **not** enable recovery commands. New executable
profiles require explicit maintainer review of identification, image provenance,
partition/write boundaries, owner authorization, build/rollback limitations and
the hardware acceptance plan. The current CLI intentionally accepts only its
existing profile. Editing JSON or adding a registry entry is not onboarding a
new chipset into the flashing implementation.

## 4. Send focused PRs

Include the issue, exact combinations affected, evidence level before/after,
tests performed and tests not performed. Separate documentation/intake from
hardware-write behavior. A generalization must retain existing profile gates
and explain why it will not broaden writes on unrelated devices.

Local checks (no mirror or paid service needed):

```sh
python3 -m unittest discover -s tests -v
python3 tools/check-manifest.py
python3 tools/check-camera.py
git diff --check
```

The camera checks need a host C/C++ compiler with sanitizer support. Full Android
builds have separate [resource and vendor-input requirements](docs/BUILD.md);
never run concurrent heavyweight Docker builders. CI availability is recorded
separately from local test results.

## Privacy, rights and testing consent

Issues and pull requests are public. Do not upload private/public owner ADB keys,
serial/MAC addresses, Wi-Fi credentials, home IP addresses, complete `getprop`
or `getvar all` dumps, raw firmware/userdata, account tokens, room photos/audio,
or camera recordings. Crop/redact stickers and reflections before uploading.
Use small allowlisted excerpts and hashes, not links to unreviewed personal dumps.
There is no promise of private evidence storage; redact locally first.

Work on hardware you own or have permission to test. No issue or maintainer
request is authorization to erase another owner's mirror. Keep existing working
installations unchanged unless that owner explicitly approves a reviewed test.
Document backup gaps honestly; system-only writes are not risk-free. Do not
disable signing/authentication globally to make a support claim look broader.
