#! /usr/bin/env python3

def pip_wtenv(*args: str, name: str = "", venv_parent_dir: str = "") -> None:
    """
    Download and install dependencies in a virtual environment.
    See https://github.com/dbohdan/pip-wtenv.

    Warning: this function will restart Python
    if Python is not running in a venv.

    pip-wtenv requires Python >= 3.6 on POSIX systems
    and Python >= 3.8 on Windows.
    """

    from os import execl
    from pathlib import Path
    from subprocess import run
    from sys import argv, base_prefix, platform, prefix
    from venv import create as create_venv

    me = Path(__file__)
    venv_dir = (
        Path(venv_parent_dir).expanduser() if venv_parent_dir else me.parent
    ) / f".venv.{name or me.name}"

    if not venv_dir.exists():
        create_venv(venv_dir, with_pip=True)

    ready_marker = venv_dir / "ready"
    venv_python = venv_dir / (
        "Scripts/python.exe" if platform == "win32" else "bin/python"
    )

    if not ready_marker.exists():
        run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        run([venv_python, "-m", "pip", "install", *args], check=True)
        ready_marker.touch()

    # If we are not running in a venv, restart with `venv_python`.
    if prefix == base_prefix:
        execl(venv_python, venv_python, *argv)


# A use example.

if __name__ == "__main__":
    pip_wtenv("httpx", "rich<13")

    import httpx
    from rich import print

    ip = httpx.get("https://icanhazip.com").text.strip()
    print(f"Your public IP address is [bold]{ip}[/bold]")
