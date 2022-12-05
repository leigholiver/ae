import os
import platform
import subprocess
import signal
from InquirerPy import inquirer

try:
    import readline
except:
    pass

from .aws import credentials

def run(command, env = {}, role=None, interactive=True):

    creds = credentials.credentials(role)

    env = {
        **os.environ,
        **env,
        **creds,
    }

    # Compatibility notes
    # - if `shell` is False on windows, things become non-interactive
    #   however, if `shell` is True on linux and macos, things break
    # - if `interactive` is true, we remove the SIGINT (ctrl+c) signal
    #   to prevent it quitting the python app rather than passing it through
    if interactive:
        _ = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        subprocess.call(
            command,
            env=env,
            shell=(platform.system() == "Windows")
        )

        signal.signal(signal.SIGINT, _)

    else:
        try:
            return subprocess.check_output(
                command,
                env=env,
            ).decode("utf-8")

        except subprocess.CalledProcessError as e:
            return f"Command exited with code {e.returncode}\n{e.output.decode('utf-8')}"

def choose(options, message):
    choice = inquirer.fuzzy(
        message=message,
        choices=options
    ).execute()
    return options[choice]
