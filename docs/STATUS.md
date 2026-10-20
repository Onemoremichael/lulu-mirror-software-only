# Verification status

As of October 20, 2026, this repository is being extracted into a focused recovery
project. Original hardware evidence is in
[mirror-mirror's checkpoint](https://github.com/Onemoremichael/mirror-mirror/blob/main/RECOVERY-STATUS.md).

| Requirement | Evidence / remaining work |
| --- | --- |
| Usable Android 6.0.1 on original board | Verified on one RevP21 unit in September 2026 |
| Preserved boot chain and stock kernel | Original recovery checkpoint and build recipes |
| Wi-Fi, speaker, microphone, ADB | Verified on original unit; second-owner validation needed |
| Camera | Research image usable with dark/noisy image and intermittent startup limitations |
| Clean-checkout recovery tools | Inspection, bundle verification, plan, explicit flash and Android verification implemented; host regression tests cover write boundaries |
| Reproducible Android build | Pinned build inputs and owner-specific recipes extracted; complete image build and fresh-source reproduction still pending |
| Public firmware release | Not published; redistribution and owner authorization need review |
| Second owner installation | Not yet verified |

No Mirror is connected to the development Mac at the start of this migration.
Host-side checks cannot replace device boot, cold restart, network, speaker or
microphone acceptance. Record those results with dates and image hashes.

October 20 host acceptance: a disposable ADB key was used to build a 128 MiB
Android-compatible userdata filesystem. Key readback, UID/GID, modes, SELinux
labels, supported ext4 features and e2fsck passed. RAW/DONT_CARE conversion
produced 25,215,040 bytes and independently matched the raw expanded SHA-256.
This was a temporary host image, not a flash or a full-size hardware test.

GitHub Actions could not start the foundation checks because GitHub reported an
account billing lock. Local test results are recorded separately; a skipped
runner is not a successful CI check.

Camera migration: minimal sensor/ISP compatibility, checked vendor binary
corrections, HAL metadata, portrait preview/photo/video and padded-video packing
sources have been extracted. Native ARM ABI compilation, clean-source patch
application/idempotence and host sanitizer tests passed. Camera artifact reports
are hash-checked before consumption. Full firmware integration and hardware
acceptance remain pending; see [camera compatibility](../camera/README.md).

Docker crashed during two concurrent emulated builds. After user approval, only
the disposable Android working copy was resumed, capped at two CPU cores and
4 GiB memory with no extra swap or automatic restart. Both build entry points
now share an exclusive container name. The earlier logs and original source
image were preserved. The crash cause has not been established; resource limits
reduce pressure but are not proof of a Docker stability fix.
