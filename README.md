# pip-wtenv

**pip-wtenv** lets a single-file Python script download and install its own dependencies
(without affecting the rest of the system).
To use it,
copy and paste the function `pip_wtenv` into your script and call it with the dependencies as arguments.

```python
#! /usr/bin/env python3


def pip_wtenv(*args: str, name: str = "", venv_parent: str = "") -> None:
    """
    See https://github.com/dbohdan/pip-wtenv.

    Requires Python >= 3.6 on POSIX systems and >= 3.8 on Windows.

    Warning: this function restarts Python in a virtual environment.
    """

    from os import execl
    from pathlib import Path
    from subprocess import run
    from sys import argv, base_prefix, platform, prefix
    from venv import create as create_venv

    me = Path(__file__)
    venv_dir = (
        Path(venv_parent).expanduser() if venv_parent else me.parent
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

    # If we are not running in a venv,
    # restart with `venv_python`.
    if prefix == base_prefix:
        execl(venv_python, venv_python, *argv)


# A use example.

pip_wtenv("httpx", "rich<13")

import httpx
from rich import print

ip = httpx.get("https://icanhazip.com").text.strip()
print(f"Your public IP address is [bold]{ip}[/bold]")
```

The source code above is developed in [`pip-wtenv.py`](pip-wtenv.py).

## Contents

- [Requirements](#requirements)
- [Comparison with pip\.wtf](#comparison-with-pipwtf)
- [Alternatives](#alternatives)
- [Usage](#usage)
- [License](#license)

## Requirements

pip-wtenv requires Python &ge; 3.6 on POSIX systems
and Python &ge; 3.8 on Windows.
[PyPy](https://github.com/pypy/pypy)
(Python 3.9 and 3.10)
is supported.

<details>
<summary><h3>Tested versions and OSs</h3></summary>

The following Python versions and operating systems have been tested
(all on x86-64):

- CPython:
  - 3.7, 3.12 on FreeBSD 14.0-RELEASE
  - 3.7—3.12 on macOS 12 (GitHub Actions)
  - 3.10 on NetBSD 9.3
  - 3.10 on OpenBSD 7.4
  - 3.6 on Ubuntu 22.04
  - 3.7—3.12 on Ubuntu 22.04 (GitHub Actions)
  - 3.8 on Windows 10
  - 3.9—3.12 on Windows Server 2022 (GitHub Actions)
- PyPy:
  - 7.3 (Python 3.9, 3.10) on macOS 12 (GitHub Actions)
  - 7.3 (Python 3.9, 3.10) on Ubuntu 22.04 (GitHub Actions)
  - 7.3 (Python 3.9, 3.10) on Windows Server 2022 (GitHub Actions)
</details>

## Comparison with pip.wtf

pip-wtenv is inspired by pip.wtf
([website](https://pip.wtf),
[repository](https://github.com/sabslikesobs/pip.wtf)).
It differs from pip.wtf in several ways,
namely:

- pip-wtenv lacks compatibility
  with Python 2.7 and early versions of Python 3.
- pip-wtenv installs dependencies in a
  [virtual environment](https://docs.python.org/3/library/venv.html) (venv).
- pip-wtenv works on Windows.
- pip-wtenv has a free/libre/open-source license.

## Alternatives

I wrote pip-wtenv out of curiosity.
My goal was to see what a pip.wtf counterpart that used virtual environments
would look like.
I think
the mechanism that manages the dependencies of single-file scripts should not
be duplicated in each script.
It is usually better to use a script runner
like one of the following
([my comparison](https://dbohdan.com/scripts-with-dependencies#python)):

- [fades](https://github.com/PyAr/fades)
  ([Repology](https://repology.org/project/fades/versions))&thinsp;&mdash;&thinsp;`sudo apt install fades` on Debian 10 or later and Ubuntu 16.04 or later
- [pip-run](https://github.com/jaraco/pip-run)
  ([Repology](https://repology.org/project/python:pip-run/versions))
- [pipx](https://github.com/pypa/pipx)
  ([Repology](https://repology.org/project/pipx/versions))&thinsp;&mdash;&thinsp;Version
  &ge; 1.4.2 has
  [PEP 723 compatibility](https://github.com/pypa/pipx/issues/1187).
  Choose pipx
  if you are not sure what to choose.

To use a script runner,
a user of the script needs to fulfill certain conditions.
They must have the runner installed on their machine.
If they don't,
they need the access and the technical skill to install it.
To cache packages and venvs and reduce startup time,
they need a user directory on persistent storage.
For beginners,
those who are not allowed to install software,
or those who have a USB flash drive but no persistent home directory,
a script that manages its own dependencies may be better.

A self-contained
[zipapp](https://docs.python.org/3/library/zipapp.html)
that depends only on Python
is potentially a good alternative for all users.
One way to produce a self-contained zipapp is with
[shiv](https://github.com/linkedin/shiv).
However,
shiv only packages binary dependencies
[for the current platform](https://github.com/linkedin/shiv/issues/26).

## Usage

Call `pip_wtenv(*args: str, name: str = "", venv_parent: str = "")` with your arguments to pip.
This will,
if necessary,
restart the script in a virtual environment.
Before restarting,
`pip_wtenv` will:

- Create the venv
  if the venv directory does not exist.
- Upgrade pip,
  then run it with the specified arguments
  if the venv directory does not contain a file called `ready`.

By default,
the venv directory for `foo.py` is named `.venv.foo.py`
and is created in the same directory as `foo.py`.
Pass `pip_wtenv` the argument `name` to use `f".venv.{name}"` instead.
To change the location of the venv directory,
pass the function a non-empty `venv_parent` argument;
for example,
`~/.cache/pip-wtenv/`.
To update the dependencies,
delete the venv directory before running the script.

Note that symlinks in the script path are not resolved.
This means that
if you invoke a script that uses pip-wtenv through a symlink,
the venv will be created in the directory with the symlink,
not its target file.
This allows for greater flexibility:

- You can use a symlink
  to run a script stored in a location
  where you have no write access.
- The same script can have different venvs
  with different dependencies
  in different places.

## License

This work is licensed under the terms of the
[BSD Zero Clause License](LICENSE.0BSD)
or,
alternatively,
under the terms of
[MIT No Attribution](LICENSE.MIT-0).
You may use this work under either of these licenses,
based on your preference.
Both licenses do not require attribution (credit).
