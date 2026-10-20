#!/usr/bin/env bash
set -euo pipefail
# Invoked by tools/build-system.py in the pinned Linux build environment.
tree=/source
mounted=0
if [[ -f /source.img ]]; then
  mkdir -p "$tree"
  mount -o loop /source.img "$tree"
  mounted=1
fi
cleanup() {
  cd /
  if [[ "$mounted" = 1 ]]; then sync; umount "$tree"; fi
}
trap cleanup EXIT
cd "$tree"
test -s build/envsetup.sh
test -s vendor/qcom/proprietary/prebuilt_HY22/Android.mk
python /inputs/prepare.py --tree "$tree" --public-key /owner.pub --inputs /inputs

# Compile only a compatibility module for the existing stock kernel. Never export a boot image.
kernel_out="$tree/out/kernel-software-only"
mkdir -p "$kernel_out"
cp /inputs/kernel.config "$kernel_out/.config"
kernel/scripts/config --file "$kernel_out/.config" \
  --set-str LOCALVERSION '-perf-gf46dad5260f' --disable LOCALVERSION_AUTO
cross="$tree/prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/bin/aarch64-linux-android-"
make -C kernel O="$kernel_out" ARCH=arm64 CROSS_COMPILE="$cross" olddefconfig
make -C kernel O="$kernel_out" -j"${BUILD_JOBS:-4}" ARCH=arm64 CROSS_COMPILE="$cross"
wlan="$tree/vendor/qcom/opensource/wlan/prima"
make -C kernel O="$kernel_out" -j"${BUILD_JOBS:-4}" ARCH=arm64 CROSS_COMPILE="$cross" \
  M="$wlan" WLAN_ROOT="$wlan" MODNAME=wlan BOARD_PLATFORM=msm8916 CONFIG_PRONTO_WLAN=m modules
modinfo "$wlan/wlan.ko" | grep -q '3.10.49-perf-gf46dad5260f'

export USE_CCACHE=1
export CCACHE_DIR="$tree/.ccache"
# Legacy Android's envsetup is not compatible with nounset.
set +u
source build/envsetup.sh
lunch msm8916_64-userdebug
set -u
make -j"${BUILD_JOBS:-4}" systemimage
product=out/target/product/msm8916_64
install -m 0644 "$wlan/wlan.ko" "$product/system/lib/modules/pronto/pronto_wlan.ko"
# The original product doesn't include the camera media controller modules in its
# package list; retain the vendor components needed by its installed daemon.
vendor=vendor/qcom/proprietary/prebuilt_HY22/target/product/msm8916_64/system/vendor/lib
for module in stats iface isp sensor pproc imglib c2d cpp vpe wnr; do
  if [[ -s "$vendor/libmmcamera2_${module}_modules.so" ]]; then
    install -m 0755 "$vendor/libmmcamera2_${module}_modules.so" "$product/system/vendor/lib/"
  elif [[ -s "$vendor/libmmcamera2_${module}_module.so" ]]; then
    install -m 0755 "$vendor/libmmcamera2_${module}_module.so" "$product/system/vendor/lib/"
  else
    echo "Missing vendor camera module: $module" >&2; exit 1
  fi
done
# Remove known lab-only generated files from a migrated output tree.
rm -f "$product/system/lib/modules/mirror_camera_diag.ko" "$product/system/vendor/lib/libMD2.so"
sed -i '/^persist.camera.*debug/d; /^debug.mirror./d; /^service.adb.tcp.port=/d; /^ro.mirror.software_only=/d' "$product/system/build.prop"
printf '\nservice.adb.tcp.port=-1\nro.mirror.software_only=1\n' >> "$product/system/build.prop"
make -j"${BUILD_JOBS:-4}" snod
cp "$product/system.img" /artifacts/system.img
cp "$wlan/wlan.ko" /artifacts/pronto_wlan.ko
cp "$product/system/build.prop" /artifacts/build.prop
sha256sum /artifacts/system.img /artifacts/pronto_wlan.ko > /artifacts/SHA256SUMS

# Inspect the built filesystem, rather than accepting make's exit code alone.
out/host/linux-x86/bin/simg2img /artifacts/system.img /artifacts/system.raw.img
mkdir -p /inspect
mount -o loop,ro /artifacts/system.raw.img /inspect
trap 'umount /inspect; cleanup' EXIT
grep -qx 'service.adb.tcp.port=-1' /inspect/build.prop
grep -qx 'ro.mirror.software_only=1' /inspect/build.prop
test -s /inspect/app/Launcher3/Launcher3.apk
test -s /inspect/lib/modules/pronto/pronto_wlan.ko
test ! -e /inspect/lib/modules/mirror_camera_diag.ko
test ! -e /inspect/vendor/lib/libMD2.so
umount /inspect
trap cleanup EXIT
rm -f /artifacts/system.raw.img
echo 'System image built and filesystem checks passed. No device was accessed.'
