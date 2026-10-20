# Build inputs and redistribution

The starting implementation comes from mirror-mirror commit history, including
its Android revival patch, manifest rewrite, filesystem tools and kernel/Wi-Fi
compatibility work. The migration will make the required inputs explicit here.

Android and Qualcomm source trees, licensed vendor components and kernel inputs
are needed to build system. The original workstation's `.work` directory is not
a distributable SDK. Build inputs must be pinned, hash-checked and attributable;
public availability alone is not a license to redistribute vendor binaries.

Never publish owner ADB keys, private keys, Wi-Fi configuration, room recordings,
camera captures or an image containing a previous owner's authorization. Build
authorization for the receiving owner's public key. RSA authentication remains
enabled; generic auto-authorization and unrestricted LAN ADB are not defaults.

Until clean-checkout reconstruction and artifact provenance are verified, do not
advertise a ready-to-flash public firmware release. The CLI and documentation
can be used for inspection without any firmware download.
