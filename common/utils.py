"""Shared utilities for Snow Crash exploit scripts."""

import subprocess
import sys


def ssh_cmd(host, port, user, pwd, cmd):
    """Execute SSH command with sshpass."""
    try:
        result = subprocess.run(
            [
                "sshpass",
                "-p",
                pwd,
                "ssh",
                "-o",
                "StrictHostKeyChecking=no",
                "-p",
                str(port),
                f"{user}@{host}",
                cmd,
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode, result.stdout, result.stderr
    except:
        return -1, "", ""


def scp_cmd(host, port, user, pwd, remote_path, local_path):
    """Copy file from remote to local using scp."""
    try:
        result = subprocess.run(
            [
                "sshpass",
                "-p",
                pwd,
                "scp",
                "-o",
                "StrictHostKeyChecking=no",
                "-P",
                str(port),
                f"{user}@{host}:{remote_path}",
                local_path,
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except:
        return False


def read_flag(level_num):
    """Read flag from previous level."""
    try:
        with open(f"level{level_num:02d}/flag", "r") as f:
            return f.read().strip()
    except:
        print(f"[!] Could not read level{level_num:02d}/flag")
        sys.exit(1)


def save_flag(level_num, token):
    """Save token to flag file."""
    try:
        with open(f"level{level_num:02d}/flag", "w") as f:
            f.write(token)
        print(f"[+] Token saved to level{level_num:02d}/flag")
    except Exception as e:
        print(f"[!] Could not save token: {e}")
