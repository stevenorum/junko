#!/usr/bin/env python3

from junko.template_dispatchers import load_template

class HttpException(Exception):
    def __init__(self, template=None, code=None, params={}):
        self.template = template
        self.code = int(code)
        self.params = params
        pass

    @classmethod
    def from_code(cls, code, params={}):
        return cls(template="{code}.html".format(code=code), code=code, params=params)
    
    def render(self):
        return load_template(self.template, params=self.params, code=self.code)
    pass

def render_http_exceptions(function):
    def newfunc(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except HttpException as e:
            return e.render()
    return newfunc
