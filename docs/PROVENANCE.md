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

Android framework and platform source retain their upstream licenses. Qualcomm
vendor components have separate terms. Kernel/module source has its upstream
license requirements. This repository does not apply a blanket license to vendor
binaries or publish an owner's firmware dump. Review upstream terms when building
or distributing derived artifacts. Tools and patches retain their source history
and attribution through this table and the originating repository.

The Docker build environment originally used was
`alleen/apq8016_bm@sha256:b1d5749735cd5e8c3a8915cbc2d06f4d74da62be1082534528da1e6b127fac6c`.
An immutable digest establishes which image was used, not its trustworthiness or
license. Any replacement environment must be validated against the source build.
