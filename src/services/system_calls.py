from subprocess import DEVNULL, PIPE, STDOUT, check_call, check_output, run
from typing import Any


def exec(cmd: Any, verbose: bool = False) -> int:
    return check_call(
        cmd,
        stdout=DEVNULL if not verbose else None,
        stderr=STDOUT,
        shell=True,
    )


def exec_output(cmd: Any) -> str:
    return check_output(
        cmd,
        stderr=STDOUT,
    ).decode("UTF-8")


def powershell_exec_output(cmd: Any) -> str:
    """
    Utility function to run a command in powershell mode.
    """
    completed = run(
        ["powershell", "-Command", cmd], capture_output=True,
    )
    return completed.stdout.decode("UTF-8")
