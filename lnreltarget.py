import sys
import os.path


def lnreltarget(topath, frompath):
    topath = os.path.abspath(topath)
    frompath = os.path.dirname(os.path.abspath(frompath))
    return topath if os.path.commonprefix([topath, frompath]) == '/' else os.path.relpath(topath, frompath)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {} TO_PATH FROM_PATH'.format(sys.argv[0]), file=sys.stderr)
        sys.exit(100)

    print(lnreltarget(sys.argv[1], sys.argv[2]))
