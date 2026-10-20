from .device import RecoveryError, adb, inspect


def configure(serial, board, orientation):
    identity = inspect(serial, board)
    if identity['transport'] != 'adb' or not identity['compatible']:
        raise RecoveryError('Android setup requires the compatible, authorized ADB device.')
    # This panel's measured upright portrait rotation is 3 (270 degrees).
    rotation = '3' if orientation == 'portrait' else '0'
    for namespace, key, value in [('global', 'device_provisioned', '1'),
                                  ('secure', 'user_setup_complete', '1'),
                                  ('system', 'accelerometer_rotation', '0'),
                                  ('system', 'user_rotation', rotation)]:
        adb(serial, 'shell', 'settings', 'put', namespace, key, value)
        if adb(serial, 'shell', 'settings', 'get', namespace, key) != value:
            raise RecoveryError(f'Android did not retain {key}.')
    adb(serial, 'shell', 'input', 'keyevent', '224')
    adb(serial, 'shell', 'wm', 'dismiss-keyguard')
    adb(serial, 'shell', 'input', 'keyevent', '3')
    return {'configured': True, 'orientation': orientation,
            'next': 'Open the remote, connect Wi-Fi through Android settings, and run verify.'}
