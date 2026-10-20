# Sourced after selecting the Android product and compiling the compatible kernel.
android_make() {
  # Vendor module recipes prepend ../ to KERNEL_OUT, so it must stay relative
  # to the Android source root even though TARGET_PREBUILT_KERNEL is absolute.
  make -j"${BUILD_JOBS:-2}" \
    TARGET_PREBUILT_KERNEL="$kernel_out/arch/arm64/boot/Image.gz-dtb" \
    KERNEL_OUT=out/kernel-software-only \
    KERNEL_CONFIG=out/kernel-software-only/.config \
    TARGET_KERNEL_DLKM_DISABLE=true \
    KERNEL_HEADERS_INSTALL="$tree/$product/obj/KERNEL_OBJ/usr" "$@"
}
