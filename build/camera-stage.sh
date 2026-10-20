# Sourced after the Android environment is selected, before the final system pack.
# The native camera artifacts were compiled/hash-checked by tools/build-camera.py.
prepare_camera_sources() {
  python /inputs/prepare-camera.py --tree "$tree" --patches /camera-patches
  make -j"${BUILD_JOBS:-4}" camera.msm8916_32 libstagefright libstagefright_32 SnapdragonCamera
}

install_camera_artifacts() {
  install -m 0755 /camera-artifacts/libmmcamera_ov5640.so "$product/system/vendor/lib/libmmcamera_ov5640.so"
  install -m 0755 /camera-artifacts/libmmcamera_mirror_haf.so "$product/system/vendor/lib/libmmcamera_mirror_haf.so"
  install -m 0755 /camera-artifacts/mm-qcamera-daemon "$product/system/bin/mm-qcamera-daemon"
  install -m 0755 /camera-artifacts/libmmcamera2_cpp_module.so "$product/system/vendor/lib/libmmcamera2_cpp_module.so"
  sed -i '/^ro.mirror.camera.front=/d; /^debug.mirror.video_raw=/d' "$product/system/build.prop"
  printf '\nro.mirror.camera.front=1\ndebug.mirror.video_raw=1\n' >> "$product/system/build.prop"
}

verify_camera_image() {
  grep -qx 'ro.mirror.camera.front=1' /inspect/build.prop
  grep -qx 'debug.mirror.video_raw=1' /inspect/build.prop
  for component in libmmcamera_ov5640.so libmmcamera_mirror_haf.so libmmcamera2_cpp_module.so; do
    cmp "/camera-artifacts/$component" "/inspect/vendor/lib/$component"
  done
  cmp /camera-artifacts/mm-qcamera-daemon /inspect/bin/mm-qcamera-daemon
  grep -a -q 'Mirror camera metadata: front, mount 0' /inspect/lib/hw/camera.msm8916.so
  for arch in lib lib64; do
    grep -a -q 'Mirror recording: refusing oversized input' "/inspect/$arch/libstagefright.so"
  done
  test -s /inspect/app/SnapdragonCamera/SnapdragonCamera.apk
}
