# Extending `ae`
`ae` is extendible by adding custom subcommands, either from local files or pip packages.

Commands are implemented using the [Click](https://click.palletsprojects.com/en/8.1.x/) package, as sub-commands of a primary `ae` command group by decorating the function with `@ae.command()`:

```python
from ae import ae

@ae.command(
    name="hello-world",
    aliases=["hi"],
    help="prints hello world"
)
def hello_world():
    print("hello world from custom command")
```

## The `custom` package
On startup, `ae` will try to load a Python package from `~/.ae/custom`.
This package defines or imports any additional commands to make available to `ae`.
As a Python package, there are two ways to set it up:
- A single file package in `~/.ae/custom.py`
- A directory at `~/.ae/custom/` containing an `__init__.py` file

## Command packages from Pip/Git
Packages of commands can be installed from any source and referenced in the `custom` package.
The reccommended method for creating a new command package is a [Poetry](https://python-poetry.org/docs/basic-usage/) project.

After declaring `ae` as a dependency of the project, the command group can be used in the same way as in local custom commands.
To register the command package (or specific subcommands) they must be imported in the users `custom` package.
