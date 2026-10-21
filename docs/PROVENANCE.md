# Source provenance

Recovery extraction began from
`Onemoremichael/mirror-mirror` at revision
`219300a99861c4744d8b7313ab05bc4ea8c50bd0`. The original repository remains the historical source
of the September 2026 device tests.

Migrated source utilities:

| New path | Original path | Adaptation |
| --- | --- | --- |
| tools/build-userdata.py | mirror-build-adb-userdata.py | Configurable platform-tools/e2fsprogs paths |
| tools/sparse-userdata.py | mirror-sparse-userdata.py | Configurable dumpe2fs path |
| tools/rewrite-manifest.mjs | mirror-rewrite-apq8016-manifest.mjs | Original 450-to-447 pinned-project rewrite |
| build/android-revival.patch.in | patches/android-m-mirror-revival.patch | Owner fingerprint placeholder; omit LAN ADB and verbose camera properties |
| build/kernel.config | artifacts/.../running-kernel-build.config | Observed kernel configuration for compatibility build; original kernel remains on device |
| build/manifest.xml | .work/android-m/.repo/manifests/advan/LA.BR.1.2.7-01010-8x16.0-github.xml | Pinned Android/Qualcomm checkout manifest |
| camera/isp-compat.c | camera/legacy-camera-compat.c | Keep ISP ABI translation and missing fixed-focus hooks; remove exposure, diagnostics and ioctl logging |
| camera/quectel-ov5640-*.patch and camera/mirror-ov5640-stock-modes.patch | camera/ with the same filenames | Sensor ABI and default mode/timing fixes, without runtime timing sweeps |
| camera/mirror-camera-*.patch | camera/ with the same filenames | Front/mount-0 metadata and raw software video; omit startup exposure experiment |
| camera/mirror-snapcam-*.patch | camera/ with the same filenames | Portrait preview/photo/video and bounded software-video bitrate |
| camera/mirror-codec-video-pack.patch and camera/mirror-video-pack.h | camera/ with the same filenames | Bounded NV12 Venus-to-packed recording conversion |
| camera/test-video-pack.cpp | camera/test-video-pack.cpp | Host sanitizer regression for the recording buffer layout |

The sensor source comes from the owner-supplied
`copslock/Quectel_sc20_linux_sdk` checkout at
`ed0e50a102c7ee115c6999ba0a26ce50537c616e`; its redistribution terms must be
reviewed separately. `tools/build-camera.py` requires this revision and exact
hashes of the two HY22 vendor inputs before binary modification. Build reports
record output hashes; those checks identify supported inputs, not permission to
redistribute the outputs. The minimal shim has not yet been accepted on a newly
built recovery image and is not equivalent to the exposure-enabled research
checkpoint.

Android framework and platform source retain their upstream licenses. Qualcomm
vendor components have separate terms. Kernel/module source has its upstream
license requirements. This repository does not apply a blanket license to vendor
binaries or publish an owner's firmware dump. Review upstream terms when building
or distributing derived artifacts. Tools and patches retain their source history
and attribution through this table and the originating repository.

The inspected legacy HY22 vendor directories contain no Git checkout metadata.
Their directory names do not establish a repository origin, revision or
redistribution permission. The successful legacy-workspace build must not be
presented as a complete pinned-source reproduction. Supplying attributable,
matching vendor inputs remains necessary for that claim.

The Docker build environment originally used was
`alleen/apq8016_bm@sha256:b1d5749735cd5e8c3a8915cbc2d06f4d74da62be1082534528da1e6b127fac6c`.
An immutable digest establishes which image was used, not its trustworthiness or
license. Any replacement environment must be validated against the source build.
