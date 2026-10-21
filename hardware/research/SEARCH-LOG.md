# Research coverage and reproducibility

Initial pass: October 20, 2026. No claim of an exhaustive internet search or
complete hardware population. No messages were sent to outside researchers, no
firmware/APKs were downloaded, and no device or Docker build was used.

## Discovery and primary-source follow-up

- General search: MIRROR/lululemon teardown, chipset, motherboard, APQ8016,
  MSM8916, i.MX8/i.MX8MM, Inforce/IFC6309 and PCB designations. Followed primary
  teardown and maintainer links rather than treating news summaries as hardware
  proof. Many exact-label searches returned unrelated results, not a contradiction.
- GitHub: repository search for `lululemon mirror`, `lululemon`, `mirror imx8`;
  reviewed olm3ca's root hardware documentation, issue titles through 37 and
  relevant issue bodies/comments (not every discussion exhaustively). Reviewed
  TimStewartJ's exact device profile, supported-devices and OS investigation.
  GitHub documents in the catalog are pinned to retrieved HEAD revisions.
- Owner discussions: followed technical comments in hardwarehacking's 17ii9bn
  thread to the author's Neocities site. Live Reddit rendering omitted some
  replies found in indexed results; those are explicitly marked lower-access
  evidence, with direct confirmation still requested. This pass is not a raw
  transcript archive or proof that every claim in that discussion is correct.
- Regulatory: searched Curiouser/FCC identifiers, reviewed the 2AOSD grantee and
  MIRROR exhibit index. Original FCC/photo PDF paths failed in the reader, and
  fcc.report returned 403. Index metadata was retained; unread photos were not
  used for chip/PCB claims. Other fitness mirrors and connected weights were
  screened out rather than counted as board revisions.
- Component/platform references: Qualcomm specification identity/revision,
  NXP i.MX8M Mini documentation, TI amplifier specifications and Inforce's own
  Nougat announcement. Their capabilities are not treated as an assembled
  MIRROR BOM, operating clock/power rating or accepted firmware upgrade.

## Other discoveries and unresolved leads

- `zarif98/lululemon-mirror-project` documents a Pi/controller conversion; useful
  display-context evidence, not another original SoC or software-only unlock.
- `liamschwie/lululemon-mirror-discovery` exposed a pairing script, no README or
  hardware specification; it was not treated as board identity evidence.
- Other search hits concerned apparel, retail RFID, unrelated brands, resale or
  secondary videos/articles. No chipset row was created from those results.
- Public panel data/vendor listings were found through community references but
  are not used here as authority for cable pinouts, timing or interchangeability.
- XDA mentions were found in owner discussion, but no directly reviewed XDA
  technical source was established. The catalog does not claim to have audited it.
- Photo albums under RevP1 and the NXP label need close label review and direct
  owner context. No image set was mirrored or promoted into verified evidence.

## Next passes

Prioritize exact source-to-unit joins, publicly readable regulatory exhibits,
direct comment permalinks and independent owner confirmation over accumulating
more repetitions of the same report. Preserve access limitations and competing
claims. Future owner tests can promote individual observations under
[EVIDENCE.md](EVIDENCE.md); they must not retroactively make all researched
specifications or recovery paths verified.
