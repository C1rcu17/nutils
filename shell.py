def q(arg):
    from shlex import quote
    return quote(arg)


def bash(cmd, *args):
    from subprocess import check_call
    check_call(cmd.format(*args), shell=True)


def stdout(cmd, *args):
    from subprocess import check_output
    return check_output(cmd.format(*args), shell=True, universal_newlines=True)
