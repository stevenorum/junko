#!/usr/bin/env python3

from junko.response_core import make_response
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

class HttpError(Exception):
    code = 500
    def __init__(self, body='Internal server error.', code=None, contenttype='text/html', headers={}):
        self.headers=headers
        if contenttype:
            headers["Content-Type"] = contenttype
        self.body = body
        self.code = code if code else self.code
        pass

    def response(self):
        return make_response(body=self.body, code=self.code, headers=self.headers)

class HttpInvalid(HttpError):
    code = 400

class HttpUnauthorized(HttpError):
    code = 401

class HttpForbidden(HttpError):
    code = 403

class HttpNotFound(HttpError):
    code = 404

class HttpBradbury(HttpError):
    code = 451

class HttpInternal(HttpError):
    code = 500

class HttpNotImplemented(HttpError):
    code = 501
