import readline


class AskException(Exception):
    pass


def question(text='', mods=[]):
    for mod in mods:
        if(mod[0]):
            text = mod[0](text)

    text = text + ' ' if text else ''

    while True:
        read = input(text)

        try:
            for mod in mods:
                if mod[1]:
                    read = mod[1](read)
        except AskException as e:
            print(e)
            continue
        else:
            return(read)


def required():
    def v(read):
        if not read:
            raise AskException('a value is required')
        else:
            return(read)

    return None, v


def default(value):
    def t(text):
        return '{} [{}]'.format(text, value)

    def v(read):
        return read if read else value

    return t, v


def yesno():
    def t(text):
        return '{} (y/n)'.format(text)

    def v(read):
        if read is 'y':
            return True
        elif read is 'n':
            return False
        else:
            raise AskException('answer (y)es or (n)o')

    return t, v


def number(minimum=None, maximum=None):
    def v(read):
        try:
            n = int(read)
        except ValueError:
            raise AskException('"{}" is not a number'.format(read))
        else:
            if minimum and n < minimum:
                raise AskException('{} is smaller than {}'.format(read, minimum))
            if maximum and n > maximum:
                raise AskException('{} is greater than {}'.format(read, maximum))

            return(n)

    return None, v


def option(options=[]):
    def t(text):
        return '\n'.join(['{:>4} {}'.format(i + 1, opt[1]) for i, opt in enumerate(options)]) + '\n{}'.format(text)

    def v(read):
        read = number(1, len(options))[1](read)
        return(options[read - 1][0])

    return t, v

readline.clear_history()
