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
| Reproducible Android build | Pinned recipes completed a legacy-workspace image build and filesystem inspection; fresh-source reproduction remains unverified |
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
are hash-checked before consumption. Integrated firmware passed the host checks
recorded below; hardware acceptance remains pending. See [camera compatibility](../camera/README.md).

Docker crashed during two concurrent emulated builds. After user approval, only
the disposable Android working copy was resumed, capped at two CPU cores and
4 GiB memory with no extra swap or automatic restart. Both build entry points
now share an exclusive container name. The earlier logs and original source
image were preserved. The crash cause has not been established; resource limits
reduce pressure but are not proof of a Docker stability fix.

The first capped attempt stopped with truncated/zero-length objects in Android's
secondary generic kernel output, not another Docker crash. The stock-compatible
kernel and Wi-Fi build succeeded. The recipe now explicitly exports headers and
reuses that completed kernel for Android's internal dependency, rather than
building a second unused generic kernel. The integrated camera image is being
built from the disposable working copy with the same limits and frozen inputs.

That integrated attempt then reached a malformed cached `libMcClient.so`: its
section-header table extended beyond the packed file. A fresh relocation-packer
run on its linked input completed without the earlier readelf error. Independent
Python bounds checks confirmed the two malformed cached copies (PACKED and
symbols); only those two files were moved into the working image's
`.recovery-quarantine-20261020/` for recoverability. No source or vendor input
was removed. Kernel `.o` audit results were not blindly cleaned: Kbuild also
legitimately produces archive-format `built-in.o` files. The new final image
gate checks ELF header tables, file-backed sections and segments and records
`elf-audit.json`. This checks truncation, not full link/runtime correctness.

The repaired attempt regenerated the packed library, then exposed an integration
gap: vendor DLKM rules expected `KERNEL_OUT`, which the prebuilt-kernel shortcut
had not supplied. The make wrapper now supplies the relative prepared-kernel
path/config, with a shell argument regression test. A targeted test reached the
vendor bus-timeout fault-injection module but hit its own forbidden compiler
warning. These generic kernel test modules are outside normal recovery operation;
the vendor's `TARGET_KERNEL_DLKM_DISABLE` hook now disables them. The required
stock-compatible Wi-Fi module remains an explicit, verified build/install step.

With that hook disabled, actual Android compilation and image packing completed.
Read-only inspection independently passed the camera binary comparisons,
front/mount-0 metadata, 32/64-bit recording guards, Wi-Fi module, speaker route,
vold marker and ELF audit. The candidate was nevertheless rejected: Launcher3
was absent from Qualcomm's default product selection, and the generated
`install-recovery.sh`/recovery patch violated the preserved-recovery boundary.
The recipe now explicitly builds Launcher3, removes generated automatic
recovery installers/payload before the final pack, and checks their absence
inside the finished image. An ERR trap identifies any future failed shell gate.
No candidate was flashed and no automatic updater was executed.

## Successful host build — October 20, 2026

The revised integrated build exited successfully. The sparse system image is
855,546,960 bytes, expanding to 1,288,413,184 bytes, with SHA-256:

```text
6ea30e58069cdc9dde064198a66606abe19f39606f663f433c878fd2d9b5f2e9
```

Read-only filesystem checks passed: privileged Launcher3/Settings, vold handoff
marker, Wi-Fi framework/module, speaker routing, camera artifact
comparisons and front/mount-0 metadata, both software-recording libraries,
Snapcam APK, absence of lab modules and automatic recovery updaters, and an empty
ELF truncation audit. All 39 frozen input hashes and the exported sparse stream
and hash were independently rechecked on the host.
An independent inspection of that exported image also verified the intended
owner fingerprint and authorization-branch marker in compiled `services.jar`.
Future builds record this check in `owner-check.json`; it is not a live ADB
authorization test.

This was a resumed disposable **legacy workspace**, not a clean-source
reproduction. It used a disposable test public key, not a community/default
owner key. `hardware_verified` remains false. The image is an ignored local
test artifact, not a public release or an instruction to flash an existing
installation. Boot, camera quality and physical audio acceptance on this newly
built image remain untested.

The separate `--fresh-headers` native camera test also completed under the
two-core/4 GiB limit. It exported kernel userspace headers into an empty temporary
output directory rather than using the legacy workspace's generated headers.
All four output hashes matched the camera artifacts in the successful system
image. This validates that header-export path, not an entire clean Android build.

Source-provenance inspection found no Git checkout metadata in the legacy
`vendor/qcom/proprietary` or `prebuilt_HY22` directories. No vendor repository
origin or revision is inferred from that directory name. The full clean-source
build and attributable matching vendor inputs therefore remain separate work.

Build diagnostics now suppress the handled `tput colors` subshell probe that
looked like a build failure in the successful log. Regression tests still
require nonzero status and diagnostics for real failures and failing command
substitutions. This changes reporting, not the inspected firmware payload.

Later on October 20, the migrated `inspect` and `verify` commands ran over USB
against the existing installation. All eight automated checks passed: matching
platform/kernel, Android 6.0.1, boot completion, Launcher3, RSA authorization,
1080p display, mounted userdata and loaded Wi-Fi driver. The local report stays
in ignored `reports/` because it contains device identity. No setup command,
power change, audio/camera capture or flash was performed. This is evidence for
the migrated read-only tooling, not acceptance of the newly built image.
