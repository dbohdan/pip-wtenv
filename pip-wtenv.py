#! /usr/bin/env python3


def pip_wtenv(*args: str, name: str = "") -> None:
    """
    Requires Python >= 3.6.

    Warning: this function restarts the script in a virtual environment.
    """

    from os import execl
    from pathlib import Path
    from subprocess import run
    from sys import argv, executable, platform
    from venv import create as create_venv

    me = Path(__file__)
    venv_dir = me.resolve().parent / f".venv.{name if name else me.name}"
    venv_python = venv_dir / (
        "Scripts/python.exe" if platform == "win32" else "bin/python"
    )

    if not venv_dir.exists():
        create_venv(venv_dir, with_pip=True)

    installed_marker = venv_dir / "installed"

    if not installed_marker.exists():
        run([venv_python, "-m", "pip", "install", "pip"], check=True)
        run([venv_python, "-m", "pip", "install", *args], check=True)
        installed_marker.touch()

    if not venv_python.samefile(executable):
        execl(venv_python, venv_python, *argv)


pip_wtenv("beautifulsoup4", "requests>=1,<2.26", "pyyaml==5.3.1")

import requests
import yaml
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get("https://pypi.org").content, "html.parser")
print(yaml.dump({"header": soup.find("h1").get_text()}))
