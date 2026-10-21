# lulu-mirror-software-only

Recover a discontinued lululemon Studio MIRROR as a usable Android computer on
its original mainboard. The screen has no touch layer; setup and everyday
control happen from your computer or phone.

## Mission: every original-board MIRROR

Our goal is a documented **software-only recovery path for every lululemon
MIRROR hardware combination**, so any owner can unlock the useful potential of
the hardware they already own. This is a community research program, not a claim
that all chipsets are supported today or that every secure-boot configuration
can be bypassed. We prefer retaining a working signed boot chain when possible;
usable Android does not require an unlocked bootloader or unrestricted root.

No replacement mainboard is the baseline. Software-only can still require
physical access to internal USB or buttons; it does not mean a remote one-click
unlock. Hardware modifications are a separate experimental path, not a hidden
prerequisite for a software-only success claim.

**Have a different board, or not sure what you have? You belong here.** Start
with the [hardware registry](hardware/README.md) and
[contributor guide](CONTRIBUTING.md). Report the board even if it is still locked,
you cannot get ADB, or your only result is a failed attempt. Do not select our
existing flash profile merely because your unit has a similar chipset.

This project extracts the Android recovery work from
[mirror-mirror](https://github.com/Onemoremichael/mirror-mirror). That repository
keeps the hardware research and experimental applications. The separate
[Looking Glass](https://github.com/Onemoremichael/looking-glass) assistant can be
installed after Android works.

The verified unit runs reconstructed Android 6.0.1, Launcher3, authorized ADB,
Wi-Fi, speakers and microphone while retaining its original signed bootloader,
boot image, kernel, recovery and board firmware. Camera preview, photos and
software-encoded video work on the research image, with brightness and startup
limitations. This does not establish a bootloader unlock or unrestricted root.
The extracted pipeline has passed a local legacy-workspace build and filesystem
inspection, but has not produced a hardware-accepted replacement release. See the [camera migration](camera/README.md)
for the compatibility mechanisms and remaining acceptance checks.

## Start here

The supported hardware candidate is **MIR63A0-00-P1 / PCA#500240 RevP21**,
Qualcomm APQ8016/MSM8916. Check the printed board label. Other revisions need
their own evidence; a matching chipset alone is insufficient.
This is our first research success, not the project's scope limit. See the
[porting strategy](docs/PORTING.md) for how shared findings become separately
verified recovery paths rather than copied firmware.

Requirements: Python 3.10+ and Google's Android platform-tools (`adb`,
`fastboot`) on your PATH. No Python packages are required.

```sh
python3 mirror.py doctor
python3 mirror.py devices
# Only after confirming the matching printed board label:
python3 mirror.py inspect --serial YOUR_SERIAL --board mir63a0-revp21
```

These commands only inspect the host/device. They do not reboot, unlock, erase,
flash, record microphone audio, capture the camera or change ADB authorization.
Local reports stay in ignored `reports/`; review them before sharing.

Follow [the recovery guide](docs/RECOVERY.md),
[hardware compatibility](docs/COMPATIBILITY.md) and
[what is verified](docs/STATUS.md). Existing Android installations should start
with verification and remote control, without reflashing.
Use the [owner acceptance checklist](docs/ACCEPTANCE.md) to distinguish automated
Android checks from actual display, Wi-Fi, audio and camera tests.

### Already have working Android?

Migrating to these tools does **not** require replacing your installation. Start
with the read-only check below; it does not change orientation, power state,
settings or authorization. A pass describes the installed system, not an unflashed
image built by this project.

```sh
python3 mirror.py verify --serial YOUR_SERIAL --board mir63a0-revp21 \
  --output reports/existing-installation.json
```

Keep your current apps and settings. Skip `configure` unless you specifically
want the setup changes described in the [control guide](docs/REMOTE.md).
Starting the remote serves its control page; using its buttons can change the
device, so it is separate from read-only verification.

```sh
# Optional controls, once Android ADB is authorized:
python3 mirror.py remote --serial YOUR_SERIAL --board mir63a0-revp21
```

Open the printed remote address for screen preview, Back/Home, directional
navigation, Wi-Fi setup, text entry, volume and wake/sleep. See
[computer and phone controls](docs/REMOTE.md). The remote defaults to this
computer; phone access requires an explicit trusted-LAN bind address.

For a new installation, the guided sequence is **inspect → build → bundle →
plan → flash → configure → verify**. The recovery guide gives the exact commands
and explains which steps replace data. Images and partition geometry are checked
before a serial-specific plan can be executed.

## Development

```sh
python3 -m unittest discover -s tests -v
```

Python and JavaScript source written for this recovery project is tracked here.
Vendor firmware, keys, room images, recordings and full Android source trees are
excluded. Read [build inputs and redistribution](docs/BUILD.md) before preparing
an image. A checksum identifies an artifact; it does not establish its origin or
permission to redistribute it.
