#! /usr/bin/env python3
# Copyright (c) 2024 D. Bohdan.
# License: choice of 0BSD or MIT-0.
# See the files `LICENSE.0BSD` and `LICENSE.MIT-0`.

import re
import shutil
import subprocess as sp
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path
from typing import Tuple, Union

PIP_WTENV_PY = Path(__file__).resolve().parent / "pip_wtenv.py"
PYTHON = sys.executable

EXAMPLE_OUTPUT_RE = r"IP address is \d+\.\d+\.\d+\.\d+"


def time_run(
    *args: Union[str, Path],
    cwd: Union[str, Path, None] = None,
) -> Tuple[sp.CompletedProcess, float]:
    start = time.time()
    completed = sp.run(
        args,
        check=False,
        cwd=cwd,
        stderr=sp.PIPE,
        stdout=sp.PIPE,
        universal_newlines=True,
    )
    duration = time.time() - start

    return completed, duration


class TestPipWtenv(unittest.TestCase):
    def test_args(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir_name:
            temp_dir = Path(temp_dir_name)
            shutil.copy2(PIP_WTENV_PY, temp_dir)

            script_file = temp_dir / "script.py"
            script = textwrap.dedent("""
                from pip_wtenv import pip_wtenv

                pip_wtenv("-qq", "httpx", name="foo", venv_parent_dir="venvs")

                import httpx
            """)
            script_file.write_text(script)

            completed, _ = time_run(PYTHON, script_file, cwd=temp_dir)
            assert completed.returncode == 0

            assert (temp_dir / "venvs/.venv.foo").is_dir()

    def test_run_example_repeatedly(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir_name:
            temp_dir = Path(temp_dir_name)
            shutil.copy2(PIP_WTENV_PY, temp_dir)

            durations = []
            for _ in range(3):
                completed, duration = time_run(PYTHON, temp_dir / PIP_WTENV_PY.name)
                assert completed.returncode == 0
                assert re.search(EXAMPLE_OUTPUT_RE, completed.stdout)

                durations.append(duration)

            for duration in durations[1:]:
                # A rough heuristic.
                # The difference is normally much greater.
                assert duration < durations[0] / 2


if __name__ == "__main__":
    unittest.main()
