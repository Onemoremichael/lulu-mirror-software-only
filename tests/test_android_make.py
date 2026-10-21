import os
from pathlib import Path
import subprocess
import unittest


class AndroidMakeTests(unittest.TestCase):
    def test_error_trap_ignores_handled_subshell_probe_but_reports_fatal_errors(self):
        recipe = Path(__file__).resolve().parent.parent / 'build/container-build.sh'
        trap = next(line for line in recipe.read_text().splitlines() if line.startswith('trap '))
        for body, fatal in [('probe() { local colors=$(false); }; probe; echo survived', False),
                            ('false', True), ('result=$(false)', True)]:
            with self.subTest(body=body):
                result = subprocess.run(['bash', '-c', 'set -Eeuo pipefail\n' + trap + '\n' + body],
                                        capture_output=True, text=True)
                if fatal:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn('Build step failed', result.stderr)
                    self.assertIn('false', result.stderr)
                else:
                    self.assertEqual(result.returncode, 0)
                    self.assertEqual(result.stderr, '')
                    self.assertEqual(result.stdout.strip(), 'survived')

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
