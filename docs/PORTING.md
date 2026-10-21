# Software-only recovery across hardware combinations

## Outcome and limits

The project's destination is a useful original-board computer for every
lululemon MIRROR owner, with documented software-only paths across chipset,
board, firmware and peripheral combinations. Today's RevP21 recovery is the
first evidence base, not a universal image or a scope boundary.

"Unlock" means escaping the discontinued application's limits to run useful
owner-controlled software. Bootloader unlock, root, a newer Android version and
a replacement OS are separate capabilities, each requiring its own evidence.
The first path keeps signed stock boot components. Another family may need a
different path; cryptographic or missing-source barriers may prevent a path with
the inputs available today. Report such blockers rather than promising a bypass.
Do not turn hardware modification into an undocumented software-only prerequisite.

## Organize work around combinations and shared findings

Use three linked units of work:

1. **Owner report:** observations from a real unit, with privacy-safe evidence.
   Multiple reports reveal variants and independently reproduce results.
2. **Combination record:** stable board identity plus observed firmware/storage/
   peripheral variants, current evidence level and subsystem acceptance. Unknown
   fields stay unknown. The [registry](../hardware/README.md) indexes these.
3. **Shared finding:** a mechanism, tool, patch or failure mode with stated
   prerequisites and a reproducible test. Link it from each relevant record;
   distinguish an applicability hypothesis from a result actually tested there.

Keep a canonical investigation issue per combination and focused issues for
cross-cutting findings. Add attempts as linked updates. Avoid parallel folklore
threads with no source revision or outcome. Contributors do not need to wait
for a universal framework before reporting an inaccessible unit.

### Example transfer reasoning—not additional compatibility claims

| Observation or shared part | What can transfer | What must be established on the receiving combination |
| --- | --- | --- |
| Same SoC family | Leads for source archives, ABI/tools and boot documentation | OEM signing policy, bootloader behavior, board/device-tree integration, exact build inputs |
| Same printed PCB revision | Stronger identity hypothesis and candidate peripheral map | Firmware variants, component substitutions, storage geometry and artifact acceptance |
| Same kernel release string | Candidate module/toolchain investigation | Config/exported ABI, actual module and firmware compatibility; a release string alone is weak evidence |
| Same camera sensor | Sensor mode/timing and fixed-focus findings | Sensor wiring, ISP/vendor ABI, library hashes, mount orientation, preview/photo/video correctness |
| Same panel or audio component | Candidate display timing or route knowledge | Interface, device-tree bindings, GPIO/amp wiring and real display/audio tests |
| Same fastboot transport | Host transport/parser/test infrastructure | Supported commands, write permissions, download limits and partition map; no trial writes to find out |
| Same userdata filesystem problem | Ext4 validation and sparse-stream tooling | Kernel feature support, encryption policy, size, SELinux/ownership and owner's key |
| Different chipset entirely | Privacy-safe intake, artifact hashes, evidence levels, write-plan discipline, non-touch UX principles | A new access/build/driver path; Qualcomm camera or boot recipes are not presumed portable |

An example shared finding could say: "The observed bootloader rejects later
split sparse downloads; send the validated whole image only when it fits the
measured limit." Its reusable part is the checked transport rule, not the first
unit's numeric limit. Likewise our bounded NV12 packing tests can teach a camera
port, but applying the patch still requires matching layout and codec evidence.

## Investigation stages

### A. Identify without changing the device

Use the [intake form](../CONTRIBUTING.md#1-report-your-hardware). Start from labels,
existing USB enumeration and owner-observed state. Do not force a profile match
or guess a partition from chipset similarity. Physical access must be voluntary
and safe; a closed-back owner report is still useful.

Result: reviewed identity, unknowns, available transports and an investigation
issue. No enabled writes. If ADB is unauthorized or unavailable, record that;
do not instruct an owner to bypass authorization merely to complete a form.

### B. Establish the access and preservation boundary

Determine what existing signed software/boot components allow, what can be read
lawfully, whether required inputs are obtainable, and what is essential to the
panel/peripherals. Prefer documented transports and retaining functional stock
components. Record negative evidence and its scope. Never claim a full backup
from empty/partial dumps. Do not use OEM unlock, generic programmers, recovery
updates or random images as generic troubleshooting steps.

Result: a scoped hypothesis, explicit preservation list, evidence gaps and a
reviewed test proposal. Some combinations may remain blocked here; they still
belong in the registry with honest next questions.

### C. Build an owner-specific candidate on the host

Establish attributable sources/vendor inputs, toolchain/ABI, image formats,
storage constraints and owner authorization. Adapt common tools only behind
explicit capabilities; keep family-specific implementation separate. Freeze
inputs and hashes, validate filesystems/native binaries, and test rejected cases.
No build success is a flash approval. Do not redistribute artifacts until rights
and embedded data have been reviewed.

Result: exact candidate and report, checked failure behavior and an acceptance
plan. Host-only evidence remains host-only, including tests that mock Docker or
device writes.

### D. Review and enable a combination-specific recovery path

New `profiles/` entries and CLI support need code review together. The existing
implementation is deliberately single-profile, not a generic flashing engine.
Do not remove that guard to make intake easier. Before enabling another path:

- Verify identity predicates and physical owner attestation; reject ambiguity.
- Document image origin, ABI/driver prerequisites and supported starting states.
- Define exact permitted/preserved partitions, required geometry, image/download
  constraints and the authorization model. Unsupported transports/actions fail
  closed, without speculative retries, automatic erase or automatic reboot.
- Provide a serial-specific reviewed write plan with explicit consent and a
  truthful rollback/recovery boundary. Preservation is preferable to trying to
  reconstruct signed boot components. No guarantee of recovery without evidence.
- Add fixture tests for wrong boards, changed artifacts, unknown geometry,
  unsupported operations and interrupted writes. Existing-board tests must pass.
- Perform the [physical acceptance checks](ACCEPTANCE.md) on the exact artifact
  with the owner's approval, reporting partial/failing peripherals individually.

Future architecture should reuse transport and artifact validators where their
contracts genuinely match, with explicit per-family adapters for divergent
boot/build behavior. A profile is not sufficient to port a different chipset.
Implement that abstraction when a second evidenced path needs it, not by
inventing untested generic flashing behavior now.

### E. Reproduce and maintain

A second independent owner follows published instructions and records exact
artifacts plus acceptance results before the combination becomes **repeatable
recovery**. Support is specific to the documented combinations and starting
states. Release provenance/license review remains a separate gate. Track
regressions against artifacts, retain failed observations, and adjust evidence
levels when later results contradict earlier ones.

## Near-term community work

- Collect real board/firmware/peripheral reports, including inaccessible units.
- Map variation among RevP21 units and gather independent read-only observations.
- Investigate other reported families without reusing the RevP21 write profile.
- Resolve the first path's clean-source/vendor and exact-image acceptance gaps.
- Extract a common implementation only when evidence shows a second path shares
  the same contract; contribute shared tests and applicability notes alongside it.

No estimated unlock date or guaranteed outcome is implied for an unknown board.
The useful promise is a central evidence trail, welcoming contribution path and
honest, increasingly repeatable recovery work—not a universal unlock button today.
