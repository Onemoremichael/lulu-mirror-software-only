# Migration completion ledger

Objective: make original-board Android recovery a focused, repeatable community
project, separate from optional assistant/dashboard/clock applications and lab
experiments. Work is committed, pushed and merged in reviewable passes.

| Deliverable | Proof required | Current state |
| --- | --- | --- |
| Dedicated public repo and local checkout | GitHub main and clean local checkout | Created at the requested name/path |
| Model-specific identification | Board profile plus explicit serial inspection | Implemented; one verified RevP21 model |
| Owner-specific authorization | No embedded owner key; public-key generation/readback checks | Implemented and tested on temporary filesystem |
| Android-compatible userdata | Filesystem/labels/features/e2fsck and sparse expansion proof | Real 128 MiB host test passed |
| Guided recovery | Validated artifacts, geometry checks, explicit write plan, failure handling | Implemented; mocked write-boundary tests passed |
| Non-touch Android setup and control | Configure command and working remote controls | Implemented; HTTP tests passed; hardware acceptance pending |
| Reproducible Android build | Pinned inputs, successful build and clean-checkout validation | Pinned sources/recipes extracted; legacy-workspace build under test |
| Wi-Fi/audio/camera parity | Physical acceptance with resulting image | Original research evidence exists; new baseline not yet accepted |
| Camera compatibility extraction | Minimal native code, source patches, ABI and buffer-safety checks | Extracted and host/native-tested; integrated image build under test |
| Upstream repo pivot | Main README and ownership links point to new recovery repo | mirror-mirror PR #10 merged |
| Assistant/platform boundary | Looking Glass points recovery to the dedicated repo, without moving its optional wrapper | Looking Glass PR #25 merged; unrelated local app changes preserved |
| Public firmware distribution | Provenance/license review and verified release artifacts | Pending; no release published |
| Second-owner onboarding | Matching board recovers from published instructions | Pending |
| Each pass pushed and merged | PR merge state plus detailed validation | New repo PRs #1–3 and mirror-mirror PR #10 merged; build pass in progress |

Hardware is currently disconnected. GitHub Actions cannot start because the
account is billing-locked. These are distinct from build/test failures, and
neither supports a claim of complete device acceptance.
