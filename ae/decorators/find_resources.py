import sys
from functools import wraps
from .. import resources
from ..shell import choose

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
