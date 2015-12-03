from subprocess import check_call, check_output, CalledProcessError
from shlex import quote


def q(arg):
    return quote(arg)


def bash(cmd, *args):
    try:
        check_call(cmd.format(*args), shell=True)
    except CalledProcessError:
        return False
    else:
        return True


def stdout(cmd, *args):
    return check_output(cmd.format(*args), shell=True, universal_newlines=True)
