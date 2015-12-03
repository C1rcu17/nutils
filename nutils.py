import os
import sys


class NutilsException(Exception):
    pass


def convert_exceptions(fn):
    def inner(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except Exception as e:
            raise(NutilsException(str(e)))

    return inner


def abort_on_exception(fn):
    def inner(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except NutilsException as e:
            sys.exit('error: {}'.format(e))

    return inner


def require_root():
    if os.geteuid() != 0:
        raise NutilsException('permission denied')
