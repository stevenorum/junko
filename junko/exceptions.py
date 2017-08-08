#!/usr/bin/env python3

class HttpException(Exception):
    def __init__(self, template=None, code=None, message=None):
        self.template = template
        self.code = int(code)
        self.message = message
        pass

    @classmethod
    def from_code(cls, code, message=None):
        return cls(tempalte="{code}.html".format(code=code), code=code, message=message)
    
    def render(self, *args, **kwargs):
        # TODO
        return None
    pass
