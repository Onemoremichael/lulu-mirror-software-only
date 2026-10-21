# Board record: <printed label, revision; unknown is allowed>

Copy into `hardware/boards/<reviewed-stable-id>.md`. Remove prompts, keep unknowns
explicit and add the index entry in `hardware/registry.json`. This is a research
record, not an executable profile. Do not include owner keys, serials, network
identifiers, unredacted personal data or private dump links.

## Identity and evidence

- Stable ID / evidence level:
- Intake and investigation issues (public, redacted):
- Printed PCB/PCA label and revision; source and observation date:
- SoC markings/platform; observed vs reported vs inferred:
- Firmware/kernel/security state; unknown if inaccessible:
- Storage/partition geometry source (not values borrowed from another board):
- Known variants / differences / open identity questions:
- Method constraints: internal USB/buttons needed? Hardware modifications used?
- Executable recovery profile: none unless separately reviewed and implemented.

## Component map

| Subsystem | Identity and evidence source | Candidate shared finding | Result on this combination/artifact |
| --- | --- | --- | --- |
| Boot/security/transport | Unknown | None yet | Not tested |
| Storage/userdata | Unknown | None yet | Not tested |
| Display | Unknown | None yet | Not tested |
| Wi-Fi/Bluetooth | Unknown | None yet | Not tested |
| Speakers/amplifier/microphone | Unknown | None yet | Not tested |
| Camera/sensor/ISP | Unknown | None yet | Not tested |

## Attempt history

For each attempt: date, issue/comment, starting state, source revision/artifact
hash, method (read-only/host build/device write/physical test), expected/actual
result, resulting state, failures and next falsifiable hypothesis. A successful
build or ADB enumeration is not a recovered system. Keep negative evidence.

## Recovery and reuse boundaries

What has actually worked? What is preserved? What may be written and why? Are
backups complete or partial? What still depends on stock signed components?
Which shared findings were revalidated here, and which remain hypotheses?
State provenance/redistribution gaps and link acceptance results per artifact.

## Next work and independent replication

List concrete open questions, needed expertise/inputs and safe next observations.
Link independent-owner reports without owner identifiers. Do not promote to
repeatable recovery without a second owner's published-process acceptance.
