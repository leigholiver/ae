import sys
from functools import wraps
from .. import resources
from ..shell import choose
from InquirerPy import inquirer
from InquirerPy.base import Choice

# find resources by a single ident
def find_resources(arg_name, kinds=[], single=True):
    def _find_resources(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            res = resources.find_resources(kwargs[arg_name], kinds)

            if len(res) == 0:
                print("No resources found...")
                sys.exit(1)

            elif single:
                if len(res) == 1:
                    res = res[0]
                else:
                    res = choose({ r["Ident"]: r for r in res }, "Choose a resource")

            kwargs[arg_name] = res
            fn(*args, **kwargs)

        return wrapper
    return _find_resources

# find resources by multiple identifiers
def find_resources_multi(arg_name, kinds=[]):
    def _find_resources_multi(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            output = []
            for ident in kwargs[arg_name]:
                res = resources.find_resources(ident, kinds)
                if res:
                    output += res

            if len(output) == 0:
                print("No resources found...")
                sys.exit(1)

            elif len(output) > 1:
                choices = inquirer.checkbox(
                    message=f"""Choose resources...
Space to toggle, Enter to continue, Ctrl + C to abort...
""",
                    choices=[
                        Choice(r["Ident"], enabled=True)
                        for r in output
                    ],
                    validate=lambda result: len(result) >= 1,
                    transformer=lambda result: f"{len(result)} resource{'s' if len(result) > 1 else ''} selected",
                ).execute()
                output = [ r for r in output if r["Ident"] in choices]

            kwargs[arg_name] = output
            fn(*args, **kwargs)

        return wrapper
    return _find_resources_multi
