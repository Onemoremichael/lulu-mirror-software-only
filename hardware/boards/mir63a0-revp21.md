# MIR63A0-00-P1 / PCA#500240 RevP21

- Stable ID: `mir63a0-revp21`.
- Evidence level: **research-unit recovered**, not repeatable recovery.
- SoC family: APQ8016/MSM8916, as recorded in the original research; the tooling
  checks the observed `msm8916` platform and requires physical label attestation.
- Research OS: reconstructed Android 6.0.1 with stock kernel
  `3.10.49-perf-gf46dad5260f`; retains the signed boot chain, boot and recovery.
- Exact peripheral/firmware equivalence across other RevP21 units is unproven.
- Profile: [`mir63a0-revp21`](../../profiles/mir63a0-revp21.json). Its presence
  does not certify the newly extracted firmware or every unit with this label.
- Primary evidence: [original recovery checkpoint](https://github.com/Onemoremichael/mirror-mirror/blob/main/RECOVERY-STATUS.md),
  [source provenance](../../docs/PROVENANCE.md),
  [migration/build evidence](../../docs/STATUS.md). Historical research lives in
  mirror-mirror; new independent reports should use this repository's issue forms.

## Component and reuse map

| Subsystem | Evidence on the research unit | Transfer boundary |
| --- | --- | --- |
| Boot/security/USB | Useful Android without bootloader unlock; generic Qualcomm programmers rejected; fastboot/recovery observed | Signing policy and write behavior must be measured on each firmware/board; no universal Qualcomm unlock inferred |
| Storage/userdata | Compatible ext4 features and vold handoff needed; one-download sparse handling mattered | Filesystem tooling may transfer; geometry, encryption handoff and download limits do not transfer as constants |
| Display | Stock kernel drives 1080p non-touch LCD, roughly upper two-thirds of mirror | Preserve kernel/panel bindings; same screen appearance is not proof of equal device tree or orientation |
| Wi-Fi | Matching stock-kernel module and Android framework integration | Module/config/firmware must match target ABI and hardware; exact radio identity not newly cataloged here |
| Audio | Speaker route/amplifier setup and microphone worked on research image | Mixer/codec/amp topology and routing require separate tests; do not infer Bluetooth acceptance |
| Camera | Fixed-focus OV5640; sensor/ISP ABI, metadata, NV12 packing and orientation adaptations | Exact sensor/vendor hashes and ABI are prerequisites; dark/noisy preview and intermittent startup remain limitations |

## Attempts and current acceptance

September 2026 research recovered one unit; camera preview/photo/software video
worked with recorded limitations. October migration extracted host tools,
owner-specific authorization, kernel/Wi-Fi/audio and minimal camera recipes.
[PR #4](https://github.com/Onemoremichael/lulu-mirror-software-only/pull/4)
produced an inspected legacy-workspace image, using a disposable test key.
[PR #5](https://github.com/Onemoremichael/lulu-mirror-software-only/pull/5)
validated fresh camera headers and read-only checks against the existing install.
[PR #6](https://github.com/Onemoremichael/lulu-mirror-software-only/pull/6)
added actual checkout HEAD inventory. The [status history](../../docs/STATUS.md)
retains build failures and corrections; hashes are not substituted for runtime tests.

The extracted image has **not** been flashed or physically accepted. No second
owner has completed the published recovery process. Matching vendor provenance,
clean-source reproduction and release licensing remain open. Bootloader unlock,
unrestricted root, modern Android upgrades and Bluetooth acceptance are not
claimed. The working owner's installation must remain unchanged without consent.

## Next work

Independent redacted owner reports can establish revision/firmware/peripheral
variation now. A suitably resourced clean build and attributable vendor inputs
are needed before reproduction claims. Exact-image physical acceptance should
use a separately approved target, preferably a spare matching unit. See the
[acceptance checklist](../../docs/ACCEPTANCE.md); no new owner needs to flash to
help identify hardware or review sources.
