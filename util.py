'''
This file contains basic utility function that can be used.
'''

MAX_NUM_CLIENTS = 10


def make_message(msg_type, msg_format, message=None):
    if msg_format == 2:
        return "%s" % (msg_type)
    if msg_format in [1, 3, 4]:
        return "%s %s" % (msg_type, message)
    return ""
