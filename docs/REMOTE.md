# Control Android without a touchscreen

The screen is output only. After Android boots and your computer has authorized
ADB, finish setup and open the remote:

```sh
python3 mirror.py configure --serial YOUR_SERIAL --board mir63a0-revp21
python3 mirror.py remote --serial YOUR_SERIAL --board mir63a0-revp21
```

`configure` marks Android's first-run setup complete, locks the measured portrait
rotation, wakes/dismisses the keyguard and goes Home. It does not select a new
launcher or install optional apps. Add `--orientation landscape` if preferred.

Open the printed address, normally <http://127.0.0.1:8765>. Use Back, Home,
directional navigation, Settings, Wi-Fi settings, volume and wake/sleep. Refresh
the screen to view Android; click/tap its preview or drag for a swipe. Screen
refresh is manual until you enable automatic refresh. Images are decoded before
replacement so a slow ADB capture does not blank the preview.

Select an Android text field, enter text in the remote and send it. The remote
masks text because Wi-Fi setup may need a password. It does not persist text or
screenshots. Android may display the entered text; navigate carefully.

For an iPhone on the same trusted Wi-Fi, bind to this computer's specific LAN
address (find it in Network settings):

The bind must be loopback or an explicit RFC1918 LAN IPv4 address (10/8,
172.16/12 or 192.168/16). Wildcard `0.0.0.0`, public addresses and IPv6 are
rejected before contacting Android. This restricts binding; it does not add
authentication or make an untrusted LAN safe.

```sh
python3 mirror.py remote --serial YOUR_SERIAL --board mir63a0-revp21 \
  --host YOUR_COMPUTERS_PRIVATE_IPV4
```

Open that printed address on the phone. Anyone on that network who can reach
the remote can control Android; there is no access key. Stop it with Ctrl+C when
finished. Do not forward its port through your router. No account or cloud
service is involved. Every command stays pinned to the selected serial.

USB works without enabling network ADB. Wi-Fi ADB is optional: use Android's
existing authorized ADB workflow if your installation supports it. The firmware
builder does not automatically enable port 5555. A USB reconnect/reboot can
remove `adb reverse` tunnels used by other apps; this Android remote itself
does not need reverse tunnels.

For a native desktop window, optionally install scrcpy from its official
distribution and run `scrcpy -s YOUR_SERIAL --no-audio`. That tool is independent
of this repository.
