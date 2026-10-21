# Researched specifications versus verified implementations

## Keep two axes

**Specification confidence** answers "what supports this particular claim?"
**Recovery progress** answers "what has been made to work on which unit and
artifact?" They are not one ladder. Keep the existing board recovery levels in
[the registry](../README.md); attach the following state to individual research
claims instead of promoting whole families at once.

| Claim state | Meaning | Not implied |
| --- | --- | --- |
| `researched` | A reviewed source or explicit inference supports the scoped claim | Local physical confirmation, exact board pairing or recovery support |
| `verified-here` | A documented project observation validates that specific claim on a named combination | Every peripheral works, another board matches, or firmware may be redistributed |
| `disputed` | Relevant evidence conflicts; retain both sources and explain scope | That either source is fraudulent, or every variant is contradicted |

Unknown facts stay explicitly unknown in the research notes; do not manufacture
a claim with a guessed number. A "manufacturer-document" basis confirms what a
component vendor specifies, not that the component is fitted or configured on a
MIRROR. An "external-primary-report" is first-person evidence from elsewhere,
even if its author says verified. An "inference" must say why it follows and what
could disprove it. Regulatory index metadata is not the unread exhibit itself.

## Claim contract

Each `catalog.json` claim has a stable ID, subject/entity, attribute, concise
value, basis, validation state, source IDs, precise locator, limitations and next
validation needed. Inferences additionally need `reasoning`; disputed claims
need `conflict` explaining the competing evidence. Optional `related_entities` link only source-supported
relationships; adjacency does not grant compatibility. Entity kinds distinguish
boards/leads, firmware, panels, reference platforms and excluded lookalikes.

Sources retain URLs, reviewed access extent, type and an `origin_group` to expose
likely dependence. A README copying an issue, a blog rephrasing a teardown and a
forum linking its author's writeup are not three independent implementations.
GitHub documents are pinned to the revision read. Dynamic issue/thread pages
have review dates and locators, not an implied immutable snapshot. No personal
dumps or source media are mirrored in the repo.

## Promotion is a scoped review, not an automated inference

To promote a claim to `verified-here`, add a `verification` object with:

- `record`: a public, redacted repository evidence path;
- `observed_on`: the observation date;
- `scope`: the exact unit/combination, method, artifact if relevant, outcome and
  limitations explained by that record. Use anonymous unit tags, not serials.

Use basis `project-observation`; retain the prior source history. The validator
requires those fields and an existing record, but a maintainer must still review
whether the record actually supports the claim. A test fixture or existing file
is not physical evidence. If the observation establishes only the chip label,
promote only that claim—not signed-boot bypass, camera, root or repeatability.

To move an entity into `hardware/boards/`, provide reviewed same-unit identity
evidence and link the research claims it resolves. This may start at `reported`
or `identified`, with `recovery_profile: null`. An executable profile still
requires separate implementation and safety review. Independent reproduction
and public release have the [existing additional gates](../../docs/PORTING.md).

## Conflicts, missing data and invalid extrapolations

- Different capacities or panels may indicate variants rather than an error.
  Keep observations attached to their units before merging or splitting IDs.
- A transcript/configuration naming an SoC is weaker than a legible chip marking
  plus runtime identity. Debugger target names can be chosen by a user.
- An ATF/BSP version string is not the installed Android API level. A component's
  maximum clock, output wattage or interface capability is not measured device
  configuration.
- No search result is proof of absence. "Not found in this pass" is not "doesn't
  exist." Repeated anecdotes and marketing model names are not a hardware census.
- Reports involving soldering/JTAG or replacement electronics must retain that
  classification even if later steps run software. Do not advertise an unproven
  software-only initial-access path from those reports.
- Do not run referenced commands, exploits, pin experiments or firmware downloads
  as a consequence of cataloging them. This is documentation, not approval.
