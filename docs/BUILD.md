# Build inputs and redistribution

The implementation comes from mirror-mirror commit history, including its Android
revival patch, manifest rewrite, filesystem tools and kernel/Wi-Fi compatibility
work. Exact source provenance is in [PROVENANCE.md](PROVENANCE.md).

Android and Qualcomm source trees, licensed vendor components and kernel inputs
are needed to build system. The original workstation's `.work` directory is not
a distributable SDK. Build inputs must be pinned, hash-checked and attributable;
public availability alone is not a license to redistribute vendor binaries.

Never publish owner ADB keys, private keys, Wi-Fi configuration, room recordings,
camera captures or an image containing a previous owner's authorization. Build
authorization for the receiving owner's public key. RSA authentication remains
enabled; generic auto-authorization and unrestricted LAN ADB are not defaults.

## Source checkout

`build/manifest.xml` pins 447 Android/Qualcomm projects to commit IDs and replaces
retired CodeAurora endpoints with archival HTTPS mirrors. Check it with:

```sh
python3 tools/check-manifest.py
```

On a Linux case-sensitive filesystem, Google's `repo` tool can consume this repo
as its manifest repository:

```sh
mkdir android-m && cd android-m
repo init -u https://github.com/Onemoremichael/lulu-mirror-software-only.git \
  -b main -m build/manifest.xml
repo sync -c -j4
```

Expect a large download and a build workspace of at least 100 GiB; provision
additional space for compiler output and caches. `repo sync` must complete with
the exact revisions. An unavailable archived commit is a real dependency gap;
do not silently substitute the tip of a repository.

The manifest does **not** supply the proprietary Qualcomm HY22 vendor tree.
Provide that from your lawfully obtained matching SDK/build inputs at
`vendor/qcom/proprietary`, including `prebuilt_HY22` and the common vendor build
files. Their source and redistribution rights must be established before a
community firmware release. The pinned build container supplies the old host
toolchain environment; it is not a substitute for these vendor inputs.

## Build system and the matching Wi-Fi module

The host needs Python 3.10+ and Docker. The container uses its existing Python 2.7
for legacy Android preparation; `build/prepare.py` supports both interpreters.
The build container is capped at two CPU cores, 4 GiB RAM, no additional swap,
and 1,024 processes. Compilation defaults to two jobs. Its fixed container name
prevents two copies of this builder from running together; do not run the
separate camera builder concurrently. These limits reduce host pressure, but
cannot guarantee Docker stability. An out-of-memory failure stops the build;
there is no automatic restart or retry.
Build against a disposable source checkout:

```sh
python3 tools/build-system.py --tree /absolute/path/to/android-m \
  --public-key "$HOME/.android/adbkey.pub" --output-dir artifacts/my-system \
  --camera-artifacts artifacts/my-camera
```

The source tree must be on a Linux-compatible, case-sensitive filesystem. A Linux
Docker volume or ext4 working image avoids macOS filesystem incompatibilities.
The build modifies that workspace and compiler output; use a disposable copy.
Prepare `artifacts/my-camera` first using the
[camera build instructions](../camera/README.md). The native camera build and
system build run sequentially under the same exclusive Docker name. Omit
`--camera-artifacts` only for a diagnostic generic-camera build; that output is
not the complete camera recovery baseline.

For the existing ext4 legacy workspace, the tool makes a filesystem clone first:

```sh
python3 tools/build-system.py --legacy-image /absolute/path/to/old-build.ext4.img \
  --work-image /absolute/path/to/new-working-build.img \
  --public-key "$HOME/.android/adbkey.pub" --output-dir artifacts/my-system \
  --camera-artifacts artifacts/my-camera
```

APFS cloning on macOS or reflink support on Linux is required for this path. The
tool refuses an existing working-image path and does not silently allocate a
full physical copy. Docker needs privileged loop mounts for an ext4 image.
`build.log` records compilation progress; `build-report.json` and `SHA256SUMS`
identify successful output. `system.img` is the only firmware image exported.
Building never invokes ADB or fastboot.
Each new invocation freezes its recipes and owner public key under the ignored
output directory's `inputs/`, and writes `input-hashes.json` before starting
Docker. Editing the repository then cannot alter that invocation's recipes.
Only the public key is copied, never the owner's private ADB key. Preserve the
input hashes with the build log when investigating a failure. Builds started
before this snapshot feature still use their original live recipe mounts.

If an interrupted job left a disposable cloned working image, retain its logs
and resume that copy into a new output directory:

```sh
python3 tools/build-system.py --resume-image /absolute/path/to/new-working-build.img \
  --public-key "$HOME/.android/adbkey.pub" --output-dir artifacts/my-system-retry \
  --camera-artifacts artifacts/my-camera
```

Use `--resume-image` only for the disposable working copy. It is modified in
place. The tool checks actual live Docker mounts and refuses a workspace another
job is using. A slow observation or a stale log is not enough to declare a build
stopped; inspect its live container/process before retrying.

The kernel is compiled to obtain compatible module symbols, but the device keeps
its original kernel. The Wi-Fi module must match
`3.10.49-perf-gf46dad5260f`. The Android patch supplies owner-key authorization,
the userdata encryption-handoff fix, speaker routing and delayed WLAN loading.
USB RSA authorization stays enabled; network ADB is disabled by default.
Android's internal kernel dependency reuses that completed compatibility build;
headers are exported explicitly. No replacement boot image is exported or flashed.

The baseline does not add the camera lab's diagnostic kernel module, C2D sampler,
exposure experiments, clock, assistant or dashboard. A clean generic vendor
camera stack is **not** equivalent to the repaired research camera. Supplying
`--camera-artifacts` validates and freezes the four native camera files, applies
the HAL/Snapcam/recording source fixes, builds both recording architectures, and
checks installed files and metadata in the finished filesystem. Full integrated
image compilation and hardware acceptance are still under test; this is not yet
proof of camera parity. A legacy workspace can retain source changes from that work; its
build report must not be described as a clean-source reproduction.

Until a clean-source build, vendor provenance and device acceptance are verified,
there is no ready-to-flash public firmware release. Inspection, owner userdata
creation and remote controls work independently of that release milestone.
