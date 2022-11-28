# ae
awscli extended

usage:
```bash
$ ae [-p/--profile <aws cli profile>] <command>
```

config file at `~/.ae/ae.yml`, or if using an aws cli profile `~/.ae/<aws cli profile>.yml`
see `ae.example.yml` for possible config file keys

ae will automatically pick up any accounts/assume roles that you have configured in your aws cli config file

custom commands are loaded in from `~/.ae/custom` in python package format, so either:

single file:
`~/.ae/custom.py`
```python
# import the ae command group
from ae import ae

# one or more sub-commands
@ae.command(
    name="hello-world",
    aliases=["hi"],
    help="prints hello world"
)
def hello_world():
    print("hello world from custom command")
```

package:
```python
# ~/.ae/custom/__init__.py
from hello_world import hello_world


# ~/.ae/custom/hello_world.py
from ae import ae

@ae.command(
    name="hello-world",
    aliases=["hi"],
    help="prints hello world"
)
def hello_world():
    print("hello world from custom command")
```
