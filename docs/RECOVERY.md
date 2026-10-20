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
