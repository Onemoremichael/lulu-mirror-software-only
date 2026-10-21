import os
from pathlib import Path
import subprocess
import unittest


class AndroidMakeTests(unittest.TestCase):
    def test_vendor_modules_get_relative_prepared_kernel_output(self):
        recipe = Path(__file__).resolve().parent.parent / 'build/android-make.sh'
        # Replace make with an argument-printing shell function. No compilation.
        command = '''
make() { printf '%s\n' "$@"; }
tree='/tmp/source with spaces'
kernel_out="$tree/out/kernel-software-only"
product=out/target/product/msm8916_64
source "$1"
android_make systemimage camera.msm8916_32
'''
        result = subprocess.check_output(['bash', '-c', command, 'test', str(recipe)],
                                         env=dict(os.environ, BUILD_JOBS='2'), text=True).splitlines()
        self.assertIn('-j2', result)
        self.assertIn('KERNEL_OUT=out/kernel-software-only', result)
        self.assertIn('KERNEL_CONFIG=out/kernel-software-only/.config', result)
        self.assertIn('TARGET_KERNEL_DLKM_DISABLE=true', result)
        self.assertIn('TARGET_PREBUILT_KERNEL=/tmp/source with spaces/out/kernel-software-only/arch/arm64/boot/Image.gz-dtb', result)
        self.assertIn('KERNEL_HEADERS_INSTALL=/tmp/source with spaces/out/target/product/msm8916_64/obj/KERNEL_OBJ/usr', result)
        self.assertEqual(result[-2:], ['systemimage', 'camera.msm8916_32'])
