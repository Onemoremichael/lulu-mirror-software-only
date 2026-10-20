#!/usr/bin/env python
"""Apply camera HAL, recording and UI fixes transactionally in the build workspace."""
from __future__ import print_function
import argparse
import io
import os
import shutil
import subprocess
import tempfile


def prepare(tree, patches):
    changes = [
        ('hardware/qcom/camera', 'QCamera2/HAL/QCamera2Factory.cpp', 'mirror-camera-metadata.patch', 'ro.mirror.camera.front'),
        ('hardware/qcom/camera', 'QCamera2/HAL/QCamera2Factory.cpp', 'mirror-camera-mount-correction.patch', 'front, mount 0'),
        ('frameworks/av', 'media/libstagefright/CameraSource.cpp', 'mirror-camera-raw-video.patch', 'debug.mirror.video_raw'),
        ('frameworks/av', 'media/libstagefright/MediaCodecSource.cpp', 'mirror-codec-video-pack.patch', 'mirror_pack_venus_nv12'),
        ('packages/apps/SnapdragonCamera', 'src/com/android/camera/PhotoUI.java', 'mirror-snapcam-preview.patch', 'mMirrorSensorAspectRatio'),
        ('packages/apps/SnapdragonCamera', 'src/com/android/camera/PhotoModule.java', 'mirror-snapcam-photo-rotation.patch', 'private int getCaptureRotation'),
        ('packages/apps/SnapdragonCamera', 'src/com/android/camera/PhotoModule.java', 'mirror-snapcam-photo-front-rotation.patch', 'Front preview is mirrored; saved JPEG is not'),
        ('packages/apps/SnapdragonCamera', 'src/com/android/camera/VideoUI.java', 'mirror-snapcam-video-preview.patch', 'mMirrorSensorAspectRatio'),
        ('packages/apps/SnapdragonCamera', 'src/com/android/camera/VideoModule.java', 'mirror-snapcam-video-rotation.patch', 'Mirror video rotation='),
        ('packages/apps/SnapdragonCamera', 'src/com/android/camera/VideoModule.java', 'mirror-snapcam-video-bitrate.patch', 'Mirror 720p recording bitrate=')]
    temp = tempfile.mkdtemp(prefix='mirror-camera-source-')
    try:
        files = sorted(set(os.path.join(repo, relative) for repo, relative, unused, marker in changes))
        for relative in files:
            dest = os.path.join(temp, relative)
            if not os.path.isdir(os.path.dirname(dest)):
                os.makedirs(os.path.dirname(dest))
            shutil.copyfile(os.path.join(tree, relative), dest)
        for repo, relative, patch_name, marker in changes:
            target = os.path.join(temp, repo, relative)
            with io.open(target, encoding='utf-8') as f:
                text = f.read()
            if marker in text:
                continue
            with open(os.path.join(patches, patch_name), 'rb') as f:
                patch = f.read()
            command = ['patch', '--batch', '--forward']
            if patch_name == 'mirror-camera-raw-video.patch':
                command.append(target)
            else:
                command += ['-p1']
            process = subprocess.Popen(command, cwd=os.path.join(temp, repo), stdin=subprocess.PIPE)
            process.communicate(patch)
            if process.returncode:
                raise ValueError('Camera patch failed; original workspace files unchanged: ' + patch_name)
        # Commit source changes only after the complete staged patch chain passed.
        for relative in files:
            source, dest = os.path.join(temp, relative), os.path.join(tree, relative)
            with open(source, 'rb') as f:
                updated = f.read()
            with open(dest, 'rb') as f:
                original = f.read()
            if updated != original:
                shutil.copyfile(source, dest)
        shutil.copyfile(os.path.join(patches, 'mirror-video-pack.h'),
                        os.path.join(tree, 'frameworks/av/media/libstagefright/mirror-video-pack.h'))
    finally:
        shutil.rmtree(temp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tree', required=True)
    parser.add_argument('--patches', required=True)
    args = parser.parse_args()
    prepare(args.tree, args.patches)
    print('Camera HAL, software recording and upright UI patches prepared.')
