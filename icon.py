from os.path import dirname, abspath


def Path(icon: str) -> str:
    return '%s\\%s' % (dirname(abspath(__file__)), icon)
