import json

def format_return_msg(msg):
    format = '''{
                'message': {msg}
            }'''
    return format