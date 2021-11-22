from subprocess import DEVNULL, STDOUT, check_call, check_output, run, CalledProcessError
from typing import Any


def exec(cmd: Any, verbose: bool = False) -> int:
    try:
        return check_call(
            cmd,
            stdout=None if verbose else DEVNULL,
            stderr=STDOUT,
            shell=True,
        )
    except CalledProcessError as e:
        if verbose: print(e)
    


def exec_output(cmd: Any, verbose: bool = False) -> str:
    try:
        return check_output(
            cmd,
            stderr=STDOUT,
        ).decode("UTF-8")
    except CalledProcessError as e:
        if verbose: print(e)



def powershell_exec_output(cmd: Any) -> str:
    """
    Utility function to run a command in powershell mode.
    """
    completed = run(
        ["powershell", "-Command", cmd], capture_output=True,
    )
    return completed.stdout.decode("UTF-8")
