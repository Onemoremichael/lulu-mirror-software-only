# Panels, revision labels and regulatory anchors

These are **researched** identifiers, not a list of flashable combinations. See
claims **p01–p06/r01–r03** in [catalog.json](catalog.json) for exact attribution.

| Entity | Source association | Boundary |
| --- | --- | --- |
| BOE DV430FHM-NN5 | olm3ca's own Rev08-designated unit | No SoC or complete PCB label established by this designation here |
| LM40SAMFHD700AG25WV | Owner conversion reports | Original-board firmware relationship not established |
| Samsung LTI400HN01 | MDME teardown and owner accounts | No universal controller/cable equivalence |
| RevP1 | Linked photo-album designation | Namespace unresolved; not normalized into RevP21 |
| FCC 2AOSD-RLSYM1R0 | 2018 Curiouser filing metadata | Regulatory identifier is not a PCB revision |

Primary community sources: [pinned hardware-version notes](https://github.com/olm3ca/mirror/blob/c3dd836150759b9302e5d797c0b63c79ac06cc4a/README.md),
[LM40 owner report](https://github.com/olm3ca/mirror/issues/8),
[LTI owner report](https://github.com/olm3ca/mirror/issues/24), and
[two-unit purchase/manufacture-date observation](https://github.com/olm3ca/mirror/issues/36).
Those display-controller conversions do not validate an original-board software
unlock. Do not transfer their electrical instructions into our recovery guide.

Marketing size, year bought, branding and a reset button are weak clues. Record
them as observations, but do not use them to assign SoC, revision or firmware.
Manufacture and purchase dates differ; overlapping inventory defeats a clean
"old chipset/new panel" timeline. We have not established the total panel count.
The suggested relation between BOE module/cell identifiers, and between the two
40-inch assemblies, is not adopted as an interchangeable pinout or cable claim.

## Regulatory research boundary

The [filing index](https://fccid.io/2AOSD-RLSYM1R0) identifies an internal-photo
exhibit, but attempts to retrieve its PDF through the available web paths failed.
Consequently this pass makes **no component identification from those photos**.
Future review should use the actual exhibit and document the page/label, not
infer a BOM from the FCC model name. Other grantee entries for connected weights
are accessories, not additional MIRROR mainboards.

## Exclude similar-looking products

The [Rflex owner report](https://github.com/olm3ca/mirror/issues/23) describes a
different product with a related-looking display assembly. It is useful as a
comparison, not proof of a lululemon variant. Likewise unrelated fitness-mirror
FCC results, retail RFID case studies, guessed Amlogic processors and
replacement Raspberry Pi/Jetson/TV boards are not added as original MIRROR SoCs.

## Useful shared-hardware work

Build a same-unit relation map: original PCB → stock display driver/bridge →
TCON → exact panel, alongside audio/radio/camera assemblies. Shared panels can
focus timing/bridge research; shared sensors can focus driver research. Neither
relationship establishes boot trust or firmware compatibility. Unobserved edges
remain absent rather than being filled by a Cartesian product of known parts.
