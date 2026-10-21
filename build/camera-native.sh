#!/usr/bin/env bash
set -euo pipefail
mounted=0
tree=/source
if [[ -f /source.img ]]; then
  tree=/mnt/build
  mkdir -p "$tree"
  mount -o loop,ro,noload /source.img "$tree"
  mounted=1
fi
cleanup() { cd /; if [[ "$mounted" = 1 ]]; then umount "$tree"; fi; }
trap cleanup EXIT
cc="$tree/prebuilts/gcc/linux-x86/arm/arm-linux-androideabi-4.9/bin/arm-linux-androideabi-gcc"
strip="$tree/prebuilts/gcc/linux-x86/arm/arm-linux-androideabi-4.9/bin/arm-linux-androideabi-strip"
readelf="$tree/prebuilts/gcc/linux-x86/arm/arm-linux-androideabi-4.9/bin/arm-linux-androideabi-readelf"
sysroot="$tree/prebuilts/ndk/9/platforms/android-21/arch-arm"
sensors=/sdk/camera/services/mm-camera-legacy/mm-camera2/media-controller/modules/sensors
headers="$tree/out/target/product/msm8916_64/obj/KERNEL_OBJ/usr/include"
if [[ ! -f "$headers/media/msm_cam_sensor.h" || "${CAMERA_FRESH_HEADERS:-0}" = 1 ]]; then
  # A clean checkout has no Android output yet. Export the matching kernel's
  # userspace headers in a temporary directory without compiling/flashing a kernel.
  mkdir -p /tmp/camera-headers
  make -C "$tree/kernel" O=/tmp/camera-headers ARCH=arm64 headers_install \
    INSTALL_HDR_PATH=/tmp/camera-headers/usr
  headers=/tmp/camera-headers/usr/include
fi
mkdir -p /tmp/sensor-include
cp "$sensors/includes/sensor_lib.h" /tmp/sensor-include/sensor_lib.h
patch /tmp/sensor-include/sensor_lib.h < /patches/quectel-ov5640-hy22-abi.patch
cp "$sensors/sensor_libs/ov5640/ov5640_lib.c" /tmp/ov5640_lib.c
patch /tmp/ov5640_lib.c < /patches/quectel-ov5640-hy22-modes.patch
patch /tmp/ov5640_lib.c < /patches/mirror-ov5640-stock-modes.patch
"$cc" --sysroot="$sysroot" -fPIC -shared -Wl,--no-undefined -DVFE_40 \
  -I/tmp/sensor-include -I"$sensors/includes" -I"$headers" -I"$tree/system/core/include" \
  -Wl,-soname,libmmcamera_ov5640.so -o /artifacts/libmmcamera_ov5640.so /tmp/ov5640_lib.c
"$readelf" -s /artifacts/libmmcamera_ov5640.so > /artifacts/sensor-symbols.txt
awk '$NF == "sensor_lib_ptr" { if ($3 == 376) ok=1 } END { exit !ok }' /artifacts/sensor-symbols.txt
awk '$NF == "sensor_out_info" { if ($3 == 96) ok=1 } END { exit !ok }' /artifacts/sensor-symbols.txt
"$strip" --strip-unneeded /artifacts/libmmcamera_ov5640.so
"$cc" --sysroot="$sysroot" -fPIC -shared -nostdlib -Wall -Wextra -Werror \
  -Wl,-soname,libmmcamera_mirror_haf.so -o /artifacts/libmmcamera_mirror_haf.so /patches/isp-compat.c
"$readelf" -Ws /artifacts/libmmcamera_mirror_haf.so > /artifacts/compat-symbols.txt
grep -Eq '[[:space:]]ioctl$' /artifacts/compat-symbols.txt
vendor="$tree/vendor/qcom/proprietary/prebuilt_HY22/target/product/msm8916_64/system"
cp "$vendor/bin/mm-qcamera-daemon" /artifacts/mm-qcamera-daemon
cp "$vendor/vendor/lib/libmmcamera2_cpp_module.so" /artifacts/libmmcamera2_cpp_module.so
echo 'Camera sensor ABI and compatibility library compiled.'
