import os
import platform
import subprocess
import signal

try:
    import readline
except:
    pass

from .aws import session

def run(command, env = {}, role=None, interactive=True):

    creds = session.credentials(role)

    env = {
        **os.environ,
        **env,
        **creds,
    }

    # Odd compatibility note - if `shell`` is False on windows, things become non-interactive
    # however, if `shell`` is True on linux and macos, things break
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


# https://stackoverflow.com/a/64536882
def choose(options, name, name_field):
    if len(options) == 0:
        return None

    elif len(options) == 1:
        return list(options.values())[0]

    index = 0
    indexValidList = []
    print('Select a ' + name + ':')
    for optionName in options:
        index = index + 1
        indexValidList.extend([options[optionName]])
        print(str(index) + ') ' + optionName)
    inputValid = False
    while not inputValid:
        inputRaw = input(name.capitalize() + ': ')
        inputNo = int(inputRaw) - 1
        if inputNo > -1 and inputNo < len(indexValidList):
            selected = indexValidList[inputNo]
            print('Selected ' +  name + ': ' + selected[name_field])
            inputValid = True
            break
        else:
            print('Please select a valid ' + name + ' number')

    return selected
