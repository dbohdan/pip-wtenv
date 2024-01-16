#! /usr/bin/env python3


def pip_wtenv(*args: str, name: str = "") -> None:
    """
    https://github.com/dbohdan/pip-wtenv

    Requires Python >= 3.6.

    Warning: this function restarts Python in a virtual environment.
    """

    from os import execl
    from pathlib import Path
    from subprocess import run
    from sys import argv, executable, platform
    from venv import create as create_venv

    me = Path(__file__)
    venv_dir = me.absolute().parent / f".venv.{name or me.name}"
    venv_python = venv_dir / (
        "Scripts/python.exe" if platform == "win32" else "bin/python"
    )

    if not venv_dir.exists():
        create_venv(venv_dir, with_pip=True)

    installed_marker = venv_dir / "installed"

    if not installed_marker.exists():
        run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        run([venv_python, "-m", "pip", "install", *args], check=True)
        installed_marker.touch()

    if not venv_python.samefile(executable):
        execl(venv_python, venv_python, *argv)


# A use example.

pip_wtenv("httpx", "rich<13")

import httpx
from rich import print

ip = httpx.get("https://icanhazip.com").text.strip()
print(f"Your public IP address is [bold]{ip}[/bold]")
