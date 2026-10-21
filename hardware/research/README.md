# MIRROR hardware research catalog

Reviewed October 20, 2026. This is a first source-backed landscape, **not an
exhaustive bill of materials, generation census or compatibility list**. It is
deliberately separate from owner-validated [board records](../README.md) and
executable recovery profiles. No device was queried or changed for this pass.

[`catalog.json`](catalog.json) records 24 individual claims, 12 entities and 19
source references. Read the [evidence rules](EVIDENCE.md) before treating a value
as verified. All external claims in this first catalog are **researched**, not
validated on this project's hardware. Source authors may have tested their own
units; that is attributed external evidence, not our independent replication.

## Landscape: facts do not imply a complete combination

| Research cluster | Current documentary evidence | What is still missing |
| --- | --- | --- |
| [Qualcomm](qualcomm.md) | Exact stock firmware profile; component-level teardown; signed boot observations | Same-unit joins among PCB revision, firmware, storage and panel |
| [NXP i.MX8M Mini](nxp.md) | Owner board-label/runtime reports and hardware-assisted access writeup | Independent board identification, stock fingerprint and software-only initial access |
| [Display variants and revision names](panels.md) | Three named panel models, Rev08/RevP1 leads and a regulatory anchor | Trustworthy mapping between those labels and each compute/firmware variant |

Do not create a six-model matrix by multiplying two SoCs by three panels. A
connection only exists when a source ties both observations to the **same unit**.
Likewise, `Rev08`, `RevP1`, `RevP21`, an external product model, a SoC reference
platform and a firmware build are different identifier namespaces. A source's
"newer model" description is not a dependable chronology or identity gate.

## Most useful implications

1. **Several recovery approaches belong in the map.** An app-level path over
   already-authorized stock Android, our reconstructed system route, and an
   external JTAG-assisted investigation have different prerequisites. None is a
   universal bootstrap for an untouched device. Hardware-swap conversions are
   useful panel evidence but do not count as software-only recovery.
2. **Common components are porting leads, not authorization.** Sensor findings
   may be useful across units if sensor/ISP ABI and wiring match. A shared panel
   may inform timing research while saying nothing about OEM signing. Boot-chain
   findings need exact firmware/security context. See [reuse strategy](../../docs/PORTING.md).
3. **Research can progress before another unit is available.** Contributors can
   source specifications, resolve identifiers, find lawful BSPs and correlate
   publicly documented components. Hardware owners later validate those claims
   through scoped observations and separately approved tests.

## Highest-value next validation

- Confirm the reported NXP PCB label against a legible redacted photo and obtain
  an allowlisted stock release/SDK/fingerprint report. Do not infer Android API
  from a boot-firmware branch name.
- Get a same-unit PCB/SoC/panel/firmware report for a Rev08-designated unit, and
  resolve what the RevP1 designation actually labels. Do not merge either with
  RevP21 based on a shortened string or chronology.
- Confirm peripheral/storage variation among actual RevP21 units; the research
  teardown's complete component list must not be silently assigned to ours.
- Establish whether a documented authorized-ADB app route fits a collaborator's
  exact starting firmware before considering system replacement. External
  support does not automatically extend our CLI profile.
- Retrieve the original regulatory exhibits and inspect labels; inaccessible
  photo PDFs remain discovery leads rather than hidden proof of a BOM.

## Contribute research or validation

Use **Recovery investigation or shared finding** for desk research, and **Board
identification and progress report** for observations from a real unit. Cite a
primary source, precise section/comment, access date and scope; distinguish
source assertions from your inference. Follow [EVIDENCE.md](EVIDENCE.md) and
[CONTRIBUTING.md](../../CONTRIBUTING.md). Update the claim rather than copying its
value into a support badge. Check catalog integrity with:

```sh
python3 tools/check-hardware-research.py
```

That check validates structure, links and evidence fields, not truth. Neither
new research nor a passing validator enables a flash profile.
