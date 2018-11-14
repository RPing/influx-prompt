import sys

def string(input):
    if sys.version_info.major == 2:
        return unicode(input)

    return str(input)
