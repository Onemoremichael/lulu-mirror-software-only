from datetime import datetime, timezone
from .device import adb, inspect, RecoveryError


def verify(serial, board):
    identity = inspect(serial, board)
    if identity['transport'] != 'adb':
        raise RecoveryError('Verification requires authorized Android ADB.')
    props = identity['properties']
    launcher = adb(serial, 'shell', 'pm', 'path', 'com.android.launcher3')
    size = adb(serial, 'shell', 'wm', 'size')
    data = adb(serial, 'shell', 'df', '/data')
    wifi = adb(serial, 'shell', 'getprop', 'wlan.driver.status')
    checks = {
        'matching_kernel_platform': identity['compatible'],
        'android_6_0_1': props['ro.build.version.release'] == '6.0.1',
        'boot_completed': props['sys.boot_completed'] == '1',
        'launcher_installed': launcher.startswith('package:'),
        'adb_requires_authorization': props['ro.adb.secure'] == '1',
        'display_1080p': '1080' in size and '1920' in size,
        'userdata_mounted': '/data' in data,
        'wifi_driver_loaded': wifi == 'ok',
    }
    return {'schema': 1, 'at': datetime.now(timezone.utc).isoformat(),
            'identity': identity, 'checks': checks, 'automated_checks_passed': all(checks.values()),
            'display': size, 'data_filesystem': data, 'wifi_driver_status': wifi,
            'manual_acceptance': {'cold_boot_and_wifi_reconnect': 'not_measured',
                                  'internet_and_dns': 'not_measured',
                                  'speakers_audible': 'not_measured',
                                  'microphone_usable': 'not_measured',
                                  'camera_image_quality': 'not_measured'}}
