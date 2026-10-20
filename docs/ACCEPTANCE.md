# Accepting an owner-built recovery image

A successful build, filesystem inspection or ADB response is not a completed
hardware acceptance test. Keep the build report and image hashes, then record
the following on the owner's matching RevP21 unit. Do not publish serials, owner
keys, Wi-Fi credentials, room screenshots or recordings in GitHub issues.

Nothing in this checklist runs automatically. Follow [RECOVERY.md](RECOVERY.md)
for the explicit flash plan; an attached device never authorizes a flash by
itself. Do not test an image from an unfinished or failed build.

## Establish the installation

1. Record the system image SHA-256 and the owner public-key fingerprint from the
   build report. Keep the private ADB key on the controlling computer.
2. After successful planned writes and reboot, run:

   ```sh
   python3 mirror.py verify --serial YOUR_SERIAL --board mir63a0-revp21 \
     --output reports/acceptance-android.json
   ```

3. Use `configure` and the [remote](REMOTE.md) to reach normal Launcher3. Confirm
   Back, Home, directional navigation, screen preview, volume, Sleep and Wake.
   Waking should not open the old Afterglow menu. No assistant, dashboard or
   clock should need to launch for Android to remain usable.
4. Confirm the chosen portrait/landscape orientation on the physical screen.
   This is a non-touch display occupying roughly the mirror's upper two-thirds.

The automated report checks observable Android state. It does not prove that
the panel is readable, speakers are audible or the camera image is usable.

## Test the hardware, with the owner present

| Check | What to observe |
| --- | --- |
| Cold boot | Normal Android starts after a deliberate power-off/restart; no encryption-failure screen or recovery/update loop |
| Saved Wi-Fi | Connect using Settings through the remote, reboot, and confirm the saved network reconnects and Internet/DNS work |
| USB authorization | The intended computer remains authorized; another computer must not inherit the original research owner's key |
| Phone controls | On the same trusted LAN, open the explicitly LAN-bound remote; confirm Back/Home and stop the service after testing |
| Speakers | Play owner-chosen audio in Android, start at low volume, and confirm audible output and volume controls |
| Microphone | With explicit consent, make and play a short local recording; confirm it uses the mirror microphone, then delete the test recording when no longer needed |
| Camera preview | Open the included camera app; confirm there is one front camera, upright preview and correct proportions |
| Photo | With consent, save a test photo and inspect its actual saved orientation and proportions, not just the preview |
| Video | With consent, record a short software-encoded clip with audio; inspect the saved clip's orientation, decode, sound and synchronization |
| Repeatability | Repeat camera open/release and a post-reboot open; record failures as well as passes rather than treating one successful frame as reliability proof |

The original research camera remained dark/noisy and sometimes failed to start.
Its software recording was around 23 fps, not a verified 30 fps. The minimal
recovery baseline deliberately excludes the exposure experiments and diagnostic
kernel module. Do not describe the new image as camera-equivalent merely because
its native files have matching hashes. See [camera details](../camera/README.md).

## Record outcomes without changing the evidence

Keep a local note under ignored `reports/` containing the image hash, date, board
label confirmation, each pass/fail/not-tested result and any observed failures.
Retain failed build/flash logs. An untested row remains untested; do not copy a
pass from the original research unit or a previous firmware image.

Stop if a required function regresses. Inspection and app testing do not require
another flash; diagnose the particular failure before replacing partitions.
Original boot/recovery/board firmware must remain outside recovery write plans.
