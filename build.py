#! /usr/bin/env python3

from pathlib import Path
from string import Template

CODE_FILE = Path("pip-wtenv.py")
README_FILE = Path("README.md")
TEMPLATE_FILE = Path("README.template.md")


def main() -> None:
    template = Template(TEMPLATE_FILE.read_text())

    readme = template.substitute(
        code=CODE_FILE.read_text().strip(),
    )

    README_FILE.write_text(readme)


if __name__ == "__main__":
    main()
