# Recovery guide

1. Read the printed board label and check [compatibility](COMPATIBILITY.md).
2. Run `python3 mirror.py doctor` and `python3 mirror.py devices`.
3. If authorized Android ADB already works, inspect that installation first.
   There is no reason to erase working Android just to install ordinary apps.
4. If the stock application blocks access, the tested PCB enters fastboot when
   powered on with VOL- held. A blank display in fastboot can be normal. VOL+
   enters the original signed recovery/update UI. “Update complete” alone is
   not proof that custom Android was installed.
5. In fastboot, inspect the explicitly selected serial and record the actual
   system/userdata partition sizes. Do not borrow another owner's geometry.
6. Build or obtain a verified image for the exact profile, and prepare fresh
   userdata with your own ADB public key. See [build inputs](BUILD.md).
7. Follow the generated recovery plan, then verify Android before adding apps.

Recovery replaces system and, when needed, userdata. Replacing userdata deletes
installed applications and personal data. Obtain any available backup first.
The research project did not obtain a complete factory eMMC backup: empty boot
dump files are not backups. Preserve anything readable from your own unit.

Keep boot, recovery, bootloader, trust, modem, partition tables and board firmware
intact. The recovery does not need an OEM unlock command or an unsigned Firehose.
The tested OEM secure-boot root rejected generic Qualcomm programmers.

The existing signed boot image forces an encryption handoff which the replacement
system could not complete. The recovery's vold patch mounts fresh userdata
unencrypted. Do not expect encryption at rest from this Android installation.
Modern host `fastboot format:ext4 userdata` produced unsupported ext4 features;
use the Android-compatible userdata builder instead. The tested bootloader also
rejected a later split sparse userdata chunk; send a verified image whole within
the actual download limit.

If a flash fails, stop and retain the command output. Remain in fastboot, inspect
the device and image again, and correct that step. Reboot only after required
writes succeed. Do not try unrelated partitions to cure a blank display.

## Prepare fresh userdata locally

Use the public half of the ADB key belonging to the computer that will control
the mirror. Start `adb start-server` to create a key if you have never used ADB.
Keep the private `adbkey` file on that computer. Install e2fsprogs (`brew install
e2fsprogs` on macOS) for debugfs/e2fsck/dumpe2fs. Google's platform-tools supply
the legacy-compatible `mke2fs` and `mke2fs.conf`; generic modern defaults are
rejected if they introduce unsupported filesystem features.

```sh
# Replace SIZE_FROM_INSPECT with this unit's actual userdata partition bytes.
# On macOS, add Homebrew's e2fsprogs sbin directory to PATH first.
export PATH="$(brew --prefix e2fsprogs)/sbin:$PATH"
python3 tools/build-userdata.py --size SIZE_FROM_INSPECT \
  --public-key "$HOME/.android/adbkey.pub" --output-dir artifacts/my-userdata
python3 tools/sparse-userdata.py artifacts/my-userdata/userdata-adb.img \
  artifacts/my-userdata/userdata.sparse
```

If `mke2fs` on PATH is from e2fsprogs rather than Android platform-tools, set
`MKE2FS_PATH` and `MKE2FS_CONFIG` to the platform-tools executable and its config.
`DEBUGFS_PATH`, `E2FSCK_PATH`, and `DUMPE2FS_PATH` can override the other tools.
The builder verifies key readback, ownership, modes, SELinux labels, filesystem
features and e2fsck. The converter omits only zero-valued free blocks and verifies
the expanded hash. DONT_CARE sparse ranges do not securely erase old free space.

## Plan, inspect, execute

Supply a system image built for this profile and owner. `bundle` records hashes
and validates the complete sparse stream; it does not authenticate firmware
provenance. The bundle references local files and does not copy or upload them.

```sh
python3 mirror.py bundle --board mir63a0-revp21 \
  --system artifacts/system.img --userdata artifacts/my-userdata/userdata.sparse \
  --directory bundles/my-recovery --provenance 'My documented source build'
python3 mirror.py plan --serial YOUR_SERIAL --board mir63a0-revp21 \
  --bundle bundles/my-recovery/bundle.json --output reports/recovery-plan.json
```

Read the plan. `system` is required; omit `--userdata` only when deliberately
retaining an already usable data filesystem. Unknown partition sizes or download
limits stop planning. The only writable partitions are system and userdata.
Bootloader security remains in place; write support on this one tested unit does
not prove that another unit accepts the same images.

```sh
python3 mirror.py flash --plan reports/recovery-plan.json \
  --confirm 'RECOVER YOUR_SERIAL' --journal reports/flash-journal.json
fastboot -s YOUR_SERIAL reboot
python3 mirror.py verify --serial YOUR_SERIAL --board mir63a0-revp21 \
  --output reports/android-verification.json
```

Execution re-reads device identity, limits and hashes rather than trusting commands
in a plan file. Any changed evidence requires a new plan. Failed writes halt the
sequence and leave a journal; there is no automatic retry or reboot. Verification
checks boot, Android version, launcher, display, userdata, Wi-Fi driver and RSA
ADB configuration. Cold boot, saved Wi-Fi reconnection, Internet, audible speaker
output, microphone quality and camera quality still require physical acceptance.
