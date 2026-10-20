# Verification status

As of October 20, 2026, this repository is being extracted into a focused recovery
project. Original hardware evidence is in
[mirror-mirror's checkpoint](https://github.com/Onemoremichael/mirror-mirror/blob/main/RECOVERY-STATUS.md).

| Requirement | Evidence / remaining work |
| --- | --- |
| Usable Android 6.0.1 on original board | Verified on one RevP21 unit in September 2026 |
| Preserved boot chain and stock kernel | Original recovery checkpoint and build recipes |
| Wi-Fi, speaker, microphone, ADB | Verified on original unit; second-owner validation needed |
| Camera | Research image usable with dark/noisy image and intermittent startup limitations |
| Clean-checkout recovery tools | Under migration; tests must verify command boundaries |
| Reproducible Android build | Local legacy source/vendor inputs still need extraction and provenance |
| Public firmware release | Not published; redistribution and owner authorization need review |
| Second owner installation | Not yet verified |

No Mirror is connected to the development Mac at the start of this migration.
Host-side checks cannot replace device boot, cold restart, network, speaker or
microphone acceptance. Record those results with dates and image hashes.
