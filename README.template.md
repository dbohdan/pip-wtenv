# pip-wtenv

**pip-wtenv** lets your single-file Python script download and install its own dependencies
(without affecting the rest of the system).
To use it,
copy and paste the function `pip_wtenv` into your script and call it with the dependencies as arguments.

```python
$code
```

The source code above is developed in [`pip-wtenv.py`](pip-wtenv.py).

pip-wtenv is inspired by pip.wtf
([website](https://pip.wtf),
[repository](https://github.com/sabslikesobs/pip.wtf)).
It differs from pip.wtf in several ways,
namely:

- pip-wtenv lacks Python 2.7 compatibility.
  It requires Python &ge; 3.6 on POSIX systems
  and Python &ge; 3.8 on Windows.
  (3.6 has been tested on Linux and 3.7 on FreeBSD.)
- pip-wtenv installs dependencies in a
  [virtual environment](https://docs.python.org/3/library/venv.html).
- pip-wtenv works on Windows.
- pip-wtenv has a free/open-source license.

## Should you use this?

I wrote pip-wtenv out of curiosity.
I wanted to see what a pip.wtf counterpart that used a venv would look like.
The mechanism that manages the dependencies of single-file scripts should not,
I think,
be duplicated in each script.
What I actually recommend using is one of the following script runners:

- [fades](https://github.com/PyAr/fades)
  ([Repology](https://repology.org/project/fades/versions))&thinsp;&mdash;&thinsp;`sudo apt install fades` on Debian 10 or later and Ubuntu 16.04 or later.
- [pip-run](https://github.com/jaraco/pip-run)
  ([Repology](https://repology.org/project/python:pip-run/versions)).
- [pipx](https://github.com/pypa/pipx) &ge; 1.4.2 for [PEP 723 compatibility](https://github.com/pypa/pipx/issues/1187)
  ([Repology](https://repology.org/project/pipx/versions)).

You can also package your script with its dependecies as a
[zipapp](https://docs.python.org/3/library/zipapp.html)
using
[shiv](https://github.com/linkedin/shiv).
However,
this only packages binary dependencies
[for the current platform](https://github.com/linkedin/shiv/issues/26).

## Usage

Call `pip_wtenv(*args: str, name: str = "")` with your arguments to pip.
This will,
if necessary,
restart the script in a virtual environment (venv).
Before restarting,
`pip_wtenv` will:

- Create the venv
  if the venv directory does not exist;
- Upgrade pip,
  then run it with the specified arguments
  if the venv directory does not contain a file called `ready`.

The venv directory for `foo.py` is named `.venv.foo.py` by default and is created in the same directory as `foo.py`.
Pass the argument `name` to use `f".venv.{name}"` instead.
To update the dependencies,
delete the venv directory before running the script.

## License

[0BSD](LICENSE).
This means attribution (credit) is not required.
