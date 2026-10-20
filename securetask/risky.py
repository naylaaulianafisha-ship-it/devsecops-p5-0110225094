import subprocess


def run_command(cmd):
    return subprocess.call(cmd, shell=True)
