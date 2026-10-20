# lulu-mirror-software-only

Recover a discontinued lululemon Studio MIRROR as a usable Android computer on
its original mainboard. The screen has no touch layer; setup and everyday
control happen from your computer or phone.

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
The extracted build pipeline is still under validation; it is not yet a
hardware-accepted replacement image. See the [camera migration](camera/README.md)
for the compatibility mechanisms and remaining acceptance checks.

## Start here

The supported hardware candidate is **MIR63A0-00-P1 / PCA#500240 RevP21**,
Qualcomm APQ8016/MSM8916. Check the printed board label. Other revisions need
their own evidence; a matching chipset alone is insufficient.

Requirements: Python 3.10+ and Google's Android platform-tools (`adb`,
`fastboot`) on your PATH. No Python packages are required.

```sh
python3 mirror.py doctor
python3 mirror.py devices
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

```sh
# Once Android ADB is authorized:
python3 mirror.py configure --serial YOUR_SERIAL --board mir63a0-revp21
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
