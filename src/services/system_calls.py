from subprocess import DEVNULL, STDOUT, check_call, check_output, run, CalledProcessError
from typing import Any


def exec(cmd: Any, verbose: bool = False) -> int:
    """
    Utility function to execute a command in bash and return the exit code.

    PARAMETERS
    ----------
    cmd : Any
        The command to execute.
    verbose : bool
        Whether to print the command and output.

    RETURNS
    -------
    int
        The exit code of the command.
    """
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
    """
    Utility function to execute a command in bash and return the STDOUT output.

    PARAMETERS
    ----------
    cmd : Any
        The command to execute.
    verbose : bool
        Whether to print the command and output.
    
    RETURNS
    -------
    str
        The output of the command.
    """
    try:
        return check_output(
            cmd,
            stderr=STDOUT,
        ).decode("UTF-8")
    except CalledProcessError as e:
        if verbose: print(e)


def powershell_exec_output(cmd: Any) -> str:
    """
    Utility function to execute a powershell command and return the STDOUT output.

    PARAMETERS
    ----------
    cmd : Any
        The command to execute.
    
    RETURNS
    -------
    str
        The output of the command.
    """
    completed = run(
        ["powershell", "-Command", cmd], capture_output=True,
    )
    return completed.stdout.decode("UTF-8")
