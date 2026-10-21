# Android camera compatibility

These are the camera compatibility fixes extracted from mirror-mirror. They
belong to the Android hardware platform; clocks, the assistant and dashboards
remain separate applications.

The RevP21 board has one fixed-focus OV5640 front camera. Its original kernel and
replacement HY22 camera userspace disagree about sensor structure sizes, one ISP
ioctl layout, sensor mode dimensions and UYVY/YUYV format. The recovered path also
needs a narrowly checked CPP stream-on branch correction. These fixes made the
original research installation produce coherent preview and photos.

The new minimal `isp-compat.c` keeps the 88-to-104-byte ISP configuration mapping
and five missing fixed-focus hooks. It omits exposure register writes, gain
overrides, ioctl logging and diagnostic kernel interfaces. Sensor timing is the
tested default 0x18; the bring-up timing override is not included.

HAL metadata describes FRONT/0. Snapcam patches preserve preview proportions,
upright photos and upright software H.264/AAC recordings on the sensor-less
portrait display. `mirror-video-pack.h` copies only active NV12 rows from the
exact known Venus allocation and rejects unknown oversized layouts. Both 32-bit
and 64-bit recording libraries are required.

## Build native components

Requirements: Docker, git, Python 3.10+, patchelf, an existing matching Android
build filesystem or a case-sensitive Linux source checkout, and the pinned sensor source.
Use a read-only source image which is not concurrently mounted for writing.

```sh
git clone https://github.com/copslock/Quectel_sc20_linux_sdk.git .work/camera-sdk
git -C .work/camera-sdk checkout --detach ed0e50a102c7ee115c6999ba0a26ce50537c616e
python3 tools/build-camera.py --source-image /absolute/path/to/android-build.ext4.img \
  --camera-source .work/camera-sdk --output-dir artifacts/my-camera
```

The compiler verifies the 376-byte sensor structure and 96-byte mode table. The
host checks exact hashes of both vendor inputs before patching, confirms the
daemon's new dependency and records output hashes. No binary is distributed by
this repository and no command accesses the Mirror. Read upstream source/vendor
terms before redistributing derived firmware.

For a fresh Linux source checkout, substitute `--source-tree /path/to/android-m`
for `--source-image`. The tool can export kernel userspace headers into its
temporary build directory without compiling a kernel. `--fresh-headers` forces
that path for validation when a legacy workspace already has generated headers.
The forced fresh-header path was tested on October 20 and produced the same four
artifact hashes as the integrated image's camera inputs. A full fresh Android
checkout/build is still a separate, unverified step.
Run image-based build jobs sequentially; do not mount a workspace while another
job is writing to it.
Both build entry points use the same exclusive Docker container name and a
two-core/4 GiB limit, with no extra swap or automatic restart. Docker rejects a
second builder while one is running. This is a host-stability precaution, not a
guarantee that an emulated legacy toolchain cannot exhaust its own memory limit.

Then supply this output to the system builder:

```sh
python3 tools/build-system.py --tree /absolute/path/to/disposable/android-m \
  --public-key "$HOME/.android/adbkey.pub" --camera-artifacts artifacts/my-camera \
  --output-dir artifacts/my-system
```

Use the image clone/resume options in [BUILD.md](../docs/BUILD.md) instead of
`--tree` when appropriate. The builder validates the native report and copies
only its four required binaries into an immutable per-build snapshot. It applies
the HAL/Snapcam/recording source fixes, builds both recording architectures, then
checks native file hashes, front/mount-0 metadata, buffer-bound guards and the
camera APK in the final filesystem. The integrated legacy-workspace build and
these checks passed on October 20; none constitutes physical camera acceptance
or clean-source reproduction. See the exact image hash in [STATUS.md](../docs/STATUS.md).

Camera source preparation runs inside the pinned Linux environment with GNU
patch. macOS BSD patch does not handle some of the historical one-line hunks the
same way. Preparation stages the complete patch chain before updating source
files, so a failed later patch does not partly alter the workspace.

## Verification and remaining work

```sh
python3 tools/check-camera.py
```

Host address/undefined-behavior sanitizer checks cover padded NV12 packing,
invalid dimensions and buffer bounds, ISP pixel/RDI translation and ioctl
passthrough. Target ARM compilation and ABI/symbol checks also passed on October
20. The full camera source chain applied to clean upstream files and a second
idempotent run passed in the pinned Python 2.7 container.

Those results do not prove camera operation on the new firmware. The original
research camera was dark/noisy and sometimes failed to start; software recording
was roughly 23 fps rather than guaranteed 30 fps. Exposure experiments remain in
the research repo. Image quality, repeated startup, photo/video rotation and A/V
sync need physical acceptance on the new image before the camera is called ready.

Source: mirror-mirror revision `219300a99861c4744d8b7313ab05bc4ea8c50bd0`.
The original lab history is available in that repo's CAMERA-RECOVERY.md. The
compatibility shim here is a minimal extraction, not a byte-identical copy of
the experimental exposure-enabled library.
