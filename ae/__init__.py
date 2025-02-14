from pathlib import Path
__home__ = str(Path.home())
__base_path__ = f"{__home__}/.ae"
__version__ = "0.0.4"

from . import config
from . import decorators
from . import shell
from . import parallel

from .ae import ae
from . import commands

# Import custom commands from ~/.ae/custom.py or ~/.ae/custom/
import sys
sys.path.insert(1, f"{__base_path__}")
try:
    import custom # type: ignore
except ModuleNotFoundError as e:
    pass
