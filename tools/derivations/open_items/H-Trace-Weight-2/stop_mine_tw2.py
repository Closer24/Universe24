"""Stops tw2's own pytest processes alone (a python whose working directory is tw2's scratch checkout apply/)."""
import os, signal, sys
H = os.path.dirname(os.path.abspath(__file__))
for pid in os.listdir("/proc"):
    if not pid.isdigit():
        continue
    try:
        exe = os.readlink(f"/proc/{pid}/exe"); cwd = os.readlink(f"/proc/{pid}/cwd")
        cmd = open(f"/proc/{pid}/cmdline", "rb").read().replace(b"\0", b" ").decode()
    except Exception:
        continue
    if "python" in exe and cwd == os.path.join(H, "apply") and "pytest" in cmd:
        os.kill(int(pid), signal.SIGTERM); print("stopped mine", pid)
