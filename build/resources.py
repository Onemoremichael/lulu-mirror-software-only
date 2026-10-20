"""Shared, conservative limits for heavyweight Docker build entry points."""


def docker_build_command():
    # One name across both builders: Docker atomically rejects a concurrent run.
    # MemorySwap equals Memory, so the container gets no additional swap budget.
    return ['docker', 'run', '--rm', '--name', 'lulu-android-build',
            '--cpus', '2', '--memory', '4g', '--memory-swap', '4g',
            '--pids-limit', '1024', '--restart', 'no',
            '--platform', 'linux/amd64']
