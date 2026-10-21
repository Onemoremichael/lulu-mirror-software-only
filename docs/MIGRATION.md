# Migration completion ledger

Objective: make original-board Android recovery a focused, repeatable community
project, separate from optional assistant/dashboard/clock applications and lab
experiments. Work is committed, pushed and merged in reviewable passes.

| Deliverable | Proof required | Current state |
| --- | --- | --- |
| Dedicated public repo and local checkout | GitHub main and clean local checkout | Created at the requested name/path |
| Model-specific identification | Board profile plus explicit serial inspection | Implemented; one verified RevP21 model |
| Owner-specific authorization | No embedded owner key; public-key generation/readback checks | Temporary filesystem and compiled services fingerprint/branch checks passed; live new-image acceptance pending |
| Android-compatible userdata | Filesystem/labels/features/e2fsck and sparse expansion proof | Real 128 MiB host test passed |
| Guided recovery | Validated artifacts, geometry checks, explicit write plan, failure handling | Implemented; mocked write-boundary tests passed |
| Non-touch Android setup and control | Configure command and working remote controls | Implemented; HTTP tests passed; hardware acceptance pending |
| Reproducible Android build | Pinned inputs, successful build and clean-checkout validation | Integrated legacy-workspace build and image checks passed; clean-source reproduction pending |
| Wi-Fi/audio/camera parity | Physical acceptance with resulting image | Original research evidence exists; new baseline not yet accepted |
| Camera compatibility extraction | Minimal native code, source patches, ABI and buffer-safety checks | Native/host tests and integrated filesystem checks passed; physical acceptance pending |
| Camera fresh-header path | Export headers without relying on prior compiler output | Passed; all four native output hashes match the integrated image inputs |
| Upstream repo pivot | Main README and ownership links point to new recovery repo | mirror-mirror PR #10 merged |
| Assistant/platform boundary | Looking Glass points recovery to the dedicated repo, without moving its optional wrapper | Looking Glass PR #25 merged; unrelated local app changes preserved |
| Public firmware distribution | Provenance/license review and verified release artifacts | Pending; no release published |
| Second-owner onboarding | Matching board recovers from published instructions | Pending |
| Each pass pushed and merged | PR merge state plus detailed validation | New repo PRs #1–6, mirror-mirror PR #10 and Looking Glass PR #25 merged |
| Checkout provenance audit | Compare actual Git HEADs with all manifest pins | Host checkout matches 447/447; legacy Linux image lacks Git metadata; working-file/vendor contents remain unattested |

The mirror later became reachable through USB, and the migrated inspection and
verification commands passed all eight read-only checks on its **existing**
installation. The newly built image remains unflashed and physically untested.
GitHub Actions cannot start because the account is billing-locked. These are
distinct evidence boundaries, not support for a claim of new-image acceptance.
The owner prioritizes preserving the current installation; hardware writes need
separate explicit approval and are not part of the ongoing host-side audit.

## Remaining acceptance gates

The repository extraction and cross-repository ownership pivot are merged.
This is not a claim that a repeatable community firmware release is ready:

- Clean-source reproduction still requires attributable matching proprietary
  inputs and an adequately sized Linux build workspace. The audited workstation
  had about 29 GiB free, below the documented 100 GiB minimum workspace estimate;
  do not start another full build or delete unrelated files to make it fit.
- New-image boot, owner authorization, display, Wi-Fi, audio and camera behavior
  require physical acceptance of that exact image. Existing-installation checks
  and source/artifact hashes cannot substitute for this. Preserving the current
  mirror takes priority; attached USB does not authorize replacement testing.
- Public firmware distribution needs provenance/license review and release
  artifacts, followed by a second-owner onboarding test. No such release or test
  is claimed here.
- Hosted CI execution remains blocked by account billing. Local checks are
  recorded separately and do not establish a green GitHub Actions run.

The next phase needs these external inputs or separately approved hardware work,
not additional speculative flashes or a broader rewrite of the assistant app.
